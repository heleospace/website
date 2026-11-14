#!/usr/bin/env python3
"""Builds the heleo.space static site into ../site.
Edit the shared header/footer or any page body here, then run:  python3 _build/build.py
Updates (news) do NOT need this script: add a Markdown file in site/updates/posts/ and list it in site/updates/posts.json."""
import os, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "site"
CONTACT = "hello@heleo.space"
GA_ID = "G-WWS90D42NG"   # Google Analytics 4 Measurement ID; set "" to switch analytics and the cookie banner off
X_URL = ""          # company X account; "" hides the footer link
GITHUB_URL = "https://github.com/heleospace/"
LINKEDIN_URL = ""   # company LinkedIn page; "" hides the footer link
SOCIAL_LINKS = "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in (("X", X_URL), ("LinkedIn", LINKEDIN_URL)) if u)
# Technical paper PDF: leave "" until the paper is published,
# then set to "/research/autonomous-mesh-technical-paper-v0.1.pdf" and upload that PDF.
PAPER_PDF = ""
# Origin of the Autonomous Mesh concept (credited on /research/ and /mesh/).
ORIGINATOR = "Eric Chan"
ORIGIN_TITLE = ""                      # optional: exact title of the original X article; if empty the link reads "an article on X"
ORIGIN_DATE = "26 October 2026"        # publish date of the article
ORIGIN_URL = "https://x.com/canmasu/status/2114704255148011772"   # PUBLIC link of the article, not the /compose/ edit link
def origin_link(text=None):
    t = text or (f"“{ORIGIN_TITLE}”, an article on X" if ORIGIN_TITLE else "an article on X")
    return f'<a href="{ORIGIN_URL}" rel="noopener">{t}</a>' if ORIGIN_URL else t

# ---- media (all free to use; see /credits/) ----
SVS = "https://svs.gsfc.nasa.gov/vis/a010000/a011400/a011474/"
M = {
  "hero_webm": "https://svs.gsfc.nasa.gov/vis/a010000/a010700/a010766/Earth_View_limb_1.webmhd.webm",
  "hero_poster": "https://svs.gsfc.nasa.gov/vis/a010000/a010700/a010766/Earth_View-limb_1-prvWeb..00002_print.jpg",
  "og_image": "https://www.nasa.gov/wp-content/uploads/2023/03/iss066e152098.jpg",
  "aurora": SVS + "a-1920.jpg",
  "startrails": SVS + "pf-1920.jpg",
  "cities": SVS + "cover-1920.jpg",
  "sunrise": "https://www.nasa.gov/wp-content/uploads/2023/03/iss066e152098.jpg",
  "first_rays": "https://www.nasa.gov/wp-content/uploads/2024/01/the-suns-first-rays-peek-above-earths-limb-46976234625-o.jpg",
  "arrays": "https://www.nasa.gov/wp-content/uploads/2023/03/iss065e049854-1.jpg",
  "network": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1800&q=75",
  "cables": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=75",
  "aisle": "https://images.unsplash.com/photo-1584169417032-d34e8d805e8b?auto=format&fit=crop&w=1600&q=75",
}

NAV = [
  ("Technology", [("Agents", "/agents/", "Deploy an AI agent in minutes"),
                  ("Autonomous Mesh", "/mesh/", "Open software that routes and settles work"),
                  ("Machine economy", "/machines/", "Robots and fleets that buy and sell compute"),
                  ("Heleo-1", "/technology/", "A data center redesigned for orbit"),
                  ("Research", "/research/", "Five Year 1 workstreams with labs")]),
  ("Company", [("About", "/about/", "Why we exist and how we work"),
               ("Roadmap", "/roadmap/", "From the ground mesh to orbit")]),
  ("Updates", "/updates/"),
]

# The logo files come from _build/brand_assets.py. Size and colour are set in site.css.
LOGO = '<svg class="logo" viewBox="0 0 1429.45 217.87" aria-hidden="true"><use href="/assets/img/logo-sprite.svg#logo"/></svg>'

def head(title, desc, path, extra=""):
    full = title if title.startswith("Heleospace") else f"{title} · Heleospace"
    return f"""<!doctype html>
<html lang="en" data-root="/" data-ga="{GA_ID}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://heleo.space{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Heleospace">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://heleo.space{path}">
<meta property="og:image" content="https://heleo.space/assets/img/og-image.png">
<meta property="og:image:secure_url" content="https://heleo.space/assets/img/og-image.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Heleospace">
<meta property="og:locale" content="en_US">
<meta name="twitter:title" content="{full}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://heleo.space/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07080A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,200..700&family=Newsreader:opsz,wght@6..72,300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(path):
    cur = ' aria-current="page"'
    parts = []
    for i, (name, target) in enumerate(NAV):
        if isinstance(target, str):
            parts.append(f'<a class="nav-top" href="{target}"{cur if path.startswith(target) else ""}>{name}</a>')
            continue
        active = any(path.startswith(h) for _, h, _ in target)
        items = "".join(f'<a href="{h}"{cur if path.startswith(h) else ""}><b>{n}</b><span>{d}</span></a>' for n, h, d in target)
        parts.append(f'<div class="nav-group{" is-active" if active else ""}"><button type="button" class="nav-top" aria-expanded="false" aria-controls="sub-{i}">{name}<svg viewBox="0 0 12 12" width="10" height="10" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button><div class="nav-sub" id="sub-{i}">{items}</div></div>')
    parts.append('<a class="nav-top nav-contact" href="/contact/">Contact</a>')
    links = "".join(parts)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Heleospace home">{LOGO}</a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <a class="btn header-cta" href="/contact/">Contact</a>
    <button class="menu-btn" aria-expanded="false" aria-label="Open menu">Menu</button>
  </div>
</header>
"""

def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="/" aria-label="Heleospace home">{LOGO}</a>
        <p>Orbital data centers, run as an autonomous economy.</p>
      </div>
      <div><h4>Company</h4><ul><li><a href="/about/">About</a></li><li><a href="/roadmap/">Roadmap</a></li><li><a href="/updates/">Updates</a></li><li><a href="/contact/">Contact</a></li><li><a href="/brand/">Brand kit</a></li></ul></div>
      <div><h4>Technology</h4><ul><li><a href="/agents/">Agents</a></li><li><a href="/mesh/">Autonomous Mesh</a></li><li><a href="/machines/">Machine economy</a></li><li><a href="/technology/">Heleo-1</a></li><li><a href="/research/">Research</a></li></ul></div>
      <div><h4>Work with us</h4><ul><li><a href="/contact/?topic=research">Research labs</a></li><li><a href="/contact/?topic=partner">Partners</a></li><li><a href="/contact/?topic=careers">Careers</a></li><li><a href="/contact/?topic=investor">Investors</a></li></ul></div>
      <div><h4>Elsewhere</h4><ul>{SOCIAL_LINKS}<li><a href="{GITHUB_URL}" rel="noopener">GitHub</a></li><li><a href="mailto:{CONTACT}">{CONTACT}</a></li></ul></div>
    </div>
    <div class="foot-bottom">
      <p>© <span data-year>2026</span> Heleospace LLC. Heleospace Inc. is planned. Information on this site is not an offer to sell or a solicitation of an offer to buy any security. Plans and figures describe research and targets, not promises.</p>
      <p><a href="/legal/">Legal &amp; privacy</a> · <a href="/legal/#cookies">Cookies</a> · <a href="#" data-cookie-settings>Cookie settings</a> · <a href="/credits/">Image credits</a></p>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""

ORBIT = '<svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true"><circle cx="16" cy="16" r="7.5" fill="none" stroke="currentColor" stroke-width="1.6"/><ellipse cx="16" cy="16" rx="14" ry="5" fill="none" stroke="currentColor" stroke-width="1.1" transform="rotate(-28 16 16)" opacity=".7"/><circle cx="27.6" cy="10.3" r="2.2" fill="#FF5E3A"/></svg>'

def page_hero(label, title, lede, img, credit, btns=""):
    return f"""<section class="page-hero on-night">
  <img class="bg" src="{img}" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="eyebrow">{label}</p>
    <h1 class="display">{title}</h1>
    <p class="lede">{lede}</p>{btns}
  </div>
  <span class="credit">{credit}</span>
</section>
"""

def article(body, rail, cta, updated="4 November 2026"):
    rail_html = "".join(f'<a href="#{i}">{t}</a>' for i, t in rail)
    return f"""<main id="main" class="article">
  <article>
    <div class="body">{body}</div>
    <div class="cta">{cta}</div>
    <p class="meta">Last updated {updated}</p>
  </article>
  <nav class="rail" aria-label="On this page"><h4>On this page</h4>{rail_html}</nav>
</main>
"""

def write(path, html):
    p = OUT / path.strip("/") / "index.html" if not path.endswith(".html") else OUT / path.strip("/")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")

