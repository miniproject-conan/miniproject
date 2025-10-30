document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.theme-btn')?.forEach(b => {
    b.addEventListener('click', () => {
      document.body.dataset.theme = b.dataset.theme;
    });
  });

  const form = document.querySelector('form');
  if (!form) return;

  if (document.getElementById('pw2')) form.addEventListener('submit', handleSignup);
  else form.addEventListener('submit', handleLogin);
});

async function handleLogin(e) {
  e.preventDefault();
  const id = document.getElementById('id').value.trim();
  const pw = document.getElementById('pw').value.trim();

  if (!id || !pw) return alert('아이디와 비밀번호를 입력하세요.');

  try {
    const res = await fetch(`/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ login_id: id, password: pw }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || '로그인 실패');
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    alert('로그인 성공!');
    window.location.href = '/';
  } catch (err) {
    alert(err.message);
  }
}

async function handleSignup(e) {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const id = document.getElementById('id').value.trim();
  const pw = document.getElementById('pw').value.trim();
  const pw2 = document.getElementById('pw2').value.trim();

  if (!name || !id || !pw || !pw2) return alert('모든 필드를 입력해주세요.');
  if (pw !== pw2) return alert('비밀번호가 일치하지 않습니다.');

  try {
    const res = await fetch(`/api/v1/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: name, login_id: id, password: pw }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || '회원가입 실패');
    alert('회원가입 완료!');
    window.location.href = '/api/v1/auth/login';
  } catch (err) {
    alert(err.message);
  }
}
