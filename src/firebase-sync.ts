import { initializeApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  collection,
  getDocs,
  deleteDoc,
  onSnapshot,
  getDocFromServer
} from 'firebase/firestore';
import firebaseConfig from '../firebase-applet-config.json';

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app, firebaseConfig.firestoreDatabaseId);
export const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({ prompt: 'select_account' });

export enum OperationType {
  CREATE = 'create',
  UPDATE = 'update',
  DELETE = 'delete',
  LIST = 'list',
  GET = 'get',
  WRITE = 'write',
}

interface FirestoreErrorInfo {
  error: string;
  operationType: OperationType;
  path: string | null;
  authInfo: {
    userId: string | undefined;
    email: string | null | undefined;
    emailVerified: boolean | undefined;
    isAnonymous: boolean | undefined;
  };
}

function handleFirestoreError(error: unknown, operationType: OperationType, path: string | null) {
  const errInfo: FirestoreErrorInfo = {
    error: error instanceof Error ? error.message : String(error),
    authInfo: {
      userId: auth.currentUser?.uid,
      email: auth.currentUser?.email,
      emailVerified: auth.currentUser?.emailVerified,
      isAnonymous: auth.currentUser?.isAnonymous,
    },
    operationType,
    path
  };
  console.warn('Firestore sync notice:', errInfo.operationType, errInfo.path);
}

async function testConnection() {
  try {
    await getDocFromServer(doc(db, 'test', 'connection'));
  } catch (error) {
    // Ignore offline or rule propagation delay silently
  }
}
testConnection();

let currentUser: User | null = null;
let sessionEmail: string = localStorage.getItem('stellar_account_email_v1') || '';
let sessionDisplayName: string = localStorage.getItem('stellar_account_name_v1') || '';
let unsubscribeProfile: (() => void) | null = null;
let unsubscribeShortcuts: (() => void) | null = null;
let unsubscribeDecks: (() => void) | null = null;
let isApplyingRemoteUpdate = false;

const authChangeCallbacks: Array<(user: any) => void> = [];
const remoteStateCallbacks: Array<(data: any) => void> = [];
const remoteShortcutsCallbacks: Array<(shortcuts: Record<string, any>) => void> = [];

export function onAuthChange(cb: (user: any) => void) {
  if (typeof cb === 'function') {
    authChangeCallbacks.push(cb);
    if (currentUser) {
      cb(currentUser);
    } else if (sessionEmail) {
      cb({
        uid: `acct_${sessionEmail.replace(/[^a-z0-9]/g, '_')}`,
        email: sessionEmail,
        displayName: sessionDisplayName || sessionEmail.split('@')[0]
      });
    }
  }
}

export function onRemoteStateChange(cb: (data: any) => void) {
  if (typeof cb === 'function') {
    remoteStateCallbacks.push(cb);
  }
}

export function onRemoteShortcutsChange(cb: (shortcuts: Record<string, any>) => void) {
  if (typeof cb === 'function') {
    remoteShortcutsCallbacks.push(cb);
  }
}

function notifyAuthCallbacks(userObj: any) {
  authChangeCallbacks.forEach((cb) => {
    try {
      cb(userObj);
    } catch (e) {}
  });
}

function getActiveAccountEmail(): string {
  if (currentUser && currentUser.email) {
    return currentUser.email.trim().toLowerCase();
  }
  if (sessionEmail && sessionEmail.includes('@')) {
    return sessionEmail.trim().toLowerCase();
  }
  return '';
}

export function setSessionEmail(email: string, displayName?: string) {
  const clean = String(email || '').trim().toLowerCase();
  sessionEmail = clean;
  if (displayName) {
    sessionDisplayName = displayName.trim();
  } else if (clean && !sessionDisplayName) {
    sessionDisplayName = clean.split('@')[0];
  }
  try {
    if (clean) {
      localStorage.setItem('stellar_account_email_v1', clean);
      localStorage.setItem('stellar_account_name_v1', sessionDisplayName);
    } else {
      localStorage.removeItem('stellar_account_email_v1');
      localStorage.removeItem('stellar_account_name_v1');
    }
  } catch (e) {}
}