# ---------------- diagram: the mesh across ground and orbit ----------------
MESH_SVG = """<svg viewBox="0 0 1200 420" role="img" aria-label="Diagram: orbital nodes and ground data centers linked by the Heleo Mesh, with work and payments flowing between them">
<defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#93A6BA" stop-opacity=".22"/><stop offset="1" stop-color="#93A6BA" stop-opacity="0"/></linearGradient></defs>
<path d="M-20 420 Q600 250 1220 420Z" fill="url(#g)"/><path d="M-20 420 Q600 250 1220 420" fill="none" stroke="#9AA6B4" stroke-opacity=".5"/>
<path d="M-20 300 Q600 -40 1220 300" fill="none" stroke="#FFF3DC" stroke-opacity=".25" stroke-dasharray="3 7"/>
<g stroke="#FF5E3A" stroke-width="1.4" fill="none" stroke-opacity=".85">
<path d="M190 205 L420 120"/><path d="M420 120 L780 120"/><path d="M780 120 L1010 205"/>
<path d="M420 120 L330 352"/><path d="M780 120 L870 352"/><path d="M190 205 L330 352"/><path d="M1010 205 L870 352"/><path d="M330 352 L600 335 L870 352" stroke-dasharray="5 6"/><path d="M600 335 L780 120" stroke-opacity=".45"/></g>
<g fill="#07080A" stroke="#FFF3DC" stroke-width="1.4">
<rect x="176" y="191" width="28" height="28" transform="rotate(45 190 205)"/><rect x="406" y="106" width="28" height="28" transform="rotate(45 420 120)"/><rect x="766" y="106" width="28" height="28" transform="rotate(45 780 120)"/><rect x="996" y="191" width="28" height="28" transform="rotate(45 1010 205)"/></g>
<g fill="#FF5E3A"><circle cx="330" cy="352" r="9"/><circle cx="600" cy="335" r="9"/><circle cx="870" cy="352" r="9"/></g>
<g font-family="Archivo, Arial, sans-serif" font-size="17" fill="#9AA6B4">
<text x="420" y="84" text-anchor="middle">Orbital node</text><text x="780" y="84" text-anchor="middle">Orbital node</text>
<text x="190" y="172" text-anchor="middle">Orbital node</text><text x="1010" y="172" text-anchor="middle">Orbital node</text>
<text x="330" y="394" text-anchor="middle">Ground data center</text><text x="600" y="377" text-anchor="middle">Research lab</text><text x="870" y="394" text-anchor="middle">Ground data center</text>
<text x="600" y="162" text-anchor="middle" fill="#FF5E3A">work + payment, settled machine to machine</text></g>
</svg>"""

# ---------------- HOME ----------------
home = head("Heleospace — Orbital data centers, run as an autonomous economy",
            "Heleospace builds orbital data centers that run as an autonomous economy: compute in orbit and on the ground that finds work, agrees a price and settles on its own.", "/") + header("/") + f"""
<main id="main">
<section class="hero on-night">
  <video class="hero-launch is-on" autoplay muted loop playsinline preload="metadata" poster="/assets/media/hero-launch-poster.jpg" aria-hidden="true" data-hold="18" data-caption="Artemis II liftoff, seen from Banana Creek · NASA">
    <source src="/assets/media/hero-launch.mp4" type="video/mp4">
  </video>
  <video muted loop playsinline preload="none" aria-hidden="true" data-hold="20" data-caption="Earth&#8217;s limb from the International Space Station · NASA">
    <source src="{M['hero_webm']}" type="video/webm">
  </video>
  <div class="wrap">
    <p class="eyebrow">Heleospace</p>
    <h1 class="display">Orbital data centers, run as an autonomous economy.</h1>
    <p class="lede">Solar-powered compute in orbit and on the ground that finds work, agrees a price and settles on its own, through the open Heleo Mesh, where AI agents and machines buy compute, get paid and are trusted.</p>
    <div class="btns"><a class="btn primary" href="/mesh/"><span class="arrow">How the Mesh works</span></a><a class="btn" href="/updates/">Latest updates</a></div>
    <div class="hero-meta"><span data-video-caption>Artemis II liftoff, seen from Banana Creek · NASA</span><button type="button" data-video-toggle>Pause video</button></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">The problem</p><h2 class="display">AI compute is outgrowing the ground.</h2></div>
      <p>Demand for AI compute keeps rising. The ground cannot add power, cooling and land fast enough, and nothing yet lets machines on Earth and in orbit work as one system.</p>
    </div>
    <div class="cols c4 reveal">
      <div class="col"><span class="num">01</span><h3>Power</h3><p>New AI data centers wait years for a grid connection.</p></div>
      <div class="col"><span class="num">02</span><h3>Cooling</h3><p>Every new site needs large amounts of water and cooling.</p></div>
      <div class="col"><span class="num">03</span><h3>Land</h3><p>Sites near spare grid capacity are scarce.</p></div>
      <div class="col accent"><span class="num">04</span><h3>Coordination</h3><p>Orbital and ground nodes have no shared way to route work and pay each other.</p></div>
    </div>
  </div>
</section>

<section class="section night band on-night">
  <img class="bg" src="{M['sunrise']}" alt="" loading="lazy">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">The physics</p><h2 class="display">In orbit, the sun barely sets and space is the heat sink.</h2></div>
      <p>A dawn-dusk orbit keeps solar arrays in near-continuous sunlight, and heat leaves as radiation, with no water. The hard parts are radiation, heat at high density and launch cost, and that is where our research starts.</p>
    </div>
    <div class="stats reveal">
      <div class="stat"><b>1,361<small>W/m²</small></b><span>Sunlight above the atmosphere, near-continuous in a dawn-dusk orbit</span></div>
      <div class="stat"><b>≈400<small>W/m²</small></b><span>Solar array output at roughly 30% cell efficiency</span></div>
      <div class="stat"><b>≈410<small>W/m²</small></b><span>Heat a 300 K radiator rejects per face in vacuum</span></div>
      <div class="stat"><b>&lt;600<small>km</small></b><span>Low Earth orbit; satellites deorbit by natural decay at end of life</span></div>
    </div>
  </div>
</section>

<section class="section night on-night" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal rule-top">
      <div><p class="eyebrow">How it works</p><h2 class="display">One network. Machines trade compute, energy and data.</h2></div>
      <p>A satellite with spare capacity, a ground data center short of power and a lab with a workload find each other, agree a price and settle in seconds, with no person in the loop.</p>
    </div>
    <div class="diagram reveal">{MESH_SVG}</div>
    <div class="cols c4 reveal" style="margin-top:48px">
      <div class="col"><span class="num">Layer 0</span><h3>Agents</h3><p>Free agents, deployed in minutes, buy their compute through the Mesh. <a href="/agents/">Agents</a></p></div>
      <div class="col"><span class="num">Layer 1</span><h3>Autonomous Mesh</h3><p>Heleo Mesh, our open software, routes each piece of work to where it runs best, on Earth or in orbit.</p></div>
      <div class="col"><span class="num">Layer 2</span><h3>Orbital and ground nodes</h3><p>Solar-powered compute in low Earth orbit, linked with data centers on the ground.</p></div>
      <div class="col"><span class="num">Layer 3</span><h3>Settlement</h3><p>Machines pay and get paid for compute, energy, bandwidth and data, automatically.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <figure class="media reveal" style="aspect-ratio:3/2;margin:0"><img src="{M['arrays']}" alt="The International Space Station's solar arrays across Earth's horizon" loading="lazy"></figure>
    <div class="reveal">
      <p class="eyebrow">Capital-light by design</p>
      <h2 class="display" style="font-size:clamp(1.9rem,3.6vw,3rem)">Partners build the hardware. We build the network.</h2>
      <p class="lede" style="max-width:none">Partners supply launch, satellite buses and most data centers. Heleospace owns the layers that compound: the network, the settlement and the chip designs.</p>
      <ul>
        <li><b>Heleospace</b><span>Heleo Mesh and agents, settlement, node certification, chip designs, reference satellites</span></li>
        <li><b>Partners</b><span>Launch, satellite buses, ground data centers, chip manufacturing</span></li>
        <li><b>Together</b><span>Chips designed from Mesh workload data and orbital heat limits</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section surface">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Why it lasts</p><h2 class="display">Code can be forked. A working orbital economy cannot.</h2></div>
      <p>Hardware can be bought. A running network, with its nodes, settlement history and the labs that depend on it, takes years to build and grows harder to replace with every node that joins.</p>
    </div>
    <div class="moat reveal">
      <div><h3>Network effect</h3><p>Every node adds both supply and demand. Settlement history and node reputation stay in the network.</p><small>Testnet in Year 1</small></div>
      <div><h3>Radiation- and heat-aware routing</h3><p>The mesh moves work away from radiation zones and hot nodes, and recovers it without losing a payment.</p><small>Ground testbed in Year 1</small></div>
      <div><h3>Open standard, certified network</h3><p>Anyone can build on Heleo Mesh. Only Heleospace certifies nodes for the official network.</p><small>From incorporation</small></div>
      <div><h3>Data and flight heritage</h3><p>Lab results, then orbital telemetry, improve routing. A new entrant starts with none.</p><small>First flight in Year 3</small></div>
    </div>
  </div>
</section>

<section class="section night on-night">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Roadmap</p><h2 class="display">Live on the ground. Then fly.</h2></div>
      <p>The Mesh and its agents go live on the ground in Year 1, alongside lab work with universities and government. The first orbital demonstration follows in Year 3. These are targets, not promises.</p>
    </div>
    <div class="roadmap reveal">
      <div class="step now"><b>Year 1</b><h3>Mesh live</h3><p>Agents, Mesh ID and AI inference routing; first certified ground data centers; lab validation.</p></div>
      <div class="step"><b>Year 2</b><h3>Certified network</h3><p>Ground network grows; machine-to-machine payments between partner nodes; in-house chip design.</p></div>
      <div class="step"><b>Year 3</b><h3>Heleo-1</h3><p>First orbital demonstration and first payments settled in orbit.</p></div>
      <div class="step"><b>Year 4</b><h3>Heleo-2 to Heleo-4</h3><p>Partner fleets join; inter-satellite links; national capacity; first Heleospace chip in certified nodes.</p></div>
      <div class="step"><b>Year 5</b><h3>Open standard</h3><p>The protocol for agents and ground-to-orbit compute, with recurring settlement revenue.</p></div>
    </div>
    <div class="btns reveal"><a class="btn" href="/roadmap/"><span class="arrow">Full roadmap</span></a></div>
  </div>
</section>

<section class="section">
  <div class="wrap split flip">
    <figure class="media reveal" style="margin:0"><img src="{M['aisle']}" alt="An aisle between server racks in a data center" loading="lazy"></figure>
    <div class="reveal">
      <p class="eyebrow">Research</p>
      <h2 class="display" style="font-size:clamp(1.9rem,3.6vw,3rem)">Measured results, not claims.</h2>
      <p class="lede" style="max-width:none">Five Year 1 workstreams with university and government labs remove the barriers before the first flight.</p>
      <ul>
        <li><b>Radiation</b><span>Beam tests of a low-power compute module</span></li>
        <li><b>Shielding</b><span>The lightest option that meets the dose target</span></li>
        <li><b>Fault tolerance</b><span>Mesh recovery under injected faults</span></li>
        <li><b>Thermal-vacuum</b><span>Verified heat limits per node</span></li>
        <li><b>Settlement</b><span>Payments that stay correct when nodes fail</span></li>
      </ul>
      <div class="btns"><a class="btn" href="/research/"><span class="arrow">Research program</span></a></div>
    </div>
  </div>
</section>

<section class="section surface">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Updates</p><h2 class="display">From the team.</h2></div>
      <p><a class="link arrow" href="/updates/">All updates </a></p>
    </div>
    <div class="posts" data-posts="3"><p class="posts-empty">Loading updates…</p></div>
  </div>
</section>

<section class="section night band on-night">
  <img class="bg" src="{M['cities']}" alt="" loading="lazy">
  <div class="wrap closing reveal">
    <p class="eyebrow">Work with us</p>
    <h2 class="display">Build the orbital economy with us.</h2>
    <p class="lede">Research labs, launch and chip partners, engineers and long-term investors: we would like to hear from you.</p>
    <div class="btns"><a class="btn primary" href="/contact/"><span class="arrow">Get in touch</span></a><a class="btn" href="/about/">About Heleospace</a></div>
  </div>
</section>
</main>
""" + footer()
write("/", home)

