// Stock Research — Auth Gate
// Change credentials by updating the SHA-256 hashes below.
// To generate a new hash: echo -n "yourpassword" | shasum -a 256
const AUTH_KEY = 'sr_auth_v1';
const VALID_USER_HASH = 'b7ee66d972bbc9b1e7ec85e1e4d88304b99781182d121396c6acf69418394fe3'; // "nitish"
const VALID_PASS_HASH = 'fba90237ea4b87e3cd1e2dec197d887de0e51340f1d4a5cb0f26062eb809968c'; // "stocks2026"

async function sha256(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function isAuthed() {
  return sessionStorage.getItem(AUTH_KEY) === '1';
}

function buildOverlay() {
  const el = document.createElement('div');
  el.id = 'auth-overlay';
  el.innerHTML = `
    <div id="auth-box">
      <div id="auth-title">Stock Research</div>
      <div id="auth-sub">Private · Nitish</div>
      <input id="auth-user" type="text" placeholder="Username" autocomplete="username" />
      <input id="auth-pass" type="password" placeholder="Password" autocomplete="current-password" />
      <button id="auth-btn">Sign in</button>
      <div id="auth-err"></div>
    </div>`;

  const style = document.createElement('style');
  style.textContent = `
    #auth-overlay {
      position: fixed; inset: 0; z-index: 9999;
      background: #1a1a2e;
      display: flex; align-items: center; justify-content: center;
    }
    #auth-box {
      background: white; border-radius: 14px;
      padding: 36px 32px; width: 100%; max-width: 340px;
      display: flex; flex-direction: column; gap: 12px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    #auth-title {
      font-family: -apple-system, sans-serif;
      font-size: 1.3rem; font-weight: 700; color: #1a1a2e;
    }
    #auth-sub {
      font-family: -apple-system, sans-serif;
      font-size: 0.8rem; color: #999; margin-top: -6px; margin-bottom: 4px;
    }
    #auth-box input {
      font-family: -apple-system, sans-serif;
      padding: 11px 14px; border: 1px solid #ddd; border-radius: 8px;
      font-size: 0.95rem; outline: none; transition: border 0.15s;
    }
    #auth-box input:focus { border-color: #1a1a2e; }
    #auth-btn {
      font-family: -apple-system, sans-serif;
      padding: 12px; background: #1a1a2e; color: white;
      border: none; border-radius: 8px; font-size: 0.95rem;
      font-weight: 600; cursor: pointer; margin-top: 4px;
      transition: background 0.15s;
    }
    #auth-btn:hover { background: #2d2d4e; }
    #auth-err {
      font-family: -apple-system, sans-serif;
      font-size: 0.8rem; color: #dc2626;
      min-height: 18px; text-align: center;
    }
  `;

  document.head.appendChild(style);
  document.body.appendChild(el);

  const btn = document.getElementById('auth-btn');
  const err = document.getElementById('auth-err');

  async function tryLogin() {
    const u = document.getElementById('auth-user').value.trim();
    const p = document.getElementById('auth-pass').value;
    btn.textContent = '…';
    btn.disabled = true;

    const [uh, ph] = await Promise.all([sha256(u), sha256(p)]);

    if (uh === VALID_USER_HASH && ph === VALID_PASS_HASH) {
      sessionStorage.setItem(AUTH_KEY, '1');
      document.getElementById('auth-overlay').remove();
    } else {
      err.textContent = 'Incorrect username or password.';
      btn.textContent = 'Sign in';
      btn.disabled = false;
      document.getElementById('auth-pass').value = '';
      document.getElementById('auth-pass').focus();
    }
  }

  btn.addEventListener('click', tryLogin);
  document.getElementById('auth-pass').addEventListener('keydown', e => {
    if (e.key === 'Enter') tryLogin();
  });
  document.getElementById('auth-user').addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('auth-pass').focus();
  });

  // Focus username on load
  setTimeout(() => document.getElementById('auth-user').focus(), 50);
}

// Run on every page
if (!isAuthed()) {
  if (document.body) {
    buildOverlay();
  } else {
    document.addEventListener('DOMContentLoaded', buildOverlay);
  }
}
