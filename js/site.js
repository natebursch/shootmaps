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
  // Matches pulled from PractiScore (practiscore_sync.py) link straight to that match's
  // registration page. The hand-typed EVENTS list in build.py is the fallback.
  const ps = (window.MAPSA_PS || []).map(m => ({ start: m.date, end: m.date, name: m.name, url: m.url, status: m.status }));
  const psDates = new Set(ps.map(m => m.start));
  const all = ps.concat(window.MAPSA_EVENTS.filter(e => !psDates.has(e.start)))
    .filter(e => asDate(e.end) >= today)
    .sort((a, b) => a.start < b.start ? -1 : a.start > b.start ? 1 : 0);
  const next = all[0];
  const box = document.getElementById("next-match");
  if (next && box) {
    const start = asDate(next.start);
    const days = Math.round((start - today) / 864e5);
    const when = start.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: start.getFullYear() !== today.getFullYear() ? "numeric" : undefined });
    const count = days <= 0 ? "Today!" : days === 1 ? "Tomorrow" : `in ${days} days`;
    const status = next.status === "open" ? "Registration open" : next.status ? "Registration not open yet" : "";
    const btn = next.status && next.status !== "open" ? "View on PractiScore" : "Register";
    box.innerHTML = `<div><span class="label">Next Match</span><span class="name">${next.name}</span>
      <span class="when">${when} &middot; <span class="count">${count}</span></span>
      ${status ? `<span class="status">${status}</span>` : ""}</div>
      <a class="btn" href="${next.url || SITE.registrationUrl}" target="_blank" rel="noopener">${btn}</a>`;
    box.hidden = false;
  }
  document.querySelectorAll(".ps-events .event").forEach(li => { if (asDate(li.dataset.end) < today) li.remove(); });
  document.querySelectorAll(".ps-wrap").forEach(w => { if (!w.querySelector(".event")) w.remove(); });
  let marked = false;
  document.querySelectorAll(".events:not(.ps-events) .event").forEach(li => {
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
