/* ============================================================
   profile.js — app/profile.html
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('profile');
  renderProfilePage();
});

function renderProfilePage(){
  const s = Store.get();

  document.getElementById('profile-avatar').textContent = initials(s.me.name);
  document.getElementById('profile-name').textContent = s.me.name;
  document.getElementById('profile-meta').textContent = `${s.me.email} · ${s.me.uni}`;
  document.getElementById('stat-rating').textContent = s.me.reviewCount ? s.me.avgRating.toFixed(1) : '—';
  document.getElementById('stat-reviews').textContent = s.me.reviewCount;
  document.getElementById('stat-connections').textContent = s.connections.length;

  renderChips();
}

function renderChips(){
  const s = Store.get();
  document.getElementById('offered-chips').innerHTML = chipsHTML(s.me.offered, 'offered');
  document.getElementById('desired-chips').innerHTML = chipsHTML(s.me.desired, 'desired');
}

function chipsHTML(arr, kind){
  if(!arr.length) return `<span style="font-size:12.5px;color:var(--ink-70);">None added yet.</span>`;
  return arr.map((sk, i) =>
    `<div class="chip">${sk.skill} <span class="lvl">${sk.level}</span> <button onclick="removeSkill('${kind}',${i})">×</button></div>`
  ).join('');
}

function addSkill(kind){
  const skill = document.getElementById(kind === 'offered' ? 'off-skill' : 'des-skill').value.trim();
  const cat = document.getElementById(kind === 'offered' ? 'off-cat' : 'des-cat').value;
  const lvl = document.getElementById(kind === 'offered' ? 'off-lvl' : 'des-lvl').value;
  if(!skill){ toast('Enter a skill name first.'); return; }

  Store.update(s => { s.me[kind].push({ skill, cat, level: lvl }); });
  document.getElementById(kind === 'offered' ? 'off-skill' : 'des-skill').value = '';
  renderChips();
}

function removeSkill(kind, idx){
  Store.update(s => { s.me[kind].splice(idx, 1); });
  renderChips();
}
