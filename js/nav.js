/* ============================================================
   nav.js — renders the left rail nav into <aside id="rail"></aside>
   Call renderNav('discover' | 'matches' | 'requests' | 'chat' |
                   'schedule' | 'feedback' | 'profile') on each app page.
   ============================================================ */
function initials(name){
  if(!name) return "—";
  return name.split(" ").map(w => w[0]).slice(0, 2).join("").toUpperCase();
}

function renderNav(activePage){
  const s = Store.get();
  const rail = document.getElementById('rail');
  if(!rail) return;

  const reqCount = s.requests.incoming.length;

  rail.innerHTML = `
    <div class="logo"><span class="mark"></span>CrossSkill</div>
    <div class="rail-nav">
      <a class="rail-item ${activePage === 'discover' ? 'active' : ''}" href="discover.html"><span class="ic">⌕</span>Discover</a>
      <a class="rail-item ${activePage === 'matches' ? 'active' : ''}" href="recommendations.html"><span class="ic">✦</span>Recommendations</a>
      <a class="rail-item ${activePage === 'requests' ? 'active' : ''}" href="requests.html"><span class="ic">⇄</span>Requests${reqCount ? `<span class="badge-count">${reqCount}</span>` : ''}</a>
      <a class="rail-item ${activePage === 'chat' ? 'active' : ''}" href="chat.html"><span class="ic">✉</span>Chat</a>
      <a class="rail-item ${activePage === 'schedule' ? 'active' : ''}" href="schedule.html"><span class="ic">▤</span>Schedule</a>
      <a class="rail-item ${activePage === 'feedback' ? 'active' : ''}" href="feedback.html"><span class="ic">★</span>Feedback</a>
      <a class="rail-item ${activePage === 'profile' ? 'active' : ''}" href="profile.html"><span class="ic">◎</span>Profile</a>
    </div>
    <div class="rail-foot">
      <div class="rail-user">
        <div class="avatar">${initials(s.me.name)}</div>
        <div><div class="name">${s.me.name || 'Student'}</div><div class="role">Student</div></div>
      </div>
    </div>
  `;
}

function logout(){
  Store.reset();
  location.href = '../index.html';
}
