/* ============================================================
   schedule.js — app/schedule.html
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('schedule');
  renderSchedulePage();
});

function renderSchedulePage(){
  const s = Store.get();
  const formBox = document.getElementById('sched-form');
  const listBox = document.getElementById('sched-list');

  if(!s.connections.length){
    formBox.innerHTML = `<h3 style="font-size:16px; margin-bottom:16px;">New session</h3><p style="font-size:13.5px; color:var(--ink-70);">You need an active connection before scheduling a session.</p>`;
  } else {
    const peerOptions = s.connections.map(c =>
      `<option value="${c.peer.id}" ${c.peer.id === s.activeChatId ? 'selected' : ''}>${c.peer.name}</option>`
    ).join('');
    formBox.innerHTML = `
      <h3 style="font-size:16px; margin-bottom:16px;">New session</h3>
      <div class="field"><label>Connected peer</label><select id="sc-peer">${peerOptions}</select></div>
      <div class="field"><label>Number of slots</label><input id="sc-slots" type="number" value="1" min="1"></div>
      <div class="field"><label>Start</label><input id="sc-start" type="datetime-local"></div>
      <div class="field"><label>End</label><input id="sc-end" type="datetime-local"></div>
      <div class="field"><label>Agenda</label><textarea id="sc-agenda" rows="3" placeholder="e.g. Introduction to React components and props"></textarea></div>
      <button class="btn btn-brass" style="width:100%;" onclick="createSchedule()">Confirm slot</button>
    `;
  }

  if(!s.schedules.length){
    listBox.innerHTML = `<h3 style="font-size:16px; margin-bottom:16px;">Upcoming sessions</h3><div class="empty"><h4>No sessions booked yet</h4><p>Fill out the form to schedule your first swap session.</p></div>`;
  } else {
    listBox.innerHTML = `<h3 style="font-size:16px; margin-bottom:16px;">Upcoming sessions</h3>` + s.schedules.map(sc => `
      <div class="sched-card">
        <div class="date-badge">${sc.start || 'TIME TBC'} — ${sc.end || ''}</div>
        <h4>${sc.peer.name} · ${sc.agenda ? sc.agenda.slice(0, 40) : 'Skill session'}</h4>
        <div class="agenda">${sc.agenda || 'No agenda added.'}</div>
        <div class="foot">
          <span class="mono" style="font-size:11.5px; color:var(--ink-70);">${sc.slots} slot(s)</span>
          ${sc.completed ? `<span class="status-badge status-completed">COMPLETED</span>` : `<button class="btn btn-outline btn-sm" onclick="completeSchedule(${sc.id})">Mark as completed</button>`}
        </div>
      </div>
    `).join('');
  }
}

function fmtDT(v){
  const d = new Date(v);
  return d.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function createSchedule(){
  const s = Store.get();
  const peerId = parseInt(document.getElementById('sc-peer').value);
  const peer = s.connections.find(c => c.peer.id === peerId).peer;
  const slots = document.getElementById('sc-slots').value;
  const start = document.getElementById('sc-start').value;
  const end = document.getElementById('sc-end').value;
  const agenda = document.getElementById('sc-agenda').value;

  if(!start || !end){ toast('Pick a start and end time.'); return; }
  if(new Date(end) <= new Date(start)){ toast('End time must be after start time.'); return; }

  Store.update(state => {
    state.schedules.unshift({ id: Date.now(), peer, slots, start: fmtDT(start), end: fmtDT(end), agenda, completed: false });
  });
  toast('Session scheduled with ' + peer.name + '.');
  renderSchedulePage();
}

function completeSchedule(id){
  let peer;
  Store.update(s => {
    const sc = s.schedules.find(x => x.id === id);
    sc.completed = true;
    peer = sc.peer;
    s.pendingFeedbackFor = peer;
  });
  toast('Session marked complete — leave feedback for ' + peer.name + '.');
  setTimeout(() => { location.href = 'feedback.html'; }, 400);
}
