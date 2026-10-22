import { initializeApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
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

// Detect if hosted on a static site (e.g. Render Static Site *.onrender.com) where /api/* routes do not exist
let serverApiAvailable: boolean = (() => {
  if (typeof window === 'undefined' || !window.location) return false;
  const host = String(window.location.hostname || '').toLowerCase();
  if (
    host.endsWith('.onrender.com') ||
    host.endsWith('.github.io') ||
    host.endsWith('.netlify.app') ||
    host.endsWith('.vercel.app') ||
    host.endsWith('.pages.dev')
  ) {
    return false;
  }
  return true;
})();

export function isServerApiAvailable(): boolean {
  return serverApiAvailable;
}

export function markServerApiUnavailable() {
  serverApiAvailable = false;
}

// Purge all legacy or unverified localStorage keys
try {
  localStorage.removeItem('active_cloud_user_email');
  localStorage.removeItem('stellar_account_email_v1');
  localStorage.removeItem('stellar_account_name_v1');
  localStorage.removeItem('vocab_google_session_v2');
  localStorage.removeItem('vocab_auth_session_v3');
  localStorage.removeItem('vocab_verified_google_session_v4');
  localStorage.removeItem('vocab_verified_auth_session_v5');
  localStorage.removeItem('vocab_google_known_accounts_v2');
} catch (e) {}

export const COMMON_CLOUD_ACCOUNT = 'common_all_devices@stellar.cloud';
export const COMMON_CLOUD_DOC_ID = 'global_common_cloud_v1';

const VERIFIED_AUTH_STORAGE_KEY = 'vocab_verified_auth_session_v6';

let currentUser: User | null = null;
let verifiedSession: {
  uid: string;
  googleSub: string;
  email: string;
  displayName: string;
  photoURL?: string;
  idToken?: string;
  accessToken?: string;
  authMethod?: string;
  verified: boolean;
} | null = null;

function isBlockedOrDummyEmail(email: string): boolean {
  const clean = String(email || '').trim().toLowerCase();
  if (!clean || !clean.includes('@')) return true;
  if (clean === COMMON_CLOUD_ACCOUNT) return false;
  if (
    clean === 'sgsgds@gmail.com' ||
    clean === 'cloud_sync@sync.internal' ||
    clean.endsWith('@cloud.sync') ||
    clean.endsWith('@sync.internal')
  ) {
    return true;
  }
  return false;
}

try {
  const saved = JSON.parse(localStorage.getItem(VERIFIED_AUTH_STORAGE_KEY) || 'null');
  if (
    saved &&
    saved.verified === true &&
    typeof saved.email === 'string' &&
    !isBlockedOrDummyEmail(saved.email) &&
    typeof saved.googleSub === 'string' &&
    saved.googleSub.length > 3 &&
    (saved.authMethod === 'email_account' ||
      saved.authMethod === 'google_oauth' ||
      saved.authMethod === 'common_cloud')
  ) {
    verifiedSession = {
      uid: saved.uid || `google_${saved.googleSub}`,
      googleSub: saved.googleSub,
      email: saved.email.trim().toLowerCase(),
      displayName: saved.displayName || saved.email.split('@')[0],
      photoURL: saved.photoURL || '',
      idToken: saved.idToken || '',
      accessToken: saved.accessToken || '',
      authMethod: saved.authMethod,
      verified: true
    };
  } else {
    localStorage.removeItem(VERIFIED_AUTH_STORAGE_KEY);
  }
} catch (e) {}

let unsubscribeStudyStateList: Array<() => void> = [];
let isApplyingRemoteUpdate = false;

const authChangeCallbacks: Array<(user: any) => void> = [];
const remoteStateCallbacks: Array<(data: any) => void> = [];
const remoteShortcutsCallbacks: Array<(shortcuts: Record<string, any>) => void> = [];

export function emailToDocId(email: string): string {
  const clean = String(email || '').trim().toLowerCase();
  let h1 = 0xdeadbeef ^ clean.length;
  let h2 = 0x41c6ce57 ^ clean.length;
  for (let i = 0, ch; i < clean.length; i++) {
    ch = clean.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  return 'acct_' + (h2 >>> 0).toString(16).padStart(8, '0') + (h1 >>> 0).toString(16).padStart(8, '0');
}

async function hashStringSHA256(str: string): Promise<string> {
  try {
    if (typeof crypto !== 'undefined' && crypto.subtle) {
      const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
      return Array.from(new Uint8Array(buf))
        .map((b) => b.toString(16).padStart(2, '0'))
        .join('');
    }
  } catch (e) {}
  return emailToDocId(str).replace(/^acct_/, '').padEnd(32, '0');
}

async function getAccountDocIds(email: string): Promise<{ primaryDocId: string; shaDocId: string; legacyDocId: string }> {
  const clean = String(email || '').trim().toLowerCase();
  if (clean === COMMON_CLOUD_ACCOUNT) {
    const shaFull = await hashStringSHA256(clean);
    return {
      primaryDocId: COMMON_CLOUD_DOC_ID,
      shaDocId: `acct_${shaFull.slice(0, 32)}`,
      legacyDocId: emailToDocId('stellarnetworkhub@gmail.com')
    };
  }
  const primaryDocId = emailToDocId(clean);
  const shaFull = await hashStringSHA256(clean);
  const shaDocId = `acct_${shaFull.slice(0, 32)}`;
  const legacyDocId = `acct_${clean.replace(/[^a-z0-9]/g, '_')}`.slice(0, 120);
  return { primaryDocId, shaDocId, legacyDocId };
}

export function onAuthChange(cb: (user: any) => void) {
  if (typeof cb === 'function') {
    authChangeCallbacks.push(cb);
    if (verifiedSession && verifiedSession.verified) {
      cb(verifiedSession);
    } else if (currentUser && currentUser.email) {
      cb(currentUser);
    } else {
      cb({
        uid: COMMON_CLOUD_DOC_ID,
        googleSub: COMMON_CLOUD_DOC_ID,
        email: COMMON_CLOUD_ACCOUNT,
        displayName: 'Common Cloud (All Devices)',
        photoURL: '',
        authMethod: 'common_cloud',
        verified: true
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

export function getActiveAccountEmail(): string {
  if (verifiedSession && verifiedSession.verified && verifiedSession.email) {
    return verifiedSession.email.trim().toLowerCase();
  }
  if (currentUser && currentUser.email) {
    return currentUser.email.trim().toLowerCase();
  }
  return COMMON_CLOUD_ACCOUNT;
}

function clearStudyStateListeners() {
  if (unsubscribeStudyStateList.length > 0) {
    unsubscribeStudyStateList.forEach((unsub) => {
      try {
        unsub();
      } catch (e) {}
    });
    unsubscribeStudyStateList = [];
  }
}

async function attachStudyStateListener(email: string) {
  clearStudyStateListeners();
  const clean = String(email || COMMON_CLOUD_ACCOUNT).trim().toLowerCase();
  if (!clean || isBlockedOrDummyEmail(clean)) return;

  const { primaryDocId, shaDocId } = await getAccountDocIds(clean);
  const docIds = Array.from(new Set([primaryDocId, shaDocId, ...(clean === COMMON_CLOUD_ACCOUNT ? [COMMON_CLOUD_DOC_ID] : [])]));

  docIds.forEach((docId) => {
    const stateDocRef = doc(db, 'study_state', docId);
    const unsub = onSnapshot(
      stateDocRef,
      (docSnap) => {
        if (!docSnap.exists()) return;
        const raw = docSnap.data();
        const payload = raw?.payload && typeof raw.payload === 'object' ? raw.payload : raw;
        if (!payload) return;

        isApplyingRemoteUpdate = true;
        remoteStateCallbacks.forEach((cb) => {
          try {
            cb({ ...payload, email: clean, updatedAt: raw.updatedAt || payload.updatedAt });
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
    unsubscribeStudyStateList.push(unsub);
  });

  // Also attach real-time listener to production user_progress/{userId}
  const uid =
    clean === COMMON_CLOUD_ACCOUNT
      ? COMMON_CLOUD_DOC_ID
      : currentUser?.uid || verifiedSession?.uid;
  if (uid) {
    const progDocRef = doc(db, 'user_progress', uid);
    const unsubProg = onSnapshot(
      progDocRef,
      (docSnap) => {
        if (!docSnap.exists()) return;
        const raw = docSnap.data();
        if (!raw) return;

        isApplyingRemoteUpdate = true;
        const payload = {
          email: clean,
          learnedCardNums: raw.learnedCards || raw.learnedCardNums || [],
          deletedCardNums: raw.deletedCardNums || [],
          lastActiveCardNum: raw.lastActiveCardNum,
          activeDeckId: raw.activeDeckId,
          customShortcuts: raw.customShortcuts,
          customDecks: raw.customDecks,
          customSections: raw.customSections,
          streakCount: typeof raw.streakCount === 'number' ? raw.streakCount : 0,
          updatedAt: raw.lastStudied || raw.updatedAt || new Date().toISOString()
        };
        remoteStateCallbacks.forEach((cb) => {
          try {
            cb(payload);
          } catch (e) {}
        });
        setTimeout(() => {
          isApplyingRemoteUpdate = false;
        }, 250);
      },
      (error) => {
        handleFirestoreError(error, OperationType.GET, `user_progress/${uid}`);
      }
    );
    unsubscribeStudyStateList.push(unsubProg);
  }
}

export async function applyVerifiedGoogleUser(userObj: any) {
  if (!userObj || !userObj.email || !userObj.verified) return null;
  const cleanEmail = String(userObj.email).trim().toLowerCase();
  if (isBlockedOrDummyEmail(cleanEmail)) return null;

  const rawSub = String(userObj.googleSub || userObj.uid || '').trim();
  if (!cleanEmail.includes('@') || !rawSub) return null;

  const uid = userObj.uid || (rawSub.startsWith('acct_') ? rawSub : `google_${rawSub.replace(/^google_/, '')}`);
  const googleSub = rawSub.replace(/^google_/, '');
  const resolvedAuthMethod =
    userObj.authMethod === 'google_oauth' ? 'google_oauth' : 'email_account';

  verifiedSession = {
    uid,
    googleSub,
    email: cleanEmail,
    displayName: String(userObj.displayName || cleanEmail.split('@')[0]).trim(),
    photoURL: String(userObj.photoURL || ''),
    idToken: String(userObj.idToken || ''),
    accessToken: String(userObj.accessToken || ''),
    authMethod: resolvedAuthMethod,
    verified: true
  };

  try {
    localStorage.setItem(VERIFIED_AUTH_STORAGE_KEY, JSON.stringify(verifiedSession));
  } catch (e) {}

  // Sync user profile to Firestore users/{uid}
  try {
    setDoc(
      doc(db, 'users', uid),
      {
        uid,
        email: cleanEmail,
        name: verifiedSession.displayName,
        photoURL: verifiedSession.photoURL,
        lastActive: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      { merge: true }
    ).catch(() => {});
  } catch (e) {}

  attachStudyStateListener(cleanEmail);
  notifyAuthCallbacks(verifiedSession);

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
    } catch (e) {}
  }

  return verifiedSession;
}

export async function saveAccountStateToFirestore(email: string, payload: any): Promise<boolean> {
  const clean = String(email || COMMON_CLOUD_ACCOUNT).trim().toLowerCase();
  if (!clean || isBlockedOrDummyEmail(clean) || !payload) return false;
  const { primaryDocId, shaDocId } = await getAccountDocIds(clean);
  const path = `study_state/${primaryDocId}`;
  try {
    const updatedAt = payload.updatedAt || new Date().toISOString();
    const sanitizedPayload = { ...payload, updatedAt };
    delete sanitizedPayload.email;

    const writes: Promise<any>[] = [
      setDoc(doc(db, 'study_state', primaryDocId), {
        accountId: primaryDocId,
        updatedAt,
        payload: sanitizedPayload
      }),
      setDoc(doc(db, 'study_state', shaDocId), {
        accountId: shaDocId,
        updatedAt,
        payload: sanitizedPayload
      })
    ];

    const uid =
      clean === COMMON_CLOUD_ACCOUNT
        ? COMMON_CLOUD_DOC_ID
        : currentUser?.uid || verifiedSession?.uid;
    if (uid) {
      writes.push(
        setDoc(
          doc(db, 'user_progress', uid),
          {
            userId: uid,
            email: clean,
            learnedCards: sanitizedPayload.learnedCardNums || [],
            deletedCardNums: sanitizedPayload.deletedCardNums || [],
            lastActiveCardNum: sanitizedPayload.lastActiveCardNum || 800,
            activeDeckId: sanitizedPayload.activeDeckId || 'deck-800-1000',
            customShortcuts: sanitizedPayload.customShortcuts || {},
            customDecks: sanitizedPayload.customDecks || {},
            customSections: sanitizedPayload.customSections || [],
            streakCount: typeof sanitizedPayload.streakCount === 'number' ? sanitizedPayload.streakCount : 0,
            lastStudied: updatedAt,
            updatedAt
          },
          { merge: true }
        )
      );
      writes.push(
        setDoc(
          doc(db, 'users', uid),
          {
            uid,
            email: clean,
            name:
              clean === COMMON_CLOUD_ACCOUNT
                ? 'Common Cloud (All Devices)'
                : verifiedSession?.displayName || clean.split('@')[0],
            photoURL: verifiedSession?.photoURL || '',
            lastActive: updatedAt,
            updatedAt
          },
          { merge: true }
        )
      );
    }

    await Promise.all(writes);
    return true;
  } catch (error) {
    handleFirestoreError(error, OperationType.WRITE, path);
    return false;
  }
}

export async function loadAccountStateFromFirestore(
  email: string
): Promise<{ exists: boolean; updatedAt: string; payload: any } | null> {
  const clean = String(email || COMMON_CLOUD_ACCOUNT).trim().toLowerCase();
  if (!clean || isBlockedOrDummyEmail(clean)) return null;
  const { primaryDocId, shaDocId, legacyDocId } = await getAccountDocIds(clean);
  const path = `study_state/${primaryDocId}`;
  try {
    const uid =
      clean === COMMON_CLOUD_ACCOUNT
        ? COMMON_CLOUD_DOC_ID
        : currentUser?.uid || verifiedSession?.uid;
    const fetchPromises: Promise<any>[] = [
      getDoc(doc(db, 'study_state', primaryDocId)),
      getDoc(doc(db, 'study_state', shaDocId)),
      getDoc(doc(db, 'study_state', legacyDocId))
    ];
    if (uid) {
      fetchPromises.push(getDoc(doc(db, 'user_progress', uid)));
    }

    const snaps = await Promise.all(fetchPromises);
    const candidates: Array<{ data: any; ts: number; isProgressDoc?: boolean }> = [];

    snaps.forEach((s, idx) => {
      if (s && s.exists()) {
        const d = s.data();
        const t = Date.parse(d?.updatedAt || d?.payload?.updatedAt || d?.lastStudied || '') || 0;
        candidates.push({ data: d, ts: t, isProgressDoc: idx === 3 });
      }
    });

    if (candidates.length === 0) {
      return { exists: false, updatedAt: '', payload: null };
    }

    candidates.sort((a, b) => b.ts - a.ts);
    const chosen = candidates[0];
    const chosenData = chosen.data;

    let payload: any = null;
    if (chosen.isProgressDoc) {
      payload = {
        learnedCardNums: chosenData.learnedCards || chosenData.learnedCardNums || [],
        deletedCardNums: chosenData.deletedCardNums || [],
        lastActiveCardNum: chosenData.lastActiveCardNum || 800,
        activeDeckId: chosenData.activeDeckId || 'deck-800-1000',
        customShortcuts: chosenData.customShortcuts || {},
        customDecks: chosenData.customDecks || {},
        customSections: chosenData.customSections || [],
        streakCount: chosenData.streakCount || 0,
        updatedAt: chosenData.lastStudied || chosenData.updatedAt || new Date().toISOString()
      };
    } else {
      payload = chosenData?.payload && typeof chosenData.payload === 'object' ? chosenData.payload : chosenData;
    }

    return {
      exists: true,
      updatedAt: chosenData?.updatedAt || payload?.updatedAt || new Date().toISOString(),
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
  const uid = currentUser?.uid || verifiedSession?.uid || COMMON_CLOUD_DOC_ID;
  if (!uid) return;
  const path = `users/${uid}`;
  try {
    const updatedAt = new Date().toISOString();
    await Promise.all([
      setDoc(
        doc(db, 'users', uid),
        {
          userId: uid,
          displayName: currentUser?.displayName || verifiedSession?.displayName || 'Common Cloud (All Devices)',
          ...partialState,
          updatedAt
        },
        { merge: true }
      ),
      setDoc(
        doc(db, 'user_progress', uid),
        {
          userId: uid,
          learnedCards: partialState.learnedCardNums || [],
          streakCount: typeof partialState.streakCount === 'number' ? partialState.streakCount : 0,
          lastStudied: updatedAt,
          updatedAt
        },
        { merge: true }
      )
    ]);
  } catch (error) {
    handleFirestoreError(error, OperationType.WRITE, path);
  }
}

export async function pushCustomShortcutToCloud(cardNum: number | string, es: string, hi: string) {
  if (isApplyingRemoteUpdate) return;
  const uid = currentUser?.uid || verifiedSession?.uid || COMMON_CLOUD_DOC_ID;
  if (!uid) return;
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
  const uid = currentUser?.uid || verifiedSession?.uid || COMMON_CLOUD_DOC_ID;
  if (!uid) return;
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
  const uid = currentUser?.uid || verifiedSession?.uid || COMMON_CLOUD_DOC_ID;
  if (!uid) return;
  const path = `users/${uid}/decks/${deckId}`;
  try {
    await deleteDoc(doc(db, 'users', uid, 'decks', deckId));
  } catch (error) {
    handleFirestoreError(error, OperationType.DELETE, path);
  }
}

const GOOGLE_OAUTH_CLIENT_ID =
  firebaseConfig.oAuthClientId ||
  '328045128-9o8clmes7c6itrht7acmc4v56e3sfs9n.apps.googleusercontent.com';

export function buildGoogleOAuthUrl(stateId: string): string {
  const nonceId = 'nc_' + Date.now() + '_' + Math.random().toString(36).slice(2, 10);
  let origin = 'https://ais-dev-kgrpdx7hnunkkpn4rtvjsl-444550834163.asia-east1.run.app';
  if (typeof window !== 'undefined' && window.location && window.location.origin) {
    const winOrig = window.location.origin;
    if (winOrig && winOrig !== 'null' && winOrig.startsWith('http')) {
      origin = winOrig;
    }
  }
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

export async function signInWithAccount(
  email: string,
  password: string,
  displayName?: string,
  action: string = 'login'
): Promise<any> {
  const cleanEmail = String(email || '').trim().toLowerCase();
  const cleanPassword = String(password || '').trim();
  const normalizedAction = String(action || 'login').toLowerCase();
  const isRegister = normalizedAction === 'register' || normalizedAction === 'signup';

  if (!cleanEmail || !cleanEmail.includes('@') || !cleanEmail.split('@')[1]?.includes('.')) {
    throw new Error('Please enter a valid Google or email address (e.g. yourname@gmail.com).');
  }
  if (!cleanPassword || cleanPassword.length < (isRegister ? 6 : 4)) {
    throw new Error(
      isRegister
        ? 'Password must be at least 6 characters.'
        : 'Please enter your account password.'
    );
  }

  // 1. Direct client-side Firestore authentication (works on ALL devices & domains including Render static site)
  const emailHash = await hashStringSHA256(cleanEmail);
  const credDocId = `cred_${emailHash.slice(0, 32)}`;
  const passHash = await hashStringSHA256(cleanPassword + '_salt_stellar');

  let credSnap: any = null;
  try {
    credSnap = await getDoc(doc(db, 'study_state', credDocId));
  } catch (fsErr) {
    // Fallback to server endpoint if Firestore client is unreachable
    if (serverApiAvailable) {
      const res = await fetch('/api/auth/account-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: cleanEmail, password: cleanPassword, displayName, action: normalizedAction })
      });
      const contentType = res.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        const data = await res.json();
        if (!res.ok || !data || !data.ok) {
          throw new Error(data?.error || 'Invalid email or password.');
        }
        if (data.user) {
          return await applyVerifiedGoogleUser(data.user);
        }
      } else {
        serverApiAvailable = false;
      }
    }
    throw new Error('Unable to reach cloud authentication server. Please check your internet connection.');
  }

  let resolvedDisplayName = displayName || cleanEmail.split('@')[0];

  if (isRegister) {
    if (credSnap && credSnap.exists()) {
      const data = credSnap.data();
      const storedMatches =
        data &&
        (data.passwordHash === passHash || data.sha256Hash === passHash);
      if (!storedMatches) {
        throw new Error(
          `An account for "${cleanEmail}" is already registered. Please switch to "Log In" and enter your saved password.`
        );
      }
      resolvedDisplayName = data.displayName || resolvedDisplayName;
    } else {
      await setDoc(doc(db, 'study_state', credDocId), {
        accountId: emailHash,
        displayName: resolvedDisplayName,
        passwordHash: passHash,
        sha256Hash: passHash,
        createdAt: new Date().toISOString()
      });
    }
  } else {
    if (!credSnap || !credSnap.exists()) {
      throw new Error(
        `No registered account found for "${cleanEmail}". Please tap "Create Account" above to register your password first.`
      );
    }
    const data = credSnap.data();
    const storedMatches =
      data &&
      (data.passwordHash === passHash || data.sha256Hash === passHash);
    if (!storedMatches) {
      throw new Error(
        `Incorrect password for "${cleanEmail}". Please enter your correct password.`
      );
    }
    resolvedDisplayName = data.displayName || resolvedDisplayName;
  }

  if (serverApiAvailable) {
    fetch('/api/auth/account-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: cleanEmail, password: cleanPassword, displayName: resolvedDisplayName, action: isRegister ? 'register' : 'login' })
    })
      .then((r) => {
        const ct = r.headers.get('content-type') || '';
        if (!ct.includes('application/json')) serverApiAvailable = false;
      })
      .catch(() => {
        serverApiAvailable = false;
      });
  }

  const verifiedUser = {
    uid: `acct_${emailHash.slice(0, 24)}`,
    googleSub: `acct_${emailHash.slice(0, 24)}`,
    email: cleanEmail,
    displayName: resolvedDisplayName,
    photoURL: '',
    verified: true,
    authMethod: 'email_account',
    authenticatedAt: new Date().toISOString()
  };
  return await applyVerifiedGoogleUser(verifiedUser);
}

export async function registerAccount(email: string, password: string, displayName?: string): Promise<any> {
  return signInWithAccount(email, password, displayName, 'register');
}

export function getNativeWindowOpen(): typeof window.open {
  try {
    let helper = document.getElementById('__native_open_helper__') as HTMLIFrameElement | null;
    if (!helper && typeof document !== 'undefined' && document.body) {
      helper = document.createElement('iframe');
      helper.id = '__native_open_helper__';
      helper.style.display = 'none';
      helper.src = 'about:blank';
      document.body.appendChild(helper);
    }
    if (helper && helper.contentWindow && typeof helper.contentWindow.open === 'function') {
      return helper.contentWindow.open.bind(helper.contentWindow);
    }
  } catch (e) {}
  return window.open ? window.open.bind(window) : window.open;
}

export function restoreNativeWindowOpen() {
  try {
    const native = getNativeWindowOpen();
    if (native && typeof window !== 'undefined') {
      window.open = native;
    }
  } catch (e) {}
}

if (typeof window !== 'undefined') {
  restoreNativeWindowOpen();
}

if (typeof window !== 'undefined') {
  getRedirectResult(auth)
    .then(async (result) => {
      if (result && result.user && result.user.email) {
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const cleanEmail = result.user.email.trim().toLowerCase();
        const verifiedUser = {
          uid: result.user.uid,
          googleSub: result.user.uid,
          email: cleanEmail,
          displayName: result.user.displayName || cleanEmail.split('@')[0],
          photoURL: result.user.photoURL || '',
          idToken: credential?.idToken || '',
          accessToken: credential?.accessToken || '',
          verified: true,
          authMethod: 'google_oauth',
          authenticatedAt: new Date().toISOString()
        };
        await applyVerifiedGoogleUser(verifiedUser);
      }
    })
    .catch((e) => {
      console.warn('Redirect sign-in notice:', e);
    });
}

export async function signInWithGoogle(forceAccountSelect = true): Promise<any> {
  restoreNativeWindowOpen();

  const provider = new GoogleAuthProvider();
  provider.addScope('email');
  provider.addScope('profile');
  if (forceAccountSelect) {
    provider.setCustomParameters({
      prompt: 'select_account'
    });
  }

  const isMobile = typeof navigator !== 'undefined' && /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  try {
    const result = await signInWithPopup(auth, provider);
    if (!result || !result.user || !result.user.email) {
      throw new Error('Google Sign-In was cancelled.');
    }

    const credential = GoogleAuthProvider.credentialFromResult(result);
    const cleanEmail = result.user.email.trim().toLowerCase();
    const verifiedUser = {
      uid: result.user.uid,
      googleSub: result.user.uid,
      email: cleanEmail,
      displayName: result.user.displayName || cleanEmail.split('@')[0],
      photoURL: result.user.photoURL || '',
      idToken: credential?.idToken || '',
      accessToken: credential?.accessToken || '',
      verified: true,
      authMethod: 'google_oauth',
      authenticatedAt: new Date().toISOString()
    };

    return await applyVerifiedGoogleUser(verifiedUser);
  } catch (err: any) {
    const code = err && err.code ? String(err.code) : '';
    if (code === 'auth/popup-closed-by-user' || code === 'auth/cancelled-popup-request') {
      throw new Error('Google Sign-In window was closed.');
    }
    if (code === 'auth/popup-blocked' || isMobile) {
      try {
        await signInWithRedirect(auth, provider);
        return { isRedirecting: true };
      } catch (redirErr: any) {
        throw new Error(redirErr?.message || 'Popup was blocked. Please enable popups to sign in with Google.');
      }
    }
    throw new Error(err?.message || 'Could not connect to Google Sign-In.');
  }
}

export async function saveCardProgress(learnedIndicesArray: (number | string)[], streak: number) {
  const uid = currentUser?.uid || verifiedSession?.uid || COMMON_CLOUD_DOC_ID;
  if (!uid) return;
  const userProgressRef = doc(db, 'user_progress', uid);
  const updatedAt = new Date().toISOString();
  await setDoc(userProgressRef, {
    learnedCards: learnedIndicesArray,
    streakCount: streak,
    lastStudied: updatedAt,
    updatedAt
  }, { merge: true });
}

export async function activateCommonCloudMode() {
  verifiedSession = null;
  currentUser = null;
  try {
    localStorage.removeItem(VERIFIED_AUTH_STORAGE_KEY);
    if (auth.currentUser) {
      await signOut(auth);
    }
  } catch (e) {}
  attachStudyStateListener(COMMON_CLOUD_ACCOUNT);
  const commonUser = {
    uid: COMMON_CLOUD_DOC_ID,
    googleSub: COMMON_CLOUD_DOC_ID,
    email: COMMON_CLOUD_ACCOUNT,
    displayName: 'Common Cloud (All Devices)',
    photoURL: '',
    authMethod: 'common_cloud',
    verified: true
  };
  notifyAuthCallbacks(commonUser);
  return commonUser;
}

export const switchGoogleAccount = () => signInWithGoogle(true);
export const loginWithGoogle = signInWithGoogle;
export const logoutUser = signOutUser;

export async function signOutUser() {
  return await activateCommonCloudMode();
}

// Initialize listener immediately (either verified session or Universal Common Cloud)
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
} else {
  attachStudyStateListener(COMMON_CLOUD_ACCOUNT);
}

onAuthStateChanged(auth, async (user) => {
  currentUser = user;
  if (user && user.email && !isBlockedOrDummyEmail(user.email)) {
    const cleanEmail = user.email.trim().toLowerCase();
    const displayName = user.displayName || cleanEmail.split('@')[0];
    if (!verifiedSession || verifiedSession.email !== cleanEmail) {
      verifiedSession = {
        uid: user.uid,
        googleSub: user.uid,
        email: cleanEmail,
        displayName,
        photoURL: user.photoURL || '',
        authMethod: 'google_oauth',
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
    attachStudyStateListener(COMMON_CLOUD_ACCOUNT);
    notifyAuthCallbacks({
      uid: COMMON_CLOUD_DOC_ID,
      googleSub: COMMON_CLOUD_DOC_ID,
      email: COMMON_CLOUD_ACCOUNT,
      displayName: 'Common Cloud (All Devices)',
      photoURL: '',
      authMethod: 'common_cloud',
      verified: true
    });
  }
});

(window as any).firebaseSync = {
  auth,
  db,
  COMMON_CLOUD_ACCOUNT,
  COMMON_CLOUD_DOC_ID,
  isServerApiAvailable,
  markServerApiUnavailable,
  signInWithGoogle,
  loginWithGoogle,
  switchGoogleAccount,
  activateCommonCloudMode,
  restoreNativeWindowOpen,
  signInWithAccount,
  registerAccount,
  applyVerifiedGoogleUser,
  buildGoogleOAuthUrl,
  signOutUser,
  logoutUser,
  getActiveAccountEmail,
  saveAccountStateToFirestore,
  saveCardProgress,
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
