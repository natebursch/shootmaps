/* ==========================================================
   SITE SETTINGS — edit these, every page picks them up.
   ========================================================== */
const SITE = {
  // Paste your Google Form link here (Form > Send > link icon > copy).
  signupFormUrl: "https://forms.gle/REPLACE_ME",
  registrationUrl: "https://practiscore.com/clubs/mapsa_at_flsc",
  email: "shootmapsa@gmail.com",
  instagram: "https://www.instagram.com/mapsa_mn"
};

document.querySelectorAll("[data-signup]").forEach(a => a.href = SITE.signupFormUrl);
document.querySelectorAll("[data-register]").forEach(a => a.href = SITE.registrationUrl);
document.querySelectorAll("[data-year]").forEach(el => el.textContent = new Date().getFullYear());

// Mobile menu
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");
if (toggle && nav) toggle.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});

// Highlight current page
const here = location.pathname.split("/").pop() || "index.html";
document.querySelectorAll(".nav a").forEach(a => {
  if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page");
});

// Photo lightbox
const lb = document.querySelector(".lightbox");
if (lb) {
  const big = lb.querySelector("img");
  document.querySelectorAll(".gallery img").forEach(img => img.addEventListener("click", () => {
    big.src = img.src; big.alt = img.alt; lb.classList.add("open");
  }));
  lb.addEventListener("click", () => lb.classList.remove("open"));
}
