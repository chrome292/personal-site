#!/usr/bin/env python3
"""
Builds conormaloney.me as plain static HTML into ./site.

Run:  python3 build.py
Then deploy the ./site folder to Netlify (drag-and-drop, or set publish directory = site).

All copy lives in this file. Edit SITE / LINKS below to change the domain or add profiles;
every page, the sitemap and the structured data pick the change up on the next build.
"""
import json, os
from html import escape as e

# ---------------------------------------------------------------- config
SITE = "https://conormaloney.me"          # canonical origin, no trailing slash
EMAIL = "conormaloney29@gmail.com"
LASTMOD = "2026-10-20"
# Outbound profiles. Shown in the footer + contact page and used as schema.org sameAs.
# Add GitHub / HARDWEAR here, e.g. ("GitHub", "https://github.com/USERNAME").
LINKS = [
    ("LinkedIn", "https://www.linkedin.com/in/conormaloney29"),
]
REPO = "https://github.com/chrome292/store-visit-tracker"   # VisitTracker source
# Résumé PDF, served from ./site. The contact page links it only once the file exists.
RESUME = "/assets/conor-maloney-resume.pdf"

NAV = [("Home", "/"), ("Work", "/work/visittracker/"), ("Experience", "/experience/"),
       ("About", "/about/"), ("Contact", "/contact/")]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# ---------------------------------------------------------------- shared chrome
def head(title, desc, path, jsonld=None, og_type="website"):
    url = SITE + path
    ld = ""
    if jsonld:
        ld = '\n<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")) + "</script>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="author" content="Conor Maloney">
<meta name="theme-color" content="#1B2A24">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Conor Maloney">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Conor Maloney, Baltimore, MD">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/newsreader-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

CUR = ' aria-current="page"'

def header(active):
    items = "".join(
        f'<a href="{href}"{CUR if label == active else ""}>{label}</a>'
        for label, href in NAV)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">Conor Maloney.</a>
    <nav class="site-nav" aria-label="Main">{items}</nav>
  </div>
</header>
<main id="main">
"""

def footer(show_cta=True):
    cta = f"""<section class="cta" aria-label="Get in touch">
  <div class="wrap">
    <div class="stack" style="gap:16px">
      <div class="eyebrow">Get in touch</div>
      <a class="mail" href="mailto:{EMAIL}">{EMAIL} ↗</a>
    </div>
    <div class="where">Based in Baltimore. Open to roles in Baltimore and Washington, DC.</div>
  </div>
</section>
""" if show_cta else ""
    profiles = "".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n, u in LINKS)
    return f"""</main>
{cta}<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 Conor Maloney</span>
    <nav aria-label="Footer">
      <a href="/work/visittracker/">Work</a><a href="/experience/">Experience</a><a href="/about/">About</a>{profiles}
    </nav>
  </div>
