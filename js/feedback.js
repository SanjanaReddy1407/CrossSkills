/* ============================================================
   feedback.js — app/feedback.html
   ============================================================ */
let starPick = 0;
let __fbTarget = null;

document.addEventListener('DOMContentLoaded', () => {
  if(!requireAuth('../login.html')) return;
  if(!requireProfile('../profile-setup.html')) return;
  renderNav('feedback');
  renderFeedbackPage();
});

function renderFeedbackPage(){
  const s = Store.get();
  __fbTarget = s.pendingFeedbackFor || (s.connections[0] && s.connections[0].peer) || null;
  const box = document.getElementById('fb-wrap');

  if(!__fbTarget){
    box.innerHTML = `<div class="empty"><h4>Nothing to review yet</h4><p>Complete a scheduled session to leave feedback.</p></div>`;
    return;
  }

  box.innerHTML = `
    <div class="fb-box">
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
        <div class="avatar">${initials(__fbTarget.name)}</div>
        <div><div style="font-weight:600;">${__fbTarget.name}</div><div style="font-size:12px; color:var(--ink-70);">Reviewer: ${s.me.name}</div></div>
      </div>
      <label style="display:block; font-size:12px; font-weight:600; margin-top:20px; text-transform:uppercase; letter-spacing:.06em; color:var(--ink-70);">Rating</label>
      <div class="star-input" id="star-input">
        ${[1, 2, 3, 4, 5].map(n => `<span data-n="${n}" onclick="setStar(${n})">★</span>`).join('')}
      </div>
      <div class="field"><label>Written feedback</label><textarea id="fb-text" rows="4" placeholder="Very helpful session. The explanation was clear and easy to understand."></textarea></div>
      <button class="btn btn-brass" style="width:100%;" onclick="submitFeedback()">Submit feedback & complete swap</button>
    </div>
  `;
  starPick = 0;
}

function setStar(n){
  starPick = n;
  document.querySelectorAll('#star-input span').forEach(el => el.classList.toggle('on', parseInt(el.dataset.n) <= n));
}

function submitFeedback(){
  if(starPick === 0){ toast('Pick a star rating first.'); return; }
  const text = document.getElementById('fb-text').value.trim();

  Store.update(s => {
    s.feedbackGiven.push({ peerId: __fbTarget.id, stars: starPick, text });
    s.me.reviewCount += 1;
    s.me.avgRating = ((s.me.avgRating * (s.me.reviewCount - 1)) + starPick) / s.me.reviewCount;
    s.pendingFeedbackFor = null;
  });

  toast('Feedback submitted — thanks!');
  setTimeout(() => { location.href = 'profile.html'; }, 400);
}
