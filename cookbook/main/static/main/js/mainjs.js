function updateCurrentTime() {
    const currentTimeElement = document.getElementById("current-time");
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const currentTimeString = `${hours}:${minutes}:${seconds}`;
    currentTimeElement.textContent = currentTimeString;
}

setInterval(updateCurrentTime, 1000);
updateCurrentTime();



const themeToggle = document.getElementById("theme-toggle");
const body = document.body;
const dropdown = document.getElementById("dropdown");

function setThemeStatus(status) {
  if (status) {
    body.classList.add("dark-theme");
    dropdown.style.backgroundColor = "#333333";
  } else {
    body.classList.remove("dark-theme");
    dropdown.style.backgroundColor = "#fff";
  }
}

const storedThemeStatus = localStorage.getItem("themeStatus");

if (storedThemeStatus === "1") {
  themeToggle.checked = true;
  setThemeStatus(true);
} else {
  themeToggle.checked = false;
  setThemeStatus(false);
}

themeToggle.addEventListener("change", () => {
  if (themeToggle.checked) {
    setThemeStatus(true);
    localStorage.setItem("themeStatus", "1");
  } else {
    setThemeStatus(false);
    localStorage.setItem("themeStatus", "0");
  }
});


document.getElementById("toggleSidebar").addEventListener("click", function() {
  var sidebar = document.getElementById("sidebar");
  var firstsidebarbutton = document.getElementById('toggleSidebar');
  var firstsidebarbutton2 = document.getElementById('toggleSidebar2');

  if (sidebar.style.left === "-250px") {
    sidebar.style.left = "0"; // Открываем боковую панель
    sidebar.style.display = 'block';
    firstsidebarbutton.style.display = "none";
  } else {
    sidebar.style.left = "-250px";
  }

  function resetSidebar() {

    sidebar.style.left = "-250px";
    sidebar.style.display = 'none';
    firstsidebarbutton.style.display = "block";
  }

  firstsidebarbutton2.addEventListener('click', resetSidebar);
});