# ---------------- AGENTS ----------------
agents_body = """
<h2 id="what">Agents on the Heleo Mesh</h2>
<p>Anyone can deploy an AI agent on the Heleo Mesh in minutes. Start from a <strong>Mold</strong>, a free and open template for an agent. <strong>Remold</strong> it to change what it does, then <strong>Deploy</strong> it. The agent layer is planned for Year 1.</p>
<h2 id="id">Mesh ID</h2>
<p>Every agent and machine on the Mesh gets a Mesh ID: one identity that carries its trust record and lets it pay and be paid. Mesh ID builds on open standards, ERC-8004 for agent identity and ERC-6551 for agent accounts, so it is not locked to one company.</p>
<h2 id="neutral">Neutral by design</h2>
<p>Agents can use any AI model, any chip and any chain. Heleo Mesh routes each job to where it runs best, on the ground or in orbit.</p>
<h2 id="how">How agents use the Mesh</h2>
<p>An agent pays for its AI inference through the Mesh: from certified ground data centers first, and from orbital nodes once they fly. Each job is settled automatically, machine to machine. The same identity and settlement serve robots and fleets; see <a href="/machines/">the machine economy</a>.</p>
<h2 id="next">What comes next</h2>
<ol><li>Molds, Deploy and Mesh ID on the ground mesh.</li><li>Hosted agents for organisations.</li><li>Agents that run across ground and orbit after Heleo-1 flies.</li></ol>
"""
write("/agents/", head("Agents", "Deploy an AI agent on the Heleo Mesh in minutes. Every agent gets a Mesh ID to be trusted, pay and get paid.", "/agents/")
      + header("/agents/") + page_hero("Agents", "Deploy an AI agent in minutes", "Free, open agents that buy their compute through the Heleo Mesh, with one identity to be trusted, pay and get paid.", M["cities"], "City lights from the ISS · NASA")
      + article(agents_body, [("what", "Agents"), ("id", "Mesh ID"), ("neutral", "Neutral by design"), ("how", "How agents use the Mesh"), ("next", "What comes next")],
                '<a class="btn primary" href="/mesh/"><span class="arrow">The Autonomous Mesh</span></a><a class="btn" href="/contact/?topic=research">Build with us</a>', updated="13 November 2026") + footer())

# ---------------- MESH ----------------
mesh_body = f"""
<h2 id="what">What the Mesh is</h2>
<p>Heleo Mesh is our open implementation of the Autonomous Mesh: software that lets compute, energy, data and tasks route themselves across Earth and orbit. Nodes on the ground and in orbit offer capacity. Software agents decide where each piece of work should run. A settlement layer lets machines agree a price and pay each other automatically.</p>
<p>Heleospace builds Heleo Mesh and operates the official network. The code is open; the certified network, its settlement history and its operations are ours.</p>
<h2 id="stack">Six layers</h2>
<div class="table-wrap"><table>
<tr><th>Layer</th><th>What it does</th><th>Who provides it</th></tr>
<tr><td>Agents</td><td>Free Molds deploy agents in minutes; each agent and machine gets a Mesh ID</td><td>Heleospace (open source)</td></tr>
<tr><td>Autonomous Mesh</td><td>Routes compute, energy, data and tasks to where they run best</td><td>Heleospace (open source)</td></tr>
<tr><td>Compute and energy</td><td>Solar-powered AI compute on the ground and in orbit</td><td>Certified ground data centers, partner orbital fleets and Heleospace&#8217;s reference fleet</td></tr>
<tr><td>Chips</td><td>Low-power processors designed from Mesh workload data, which also cut heat in orbit</td><td>Heleospace owns the designs; foundries manufacture</td></tr>
<tr><td>Deployment</td><td>Launch and operation of orbital nodes</td><td>Chartered launches and partner satellite buses</td></tr>
<tr><td>Settlement</td><td>Machine-to-machine payment for compute, energy, bandwidth and data</td><td>Heleospace</td></tr>
</table></div>
<p>Heleospace owns the network, the settlement, the chip designs and a reference fleet. Partners own launch and most data centers.</p>
<h2 id="economy">An economy, not a schedule</h2>
<p>Today, compute is bought by people, through contracts and invoices. In the Mesh, a satellite with spare capacity, a ground data center short of power and a lab with a workload find each other, agree a price and settle in seconds. Every transaction carries a small settlement fee, and every new node makes the network more useful to the others. AI agents are the first buyers: each one buys its compute through the Mesh.</p>
<figure><img src="{M['network']}" alt="Earth at night with city lights and network lines" loading="lazy"><figcaption>Earth at night. Photo: NASA, via Unsplash.</figcaption></figure>
<h2 id="lineage">Lineage</h2>
<p>Heleo Mesh extends the open-source Morpheus codebase (<a href="https://mor.org" rel="noopener">mor.org</a>), a decentralized AI network running on the ground since 2024. Heleospace adapts that ground mesh for orbit: a compute marketplace across Earth and space first, then an autonomous gateway between ground and orbital nodes, then settlement, then one network across both.</p>
<p>The Autonomous Mesh concept was originated by {ORIGINATOR}, who first described it in {origin_link()} ({ORIGIN_DATE}). <a href="/research/#origin">From idea to paper</a>.</p>
<h2 id="unknown">What we are still finding out</h2>
<ol><li>How much work the mesh can recover after a radiation event without losing settlement correctness.</li><li>How fast routing decisions must be when links between orbit planes come and go.</li><li>Which settlement design stays correct when nodes drop out mid-transaction.</li></ol>
"""
write("/mesh/", head("The Autonomous Mesh", "Heleo Mesh, our open implementation of the Autonomous Mesh, routes compute, energy and data across Earth and orbit and lets machines settle automatically.", "/mesh/")
      + header("/mesh/") + page_hero("Mesh", "The Autonomous Mesh", "Open software that lets compute, energy, data and tasks route themselves across Earth and orbit, and lets machines pay each other.", M["aurora"], "Aurora from the ISS · NASA")
      + article(mesh_body, [("what", "What the Mesh is"), ("stack", "Six layers"), ("economy", "An economy"), ("lineage", "Lineage"), ("unknown", "Still unknown")],
                '<a class="btn primary" href="/technology/"><span class="arrow">Technology</span></a><a class="btn" href="/contact/?topic=research">Build with us</a>', updated="13 November 2026") + footer())

