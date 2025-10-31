console.log("[디버깅용] quote.js loaded");

const quoteMessage = document.getElementById("quoteMessage");
const quoteAuthor  = document.getElementById("quoteAuthor");
const bookmarkBtn  = document.getElementById("bookmarkBtn");
const refreshBtn   = document.getElementById("refreshBtn");

let currentQuote = null;

async function fetchRandomQuote() {
  try {
    quoteMessage.innerHTML = '<span class="loading-text"><i class="fa-solid fa-spinner fa-spin"></i> 불러오는 중...</span>';
    quoteAuthor.textContent = "";

    const res = await fetch(`${API_BASE}/quote`);
    const data = await res.json();
    currentQuote = data.data;
    quoteMessage.textContent = `"${currentQuote.message}"`;
    quoteAuthor.textContent = `– ${currentQuote.author}`;

    await checkIfBookmarked();
  } catch {
    quoteMessage.textContent = "명언을 불러오지 못했습니다.";
  }
}

async function toggleBookmark(e) {

  const icon = bookmarkBtn.querySelector(".heart-icon");
  const isActive = bookmarkBtn.classList.contains("active");

  try {
    if (!isActive) {
      const res = await fetch(`${API_BASE}/bookmark`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${TOKEN}`,
        },
        body: JSON.stringify({ quote_id: currentQuote.id }),
      });

      if (res.status === 201) {
        bookmarkBtn.classList.add("active");
        icon.classList.replace("fa-regular", "fa-solid");

        if (typeof fetchBookmarks === "function") fetchBookmarks();
      }

    } else {
      const res = await fetch(`${API_BASE}/bookmark/${currentQuote.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${TOKEN}`,
        },
      });

      if (res.status === 204) {
        bookmarkBtn.classList.remove("active");
        icon.classList.replace("fa-solid", "fa-regular");

        if (typeof fetchBookmarks === "function") fetchBookmarks();
      }
    }
  } catch (err) {
    console.error(err);
  }
}

async function checkIfBookmarked() {
  if (!TOKEN || !currentQuote) return;
  try {
    const res = await fetch(`${API_BASE}/bookmark`, {
      headers: { Authorization: `Bearer ${TOKEN}` },
    });
    const data = await res.json();
    const found = data.some(b => b.quote.id === currentQuote.id);
    const icon = bookmarkBtn.querySelector(".heart-icon");
    if (found) {
      bookmarkBtn.classList.add("active");
      icon.classList.replace("fa-regular", "fa-solid");
    } else {
      bookmarkBtn.classList.remove("active");
      icon.classList.replace("fa-solid", "fa-regular");
    }
  } catch {}
}

refreshBtn.addEventListener("click", fetchRandomQuote);
bookmarkBtn.addEventListener("click", toggleBookmark);
window.addEventListener("DOMContentLoaded", fetchRandomQuote);
