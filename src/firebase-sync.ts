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

// Purge all legacy localStorage keys that could hold old hardcoded emails
try {
  localStorage.removeItem('active_cloud_user_email');
  localStorage.removeItem('stellar_account_email_v1');
  localStorage.removeItem('stellar_account_name_v1');
  localStorage.removeItem('vocab_google_session_v2');
} catch (e) {}

const PROD_AUTH_STORAGE_KEY = 'vocab_auth_session_v3';

let currentUser: User | null = null;
let sessionEmail = '';
let sessionDisplayName = '';

try {
  const saved = JSON.parse(localStorage.getItem(PROD_AUTH_STORAGE_KEY) || 'null');
  if (saved && typeof saved.email === 'string' && saved.email.includes('@')) {
    sessionEmail = saved.email.trim().toLowerCase();
    sessionDisplayName = saved.displayName || sessionEmail.split('@')[0];
  }
} catch (e) {}

let unsubscribeStudyState: (() => void) | null = null;
let isApplyingRemoteUpdate = false;

const authChangeCallbacks: Array<(user: any) => void> = [];
const remoteStateCallbacks: Array<(data: any) => void> = [];
const remoteShortcutsCallbacks: Array<(shortcuts: Record<string, any>) => void> = [];

function emailToDocId(email: string): string {
  return `acct_${email.trim().toLowerCase().replace(/[^a-z0-9]/g, '_')}`.slice(0, 120);
}

