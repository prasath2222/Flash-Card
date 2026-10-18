import { initializeApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInAnonymously,
  signOut,
  onAuthStateChanged,
  type User
} from 'firebase/auth';
import {
  getFirestore,
  doc,
  getDocFromServer,
  setDoc,
  deleteDoc,
  onSnapshot,
  collection
} from 'firebase/firestore';
import firebaseConfig from '../firebase-applet-config.json';

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app, firebaseConfig.firestoreDatabaseId);
export const auth = getAuth(app);

// Connection test as required by Firebase skill
export async function testConnection() {
  try {
    await getDocFromServer(doc(db, 'test', 'connection'));
    console.log('[Firebase] Connection verified successfully.');
  } catch (error) {
    if (error instanceof Error && error.message.includes('the client is offline')) {
      console.warn('[Firebase] Offline or Firebase configuration pending.');
    }
  }
}
testConnection();

// Auto-check redirect result for mobile browsers returning from Google OAuth
getRedirectResult(auth)
  .then((result) => {
    if (result && result.user) {
      console.log('[Firebase] Mobile redirect login succeeded for:', result.user.email);
    }
  })
  .catch((error) => {
    console.warn('[Firebase] Mobile redirect check notice:', error);
  });

// Standard Error Handling for Firestore
export enum OperationType {
  CREATE = 'create',
  UPDATE = 'update',
  DELETE = 'delete',
  LIST = 'list',
  GET = 'get',
  WRITE = 'write',
}

export interface FirestoreErrorInfo {
  error: string;
  operationType: OperationType;
  path: string | null;
  authInfo: {
    userId?: string | null;
    email?: string | null;
    emailVerified?: boolean | null;
    isAnonymous?: boolean | null;
    tenantId?: string | null;
    providerInfo?: {
      providerId?: string | null;
      email?: string | null;
    }[];
  };
}

export function handleFirestoreError(error: unknown, operationType: OperationType, path: string | null): never {
  const errInfo: FirestoreErrorInfo = {
    error: error instanceof Error ? error.message : String(error),
    authInfo: {
      userId: auth.currentUser?.uid,
      email: auth.currentUser?.email,
      emailVerified: auth.currentUser?.emailVerified,
      isAnonymous: auth.currentUser?.isAnonymous,
      tenantId: auth.currentUser?.tenantId,
      providerInfo: auth.currentUser?.providerData?.map(provider => ({
        providerId: provider.providerId,
        email: provider.email,
      })) || []
    },
    operationType,
    path
  };
  console.error('Firestore Error: ', JSON.stringify(errInfo));
  throw new Error(JSON.stringify(errInfo));
}

// User Study State Interface
export interface RemoteStudyState {
  userId: string;
  email?: string;
  displayName?: string;
  lastActiveCardNum?: number;
  activeDeckId?: string;
  streakCount?: number;
  lastStudyDate?: string;
  learnedCardNums?: number[];
  deletedCardNums?: number[];
  updatedAt: string;
  createdAt?: string;
}

export interface CustomDeck {
  deckId: string;
  title: string;
  description?: string;
  cardCount: number;
  cards: any[];
  updatedAt: string;
  createdAt?: string;
}

// Global Sync Handlers
let unsubscribeProfile: (() => void) | null = null;
let unsubscribeShortcuts: (() => void) | null = null;
let unsubscribeDecks: (() => void) | null = null;
let isApplyingRemoteChange = false;

// Mobile-resilient Google Sign-In with automatic redirect fallback
export async function loginWithGoogle(): Promise<User> {
  const provider = new GoogleAuthProvider();
  provider.setCustomParameters({ prompt: 'select_account' });
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

  try {
    const res = await signInWithPopup(auth, provider);
    return res.user;
  } catch (err: any) {
    console.warn('[Firebase] signInWithPopup encountered error:', err);
    if (
      err &&
      (err.code === 'auth/popup-blocked' ||
        err.code === 'auth/cancelled-popup-request' ||
        isMobile)
    ) {
      try {
        await signInWithRedirect(auth, provider);
      } catch (redirErr) {
        console.error('[Firebase] signInWithRedirect also failed:', redirErr);
      }
    }
    throw err;
  }
}

