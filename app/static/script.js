document.addEventListener("DOMContentLoaded", () => {

const API_BASE = "/api/v1";
const TOKEN = localStorage.getItem("access_token") || "";

const panes = document.querySelectorAll('.pane');
const monthButtons = document.querySelectorAll('[data-month-btn]');
const yearSelect = document.getElementById('yearSelect');

let currentYear = yearSelect.value;
let currentMonth = new Date().getMonth() + 1;

const params = new URLSearchParams(window.location.search);
if (params.get("month")) currentMonth = params.get("month");
if (params.get("year")) currentYear = params.get("year");

function show(year, month) {
  panes.forEach(p => {
    const ok = p.dataset.year === String(year) && p.dataset.month === String(month);
    p.classList.toggle('active', ok);
  });
  monthButtons.forEach(b => b.classList.toggle('active', b.dataset.monthBtn === String(month)));
  document.getElementById('leftPane').scrollTop = 0;
  document.getElementById('rightPane').scrollTop = 0;
}

if (currentMonth < 1 || currentMonth > 12) currentMonth = 1;
show(currentYear, currentMonth);

monthButtons.forEach(btn => btn.addEventListener('click', () => {
  currentMonth = btn.dataset.monthBtn;
  show(currentYear, currentMonth);
}));

yearSelect.addEventListener('change', () => {
  currentYear = yearSelect.value;
  show(currentYear, currentMonth);
});

});