# ---------------- MACHINES ----------------
MM = {
  "highway": "https://images.unsplash.com/photo-1641558024625-5906eae28712?auto=format&fit=crop&w=2000&q=75",
  "citytrails": "https://images.unsplash.com/photo-1647962924881-88c4029bbb9d?auto=format&fit=crop&w=1600&q=75",
  "robonaut": "https://www.nasa.gov/wp-content/uploads/2023/03/iss036e013254.jpg",
  "astrobee": "https://images-assets.nasa.gov/image/iss071e046284/iss071e046284~medium.jpg",
  "desert": "https://svs.gsfc.nasa.gov/vis/a010000/a010700/a010766/Earth_View-desert-Africa-prvWeb..00002_print.jpg",
}
def machine(i, flip, img, alt, cap, label, title, lede, buys, sells):
    return f"""<section class="section{' surface' if i % 2 else ''}">
  <div class="wrap split{' flip' if flip else ''}">
    <figure class="media reveal" style="aspect-ratio:4/3"><img src="{img}" alt="{alt}" loading="lazy"><figcaption class="caption" style="position:absolute;left:12px;bottom:10px;margin:0;color:#fff;opacity:.8">{cap}</figcaption></figure>
    <div class="reveal">
      <p class="eyebrow">{label}</p>
      <h2 class="display" style="font-size:clamp(1.9rem,3.6vw,3rem)">{title}</h2>
      <p class="lede" style="max-width:none">{lede}</p>
      <ul>
        <li><b>Buys from the Mesh</b><span>{buys}</span></li>
        <li><b>Sells back</b><span>{sells}</span></li>
      </ul>
    </div>
  </div>
</section>
"""
machines_html = head("The machine economy", "Robots, vehicles and drones generate more data than they can process on board. The Heleo Mesh gives them somewhere to send it, and a way to pay.", "/machines/") + header("/machines/") + page_hero(
  "Machines", "Machines that buy, sell and share compute", "Robots, vehicles and drones generate more data than they can process on board. The Mesh gives them somewhere to send it, and a way to pay.", MM["highway"], "Photo: Akin Cakiner, Unsplash") + f"""
<main id="main">
<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Why machines need the Mesh</p><h2 class="display">On-board compute runs out. Data does not.</h2></div>
      <p>A machine's own compute is limited by its battery and its heat. Fleets produce large volumes of driving and sensor data every day. Today a person signs a cloud contract on their behalf. In the Mesh, the machine buys what it needs, when it needs it, and settles automatically.</p>
    </div>
    <div class="cols c3 reveal">
      <div class="col"><span class="num">01</span><h3>Limited on board</h3><p>Battery and heat cap how much a robot or vehicle can compute while it works.</p></div>
      <div class="col"><span class="num">02</span><h3>Data keeps growing</h3><p>Cameras and sensors produce far more data than a machine can learn from on its own.</p></div>
      <div class="col accent"><span class="num">03</span><h3>Pay as it goes</h3><p>Machines find capacity on the ground or in orbit, agree a price and pay for verified work. Each machine carries a Mesh ID, so it can be trusted and paid.</p></div>
    </div>
  </div>
</section>
""" + machine(1, False, MM["citytrails"], "Long-exposure light trails of city traffic at night", "Photo: Richard Horne, Unsplash",
   "Robotaxi fleets", "Learn from every trip, overnight.", "A fleet ends the day with hours of driving data. The Mesh finds capacity to train on it while the vehicles charge.",
   "Overnight training on the day's driving data; map updates", "Idle on-board compute while parked and charging") \
+ machine(2, True, MM["desert"], "A desert landscape seen from the International Space Station", "NASA",
   "Delivery and logistics fleets", "Plan the whole fleet, not one route.", "Fleet-wide route planning and simulation need more compute than any single vehicle carries.",
   "Fleet-wide route planning, simulation of new routes", "Spare battery energy at depots, road and sensor data") \
+ machine(3, False, MM["robonaut"], "Robonaut 2, a humanoid robot, aboard the International Space Station", "Robonaut 2 on the ISS · NASA",
   "Humanoid robots", "Think harder when it matters.", "A humanoid handles balance and movement on board, and sends heavy reasoning and learning to the Mesh.",
   "Heavy reasoning, new skills downloaded when ready", "Task data that improves shared models") \
+ machine(4, True, MM["desert"].replace("desert-Africa","Ocean_and_Land-snowy_mountains").replace("00002","00952"), "Snow-covered mountains seen from the International Space Station", "NASA",
   "Legged robots at remote sites", "Inspect where there is no network.", "Legged robots inspect pipelines, mines and power lines far from ground networks. A satellite link and orbital compute bring the analysis to them.",
   "Inspection analysis through satellite links", "Site imagery and sensor readings") \
+ machine(5, False, MM["astrobee"], "An Astrobee free-flying robot aboard the International Space Station", "Astrobee on the ISS · NASA",
   "Drones and space robots", "Process data where it is captured.", "Drones and robots in orbit capture data far from any data center. Nearby nodes process it and send back only results.",
   "Processing close to where data is captured", "Spare capacity while in sunlight") + """
<section class="section night on-night">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">A night in the Mesh</p><h2 class="display">A robotaxi parks. By morning it has learned.</h2></div>
      <p>An illustration of how a single job could flow through the Mesh. Times are an example, not a measurement.</p>
    </div>
    <div class="roadmap reveal">
      <div class="step"><b>02:00</b><h3>Parks and charges</h3><p>The vehicle uploads the day's driving data and posts a training job with a deadline and a maximum price.</p></div>
      <div class="step"><b>02:01</b><h3>Finds capacity</h3><p>An orbital node in sunlight has spare compute. Its agent quotes a price; the vehicle's agent accepts and locks payment.</p></div>
      <div class="step now"><b>02:05</b><h3>Trains</h3><p>The job runs with checkpoints. If a node drops out, the Mesh moves the work to another node.</p></div>
      <div class="step"><b>05:30</b><h3>Verifies and pays</h3><p>Checkpoints are verified and payment for verified work is released automatically.</p></div>
      <div class="step"><b>06:00</b><h3>Back on the road</h3><p>The updated model is ready before the first ride of the day.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">What stays on board</p><h2 class="display">Real-time control never leaves the machine.</h2></div>
      <p>Even low Earth orbit adds tens of milliseconds and links come and go. Steering, balance and safety decisions always run on the machine. The Mesh is for work that can wait seconds, minutes or hours.</p>
    </div>
    <div class="cols c2 reveal">
      <div class="col"><span class="num">On the machine</span><h3>Milliseconds matter</h3><p>Steering, braking, balance, obstacle avoidance, safety stops and anything that must answer in under about 100 ms.</p></div>
      <div class="col accent"><span class="num">On the Mesh</span><h3>Work that can wait</h3><p>Training, map building, fleet learning, simulation, inspection analysis and heavy reasoning that can take seconds or longer.</p></div>
    </div>
  </div>
</section>

<section class="section surface">
  <div class="wrap closing reveal">
    <p class="eyebrow">Status</p>
    <h2 class="display">The market we are designing for.</h2>
    <p class="lede">Today the Mesh runs on ground nodes. Machine participants are part of our research and future pilots; the machines on this page describe who the Mesh is built for, not current customers.</p>
    <div class="btns"><a class="btn primary" href="/contact/?topic=partner"><span class="arrow">Fleet or robot builder? Work with us</span></a><a class="btn" href="/mesh/">How the Mesh works</a></div>
  </div>
</section>
</main>
""" + footer()
write("/machines/", machines_html)

