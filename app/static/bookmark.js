console.log("[loaded] bookmark.js");

// API_BASE는 /api/v1 로 고정 (백엔드 prefix)
const API_BASE = "/api/v1";
const bookmarkList = document.getElementById("bookmarkList");

async function fetchBookmarks() {
  console.log("[실행] fetchBookmarks()");
  try {
    const res = await fetch(`${API_BASE}/bookmark`, {
      credentials: "include",
    });

    if (!res.ok) {
      if (res.status === 401) {
        bookmarkList.innerHTML = "<li>로그인이 필요합니다.</li>";
        return;
      }
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();
    const items = data.items || data;

    if (!items || items.length === 0) {
      bookmarkList.innerHTML = "<li>북마크가 없습니다.</li>";
      return;
    }

    bookmarkList.innerHTML = items
      .map(
        (b) => `
        <li data-quote-id="${b.quote.id}">
          <span>“${b.quote.message}” – ${b.quote.author}</span>
          <button class="remove-btn" title="북마크 해제">
            <i class="fa-solid fa-heart-crack"></i>
          </button>
        </li>`
      )
      .join("");

    // 삭제 버튼 이벤트 등록
    document.querySelectorAll(".remove-btn").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        const li = e.target.closest("li");
        const quoteId = li.dataset.quoteId;

        // 현재 화면의 명언과 동일한 항목이면, 메인 하트 버튼을 대신 눌러서 중복 DELETE 방지
        if (
          window.bookmarkBtn &&
          window.currentQuote &&
          String(window.currentQuote.id) === String(quoteId)
        ) {
          window.bookmarkBtn.click();   // toggleBookmark 호출 → DELETE 실행
          setTimeout(fetchBookmarks, 150); // 목록 새로고침
          return;
        }

        // 그 외 항목은 기존처럼 API로만 삭제
        await removeBookmark(quoteId);
      });
    });
  } catch (err) {
    console.error("북마크 불러오기 오류:", err);
    bookmarkList.innerHTML = "<li>북마크 목록을 불러오지 못했습니다.</li>";
  }
}

async function removeBookmark(quoteId) {
  try {
    const res = await fetch(`${API_BASE}/bookmark/${quoteId}`, {
      method: "DELETE",
      credentials: "include",
    });

    if (res.status === 204) {
      console.log("북마크 제거 완료:", quoteId);
      await fetchBookmarks();
      // 필요 시 quote 하트와 동기화 (현재 명언이 이 항목이었다면)
      if (
        window.currentQuote &&
        String(window.currentQuote.id) === String(quoteId)
      ) {
        // 하트 아이콘 상태 강제 동기화
        if (window.bookmarkBtn) {
          window.bookmarkBtn.classList.remove("active");
          const icon = window.bookmarkBtn.querySelector(".heart-icon");
          if (icon) icon.classList.replace("fa-solid", "fa-regular");
        }
      }
    } else {
      throw new Error(`HTTP ${res.status}`);
    }
  } catch (err) {
    console.error("북마크 삭제 실패:", err);
    alert("북마크 삭제 중 오류가 발생했습니다.");
  }
}

window.addEventListener("DOMContentLoaded", fetchBookmarks);
// 외부에서 재호출 가능하도록 공개
window.fetchBookmarks = fetchBookmarks;
