console.log("[loaded] quote.js");

const quoteMessage = document.getElementById("quoteMessage");
const quoteAuthor  = document.getElementById("quoteAuthor");
const bookmarkBtn  = document.getElementById("bookmarkBtn");
const refreshBtn   = document.getElementById("refreshBtn");

let currentQuote = null;

async function fetchRandomQuote() {
  try {
    quoteMessage.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 불러오는 중...';
    quoteAuthor.textContent = "";

    const res = await fetch(`${API_BASE}/quote`);
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

async function addBookmark() {
  if (!TOKEN) return alert("로그인이 필요합니다.");
  const icon = bookmarkBtn.querySelector(".heart-icon");

  try {
    const res = await fetch(`${API_BASE}/bookmark`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${TOKEN}`
      },
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

async function checkIfBookmarked() {
  if (!TOKEN || !currentQuote) return;
  try {
    const res = await fetch(`${API_BASE}/bookmark`, {
      headers: { Authorization: `Bearer ${TOKEN}` },
    });
    const data = await res.json();
    const items = data.items || data;
    const found = items.some(b => b.quote.id === currentQuote.id);

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

refreshBtn.addEventListener("click", fetchRandomQuote);
bookmarkBtn.addEventListener("click", addBookmark);
window.addEventListener("DOMContentLoaded", fetchRandomQuote);
