"""
MAPSA site builder.  Edit the data below, then run:   python build.py
It regenerates every page (HTML, SEO tags, Google event data, sitemap).
"""
import os, json, datetime as dt
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://shootmapsa.com"
VER = dt.datetime.now().strftime("%Y%m%d%H%M")  # cache-buster for css/js

# ------------------------------------------------------------------ SITE DATA
REGISTER = "https://practiscore.com/clubs/mapsa_at_flsc"
EMAIL = "shootmapsa@gmail.com"
IG = "https://www.instagram.com/mapsa_mn"
ADDRESS = {"street": "4880 240th St N", "city": "Forest Lake", "region": "MN", "zip": "55025", "note": "Gate 3"}
CAL = ("https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FChicago"
       "&src=Mjg5Mzg4ZDgyNzBmNzRlY2E5NmVjNjM0ZDMzMmM3YTg1YmVhZTZiODMyZWUwNjA1ZmE2ODJlNTAxZmNlN2YzMUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t"
       "&src=ZW4udXNhI2hvbGlkYXlAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&color=%23b39ddb&color=%230b8043")

# Matches: (start date, end date or None, name, short type)
EVENTS = [
    ("2026-03-07", None, "USPSA Match", "USPSA"),
    ("2026-03-22", None, "AT3 Cold War Carbine x Obsidian", "Carbine"),
    ("2026-04-04", None, "USPSA Match", "USPSA"),
    ("2026-04-18", None, "PCSL 2-Gun Match", "PCSL 2-Gun"),
    ("2026-05-02", "2026-05-03", "Vortex Optics Northwoods Showdown, presented by Hunter Constantine", "Major match"),
    ("2026-05-23", None, "PCSL 2-Gun Points Series", "PCSL 2-Gun"),
    ("2026-06-20", None, "USPSA Match", "USPSA"),
    ("2026-07-25", None, "USPSA MN Section Points Match", "USPSA"),
    ("2026-09-12", None, "USPSA Match", "USPSA"),
    ("2026-09-27", None, "PCSL 2-Gun Points Series", "PCSL 2-Gun"),
    ("2026-10-03", None, "USPSA Match", "USPSA"),
    ("2026-10-10", None, "AT3 Tactical MN PCSL 2-Gun Championship, presented by Obsidian Arms", "Championship"),
]

LEADERS = [
    ("Tim Dunderi", "President", "https://www.instagram.com/tanfo_timmy"),
    ("Ryan Carlson", "Vice President", None),
    ("Ben Egelston", "Chief Technology Officer", "https://www.instagram.com/benegelston_mn"),
    ("Luke Faust", "Secretary", "https://www.instagram.com/faust9057"),
    ("Clinton Fjerstad", "Press Secretary", "https://www.instagram.com/clinton_fjerstad"),
]

