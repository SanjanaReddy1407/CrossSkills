/* ============================================================
   chat.js — app/chat.html
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('chat');
  renderChatPage();
});

function renderChatPage(){
  const s = Store.get();
  const wrap = document.getElementById('chat-wrap');

  if(!s.connections.length){
    wrap.innerHTML = `<div class="empty"><h4>No conversations yet</h4><p>Accept a request to unlock chat with that student.</p></div>`;
    return;
  }

  if(!s.activeChatId || !s.connections.some(c => c.peer.id === s.activeChatId)){
    Store.update(state => { state.activeChatId = state.connections[0].peer.id; });
  }
  const active = Store.get().connections.find(c => c.peer.id === Store.get().activeChatId).peer;
  const msgs = s.chats[active.id] || [];

  wrap.innerHTML = `
    <div class="chat-shell">
      <div class="chat-list">
        ${s.connections.map(c => `
          <button class="chat-list-item ${c.peer.id === active.id ? 'active' : ''}" onclick="openChatWith(${c.peer.id})">
            <div class="avatar">${initials(c.peer.name)}</div>
            <div><div class="cli-name">${c.peer.name}</div><div class="cli-snippet">${(s.chats[c.peer.id] || []).slice(-1)[0]?.text || 'No messages yet'}</div></div>
          </button>`).join('')}
      </div>
      <div class="chat-main">
        <div class="chat-header">
          <div><div style="font-weight:600;">${active.name}</div><div class="pair">${active.offered[0].skill} ⇄ ${active.desired[0].skill}</div></div>
          <button class="btn btn-outline btn-sm" onclick="jumpToSchedule(${active.id})">Schedule session</button>
        </div>
        <div class="chat-feed" id="chat-feed">
          ${msgs.length ? msgs.map(m => `<div class="msg ${m.from === 'me' ? 'me' : 'them'}">${m.text}<span class="ts">${m.ts}</span></div>`).join('') : '<div class="empty" style="padding:30px;"><p>No messages yet. Start the conversation.</p></div>'}
        </div>
        <div class="chat-input-bar">
          <input id="chat-input" placeholder="Write a message…" onkeydown="if(event.key==='Enter') sendMsg(${active.id})">
          <button class="btn btn-brass btn-sm" onclick="sendMsg(${active.id})">Send</button>
        </div>
      </div>
    </div>
  `;
  const feed = document.getElementById('chat-feed');
  if(feed) feed.scrollTop = feed.scrollHeight;
}

function openChatWith(peerId){
  Store.update(s => { s.activeChatId = peerId; });
  renderChatPage();
}

function sendMsg(peerId){
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if(!text) return;
  Store.update(s => {
    s.chats[peerId] = s.chats[peerId] || [];
    s.chats[peerId].push({ from: 'me', text, ts: 'Just now' });
  });
  input.value = '';
  renderChatPage();
}

function jumpToSchedule(peerId){
  Store.update(s => { s.activeChatId = peerId; });
  location.href = 'schedule.html';
}