// 100% Mobile-Safe Email / PIN Authentication (Never blocked by popup blockers or iframe restrictions)
export async function loginWithEmailOrPin(emailOrUser: string, passOrPin: string): Promise<User> {
  const cleanInput = (emailOrUser || '').trim().toLowerCase();
  const validEmail = cleanInput.includes('@')
    ? cleanInput
    : `${cleanInput.replace(/[^a-z0-9]/g, '') || 'learner'}@stellarsync.app`;
  
  const rawPass = (passOrPin || '').trim();
  const cleanPass = rawPass.length >= 6 ? rawPass : `${rawPass}123456`.slice(0, 10);

  try {
    const res = await signInWithEmailAndPassword(auth, validEmail, cleanPass);
    return res.user;
  } catch (err: any) {
    if (
      err &&
      (err.code === 'auth/user-not-found' ||
        err.code === 'auth/invalid-credential' ||
        err.code === 'auth/wrong-password')
    ) {
      try {
        // Automatically create account if it does not exist
        const newRes = await createUserWithEmailAndPassword(auth, validEmail, cleanPass);
        return newRes.user;
      } catch (createErr: any) {
        // If email already in use, re-throw original
        throw createErr;
      }
    }
    throw err;
  }
}

// Instant Anonymous / Guest Cloud Authentication
export async function loginAsGuest(): Promise<User> {
  const res = await signInAnonymously(auth);
  return res.user;
}

export async function logoutUser(): Promise<void> {
  if (unsubscribeProfile) { unsubscribeProfile(); unsubscribeProfile = null; }
  if (unsubscribeShortcuts) { unsubscribeShortcuts(); unsubscribeShortcuts = null; }
  if (unsubscribeDecks) { unsubscribeDecks(); unsubscribeDecks = null; }
  await signOut(auth);
}

// Push local changes to Firestore with strict schema whitelist matching firestore.rules
const ALLOWED_PROFILE_KEYS = [
  'userId', 'email', 'displayName', 'lastActiveCardNum',
  'activeDeckId', 'streakCount', 'lastStudyDate', 'learnedCardNums',
  'deletedCardNums', 'updatedAt', 'createdAt'
];

export async function pushStudyStateToCloud(partial: Partial<RemoteStudyState>) {
  if (isApplyingRemoteChange) return; // Prevent echo loops
  const user = auth.currentUser;
  if (!user) return;

  const docPath = `users/${user.uid}`;
  try {
    const rawPayload: Record<string, unknown> = {
      userId: user.uid,
      email: user.email || '',
      displayName: user.displayName || (user.isAnonymous ? 'Guest Learner' : 'Learner'),
      updatedAt: new Date().toISOString(),
      ...partial
    };

    // Filter strictly to allowed keys to prevent firestore rule rejection
    const cleanPayload: Record<string, unknown> = {};
    for (const key of ALLOWED_PROFILE_KEYS) {
      if (rawPayload[key] !== undefined) {
        cleanPayload[key] = rawPayload[key];
      }
    }

    await setDoc(doc(db, 'users', user.uid), cleanPayload, { merge: true });
  } catch (err) {
    handleFirestoreError(err, OperationType.WRITE, docPath);
  }
}

// Push custom shortcut edits to Firestore
export async function pushCustomShortcutToCloud(cardNum: number, es: string, hi: string) {
  if (isApplyingRemoteChange) return;
  const user = auth.currentUser;
  if (!user) return;

  const docPath = `users/${user.uid}/customShortcuts/${cardNum}`;
  try {
    await setDoc(doc(db, 'users', user.uid, 'customShortcuts', String(cardNum)), {
      userId: user.uid,
      cardNum,
      es,
      hi,
      updatedAt: new Date().toISOString()
    }, { merge: true });
  } catch (err) {
    handleFirestoreError(err, OperationType.WRITE, docPath);
  }
}