FAQ = [
    ("What is practical shooting?",
     "Practical shooting is a timed sport where you move through a course of fire (a &ldquo;stage&rdquo;), engaging paper and steel targets from different positions. Your score balances accuracy and speed. Every stage is run one shooter at a time under a Range Officer, so safety is built in."),
    ("What is USPSA?",
     "The United States Practical Shooting Association is the largest practical shooting organization in the country. USPSA matches are handgun matches with divisions for everything from stock pistols to fully customized race guns, so whatever you already own probably has a home. <a href=\"https://uspsa.org/rules\" target=\"_blank\" rel=\"noopener\">USPSA rules</a>."),
    ("What is PCSL 2-Gun?",
     "The Practical Competition Shooting League runs pistol and carbine matches. In 2-Gun you shoot both a pistol and a rifle/carbine, often on the same stage. <a href=\"https://www.pcsleague.us/\" target=\"_blank\" rel=\"noopener\">PCSL website</a>."),
    ("Do I need experience to come shoot?",
     "No. You should be able to safely handle and draw your firearm from a holster, but you don&rsquo;t need to be fast or have competed before. Tell your squad it&rsquo;s your first match &mdash; practical shooters love helping new people get started."),
    ("What should I bring?",
     "<ul><li>Eye and ear protection (required)</li><li>A pistol and a strong-side holster that fully covers the trigger guard</li><li>At least 3&ndash;4 magazines and magazine pouches</li><li>Enough ammo &mdash; the round count is listed on each match&rsquo;s PractiScore page (plus extra)</li><li>For 2-Gun: a carbine/rifle, magazines, and a sling or case</li><li>Weather-appropriate clothes, water, and snacks &mdash; it&rsquo;s Minnesota</li></ul>"),
    ("How do I sign up for a match?",
     f"All MAPSA matches are listed on <a href=\"{REGISTER}\" target=\"_blank\" rel=\"noopener\">PractiScore</a> (search keyword <strong>MAPSA</strong>). Create a free PractiScore account, pick the match, choose your division, and register. Spots can fill up, so register early."),
    ("Where are matches held?",
     f"{ADDRESS['street']}, {ADDRESS['city']}, {ADDRESS['region']} {ADDRESS['zip']} &mdash; use {ADDRESS['note']}. See the map on our <a href=\"/schedule/\">schedule page</a>."),
    ("What are the basic safety rules?",
     "Matches run on a <strong>cold range</strong>: arrive with your firearm unloaded, and only handle it in designated safe areas or when a Range Officer directs you on the line. Keep your finger off the trigger and the muzzle pointed downrange. Breaking a safety rule means a disqualification for the day &mdash; nobody gets hurt, and you come back next time."),
]

# ------------------------------------------------------------------ HELPERS
def d(s): return dt.date.fromisoformat(s)
def pretty(e):
    s = d(e[0]); t = d(e[1]) if e[1] else None
    if t: return f"{s.strftime('%a, %b')} {s.day}&ndash;{t.day}, {s.year}" if s.month == t.month else f"{s:%b} {s.day} &ndash; {t:%b} {t.day}, {s.year}"
    return f"{s.strftime('%a, %b')} {s.day}, {s.year}"

PLACE = {"@type": "Place", "name": f"MAPSA Range ({ADDRESS['note']})",
         "address": {"@type": "PostalAddress", "streetAddress": ADDRESS["street"], "addressLocality": ADDRESS["city"],
                     "addressRegion": ADDRESS["region"], "postalCode": ADDRESS["zip"], "addressCountry": "US"}}
ORG = {"@context": "https://schema.org", "@type": "SportsOrganization", "@id": DOMAIN + "/#org",
       "name": "Metro Area Practical Shooting Association", "alternateName": "MAPSA", "url": DOMAIN + "/",
       "logo": DOMAIN + "/images/mapsa-logo.png", "image": DOMAIN + "/images/og-image.jpg",
       "email": EMAIL, "sport": "Practical shooting", "sameAs": [IG],
       "location": PLACE, "areaServed": "Minneapolis–Saint Paul, Minnesota"}

def event_ld():
    out = []
    for e in EVENTS:
        out.append({"@context": "https://schema.org", "@type": "SportsEvent",
                    "name": f"MAPSA {e[2]}", "startDate": e[0],
                    "endDate": e[1] or e[0], "eventStatus": "https://schema.org/EventScheduled",
                    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                    "location": PLACE, "image": [DOMAIN + "/images/event.jpg"],
                    "description": f"{e[3]} practical shooting match hosted by MAPSA in Forest Lake, MN. Register on PractiScore.",
                    "organizer": {"@type": "Organization", "name": "MAPSA", "url": DOMAIN + "/"},
                    "offers": {"@type": "Offer", "url": REGISTER, "availability": "https://schema.org/InStock", "validFrom": "2026-01-01"},
                    "sport": "Practical shooting"})
    return out

def ld(obj): return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

NAV = [("/", "Home"), ("/about-us/", "About Us"), ("/schedule/", "Schedule"), ("/new-shooters/", "New Shooters"),
       ("/match-rules/", "Match Rules"), ("/photos/", "Photos")]