</footer>
</body>
</html>
"""

def write(path, html):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/404" else os.path.join(OUT, "404.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", os.path.relpath(fp, OUT))

IMG = "/assets/img/"
def phone(name, alt, cls="", w=560, h=1218, lazy=True):
    c = f' class="{cls}"' if cls else ""
    ld = ' loading="lazy"' if lazy else ""
    return f'<img{c} src="{IMG}visittracker-{name}.webp" alt="{e(alt)}" width="{w}" height="{h}"{ld} decoding="async">'

# ---------------------------------------------------------------- content
HOME_ROLES = [
    ("2025 – 2026", "Altria Group Distribution Co.", "Retail Merchandising Associate"),
    ("2025", "Merchant Processing Solutions", "Sales Representative"),
    ("2024 – 2025", "Shift4", "Solutions Specialist"),
    ("2024", "BDS Connected Solutions", "Market Development Manager"),
    ("2022 – 2024", "3 Bean Coffee · Ovenbird Bakery", "Café & Beverage Manager"),
    ("2015 – 2022", "Evergrain Bread Company", "Front of House Manager"),
]

SERVICES = [
    ("Retail merchandising", "At Altria I handled resets, planograms and promotional placement across about 570 convenience and drug stores. Most of the job was working with store managers to get things done right."),
    ("Sales", "I've sold payment and point-of-sale systems to small business owners, cold and by referral. I build the pitch around how the business actually runs."),
    ("Data and tools", "I keep my own numbers. I built a route model that cut my territory driving by 54%, and an iPhone app that logs every store visit on its own."),
    ("Cafés and coffee", "Seven years running the front of house at a bakery café, then beverage programs in Baltimore. I trained baristas and wrote seasonal menus, a few of which stayed on permanently."),
]

VIEWS = [
    ("board", "Board", "Today's visits in order, with a live timer for the store I'm in."),
    ("map-all", "Map", "Every store visited, plus today's route and miles driven."),
    ("stats", "Stats", "Visit counts, average time in store, time on site by weekday, and how many working days in a row are logged."),
    ("store-detail", "Store history", "Twelve weeks per store as a heatmap, showing the usual visit day and arrival time."),
]

PARTS = [
    ("1", "Geocoding tool · TypeScript", "Takes the store list from an Excel export and finds coordinates for each address. If it can't place an address, that store goes into a failure report instead of the app, so nothing gets tracked in the wrong spot. When the list grew from 131 stores to 528, it added only the new ones and left existing visit history alone."),
    ("2", "iPhone app · Swift and SwiftUI", "The app itself. The math lives in its own layer, apart from the screens, and that layer is fully tested. Every number on screen comes from tested code."),
    ("3", "Google Sheets webhook · Apps Script", "Takes each visit from the phone and writes it to the sheet. No server to maintain, and the data lands in a spreadsheet I already used every day."),
]

PROBLEMS = [
    ("iOS only watches 20 locations at a time. I had 528.", "The app keeps a rough fix on where I am without running GPS all day. As I move into a new area, it swaps in the 20 nearest stores."),
    ("Driving past a store isn't a visit.", "Each arrival pops up a lock-screen notification I can confirm or dismiss with one tap. Stops under three minutes get thrown out unless I confirm them."),
    ("No signal can't mean a lost visit.", "Every visit saves to the phone first. Syncing is a separate step that keeps retrying until the sheet confirms it got the row."),
    ("No duplicate rows.", "Each visit has its own ID. If the phone sends the same visit twice, the sheet updates the row that's already there."),
    ("Edits are allowed, and they show.", "I can fix a time, move a visit to the right store in a crowded plaza, or add one the phone missed. Anything edited or entered by hand stays flagged in the data."),
    ("No Google login on the phone.", "Each request carries a secret token stored in the iPhone Keychain. The sheet rejects anything without it."),
]

# (period, company, role, location, summary, bullets)
ROLES = [
    ("Dec 2025 – Oct 2026", "Altria Group Distribution Company", "Retail Merchandising Associate", "Baltimore area",
     "Covered about 570 stores across the Baltimore metro and nearby Maryland counties, including 7-Eleven, Royal Farms, Wawa, Walgreens and Food Lion.", [
        "Built a route model using geographic clustering and shortest-path solving. It cut total territory driving by 54% and let me fit more stores into a day.",
        "Built VisitTracker, an iPhone app that logged every store visit automatically.",
        "Ran resets, planogram compliance and POS placement, logged in the company's Salesforce-based field app.",
        "Kept my own Excel tracking of visits and GPS data to catch gaps and errors in the visit record.",
        "Worked with store managers on promotions to improve placement and sell-through.",
        "Recognized company-wide in Q2 for store-level execution. Pitched an original product idea through the company's innovation program.",
    ]),
    ("May – Jul 2025", "Merchant Processing Solutions", "Sales Representative (contract)", "Annapolis, MD", "", [
        "Met 10 to 15 business owners a week, cold and by referral.",
        "Built pricing and equipment proposals from each merchant's card volume and how they ran.",
    ]),
    ("Dec 2024 – Feb 2025", "Shift4", "Solutions Specialist", "Baltimore to Washington, DC", "", [
        "Sold payment and point-of-sale systems to businesses between Baltimore and DC. Beat my sales targets.",
        "Put together hardware and software packages for each client, then ran the demo and trained their staff on site.",
        "Managed my own Salesforce pipeline from first contact through setup.",
    ]),
    ("Jun – Dec 2024", "BDS Connected Solutions", "Market Development Manager", "Philadelphia, PA", "", [
        "Trained retail staff and ran live product demos across a group of stores.",
        "Worked with store leaders on placement. Set up in-store displays and campaigns.",
    ]),
    ("Oct 2023 – Jun 2024", "3 Bean Coffee by Vagrant Coffee", "Café Manager", "Baltimore, MD", "", [
        "Reworked the menu around what customers were buying.",
        "Ran scheduling, inventory and food cost. Trained baristas and rotated seasonal menus.",
        "Grew sales 15% with new food and drink options, standardized recipes and procedures, and the café's social media.",
    ]),
    ("Jan 2022 – Aug 2023", "Ovenbird Bakery", "Beverage Manager / Head Barista", "Baltimore, MD", "", [
        "Grew total beverage sales 400% in my first year: a new seasonal drink program, more food and drink options, standardized recipes, and social media.",
        "Wrote barista training for technique and consistency.",
        "Developed signature drinks through testing and customer feedback. Several became permanent menu items.",
    ]),
    ("Jun 2015 – Apr 2022", "Evergrain Bread Company", "Front of House Manager / Head Barista", "Chestertown, MD", "", [
        "Ran daily café operations for seven years alongside the bakery and kitchen teams.",
        "Hired and trained the front-of-house staff.",
        "Wrote seasonal menus that built a loyal local following.",
        "Handled scheduling, ordering and the POS.",
    ]),
]

# Shorter side jobs, listed under "Also". Leave dates "" when unknown.
ALSO = [
    ("Productions Plus", "Brand Ambassador / Coffee Advisor", "Arlington, VA", "Aug – Sep 2025 (seasonal)", "Ran weekly Nespresso tastings in retail stores and helped customers pick machines."),
    ("Miel Coffee Co", "Event Barista", "Washington, DC", "", "Ran a mobile espresso bar for private and corporate events, with a custom drink menu for each."),
]

SKILLS = [
    ("Analytics and systems", "Excel modeling and reporting · Route optimization · Territory mapping · Salesforce · POS systems"),
    ("Sales", "Territory management · B2B and B2C sales · Consultative selling · Pipeline management · Cold and referral outreach"),
    ("Retail and merchandising", "Planogram compliance · Resets · Visual display · POS placement · Product promotion"),
    ("Leadership and training", "Hiring · Coaching · Training program design"),
    ("Operations", "Inventory and cost control · Scheduling · Front and back of house · Vendor ordering · Microsoft Office · Adobe Creative Suite"),
]

# ---------------------------------------------------------------- structured data
PERSON_ID = SITE + "/#person"
PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Conor Maloney",
    "url": SITE + "/",
    "image": SITE + "/assets/img/conor-maloney.jpg",
    "email": "mailto:" + EMAIL,
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Washington College"},
    "address": {"@type": "PostalAddress", "addressLocality": "Baltimore", "addressRegion": "MD", "addressCountry": "US"},
    "description": "Field sales and retail merchandising professional in Baltimore, MD. Builds his own tools, including VisitTracker, an iPhone app that logs store visits automatically.",
    "knowsAbout": ["Field sales", "Merchandising", "Route optimization", "Sales", "Data analytics", "Salesforce", "Swift", "Specialty coffee"],
    "sameAs": [u for _, u in LINKS],
}

def home_ld():
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Conor Maloney", "inLanguage": "en", "publisher": {"@id": PERSON_ID}},
        {"@type": "ProfilePage", "@id": SITE + "/#profile", "url": SITE + "/", "name": "Conor Maloney", "isPartOf": {"@id": SITE + "/#website"},
         "dateModified": LASTMOD, "mainEntity": {"@id": PERSON_ID}},
        PERSON,
    ]}

def page_ld(path, name, typ="WebPage", extra=None):
    d = {"@context": "https://schema.org", "@type": typ, "url": SITE + path, "name": name,
         "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website"},
         "about": {"@id": PERSON_ID}, "author": {"@type": "Person", "@id": PERSON_ID, "name": "Conor Maloney", "url": SITE + "/"}}
    if extra: d.update(extra)
    return d

# ---------------------------------------------------------------- pages
def page_home():
    services = "".join(f'<div><h3>{e(t)}</h3><p class="body">{e(d)}</p></div>' for t, d in SERVICES)
    roles = "".join(f'<li><span class="yrs">{e(y)}</span><span class="co">{e(c)}</span><span class="rl">{e(r)}</span></li>' for y, c, r in HOME_ROLES)
    return head("Conor Maloney — Field Sales, Marketing & Analytics | Baltimore, MD",
                "Conor Maloney is a Baltimore-based field sales and retail merchandising professional with ten years in cafés and retail. He builds his own tools, including VisitTracker, an iPhone app that logs store visits automatically.",
                "/", home_ld(), "profile") + header("Home") + f"""
