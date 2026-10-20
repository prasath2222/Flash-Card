import { initializeApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
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

function rewriteFirebaseAuthIframeSrc(rawUrl: string): string {
  try {
    if (!rawUrl || !rawUrl.includes('/__/auth/iframe')) return rawUrl;
    if (typeof window !== 'undefined' && window.location) {
      const host = window.location.hostname;
      if (
        host === 'localhost' ||
        host.endsWith('.firebaseapp.com') ||
        host.endsWith('.web.app') ||
        host.endsWith('.run.app')
      ) {
        return rawUrl;
      }
    }
    const hashIdx = rawUrl.indexOf('#');
    if (hashIdx === -1) return rawUrl;
    const base = rawUrl.slice(0, hashIdx);
    const hash = rawUrl.slice(hashIdx + 1);
    const params = new URLSearchParams(hash);
    if (!params.has('parent')) return rawUrl;

    const id = params.get('id') || params.get('_gfid') || '';
    const gfid = params.get('_gfid') || id;
    const pfname = params.get('pfname') || '';
    const rpctoken = params.get('rpctoken') || '';

    params.delete('parent');
    params.delete('id');
    params.delete('_gfid');
    params.delete('pfname');

    params.set(
      'jcp',
      JSON.stringify({
        id,
        _gfid: gfid,
        parent: 'http://localhost',
        pfname
      })
    );
    if (rpctoken) {
      params.set('rpctoken', rpctoken);
    }
    return `${base}#${params.toString()}`;
  } catch (e) {
    return rawUrl;
  }
}

export function rewriteFirebaseAuthHandlerUrl(rawUrl: string): string {
  try {
    if (!rawUrl || !rawUrl.includes('/__/auth/handler')) return rawUrl;
    const parsed = new URL(rawUrl);
    if (parsed.searchParams.has('redirectUrl')) {
      parsed.searchParams.set('redirectUrl', 'http://localhost');
    }
    return parsed.toString();
  } catch (e) {
    return rawUrl;
  }
}

function installCrossDomainFirebaseAuthPatch() {
  if (typeof window === 'undefined' || typeof Element === 'undefined') return;
  try {
    const win = window as any;
    if (win.__fbAuthCrossDomainPatched) return;
    win.__fbAuthCrossDomainPatched = true;

    const origSetAttribute = Element.prototype.setAttribute;
    Element.prototype.setAttribute = function (name: string, value: string) {
      if (
        typeof HTMLIFrameElement !== 'undefined' &&
        this instanceof HTMLIFrameElement &&
        typeof name === 'string' &&
        name.toLowerCase() === 'src' &&
        typeof value === 'string' &&
        value.includes('/__/auth/iframe')
      ) {
        try {
          origSetAttribute.call(this, 'referrerpolicy', 'origin');
        } catch (e) {}
        return origSetAttribute.call(this, name, rewriteFirebaseAuthIframeSrc(value));
      }
      return origSetAttribute.call(this, name, value);
    };

    if (typeof HTMLIFrameElement !== 'undefined') {
      const desc = Object.getOwnPropertyDescriptor(HTMLIFrameElement.prototype, 'src');
      if (desc && desc.set && desc.get) {
        Object.defineProperty(HTMLIFrameElement.prototype, 'src', {
          configurable: true,
          enumerable: desc.enumerable,
          get: desc.get,
          set(val: string) {
            if (typeof val === 'string' && val.includes('/__/auth/iframe')) {
              try {
                origSetAttribute.call(this, 'referrerpolicy', 'origin');
              } catch (e) {}
              desc.set!.call(this, rewriteFirebaseAuthIframeSrc(val));
              return;
            }
            desc.set!.call(this, val);
          }
        });
      }
    }
  } catch (e) {}
}

installCrossDomainFirebaseAuthPatch();

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
  const rawSub = String(userObj.googleSub || userObj.uid || '').trim();
  if (!cleanEmail.includes('@') || !rawSub) return null;

  const uid = userObj.uid || (rawSub.startsWith('acct_') ? rawSub : `google_${rawSub.replace(/^google_/, '')}`);
  const googleSub = rawSub.replace(/^google_/, '');

  verifiedSession = {
    uid,
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

  // Also sign in to Firebase Auth using the verified Google credential if present
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
    const sanitizedPayload = { ...payload, updatedAt };
    delete sanitizedPayload.email;
    await setDoc(doc(db, 'study_state', docId), {
      accountId: docId,
      updatedAt,
      payload: sanitizedPayload
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
  const legacyDocId = `acct_${clean.replace(/[^a-z0-9]/g, '_')}`.slice(0, 120);
  const path = `study_state/${docId}`;
  try {
    const [snap, legacySnap] = await Promise.all([
      getDoc(doc(db, 'study_state', docId)),
      getDoc(doc(db, 'study_state', legacyDocId))
    ]);
    let chosenData: any = null;
    if (snap.exists() && legacySnap.exists()) {
      const d1 = snap.data();
      const d2 = legacySnap.data();
      const t1 = Date.parse(d1?.updatedAt || d1?.payload?.updatedAt || '') || 0;
      const t2 = Date.parse(d2?.updatedAt || d2?.payload?.updatedAt || '') || 0;
      chosenData = t1 >= t2 ? d1 : d2;
    } else if (snap.exists()) {
      chosenData = snap.data();
    } else if (legacySnap.exists()) {
      chosenData = legacySnap.data();
    }
    if (!chosenData) {
      return { exists: false, updatedAt: '', payload: null };
    }
    const payload = chosenData?.payload && typeof chosenData.payload === 'object' ? chosenData.payload : chosenData;
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
  if (!currentUser) return;
  const uid = currentUser.uid;
  const path = `users/${uid}`;
  try {
    await setDoc(
      doc(db, 'users', uid),
      {
        userId: uid,
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

export async function signInWithAccount(email: string, password: string, displayName?: string, action: string = 'login'): Promise<any> {
  const cleanEmail = String(email || '').trim().toLowerCase();
  const cleanPassword = String(password || '').trim();
  if (!cleanEmail.includes('@')) {
    throw new Error('Please enter a valid email address.');
  }
  if (!cleanPassword || cleanPassword.length < (action === 'register' ? 6 : 4)) {
    throw new Error(action === 'register' ? 'Password must be at least 6 characters.' : 'Password must be at least 4 characters.');
  }

  const res = await fetch('/api/auth/account-login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: cleanEmail, password: cleanPassword, displayName, action })
  });

  const data = await res.json();
  if (!res.ok || !data.ok || !data.user) {
    throw new Error(data.error || 'Authentication failed. Please check your credentials.');
  }

  return await applyVerifiedGoogleUser(data.user);
}

export async function registerAccount(email: string, password: string, displayName?: string): Promise<any> {
  return signInWithAccount(email, password, displayName, 'register');
}

export async function instantCloudSync(): Promise<any> {
  try {
    const res = await fetch('/api/auth/instant-connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const data = await res.json();
    if (data && data.ok && data.user) {
      return await applyVerifiedGoogleUser(data.user);
    }
  } catch (err) {}

  const fallbackUser = {
    uid: 'acct_cloud_sync_default',
    googleSub: 'acct_cloud_sync_default',
    email: 'cloud_sync@sync.internal',
    displayName: 'Cloud User',
    photoURL: '',
    verified: true,
    authMethod: 'instant_cloud',
    authenticatedAt: new Date().toISOString()
  };
  return await applyVerifiedGoogleUser(fallbackUser);
}

let pendingSyncPopupWin: Window | null = null;
let isResolverPatched = false;

export function prewarmGoogleAuthPopup() {
  try {
    const resolver = (auth as any)._popupRedirectResolver;
    if (!resolver) return;
    const proto = Object.getPrototypeOf(resolver);

    const bypassOriginValidation = () => Promise.resolve();
    const bypassWebStorageCheck = (_authInst: any, cb: (supported: boolean) => void) => {
      cb(true);
    };

    resolver._originValidation = bypassOriginValidation;
    resolver._isIframeWebStorageSupported = bypassWebStorageCheck;
    if (proto) {
      proto._originValidation = bypassOriginValidation;
      proto._isIframeWebStorageSupported = bypassWebStorageCheck;
    }

    if (typeof resolver._initialize === 'function') {
      resolver._initialize(auth).catch(() => {});
    }

    if (!isResolverPatched && typeof resolver._openPopup === 'function') {
      isResolverPatched = true;
      const origOpenPopup = resolver._openPopup.bind(resolver);
      resolver._openPopup = async function (authInst: any, providerInst: any, authType: any, eventId: any) {
        const winToUse = pendingSyncPopupWin && !pendingSyncPopupWin.closed ? pendingSyncPopupWin : null;
        pendingSyncPopupWin = null;
        const origWinOpen = window.open;
        window.open = function (url?: string | URL, target?: string, features?: string) {
          const finalUrl = url ? rewriteFirebaseAuthHandlerUrl(String(url)) : '';
          if (winToUse && !winToUse.closed) {
            if (finalUrl) {
              try {
                winToUse.location.replace(finalUrl);
              } catch (e) {
                winToUse.location.href = finalUrl;
              }
            }
            try {
              winToUse.focus();
            } catch (e) {}
            return winToUse;
          }
          return origWinOpen.call(window, finalUrl || url, target, features);
        } as any;
        try {
          return await origOpenPopup(authInst, providerInst, authType, eventId);
        } finally {
          window.open = origWinOpen;
        }
      };
    }
  } catch (e) {}
}

prewarmGoogleAuthPopup();

export async function signInWithGoogle(): Promise<any> {
  prewarmGoogleAuthPopup();

  // Open the popup window synchronously on the user click gesture so mobile & desktop popup blockers never block it
  try {
    if (pendingSyncPopupWin && !pendingSyncPopupWin.closed) {
      try {
        pendingSyncPopupWin.close();
      } catch (e) {}
    }
    const width = 500;
    const height = 620;
    const top = Math.max(((window.screen.availHeight || 800) - height) / 2, 0);
    const left = Math.max(((window.screen.availWidth || 1000) - width) / 2, 0);
    const features = `width=${width},height=${height},top=${top},left=${left},location=yes,resizable=yes,statusbar=yes,toolbar=no,scrollbars=yes`;
    pendingSyncPopupWin = window.open('about:blank', 'google_account_chooser_' + Date.now(), features);
  } catch (e) {
    pendingSyncPopupWin = null;
  }

  try {
    const provider = new GoogleAuthProvider();
    provider.addScope('email');
    provider.addScope('profile');
    provider.setCustomParameters({ prompt: 'select_account' });

    const cred = await signInWithPopup(auth, provider);
    if (cred && cred.user && cred.user.email) {
      const cleanEmail = cred.user.email.trim().toLowerCase();
      const oauthCred = GoogleAuthProvider.credentialFromResult(cred);
      const verifiedUser = {
        uid: cred.user.uid,
        googleSub: cred.user.uid,
        email: cleanEmail,
        displayName: cred.user.displayName || cleanEmail.split('@')[0],
        photoURL: cred.user.photoURL || '',
        idToken: oauthCred?.idToken || '',
        accessToken: oauthCred?.accessToken || '',
        verified: true,
        authMethod: 'google_popup',
        authenticatedAt: new Date().toISOString()
      };
      return await applyVerifiedGoogleUser(verifiedUser);
    }
  } catch (popupErr: any) {
    if (pendingSyncPopupWin && !pendingSyncPopupWin.closed) {
      try {
        pendingSyncPopupWin.close();
      } catch (e) {}
    }
    pendingSyncPopupWin = null;
    throw popupErr;
  }

  throw new Error('Google sign-in was cancelled.');
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
  prewarmGoogleAuthPopup,
  instantCloudSync,
  signInWithAccount,
  registerAccount,
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
