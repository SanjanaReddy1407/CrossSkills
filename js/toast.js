/* ============================================================
   toast.js — small bottom notification.
   Every page must include: <div id="toast"><span class="dot"></span><span id="toast-msg"></span></div>
   ============================================================ */
let __toastTimer;
function toast(msg){
  const el = document.getElementById('toast');
  const label = document.getElementById('toast-msg');
  if(!el || !label) return;
  label.textContent = msg;
  el.classList.add('show');
  clearTimeout(__toastTimer);
  __toastTimer = setTimeout(() => el.classList.remove('show'), 2600);
}
