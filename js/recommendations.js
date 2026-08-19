/* ============================================================
   recommendations.js — app/recommendations.html
   ============================================================ */
document.addEventListener('DOMContentLoaded', async () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('matches');

  const students = await fetch('../data/students.json').then(r => r.json());
  renderRanked(students);
});

function renderRanked(students){
  const s = Store.get();
  const ranked = students
    .map(c => ({ c, m: computeMatch(s.me, c) }))
    .sort((a, b) => b.m.score - a.m.score);

  document.getElementById('rec-list').innerHTML = ranked.map(({ c, m }) => {
    const already = s.requests.sent.some(r => r.to.id === c.id) || s.connections.some(x => x.peer.id === c.id);
    return `
      <div class="match-card">
        <div class="match-stamp"><b>${m.score}%</b><span>MATCH</span></div>
        <div class="match-body">
          <div class="mname">${c.name} <span style="font-weight:400; font-size:12.5px; color:var(--ink-70);">· ${c.uni}</span></div>
          <div class="exchange-lines">
            ${m.lines.map(l => `<div class="exchange-line"><span class="${l.ok ? 'check' : 'cross'}">${l.ok ? '✓' : '✕'}</span>${l.text}</div>`).join('')}
          </div>
          <div style="margin-top:10px;" class="stars">${'★'.repeat(Math.round(c.rating))}${'☆'.repeat(5 - Math.round(c.rating))} <span class="mono" style="color:var(--ink-70); font-size:11.5px;">${c.rating.toFixed(1)} (${c.reviews})</span> ${m.mutual ? '<span class="status-badge status-active" style="margin-left:8px;">MUTUAL SWAP</span>' : ''}</div>
        </div>
        <div class="match-actions">
          <button class="btn btn-brass btn-sm" ${already ? 'disabled' : ''} onclick="connectFrom(${c.id})">${already ? 'Requested' : 'Connect'}</button>
        </div>
      </div>`;
  }).join('');

  window.__recStudents = students;
}

function connectFrom(candId){
  const cand = window.__recStudents.find(c => c.id === candId);
  Store.update(s => { s.requests.sent.push({ id: Date.now(), to: cand, status: 'PENDING' }); });
  toast(`Request sent to ${cand.name}.`);
  renderRanked(window.__recStudents);
  renderNav('matches');
}