<div class="wrap hero">
  <div class="hero-text">
    <div class="eyebrow">Field sales · Merchandising · Marketing · Analytics</div>
    <h1>Conor Maloney</h1>
    <p class="hero-intro">I've worked in cafés, field sales and retail merchandising since 2015. Most recently I covered about 570 stores across Maryland for Altria. I like being out with customers, and I like knowing whether the work is paying off. When a process wastes time, I build something to fix it.</p>
    <div class="actions">
      <a class="btn" href="/experience/">Experience</a>
      <a class="btn-outline" href="/about/">About me</a>
      <a class="arrow-link" href="mailto:{EMAIL}">Email me →</a>
    </div>
  </div>
  <figure class="hero-portrait">
    <picture><source srcset="{IMG}conor-maloney.webp" type="image/webp"><img src="{IMG}conor-maloney.jpg" alt="Portrait of Conor Maloney" width="800" height="800" fetchpriority="high"></picture>
    <figcaption>Baltimore, MD</figcaption>
  </figure>
</div>

<section class="wrap section split" aria-labelledby="what-i-do">
  <div class="label wide"><h2 id="what-i-do" class="h2-lg">What I do</h2></div>
  <div class="services">{services}</div>
</section>

<section class="wrap section section-last feature" aria-labelledby="visittracker">
  <div class="feature-text">
    <div class="eyebrow accent">A tool I built for my own route</div>
    <h2 id="visittracker">VisitTracker</h2>
    <p class="body" style="font-size:17px">An iPhone app that notices when I walk into one of my stores and logs the visit: arrival, departure and time on site. Each visit goes straight to a Google Sheet. I never have to tap anything.</p>
    <ul class="tags"><li>Swift</li><li>Core Location</li><li>Apps Script</li><li>TypeScript</li></ul>
    <div class="actions" style="margin-top:8px">
      <a class="arrow-link" href="/work/visittracker/">How I built it →</a>
      <a class="arrow-link" href="{REPO}" rel="noopener" target="_blank">Code on GitHub ↗</a>
    </div>
  </div>
  <a class="stage stage-home" href="/work/visittracker/" aria-label="Read the VisitTracker case study">
    {phone("ledger", "VisitTracker visits ledger screen")}
    {phone("board", "VisitTracker visits board with a live in-store timer", "mid")}
    {phone("stats", "VisitTracker weekly stats screen")}
  </a>
