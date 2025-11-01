console.log("[loaded] theme-manager.js");

// 페이지 로드되면 테마 복원 + 버튼 연결
document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme") || "pink";
  document.body.dataset.theme = savedTheme;

  // 버튼 클릭시 테마 변경
  document.querySelectorAll(".theme-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const theme = btn.dataset.theme;
      document.body.dataset.theme = theme;
      localStorage.setItem("theme", theme);
    });
  });
});
