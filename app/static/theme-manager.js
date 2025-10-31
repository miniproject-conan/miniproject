console.log("[loaded] theme-manager.js");

document.addEventListener("DOMContentLoaded", () => {
  // 저장된 테마 불러와서 즉시 적용
  const currentTheme = localStorage.getItem("theme") || "pink";
  document.body.dataset.theme = currentTheme;

  // 버튼 클릭 시 테마 변경 및 저장
  document.querySelectorAll(".theme-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const theme = btn.dataset.theme;
      document.body.dataset.theme = theme;
      localStorage.setItem("theme", theme);
    });
  });
});