</section>

<section class="wrap section-last split" aria-labelledby="history">
  <div class="label wide" style="gap:16px">
    <h2 id="history" class="h2-lg">Where I've worked</h2>
    <a class="arrow-link" href="/experience/" style="font-size:15px">Full work history →</a>
  </div>
  <ul class="plain roles-brief ruled ruled-end">{roles}</ul>
</section>
""" + footer()

def page_work():
    views = "".join(f'<figure><div class="shot">{phone(k, f"VisitTracker {t} screen")}</div><figcaption><h3>{e(t)}</h3><p>{e(d)}</p></figcaption></figure>' for k, t, d in VIEWS)
    parts = "".join(f'<li><span class="n">{n}</span><div><h3>{e(t)}</h3><p class="body">{e(d)}</p></div></li>' for n, t, d in PARTS)
    probs = "".join(f'<li><h3>{e(t)}</h3><p class="body">{e(d)}</p></li>' for t, d in PROBLEMS)
    path = "/work/visittracker/"
    ld = page_ld(path, "VisitTracker case study", "Article", {
        "headline": "VisitTracker: an iPhone app that logs store visits automatically",
        "description": "How Conor Maloney designed and built VisitTracker, a Swift iPhone app that used geofencing to log arrivals, departures and time on site across 528 stores and sync every visit to Google Sheets.",
        "image": SITE + "/assets/img/og.jpg", "datePublished": "2026-08-31", "dateModified": LASTMOD, "inLanguage": "en",
    })
    return head("VisitTracker: An iPhone App That Logs Store Visits Automatically — Conor Maloney",
                "How Conor Maloney designed and built VisitTracker, a Swift iPhone app that used geofencing to log arrivals, departures and time on site across 528 stores and sync every visit to Google Sheets.",
                path, ld, "article") + header("Work") + f"""
