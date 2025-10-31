const bookmarkList = document.getElementById("bookmarkList");

async function fetchBookmarks() {
  try {
    const res = await fetch(`${API_BASE}/bookmark`, {
      credentials: 'include',
    });

    if (!res.ok) {
      if (res.status === 401) {
        bookmarkList.innerHTML = "<li>로그인이 필요합니다.</li>";
        return;
      }
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();
    bookmarkList.innerHTML =
      data.length === 0
        ? "<li>북마크가 없습니다.</li>"
        : data.map(b => `<li>“${b.quote.message}” – ${b.quote.author}</li>`).join("");
  } catch (err) {
    console.error(err);
    bookmarkList.innerHTML = "<li>북마크 목록을 불러오지 못했습니다.</li>";
  }
}


window.addEventListener("DOMContentLoaded", fetchBookmarks);