# ---------------- TECHNOLOGY ----------------
tech_body = f"""
<h2 id="physics">The physics</h2>
<div class="table-wrap"><table>
<tr><th>Factor</th><th>Figure and assumption</th></tr>
<tr><td>Sunlight</td><td>About 1,361 W/m² above the atmosphere, near-continuous in a dawn-dusk orbit</td></tr>
<tr><td>Solar array</td><td>About 400 W/m² at roughly 30% cell efficiency</td></tr>
<tr><td>Heat rejection</td><td>Heat leaves only as radiation: a 300 K radiator rejects about 410 W/m² per face</td></tr>
<tr><td>Radiator size</td><td>A 500 W payload needs roughly 1.2–1.5 m² of radiator</td></tr>
<tr><td>Orbit</td><td>Low Earth orbit below 600 km; deorbit by natural decay at end of life</td></tr>
</table></div>
<h2 id="radiation">Radiation, in layers</h2>
<p><strong>Shielding.</strong> A trade study compares aluminium, spot shielding and layered materials to find the lightest option that meets the dose target. <strong>Hardware.</strong> A supervisor circuit detects a latch-up, cuts power almost instantly and restarts the processor. <strong>Software.</strong> Error-correcting memory and checkpointing. <strong>Network.</strong> The mesh moves interrupted work to a healthy node, so a radiation event costs no work. <strong>Orbit.</strong> The mesh schedules sensitive work around the polar regions and the South Atlantic Anomaly.</p>
<h2 id="thermal">Heat and energy</h2>
<p>Low-power chips cut heat at the source; Heleospace designs them from Mesh workload data, and foundries manufacture them. Heat pipes carry it to deployable radiators, and a dawn-dusk orbit keeps the load steady. The mesh throttles work and routes it to nodes with thermal headroom.</p>
<figure><img src="{M['first_rays']}" alt="The sun's first rays above Earth's limb, seen from the International Space Station" loading="lazy"><figcaption>An orbital sunrise from the International Space Station, 2019. Photo: NASA.</figcaption></figure>
<h2 id="heleo-1">Heleo-1, the reference satellite</h2>
<p>Heleo-1 is the reference satellite for the Heleo Mesh in orbit. It is a concept; none has flown.</p>
<div class="table-wrap"><table>
<tr><th>Satellite</th><th>Plan</th></tr>
<tr><td>Heleo-1</td><td>First orbital demonstration, Year 3. About 60 kg on a commercial bus, rideshare launch, dawn-dusk orbit</td></tr>
<tr><td>Heleo-2 to Heleo-4</td><td>Year 4. Inclined 53°, polar and near-equatorial orbits with inter-satellite links, so work can route across orbit planes</td></tr>
</table></div>
<h2 id="launch">Launch and servicing</h2>
<p>Designed for rideshare missions with a launch partner. Satellites are replaced, not repaired; software updates go over the air; and the mesh routes around any failed node. Our economic model states the launch price at which orbital compute matches ground data centers as an explicit assumption: today orbital compute costs more per GPU-hour, and the case depends on launch costs falling.</p>
"""
write("/technology/", head("Technology · Heleo-1", "How Heleospace handles radiation, heat and launch, and Heleo-1, the reference satellite for the Heleo Mesh.", "/technology/")
      + header("/technology/") + page_hero("Technology", "A data center, redesigned for orbit", "The main barrier is radiation. Our research is built to remove it in partner labs before the first flight; the flight validates what labs cannot reproduce.", M["sunrise"], "Orbital sunrise from the ISS · NASA")
      + article(tech_body, [("physics", "The physics"), ("radiation", "Radiation"), ("thermal", "Heat and energy"), ("heleo-1", "Heleo-1"), ("launch", "Launch and servicing")],
                '<a class="btn primary" href="/research/"><span class="arrow">Research program</span></a><a class="btn" href="/roadmap/">Roadmap</a>', updated="13 November 2026") + footer())

# ---------------- RESEARCH ----------------
res_body = f"""
<h2 id="origin">From idea to paper</h2>
<p>Concept originated by {ORIGINATOR}.</p>
<div class="table-wrap"><table>
<tr><th>When</th><th>Milestone</th></tr>
<tr><td>{ORIGIN_DATE}</td><td><strong>Origin.</strong> {ORIGINATOR} first describes the Autonomous Mesh in {origin_link()}.</td></tr>
<tr><td>November 2026</td><td><strong>Technical paper, Version 0.1.</strong> The formal design: architecture, settlement, routing, the research program and the risks (below).</td></tr>
<tr><td>Years 1–2</td><td><strong>Measured results.</strong> Findings from the five lab workstreams, published with partner labs where they contribute.</td></tr>
</table></div>
<h2 id="paper">Technical paper</h2>
<p><strong>The Autonomous Mesh: a technical paper</strong> (Version 0.1, November 2026). Eric Chan, Heleospace. How compute nodes on Earth and in orbit can find work, agree a price and settle automatically, with the settlement design, radiation- and heat-aware routing, the Heleo-1 reference satellite, our research program and the risks behind every figure.</p>
{('<p><a href="' + PAPER_PDF + '">Read the paper (PDF)</a></p>') if PAPER_PDF else ('<p><em>Publication coming soon.</em> To request an early copy for research or partnership, write to <a href="mailto:' + CONTACT + '">' + CONTACT + '</a>.</p>')}
<h2 id="approach">How we work</h2>
<p>Years 1 and 2 are research-led. We work with university and government research labs on joint testing, shared testbeds and co-authored papers. Every workstream produces a measured result rather than a claim, and every collaboration is also a route to the first users of Heleo Mesh.</p>
<h2 id="workstreams">Five Year 1 workstreams</h2>
<div class="table-wrap"><table>
<tr><th>Workstream</th><th>What is done</th><th>Output</th></tr>
<tr><td>1. Radiation</td><td>Beam-test the selected low-power compute module at a proton or heavy-ion facility</td><td>Measured error and latch-up rates, total dose tolerance</td></tr>
<tr><td>2. Shielding</td><td>Compare shielding options by mass against radiation reduction</td><td>The lightest shielding that meets the dose target</td></tr>
<tr><td>3. Fault-tolerant mesh</td><td>Combine the hardware supervisor with mesh-level recovery on the ground testbed, under injected faults</td><td>Recovery time and data-loss figures</td></tr>
<tr><td>4. Thermal-vacuum</td><td>Test the compute module and radiator in a vacuum chamber; validate heat-aware scheduling</td><td>Verified heat limits per node</td></tr>
<tr><td>5. Settlement under stress</td><td>Run settlement between ground nodes while faults are injected</td><td>Proof that payments stay correct when nodes fail</td></tr>
</table></div>
<h2 id="risks">Risks we track openly</h2>
<ul><li>Thermal performance at high compute density.</li><li>Long-term memory degradation under radiation.</li><li>Inter-satellite link cost and timing.</li><li>Ground-station bandwidth.</li><li>Launch price: the business case depends on launch costs falling.</li></ul>
<h2 id="questions">Open questions</h2>
<ol><li>Which shielding mass gives the best cost per unit of radiation reduction for the chosen compute module?</li><li>How much work can the mesh recover after a radiation event without losing settlement correctness?</li><li>At what launch price per kilogram does an orbital node match a ground node on cost per unit of compute?</li></ol>
<h2 id="collaborate">Collaborate</h2>
<p>We are looking for labs with beam-test, thermal-vacuum or distributed-systems capability, and for researchers who want to work on these questions with us. Results are shared with research partners and published where we can.</p>
"""
write("/research/", head("Research", "Heleospace's Year 1 research program: radiation, shielding, fault-tolerant mesh, thermal-vacuum and settlement under stress.", "/research/")
      + header("/research/") + page_hero("Research", "Measured results, not claims", "Five workstreams with university and government labs remove the barriers to compute in orbit before the first flight.", M["cables"], "Photo: Taylor Vick, Unsplash")
      + article(res_body, [("origin", "From idea to paper"), ("paper", "Technical paper"), ("approach", "How we work"), ("workstreams", "Workstreams"), ("risks", "Risks"), ("questions", "Open questions"), ("collaborate", "Collaborate")],
                '<a class="btn primary" href="/contact/?topic=research"><span class="arrow">Collaborate on research</span></a><a class="btn" href="/technology/">Technology</a>') + footer())

