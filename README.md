# MAPSA website (shootmapsa.com)

Plain HTML/CSS site — no WordPress, no build step, free to host on GitHub Pages.

## Files
- `index.html`, `about.html`, `schedule.html`, `match-rules.html`, `photos.html` — the pages
- `css/style.css` — colors and fonts (edit the variables at the top)
- `js/site.js` — **site settings**: Google Form sign-up link, PractiScore link, email, Instagram
- `images/` — logo, hero, and photos
- `CNAME` — tells GitHub Pages to serve this at shootmapsa.com

## Newsletter sign-up (Google Form)
1. Go to forms.google.com → Blank form. Add fields (Name, Email, "What do you shoot?", etc.).
2. Responses tab → "Link to Sheets" so sign-ups land in a spreadsheet.
3. Click **Send** → link icon → check "Shorten URL" → Copy.
4. Paste it into `signupFormUrl` in `js/site.js`. Every Sign Up button on the site updates.

## Put it online (GitHub Pages)
1. In GitHub Desktop: File → Add local repository → pick this folder → create repository → Publish (public).
2. On github.com: repo → Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)` → Save.
3. Same page, Custom domain: `shootmapsa.com` → Save. Tick **Enforce HTTPS** once it's available.
4. At your domain registrar, set DNS:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `<your-github-username>.github.io`
   - Remove any old A/CNAME records pointing at WordPress.
   - If the domain itself is registered through WordPress.com, transfer it out (or change its DNS there) **before** the plan ends.

## Common edits
- **New match:** in `schedule.html`, copy an `<div class="event">` block. The Google Calendar embed updates itself.
- **New photos:** drop them in `images/` and copy an `<img>` line in `photos.html`.
- **Leadership changes:** edit the cards in `about.html`.