def page(path, title, desc, body, hero="", extra_head="", image="/images/og-image.jpg", events_js=False):
    url = DOMAIN + path
    nav = "\n      ".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    ev = ""
    if events_js:
        ev = "<script>window.MAPSA_EVENTS=" + json.dumps([{"start": e[0], "end": e[1] or e[0], "name": e[2]} for e in EVENTS]) + ";</script>\n"
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#2b2f2f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MAPSA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.png">
<link rel="apple-touch-icon" href="/images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Kanit:wght@200;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v={VER}">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><img src="/images/mapsa-logo.png" alt="MAPSA logo" width="44" height="44"><span>MAPSA</span></a>
    <button class="menu-toggle" aria-label="Menu" aria-expanded="false">&#9776;</button>
    <nav class="nav" aria-label="Main">
      {nav}
      <a class="btn mobile-only" data-register href="{REGISTER}" target="_blank" rel="noopener">Match Registration</a>
    </nav>
    <a class="btn header-cta" data-register href="{REGISTER}" target="_blank" rel="noopener">Match Registration</a>
  </div>
</header>
{hero}
<main id="main">
{body}
</main>
<section class="signup">
  <div class="wrap">
    <h2>Join the Mailing List</h2>
    <hr class="rule">
    <p>Stay informed about our upcoming shoots and events. Fill out our quick sign-up form and we'll keep you in the loop.</p>
    <a class="btn" data-signup href="https://forms.gle/i1g2Vddg6NpA3Acd6" target="_blank" rel="noopener">Sign Up</a>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3>MAPSA</h3>
        <p>Metro Area Practical Shooting Association. Here at MAPSA, we like shooting stuff and we want you to come shoot stuff with us.</p>
      </div>
      <div>
        <h3>Contact</h3>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p><a href="{IG}" target="_blank" rel="noopener">Instagram @mapsa_mn</a></p>
        <p>{ADDRESS['street']}, {ADDRESS['city']}, {ADDRESS['region']} {ADDRESS['zip']} ({ADDRESS['note']})</p>
      </div>
      <div>
        <h3>Quick Links</h3>
        <ul class="link-list">
          <li><a data-register href="{REGISTER}" target="_blank" rel="noopener">Match Registration (PractiScore)</a></li>
          <li><a href="/new-shooters/">New Shooter Guide</a></li>
          <li><a href="/schedule/">2026 Schedule</a></li>
          <li><a href="/match-rules/">Match Rules</a></li>
        </ul>
      </div>
    </div>
    <p class="copy">&copy; <span data-year>{dt.date.today().year}</span> Metro Area Practical Shooting Association</p>
  </div>
</footer>
<div class="lightbox"><img alt=""></div>
{ev}<script src="/js/site.js?v={VER}"></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write(html)