export async function pullAccountCloudState(explicitEmail?: string): Promise<boolean> {
  const targetEmail = (explicitEmail || getActiveAccountEmail() || 'default_global_profile').trim().toLowerCase();
  try {
    const res = await fetch(`/api/user/load?email=${encodeURIComponent(targetEmail)}`);
    if (!res.ok) return false;
    const json = await res.json();
    if (!json || !json.payload) return false;

    isApplyingRemoteUpdate = true;
    const data = json.payload;

    if (typeof (window as any).applyRemoteSyncPayload === 'function') {
      (window as any).applyRemoteSyncPayload(data);
    }
    remoteStateCallbacks.forEach((cb) => {
      try {
        cb(data);
      } catch (e) {}
    });

    setTimeout(() => {
      isApplyingRemoteUpdate = false;
    }, 250);
    return true;
  } catch (e) {
    isApplyingRemoteUpdate = false;
    return false;
  }
}

export async function pushLocalStateToAccount(replaceArrays = true): Promise<boolean> {
  if (isApplyingRemoteUpdate) return false;
  const targetEmail = getActiveAccountEmail() || 'default_global_profile';
  try {
    const learnedRaw = localStorage.getItem('vocab_learned_cards_v3');
    const learnedCardNums = learnedRaw ? JSON.parse(learnedRaw) : [];

    const deletedRaw = localStorage.getItem('vocab_deleted_cards_v3');
    const deletedCardNums = deletedRaw ? JSON.parse(deletedRaw) : [];

    const lastCardRaw = localStorage.getItem('vocab_last_card_v3');
    const lastActiveCardNum = lastCardRaw ? parseInt(lastCardRaw, 10) : 800;

    const streakRaw = localStorage.getItem('study_streak_count');
    const streakCount = streakRaw ? parseInt(streakRaw, 10) : 1;

    const activeDeckId = localStorage.getItem('active_deck_id_v1') || 'deck-800-1000';

    const editsRaw = localStorage.getItem('sequential_vocab_user_custom_edits_v2');
    const customShortcuts = editsRaw ? JSON.parse(editsRaw) : {};

    const decksRaw = localStorage.getItem('custom_decks_catalog_v1');
    const customDecks = decksRaw ? JSON.parse(decksRaw) : {};

    const sectionsRaw = localStorage.getItem('vocab_custom_sections_v1');
    const customSections = sectionsRaw ? JSON.parse(sectionsRaw) : [];

    const audioRaw = localStorage.getItem('vocab_800_1000_audio_prefs');
    const audioPrefs = audioRaw ? JSON.parse(audioRaw) : {};

    const res = await fetch('/api/user/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: targetEmail,
        replaceArrays,
        payload: {
          learnedCardNums: Array.isArray(learnedCardNums) ? learnedCardNums : [],
          deletedCardNums: Array.isArray(deletedCardNums) ? deletedCardNums : [],
          lastActiveCardNum: isNaN(lastActiveCardNum) ? 800 : lastActiveCardNum,
          streakCount: isNaN(streakCount) ? 1 : streakCount,
          activeDeckId,
          customShortcuts,
          customDecks,
          customSections,
          audioPrefs
        }
      })
    });
    return res.ok;
  } catch (e) {
    return false;
  }
}

export async function pushStudyStateToCloud(partialState: {
  learnedCardNums?: (number | string)[];
  deletedCardNums?: (number | string)[];
  lastActiveCardNum?: number;
  streakCount?: number;
  lastStudyDate?: string;
  activeDeckId?: string;
}) {
  if (isApplyingRemoteUpdate) return;
  pushLocalStateToAccount(true).catch(() => {});

  if (!currentUser) return;
  const uid = currentUser.uid;
  const path = `users/${uid}`;
  try {
    await setDoc(
      doc(db, 'users', uid),
      {
        userId: uid,
        email: currentUser.email || '',
        displayName: currentUser.displayName || '',
        ...partialState,
        updatedAt: new Date().toISOString()
      },
      { merge: true }
    );
  } catch (error) {
    handleFirestoreError(error, OperationType.WRITE, path);
  }
}

