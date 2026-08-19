/* ============================================================
   store.js — single source of truth, persisted to localStorage
   so state survives real page-to-page navigation.
   ============================================================ */
const STORE_KEY = 'crossskill_state_v1';

function defaultState(){
  return {
    authed: false,
    profileComplete: false,
    me: {
      name: "",
      email: "",
      uni: "Fergusson College",
      avgRating: 0,
      reviewCount: 0,
      offered: [],
      desired: []
    },
    requests: { incoming: [], sent: [] },
    connections: [],           // [{ id, peer }]
    chats: {},                 // peerId -> [{from:'me'|'them', text, ts}]
    schedules: [],             // [{ id, peer, slots, start, end, agenda, completed }]
    feedbackGiven: [],
    pendingFeedbackFor: null,
    activeChatId: null
  };
}

function loadState(){
  const raw = localStorage.getItem(STORE_KEY);
  if(raw){
    try { return JSON.parse(raw); } catch(e){ /* fall through to fresh state */ }
  }
  const fresh = defaultState();
  localStorage.setItem(STORE_KEY, JSON.stringify(fresh));
  return fresh;
}

function saveState(state){
  localStorage.setItem(STORE_KEY, JSON.stringify(state));
}

const Store = {
  get(){ return loadState(); },
  set(state){ saveState(state); },
  update(fn){
    const s = loadState();
    fn(s);
    saveState(s);
    return s;
  },
  reset(){ localStorage.removeItem(STORE_KEY); }
};

/* Redirect helpers used at the top of every protected page. */
function requireAuth(loginPath){
  const s = Store.get();
  if(!s.authed){ location.href = loginPath; return null; }
  return s;
}
function requireProfile(setupPath){
  const s = Store.get();
  if(!s.profileComplete){ location.href = setupPath; return null; }
  return s;
}