<article>
<div class="wrap page-head" style="padding-bottom:56px">
  <div class="eyebrow accent">Case study · Built July–August 2026</div>
  <h1 class="display">VisitTracker</h1>
  <p class="serif" style="font-size:clamp(22px,2.4vw,30px);line-height:1.3;color:var(--ink-2);max-width:760px;text-wrap:pretty">An iPhone app that logged my store visits on its own, so I had an accurate record of where my workday went.</p>
</div>
<div class="wrap">
  <dl class="facts">
    <div><dt>Role</dt><dd>Designed, built and used it myself</dd></div>
    <div><dt>Scale</dt><dd>528 stores · about 200 automated tests</dd></div>
    <div><dt>Built with</dt><dd>Swift, SwiftUI, Core Location, Core Data, Google Apps Script, TypeScript</dd></div>
    <div><dt>Code</dt><dd><a class="inline-link" href="{REPO}" rel="noopener" target="_blank">github.com/chrome292/store-visit-tracker ↗</a></dd></div>
  </dl>
  <div class="stage stage-case">
    {phone("ledger", "Visits ledger", lazy=False)}
    {phone("board", "Visits board with live in-store timer", "mid", lazy=False)}
    {phone("map-today", "Map of today's route", lazy=False)}
  </div>
</div>

<section class="wrap section split">
  <div class="label"><span class="num">01</span><h2 class="h2">The problem</h2></div>
  <div class="content">
    <p class="body-lg">My Altria territory had about 570 stores across Maryland. Time in store was one of the main ways my work got measured, and nothing recorded it well. Logging by hand meant stopping at every store to write down times, rounding them, and sometimes missing one.</p>
    <p class="body-lg">I had solid data on almost everything except my own day. I wanted the phone to keep that record for me.</p>
  </div>
</section>

<section class="wrap section">
  <div class="split">
    <div class="label"><span class="num">02</span><h2 class="h2">What I built</h2></div>
    <div class="content">
      <p class="body-lg">The app runs in the background. When I walk into one of my stores, it logs the arrival. When I leave, it logs the departure and the time on site. Each visit goes to a Google Sheet. There's nothing to tap.</p>
      <p class="body-lg">The app shows the data four ways.</p>
    </div>
  </div>
  <div class="views">{views}</div>
</section>

<section class="wrap section split">
  <div class="label"><span class="num">03</span><h2 class="h2">How I built it</h2></div>
  <div class="content" style="gap:0">
    <p class="body-lg" style="margin-bottom:24px">Three separate pieces.</p>
    <ol class="plain parts ruled">{parts}</ol>
    <p class="note">I wrote a short spec before building each feature. I built it with AI coding tools. I made the design decisions, told the tools what to build, and tested every piece myself.</p>
  </div>
</section>

