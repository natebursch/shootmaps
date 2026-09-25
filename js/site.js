/* ==========================================================
   SITE SETTINGS — edit these, every page picks them up.
   ========================================================== */
const SITE = {
  // Paste your Google Form link here (Form > Send > link icon > copy).
  signupFormUrl: "https://forms.gle/i1g2Vddg6NpA3Acd6",
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
const here = location.pathname.replace(/index\.html$/, "");
document.querySelectorAll(".nav a").forEach(a => {
  if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page");
});

// Next-match banner + past/next markers on the schedule list
if (window.MAPSA_EVENTS) {
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const asDate = s => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const next = window.MAPSA_EVENTS.find(e => asDate(e.end) >= today);
  const box = document.getElementById("next-match");
  if (next && box) {
    const start = asDate(next.start);
    const days = Math.round((start - today) / 864e5);
    const when = start.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
    const count = days <= 0 ? "Today!" : days === 1 ? "Tomorrow" : `in ${days} days`;
    box.innerHTML = `<div><span class="label">Next Match</span><span class="name">${next.name}</span>
      <span class="when">${when} &middot; <span class="count">${count}</span></span></div>
      <a class="btn" href="${SITE.registrationUrl}" target="_blank" rel="noopener">Register</a>`;
    box.hidden = false;
  }
  let marked = false;
  document.querySelectorAll(".events .event").forEach(li => {
    if (asDate(li.dataset.end) < today) li.classList.add("past");
    else if (!marked) { li.classList.add("next"); marked = true; }
  });
}

// Photo lightbox
const lb = document.querySelector(".lightbox");
if (lb) {
  const big = lb.querySelector("img");
  document.querySelectorAll(".gallery img").forEach(img => img.addEventListener("click", () => {
    big.src = img.src; big.alt = img.alt; lb.classList.add("open");
  }));
  lb.addEventListener("click", () => lb.classList.remove("open"));
}