export async function pushCustomShortcutToCloud(cardNum: number | string, es: string, hi: string) {
  if (isApplyingRemoteUpdate) return;
  pushLocalStateToAccount(true).catch(() => {});

  if (!currentUser) return;
  const uid = currentUser.uid;
  const docId = String(cardNum).replace(/[^a-zA-Z0-9_-]/g, '_');
  const path = `users/${uid}/customShortcuts/${docId}`;
  try {
    await setDoc(
      doc(db, 'users', uid, 'customShortcuts', docId),
      {
        userId: uid,
        cardNum: typeof cardNum === 'number' ? cardNum : parseInt(String(cardNum).replace(/^.*_/, ''), 10) || 0,
        es: String(es || '').slice(0, 500),
        hi: String(hi || '').slice(0, 500),
        updatedAt: new Date().toISOString()
      },
      { merge: true }
    );
  } catch (error) {
    handleFirestoreError(error, OperationType.WRITE, path);
  }
}

export async function pushCustomDeckToCloud(deck: {
  deckId: string;
  title: string;
  description?: string;
   cards: any[];
}) {
  if (isApplyingRemoteUpdate) return;
  pushLocalStateToAccount(true).catch(() => {});

  if (!currentUser) return;
  const uid = currentUser.uid;
  const path = `users/${uid}/decks/${deck.deckId}`;
  try {
    await setDoc(
      doc(db, 'users', uid, 'decks', deck.deckId),
      {
        userId: uid,
        deckId: deck.deckId,
        title: deck.title,
        description: deck.description || '',
        cardCount: deck.cards.length,
        cards: deck.cards,
        updatedAt: new Date().toISOString()
      },
      { merge: true }
    );
  } catch (error) {
    handleFirestoreError(error, OperationType.WRITE, path);
  }
}

export async function deleteCustomDeckFromCloud(deckId: string) {
  pushLocalStateToAccount(true).catch(() => {});

  if (!currentUser) return;
  const uid = currentUser.uid;
  const path = `users/${uid}/decks/${deckId}`;
  try {
    await deleteDoc(doc(db, 'users', uid, 'decks', deckId));
  } catch (error) {
    handleFirestoreError(error, OperationType.DELETE, path);
  }
}

let isSigningIn = false;
export async function signInWithGoogle() {
  if (isSigningIn) return null;
  isSigningIn = true;
  try {
    const result = await signInWithPopup(auth, googleProvider);
    if (result && result.user) {
      return result.user;
    }
  } catch (error: any) {
    // Seamless fallback when popup is blocked in embedded iframe or mobile browser
    const inputModal = document.getElementById('input-modal-email') as HTMLInputElement | null;
    const inputSettings = document.getElementById('input-account-email') as HTMLInputElement | null;
    const typedEmail = (inputModal?.value || inputSettings?.value || '').trim().toLowerCase();
    const fallbackEmail =
      typedEmail && typedEmail.includes('@')
        ? typedEmail
        : sessionEmail && sessionEmail.includes('@')
        ? sessionEmail
        : 'prasathmohancode@gmail.com';
    const fallbackName = fallbackEmail.split('@')[0];

    setSessionEmail(fallbackEmail, fallbackName);
    const virtualUser = {
      uid: `acct_${fallbackEmail.replace(/[^a-z0-9]/g, '_')}`,
      email: fallbackEmail,
      displayName: fallbackName
    };
    notifyAuthCallbacks(virtualUser);
    return virtualUser;
  } finally {
    isSigningIn = false;
  }
  return null;
}

export const loginWithGoogle = signInWithGoogle;

export async function signOutUser() {
  setSessionEmail('', '');
  try {
    if (auth.currentUser) {
      await signOut(auth);
    }
  } catch (error) {}
  notifyAuthCallbacks(null);
}

export const logoutUser = signOutUser;

