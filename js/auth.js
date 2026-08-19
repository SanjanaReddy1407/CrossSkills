/* ============================================================
   auth.js — login.html + signup.html
   ============================================================ */

/* login.html: demo account — seeds Aditi Rao if this browser has no
   profile yet, otherwise just re-authenticates whatever is stored. */
function loginExisting(){
  const s = Store.get();
  Store.update(state => {
    state.authed = true;
    if(!state.me.name){
      state.me.name = "Aditi Rao";
      state.me.email = "aditi.rao@campus.edu";
      state.me.offered = [{ skill: "Python", cat: "Programming", level: "Advanced" }];
      state.me.desired = [{ skill: "React", cat: "Web Development", level: "Intermediate" }];
      state.profileComplete = true;
    }
  });
  toast('Welcome back, ' + (s.me.name.split(' ')[0] || 'student') + '.');
  setTimeout(() => {
    const s2 = Store.get();
    location.href = s2.profileComplete ? 'app/discover.html' : 'profile-setup.html';
  }, 400);
}

/* signup.html: creates a blank profile, sends the student to setup. */
function signupNew(){
  const name = document.getElementById('su-name').value.trim();
  const email = document.getElementById('su-email').value.trim();

  if(!name){ markError('su-name', 'Enter your full name.'); return; }
  if(!email){ markError('su-email', 'Enter your student email.'); return; }

  Store.update(state => {
    state.authed = true;
    state.profileComplete = false;
    state.me.name = name;
    state.me.email = email;
    state.me.offered = [];
    state.me.desired = [];
  });

  toast('Account created — let’s set up your skills.');
  setTimeout(() => { location.href = 'profile-setup.html'; }, 400);
}

function markError(fieldId, msg){
  const field = document.getElementById(fieldId).closest('.field');
  field.classList.add('error');
  const err = field.querySelector('.field-err');
  if(err) err.textContent = msg;
}
