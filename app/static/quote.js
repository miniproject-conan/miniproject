console.log("[loaded] quote.js");

// API prefix는 고정: 백엔드 구조에 맞게 /api/v1
window.API_BASE = window.API_BASE || "/api/v1";

const quoteMessage = document.getElementById("quoteMessage");
const quoteAuthor = document.getElementById("quoteAuthor");
const bookmarkBtn = document.getElementById("bookmarkBtn");
const refreshBtn = document.getElementById("refreshBtn");

let currentQuote = null;

// ------------------- 공통 fetch -------------------
async function apiFetch(url, options = {}) {
  const res = await fetch(url, { ...options, credentials: "include" }); // 쿠키 포함
  if (res.status === 401) {
    const data = await res.json().catch(() => ({}));
    if (data.detail === "Access token expired") {
      console.warn("⏳ Access 토큰 만료 → Refresh 요청 중...");
      const refreshRes = await fetch(`${API_BASE}/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });
      if (refreshRes.ok) {
        console.log("토큰 갱신 성공, 요청 재시도");
        return apiFetch(url, options);
      } else {
        alert("세션이 만료되었습니다. 다시 로그인해주세요.");
        // view 라우터 기준: /login 으로 이동
        window.location.href = "/login";
        return;
      }
    }
  }
  return res;
}

// ------------------- 명언 불러오기 -------------------
async function fetchRandomQuote() {
  try {
    quoteMessage.innerHTML =
      '<i class="fa-solid fa-spinner fa-spin"></i> 불러오는 중...';
    quoteAuthor.textContent = "";

    const res = await apiFetch(`${API_BASE}/quote`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    currentQuote = data.data;

    quoteMessage.textContent = `"${currentQuote.message}"`;
    quoteAuthor.textContent = `– ${currentQuote.author}`;

    await checkIfBookmarked();
  } catch (err) {
    console.error("명언 불러오기 실패:", err);
    quoteMessage.textContent = "명언을 불러오지 못했습니다.";
  }
}

// ------------------- 북마크 추가 -------------------
async function addBookmark() {
  const icon = bookmarkBtn.querySelector(".heart-icon");

  try {
    const res = await apiFetch(`${API_BASE}/bookmark`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quote_id: currentQuote.id }),
    });

    if (res.status === 201) {
      bookmarkBtn.classList.add("active");
      icon.classList.replace("fa-regular", "fa-solid");
      console.log("북마크 추가 완료");

      // 0.3초 후 북마크 목록 강제 갱신
      setTimeout(() => {
        if (typeof window.fetchBookmarks === "function") {
          console.log("[자동 새로고침] fetchBookmarks()");
          window.fetchBookmarks();
        }
      }, 300);
    } else if (res.status === 409) {
      alert("이미 북마크된 명언입니다!");
    } else {
      throw new Error(`HTTP ${res.status}`);
    }
  } catch (err) {
    console.error("북마크 추가 오류:", err);
    alert("북마크 추가 중 문제가 발생했습니다.");
  }
}

// ------------------- 북마크 여부 확인 -------------------
async function checkIfBookmarked() {
  if (!currentQuote) return;
  try {
    const res = await apiFetch(`${API_BASE}/bookmark`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    const items = data.items || data;
    const found = Array.isArray(items)
      ? items.some((b) => b.quote.id === currentQuote.id)
      : false;

    const icon = bookmarkBtn.querySelector(".heart-icon");
    if (found) {
      bookmarkBtn.classList.add("active");
      icon.classList.replace("fa-regular", "fa-solid");
    } else {
      bookmarkBtn.classList.remove("active");
      icon.classList.replace("fa-solid", "fa-regular");
    }
  } catch (err) {
    console.error("checkIfBookmarked 오류:", err);
  }
}

// ------------------- 이벤트 연결 -------------------
refreshBtn.addEventListener("click", fetchRandomQuote);
bookmarkBtn.addEventListener("click", addBookmark);
window.addEventListener("DOMContentLoaded", fetchRandomQuote);
