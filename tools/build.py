#!/usr/bin/env python3
"""Generates the subpages and keeps the shared nav/footer in sync.

Run from the repo root:  python3 tools/build.py
- Writes residential.html, shower-doors.html, ... contact.html
- Rewrites the <!--nav--> and <!--footer--> blocks inside index.html
The logo sprite is copied from index.html so it only lives in one place.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

def u(pid, w=1600):
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&q=80"

PHONE = "360-456-0668"
TEL = "tel:3604560668"
MAPS = "https://www.google.com/maps/search/?api=1&query=1206+Franz+St+SE+Lacey+WA+98503"

# slug, menu title, small label, image id, estimate type
SERVICES = [
    ("residential",  "Windows &amp; entry doors", "Residential", "1766603636700-e9d80473f40f", "windows"),
    ("shower-doors", "Custom shower doors",       "Bath",        "1771929662486-f793e08f0f16", "shower"),
    ("commercial",   "Storefronts &amp; commercial", "Commercial", "1525119488448-d549af0dc221", "storefront"),
    ("skylights",    "Skylights",                 "Residential", "1780845591192-eaaef4ddc68f", "skylight"),
    ("specialty",    "Mirrors &amp; specialty",   "Specialty",   "1619378396304-7ef156537d7e", "mirror"),
    ("rv-auto",      "RV &amp; auto glass",       "Auto &amp; RV", "1770752575355-a9d90d5644bb", "rv"),
]
SVC = {s[0]: s for s in SERVICES}

LOGO_INNER = ('<rect class="pane-tint" x="9.6" y="0.8" width="74" height="58" fill="url(#paneGrad)"/>'
              '<g clip-path="url(#paneClip)"><rect class="glint" x="-40" y="-10" width="22" height="80" fill="url(#glintGrad)"/></g>'
              '<use href="#dk-art"/>')

# ------------------------------------------------------------------ shared chrome
def nav(current="", estimate_href="contact.html"):
    def cls(key):
        return ' class="current"' if current == key else ""
    drop = "".join(
        f'<a href="{s}.html"><img src="{u(img,200)}" alt=""><span><b>{t}</b><small>{lbl}</small></span></a>'
        for s, t, lbl, img, _ in SERVICES)
    mm = "".join(
        f'<a href="{s}.html"><img src="{u(img,500)}" alt="">{t}</a>' for s, t, lbl, img, _ in SERVICES)
    return f'''<!--nav-->
<nav class="nav" id="nav">
  <a href="./" class="logo" aria-label="D.K. Boos Glass home"><svg class="brand-logo" viewBox="0 0 303.54 84" role="img" aria-label="D.K. Boos Glass">{LOGO_INNER}</svg><span class="logo-est">Est.<br>1978</span></a>
  <div class="nav-links">
    <div class="has-drop"><button type="button" aria-expanded="false"{' class="current"' if current in SVC else ''}>Services <span class="chev">▾</span></button><div class="drop">{drop}</div></div>
    <a href="./#lab">Glass Lab</a>
    <a href="about.html"{cls("about")}>About</a>
    <a href="faq.html"{cls("faq")}>FAQ</a>
    <a href="contact.html"{cls("contact")}>Contact</a>
  </div>
  <div class="nav-cta">
    <a class="nav-phone" href="{TEL}">360·456·0668</a>
    <a class="btn btn-primary" href="{estimate_href}"><span class="long">Free estimate</span><span class="short">Estimate</span></a>
    <button class="menu-btn" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobileMenu"><i></i><i></i></button>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <div class="mm-label">Services</div>
  <div class="mm-services">{mm}</div>
  <div class="mm-links">
    <a href="./">Home <span>→</span></a>
    <a href="./#lab">Glass Lab <span>→</span></a>
    <a href="about.html">About us <span>→</span></a>
    <a href="faq.html">FAQ <span>→</span></a>
    <a href="contact.html">Contact <span>→</span></a>
  </div>
  <div class="mm-foot">
    <a class="btn btn-primary" href="{estimate_href}">Book a free estimate <span class="arrow">→</span></a>
    <a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a>
  </div>
</div>
<!--/nav-->'''

def footer():
    svc = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t, *_ in SERVICES)
    return f'''<!--footer-->
<footer>
  <div class="wrap">
    <div class="foot-big">Clear <em>since</em><br>1978.</div>
    <div class="foot-grid">
      <div><svg class="brand-logo foot-logo" viewBox="0 0 303.54 109.54" role="img" aria-label="D.K. Boos Glass">{LOGO_INNER}</svg><p style="margin-top:16px;max-width:24em">Residential, commercial, specialty and RV glass for the South Sound. Family-owned and operated.</p></div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Company</h4><ul><li><a href="about.html">Our story</a></li><li><a href="about.html#reviews">Reviews</a></li><li><a href="faq.html">FAQ</a></li><li><a href="./#lab">Glass Lab</a></li><li><a href="contact.html">Contact</a></li></ul></div>
      <div><h4>Visit</h4><ul><li>1206 Franz St SE</li><li>Lacey, WA 98503</li><li><a href="{TEL}">{PHONE}</a></li><li>Mon–Fri 8–5</li></ul></div>
    </div>
    <div class="legal"><span>© 2026 D.K. Boos Glass Inc.</span><span>Unofficial concept redesign, not the official D.K. Boos Glass website · Photos via Unsplash</span></div>
  </div>
</footer>
<!--/footer-->'''

def page(title, desc, body, current=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} · D.K. Boos Glass (Concept)</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<!--SPRITE-->

{nav(current)}

{body}

{footer()}
<script src="assets/site.js"></script>
</body>
</html>
'''

# ------------------------------------------------------------------ building blocks
def hero(img, crumbs, eyebrow, h1, lead, glance=None, actions=None, short=False):
    crumb_html = '<a href="./">Home</a>' + "".join(
        f'<span>/</span>{f"<a href={chr(34)}{h}{chr(34)}>{t}</a>" if h else f"<span>{t}</span>"}' for t, h in crumbs)
    acts = actions if actions is not None else ""
    aside = ""
    if glance:
        rows = "".join(f"<li><span>{k}</span><b>{v}</b></li>" for k, v in glance)
        aside = f'<aside class="pane reveal"><ul class="glance">{rows}</ul></aside>'
    return f'''<header class="page-hero{' short' if short else ''}">
  <div class="hero-img" style="background-image:url('{u(img,2400)}')"></div>
  <div class="wrap hero-inner">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb">{crumb_html}</nav>
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {acts}
    </div>
    {aside}
  </div>
</header>'''

def sec_head(eyebrow, h2, p=""):
    return f'''<div class="sec-head reveal"><div><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2></div>{f"<p>{p}</p>" if p else ""}</div>'''

def offers(items):
    cards = "".join(
        f'<article class="offer reveal"><span class="k">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></article>'
        for i, (t, d) in enumerate(items))
    return f'<div class="offer-grid">{cards}</div>'

def split(img, alt, eyebrow, h2, paras, checks=(), flip=False, cap=None):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    cl = ""
    if checks:
        cl = '<ul class="checks">' + "".join(f"<li><div><b>{b}</b><span>{s}</span></div></li>" for b, s in checks) + "</ul>"
    capt = f'<div class="pane"><b>{cap[0]}</b><span>{cap[1]}</span></div>' if cap else ""
    return f'''<div class="wrap split{' flip' if flip else ''}">
  <div class="split-img reveal"><img src="{u(img,1200)}" alt="{alt}" loading="lazy">{capt}</div>
  <div class="reveal"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{ps}{cl}</div>
</div>'''

def faq_list(items):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in items) + "</div>"

def related(slugs):
    tiles = ""
    for s in slugs:
        _, t, lbl, img, _ = SVC[s]
        tiles += f'''<a class="tile reveal" href="{s}.html"><img src="{u(img,900)}" alt="" loading="lazy"><span class="num">{lbl.upper()}</span><span class="go">→</span><div class="tile-body"><h3>{t}</h3></div></a>'''
    return f'<div class="related">{tiles}</div>'

def cta(h2="Ready when <em>you</em> are.", p="Free on-site measure and an honest quote. Usually back to you within one business day.", type_=""):
    href = "contact.html" + (f"?type={type_}" if type_ else "")
    return f'''<section class="cta-sec"><div class="wrap"><div class="cta-band reveal">
  <div><span class="eyebrow">Free estimate</span><h2 style="margin-top:14px">{h2}</h2><p>{p}</p></div>
  <div class="acts"><a class="btn btn-primary" href="{href}">Book an estimate <span class="arrow">→</span></a><a class="btn btn-ghost" href="{TEL}">{PHONE}</a></div>
</div></div></section>'''

def std_actions(type_):
    return (f'<div class="hero-actions"><a class="btn btn-primary" href="contact.html?type={type_}">Get a free estimate <span class="arrow">→</span></a>'
            f'<a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a></div>')

def brands(items):
    return '<div class="brands reveal">' + "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in items) + "</div>"

def service_page(slug, num, title, desc, hero_img, h1, lead, glance, offer_head, offer_items,
                 split_args, extra="", faqs=(), rel=()):
    _, name, lbl, _, type_ = SVC[slug]
    body = hero(hero_img, [("Services", "./#services"), (name, None)], f"{num} / {lbl}", h1, lead, glance, std_actions(type_))
    body += f'\n<section><div class="wrap">{sec_head(*offer_head)}{offers(offer_items)}</div></section>'
    body += f'\n<section class="tint">{split(**split_args)}</section>'
    body += extra
    if faqs:
        body += f'\n<section><div class="wrap">{sec_head("Good questions", "Asked <em>often.</em>", "Something else on your mind? Call the shop. A real person picks up.")}{faq_list(faqs)}</div></section>'
    body += f'\n<section style="padding-top:0"><div class="wrap">{sec_head("Keep exploring", "More from <em>the shop.</em>")}{related(rel)}</div></section>'
    body += "\n" + cta(type_=type_)
    return page(title, desc, body, slug)

# ------------------------------------------------------------------ pages
PAGES = {}

PAGES["residential"] = service_page(
    "residential", "01", "Windows & Entry Doors",
    "Replacement windows and entry doors for South Sound homes, from Marvin, Simonton, Ply Gem and Marlin.",
    "1761013320045-d29e4f10bcbc",
    "Windows that <em>fit</em><br>the house.",
    "Replacement windows, entry doors and the glass inside them, measured and installed by our own crew across Thurston and Pierce County.",
    [("Brands", "Marvin · Simonton · Ply Gem · Marlin"), ("Estimate", "Free, at your home"), ("Installers", "Full-time, in-house"), ("Since", "1978")],
    ("What we do", "Everything that<br>opens, <em>seals</em> or lets light in.",
     "From one cracked pane to a whole-house replacement, it's the same crew from first measure to final caulk line."),
    [("Replacement windows", "Vinyl, fiberglass and wood-clad windows from Marvin, Simonton, Ply Gem and Marlin, sized to your existing openings."),
     ("Entry doors", "Custom entry doors with decorative, textured or privacy glass that make the front of the house feel finished."),
     ("Insulated glass", "Foggy double-pane? A failed seal can often be fixed by replacing just the glass unit, not the whole window."),
     ("Storm windows", "An extra layer for older or historic windows that cuts drafts and noise without changing the look."),
     ("Window leak repair", "We track down where the water is actually getting in, then fix the seal, flashing or glazing at the source."),
     ("Pet doors", "Pet doors installed right into glass panels, sliders, doors or walls, cut clean and sealed tight.")],
    dict(img="1572739275114-ec3764ba1477", alt="White framed window with soft daylight", eyebrow="Why replace",
         h2="New windows pay you <em>back.</em>",
         paras=["Old windows quietly cost you every month. New ones look better from the curb and work better from the inside."],
         checks=[("Lower energy bills", "Modern insulated glass keeps conditioned air where you paid for it."),
                 ("More curb appeal", "One of the most visible upgrades you can make to a home's value."),
                 ("They just work", "No sticking, no squeaking, no fighting the latch in January."),
                 ("Easier to clean", "Tilt-in sashes and modern designs make the outside panes reachable.")],
         cap=("Measured on-site", "Every quote starts with a tape measure, not a guess.")),
    extra=f'\n<section><div class="wrap">{sec_head("Brands we install", "Built by the <em>best,</em><br>installed by us.")}{brands([("Marvin","Wood &amp; fiberglass"),("Simonton","Vinyl windows"),("Ply Gem","Vinyl &amp; clad"),("Marlin","Vinyl windows")])}</div></section>',
    faqs=[("Why should I replace my windows?", "Better energy efficiency and lower utility bills, a big lift in curb appeal, and windows that open, close and clean easily again. If yours are drafty, foggy or hard to operate, it's worth a look."),
          ("When do I need a new entry door?", "Drafts around the frame, a door that sticks or won't latch, visible rot or warping, or simply a front entry that doesn't match the house anymore. We'll tell you honestly whether repair or replacement makes more sense."),
          ("Can you fix a foggy window without replacing it?", "Often, yes. Fog between panes means the seal on the insulated glass unit has failed. We can usually replace just that glass unit and keep your existing frame.")],
    rel=["skylights", "shower-doors", "specialty"])

PAGES["shower-doors"] = service_page(
    "shower-doors", "02", "Custom Shower Doors",
    "Frameless and custom shower doors designed and installed in Olympia, Lacey and the South Sound.",
    "1771929662486-f793e08f0f16",
    "A shower that feels<br><em>custom.</em> Because it is.",
    "Frameless and semi-frameless shower glass, designed around your bathroom's exact layout and installed with precision.",
    [("Style", "Frameless · Semi-frameless · Sliding"), ("Fit", "Measured to your walls"), ("Glass", "Tempered safety glass"), ("Estimate", "Free, at your home")],
    ("Options", "Pick the look.<br>We'll make it <em>fit.</em>",
     "Walls are never perfectly square. That's exactly why a custom door beats one off the shelf."),
    [("Frameless enclosures", "Heavy tempered glass with minimal hardware for the clean, open, spa look."),
     ("Semi-frameless", "A slim frame for a crisp line at a friendlier price point."),
     ("Sliding &amp; bypass", "Space-saving panels for tub surrounds and tight bathrooms."),
     ("Splash panels", "A single fixed panel for walk-in showers with nothing to swing or slide."),
     ("Glass choices", "Clear, low-iron for extra clarity, frosted, or rain and reeded textures for privacy."),
     ("Hardware finishes", "Chrome, brushed nickel, matte black or brass, matched to your fixtures.")],
    dict(img="1706670359282-e5182f748973", alt="Bathroom with a glass shower door", eyebrow="Why custom",
         h2="Builder-grade to <em>custom-grade.</em>",
         paras=["A custom glass shower door is one of the few remodel upgrades you notice every single day, and buyers notice it too."],
         checks=[("Bespoke design", "Tailored to your layout and dimensions so it looks built-in, not added-on."),
                 ("Quality materials", "Thick tempered glass and solid hardware that holds up for years."),
                 ("Precision install", "Level, plumb and sealed, even when the tile work isn't perfectly square."),
                 ("Adds value", "A real return when it's time to sell.")],
         flip=True),
    faqs=[("How long does a custom shower door take?", "It's made to order, so it starts with an on-site measure once your tile is finished. We'll give you a clear timeline at that visit."),
          ("Can you install on an existing tub?", "Yes. Sliding, bypass and fixed-panel options all work on standard tubs."),
          ("Is frameless glass safe?", "Shower glass is tempered safety glass, built to be strong and to break safely if it ever does.")],
    rel=["residential", "specialty", "skylights"])

PAGES["commercial"] = service_page(
    "commercial", "03", "Storefronts & Commercial Glass",
    "Commercial storefronts, Kawneer systems, door closers, drive-thru windows and security glass in the South Sound.",
    "1525119488448-d549af0dc221",
    "Storefronts that<br>make an <em>entrance.</em>",
    "From service calls to large commercial projects, we work directly with owners, general contractors and architects, and we keep disruption to your business low.",
    [("Systems", "Kawneer storefront &amp; entrances"), ("Work with", "Owners · GCs · Architects"), ("Security", "Bullet &amp; blast resistant"), ("Service", "Repair, replace, install")],
    ("Commercial services", "Built for <em>traffic.</em><br>Serviced for life.",
     "We select the glass or storefront system that fits your budget and your design objectives, then keep it working."),
    [("Storefront systems", "Ultra-modern to classic, with quality materials that make a first impression and last for years."),
     ("Kawneer windows &amp; entrances", "Commercial-grade framing systems trusted by architects for performance and clean lines."),
     ("Door closers", "Sales and service for closers of every kind, including fire doors that must stay shut."),
     ("Hollow metal doors", "Stronger and longer-lasting than standard doors when security and durability matter."),
     ("Drive-thru windows", "Sliding service windows built for all-day use and Northwest weather."),
     ("Repair &amp; replacement", "Broken storefront glass, failed seals and damaged windows, fixed fast so you can open.")],
    dict(img="1497366754035-f200968a6e72", alt="Hallway lined with glass-panel doors", eyebrow="How we work",
         h2="We work around <em>your</em> hours.",
         paras=["Commercial glass is about more than glass. It's scheduling, access, safety and keeping your doors open while we work.",
                "We coordinate with your team or your GC so the job fits your business, not the other way around."],
         checks=[("One point of contact", "Straight answers from people who know the job."),
                 ("Spec-ready", "We help architects and GCs land on the right system for the budget."),
                 ("Service after install", "Closers, hinges and hardware maintained for the life of the building.")],
         cap=("Spec to service", "Selection, install and upkeep under one roof.")),
    extra='\n<section class="dark">' + split(
        "1784297870044-a7e4d5abd769", "Modern glass building reflecting the sky", "Security glass",
        "Bullet &amp; blast <em>resistant.</em>",
        ["Cameras watch, but they can't stop anyone. Security glass keeps your property and people safe without giving up the view."],
        [("Protection from debris", "Takes a pummeling from storms and falling branches without shattering."),
         ("Stops stray rounds", "Rated glass deflects bullets to keep people safe."),
         ("Slows forced entry", "Withstands repeated hits from heavy tools.")], flip=True) + "</section>",
    faqs=[("Do you work with general contractors and architects?", "Yes, all the time. We can help select a glass or storefront system to meet the design and the budget, then install it."),
          ("Do you service existing door closers?", "Yes. We sell, install and service door closers, including fire-rated doors that need to close reliably."),
          ("Can you do emergency storefront repairs?", "Call the shop. We'll get you secured and back open as fast as possible.")],
    rel=["rv-auto", "specialty", "residential"])

PAGES["skylights"] = service_page(
    "skylights", "04", "Skylights",
    "Velux and Crystalite skylights installed and replaced in Olympia, WA and the South Sound.",
    "1780845591192-eaaef4ddc68f",
    "Bring the sky<br><em>inside.</em>",
    "Premium Velux and Crystalite skylights that fill a room with daylight, add fresh air, and make the whole house feel bigger.",
    [("Brands", "Velux · Crystalite"), ("Types", "Fixed · Venting · Tunnels"), ("Best for", "Kitchens, baths, halls"), ("Estimate", "Free, at your home")],
    ("Options", "Light, air or <em>both.</em>",
     "Whether you want a bright kitchen or a bathroom that finally airs out, there's a skylight for the job."),
    [("Fixed skylights", "Pure daylight for living rooms, stairwells and any space that feels dim."),
     ("Venting skylights", "Open them up to let steam and heat escape. Ideal for bathrooms and kitchens."),
     ("Solar &amp; remote", "Solar-powered venting models open with a remote and can close themselves when it rains."),
     ("Sun tunnels", "Tubular skylights that bring daylight into closets and hallways where a full skylight won't fit."),
     ("Replacement", "Old, cloudy or leaking skylights swapped for modern, energy-efficient units."),
     ("Leak diagnosis", "Drips around a skylight? We find out whether it's the unit, the flashing, or the roof around it.")],
    dict(img="1774762720332-502f67f047ab", alt="Daylight from above casting geometric patterns", eyebrow="Why skylights",
         h2="Daylight changes <em>everything.</em>",
         paras=["A skylight is more than a window in the roof. It's a design feature that warms up the whole room."],
         checks=[("Natural daylight", "Brightens dull spaces and makes rooms feel more welcoming."),
                 ("A sense of openness", "Kitchens, baths, hallways and living rooms feel bigger."),
                 ("Fresh air", "Venting models move steam and stale air out."),
                 ("Lower lighting costs", "Less need for lights during the day.")],
         flip=True),
    extra=f'\n<section><div class="wrap">{sec_head("Brands we install", "Two names we <em>trust.</em>")}{brands([("Velux","Fixed, venting &amp; sun tunnels"),("Crystalite","Custom &amp; structural skylights")])}</div></section>',
    faqs=[("Will a skylight leak?", "A properly flashed, properly installed skylight shouldn't. Most leaks we see come from old flashing or installs that cut corners."),
          ("Can you replace my old skylight?", "Yes. We replace cloudy, cracked and leaking skylights with modern Velux and Crystalite units.")],
    rel=["residential", "shower-doors", "specialty"])

PAGES["specialty"] = service_page(
    "specialty", "05", "Mirrors & Specialty Glass",
    "Custom mirrors, curved glass, decorative glass, wood stove glass, plexiglass and more in Lacey, WA.",
    "1781249144138-0c63b4d5876e",
    "If it's glass,<br>we can <em>make</em> it.",
    "Glass all looks alike until you need the right kind. With nearly five decades behind us, we can identify and fabricate exactly what your project calls for.",
    [("Mirrors", "Cut to size, any shape"), ("Curved", "Bent glass, custom radius"), ("Heat-rated", "Wood stove glass"), ("Also", "Plexiglass · Tabletops")],
    ("Specialty services", "The odd jobs are our <em>favorite</em> jobs.",
     "Bring us a broken piece, a sketch or an idea. We'll figure out the rest."),
    [("Custom mirrors", "Wall mirrors, gym and dance mirrors, vanity mirrors and anything in between, cut to size and shape."),
     ("Curved glass", "Bent glass for display cases, curved windows and architectural features. Most shops can't do it."),
     ("Decorative glass", "Patterned, textured, etched or frosted glass that adds a little wow to a home or business."),
     ("Wood stove glass", "High-temperature ceramic glass made to handle the heat of a wood stove or fireplace door."),
     ("Tabletops &amp; heavy glass", "Thick glass for tabletops, shelving and heavy-duty uses, with polished edges."),
     ("Plexiglass &amp; shields", "Shatter-resistant acrylic for shields, guards, signs and picture frames.")],
    dict(img="1757837595378-18db712eaa9a", alt="Curved glass reflecting soft shadows", eyebrow="Curved glass",
         h2="Glass that <em>bends</em> the rules.",
         paras=["Curved glass is one of the hardest things in the trade to get right, and one of the few things that makes people stop and look.",
                "We fabricate curved pieces to a custom radius for display cases, architectural details and replacement of hard-to-find originals."],
         checks=[("Custom radius", "Matched to your template or the original."),
                 ("Replacement work", "We can often match curved glass others can't source.")],
         cap=("Made to order", "Fabricated to a template you can trust.")),
    faqs=[("Can you cut a mirror to an unusual shape?", "Yes. Bring a template or measurements and we'll cut, polish and install it."),
          ("Do you sell glass for picture frames?", "Yes, from a single frame to bulk orders."),
          ("What glass goes in a wood stove?", "It needs high-temperature ceramic glass, not regular tempered glass. Bring the old piece or the stove's model and we'll match it.")],
    rel=["shower-doors", "residential", "commercial"])

PAGES["rv-auto"] = service_page(
    "rv-auto", "06", "RV & Auto Glass",
    "RV windshield and window replacement, rock chip repair, trailers and campers. OEM-approved glass with a lifetime warranty.",
    "1781211901352-390b93468b01",
    "Keep the <em>road trip</em><br>on the road.",
    "RV windshields, custom-matched camper windows, trailers and rock chips, done indoors in our Lacey shop with O.E.M.-approved glass.",
    [("Glass", "O.E.M.-approved"), ("Warranty", "Lifetime on installs"), ("Shop", "Large indoor facility"), ("Ship-in", "Out-of-area service")],
    ("What we fix", "Big rigs to <em>little</em> chips.",
     "This isn't a job for just any auto glass shop. It takes the right tools, the right space and the right experience."),
    [("RV windshields", "RV windshield repair and replacement is our specialty, done in a dry indoor bay."),
     ("Replacement windows", "We custom-match all types of RV and camper windows, even ones that are hard to find."),
     ("Foggy windows", "Fog means the insulated glass has failed. We repair it to keep your RV warm and dry."),
     ("Rock chips &amp; cracks", "Small chips repaired before they spread across the windshield."),
     ("Trailers, buses &amp; campers", "Travel trailers, horse trailers, buses and camper replacement windows."),
     ("Aquapel treatment", "Rain-repellent treatment for clearer visibility in Northwest weather.")],
    dict(img="1626680114529-3f6ffa002b80", alt="RV trailer parked on a grassy field", eyebrow="Why bring it here",
         h2="Done indoors.<br>Done <em>right.</em>",
         paras=["The quality of a glass install depends on the installer and on the conditions. That's why every RV job happens inside our shop, where weather can't interfere."],
         checks=[("Large indoor facility", "A dry, controlled bay for windshields and windows."),
                 ("Room to maneuver", "A spacious lot and turnaround make bringing in a big rig easy."),
                 ("Federal safety standards", "Every job is done to spec, so you're secure on the road."),
                 ("Lifetime warranty", "We stand behind O.E.M.-approved glass for as long as you own it.")],
         flip=True),
    extra='\n<section class="dark">' + split(
        "1775641080262-1a4e3978a4b5", "RV driving down a desert highway", "Out-of-area service",
        "Far away? <em>Ship</em> it to us.",
        ["Can't drive it in? Send us your window. We'll repair it or match it and ship it back.",
         "Call our service specialists first and we'll walk you through the best way to pack and ship."],
        [("Custom match", "Long-distance window match and repair."), ("Straight answers", "We'll tell you up front what's possible.")]) + "</section>",
    faqs=[("Do I need to bring my RV in?", "Yes for windshields and most windows. We do the work in our indoor facility so weather can't affect the result, and our lot has plenty of room for big rigs."),
          ("Do you warranty RV glass?", "Yes. We install O.E.M.-approved glass and back the work with a lifetime warranty."),
          ("Can you fix a rock chip?", "Usually, if it's small and caught early. Bring it in before it spreads.")],
    rel=["commercial", "residential", "specialty"])

# ---------------- about
REVIEWS = '''<div class="reviews-row">
      <article class="review feature reveal"><div class="stars">★★★★★</div><q>Incredibly positive experience.</q><div class="who"><span class="avatar">J</span>Julie M. · Window replacement</div></article>
      <article class="review reveal"><div class="stars">★★★★★</div><q>Fantastic experience, start to finish.</q><div class="who"><span class="avatar">R</span>Robert H. · Residential</div></article>
      <article class="review reveal"><div class="stars">★★★★★</div><q>Completely satisfied!</q><div class="who"><span class="avatar">C</span>Christopher T. · Residential</div></article>
    </div>'''

AREA = '''<section class="area" id="area">
  <div class="wrap area-grid">
    <div class="reveal">
      <span class="eyebrow">Service area</span>
      <h2 style="margin-top:18px">Rooted in Lacey.<br>Serving the <em>whole</em> South Sound.</h2>
      <p style="opacity:.7;margin-top:20px;max-width:30em">Thurston and Pierce County, with an even larger area for residential and commercial windows. RV glass ships anywhere.</p>
      <div class="chips"><span class="chip">Olympia</span><span class="chip">Lacey</span><span class="chip">Tumwater</span><span class="chip">DuPont</span><span class="chip">Lakewood</span><span class="chip">South Tacoma</span><span class="chip">Shelton</span><span class="chip">Aberdeen</span><span class="chip">Rochester</span></div>
    </div>
    <div class="map reveal" aria-hidden="true">
      <div class="pin"><i></i><b>Lacey</b><span>1206 Franz St SE</span></div>
      <span class="town" style="top:30%;left:62%">Lakewood</span><span class="town" style="top:18%;left:52%">S. Tacoma</span><span class="town" style="top:38%;left:72%">DuPont</span><span class="town" style="top:56%;left:18%">Olympia</span><span class="town" style="top:66%;left:34%">Tumwater</span><span class="town" style="top:30%;left:12%">Shelton</span><span class="town" style="top:78%;left:24%">Rochester</span><span class="town" style="top:48%;left:-2%">Aberdeen</span>
    </div>
  </div>
</section>'''

about_body = hero("1761798607954-5ca1646afebe", [("About", None)], "Our story",
                  "The <em>D.K.</em><br>stands for family.",
                  "Dennis and Kathy started a hands-on glass shop in the South Sound in 1978. Their son and his wife run it the same way today.",
                  [("Founded", "1978, South Sound"), ("Owned by", "The Boos family"), ("Crew", "Full-time installers"), ("Hours", "Mon–Fri, 8–5")], short=True)
about_body += '''
<section class="story">
  <div class="wrap story-grid">
    <div class="story-img reveal">
      <img src="''' + u("1563693998336-93c10e5d8f91", 1200) + '''" alt="Sunlight through a window casting plant shadows" loading="lazy">
      <div class="badge"><svg viewBox="0 0 130 130"><defs><path id="c" d="M65,65 m-50,0 a50,50 0 1,1 100,0 a50,50 0 1,1 -100,0"/></defs><text fill="rgba(234,244,246,.6)" font-size="9.5" letter-spacing="3" font-family="Inter Tight"><textPath href="#c">FAMILY OWNED · LACEY WA · FAMILY OWNED · LACEY WA ·</textPath></text></svg><div><b>1978</b><span>Est.</span></div></div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Our name</span>
      <h2 style="margin-top:18px">Dennis in the field.<br><em>Kathy</em> in the office.</h2>
      <blockquote>“Who's the D.K. in D.K. Boos? The answer is Dennis and Kathy.”</blockquote>
      <p>Customers have asked for years, so there it is. They both took a hands-on approach, Dennis out on jobs and Kathy running the office.</p>
      <p>Things have changed a little since then. Their son and his wife now run the business, and that hands-on approach hasn't changed at all. Excellent customer service is a tradition that started with Dennis and Kathy and continues to this day.</p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">''' + sec_head("Through the years", "Nearly five decades<br>of <em>clear</em> work.") + '''
    <div class="timeline">
      <div class="tl reveal"><b>1978</b><h3>The shop opens</h3><p>Dennis and Kathy start D.K. Boos Glass with a hands-on, do-it-right approach.</p></div>
      <div class="tl reveal"><b>4</b><h3>Divisions grow</h3><p>Residential, commercial, specialty and RV &amp; auto glass, all under one roof in Lacey.</p></div>
      <div class="tl reveal"><b>2<sup style="font-size:.4em">nd</sup></b><h3>Next generation</h3><p>Their son and his wife take the reins and keep the same standards.</p></div>
      <div class="tl reveal"><b>Today</b><h3>Still hands-on</h3><p>Full-time installers, honest quotes, and the shop the South Sound calls first.</p></div>
    </div>
  </div>
</section>
<section class="dark">
  <div class="wrap">''' + sec_head("What we stand for", "How we <em>do</em> business.", "Our staff is knowledgeable, experienced and happy to walk you through every window and glass option, from colors and patterns to performance.") + '''
    <div class="values">
      <div class="value reveal"><i>◇</i><h3>Hands-on</h3><p>The family is still in the shop and on the phone. Not a call center.</p></div>
      <div class="value reveal"><i>◎</i><h3>Honest quotes</h3><p>Measured on-site, quoted straight, with no pressure.</p></div>
      <div class="value reveal"><i>▢</i><h3>Our own crew</h3><p>Full-time, experienced installers. No subcontractors.</p></div>
      <div class="value reveal"><i>✦</i><h3>We stand behind it</h3><p>If something's not right, we come back and make it right.</p></div>
    </div>
  </div>
</section>
<section id="reviews">
  <div class="wrap">''' + sec_head("Neighbors say", "Word travels<br><em>fast</em> in Lacey.") + REVIEWS + '''
  </div>
</section>
''' + AREA + "\n" + cta()
PAGES["about"] = page("About Us", "The story of D.K. Boos Glass, a family-owned glass shop in Lacey, WA since 1978.", about_body, "about")

# ---------------- faq
FAQ_GROUPS = [
    ("windows", "Windows &amp; doors", [
        ("Why should I replace my windows?", "New windows improve energy efficiency and lower utility bills, boost curb appeal and property value, operate smoothly without sticking or squeaking, and are easier to clean."),
        ("When do I need a new entry door?", "Drafts, sticking, a latch that won't catch, rot, warping, or a door that just doesn't suit the house anymore. We'll tell you whether repair or replacement makes more sense."),
        ("My double-pane window is foggy. Do I need a new window?", "Usually not. Fog means the seal on the insulated glass unit has failed, and we can often replace just the glass and keep your frame."),
        ("Which window brands do you carry?", "Marvin, Simonton, Ply Gem and Marlin, among others. We'll help you pick based on budget, style and performance.")]),
    ("shower", "Shower doors", [
        ("How long does a custom shower door take?", "It's made to order after an on-site measure, which we do once tile is finished. We'll give you a timeline at that visit."),
        ("Frameless or semi-frameless?", "Frameless gives the most open, high-end look. Semi-frameless is a crisp, budget-friendly middle ground. We'll show you both.")]),
    ("rv", "RV &amp; auto", [
        ("Do you warranty RV glass?", "Yes. We install O.E.M.-approved glass and back our RV work with a lifetime warranty."),
        ("I'm not local. Can you still help?", "Yes. Ship us your RV window and we'll repair or custom-match it and send it back. Call first for packing tips."),
        ("Is there room for a big rig?", "Plenty. We have a spacious lot and turnaround, plus a large indoor facility for the work itself.")]),
    ("commercial", "Commercial", [
        ("Do you work with contractors and architects?", "Yes. We work directly with owners, general contractors and architects to select and install the right system."),
        ("Do you service door closers?", "Yes, including sales, installation and service for fire-rated doors.")]),
    ("general", "General", [
        ("Are estimates really free?", "Yes. We come out, measure on-site and give you an honest quote with no obligation."),
        ("Where are you and when are you open?", "1206 Franz St SE in Lacey, Monday through Friday, 8am to 5pm."),
        ("What area do you serve?", "Thurston and Pierce County, including Olympia, Lacey, Tumwater, DuPont, Lakewood and South Tacoma, with a larger area for residential and commercial windows.")]),
]
faq_nav = "".join(f'<a href="#{k}">{t}</a>' for k, t, _ in FAQ_GROUPS)
faq_groups = "".join(f'<div class="faq-group" id="{k}"><h3 class="reveal">{t}</h3>{faq_list(items)}</div>' for k, t, items in FAQ_GROUPS)
faq_body = hero("1773579089983-50348cc9abd0", [("FAQ", None)], "Questions &amp; answers",
                "Good <em>questions.</em>",
                "Straight answers about windows, doors, shower glass, RVs and how we work. Still stuck? Call the shop. A real person picks up.",
                short=True)
faq_body += f'''
<section><div class="wrap faq-layout"><nav class="faq-nav reveal" aria-label="FAQ topics">{faq_nav}</nav><div>{faq_groups}</div></div></section>
''' + cta("Didn't see <em>your</em> question?", "Call 360-456-0668 or send a note. We're happy to help you understand your options.")
PAGES["faq"] = page("FAQ", "Answers to common questions about windows, doors, shower glass, RV glass and estimates.", faq_body, "faq")

# ---------------- contact
contact_body = hero("1613578519724-22fdb5d06388", [("Contact", None)], "Free at-home estimate",
                    "Let's talk <em>glass.</em>",
                    "Call, stop by the Lacey shop, or send the form. We'll come measure on-site and give you an honest quote.",
                    [("Phone", PHONE), ("Shop", "1206 Franz St SE, Lacey"), ("Hours", "Mon–Fri, 8am–5pm")], short=True)
picks = [("windows", "Windows"), ("shower", "Shower door"), ("door", "Entry door"), ("storefront", "Storefront"),
         ("skylight", "Skylight"), ("mirror", "Mirror / specialty"), ("rv", "RV / Auto")]
picks_html = "".join(f'<input type="checkbox" id="p{i}" data-type="{k}"{" checked" if i == 0 else ""}><label for="p{i}">{t}</label>' for i, (k, t) in enumerate(picks))
contact_body += f'''
<section>
  <div class="wrap visit">
    <div class="card reveal"><small>Call</small><b><a href="{TEL}">{PHONE}</a></b><p>The fastest way to reach us. A real person answers during business hours.</p><a class="more" href="{TEL}">Call now →</a></div>
    <div class="card reveal"><small>Visit the shop</small><b>1206 Franz St SE<br>Lacey, WA 98503</b><p>Plenty of room in the lot, even for RVs.</p><a class="more" href="{MAPS}" target="_blank" rel="noopener">Get directions →</a></div>
    <div class="card reveal"><small>Hours</small><ul class="hours" id="hours" style="margin-top:12px">
      <li data-d="1"><span>Monday</span><span>8–5</span></li><li data-d="2"><span>Tuesday</span><span>8–5</span></li><li data-d="3"><span>Wednesday</span><span>8–5</span></li><li data-d="4"><span>Thursday</span><span>8–5</span></li><li data-d="5"><span>Friday</span><span>8–5</span></li><li data-d="6"><span>Saturday</span><span>Closed</span></li><li data-d="0"><span>Sunday</span><span>Closed</span></li></ul></div>
  </div>
</section>
<section id="estimate" class="cta tint">
  <div class="wrap cta-grid">
    <div class="reveal">
      <span class="eyebrow">Request an estimate</span>
      <h2>Tell us about<br>the <em>opening.</em></h2>
      <p style="color:var(--muted);max-width:28em">A few details helps us come prepared. We'll call to set up a time to measure. No obligation.</p>
      <div class="contact-list">
        <div><small>Response</small><b>Usually within one business day</b></div>
        <div><small>Estimate</small><b>Free, measured on-site</b></div>
        <div><small>RV glass</small><b>Bring it in, or ship your window</b></div>
      </div>
    </div>
    <form class="reveal" id="form">
      <div id="formBody" style="display:grid;gap:18px">
        <h3>Request an estimate</h3>
        <div class="field"><label>What's the project?</label><div class="picks">{picks_html}</div></div>
        <div class="two">
          <div class="field"><label for="n">Name</label><input id="n" placeholder="Your name"></div>
          <div class="field"><label for="ph">Phone</label><input id="ph" placeholder="(360) 555-0123"></div>
        </div>
        <div class="field"><label for="c">City</label><input id="c" placeholder="Olympia"></div>
        <div class="field"><label for="d">Details</label><textarea id="d" rows="3" placeholder="e.g. 3 drafty bedroom windows, original to the house"></textarea></div>
        <button class="btn btn-primary" type="submit">Send request <span class="arrow">→</span></button>
      </div>
      <div class="sent" id="sent"><b>Thanks, we'll call you.</b><span style="color:var(--muted)">Usually within one business day.</span></div>
    </form>
  </div>
</section>
<script>(()=>{{try{{const d=new Date(new Date().toLocaleString('en-US',{{timeZone:'America/Los_Angeles'}})).getDay();const li=document.querySelector('#hours [data-d="'+d+'"]');if(li)li.classList.add('today')}}catch(e){{}}}})();</script>'''
PAGES["contact"] = page("Contact & Estimates", "Request a free at-home glass estimate from D.K. Boos Glass in Lacey, WA.", contact_body, "contact")

# ------------------------------------------------------------------ write
def main():
    idx = INDEX.read_text()
    sprite = re.search(r'<svg width="0" height="0".*?</defs></svg>', idx, re.S).group(0)
    for name, html in PAGES.items():
        (ROOT / f"{name}.html").write_text(html.replace("<!--SPRITE-->", sprite))
        print("wrote", f"{name}.html")
    idx = re.sub(r"<!--nav-->.*?<!--/nav-->", lambda _: nav("", "#estimate"), idx, flags=re.S)
    idx = re.sub(r"<!--footer-->.*?<!--/footer-->", lambda _: footer(), idx, flags=re.S)
    INDEX.write_text(idx)
    print("synced nav/footer in index.html")

if __name__ == "__main__":
    main()
