const root = document.documentElement;
const toggle = document.getElementById("theme-toggle");
const storageKey = "portfolio-theme";
const iconContainer = toggle.querySelector(".theme-icon");

const moonIcon = `
<svg viewBox="0 0 24 24" role="img" aria-hidden="true" focusable="false">
  <path d="M21 14.2A9 9 0 1 1 9.8 3a7 7 0 1 0 11.2 11.2z"></path>
</svg>
`;

const sunIcon = `
<svg viewBox="0 0 24 24" role="img" aria-hidden="true" focusable="false">
  <circle cx="12" cy="12" r="4.2"></circle>
  <path d="M12 1.8v3.1M12 19.1v3.1M4.3 4.3l2.2 2.2M17.5 17.5l2.2 2.2M1.8 12h3.1M19.1 12h3.1M4.3 19.7l2.2-2.2M17.5 6.5l2.2-2.2"></path>
</svg>
`;

const applyTheme = (theme) => {
  root.setAttribute("data-theme", theme);
  if (theme === "dark") {
    iconContainer.innerHTML = sunIcon;
    toggle.setAttribute("aria-label", "Activar modo claro");
  } else {
    iconContainer.innerHTML = moonIcon;
    toggle.setAttribute("aria-label", "Activar modo oscuro");
  }
};

const savedTheme = localStorage.getItem(storageKey) || "dark";
applyTheme(savedTheme);

toggle.addEventListener("click", () => {
  const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
  localStorage.setItem(storageKey, nextTheme);
  applyTheme(nextTheme);
});
