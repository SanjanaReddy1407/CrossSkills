/* ============================================================
   discover.js — app/discover.html
   ============================================================ */
let __students = [];
let discoverQuery = '';
let discoverCat = 'All';

document.addEventListener('DOMContentLoaded', async () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('discover');

  const [students, categories] = await Promise.all([
    fetch('../data/students.json').then(r => r.json()),
    fetch('../data/categories.json').then(r => r.json())
  ]);
  __students = students;
  renderCategoryPills(categories);
  renderResults();

  document.getElementById('discover-search').addEventListener('input', e => {
    discoverQuery = e.target.value;
    renderResults();
  });
});

function renderCategoryPills(categories){
  const cats = ['All', ...categories];
  document.getElementById('pill-row').innerHTML = cats.map(c =>
    `<button class="pill ${c === discoverCat ? 'active' : ''}" onclick="setCategory('${c}')">${c}</button>`
  ).join('');
}

function setCategory(c){
  discoverCat = c;
  document.querySelectorAll('#pill-row .pill').forEach(p => p.classList.toggle('active', p.textContent === c));
  renderResults();
}

function renderResults(){
  const s = Store.get();
  const results = __students.filter(c => {
    const text = (c.name + ' ' + c.offered.map(o => o.skill).join(' ')).toLowerCase();
    const matchesQuery = discoverQuery === '' || text.includes(discoverQuery.toLowerCase());
    const matchesCat = discoverCat === 'All' || c.offered.some(o => o.cat === discoverCat) || c.desired.some(o => o.cat === discoverCat);
    return matchesQuery && matchesCat;
  });

  const grid = document.getElementById('result-grid');
  if(!results.length){
    grid.innerHTML = '';
    document.getElementById('discover-empty').style.display = 'block';
    return;
  }
  document.getElementById('discover-empty').style.display = 'none';
  grid.innerHTML = results.map(c => pcard(c, s)).join('');
}

function pcard(c, s){
  const already = s.requests.sent.some(r => r.to.id === c.id) || s.connections.some(x => x.peer.id === c.id);
  return `
  <div class="pcard">
    <div class="pcard-top">
      <div class="avatar">${initials(c.name)}</div>
      <div><div class="pcard-name">${c.name}</div><div class="pcard-uni">${c.uni}</div></div>
    </div>
    <div class="pcard-skills">
      <div class="skillrow"><span class="lbl">Offers</span><span class="val">${c.offered[0].skill} · ${c.offered[0].level}</span></div>
      <div class="skillrow"><span class="lbl">Wants</span><span class="val">${c.desired[0].skill} · ${c.desired[0].level}</span></div>
    </div>
    <div class="pcard-foot">
      <span class="stars">${'★'.repeat(Math.round(c.rating))}${'☆'.repeat(5 - Math.round(c.rating))} <span class="mono" style="color:var(--ink-70); font-size:11.5px;">${c.rating.toFixed(1)}</span></span>
      <button class="btn btn-outline btn-sm" ${already ? 'disabled' : ''} onclick="sendRequest(${c.id})">${already ? 'Sent' : 'Send request'}</button>
    </div>
  </div>`;
}

function sendRequest(candId){
  const cand = __students.find(c => c.id === candId);
  Store.update(s => { s.requests.sent.push({ id: Date.now(), to: cand, status: 'PENDING' }); });
  toast(`Request sent to ${cand.name}.`);
  renderResults();
  renderNav('discover');
}
