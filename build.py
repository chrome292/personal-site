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
LASTMOD = "2026-09-28"
# Outbound profiles. Shown in the footer + contact page and used as schema.org sameAs.
# Add GitHub / HARDWEAR here, e.g. ("GitHub", "https://github.com/USERNAME").
LINKS = [
    ("LinkedIn", "https://www.linkedin.com/in/conormaloney29"),
]

NAV = [("Home", "/"), ("Work", "/work/storetracker/"), ("Experience", "/experience/"),
       ("About", "/about/"), ("What Drives Me", "/what-drives-me/"), ("Contact", "/contact/")]

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
<meta property="og:image:alt" content="Conor Maloney — Field operations, sales and analytics">
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
    <div class="where">Baltimore, MD — Washington, DC</div>
  </div>
</section>
""" if show_cta else ""
    profiles = "".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n, u in LINKS)
    return f"""</main>
{cta}<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 Conor Maloney</span>
    <nav aria-label="Footer">
      <a href="/work/storetracker/">Work</a><a href="/experience/">Experience</a><a href="/about/">About</a>{profiles}
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
    return f'<img{c} src="{IMG}storetracker-{name}.webp" alt="{e(alt)}" width="{w}" height="{h}"{ld} decoding="async">'

# ---------------------------------------------------------------- content
HOME_ROLES = [
    ("2025 – now", "Altria Group Distribution Co.", "Retail Merchandising Associate"),
    ("2024 – 2025", "Shift4", "Solutions Specialist"),
    ("2024", "BDS Connected Solutions", "Market Development Manager"),
    ("2022 – 2024", "3 Bean Coffee · Ovenbird Bakery", "Cafe & Beverage Manager"),
    ("2015 – 2022", "Evergrain Bread Company", "Front of House Manager"),
]

SERVICES = [
    ("Field operations", "I run a retail territory day to day: store relationships, merchandising standards and execution across hundreds of locations."),
    ("Sales and programs", "I build and launch programs that move product, then measure what worked and adjust."),
    ("Analytics and systems", "I turn route, visit and sales data into decisions, and when a process is slow or error-prone I build the tool that fixes it."),
    ("Hospitality and specialty coffee", "Years behind the bar taught me service under pressure, consistency at volume and how small details shape a customer's experience."),
]

VIEWS = [
    ("board", "Board", "Today's visits laid out like an arrivals board, with a live “in store now” card for the current stop."),
    ("map-all", "Map", "Every store visited, plus the day's route and distance traveled."),
    ("stats", "Stats", "Visit counts, average time in store, on-site time by weekday, and a working-day streak."),
    ("store-detail", "Store history", "A 12-week heatmap per store showing the usual visit day and typical arrival time."),
]

PARTS = [
    ("1", "Geocoding tool · TypeScript", "Reads the store list from an Excel export and converts each address to coordinates. Addresses it can't locate go into a failure report and stay out of the app, so no store is tracked in the wrong place. A merge mode adds only new locations, which kept 131 stores' visit history intact as the catalog grew to 528."),
    ("2", "iPhone app · Swift and SwiftUI", "Holds the core logic. Business logic lives in a separate, fully tested layer apart from the screens, so every number the app shows is calculated and verified."),
    ("3", "Google Sheets webhook · Apps Script", "Receives visits from the phone and writes them to the spreadsheet. The data lands in a tool I already use every day, with no server to maintain."),
]

PROBLEMS = [
    ("iOS watches only 20 locations at a time. I needed 528.", "The app tracks my general location in a battery-efficient way and, as I move into a new area, swaps in the 20 closest stores. It covers the whole territory without running continuous GPS."),
    ("Driving past a store shouldn't count as a visit.", "A lock-screen notification lets me confirm or reject each arrival with one tap, and any stop under three minutes is discarded unless I've confirmed it."),
    ("No visit gets lost, even with no signal.", "Every visit is saved on the phone first. Sync is a separate step that retries until the spreadsheet confirms receipt. A dead zone just means the visit waits in line."),
    ("No duplicate rows, ever.", "Each visit has a unique ID, and the spreadsheet updates existing rows instead of appending. A visit sent twice still ends up as exactly one row."),
    ("Corrections are allowed, and they're visible.", "I can fix a time, move a visit to the right store in a crowded plaza, or add one the phone missed. Every edited or hand-entered visit is permanently flagged in the data."),
    ("Secure without a login.", "The phone never signs in to Google. Each request carries a secret token stored in the iPhone Keychain, and the spreadsheet rejects anything without it."),
]