// Push custom deck to Firestore
export async function pushCustomDeckToCloud(deck: Omit<CustomDeck, 'updatedAt'>) {
  if (isApplyingRemoteChange) return;
  const user = auth.currentUser;
  if (!user) return;

  const docPath = `users/${user.uid}/decks/${deck.deckId}`;
  try {
    await setDoc(doc(db, 'users', user.uid, 'decks', deck.deckId), {
      userId: user.uid,
      deckId: deck.deckId,
      title: deck.title,
      description: deck.description || '',
      cardCount: deck.cardCount || (deck.cards ? deck.cards.length : 0),
      cards: deck.cards || [],
      updatedAt: new Date().toISOString(),
      createdAt: deck.createdAt || new Date().toISOString()
    }, { merge: true });
  } catch (err) {
    handleFirestoreError(err, OperationType.WRITE, docPath);
  }
}

// Delete custom deck from Firestore
export async function deleteCustomDeckFromCloud(deckId: string) {
  if (isApplyingRemoteChange) return;
  const user = auth.currentUser;
  if (!user) return;

  const docPath = `users/${user.uid}/decks/${deckId}`;
  try {
    await deleteDoc(doc(db, 'users', user.uid, 'decks', deckId));
  } catch (err) {
    handleFirestoreError(err, OperationType.DELETE, docPath);
  }
}

// ==========================================================
// UNIVERSAL CROSS-DEVICE SYNC CODE API (Zero popup blockers)
// ==========================================================
export async function saveToDeviceCloud(syncCode: string, payload: any): Promise<boolean> {
  try {
    const res = await fetch('/api/sync/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ syncCode, payload })
    });
    return res.ok;
  } catch (e) {
    console.warn('[Sync] Device cloud save failed:', e);
    return false;
  }
}

export async function loadFromDeviceCloud(syncCode: string): Promise<any> {
  try {
    const res = await fetch(`/api/sync/load?code=${encodeURIComponent(syncCode)}`);
    if (!res.ok) return null;
    const data = await res.json();
    return data && data.success ? data.payload : null;
  } catch (e) {
    console.warn('[Sync] Device cloud load failed:', e);
    return null;
  }
}

export async function pollDeviceCloud(syncCode: string, since: string): Promise<any> {
  try {
    const res = await fetch(`/api/sync/poll?code=${encodeURIComponent(syncCode)}&since=${encodeURIComponent(since)}`);
    if (!res.ok) return null;
    const data = await res.json();
    return data && data.hasUpdates ? data.payload : null;
  } catch (e) {
    return null;
  }
}

// Wire up window listeners for app integration
declare global {
  interface Window {
    firebaseSync?: {
      auth: typeof auth;
      loginWithGoogle: typeof loginWithGoogle;
      loginWithEmailOrPin: typeof loginWithEmailOrPin;
      loginAsGuest: typeof loginAsGuest;
      logoutUser: typeof logoutUser;
      pushStudyStateToCloud: typeof pushStudyStateToCloud;
      pushCustomShortcutToCloud: typeof pushCustomShortcutToCloud;
      pushCustomDeckToCloud: typeof pushCustomDeckToCloud;
      deleteCustomDeckFromCloud: typeof deleteCustomDeckFromCloud;
      saveToDeviceCloud: typeof saveToDeviceCloud;
      loadFromDeviceCloud: typeof loadFromDeviceCloud;
      pollDeviceCloud: typeof pollDeviceCloud;
      getCurrentUser: () => User | null;
      onAuthChange: (cb: (user: User | null) => void) => void;
      onRemoteStateChange: (cb: (data: RemoteStudyState) => void) => void;
      onRemoteShortcutsChange: (cb: (shortcuts: Record<number, { es: string; hi: string }>) => void) => void;
      onRemoteDecksChange: (cb: (decks: Record<string, CustomDeck>) => void) => void;
    };
  }
}

let remoteStateListeners: ((data: RemoteStudyState) => void)[] = [];
let remoteShortcutListeners: ((shortcuts: Record<number, { es: string; hi: string }>) => void)[] = [];
let remoteDeckListeners: ((decks: Record<string, CustomDeck>) => void)[] = [];

