// =======================
//  공용: 테마 토글 유지
// =======================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.theme-btn').forEach(b => {
    b.addEventListener('click', () => {
      document.body.dataset.theme = b.dataset.theme;
    });
  });

  // 현재 페이지가 로그인인지 회원가입인지 자동 감지
  const pw2 = document.getElementById('pw2');
  const form = document.querySelector('form');
  if (!form) return;

  if (pw2) {
    // 회원가입 페이지
    form.addEventListener('submit', handleSignup);
  } else {
    // 로그인 페이지
    form.addEventListener('submit', handleLogin);
  }
});

// =======================
//  API 연결 설정
// =======================
const BASE_URL = 'http://127.0.0.1:8000/api/v1';

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data?.detail || data?.message || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

// =======================
//  입력 검증 (기존 checkInput 대체)
// =======================
function getInputs() {
  return {
    nameInput: document.getElementById('name'),
    idInput: document.getElementById('id'),
    pwInput: document.getElementById('pw'),
    pwInput2: document.getElementById('pw2'),
  };
}
function validateCommon() {
  const { nameInput, idInput, pwInput } = getInputs();
  if (!nameInput?.value) { alert('이름을 입력해주세요'); nameInput?.focus(); return false; }
  if (!idInput?.value)   { alert('아이디를 입력해주세요'); idInput?.focus(); return false; }
  if (!pwInput?.value)   { alert('비밀번호를 입력해주세요'); pwInput?.focus(); return false; }
  return true;
}
function validateSignup() {
  const { pwInput, pwInput2 } = getInputs();
  if (!validateCommon()) return false;
  if (!pwInput2?.value) { alert('비밀번호 확인을 입력해주세요'); pwInput2?.focus(); return false; }
  if (pwInput.value !== pwInput2.value) { alert('비밀번호가 일치하지 않습니다'); pwInput2.focus(); return false; }
  return true;
}

// =======================
//  로컬 스토리지 토큰 관리
// =======================
function saveTokens({ access_token, refresh_token }) {
  localStorage.setItem('access_token', access_token);
  if (refresh_token) localStorage.setItem('refresh_token', refresh_token);
}
function getAccessToken() {
  return localStorage.getItem('access_token');
}
function clearTokens() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

// =======================
//  이벤트 핸들러
// =======================
async function handleLogin(e) {
  e.preventDefault();
  const { nameInput, idInput, pwInput } = getInputs();
  if (!validateCommon()) return;

  // 백엔드 로그인 스펙: login_id 또는 username + password
  // 우리는 login_id=idInput, username=nameInput 둘 다 보낼 수 있지만
  // 우선 login_id 기준으로 시도 (백엔드 구현과 일치)
  try {
    const data = await fetchJSON(`${BASE_URL}/auth/login`, {
      method: 'POST',
      body: JSON.stringify({
        login_id: idInput.value,
        // username: nameInput.value, // 필요시 동시 제공 가능
        password: pwInput.value,
      }),
    });
    saveTokens(data);
    alert('로그인 성공!');
    // 로그인 후 보호 API 테스트 예시 (/auth/me)
    tryMePing();
  } catch (err) {
    alert(`로그인 실패: ${err.message}`);
  }
}

async function handleSignup(e) {
  e.preventDefault();
  const { nameInput, idInput, pwInput } = getInputs();
  if (!validateSignup()) return;

  try {
    await fetchJSON(`${BASE_URL}/auth/signup`, {
      method: 'POST',
      body: JSON.stringify({
        username: nameInput.value,   // 모델의 username
        login_id: idInput.value,     // 모델의 login_id
        password: pwInput.value,
      }),
    });
    alert('회원가입 완료! 이제 로그인해 주세요.');
    // 회원가입 완료 후 로그인 페이지로 이동
    window.location.href = 'login.html';
  } catch (err) {
    alert(`회원가입 실패: ${err.message}`);
  }
}

// =======================
//  보호 API 샘플 (/auth/me)
// =======================
async function tryMePing() {
  const token = getAccessToken();
  if (!token) return;
  try {
    const me = await fetch(`${BASE_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(r => r.json());
    console.log('ME:', me);
    // 원하는 페이지로 이동하거나 화면 반영
    // window.location.href = 'index.html';
  } catch (e) {
    console.warn('me 호출 실패', e);
  }
}

// =======================
//  로그아웃(원하면 버튼에 연결)
// =======================
function logout() {
  clearTokens();
  alert('로그아웃 되었습니다');
  // window.location.href = 'login.html';
}
window.logout = logout;
