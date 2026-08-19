/* ============================================================
   requests.js — app/requests.html
   ============================================================ */
let requestsTab = 'incoming';

document.addEventListener('DOMContentLoaded', () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('requests');
  renderTabs();
  renderTabBody();
});

function setTab(tab){
  requestsTab = tab;
  renderTabs();
  renderTabBody();
}

function renderTabs(){
  const s = Store.get();
  document.getElementById('req-tabs').innerHTML = `
    <button class="req-tab ${requestsTab === 'incoming' ? 'active' : ''}" onclick="setTab('incoming')">Incoming (${s.requests.incoming.length})</button>
    <button class="req-tab ${requestsTab === 'sent' ? 'active' : ''}" onclick="setTab('sent')">Sent (${s.requests.sent.length})</button>
    <button class="req-tab ${requestsTab === 'active' ? 'active' : ''}" onclick="setTab('active')">Active (${s.connections.length})</button>
  `;
}

function renderTabBody(){
  const s = Store.get();
  const body = document.getElementById('req-body');
  if(requestsTab === 'incoming') body.innerHTML = renderIncoming(s);
  else if(requestsTab === 'sent') body.innerHTML = renderSent(s);
  else body.innerHTML = renderActive(s);
}

function emptyBlock(h, p){ return `<div class="empty"><h4>${h}</h4><p>${p}</p></div>`; }

function renderIncoming(s){
  if(!s.requests.incoming.length) return emptyBlock('No pending requests', 'New skill-swap proposals from other students will show up here.');
  return s.requests.incoming.map(r => `
    <div class="req-row">
      <div class="req-info">
        <div class="avatar">${initials(r.from.name)}</div>
        <div>
          <div style="font-weight:600; font-size:14.5px;">${r.from.name}</div>
          <div class="req-meta">Offers ${r.theirOffer} &nbsp;·&nbsp; Wants ${r.theirWant} &nbsp;·&nbsp; ${r.matchPct}% match</div>
        </div>
      </div>
      <div style="display:flex; gap:8px;">
        <button class="btn btn-danger btn-sm" onclick="respondRequest(${r.id}, false)">Reject</button>
        <button class="btn btn-brass btn-sm" onclick="respondRequest(${r.id}, true)">Accept</button>
      </div>
    </div>
  `).join('');
}

function renderSent(s){
  if(!s.requests.sent.length) return emptyBlock('No sent requests', 'Requests you send from Discover or Recommendations appear here with their status.');
  return s.requests.sent.map(r => `
    <div class="req-row">
      <div class="req-info">
        <div class="avatar">${initials(r.to.name)}</div>
        <div><div style="font-weight:600; font-size:14.5px;">${r.to.name}</div><div class="req-meta">Sent · awaiting response</div></div>
      </div>
      <span class="status-badge status-${r.status.toLowerCase()}">${r.status}</span>
    </div>
  `).join('');
}

function renderActive(s){
  if(!s.connections.length) return emptyBlock('No active connections', 'Once a request is accepted, you can chat and schedule a session here.');
  return s.connections.map(c => `
    <div class="req-row">
      <div class="req-info">
        <div class="avatar">${initials(c.peer.name)}</div>
        <div><div style="font-weight:600; font-size:14.5px;">${c.peer.name}</div><div class="req-meta">Connection active · ${c.peer.offered[0].skill} ⇄ ${c.peer.desired[0].skill}</div></div>
      </div>
      <div style="display:flex; gap:8px;">
        <button class="btn btn-outline btn-sm" onclick="openChatWith(${c.peer.id})">Chat</button>
      </div>
    </div>
  `).join('');
}

function openChatWith(peerId){
  Store.update(s => { s.activeChatId = peerId; });
  location.href = 'chat.html';
}

function respondRequest(reqId, accept){
  let target;
  Store.update(s => {
    const idx = s.requests.incoming.findIndex(r => r.id === reqId);
    const r = s.requests.incoming[idx];
    s.requests.incoming.splice(idx, 1);
    target = r;
    if(accept){
      s.connections.push({ id: Date.now(), peer: r.from });
      if(!s.chats[r.from.id]){
        s.chats[r.from.id] = [
          { from: 'them', text: `Hey! Excited to trade ${r.theirOffer.split(' · ')[0]} for some ${r.theirWant.split(' · ')[0]} help 🙂`, ts: 'Just now' }
        ];
      }
    }
  });

  toast(accept ? `Connection with ${target.from.name} is now active.` : `Request from ${target.from.name} rejected.`);
  renderNav('requests');
  renderTabs();
  requestsTab = accept ? 'active' : requestsTab;
  renderTabs();
  renderTabBody();
}