# ---------------- ROADMAP ----------------
road_body = """
<h2 id="plan">Five years, four pipelines</h2>
<p>The Heleo Mesh and its agents, compute supply, settlement and our chip work advance together. Each year adds to what makes the network hard to replace. Years are targets from the start of the program, not promises.</p>
<div class="table-wrap"><table>
<tr><th>Year</th><th>Heleo Mesh and agents</th><th>Compute supply</th><th>Settlement</th><th>Chips</th></tr>
<tr><td>1</td><td>Mesh live: Molds, deploy, Mesh ID; AI inference routing</td><td>First certified ground data centers; ground testbed and lab validation</td><td>Testnet, then live</td><td>Commercial low-power module qualified for Heleo-1</td></tr>
<tr><td>2</td><td>Hosted agents for organisations</td><td>Certified ground network grows; flight-ready engineering</td><td>Machine payments between partner nodes</td><td>In-house chip design team</td></tr>
<tr><td>3</td><td>Agents across ground and orbit</td><td>Heleo-1 in orbit; first orbital compute</td><td>First machine-to-machine payments in orbit</td><td>First Heleospace chip design</td></tr>
<tr><td>4</td><td>Logistics and robot agents at scale</td><td>Partner fleets join; Heleo-2 to Heleo-4; national (sovereign) capacity</td><td>Treasury services for machines</td><td>First Heleospace chip in certified nodes</td></tr>
<tr><td>5</td><td>Open standard for agents and ground-to-orbit compute</td><td>Orbital and ground capacity at scale</td><td>Recurring settlement revenue</td><td>Chip designs licensed to partner fleets</td></tr>
</table></div>
<h2 id="gates">Gates between phases</h2>
<p><strong>Before flight:</strong> measured radiation and thermal limits for the compute module, and settlement that stays correct under injected faults on the ground testbed. <strong>Before scale:</strong> Heleo-1 telemetry that confirms the lab results over a full year in orbit. <strong>Before the standard:</strong> independent groups running Heleo Mesh nodes in production.</p>
<h2 id="customers">Who it serves</h2>
<p><strong>Universities:</strong> open-source Heleo Mesh, testbed access and joint research. <strong>Government:</strong> resilient compute across ground and orbit, and sovereign deployments. <strong>Business:</strong> satellite operators, AI and cloud companies, telecoms and energy, with agents, AI inference routing and certified ground capacity from Year 1, and orbital capacity from Year 3.</p>
"""
write("/roadmap/", head("Roadmap", "The Heleospace roadmap: Heleo Mesh live on the ground in Year 1, Heleo-1 in Year 3, an open standard for agents and ground-to-orbit compute by Year 5.", "/roadmap/")
      + header("/roadmap/") + page_hero("Roadmap", "Live on the ground. Then fly.", "Live on the ground from Year 1. First orbital demonstration in Year 3. An open standard for agents and ground-to-orbit compute by Year 5.", M["startrails"], "Star trails from the ISS · NASA")
      + article(road_body, [("plan", "Five years"), ("gates", "Gates"), ("customers", "Who it serves")],
                '<a class="btn primary" href="/contact/?topic=partner"><span class="arrow">Partner with us</span></a><a class="btn" href="/updates/">Progress updates</a>', updated="13 November 2026") + footer())

# ---------------- ABOUT ----------------
about_body = f"""
<h2 id="mission">Why we exist</h2>
<p>AI compute is outgrowing the ground. Moving compute to orbit solves the physics of power and cooling, but the harder problem is coordination: making orbital and ground nodes work, and settle, as one economy. Heleospace exists to build that economy, in the open.</p>
<h2 id="team">Contributors</h2>
<p>Heleospace is built by a group of initiators and contributors with backgrounds in Bitcoin, decentralized AI and space engineering, working together with university and government research labs. Contributors work through Heleospace LLC under contributor agreements, and the team grows as the research program does.</p>
<p>Interested in contributing? <a href="/contact/?topic=careers">Get in touch</a>.</p>
<h2 id="company">The company</h2>
<p>Heleospace LLC, a Delaware company, is where the work happens today. Heleospace Inc. is planned as the operating company that will own Heleo Mesh. Partners supply launch, satellite buses and most data centers. Heleospace builds the network, the settlement and the chip designs, which foundries manufacture.</p>
<h2 id="principles">How we work</h2>
<ul><li><strong>Open by default.</strong> Heleo Mesh is open source; we publish what we learn.</li><li><strong>Numbers over adjectives.</strong> Every claim comes with units, a source or a stated assumption.</li><li><strong>Present tense only for what exists.</strong> Heleo-1 is a concept until it flies.</li><li><strong>Hard problems named openly.</strong> Radiation, heat, launch mass, servicing and debris.</li></ul>
<h2 id="lineage">Lineage</h2>
<p>Heleo Mesh extends the open-source Morpheus codebase. Some initiators contribute to Morpheus in their personal capacity; Heleospace is an independent company.</p>
"""
write("/about/", head("About", "Heleospace builds orbital data centers that run as an autonomous economy. Meet the initiators and how we work.", "/about/")
      + header("/about/") + page_hero("About", "Building the economy between Earth and orbit", "An independent company, built by contributors from Bitcoin, decentralized AI and space.", M["first_rays"], "Orbital sunrise from the ISS · NASA")
      + article(about_body, [("mission", "Why we exist"), ("team", "Contributors"), ("company", "The company"), ("principles", "How we work"), ("lineage", "Lineage")],
                '<a class="btn primary" href="/contact/?topic=careers"><span class="arrow">Join us</span></a><a class="btn" href="/contact/">Contact</a>', updated="13 November 2026") + footer())

# ---------------- UPDATES ----------------
write("/updates/", head("Updates", "News, research notes and milestones from Heleospace.", "/updates/") + header("/updates/")
      + page_hero("Updates", "News and research notes", "Milestones, research results and announcements from the Heleospace team.", M["startrails"], "Star trails from the ISS · NASA")
      + """<main id="main" class="section"><div class="wrap"><div class="posts" data-posts="0"><p class="posts-empty">Loading updates…</p></div></div></main>
""" + footer())
post_extra = """<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js" defer></script>
"""
write("/updates/post.html", head("Update", "News from Heleospace.", "/updates/", post_extra) + header("/updates/")
      + """<main id="main" class="article" style="grid-template-columns:minmax(0,var(--measure));padding-top:calc(var(--header-h) + 72px)"><article data-post><p class="posts-empty">Loading…</p></article></main>
""" + footer())

# ---------------- CONTACT ----------------
contact = head("Contact", "Contact Heleospace about research collaboration, partnerships, careers or investment.", "/contact/") + header("/contact/") + page_hero(
    "Contact", "Let's talk", "Research labs, partners, engineers and investors. Tell us who you are and we will reply.", M["cities"], "Earth at night from the ISS · NASA") + f"""
<main id="main" class="article">
  <article>
    <div class="body">
      <h2 id="write">Write to us</h2>
      <p>Use the form, or email <a href="mailto:{CONTACT}">{CONTACT}</a>. Messages go straight to our team.</p>
      <p class="form-error" id="form-error" role="alert" hidden></p>
      <form class="form" id="contact-form" action="/contact/send.php" method="POST">
        <div style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this empty<input type="text" name="hx_trap_9" value="" tabindex="-1" autocomplete="new-password" data-lpignore="true" data-1p-ignore></label></div>
        <label>Your name<input name="name" required maxlength="120" autocomplete="name"></label>
        <label>Email<input name="email" type="email" required maxlength="200" autocomplete="email"></label>
        <label>Organisation<input name="organisation" maxlength="160" autocomplete="organization"></label>
        <label>Topic<select name="topic"><option value="Research collaboration" data-k="research">Research collaboration</option><option value="Partnership" data-k="partner">Partnership</option><option value="Careers" data-k="careers">Careers</option><option value="Investor relations" data-k="investor">Investor relations</option><option value="Press" data-k="press">Press</option><option value="Something else" data-k="other">Something else</option></select></label>
        <label>Message<textarea name="message" rows="6" required maxlength="5000"></textarea></label>
        <label>Human check: what is <b id="hc-q">…</b>?<input name="human" inputmode="numeric" pattern="[0-9]*" required autocomplete="off" style="max-width:8rem"></label>
        <button class="btn primary" type="submit"><span class="arrow">Send</span></button>
      </form>
      <h2 id="investors">Investors</h2>
      <p>We share information about the company only with qualified investors, under a non-disclosure agreement. Nothing on this site is an offer of securities.</p>
    </div>
  </article>
  <nav class="rail" aria-label="On this page"><h4>On this page</h4><a href="#write">Write to us</a><a href="#investors">Investors</a></nav>
</main>
<script>
(function(){{var f=document.getElementById('contact-form'),q=new URLSearchParams(location.search);
var t=q.get('topic'),o=t&&f.topic.querySelector('option[data-k="'+t+'"]');if(o)o.selected=true;
var msgs={{check:'The human check answer was not right. Please try the new sum.',fields:'Please fill in your name, a valid email and a message.',limit:'Too many messages from this browser. Please try again later, or email us directly.',send:'Sorry, the message could not be sent. Please email us directly.'}};
var err=q.get('error'),box=document.getElementById('form-error');if(err&&msgs[err]){{box.textContent=msgs[err];box.hidden=false;}}
fetch('/contact/challenge.php',{{cache:'no-store',credentials:'same-origin'}}).then(function(r){{return r.json();}}).then(function(d){{document.getElementById('hc-q').textContent=d.q;}}).catch(function(){{document.getElementById('hc-q').textContent='(unavailable, please email us)';}});
}})();
</script>
""" + footer()
write("/contact/", contact)


write("/contact/thanks/", head("Thank you", "Your message has been sent to Heleospace.", "/contact/thanks/") + header("/contact/") + page_hero(
    "Contact", "Thank you. Your message is on its way.", "We read every message and will reply from {0}.".format(CONTACT), M["cities"], "Earth at night from the ISS · NASA",
    '<div class="btns"><a class="btn primary" href="/">Back to home</a><a class="btn" href="/updates/">Latest updates</a></div>') + "<main id='main'></main>" + footer())
