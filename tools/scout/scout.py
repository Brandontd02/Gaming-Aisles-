#!/usr/bin/env python3
"""Gaming Aisles Scout v1. Public itch.io RSS discovery -> private Airtable review inbox.
No AI claims: deterministic keyword triage, all decisions are tentative.
"""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = os.environ.get("AIRTABLE_BASE_ID", "app8RCmRrP4YcQ043")
INBOX = os.environ.get("AIRTABLE_SCOUT_TABLE_ID", "tbl170LhV6VciWryj")
TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1" or not TOKEN
LIMIT = int(os.environ.get("SCOUT_LIMIT", "12"))
HEADERS = {"User-Agent": "GamingAislesScout/0.1 (game discovery research)"}
FEEDS = [
    "https://itch.io/feed/new.xml",
    "https://itch.io/feed/featured.xml",
    "https://itch.io/games/free.xml",
]
FIELDS = {
 "title":"flddNbSpem0gSHSis", "source":"fldXk5Hv1QqkLjkp5",
 "url":"fld7q8hvsTIywXx9l", "evidence":"fldpF06c0ORzRKXIB",
 "shelf":"fldCM0JXruDhfoNwa", "pillar":"fldicI9on6LOAtZKk",
 "reason":"fldMa4MC9iyTTaiju", "status":"fldB02PUP9cwoui4y",
 "date":"fldX2vb7BeQe4qCAG", "key":"fldAnnfL0vQYKuGcO"
}
TERMS = {
 "Rhythm & Flow": ("rhythm","music","beat","soundtrack","dance","timing","flow","arcade"),
 "Atmosphere & Dread": ("horror","surreal","liminal","psychological","mystery","haunted","dream","nightmare","atmospheric","weird"),
 "The Cipher": ("political","detective","conspiracy","survival","dystopia","systemic","revolution","crime","simulation","narrative"),
}
def request(url, method="GET", body=None, auth=False):
    h = dict(HEADERS)
    if auth:
        h["Authorization"] = "Bearer " + TOKEN
    if body is not None:
        h["Content-Type"] = "application/json"
        body = json.dumps(body).encode()
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()

def clean(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or "")).strip()

def canonical(url):
    p = urllib.parse.urlsplit(url.strip())
    return (p.netloc.lower() + p.path.rstrip("/")).lower()

def existing():
    if DRY_RUN:
        return set(), set()
    urls, names = set(), set()
    for table, field in [(INBOX, FIELDS["url"]), ("tblp97q5q1SPohHIb", "fldmWMaEdvArm4D14"), ("tblO5nClruDII8WrB", "fldNwPr4xgz1QMSsL")]:
        offset = None
        while True:
            qs = {"pageSize": 100, "fields[]": field}
            if offset:
                qs["offset"] = offset
            uri = f"https://api.airtable.com/v0/{BASE}/{table}?" + urllib.parse.urlencode(qs)
            data = json.loads(request(uri, auth=True))
            for record in data.get("records", []):
                v = record.get("fields", {}).get(field)
                if v:
                    (urls if field == FIELDS["url"] else names).add(canonical(v) if field == FIELDS["url"] else str(v).strip().casefold())
            offset = data.get("offset")
            if not offset:
                break
    return urls, names

def collect():
    out = {}
    for feed in FEEDS:
        try:
            root = ET.fromstring(request(feed))
            for item in root.findall(".//item"):
                title = clean(item.findtext("title"))
                link = (item.findtext("link") or "").strip()
                desc = clean(item.findtext("description"))
                if not title or not link:
                    continue
                key = canonical(link)
                if key and key not in out:
                    out[key] = (title, link, desc[:1200], feed)
        except Exception as exc:
            print(f"Feed failed: {feed}: {exc}", file=sys.stderr)
    return out

def classify(title, description):
    sample = (title + " " + description).lower()
    scores = {p: sum(1 for word in words if re.search(r"\b" + re.escape(word) + r"\b", sample)) for p, words in TERMS.items()}
    pillar = max(scores, key=scores.get)
    if scores[pillar] == 0:
        return None
    keywords = [w for w in TERMS[pillar] if re.search(r"\b" + re.escape(w) + r"\b", sample)]
    shelf = "Flow State" if pillar == "Rhythm & Flow" else ("Return Bin" if "free" in sample or "/free" in sample else "Unclear")
    return pillar, shelf, keywords, scores[pillar]

def main():
    oldurls, oldnames = existing()
    pool = []
    for key, (title, link, desc, feed) in collect().items():
        if key in oldurls or title.casefold() in oldnames:
            continue
        result = classify(title, desc)
        if not result:
            continue
        pillar, shelf, words, score = result
        fields = {
            FIELDS["title"]:title[:255],
            FIELDS["source"]:"itch.io",
            FIELDS["url"]:link,
            FIELDS["evidence"]:desc or "See source page.",
            FIELDS["pillar"]:pillar,
            FIELDS["shelf"]:shelf,
            FIELDS["reason"]:"Keyword hypothesis only: " + ", ".join(words) + ". Check gameplay, pricing, developer and shelf criteria manually. Feed: " + feed,
            FIELDS["status"]:"Unreviewed",
            FIELDS["date"]:dt.datetime.now(dt.timezone.utc).date().isoformat(),
            FIELDS["key"]:key[:255]
        }
        pool.append((score, fields))
    pool.sort(key=lambda x:(-x[0], x[1][FIELDS["title"]].lower()))
    chosen = [fields for _,fields in pool[:max(0,LIMIT)]]
    print(json.dumps({"dry_run":DRY_RUN, "feeds":len(FEEDS), "matched":len(pool), "selected":chosen}, indent=2))
    if DRY_RUN:
        return
    for index in range(0,len(chosen),10):
        batch = chosen[index:index+10]
        request(f"https://api.airtable.com/v0/{BASE}/{INBOX}", method="POST",
                body={"records":[{"fields":f} for f in batch], "typecast":False},auth=True)
        time.sleep(0.3)
    print(f"Created {len(chosen)} Airtable scout records.")

if __name__ == "__main__":
    main()