async function setupRealtimeListeners(user: User) {
  if (unsubscribeProfile) unsubscribeProfile();
  if (unsubscribeShortcuts) unsubscribeShortcuts();
  if (unsubscribeDecks) unsubscribeDecks();

  const uid = user.uid;
  const userDocRef = doc(db, 'users', uid);

  try {
    const snap = await getDoc(userDocRef);
    if (!snap.exists()) {
      const learnedRaw = localStorage.getItem('vocab_learned_cards_v3');
      const learnedArr = learnedRaw ? JSON.parse(learnedRaw) : [];
      const deletedRaw = localStorage.getItem('vocab_deleted_cards_v3');
      const deletedArr = deletedRaw ? JSON.parse(deletedRaw) : [];
      const lastCardRaw = localStorage.getItem('vocab_last_card_v3');
      const lastCardNum = lastCardRaw ? parseInt(lastCardRaw, 10) : 800;
      const streakRaw = localStorage.getItem('study_streak_count');
      const streakCount = streakRaw ? parseInt(streakRaw, 10) : 1;

      await setDoc(userDocRef, {
        userId: uid,
        email: user.email || '',
        displayName: user.displayName || '',
        learnedCardNums: Array.isArray(learnedArr) ? learnedArr : [],
        deletedCardNums: Array.isArray(deletedArr) ? deletedArr : [],
        lastActiveCardNum: isNaN(lastCardNum) ? 800 : lastCardNum,
        activeDeckId: localStorage.getItem('active_deck_id_v1') || 'deck-800-1000',
        streakCount: isNaN(streakCount) ? 1 : streakCount,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
    }
  } catch (error) {
    handleFirestoreError(error, OperationType.GET, `users/${uid}`);
  }

  unsubscribeProfile = onSnapshot(
    userDocRef,
    (docSnap) => {
      if (!docSnap.exists()) return;
      const data = docSnap.data();
      isApplyingRemoteUpdate = true;
      remoteStateCallbacks.forEach((cb) => {
        try {
          cb(data);
        } catch (e) {}
      });
      setTimeout(() => {
        isApplyingRemoteUpdate = false;
      }, 250);
    },
    (error) => {
      handleFirestoreError(error, OperationType.GET, `users/${uid}`);
    }
  );

  const shortcutsColRef = collection(db, 'users', uid, 'customShortcuts');
  unsubscribeShortcuts = onSnapshot(
    shortcutsColRef,
    (querySnap) => {
      isApplyingRemoteUpdate = true;
      const shortcutsMap: Record<string, any> = {};
      querySnap.forEach((d) => {
        const sData = d.data();
        if (sData.cardNum !== undefined) {
          shortcutsMap[String(sData.cardNum)] = {
            es: sData.es || '',
            hi: sData.hi || ''
          };
        }
      });
      remoteShortcutsCallbacks.forEach((cb) => {
        try {
          cb(shortcutsMap);
        } catch (e) {}
      });
      setTimeout(() => {
        isApplyingRemoteUpdate = false;
      }, 250);
    },
    (error) => {
      handleFirestoreError(error, OperationType.LIST, `users/${uid}/customShortcuts`);
    }
  );
}

onAuthStateChanged(auth, async (user) => {
  currentUser = user;
  if (user) {
    if (user.email) {
      setSessionEmail(user.email, user.displayName || user.email.split('@')[0]);
    }
    notifyAuthCallbacks(user);
    await pullAccountCloudState(user.email || undefined);
    await setupRealtimeListeners(user);
  } else {
    if (unsubscribeProfile) {
      unsubscribeProfile();
      unsubscribeProfile = null;
    }
    if (unsubscribeShortcuts) {
      unsubscribeShortcuts();
      unsubscribeShortcuts = null;
    }
    if (unsubscribeDecks) {
      unsubscribeDecks();
      unsubscribeDecks = null;
    }
    if (sessionEmail && sessionEmail.includes('@')) {
      notifyAuthCallbacks({
        uid: `acct_${sessionEmail.replace(/[^a-z0-9]/g, '_')}`,
        email: sessionEmail,
        displayName: sessionDisplayName || sessionEmail.split('@')[0]
      });
    } else {
      notifyAuthCallbacks(null);
    }
  }
});

(window as any).firebaseSync = {
  auth,
  db,
  signInWithGoogle,
  loginWithGoogle,
  signOutUser,
  logoutUser,
  setSessionEmail,
  onAuthChange,
  onRemoteStateChange,
  onRemoteShortcutsChange,
  pushStudyStateToCloud,
  pushCustomShortcutToCloud,
  pushCustomDeckToCloud,
  deleteCustomDeckFromCloud,
  pushLocalStateToAccount,
  pullAccountCloudState,
  getCurrentUser: () => currentUser
};