export function onAuthChange(cb: (user: any) => void) {
  if (typeof cb === 'function') {
    authChangeCallbacks.push(cb);
    if (currentUser && currentUser.email) {
      cb(currentUser);
    } else if (sessionEmail && sessionEmail.includes('@')) {
      cb({
        uid: emailToDocId(sessionEmail),
        email: sessionEmail,
        displayName: sessionDisplayName || sessionEmail.split('@')[0]
      });
    } else {
      cb(null);
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

export function getActiveAccountEmail(): string {
  if (currentUser && currentUser.email) {
    return currentUser.email.trim().toLowerCase();
  }
  if (sessionEmail && sessionEmail.includes('@')) {
    return sessionEmail.trim().toLowerCase();
  }
  return '';
}

function attachStudyStateListener(email: string) {
  if (unsubscribeStudyState) {
    unsubscribeStudyState();
    unsubscribeStudyState = null;
  }
  const clean = String(email || '').trim().toLowerCase();
  if (!clean || !clean.includes('@')) return;

  const docId = emailToDocId(clean);
  const stateDocRef = doc(db, 'study_state', docId);

  unsubscribeStudyState = onSnapshot(
    stateDocRef,
    (docSnap) => {
      if (!docSnap.exists()) return;
      const raw = docSnap.data();
      const payload = raw?.payload && typeof raw.payload === 'object' ? raw.payload : raw;
      if (!payload) return;

      isApplyingRemoteUpdate = true;
      remoteStateCallbacks.forEach((cb) => {
        try {
          cb({ ...payload, updatedAt: raw.updatedAt || payload.updatedAt });
        } catch (e) {}
      });
      setTimeout(() => {
        isApplyingRemoteUpdate = false;
      }, 250);
    },
    (error) => {
      handleFirestoreError(error, OperationType.GET, `study_state/${docId}`);
    }
  );
}

export function setSessionEmail(email: string, displayName?: string) {
  const clean = String(email || '').trim().toLowerCase();
  if (clean && clean.includes('@')) {
    sessionEmail = clean;
    sessionDisplayName = (displayName || clean.split('@')[0]).trim();
    try {
      localStorage.setItem(
        PROD_AUTH_STORAGE_KEY,
        JSON.stringify({
          uid: emailToDocId(clean),
          email: clean,
          displayName: sessionDisplayName
        })
      );
    } catch (e) {}
    attachStudyStateListener(clean);
  } else {
    sessionEmail = '';
    sessionDisplayName = '';
    if (unsubscribeStudyState) {
      unsubscribeStudyState();
      unsubscribeStudyState = null;
    }
    try {
      localStorage.removeItem(PROD_AUTH_STORAGE_KEY);
    } catch (e) {}
  }
}

export async function saveAccountStateToFirestore(email: string, payload: any): Promise<boolean> {
  const clean = String(email || '').trim().toLowerCase();
  if (!clean || !clean.includes('@') || !payload) return false;
  const docId = emailToDocId(clean);
  const path = `study_state/${docId}`;
  try {
    const updatedAt = payload.updatedAt || new Date().toISOString();
    await setDoc(doc(db, 'study_state', docId), {
      email: clean,
      updatedAt,
      payload: {
        ...payload,
        email: clean,
        updatedAt
      }
    });
    return true;
  } catch (error) {
    handleFirestoreError(error, OperationType.WRITE, path);
    return false;
  }
}

export async function loadAccountStateFromFirestore(
  email: string
): Promise<{ exists: boolean; updatedAt: string; payload: any } | null> {
  const clean = String(email || '').trim().toLowerCase();
  if (!clean || !clean.includes('@')) return null;
  const docId = emailToDocId(clean);
  const path = `study_state/${docId}`;
  try {
    const snap = await getDoc(doc(db, 'study_state', docId));
    if (!snap.exists()) {
      return { exists: false, updatedAt: '', payload: null };
    }
    const data = snap.data();
    const payload = data?.payload && typeof data.payload === 'object' ? data.payload : data;
    return {
      exists: true,
      updatedAt: data?.updatedAt || payload?.updatedAt || new Date().toISOString(),
      payload
    };
  } catch (error) {
    handleFirestoreError(error, OperationType.GET, path);
    return null;
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
    if (result && result.user && result.user.email) {
      const cleanEmail = result.user.email.trim().toLowerCase();
      const displayName = result.user.displayName || cleanEmail.split('@')[0];
      setSessionEmail(cleanEmail, displayName);
      notifyAuthCallbacks(result.user);
      return result.user;
    }
  } catch (error: any) {
    // Never fall back to any hardcoded email!
    // Only use an email if the user explicitly typed one into the sign-in input field.
    const inputModal = document.getElementById('input-modal-email') as HTMLInputElement | null;
    const inputSettings = document.getElementById('input-account-email') as HTMLInputElement | null;
    const typedEmail = (inputModal?.value || inputSettings?.value || '').trim().toLowerCase();
    if (typedEmail && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(typedEmail)) {
      const displayName = typedEmail.split('@')[0];
      setSessionEmail(typedEmail, displayName);
      const virtualUser = {
        uid: emailToDocId(typedEmail),
        email: typedEmail,
        displayName
      };
      notifyAuthCallbacks(virtualUser);
      return virtualUser;
    }
    throw error;
  } finally {
    isSigningIn = false;
  }
  return null;
}

export const loginWithGoogle = signInWithGoogle;

export async function signOutUser() {
  setSessionEmail('', '');
  currentUser = null;
  try {
    if (auth.currentUser) {
      await signOut(auth);
    }
  } catch (error) {}
  notifyAuthCallbacks(null);
}

export const logoutUser = signOutUser;

onAuthStateChanged(auth, async (user) => {
  currentUser = user;
  if (user && user.email) {
    const cleanEmail = user.email.trim().toLowerCase();
    const displayName = user.displayName || cleanEmail.split('@')[0];
    setSessionEmail(cleanEmail, displayName);
    notifyAuthCallbacks(user);
  } else if (sessionEmail && sessionEmail.includes('@')) {
    attachStudyStateListener(sessionEmail);
    notifyAuthCallbacks({
      uid: emailToDocId(sessionEmail),
      email: sessionEmail,
      displayName: sessionDisplayName || sessionEmail.split('@')[0]
    });
  } else {
    notifyAuthCallbacks(null);
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
  getActiveAccountEmail,
  saveAccountStateToFirestore,
  loadAccountStateFromFirestore,
  onAuthChange,
  onRemoteStateChange,
  onRemoteShortcutsChange,
  pushStudyStateToCloud,
  pushCustomShortcutToCloud,
  pushCustomDeckToCloud,
  deleteCustomDeckFromCloud,
  getCurrentUser: () => currentUser
};
