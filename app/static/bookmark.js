const bookmarkList = document.getElementById("bookmarkList");

async function fetchBookmarks() {
  try {
    const res = await fetch(`/api/v1/bookmark`, {
      headers: { Authorization: `Bearer ${TOKEN}` },
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    const items = data.items; // ✅ 북마크 배열

    bookmarkList.innerHTML =
      items.length === 0
        ? "<li>북마크가 없습니다.</li>"
        : items
            .map(
              (b) => `
                <li>
                  “${b.quote.message}” — ${b.quote.author}
                </li>`
            )
            .join("");

  } catch (err) {
    bookmarkList.innerHTML = "<li>북마크 목록을 불러오지 못했습니다.</li>";
  }
}

window.addEventListener("DOMContentLoaded", fetchBookmarks);