<section class="wrap section stack" style="gap:40px">
  <div class="stack" style="gap:8px"><span class="num">04</span><h2 class="h2">Problems I had to solve</h2></div>
  <ul class="plain problems">{probs}</ul>
</section>

<section class="wrap section section-last split">
  <div class="label"><span class="num">05</span><h2 class="h2">The result</h2></div>
  <div class="content" style="max-width:760px">
    <p class="result">A minute-by-minute record of every store visit across the territory, in a spreadsheet I could sort and analyze. I didn't have to log a thing.</p>
    <div class="actions">
      <a class="arrow-link" href="/experience/">Full work history →</a>
      <a class="arrow-link" href="{REPO}" rel="noopener" target="_blank">Code on GitHub ↗</a>
    </div>
  </div>
</section>
</article>
""" + footer()

def page_experience():
    roles = ""
    for period, co, role, loc, summary, bullets in ROLES:
        d = (f'<p class="body">{e(summary)}</p>' if summary else "") + "<ul>" + "".join(f"<li>{e(b)}</li>" for b in bullets) + "</ul>"
        roles += f'<li class="role"><div class="period">{e(period)}</div><div class="who"><h2>{e(co)}</h2><div class="title">{e(role)}</div><div class="loc">{e(loc)}</div></div><div class="desc">{d}</div></li>'
    also = "".join(
        f'<li><strong>{e(co)},</strong> {e(role)} · {e(loc)}{" · " + e(dates) if dates else ""}. {e(desc)}</li>'
        for co, role, loc, dates, desc in ALSO)
    path = "/experience/"
    return head("Work History — Conor Maloney",
                "Conor Maloney's work history since 2015: retail merchandising at Altria, field sales at Shift4, Merchant Processing Solutions and BDS Connected Solutions, and café management in Baltimore and Chestertown, MD.",
                path, page_ld(path, "Work History — Conor Maloney", "ProfilePage", {"mainEntity": {"@id": PERSON_ID}})) + header("Experience") + f"""
<div class="wrap page-head" style="gap:24px;padding-bottom:64px">
  <div class="eyebrow">Experience · 2015 – 2026</div>
  <h1 class="display">Work history</h1>
  <p class="body-lg" style="font-size:19px;line-height:1.55;max-width:640px">Cafés first, then field sales and retail merchandising. Newest first.</p>
</div>
<div class="wrap section-last">
  <ol class="plain">{roles}
    <li class="role"><div class="period">Also</div><div class="desc"><ul class="also">{also}</ul></div></li>
    <li class="role"><div class="period">Education</div><div class="who"><h2>Washington College</h2><div class="title">B.A., Music &amp; Theatre</div><div class="loc">Chestertown, MD</div></div></li>
  </ol>
</div>
""" + footer()

def page_about():
    skills = "".join(f'<li><h3 class="kicker">{e(g)}</h3><p>{e(i)}</p></li>' for g, i in SKILLS)
    path = "/about/"
    return head("About Conor Maloney",
                "Washington College music and theatre graduate, industrial electronic musician (HARDWEAR), and former Altria merchandiser who covered about 570 stores across Maryland and built his own tools to do it.",
                path, page_ld(path, "About Conor Maloney", "AboutPage", {"mainEntity": {"@id": PERSON_ID}})) + header("About") + f"""