ROLES = [
    ("Dec 2025 – Present", "Altria Group Distribution Company", "Retail Merchandising Associate", "Greater Baltimore Metropolitan Area", "Manage a 570-store territory across the Baltimore metro and surrounding Maryland counties, including 7-Eleven, Royal Farms, Wawa, Walgreens and Food Lion. Built a route optimization system using geographic clustering and exact shortest-path solving that increased daily store call volume. Run merchandising resets, planogram compliance and POS placement, logged through Frontier, the company's Salesforce-based field platform. Built Excel territory analytics (visit tracking, GPS reconciliation and anomaly flagging) to validate field coverage against reported metrics. Partner with store managers on promotional execution to drive visibility and sell-through. Recognized at the AGDC level in Q2 for store-level execution, and submitted an original product concept through the internal innovation portal."),
    ("May – Jul 2025", "Merchant Processing Solutions", "Merchant Services Sales Representative", "Annapolis, MD", "Met with 10–15 business owners a week through in-person cold and referral consultations. Built payment technology and pricing proposals from each merchant's transaction volume and operations."),
    ("Dec 2024 – Feb 2025", "Shift4", "Solutions Specialist", "Baltimore – Washington, DC", "Exceeded field sales targets selling integrated payment and point-of-sale technology across the Baltimore–DC corridor. Designed hardware and software packages around client operations, then ran on-site demos and staff training. Managed the full Salesforce pipeline from prospecting through close and onboarding."),
    ("Jun – Dec 2024", "BDS Connected Solutions", "Market Development Manager", "Philadelphia, PA", "Delivered product training and live demos to retail staff across a multi-store territory. Worked with store leadership to improve brand visibility and placement, and executed in-store campaigns and displays."),
    ("Oct 2023 – Jun 2024", "3 Bean Coffee by Vagrant Coffee", "Cafe Manager", "Baltimore, MD", "Restructured the product lineup around customer preference and market trends. Managed scheduling, inventory and cost control, trained baristas, and curated rotating seasonal menus."),
    ("Jan 2022 – Aug 2023", "Ovenbird Bakery", "Beverage Manager / Head Barista", "Baltimore, MD", "Developed and launched a seasonal beverage program. Built barista training for technique and consistency, and created signature recipes through testing and customer feedback, several of which became permanent."),
    ("Jun 2015 – Apr 2022", "Evergrain Bread Company", "Front of House Manager / Head Barista", "Chestertown, MD", "Ran daily cafe operations for seven years alongside bakery and kitchen staff. Hired and trained front-of-house staff, curated seasonal menus that built a loyal local following, and ran scheduling, inventory sourcing and POS operations."),
    ("Additional", "Miel Coffee Co", "Event Barista", "Washington, DC", "Operated a mobile espresso service for private and corporate events, building custom drink menus for each client."),
    ("Additional", "Productions Plus", "Brand Ambassador / Coffee Advisor", "Arlington, VA", "Represented Nespresso in retail, running weekly tastings and consultative product recommendations."),
    ("Education", "Washington College", "Bachelor of Arts, Music & Theatre", "Chestertown, MD", ""),
]

MOTIVATORS = [
    ("Empathy", "I like understanding where someone is actually coming from. It’s what made me an effective barista trainer and a better salesperson than the pitch-first approach ever did."),
    ("Learning", "I’m happiest when I’m picking something up I didn’t know a month ago, whether that’s route optimization math, Salesforce, or how a roaster thinks about sourcing."),
    ("Creativity", "I want to find a better way to do a thing. The seasonal drink programs, the product concept I submitted through the innovation portal, the territory analytics I built in Excel to make our route data usable. That is the part of the job I look forward to most."),
    ("Fun", "A relaxed room is a productive room. I try to bring some levity to wherever I’m working, because people who are at ease communicate more openly, and that makes the work better."),
    ("Impact", "I need to see that the work moved something. A 54% drop in drive distance. A café’s sales up 15%. Regulars who kept coming back after I left. If I can’t point to the change yet, I keep working until I can."),
    ("Service", "I get real satisfaction from making someone else’s day easier, whether that’s a store manager, a teammate, or a customer at the counter. Most of what I’m proud of comes down to someone leaving better than they arrived."),
    ("Purpose", "I want to be part of something bigger than my own to-do list. The best jobs I’ve had were ones where I believed in what the place was trying to be."),
]