# ---------------- LEGAL / CREDITS ----------------
legal_body = f"""
<h2 id="notice">Not an offer</h2>
<p>Information on this site is provided for general information about Heleospace and its research. It is not an offer to sell, or a solicitation of an offer to buy, any security or other financial instrument, and must not be relied on in making an investment decision. Roadmaps, figures and timelines describe plans and targets, which may change.</p>
<h2 id="privacy">Privacy</h2>
<p>This site stores no form data itself. Messages sent through the contact form are emailed directly to our inbox from our own server and are not stored on this site. Fonts are loaded from Google Fonts, and some images and video are loaded from NASA and Unsplash servers, which receive your IP address when they serve them. Questions: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
<h2 id="cookies">Cookies and analytics</h2>
<p>With your consent, we use Google Analytics 4 to understand how visitors use this site, for example which pages are read and how people arrive. Google Analytics sets cookies (such as _ga) and sends usage data, including a shortened IP address, device and browser information, to Google. We use it only to improve the site, not for advertising, and we do not combine it with other data.</p>
<p>Google Analytics loads only if you choose "Accept" in the cookie banner. If you choose "Deny", no analytics cookies are set. We remember your choice in your browser's local storage for 12 months. You can change it at any time through <a href="#" data-cookie-settings>Cookie settings</a>, and you can delete cookies in your browser settings. Google's own policy is at <a href="https://policies.google.com/privacy" rel="noopener">policies.google.com/privacy</a>.</p>
<h2 id="marks">Trademarks</h2>
<p>Heleospace, Heleo and Heleo Mesh are names used by Heleospace LLC. NASA imagery is used under NASA's media guidelines and does not imply NASA endorsement.</p>
"""
write("/legal/", head("Legal & privacy", "Legal notice and privacy for heleo.space.", "/legal/") + header("/legal/")
      + """<div style="height:var(--header-h)"></div>""" + article("<h1 class='display' style='font-size:clamp(2.2rem,4.6vw,3.6rem);margin-bottom:48px'>Legal &amp; privacy</h1>" + legal_body,
      [("notice", "Not an offer"), ("privacy", "Privacy"), ("cookies", "Cookies"), ("marks", "Trademarks")], '<a class="btn" href="/contact/">Contact</a>') + footer())

CREDITS = [
  ("Earth's limb with clouds, HD Earth Views (home hero video)", "NASA Scientific Visualization Studio / ISS and Space Shuttle crews", "Public domain (NASA)", "https://svs.gsfc.nasa.gov/10766"),
  ("Artemis II liftoff from Banana Creek (home hero video; trimmed, mirrored and darkened)", "NASA", "NASA media usage guidelines", "https://images.nasa.gov/details/KSC-20260401-MH-CSH01-0002-Artemis_II_Launch_Banana_Creek-M19183.mp4"),
  ("ISS stills: aurora, star trails, city lights", "NASA Scientific Visualization Studio / ISS crew", "Public domain (NASA)", "https://svs.gsfc.nasa.gov/11474"),
  ("Orbital sunrise, iss066e152098", "NASA", "Public domain (NASA)", "https://www.nasa.gov/image-article/first-rays-of-an-orbital-sunrise-illuminate-earths-atmosphere-4"),
  ("The sun's first rays above Earth's limb, iss059e027932", "NASA", "Public domain (NASA)", "https://www.nasa.gov/image-detail/the-suns-first-rays-peek-above-earths-limb-46976234625-o"),
  ("Station solar arrays across Earth's horizon, iss065e049854", "NASA", "Public domain (NASA)", "https://www.nasa.gov/image-article/stations-solar-arrays-drape-across-earths-horizon"),
  ("Earth at night", "NASA, via Unsplash", "Unsplash License", "https://unsplash.com/photos/photo-of-outer-space-Q1p7bh3SHj8"),
  ("Highway at night, long exposure (Machines hero)", "Akin Cakiner, Unsplash", "Unsplash License", "https://unsplash.com/photos/a-long-exposure-photo-of-a-highway-at-night-ewPvwRx7ub8"),
  ("City light trails at night", "Richard Horne, Unsplash", "Unsplash License", "https://unsplash.com/photos/a-long-exposure-photo-of-a-city-at-night-Lr201W3WbTE"),
  ("Robonaut 2 aboard the ISS, ISS036-E-013254", "NASA", "Public domain (NASA)", "https://www.nasa.gov/image-detail/robonaut-2-2"),
  ("Astrobee free-flying robot aboard the ISS, iss071e046284", "NASA", "Public domain (NASA)", "https://images.nasa.gov/details/iss071e046284"),
  ("Desert and snowy mountains from orbit, HD Earth Views", "NASA Scientific Visualization Studio", "Public domain (NASA)", "https://svs.gsfc.nasa.gov/10766"),
  ("Cable network", "Taylor Vick, Unsplash", "Unsplash License", "https://unsplash.com/photos/cable-network-M5tzZtFCOfs"),
  ("Server room aisle", "İsmail Enes Ayhan, Unsplash", "Unsplash License", "https://unsplash.com/photos/server-room-aisle-with-metal-equipment-racks-lVZjvw-u9V8"),
]
rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td><a href="{d}" rel="noopener">Source</a></td></tr>' for a, b, c, d in CREDITS)
write("/credits/", head("Image credits", "Credits for photos and video on heleo.space.", "/credits/") + header("/credits/")
      + """<div style="height:var(--header-h)"></div>""" + article(f"<h1 class='display' style='font-size:clamp(2.2rem,4.6vw,3.6rem);margin-bottom:48px'>Image credits</h1><h2 id='list'>Photos and video</h2><p>All media on this site are real photographs and footage, used under public-domain or free licences. NASA material does not imply NASA endorsement.</p><div class='table-wrap'><table><tr><th>Media</th><th>By</th><th>Licence</th><th></th></tr>{rows}</table></div>",
      [("list", "Photos and video")], '<a class="btn" href="/">Home</a>') + footer())

# ---------------- BRAND KIT ----------------
KIT = "/assets/brand/heleospace-"
LOGO_BLACK, LOGO_WHITE = KIT + "logo-black.svg", KIT + "logo-white.svg"

def bk_head(id_, num, title, text):
    return f'<div class="bk-head" id="{id_}"><div><span class="bk-num">{num}</span><h2 class="display">{title}</h2></div><p>{text}</p></div>'

def bk_file(name, title, use, tone):
    def dl(ext):
        return f'<a class="bk-dl" href="{KIT}{name}.{ext}" download aria-label="Download {title.lower()} as {ext.upper()}">{ext.upper()}</a>'
    return f"""<article class="bk-card">
  <div class="bk-stage {tone}"><img src="{KIT}{name}.svg" alt="{title}" class="{'bk-mark' if name.startswith('mark') else 'bk-logo'}"></div>
  <div class="bk-card-text"><div><h3>{title}</h3><p>{use}</p></div><div class="bk-dls">{dl('svg')}{dl('png')}</div></div>
</article>"""

def bk_bg(tone, src, label, style=""):
    return f'<figure class="bk-tile"><div class="bk-stage {tone}"{style}><img class="bk-logo" src="{src}" alt="Heleospace logo on {label.lower()}"></div><figcaption>{label}</figcaption></figure>'

def bk_no(art, label, tone="on-white"):
    return f'<figure class="bk-tile bk-no"><div class="bk-stage {tone}">{art}</div><figcaption><span aria-hidden="true">✕</span> {label}</figcaption></figure>'

def bk_swatch(name, hex_, use, tone=""):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    return f'<div class="bk-swatch"><div class="chip {tone}" style="background:{hex_}"></div><h3>{name}</h3><dl><dt>HEX</dt><dd>{hex_}</dd><dt>RGB</dt><dd>{r} {g} {b}</dd></dl><p>{use}</p></div>'

# Clear space diagram: the logo is 640 wide, so its mark is 92.8 tall and x is 46.4.
BK_CLEAR = f"""<svg class="bk-clear" viewBox="0 0 900 300" role="img" aria-label="The Heleospace logo inside a dashed boundary. The space on every side equals x, which is half the height of the mark.">
<rect x="83.6" y="54.6" width="732.8" height="190.8" fill="none" stroke="#C2421F" stroke-width="1.5" stroke-dasharray="6 6"/>
<rect x="130" y="101" width="640" height="97.6" fill="none" stroke="#C2421F" stroke-opacity=".45"/>
<g fill="#C2421F" fill-opacity=".14"><rect x="83.6" y="54.6" width="46.4" height="46.4"/><rect x="770" y="54.6" width="46.4" height="46.4"/><rect x="83.6" y="198.6" width="46.4" height="46.8"/><rect x="770" y="198.6" width="46.4" height="46.8"/></g>
<g fill="#C2421F" font-family="Archivo, Arial, sans-serif" font-size="24" text-anchor="middle"><text x="106.8" y="86">x</text><text x="793.2" y="86">x</text><text x="106.8" y="230">x</text><text x="793.2" y="230">x</text></g>
<image href="{LOGO_BLACK}" x="130" y="101" width="640" height="97.55"/>
</svg>"""

