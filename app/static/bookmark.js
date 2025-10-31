const bookmarkList = document.getElementById("bookmarkList");


async function removeBookmark(quoteId) {
  if (!confirm("북마크를 삭제하시겠습니까?")) return;

  try {
    const res = await fetch(`${API_BASE}/bookmark/${quoteId}`, {
      method: "DELETE",
      credentials: "include"
    });

    if (res.status === 204) {
      fetchBookmarks(); // 삭제 후 즉시 UI 갱신
    } else {
      alert("삭제 실패");
    }
  } catch (e) {
    alert("서버 오류가 발생했습니다.");
  }
}

// ✅ 북마크 목록 불러오기
async function fetchBookmarks() {
  try {
    const res = await fetch(`/api/v1/bookmark`, {
      credentials: "include"
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    const items = data.items;

    if (!items || items.length === 0) {
      bookmarkList.innerHTML = "<li>북마크가 없습니다.</li>";
      return;
    }

    bookmarkList.innerHTML = items
      .map(
        (b) => `
        <li>
          <span>“${b.quote.message}” — ${b.quote.author}</span>
          <button class="bookmark-remove" onclick="removeBookmark(${b.quote.id})">
            <i class="heart-icon fa-solid fa-heart"></i>
          </button>
        </li>
        `
      )
      .join("");

  } catch (err) {
    bookmarkList.innerHTML = "<li>북마크 목록을 불러오지 못했습니다.</li>";
  }
}

// ✅ 페이지 로드 시 실행
window.addEventListener("DOMContentLoaded", fetchBookmarks);