VALUES = [
    ("1", "Self-direction", "I do my best work with clear expectations and the room to work out how to meet them. Give me the goal and I’ll come back with a plan."),
    ("2", "Benevolence", "Caring about the people right in front of me: the team, the store manager, the regular at the counter."),
    ("3", "Universalism", "Wanting things to be fair and good beyond my own circle, not just inside it."),
    ("4", "Stimulation", "I’m at my best with variety and a new problem to solve. When a process is running smoothly, I start looking for what could run better."),
]

SKILLS = [
    ("Analytics & systems", "Excel modeling and reporting · Route optimization · Territory mapping · Visit tracking and data reconciliation · Salesforce CRM · POS and SaaS platforms"),
    ("Sales & business development", "Territory management · B2B and B2C sales · Consultative selling · Pipeline management · Cold and referral outreach · Account relationships"),
    ("Retail & merchandising", "Planogram compliance · Visual display · POS placement · Display schematics · Product mix and store layout · Product promotion"),
    ("Leadership & training", "Hiring and coaching · Training program design · Cross-functional collaboration · Team culture"),
    ("Operations", "Inventory and cost control · Scheduling · Front- and back-of-house management · Vendor coordination · Microsoft Office · Adobe Creative Suite"),
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
    "jobTitle": "Retail Merchandising Associate",
    "worksFor": {"@type": "Organization", "name": "Altria Group Distribution Company"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Washington College"},
    "address": {"@type": "PostalAddress", "addressLocality": "Baltimore", "addressRegion": "MD", "addressCountry": "US"},
    "description": "Field operations, sales and analytics professional in Baltimore, MD. Builds data tools for retail field work, including StoreTracker, an iPhone app that logs store visits automatically.",
    "knowsAbout": ["Retail field operations", "Merchandising", "Route optimization", "Sales", "Data analytics", "Salesforce", "Swift", "Specialty coffee"],
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
    return head("Conor Maloney — Field Operations, Sales & Analytics | Baltimore, MD",
                "Conor Maloney is a Baltimore-based field operations, sales and analytics professional who uses retail data to see what's working and builds tools, like the StoreTracker iPhone app, that make field work run better.",
                "/", home_ld(), "profile") + header("Home") + f"""
<div class="wrap hero">
  <div class="hero-text">
    <div class="eyebrow">Field operations · Sales · Analytics</div>
    <div class="stack" style="gap:20px">
      <h1>Conor Maloney</h1>
      <div class="tagline"><span>Composed Systems</span></div>
    </div>
    <p class="hero-intro">Years in retail field operations taught me how marketing plays out in the store. I use data to understand what's working and build tools that make the work run better.</p>
    <div class="actions">
      <a class="btn" href="/experience/">Experience</a>
      <a class="btn-outline" href="/about/">About me</a>
      <a class="arrow-link" href="/contact/">Get in touch →</a>
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

<section class="wrap section section-last feature" aria-labelledby="storetracker">
  <div class="feature-text">
    <div class="eyebrow accent">Example · A tool I built for my own route</div>
    <h2 id="storetracker">StoreTracker</h2>
    <p class="body" style="font-size:17px">Geofencing logs every arrival, departure and minute on site across the territory, then syncs each visit to Google Sheets for analysis. No manual entry, no duplicate rows, about 200 automated tests.</p>
    <ul class="tags"><li>Swift</li><li>Core Location</li><li>Apps Script</li><li>TypeScript</li></ul>
    <a class="arrow-link" href="/work/storetracker/" style="margin-top:8px">See how I built it →</a>
  </div>
  <a class="stage stage-home" href="/work/storetracker/" aria-label="Read the StoreTracker case study">
    {phone("ledger", "StoreTracker visits ledger screen")}
    {phone("board", "StoreTracker visits board with a live in-store timer", "mid")}
    {phone("stats", "StoreTracker weekly stats screen")}
  </a>
</section>

<section class="wrap section-last split" aria-labelledby="history">
  <div class="label wide" style="gap:16px">
    <h2 id="history" class="h2-lg">Where the experience comes from</h2>
    <a class="arrow-link" href="/experience/" style="font-size:15px">Full work history →</a>
  </div>
  <ul class="plain roles-brief ruled ruled-end">{roles}</ul>
</section>
""" + footer()

def page_work():
    views = "".join(f'<figure><div class="shot">{phone(k, f"StoreTracker {t} screen")}</div><figcaption><h3>{e(t)}</h3><p>{e(d)}</p></figcaption></figure>' for k, t, d in VIEWS)
    parts = "".join(f'<li><span class="n">{n}</span><div><h3>{e(t)}</h3><p class="body">{e(d)}</p></div></li>' for n, t, d in PARTS)
    probs = "".join(f'<li><h3>{e(t)}</h3><p class="body">{e(d)}</p></li>' for t, d in PROBLEMS)
    path = "/work/storetracker/"
    ld = page_ld(path, "StoreTracker case study", "Article", {
        "headline": "StoreTracker: an iPhone app that logs every store visit automatically",
        "description": "Case study: a native iPhone app built by Conor Maloney that uses geofencing to log arrivals, departures and time on site across a 528-store retail territory, syncing each visit to Google Sheets.",
        "image": SITE + "/assets/img/og.jpg", "datePublished": "2026-08-31", "dateModified": LASTMOD, "inLanguage": "en",
    })
    return head("StoreTracker: An iPhone App That Logs Store Visits Automatically — Conor Maloney",
                "Case study: how Conor Maloney designed and built StoreTracker, a Swift iPhone app that uses geofencing to log arrivals, departures and time on site across 528 stores, syncing every visit to Google Sheets.",
                path, ld, "article") + header("Work") + f"""
<article>
<div class="wrap page-head" style="padding-bottom:56px">
  <div class="eyebrow accent">Case study · July–August 2026</div>
  <h1 class="display">StoreTracker</h1>
  <p class="serif" style="font-size:clamp(22px,2.4vw,30px);line-height:1.3;color:var(--ink-2);max-width:760px;text-wrap:pretty">A native iPhone app that logs every store visit on its own, so the numbers that measure my workday are finally accurate.</p>
</div>
<div class="wrap">
  <dl class="facts">
    <div><dt>Role</dt><dd>Designer, developer and sole user</dd></div>
    <div><dt>Scale</dt><dd>528 stores · ~200 automated tests · 3 connected components</dd></div>
    <div><dt>Built with</dt><dd>Swift, SwiftUI, Core Location, Core Data, Google Apps Script, TypeScript</dd></div>
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
    <p class="body-lg">I cover a retail territory of more than 500 stores across Maryland. In field work, time on site is one of the main ways performance gets measured, but nothing recorded it accurately. Logging by hand meant stopping at every store, rounding times, and hoping I didn't miss one. The data that described my own workday was the least reliable data I had.</p>
    <p class="pull">I didn't want a better way to log visits by hand. I wanted a record that kept itself.</p>
  </div>
</section>

<section class="wrap section">
  <div class="split">
    <div class="label"><span class="num">02</span><h2 class="h2">What I built</h2></div>
    <div class="content">
      <p class="body-lg">The app runs in the background all day. When I walk into one of my stores it records the arrival; when I leave it records the departure and the time on site. Each visit syncs to a Google Sheet where I can analyze it. I never have to tap anything. The app presents the data four ways.</p>
    </div>
  </div>
  <div class="views">{views}</div>
</section>

<section class="wrap section split">
  <div class="label"><span class="num">03</span><h2 class="h2">How I built it</h2></div>
  <div class="content" style="gap:0">
    <p class="body-lg" style="margin-bottom:24px">Three parts, each with a single job.</p>
    <ol class="plain parts ruled">{parts}</ol>
    <p class="note">I wrote a design spec for each feature before building it. I developed with AI coding tools, making the architecture decisions and directing and testing each piece myself.</p>
  </div>
</section>

<section class="wrap section stack" style="gap:40px">
  <div class="stack" style="gap:8px"><span class="num">04</span><h2 class="h2">The hard problems</h2></div>
  <ul class="plain problems">{probs}</ul>
</section>

<section class="wrap section section-last split">
  <div class="label"><span class="num">05</span><h2 class="h2">The result</h2></div>
  <div class="content" style="max-width:760px">
    <p class="result">An automatic, minute-by-minute record of my workday across the whole territory, in a spreadsheet I can analyze.</p>
    <a class="arrow-link" href="/experience/">See the full work history →</a>
  </div>
</section>
</article>
""" + footer()

def page_experience():
    roles = ""
    for period, co, role, loc, desc in ROLES:
        d = f'<p class="body">{e(desc)}</p>' if desc else ""
        roles += f'<li class="role"><div class="period">{e(period)}</div><div class="who"><h2>{e(co)}</h2><div class="title">{e(role)}</div><div class="loc">{e(loc)}</div></div><div class="desc">{d}</div></li>'
    path = "/experience/"
    return head("Experience — Conor Maloney",
                "Conor Maloney's work history since 2015: retail merchandising at Altria, field sales at Shift4 and BDS Connected Solutions, and cafe and beverage management in Baltimore and Chestertown, MD.",
                path, page_ld(path, "Experience — Conor Maloney", "ProfilePage", {"mainEntity": {"@id": PERSON_ID}})) + header("Experience") + f"""
<div class="wrap page-head" style="gap:24px;padding-bottom:64px">
  <div class="eyebrow">Experience · 2015 – present</div>
  <h1 class="display balance" style="font-size:clamp(48px,7vw,88px);line-height:1;max-width:900px">Sales, merchandising and hospitality, measured.</h1>
  <p class="body-lg" style="font-size:19px;line-height:1.55;max-width:640px">Every role taught me to read a different kind of customer data: store execution, sales pipelines, menu performance. Here's the full history.</p>
</div>
<div class="wrap section-last"><ol class="plain">{roles}</ol></div>
""" + footer()

def page_about():
    skills = "".join(f'<li><h3 class="kicker">{e(g)}</h3><p>{e(i)}</p></li>' for g, i in SKILLS)
    path = "/about/"
    return head("About Conor Maloney — A Structured Creative",
                "About Conor Maloney: Washington College music and theatre graduate, industrial electronic musician (HARDWEAR), and retail field professional covering roughly 570 stores across Maryland who builds his own tools.",
                path, page_ld(path, "About Conor Maloney", "AboutPage", {"mainEntity": {"@id": PERSON_ID}})) + header("About") + f"""
<div class="wrap about section-last">
  <div class="about-text">
    <div class="eyebrow">About</div>
    <h1 class="display" style="font-size:clamp(52px,7vw,88px);line-height:1">Hi, I'm Conor.</h1>
    <p class="lede-serif" style="max-width:680px">I'm a structured creative. I'm happiest where imagination meets a real problem that needs solving: organizing a messy system, designing a better way to work, or shaping raw ideas into something people can use and feel.</p>
    <div class="stack" style="gap:20px;max-width:640px">
      <p class="body-lg">My background doesn't follow a straight line, and I've come to see that as the point. I studied music and theatre at Washington College, and I still create: I produce industrial electronic music under the name HARDWEAR. I've also spent years in hospitality, merchant services, and retail. I now work as a retail merchandising associate covering a territory of roughly 570 stores across Maryland.</p>
      <p class="body-lg">That field work taught me how much good systems matter. Planning visits across hundreds of locations isn't glamorous, but it's a real design problem, so I treated it as one. I built <a class="inline-link" href="/work/storetracker/">StoreTracker</a>, my own app for tracking store visits, and I've spent a lot of time working out how to route and sequence a territory more efficiently. Nobody asked me to do either. I did them because I saw a better way and wanted to build it.</p>
      <p class="body-lg">That's the pattern in everything I do. I notice things other people tend to overlook: how people actually move through a space, what makes a display land, where a process quietly wastes time. Then I try to make it better, whether the medium is a spreadsheet, a café counter, a piece of software, or a song.</p>
    </div>
    <a class="arrow-link" href="/what-drives-me/">What drives me →</a>
  </div>
  <aside class="about-side">
    <picture><source srcset="{IMG}conor-maloney.webp" type="image/webp"><img src="{IMG}conor-maloney.jpg" alt="Portrait of Conor Maloney" width="800" height="800"></picture>
    <div class="skills">
      <h2>Core competencies</h2>
      <ul class="plain">{skills}</ul>
    </div>
  </aside>
</div>
""" + footer()

def page_drives():
    mot = "".join(f'<li><h3 class="kicker" style="letter-spacing:.16em">{e(t)}</h3><p class="body">{e(d)}</p></li>' for t, d in MOTIVATORS)
    val = "".join(f'<li><span class="n">{n}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for n, t, d in VALUES)
    path = "/what-drives-me/"
    return head("What Drives Me — Conor Maloney",
                "What motivates Conor Maloney, the values he ranks highest, and how he works best: a structured creative who builds ideas into systems that last.",
                path, page_ld(path, "What Drives Me — Conor Maloney")) + header("What Drives Me") + f"""
<div class="wrap page-head">
  <div class="eyebrow">Motivation · Values · Work style</div>
  <h1 class="display">What Drives Me</h1>
  <p class="lede-serif" style="max-width:760px">I’ve spent a decade in work that puts me in front of people: behind an espresso bar, on a sales floor, in the back of a 7 Eleven fixing a planogram. What I’ve learned is that I do my best work when it means something, when I’m trusted to find the best way to get there, and when the people around me are better off for it. This is the short version of what motivates me.</p>
</div>

<section class="wrap stack" style="padding-top:clamp(64px,8vw,96px);gap:32px">
  <div class="stack" style="gap:8px"><span class="num">01</span><h2 class="h2">What Motivates Me</h2></div>
  <ul class="plain motivators">{mot}</ul>
</section>

<section class="wrap section stack" style="gap:32px">
  <div class="stack" style="gap:8px">
    <span class="num">02</span><h2 class="h2">What I Value</h2>
    <p style="font-size:16px;color:var(--muted)">My core values, in the order I’d rank them.</p>
  </div>
  <ol class="plain values ruled-end">{val}</ol>
</section>

<section class="wrap section section-last split">
  <div class="label wide"><span class="num">03</span><h2 class="h2">How I Work Best</h2></div>
  <div class="content" style="flex:2 1 520px;gap:20px">
    <p class="lede-serif">I think of myself as a structured creative. I don’t just want to make something new, I want to build it into a system that holds up when I’m not there: a training program, a route model, a seasonal menu that becomes a permanent one.</p>
    <p class="body-lg">I do my most focused thinking in a quiet space, and I bring that preparation into every store visit and client conversation. I work well with managers who set clear expectations and give me room to meet them, and I make a point of keeping them informed along the way.</p>
    <p class="body-lg">I’m energized by putting original ideas into practice, and I’ve learned to build them inside the systems and standards a business already runs on. That’s how an idea becomes something that lasts after I’ve moved on to the next problem.</p>
    <p style="margin-top:12px;padding-top:24px;border-top:1px solid var(--line);font-size:18px;line-height:1.6">If that sounds like the kind of person you want on your team, the <a class="inline-link" href="/experience/">Work Experience page</a> has the specifics.</p>
  </div>
</section>
""" + footer()

def page_contact():
    profiles = "".join(f'<li><a href="{u}" rel="me noopener" target="_blank">{n} ↗</a></li>' for n, u in LINKS)
    path = "/contact/"
    return head("Contact Conor Maloney",
                "Get in touch with Conor Maloney about marketing and analytics roles where field experience is an advantage. Based in Baltimore, MD and Washington, DC.",
                path, page_ld(path, "Contact Conor Maloney", "ContactPage", {"mainEntity": {"@id": PERSON_ID}})) + header("Contact") + f"""
<div class="wrap contact">
  <div class="eyebrow">Contact</div>
  <h1 class="display">Let's talk.</h1>
  <p style="font-size:clamp(18px,1.8vw,22px);line-height:1.5;color:var(--ink-2);max-width:620px;text-wrap:pretty">I'm interested in marketing and analytics roles where field experience is an advantage. Email is the best way to reach me.</p>
  <a class="big-mail" href="mailto:{EMAIL}">{EMAIL} ↗</a>
  <ul class="elsewhere">{profiles}</ul>
  <div style="font-size:15px;color:var(--muted)">Baltimore, MD — Washington, DC</div>
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
  <div class="actions"><a class="btn" href="/">Go to the homepage</a><a class="arrow-link" href="/work/storetracker/">Read the StoreTracker case study →</a></div>
</div>
""" + footer()

PAGES = [("/", page_home, "1.0"), ("/work/storetracker/", page_work, "0.9"), ("/experience/", page_experience, "0.8"),
         ("/about/", page_about, "0.8"), ("/what-drives-me/", page_drives, "0.6"), ("/contact/", page_contact, "0.6")]

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
