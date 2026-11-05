/* Heleospace · heleo.space — header, menu, reveal, hero video, and the Updates feed.
   Updates: every post is a Markdown file in /updates/posts/. List it in /updates/posts.json. */
(function () {
  var header = document.querySelector('.site-header');
  var nightHero = document.querySelector('.hero, .page-hero');

  function onScroll() {
    if (!header) return;
    var limit = nightHero ? nightHero.offsetHeight - 80 : 10;
    header.classList.toggle('is-solid', window.scrollY > Math.max(limit, 10));
  }
  if (header && nightHero) header.classList.add('over-night');
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) menuBtn.addEventListener('click', function () {
    var open = header.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.textContent = open ? 'Close' : 'Menu';
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // Reveal on scroll
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' }) : null;
  document.querySelectorAll('.reveal').forEach(function (el) { io ? io.observe(el) : el.classList.add('in'); });

  // Hero video: pause control, and respect reduced motion
  var vid = document.querySelector('.hero video');
  var vbtn = document.querySelector('[data-video-toggle]');
  if (vid) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { vid.removeAttribute('autoplay'); vid.pause(); if (vbtn) vbtn.textContent = 'Play video'; }
    if (vbtn) vbtn.addEventListener('click', function () {
      if (vid.paused) { vid.play(); vbtn.textContent = 'Pause video'; } else { vid.pause(); vbtn.textContent = 'Play video'; }
    });
  }

  // Right rail: highlight current section
  var railLinks = document.querySelectorAll('.rail a');
  if (railLinks.length && io) {
    var map = {};
    railLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { railLinks.forEach(function (a) { a.classList.remove('on'); }); var a = map[e.target.id]; if (a) a.classList.add('on'); } });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) rio.observe(el); });
  }

  // ---------- Updates ----------
  var ROOT = (document.documentElement.getAttribute('data-root') || '/').replace(/\/?$/, '/');
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmtDate(d) { try { return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { return d; } }
  function parse(md) {
    var m = md.match(/^---\s*\n([\s\S]*?)\n---\s*\n?([\s\S]*)$/);
    var meta = {}, body = md;
    if (m) { body = m[2]; m[1].split('\n').forEach(function (l) { var i = l.indexOf(':'); if (i > 0) meta[l.slice(0, i).trim()] = l.slice(i + 1).trim().replace(/^["']|["']$/g, ''); }); }
    return { meta: meta, body: body };
  }
  function loadPosts() {
    return fetch(ROOT + 'updates/posts.json', { cache: 'no-cache' }).then(function (r) { return r.json(); })
      .then(function (list) {
        return Promise.all(list.map(function (slug) {
          return fetch(ROOT + 'updates/posts/' + slug + '.md', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.text() : null; })
            .then(function (t) { if (!t) return null; var p = parse(t); p.slug = slug; return p; });
        }));
      }).then(function (ps) { return ps.filter(Boolean).filter(function (p) { return p.meta.draft !== 'true'; }).sort(function (a, b) { return (b.meta.date || '').localeCompare(a.meta.date || ''); }); });
  }
  function card(p) {
    var img = p.meta.image ? '<figure class="media"><img loading="lazy" src="' + esc(p.meta.image) + '" alt="' + esc(p.meta.image_alt || '') + '"></figure>' : '';
    return '<a class="post-card reveal in" href="' + ROOT + 'updates/post.html?p=' + encodeURIComponent(p.slug) + '">' + img +
      '<div><span class="tag">' + esc(p.meta.category || 'Update') + '</span><time datetime="' + esc(p.meta.date) + '">' + esc(fmtDate(p.meta.date)) + '</time></div>' +
      '<h3>' + esc(p.meta.title) + '</h3><p>' + esc(p.meta.summary || '') + '</p></a>';
  }
  var feed = document.querySelector('[data-posts]');
  if (feed) {
    var limit = parseInt(feed.getAttribute('data-posts'), 10) || 0;
    loadPosts().then(function (ps) {
      if (limit) ps = ps.slice(0, limit);
      feed.innerHTML = ps.length ? ps.map(card).join('') : '<p class="posts-empty">No updates yet.</p>';
    }).catch(function () { feed.innerHTML = '<p class="posts-empty">Updates load when the site is served from a web server.</p>'; });
  }
  var single = document.querySelector('[data-post]');
  if (single) {
    var slug = new URLSearchParams(location.search).get('p');
    if (!slug || !/^[a-z0-9-]+$/.test(slug)) { single.innerHTML = '<p>Update not found. <a href="' + ROOT + 'updates/">See all updates</a>.</p>'; }
    else fetch(ROOT + 'updates/posts/' + slug + '.md', { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw 0; return r.text(); }).then(function (t) {
      var p = parse(t);
      document.title = p.meta.title + ' · Heleospace';
      var d = document.querySelector('meta[name="description"]'); if (d && p.meta.summary) d.setAttribute('content', p.meta.summary);
      var html = window.marked ? window.marked.parse(p.body) : '<pre>' + esc(p.body) + '</pre>';
      if (window.DOMPurify) html = window.DOMPurify.sanitize(html);
      single.innerHTML =
        '<p class="eyebrow"><a href="' + ROOT + 'updates/" style="text-decoration:none">Updates</a>&nbsp;·&nbsp;' + esc(p.meta.category || 'Update') + '</p>' +
        '<h1 class="display" style="font-size:clamp(2.2rem,4.6vw,3.8rem);max-width:18ch">' + esc(p.meta.title) + '</h1>' +
        (p.meta.summary ? '<p class="standfirst" style="margin-top:24px">' + esc(p.meta.summary) + '</p>' : '') +
        (p.meta.image ? '<figure class="media" style="aspect-ratio:16/9;margin:0 0 40px"><img src="' + esc(p.meta.image) + '" alt="' + esc(p.meta.image_alt || '') + '"></figure>' : '') +
        '<div class="body">' + html + '</div>' +
        '<p class="meta">' + esc(fmtDate(p.meta.date)) + (p.meta.author ? ' · ' + esc(p.meta.author) : '') + (p.meta.image_credit ? ' · Image: ' + esc(p.meta.image_credit) : '') + '</p>' +
        '<div class="cta"><a class="btn" href="' + ROOT + 'updates/"><span>All updates</span></a></div>';
    }).catch(function () { single.innerHTML = '<p>Update not found. <a href="' + ROOT + 'updates/">See all updates</a>.</p>'; });
  }

  var y = document.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();
})();

/* ---------- Cookie consent + Google Analytics 4 ----------
   GA loads only after the visitor clicks Accept. Choice kept 12 months in localStorage. */
(function () {
  var GA = document.documentElement.getAttribute('data-ga') || '';
  if (!/^G-[A-Z0-9]+$/.test(GA) || GA === 'G-XXXXXXXXXX') { document.querySelectorAll('[data-cookie-settings]').forEach(function (a) { a.style.display = 'none'; }); return; }
  var KEY = 'heleo-consent', YEAR = 365 * 864e5;
  function read() { try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); return v && Date.now() - v.t < YEAR ? v.c : null; } catch (e) { return null; } }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); } catch (e) {} }
  var loaded = false;
  function loadGA() {
    if (loaded) return; loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted' });
    gtag('config', GA, { anonymize_ip: true, allow_google_signals: false, allow_ad_personalization_signals: false });
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA); document.head.appendChild(s);
  }
  function clearGA() {
    document.cookie.split(';').forEach(function (c) { var n = c.split('=')[0].trim(); if (/^_ga/.test(n)) { ['', '; domain=' + location.hostname, '; domain=.' + location.hostname.replace(/^www\./, '')].forEach(function (d) { document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d; }); } });
  }
  var bar;
  function show() {
    if (bar) { bar.hidden = false; return; }
    bar = document.createElement('div');
    bar.className = 'consent'; bar.setAttribute('role', 'dialog'); bar.setAttribute('aria-live', 'polite'); bar.setAttribute('aria-label', 'Cookie consent');
    bar.innerHTML = '<p>We use cookies to understand how this site is used, only if you agree. <a href="/legal/#cookies">Learn more</a>.</p>' +
      '<div class="consent-btns"><button type="button" class="btn" data-c="deny">Deny</button><button type="button" class="btn primary" data-c="accept">Accept</button></div>';
    document.body.appendChild(bar);
    bar.addEventListener('click', function (e) {
      var c = e.target.closest('[data-c]'); if (!c) return;
      var ok = c.getAttribute('data-c') === 'accept';
      save(ok ? 'accept' : 'deny'); bar.hidden = true;
      if (ok) loadGA(); else if (loaded) { clearGA(); location.reload(); } else clearGA();
    });
  }
  var choice = read();
  if (choice === 'accept') loadGA(); else if (choice !== 'deny') show();
  document.addEventListener('click', function (e) { var a = e.target.closest('[data-cookie-settings]'); if (a) { e.preventDefault(); show(); } });
})();

/* grouped navigation: click/tap to open, Escape or outside click to close */
(function () {
  var groups = document.querySelectorAll('.nav-group');
  function closeAll(except) { groups.forEach(function (g) { if (g !== except) { g.classList.remove('open'); var b = g.querySelector('.nav-top'); if (b) b.setAttribute('aria-expanded', 'false'); } }); }
  groups.forEach(function (g) {
    var btn = g.querySelector('.nav-top');
    btn.addEventListener('click', function (e) { e.stopPropagation(); var open = !g.classList.contains('open'); closeAll(g); g.classList.toggle('open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false'); });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.nav-group')) closeAll(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
})();