<div class="wrap about section-last">
  <div class="about-text">
    <div class="eyebrow">About</div>
    <h1 class="display" style="font-size:clamp(52px,7vw,88px);line-height:1">Hi, I'm Conor.</h1>
    <p class="lede-serif" style="max-width:680px">I like problems that are part creative and part logistics. A messy process to clean up. A route to plan. A display that isn't selling.</p>
    <div class="stack" style="gap:20px;max-width:640px">
      <p class="body-lg">I studied music and theatre at Washington College, and I still make music. I produce industrial electronic music as HARDWEAR.</p>
      <p class="body-lg">After college I spent seven years running the front of house at a bakery café in Chestertown, then managed beverage programs in Baltimore. From there I moved into field sales, selling payment systems to small businesses. Most recently I worked in retail merchandising for Altria, covering about 570 stores across Maryland.</p>
      <p class="body-lg">That's where I started building my own tools. Planning a day across hundreds of stores is a scheduling problem, so I treated it like one. I wrote a route model that cut my driving by 54% and built <a class="inline-link" href="/work/visittracker/">VisitTracker</a>, an app that logged my store visits on its own. Neither was part of the job.</p>
      <p class="body-lg">In every job I've paid attention to the small stuff: how people move through a store, which displays get picked up, where time gets wasted. Then I fix what I can.</p>
    </div>
    <a class="arrow-link" href="/experience/">See my work history →</a>
    <div class="stack" style="gap:20px;max-width:640px;padding-top:24px;border-top:1px solid var(--line)">
      <h2 class="h2">How I work</h2>
      <p class="body-lg">I do my best work when the goal is clear and I'm trusted to figure out how to get there. Give me the target and I'll come back with a plan. I keep my manager posted along the way.</p>
      <p class="body-lg">I like variety, a new problem every so often, and a team that can laugh a little. And I care about the people right in front of me: the store manager, the person on the next shift, the regular at the counter.</p>
    </div>
  </div>
  <aside class="about-side">
    <picture><source srcset="{IMG}conor-maloney.webp" type="image/webp"><img src="{IMG}conor-maloney.jpg" alt="Portrait of Conor Maloney" width="800" height="800"></picture>
    <div class="skills">
      <h2>Skills</h2>
      <ul class="plain">{skills}</ul>
    </div>
  </aside>
</div>
""" + footer()

def page_contact():
    items = ""
    if os.path.exists(os.path.join(OUT, RESUME.lstrip("/"))):
        items += f'<li><a href="{RESUME}" download>Download my résumé (PDF) ↓</a></li>'
    items += "".join(f'<li><a href="{u}" rel="me noopener" target="_blank">{n} ↗</a></li>' for n, u in LINKS)
    path = "/contact/"
    return head("Contact Conor Maloney",
                "Get in touch with Conor Maloney about field sales, merchandising, marketing and analytics roles in Baltimore and Washington, DC.",
                path, page_ld(path, "Contact Conor Maloney", "ContactPage", {"mainEntity": {"@id": PERSON_ID}})) + header("Contact") + f"""
<div class="wrap contact">
  <div class="eyebrow">Contact</div>
  <h1 class="display">Get in touch</h1>
  <p style="font-size:clamp(18px,1.8vw,22px);line-height:1.5;color:var(--ink-2);max-width:620px;text-wrap:pretty">I'm looking for field sales, merchandising, marketing and analytics roles in Baltimore or Washington, DC. Email is the fastest way to reach me.</p>
  <a class="big-mail" href="mailto:{EMAIL}">{EMAIL} ↗</a>
  <ul class="elsewhere">{items}</ul>
  <div style="font-size:15px;color:var(--muted)">Based in Baltimore. Open to roles in DC.</div>
</div>
""" + footer(show_cta=False)

def page_404():
    h = head("Page not found — Conor Maloney", "This page doesn't exist. Head back to Conor Maloney's homepage.", "/404.html")
    h = h.replace("<meta name=\"author\"", "<meta name=\"robots\" content=\"noindex\">\n<meta name=\"author\"")
    return h + header("") + """
<div class="wrap contact">
  <div class="eyebrow">404</div>
  <h1 class="display">Nothing here.</h1>
  <p class="body-lg">That page doesn't exist, or it moved when the site was rebuilt.</p>
  <div class="actions"><a class="btn" href="/">Go to the homepage</a><a class="arrow-link" href="/work/visittracker/">Read the VisitTracker case study →</a></div>
</div>
""" + footer()

PAGES = [("/", page_home, "1.0"), ("/work/visittracker/", page_work, "0.9"), ("/experience/", page_experience, "0.8"),
         ("/about/", page_about, "0.8"), ("/contact/", page_contact, "0.6")]

def main():
    for path, fn, _ in PAGES:
        write(path, fn())
    write("/404", page_404())
    urls = "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr}</priority></url>\n" for p, _, pr in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    main()
