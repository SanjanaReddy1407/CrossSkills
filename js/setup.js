/* ============================================================
   setup.js — profile-setup.html
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  if(!requireAuth('login.html')) return;
  renderChips();
});

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

function renderChips(){
  const s = Store.get();
  const off = document.getElementById('offered-chips');
  const des = document.getElementById('desired-chips');
  off.innerHTML = s.me.offered.map((sk, i) =>
    `<div class="chip">${sk.skill} <span class="lvl">${sk.level}</span> <button onclick="removeSkill('offered',${i})">×</button></div>`
  ).join('') || '<span style="font-size:12.5px;color:var(--ink-70);">No offered skills yet.</span>';
  des.innerHTML = s.me.desired.map((sk, i) =>
    `<div class="chip">${sk.skill} <span class="lvl">${sk.level}</span> <button onclick="removeSkill('desired',${i})">×</button></div>`
  ).join('') || '<span style="font-size:12.5px;color:var(--ink-70);">No desired skills yet.</span>';
}

function finishSetup(){
  const s = Store.get();
  if(s.me.offered.length === 0 || s.me.desired.length === 0){
    toast('Add at least one offered and one desired skill.');
    return;
  }

  Store.update(state => {
    state.profileComplete = true;
    // Seed one demo incoming request so Requests isn't empty on first visit.
    if(state.requests.incoming.length === 0){
      state.requests.incoming.push({
        id: Date.now(),
        from: { id: 4, name: "Sana Iqbal", uni: "SPPU", rating: 5.0, reviews: 9,
                 offered: [{ skill: "Public Speaking", cat: "Communication", level: "Advanced" }],
                 desired: [{ skill: "Python", cat: "Programming", level: "Advanced" }] },
        theirOffer: "Public Speaking · Advanced",
        theirWant: "Python · Advanced",
        matchPct: 81
      });
    }
  });

  toast('Profile saved — matches are ready.');
  setTimeout(() => { location.href = 'app/discover.html'; }, 400);
}
