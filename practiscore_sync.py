"""
Pull MAPSA's upcoming matches + events from PractiScore into practiscore.json.
No AI involved -- it just reads the public club page.

    python practiscore_sync.py              # fetch live page
    python practiscore_sync.py --html f.html  # parse a saved copy (testing)

Then `python build.py` puts them on the site. The GitHub Action in
.github/workflows/practiscore.yml runs both automatically every day.

If PractiScore can't be reached or the page layout changes, the script exits
with an error and leaves practiscore.json untouched, so the site never breaks.
"""
import datetime as dt, html, json, os, re, sys, urllib.request

CLUB_URL = "https://practiscore.com/clubs/mapsa_at_flsc"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "practiscore.json")

BLOCK = re.compile(r'<div class="clearfix( event_item)?" id="item_\d+"')
STATUS = re.compile(r'<span class="label[^"]*">\s*([^<]*?)\s*</span>')
LINK = re.compile(r'<a href="([^"]+)">([^<]+)</a>')
DATE = re.compile(r'<small>\s*<div>\s*([A-Z][a-z]+ \d{1,2}, \d{4})')
TYPE = re.compile(r'</div>\s*<div>\s*([^<]+?)\s*</div>\s*</small>')

def fetch():
    req = urllib.request.Request(CLUB_URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def parse(page):
    start = page.find("Upcoming Matches")
    end = page.find("Match Results", start)
    if start < 0 or end < 0:
        sys.exit("PractiScore page layout changed (couldn't find 'Upcoming Matches') -- not updating.")
    section = page[start:end]
    matches, events = [], []
    starts = list(BLOCK.finditer(section))
    for i, m in enumerate(starts):
        chunk = section[m.start(): starts[i + 1].start() if i + 1 < len(starts) else len(section)]
        link, date, status = LINK.search(chunk), DATE.search(chunk), STATUS.search(chunk)
        if not (link and date):
            continue
        item = {"name": html.unescape(link.group(2)).strip(),
                "date": dt.datetime.strptime(date.group(1), "%B %d, %Y").date().isoformat(),
                "url": html.unescape(link.group(1)),
                "status": status.group(1).strip().lower() if status else ""}
        if m.group(1):
            events.append(item)
        else:
            t = TYPE.search(chunk)
            item["type"] = re.sub(r"\s+", " ", html.unescape(t.group(1))).strip() if t else ""
            matches.append(item)
    key = lambda x: (x["date"], x["name"])
    return {"source": CLUB_URL, "matches": sorted(matches, key=key), "events": sorted(events, key=key)}

def main():
    if "--html" in sys.argv:
        page = open(sys.argv[sys.argv.index("--html") + 1], encoding="utf-8").read()
    else:
        try:
            page = fetch()
        except Exception as e:
            sys.exit(f"Couldn't reach PractiScore ({e}) -- not updating.")
    data = parse(page)
    if not data["matches"] and not data["events"] and "Active Matches" not in page:
        sys.exit("Found nothing on the PractiScore page (blocked or layout changed?) -- not updating.")
    new = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if new == old:
        print("PractiScore: no changes.")
        return
    open(OUT, "w", encoding="utf-8", newline="\n").write(new)
    print(f"PractiScore: saved {len(data['matches'])} matches, {len(data['events'])} events.")
    for m in data["matches"] + data["events"]:
        print(f"  {m['date']}  [{m['status']}]  {m['name']}")

if __name__ == "__main__":
    main()
