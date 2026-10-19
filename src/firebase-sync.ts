import { initializeApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithCredential,
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

const GOOGLE_OAUTH_CLIENT_ID =
  firebaseConfig.oAuthClientId ||
  '328045128-9o8clmes7c6itrht7acmc4v56e3sfs9n.apps.googleusercontent.com';

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

// Purge all legacy or unverified localStorage keys
try {
  localStorage.removeItem('active_cloud_user_email');
  localStorage.removeItem('stellar_account_email_v1');
  localStorage.removeItem('stellar_account_name_v1');
  localStorage.removeItem('vocab_google_session_v2');
  localStorage.removeItem('vocab_auth_session_v3');
} catch (e) {}

const VERIFIED_AUTH_STORAGE_KEY = 'vocab_verified_google_session_v4';

let currentUser: User | null = null;
let verifiedSession: {
  uid: string;
  googleSub: string;
  email: string;
  displayName: string;
  photoURL?: string;
  idToken?: string;
  accessToken?: string;
  verified: boolean;
} | null = null;

try {
  const saved = JSON.parse(localStorage.getItem(VERIFIED_AUTH_STORAGE_KEY) || 'null');
  if (
    saved &&
    saved.verified === true &&
    typeof saved.email === 'string' &&
    saved.email.includes('@') &&
    typeof saved.googleSub === 'string' &&
    saved.googleSub.length > 3
  ) {
    verifiedSession = {
      uid: saved.uid || `google_${saved.googleSub}`,
      googleSub: saved.googleSub,
      email: saved.email.trim().toLowerCase(),
      displayName: saved.displayName || saved.email.split('@')[0],
      photoURL: saved.photoURL || '',
      idToken: saved.idToken || '',
      accessToken: saved.accessToken || '',
      verified: true
    };
  } else {
    localStorage.removeItem(VERIFIED_AUTH_STORAGE_KEY);
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
    if (verifiedSession && verifiedSession.verified) {
      cb(verifiedSession);
    } else if (currentUser && currentUser.email) {
      cb(currentUser);
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
  if (verifiedSession && verifiedSession.verified && verifiedSession.email) {
    return verifiedSession.email.trim().toLowerCase();
  }
  if (currentUser && currentUser.email) {
    return currentUser.email.trim().toLowerCase();
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

export async function applyVerifiedGoogleUser(userObj: any) {
  if (!userObj || !userObj.email || !userObj.verified) return null;
  const cleanEmail = String(userObj.email).trim().toLowerCase();
  const googleSub = String(userObj.googleSub || userObj.uid || '').replace(/^google_/, '');
  if (!cleanEmail.includes('@') || !googleSub) return null;

  verifiedSession = {
    uid: `google_${googleSub}`,
    googleSub,
    email: cleanEmail,
    displayName: String(userObj.displayName || cleanEmail.split('@')[0]).trim(),
    photoURL: String(userObj.photoURL || ''),
    idToken: String(userObj.idToken || ''),
    accessToken: String(userObj.accessToken || ''),
    verified: true
  };

  try {
    localStorage.setItem(VERIFIED_AUTH_STORAGE_KEY, JSON.stringify(verifiedSession));
  } catch (e) {}

  attachStudyStateListener(cleanEmail);
  notifyAuthCallbacks(verifiedSession);

  // Also sign in to Firebase Auth using the verified Google credential (pure HTTPS REST, no popup/iframe)
  if (verifiedSession.idToken || verifiedSession.accessToken) {
    try {
      const cred = GoogleAuthProvider.credential(
        verifiedSession.idToken || null,
        verifiedSession.accessToken || undefined
      );
      const fbResult = await signInWithCredential(auth, cred);
      if (fbResult && fbResult.user) {
        currentUser = fbResult.user;
      }
    } catch (e) {
      // Token may have expired on page reload; verifiedSession remains active
    }
  }

  return verifiedSession;
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

export function buildGoogleOAuthUrl(stateId: string): string {
  const nonceId = 'nc_' + Date.now() + '_' + Math.random().toString(36).slice(2, 10);
  const origin = window.location.hostname.endsWith('.run.app')
    ? window.location.origin
    : 'https://ais-pre-kgrpdx7hnunkkpn4rtvjsl-444550834163.asia-east1.run.app';
  const redirectUri = origin + '/__/auth/handler';

  return (
    'https://accounts.google.com/o/oauth2/v2/auth' +
    '?client_id=' + encodeURIComponent(GOOGLE_OAUTH_CLIENT_ID) +
    '&redirect_uri=' + encodeURIComponent(redirectUri) +
    '&response_type=' + encodeURIComponent('token id_token') +
    '&scope=' + encodeURIComponent('openid email profile') +
    '&prompt=select_account' +
    '&state=' + encodeURIComponent(stateId) +
    '&nonce=' + encodeURIComponent(nonceId)
  );
}

let activeOAuthPollTimer: any = null;

export function signInWithGoogle(): Promise<any> {
  // Construct state & URL 100% synchronously so mobile browsers never block or close the popup
  const stateId = 'st_' + Date.now() + '_' + Math.random().toString(36).slice(2, 10);
  const oauthUrl = buildGoogleOAuthUrl(stateId);

  // Open Google OAuth 2.0 directly and synchronously on user gesture
  const popup = window.open(
    oauthUrl,
    'google_oauth_signin',
    'width=500,height=660,menubar=no,toolbar=no,location=yes,status=no'
  );

  // If running top-level on mobile and popup was blocked by the browser, navigate directly
  if (!popup && window.self === window.top) {
    window.location.assign(oauthUrl);
    return new Promise(() => {});
  }

  return new Promise((resolve, reject) => {
    let settled = false;
    const startTime = Date.now();

    const cleanup = () => {
      if (activeOAuthPollTimer) {
        clearInterval(activeOAuthPollTimer);
        activeOAuthPollTimer = null;
      }
      window.removeEventListener('message', onMessage);
      if (bc) {
        try { bc.close(); } catch (e) {}
      }
    };

    const finishSuccess = async (userObj: any) => {
      if (settled) return;
      settled = true;
      cleanup();
      const applied = await applyVerifiedGoogleUser(userObj);
      resolve(applied || userObj);
    };

    const finishError = (errStr: string) => {
      if (settled) return;
      settled = true;
      cleanup();
      reject(new Error(errStr));
    };

    const onMessage = (event: MessageEvent) => {
      const data = event.data;
      if (!data || typeof data !== 'object') return;
      if (data.type === 'GOOGLE_OAUTH_SUCCESS' && data.user && data.user.verified) {
        finishSuccess(data.user);
      } else if (data.type === 'GOOGLE_OAUTH_ERROR' && data.state === stateId) {
        finishError(data.error || 'Google Sign-In cancelled');
      }
    };
    window.addEventListener('message', onMessage);

    let bc: BroadcastChannel | null = null;
    try {
      if (typeof BroadcastChannel !== 'undefined') {
        bc = new BroadcastChannel('vocab_google_auth_channel');
        bc.onmessage = (ev) => {
          const data = ev.data;
          if (data && data.type === 'GOOGLE_OAUTH_SUCCESS' && data.user && data.user.verified) {
            finishSuccess(data.user);
          }
        };
      }
    } catch (e) {}

    if (activeOAuthPollTimer) clearInterval(activeOAuthPollTimer);
    activeOAuthPollTimer = setInterval(async () => {
      if (settled) return;
      if (Date.now() - startTime > 180000) {
        finishError('Google Sign-In timed out');
        return;
      }
      try {
        const res = await fetch(`/api/auth/poll-oauth?state=${encodeURIComponent(stateId)}`);
        if (res.ok) {
          const data = await res.json();
          if (data && data.status === 'completed' && data.user && data.user.verified) {
            finishSuccess(data.user);
          } else if (data && data.status === 'error') {
            finishError(data.error || 'Google Sign-In cancelled');
          }
        }
      } catch (e) {}
    }, 900);
  });
}

export const loginWithGoogle = signInWithGoogle;

export async function signOutUser() {
  verifiedSession = null;
  currentUser = null;
  if (unsubscribeStudyState) {
    unsubscribeStudyState();
    unsubscribeStudyState = null;
  }
  try {
    localStorage.removeItem(VERIFIED_AUTH_STORAGE_KEY);
    localStorage.removeItem('vocab_auth_session_v3');
    localStorage.removeItem('vocab_google_session_v2');
    localStorage.removeItem('active_cloud_user_email');
  } catch (e) {}
  try {
    if (auth.currentUser) {
      await signOut(auth);
    }
  } catch (error) {}
  notifyAuthCallbacks(null);
}

export const logoutUser = signOutUser;

// Initialize listener if a verified session exists from previous login
if (verifiedSession && verifiedSession.verified && verifiedSession.email) {
  attachStudyStateListener(verifiedSession.email);
  if (verifiedSession.idToken || verifiedSession.accessToken) {
    try {
      const cred = GoogleAuthProvider.credential(
        verifiedSession.idToken || null,
        verifiedSession.accessToken || undefined
      );
      signInWithCredential(auth, cred).catch(() => {});
    } catch (e) {}
  }
}

onAuthStateChanged(auth, async (user) => {
  currentUser = user;
  if (user && user.email) {
    const cleanEmail = user.email.trim().toLowerCase();
    const displayName = user.displayName || cleanEmail.split('@')[0];
    if (!verifiedSession || verifiedSession.email !== cleanEmail) {
      verifiedSession = {
        uid: user.uid,
        googleSub: user.uid,
        email: cleanEmail,
        displayName,
        photoURL: user.photoURL || '',
        verified: true
      };
      try {
        localStorage.setItem(VERIFIED_AUTH_STORAGE_KEY, JSON.stringify(verifiedSession));
      } catch (e) {}
      attachStudyStateListener(cleanEmail);
    }
    notifyAuthCallbacks(verifiedSession);
  } else if (verifiedSession && verifiedSession.verified) {
    notifyAuthCallbacks(verifiedSession);
  } else {
    notifyAuthCallbacks(null);
  }
});

(window as any).firebaseSync = {
  auth,
  db,
  signInWithGoogle,
  loginWithGoogle,
  applyVerifiedGoogleUser,
  buildGoogleOAuthUrl,
  signOutUser,
  logoutUser,
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
  getCurrentUser: () => verifiedSession || currentUser
};
