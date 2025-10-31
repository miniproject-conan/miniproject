// ==== 글로벌: 캐시된 옛 스크립트/다른 코드에서 res.json() 터지는 것 잡기 ====
window.addEventListener('unhandledrejection', (e) => {
  console.warn('[UnhandledRejection]', e.reason);
});
window.addEventListener('error', (e) => {
  console.warn('[WindowError]', e.message);
});

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  if (!form) return;

  if (document.getElementById('pw2')) form.addEventListener('submit', handleSignup);
  else form.addEventListener('submit', handleLogin);
});

// JSON이 아닐 때는 절대 json() 호출 안 함
async function readBodySafely(res) {
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    try {
      return await res.json();
    } catch (err) {
      // 혹시나 서버가 content-type은 json인데 실제로는 html/text를 보낸 경우 방어
      const text = await res.text();
      return { __nonJson__: true, raw: text };
    }
  }
  return await res.text();
}

// 공통: 응답 디버그 출력
function debugResponse(where, res, body) {
  const ct = res.headers.get('content-type') || '';
  const snippet = typeof body === 'string' ? body.slice(0, 200) : JSON.stringify(body).slice(0, 200);
  console.log(`[${where}] status=${res.status} ${res.statusText} ct=${ct} body^200=`, snippet);
}

// ----- 로그인 -----
async function handleLogin(e) {
  e.preventDefault();
  // const name = document.getElementById('name').value.trim();
  const id = document.getElementById('id').value.trim();
  const pw = document.getElementById('pw').value.trim();
  if (!id || !pw) return alert('아이디와 비밀번호를 입력하세요.');

  try {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      credentials: 'include', // 백엔드가 쿠키로 토큰 관리한다 했으니 필수
      body: JSON.stringify({ login_id: id, password: pw }),
    });

    const body = await readBodySafely(res);
    debugResponse('login', res, body);

    if (!res.ok) {
      const msg = typeof body === 'string'
        ? body
        : (body?.detail || (body?.__nonJson__ ? body.raw : '로그인 실패'));
      throw new Error(msg);
    }

    alert('로그인 성공!');
    window.location.href = '/';
  } catch (err) {
    alert(err?.message || '로그인 중 오류가 발생했습니다.');
  }
}

// ----- 회원가입 -----
async function handleSignup(e) {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const id = document.getElementById('id').value.trim();
  const pw = document.getElementById('pw').value.trim();
  const pw2 = document.getElementById('pw2').value.trim();

  if (!name || !id || !pw || !pw2) return alert('모든 필드를 입력해주세요.');
  if (pw !== pw2) return alert('비밀번호가 일치하지 않습니다.');

  try {
    const res = await fetch('/api/v1/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username: name, login_id: id, password: pw }),
    });

    const body = await readBodySafely(res);
    debugResponse('signup', res, body);

    if (!res.ok) {
      const msg = typeof body === 'string'
        ? body
        : (body?.detail || (body?.__nonJson__ ? body.raw : '회원가입 실패'));
      throw new Error(msg);
    }

    alert('회원가입 완료!');
    window.location.href = '/api/v1/auth/login';
  } catch (err) {
    alert(err?.message || '회원가입 중 오류가 발생했습니다.');
  }
}
