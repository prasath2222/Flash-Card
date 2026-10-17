import { initializeApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  type User
} from 'firebase/auth';
import {
  getFirestore,
  doc,
  getDocFromServer,
  setDoc,
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
  streakCount?: number;
  lastStudyDate?: string;
  learnedCardNums?: number[];
  deletedCardNums?: number[];
  updatedAt: string;
  createdAt?: string;
}

// Global Sync Handlers
let unsubscribeProfile: (() => void) | null = null;
let unsubscribeShortcuts: (() => void) | null = null;
let isApplyingRemoteChange = false;

export async function loginWithGoogle(): Promise<User> {
  const provider = new GoogleAuthProvider();
  const res = await signInWithPopup(auth, provider);
  return res.user;
}

export async function logoutUser(): Promise<void> {
  if (unsubscribeProfile) { unsubscribeProfile(); unsubscribeProfile = null; }
  if (unsubscribeShortcuts) { unsubscribeShortcuts(); unsubscribeShortcuts = null; }
  await signOut(auth);
}

// Push local changes to Firestore
export async function pushStudyStateToCloud(partial: Partial<RemoteStudyState>) {
  if (isApplyingRemoteChange) return; // Prevent echo loops
  const user = auth.currentUser;
  if (!user) return;

  const docPath = `users/${user.uid}`;
  try {
    const payload: Record<string, unknown> = {
      userId: user.uid,
      email: user.email || '',
      displayName: user.displayName || 'Learner',
      updatedAt: new Date().toISOString(),
      ...partial
    };
    await setDoc(doc(db, 'users', user.uid), payload, { merge: true });
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

// Wire up window listeners for app integration
declare global {
  interface Window {
    firebaseSync?: {
      auth: typeof auth;
      loginWithGoogle: typeof loginWithGoogle;
      logoutUser: typeof logoutUser;
      pushStudyStateToCloud: typeof pushStudyStateToCloud;
      pushCustomShortcutToCloud: typeof pushCustomShortcutToCloud;
      getCurrentUser: () => User | null;
      onAuthChange: (cb: (user: User | null) => void) => void;
      onRemoteStateChange: (cb: (data: RemoteStudyState) => void) => void;
      onRemoteShortcutsChange: (cb: (shortcuts: Record<number, { es: string; hi: string }>) => void) => void;
    };
  }
}

let remoteStateListeners: ((data: RemoteStudyState) => void)[] = [];
let remoteShortcutListeners: ((shortcuts: Record<number, { es: string; hi: string }>) => void)[] = [];

onAuthStateChanged(auth, (user) => {
  if (unsubscribeProfile) { unsubscribeProfile(); unsubscribeProfile = null; }
  if (unsubscribeShortcuts) { unsubscribeShortcuts(); unsubscribeShortcuts = null; }

  if (user) {
    console.log('[Firebase] User authenticated:', user.email);

    // Listen to profile changes in real-time
    const userDocPath = `users/${user.uid}`;
    unsubscribeProfile = onSnapshot(
      doc(db, 'users', user.uid),
      (snapshot) => {
        if (!snapshot.exists()) {
          // Initialize first-time cloud document with current local data
          const localLearned = JSON.parse(localStorage.getItem('flashcards_learned_nums') || '[]');
          const localDeleted = JSON.parse(localStorage.getItem('flashcards_deleted_nums') || '[]');
          const lastNum = Number(localStorage.getItem('last_studied_card_num') || 800);
          const streak = Number(localStorage.getItem('study_streak_count') || 1);

          pushStudyStateToCloud({
            lastActiveCardNum: lastNum,
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
  } else {
    console.log('[Firebase] Signed out.');
  }
});

// Attach to window for seamless interaction with index.html
window.firebaseSync = {
  auth,
  loginWithGoogle,
  logoutUser,
  pushStudyStateToCloud,
  pushCustomShortcutToCloud,
  getCurrentUser: () => auth.currentUser,
  onAuthChange: (cb) => {
    onAuthStateChanged(auth, cb);
  },
  onRemoteStateChange: (cb) => {
    remoteStateListeners.push(cb);
  },
  onRemoteShortcutsChange: (cb) => {
    remoteShortcutListeners.push(cb);
  }
};