bk_body = f"""<main id="main" class="bk">
<section class="section tight"><div class="wrap">
  {bk_head("files", "01", "Logo files", "Use these official files and do not redraw the logo. SVG suits screens and print at any size. PNG files have transparent backgrounds, for tools that do not accept SVG.")}
  <div class="bk-grid two">
    {bk_file("logo-black", "Black logo", "The default, for white and light backgrounds.", "on-white")}
    {bk_file("logo-white", "White logo", "For black, dark and dark photographic backgrounds.", "on-night")}
    {bk_file("mark-black", "Black mark", "For avatars, app icons and other small or square spaces.", "on-white")}
    {bk_file("mark-white", "White mark", "The same uses, on dark backgrounds.", "on-night")}
  </div>
  <p class="bk-all"><a class="btn primary" href="{KIT}brand-kit.zip" download><span class="arrow">Download all files (ZIP)</span></a></p>
</div></section>

<section class="section tight surface"><div class="wrap">
  {bk_head("clear-space", "02", "Clear space", "Keep the space around the logo free of text, images and page edges. On every side, leave at least x, which is half the height of the mark.")}
  <div class="bk-panel">{BK_CLEAR}</div>
</div></section>

<section class="section tight"><div class="wrap">
  {bk_head("minimum-size", "03", "Minimum size", "Below these sizes the logo loses its detail. When the full logo will not fit, use the mark on its own. Shown here at actual size on a standard screen.")}
  <div class="bk-grid two">
    <div class="bk-size"><div class="bk-stage on-white"><img src="{LOGO_BLACK}" alt="Full logo at its minimum size" width="120"></div><h3>Full logo</h3><p>120 px wide on screen, 25 mm wide in print.</p></div>
    <div class="bk-size"><div class="bk-stage on-white"><img src="{KIT}mark-black.svg" alt="Mark at its minimum size" width="16"></div><h3>Mark</h3><p>16 px wide on screen, 5 mm wide in print.</p></div>
  </div>
</div></section>

<section class="section tight surface"><div class="wrap">
  {bk_head("backgrounds", "04", "Colour and backgrounds", "The logo appears only in black or white. Choose whichever stands out most clearly from the background. On photographs, place it over a calm, even area.")}
  <div class="bk-grid four">
    {bk_bg("on-white", LOGO_BLACK, "White")}
    {bk_bg("on-paper", LOGO_BLACK, "Paper")}
    {bk_bg("on-night", LOGO_WHITE, "Night")}
    {bk_bg("on-photo", LOGO_WHITE, "A dark photograph", f' style="background-image:url({M["sunrise"]});background-size:222%;background-position:84% 66%"')}
  </div>
</div></section>

<section class="section tight"><div class="wrap">
  {bk_head("misuse", "05", "What to avoid", "The logo only stays recognisable if it looks the same everywhere. Please do not change the files in any of these ways.")}
  <div class="bk-grid three">
    {bk_no(f'<img class="bk-logo" src="{LOGO_BLACK}" alt="" style="transform:scale(1.25,.6)">', "Do not stretch or squash it")}
    {bk_no(f'<img class="bk-logo" src="{LOGO_BLACK}" alt="" style="transform:rotate(-10deg)">', "Do not rotate it")}
    {bk_no('<span class="bk-recolour" role="presentation"></span>', "Do not recolour it")}
    {bk_no(f'<img class="bk-logo" src="{LOGO_BLACK}" alt="" style="filter:drop-shadow(0 7px 4px rgba(0,0,0,.55))">', "Do not add shadows or effects")}
    {bk_no(f'<img class="bk-logo" src="{LOGO_BLACK}" alt="">', "Do not use it on a low-contrast background", "on-low")}
    {bk_no(f'<span class="bk-retype"><img src="{KIT}mark-black.svg" alt="">Heleospace</span>', "Do not retype the name in another font")}
  </div>
</div></section>

<section class="section tight surface"><div class="wrap">
  {bk_head("palette", "06", "Colour palette", "These are the colours of the Heleospace website, for materials that sit alongside the logo. They do not apply to the logo itself.")}
  <div class="bk-grid three">
    {bk_swatch("Night", "#07080A", "Dark backgrounds.")}
    {bk_swatch("Ink", "#111214", "Headings and text on light backgrounds.")}
    {bk_swatch("Paper", "#F4F2ED", "Light backgrounds.", "line")}
    {bk_swatch("Sun", "#FFF3DC", "Headings and text on dark backgrounds.", "line")}
    {bk_swatch("Coral", "#FF5E3A", "The accent on dark backgrounds.")}
    {bk_swatch("Ember", "#C2421F", "The accent on light backgrounds, including links.")}
  </div>
</div></section>

<section class="section tight"><div class="wrap">
  {bk_head("typography", "07", "Typography", "Both typefaces are free under the SIL Open Font License. The logo itself is drawn artwork, so always use the files rather than typing the name in a font.")}
  <div class="bk-grid two">
    <div class="bk-type"><p class="bk-type-a">Archivo</p><h3>Headings and interface</h3><p>Use a light weight and an expanded width for large headings. <a href="https://fonts.google.com/specimen/Archivo" rel="noopener">Get Archivo</a></p></div>
    <div class="bk-type"><p class="bk-type-n">Newsreader</p><h3>Reading text</h3><p>Use a regular weight for paragraphs and longer articles. <a href="https://fonts.google.com/specimen/Newsreader" rel="noopener">Get Newsreader</a></p></div>
  </div>
</div></section>

<section class="section tight surface"><div class="wrap">
  {bk_head("name", "08", "Writing about us", "Heleospace is one word with a capital H. Please do not write HeleoSpace, Heleo Space or HELEOSPACE.")}
  <div class="table-wrap"><table>
    <tr><th>Name</th><th>What it refers to</th></tr>
    <tr><td>Heleospace</td><td>The company, in everyday use</td></tr>
    <tr><td>Heleospace LLC</td><td>The legal name, for contracts and formal notices</td></tr>
    <tr><td>Heleo Mesh</td><td>The product: our open software and network. Always two words, never Heleo alone.</td></tr>
    <tr><td>The Autonomous Mesh</td><td>The idea behind Heleo Mesh, from our technical paper</td></tr>
    <tr><td>Heleo-1 to Heleo-4</td><td>The reference satellites</td></tr>
  </table></div>
  <h3 class="bk-sub">Short description</h3>
  <blockquote class="bk-quote">Heleospace builds orbital data centers that run as an autonomous economy: compute in orbit and on the ground that finds work, agrees a price and settles on its own.</blockquote>
</div></section>

<section class="section tight"><div class="wrap">
  {bk_head("terms", "09", "Terms of use", "The Heleospace name and logo belong to Heleospace LLC, which keeps all rights in them.")}
  <div class="bk-grid two bk-terms">
    <div><h3>You may</h3><ul><li>Use the unmodified logo to refer to Heleospace or its work, for example in articles, reports, talks and directories.</li><li>Link the logo to <a href="https://heleo.space/">heleo.space</a>.</li></ul></div>
    <div><h3>Without our written permission, you may not</h3><ul><li>Use the name or logo in a way that suggests we sponsor, endorse or work with you.</li><li>Use them on merchandise or anything you sell.</li><li>Use them, or anything similar, in your own name, logo, product or domain.</li></ul></div>
  </div>
  <p class="bk-note">We may ask you to change or stop a use of the name or logo. For permission, or for a format that is not here, write to <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
  <p class="meta">Brand kit version 1.0, November 2026</p>
</div></section>
</main>
"""
write("/brand/", head("Brand kit", "Official Heleospace logo files, with guidelines for using the logo, colours, typefaces and name.", "/brand/") + header("/brand/")
      + page_hero("Brand kit", "The Heleospace logo, and how to use it", "Official logo files and simple guidelines for press, partners and anyone writing about our work.", M["first_rays"], "Orbital sunrise from the ISS · NASA",
                  f'<div class="btns"><a class="btn primary" href="{KIT}brand-kit.zip" download><span class="arrow">Download all files</span></a><a class="btn" href="#clear-space">Read the guidelines</a></div>')
      + bk_body + footer())

# 404
write("/404.html", head("Page not found", "This page does not exist.", "/404.html") + header("/x") + page_hero("404", "Lost in orbit", "This page does not exist. It may have moved.", M["startrails"], "Star trails from the ISS · NASA", '<div class="btns"><a class="btn primary" href="/">Home</a><a class="btn" href="/updates/">Updates</a></div>') + "<main id='main'></main>" + footer())
print("built", OUT)