def redirect(old, new):
    out = os.path.join(ROOT, old.strip("/"), "index.html") if old.endswith("/") else os.path.join(ROOT, old.strip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write(
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved – MAPSA</title>'
        f'<link rel="canonical" href="{DOMAIN}{new}"><meta name="robots" content="noindex">'
        f'<meta http-equiv="refresh" content="0; url={new}"><script>location.replace("{new}"+location.hash)</script></head>'
        f'<body><p>This page moved to <a href="{new}">{DOMAIN}{new}</a>.</p></body></html>\n')

def ph(t, sub="", img="hero-shooter.jpg", pos="60% 30%"):
    return (f'<div class="page-hero" style="--hero:url(/images/{img});--pos:{pos}">'
            f'<h1>{t}</h1>{f"<p>{sub}</p>" if sub else ""}</div>')
ADDR_Q = f"{ADDRESS['street']}, {ADDRESS['city']}, {ADDRESS['region']} {ADDRESS['zip']}".replace(" ", "+")
MAP = f'<iframe class="map" src="https://www.google.com/maps?q={ADDR_Q}&amp;output=embed" title="Map to the MAPSA range" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
NEXT = '<div class="next-match" id="next-match" hidden></div>'

def event_list():
    rows = "\n".join(
        f'      <li class="event" data-end="{e[1] or e[0]}"><time datetime="{e[0]}">{pretty(e)}</time><span class="tag">{e[3]}</span><h3>{e[2]}</h3></li>'
        for e in EVENTS)
    return f'<ol class="events">\n{rows}\n    </ol>'

# ------------------------------------------------------------------ PAGES
def build():
    page("/", "MAPSA | USPSA & PCSL 2-Gun Matches in Forest Lake, MN",
         "Metro Area Practical Shooting Association hosts USPSA and PCSL 2-Gun practical shooting matches in Forest Lake, MN for the Twin Cities. See the 2026 schedule and register on PractiScore.",
         f'''
<section>
  <div class="wrap">
    <h2>Upcoming Events</h2>
    <hr class="rule">
    {NEXT}
    <img class="feature-img" src="/images/event.jpg" alt="MAPSA 2026 match schedule flyer: USPSA and PCSL 2-Gun matches in Forest Lake, MN" width="1000" height="1294">
    <iframe class="cal" src="{CAL}" title="MAPSA events calendar" loading="lazy"></iframe>
    <p class="center"><a class="btn" data-register href="{REGISTER}" target="_blank" rel="noopener">Match Registration</a></p>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <h2>Never Shot a Match?</h2>
    <hr class="rule">
    <div class="split">
      <div>
        <p>Practical shooting is the most fun you can have at a range: run, move and shoot through timed courses of fire with a squad of people who are happy to help you get started. If you can safely draw from a holster, you&rsquo;re ready.</p>
        <p><a class="btn" href="/new-shooters/">New Shooter Guide</a></p>
      </div>
      <img src="/images/photo-4.jpg" alt="Competitor shooting a pistol stage at a MAPSA USPSA match" loading="lazy">
    </div>
  </div>
</section>
<section>
  <div class="wrap center">
    <h2>Follow Along</h2>
    <hr class="rule">
    <p class="lead">Match updates, sponsor announcements and photos from the range &mdash; all on our Instagram.</p>
    <a class="btn btn-outline" href="{IG}" target="_blank" rel="noopener">@mapsa_mn on Instagram</a>
  </div>
</section>''',
         hero='<div class="hero hero-photo"><img src="/images/mapsa-logo.png" alt="Metro Area Practical Shooting Association logo" width="360" height="360"><h1 class="sr-only">MAPSA &ndash; Metro Area Practical Shooting Association</h1><p class="hero-tag"><span class="nw">USPSA &amp; PCSL 2-Gun Matches</span><br><span class="nw">Forest Lake, MN</span></p></div>',
         extra_head=ld(ORG), events_js=True)

    cards = "\n".join(
        f'      <div class="card"><h3>{n}</h3><p class="role">{r}</p>{f"<a href={chr(34)}{l}{chr(34)} target=_blank rel=noopener>Instagram</a>" if l else ""}</div>'
        for n, r, l in LEADERS)
    page("/about-us/", "About MAPSA | Metro Area Practical Shooting Association",
         "MAPSA hosts safe, welcoming, high-quality practical shooting competitions in the Twin Cities area. Meet our mission and leadership team.",
         f'''
<section>
  <div class="wrap">
    <h2>Our History and Mission</h2>
    <hr class="rule">
    <p class="lead">MAPSA is dedicated to hosting the highest-quality shooting competitions &mdash; where participants are valued not as numbers, but as respected members of our community.</p>
    <p class="lead">Since our founding, we&rsquo;ve focused on advancing responsible firearm ownership, safety, and education. Our mission is to provide a safe, inclusive, and engaging environment where shooting enthusiasts can learn, compete, and share their passion for the shooting sports.</p>
    <img class="feature-img" src="/images/photo-3.jpg" alt="MAPSA leadership at a match" loading="lazy">
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <h2>Leadership Team</h2>
    <hr class="rule">
    <div class="grid">
{cards}
    </div>
  </div>
</section>''', hero=ph("About Us", img="photo-3.jpg", pos="50% 22%"), extra_head=ld(ORG))

    page("/schedule/", "2026 Match Schedule | MAPSA USPSA & PCSL 2-Gun, Forest Lake MN",
         "MAPSA's 2026 USPSA and PCSL 2-Gun match schedule in Forest Lake, MN, including the Northwoods Showdown and the MN PCSL 2-Gun Championship. Register on PractiScore.",
         f'''
<section>
  <div class="wrap">
    <h2>2026 Match Schedule</h2>
    <hr class="rule">
    <p class="lead">Registration and match details for every event are on PractiScore &mdash; search keyword <strong>MAPSA</strong>.</p>
    {NEXT}
    <img class="feature-img" src="/images/event.jpg" alt="MAPSA 2026 match schedule flyer" width="1000" height="1294">
    <iframe class="cal" src="{CAL}" title="MAPSA events calendar" loading="lazy"></iframe>
    {event_list()}
    <p class="center"><a class="btn" data-register href="{REGISTER}" target="_blank" rel="noopener">Register on PractiScore</a></p>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <h2>Getting Here</h2>
    <hr class="rule">
    <p class="lead">{ADDRESS['street']}, {ADDRESS['city']}, {ADDRESS['region']} {ADDRESS['zip']} &mdash; <strong>use {ADDRESS['note']}</strong>.</p>
    {MAP}
    <p class="center"><a class="btn btn-outline" href="https://www.google.com/maps/dir/?api=1&amp;destination={ADDR_Q}" target="_blank" rel="noopener">Get Directions</a></p>
  </div>
</section>''', hero=ph("Schedule", img="hero-shooter.jpg", pos="62% 30%"), extra_head="\n".join(ld(x) for x in event_ld()), events_js=True,
         image="/images/event.jpg")

    faq_html = "\n".join(f'    <details class="faq"><summary>{q}</summary><div>{a}</div></details>' for q, a in FAQ)
    import re
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub("<.*?>|&[a-z]+;", "", q).strip(),
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    page("/new-shooters/", "New Shooter Guide | How to Start USPSA & PCSL in Minnesota | MAPSA",
         "Never shot a USPSA or PCSL 2-Gun match? What to bring, how to register on PractiScore, safety rules and what to expect at your first MAPSA match in Forest Lake, MN.",
         f'''
<section>
  <div class="wrap">
    <h2>Your First Match</h2>
    <hr class="rule">
    <p class="lead">Practical shooting is a timed, moving, run-and-gun style of competition &mdash; and it&rsquo;s the fastest way to get better with the firearms you already own. Here&rsquo;s everything you need to show up to your first MAPSA match with confidence.</p>
    <ol class="steps">
      <li><h3>Pick a match</h3><p>USPSA matches are pistol only. PCSL 2-Gun uses a pistol and a carbine. Check the <a href="/schedule/">2026 schedule</a>.</p></li>
      <li><h3>Register</h3><p>Sign up on <a href="{REGISTER}" target="_blank" rel="noopener">PractiScore</a> (keyword MAPSA) and choose the division that matches your gear.</p></li>
      <li><h3>Gear up</h3><p>Eye &amp; ear protection, a holster that covers the trigger guard, magazines, pouches and ammo.</p></li>
      <li><h3>Show up &amp; shoot</h3><p>Arrive early, check in, and tell your squad it&rsquo;s your first match. They&rsquo;ll help you through it.</p></li>
    </ol>
  </div>
</section>
<section class="alt">
  <div class="wrap narrow">
    <h2>New Shooter FAQ</h2>
    <hr class="rule">
{faq_html}
    <p class="center" style="margin-top:32px">Still have questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or DM us on <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</p>
  </div>
</section>''', hero=ph("New Shooters", "Everything you need for your first match", img="photo-4.jpg", pos="50% 19%"), extra_head=ld(faq_ld),
         image="/images/photo-1.jpg")

    page("/match-rules/", "Match Rules | USPSA & PCSL Rulebooks | MAPSA",
         "Official USPSA and PCSL rulebooks used at MAPSA practical shooting matches in Forest Lake, MN.",
         '''
<section>
  <div class="wrap">
    <h2>Match Rules</h2>
    <hr class="rule">
    <p class="lead">MAPSA matches follow the official rulebook for each sport. New to this? Start with our <a href="/new-shooters/">New Shooter Guide</a>.</p>
    <div class="grid">
      <div class="card">
        <h3>PCSL Rules</h3>
        <ul class="link-list">
          <li><a href="https://www.pcsleague.us/" target="_blank" rel="noopener">Practical Competition Shooting League</a></li>
          <li><a href="https://drive.google.com/file/d/1dnlfHLppF5lB-Sf-HO4ariu4k8mDXM1M/view" target="_blank" rel="noopener">PCSL Rulebook (PDF)</a></li>
        </ul>
      </div>
      <div class="card">
        <h3>USPSA Rules</h3>
        <ul class="link-list">
          <li><a href="https://uspsa.org/rules" target="_blank" rel="noopener">USPSA Rulebooks</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>''', hero=ph("Match Rules", img="photo-1.jpg", pos="40% 28%"))

    photos = [("photo-4.jpg", "Competitor running a pistol stage at a MAPSA match"),
              ("photo-1.jpg", "Shooter engaging targets at a USPSA stage"),
              ("photo-5.jpg", "MAPSA 2-Gun competitors at the range"),
              ("photo-3.jpg", "MAPSA leadership at a match"),
              ("photo-2.jpg", "MAPSA members with match sponsors"),
              ("pcsl-2gun-2025.jpg", "2025 MN PCSL 2-Gun Championship flyer")]
    imgs = "\n".join(f'      <img src="/images/{f}" alt="{a}" loading="lazy">' for f, a in photos)
    page("/photos/", "Photos | MAPSA Practical Shooting Matches",
         "Photos from MAPSA USPSA and PCSL 2-Gun matches and range days in Forest Lake, MN.",
         f'''
<section>
  <div class="wrap">
    <h2>Recent Events</h2>
    <hr class="rule">
    <p class="lead">Moments captured from our latest club meets, shooting range days, and community gatherings.</p>
    <div class="gallery">
{imgs}
    </div>
    <p class="center" style="margin-top:32px"><a class="btn btn-outline" href="{IG}" target="_blank" rel="noopener">More on Instagram</a></p>
  </div>
</section>''', hero=ph("Photos", img="photo-2.jpg", pos="50% 17%"), image="/images/photo-2.jpg")

    page("/404.html", "Page Not Found | MAPSA", "This page doesn't exist.",
         '''
<section>
  <div class="wrap center">
    <h2>Missed the Target</h2>
    <hr class="rule">
    <p class="lead">That page doesn&rsquo;t exist (anymore). Try one of these:</p>
    <p><a class="btn" href="/">Home</a> &nbsp; <a class="btn btn-outline" href="/schedule/">Schedule</a></p>
  </div>
</section>''', hero=ph("404", img="hero-shooter.jpg", pos="62% 30%"))

    # Old WordPress + first-version URLs -> new pages
    for old, new in [("/gallery/", "/photos/"), ("/about.html", "/about-us/"), ("/schedule.html", "/schedule/"),
                     ("/match-rules.html", "/match-rules/"), ("/photos.html", "/photos/"), ("/contact/", "/about-us/")]:
        redirect(old, new)

    today = dt.date.today().isoformat()
    urls = [("/", "1.0"), ("/schedule/", "0.9"), ("/new-shooters/", "0.9"), ("/about-us/", "0.7"), ("/match-rules/", "0.6"), ("/photos/", "0.6")]
    sm = "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n" for u, p in urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w", newline="\n").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w", newline="\n").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    print("Built", len(urls), "pages + 404, redirects, sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