onAuthStateChanged(auth, (user) => {
  if (unsubscribeProfile) { unsubscribeProfile(); unsubscribeProfile = null; }
  if (unsubscribeShortcuts) { unsubscribeShortcuts(); unsubscribeShortcuts = null; }
  if (unsubscribeDecks) { unsubscribeDecks(); unsubscribeDecks = null; }

  if (user) {
    console.log('[Firebase] User authenticated:', user.email || user.uid);

    // Listen to profile changes in real-time
    const userDocPath = `users/${user.uid}`;
    unsubscribeProfile = onSnapshot(
      doc(db, 'users', user.uid),
      (snapshot) => {
        if (!snapshot.exists()) {
          const localLearned = JSON.parse(localStorage.getItem('vocab_learned_cards_v3') || '[]');
          const localDeleted = JSON.parse(localStorage.getItem('vocab_deleted_cards_v3') || '[]');
          const lastNum = Number(localStorage.getItem('vocab_last_card_v3') || 800);
          const streak = Number(localStorage.getItem('study_streak_count') || 1);
          const activeDeck = localStorage.getItem('active_deck_id_v1') || 'deck-800-1000';

          pushStudyStateToCloud({
            lastActiveCardNum: lastNum,
            activeDeckId: activeDeck,
            streakCount: streak,
            learnedCardNums: localLearned,
            deletedCardNums: localDeleted,
            createdAt: new Date().toISOString()
          });
          return;
        }

        const data = snapshot.data() as RemoteStudyState;
        isApplyingRemoteChange = true;
        try {
          remoteStateListeners.forEach(cb => cb(data));
        } finally {
          setTimeout(() => { isApplyingRemoteChange = false; }, 200);
        }
      },
      (error) => {
        handleFirestoreError(error, OperationType.GET, userDocPath);
      }
    );

    // Listen to custom shortcuts in real-time
    const shortcutsCollectionPath = `users/${user.uid}/customShortcuts`;
    unsubscribeShortcuts = onSnapshot(
      collection(db, 'users', user.uid, 'customShortcuts'),
      (snapshot) => {
        const shortcuts: Record<number, { es: string; hi: string }> = {};
        snapshot.forEach(docSnap => {
          const d = docSnap.data();
          if (d.cardNum) {
            shortcuts[Number(d.cardNum)] = { es: d.es || '', hi: d.hi || '' };
          }
        });

        isApplyingRemoteChange = true;
        try {
          remoteShortcutListeners.forEach(cb => cb(shortcuts));
        } finally {
          setTimeout(() => { isApplyingRemoteChange = false; }, 200);
        }
      },
      (error) => {
        handleFirestoreError(error, OperationType.GET, shortcutsCollectionPath);
      }
    );

    // Listen to custom uploaded decks in real-time
    const decksCollectionPath = `users/${user.uid}/decks`;
    unsubscribeDecks = onSnapshot(
      collection(db, 'users', user.uid, 'decks'),
      (snapshot) => {
        const decks: Record<string, CustomDeck> = {};
        snapshot.forEach(docSnap => {
          const d = docSnap.data() as CustomDeck;
          if (d.deckId) {
            decks[d.deckId] = d;
          }
        });

        isApplyingRemoteChange = true;
        try {
          remoteDeckListeners.forEach(cb => cb(decks));
        } finally {
          setTimeout(() => { isApplyingRemoteChange = false; }, 200);
        }
      },
      (error) => {
        handleFirestoreError(error, OperationType.GET, decksCollectionPath);
      }
    );
  } else {
    console.log('[Firebase] Signed out.');
  }
});

// Attach to window for seamless interaction with index.html
window.firebaseSync = {
  auth,
  loginWithGoogle,
  loginWithEmailOrPin,
  loginAsGuest,
  logoutUser,
  pushStudyStateToCloud,
  pushCustomShortcutToCloud,
  pushCustomDeckToCloud,
  deleteCustomDeckFromCloud,
  saveToDeviceCloud,
  loadFromDeviceCloud,
  pollDeviceCloud,
  getCurrentUser: () => auth.currentUser,
  onAuthChange: (cb) => {
    onAuthStateChanged(auth, cb);
  },
  onRemoteStateChange: (cb) => {
    remoteStateListeners.push(cb);
  },
  onRemoteShortcutsChange: (cb) => {
    remoteShortcutListeners.push(cb);
  },
  onRemoteDecksChange: (cb) => {
    remoteDeckListeners.push(cb);
  }
};
