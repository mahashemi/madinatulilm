/* ═══════════════════════════════════════════════════════════
   Madrasah Madinatul Ilm — Main JavaScript
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Navbar: shrink on scroll ── */
  const navbar = document.querySelector('.main-navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
      navbar && navbar.classList.add('navbar-scrolled');
    } else {
      navbar && navbar.classList.remove('navbar-scrolled');
    }
  });

  /* ── Back-to-top button ── */
  const topBtn = document.createElement('button');
  topBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
  topBtn.className = 'back-to-top';
  topBtn.setAttribute('aria-label', 'Back to top');
  document.body.appendChild(topBtn);

  window.addEventListener('scroll', () => {
    topBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
  });
  topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  /* ── Bootstrap tooltips ── */
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(el => new bootstrap.Tooltip(el));

  /* ── Auto-dismiss alerts ── */
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert && bsAlert.close();
    }, 5000);
  });

  /* ── Active nav highlight (current URL) ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  /* ── Gallery lightbox placeholder ── */
  document.querySelectorAll('.gallery-thumb').forEach(thumb => {
    thumb.addEventListener('click', e => {
      if (thumb.getAttribute('href') && thumb.getAttribute('href').match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
        e.preventDefault();
        const src = thumb.getAttribute('href');
        const alt = thumb.querySelector('img') ? thumb.querySelector('img').alt : '';
        openLightbox(src, alt);
      }
    });
  });

  function openLightbox(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'lightbox-overlay';
    modal.innerHTML = `
      <div class="lightbox-inner">
        <button class="lightbox-close" aria-label="Close">&times;</button>
        <img src="${src}" alt="${alt}" class="lightbox-img">
        ${alt ? `<p class="lightbox-caption">${alt}</p>` : ''}
      </div>`;
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    modal.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
    modal.addEventListener('click', e => { if (e.target === modal) closeLightbox(); });

    function closeLightbox() {
      modal.remove();
      document.body.style.overflow = '';
    }

    document.addEventListener('keydown', function escClose(e) {
      if (e.key === 'Escape') { closeLightbox(); document.removeEventListener('keydown', escClose); }
    });
  }

});

/* ── Lightbox & Back-to-top styles (injected) ── */
(function injectStyles() {
  const style = document.createElement('style');
  style.textContent = `
    .navbar-scrolled { padding: 0.25rem 0 !important; box-shadow: 0 4px 30px rgba(0,0,0,0.35) !important; }

    .back-to-top {
      position: fixed; bottom: 28px; right: 28px;
      width: 44px; height: 44px; border-radius: 50%;
      background: var(--gold); color: #fff; border: none;
      cursor: pointer; display: none; align-items: center;
      justify-content: center; font-size: 1rem; z-index: 999;
      box-shadow: 0 4px 18px rgba(201,168,76,0.45);
      transition: background 0.2s, transform 0.2s;
    }
    .back-to-top:hover { background: var(--gold-dark); transform: translateY(-3px); }

    .lightbox-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.88);
      z-index: 9999; display: flex; align-items: center;
      justify-content: center; padding: 1rem;
    }
    .lightbox-inner { position: relative; max-width: 90vw; max-height: 90vh; text-align: center; }
    .lightbox-img { max-width: 100%; max-height: 80vh; border-radius: 8px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    .lightbox-caption { color: #ddd; margin-top: 0.75rem; font-size: 0.9rem; }
    .lightbox-close {
      position: absolute; top: -14px; right: -14px;
      width: 36px; height: 36px; border-radius: 50%;
      background: var(--gold); color: #fff; border: none;
      font-size: 1.3rem; cursor: pointer; line-height: 1;
      display: flex; align-items: center; justify-content: center;
    }
  `;
  document.head.appendChild(style);
})();

/* ══════════════════════════════════════
   LANGUAGE SWITCHER
   Custom pure-JS toggle — no Bootstrap dropdown required
══════════════════════════════════════ */
(function () {
  var LANGS    = { en: 'EN', ar: 'AR', ur: 'UR', fa: 'FA' };
  var RTL_LANGS = ['ar', 'ur', 'fa'];
  var htmlEl   = document.getElementById('html-root');
  var labelEl  = document.getElementById('lang-label');
  var switcher = document.getElementById('langSwitcher');
  var btn      = document.getElementById('langBtn');

  /* Toggle open/close */
  if (btn && switcher) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      switcher.classList.toggle('open');
      btn.setAttribute('aria-expanded', switcher.classList.contains('open') ? 'true' : 'false');
    });
    document.addEventListener('click', function () {
      if (switcher.classList.contains('open')) {
        switcher.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* Apply a language */
  function applyLang(lang) {
    if (!LANGS[lang]) lang = 'en';
    localStorage.setItem('mil_lang', lang);
    if (labelEl) labelEl.textContent = LANGS[lang];

    if (RTL_LANGS.indexOf(lang) !== -1) {
      htmlEl && htmlEl.setAttribute('dir', 'rtl');
      htmlEl && htmlEl.setAttribute('lang', lang);
    } else {
      htmlEl && htmlEl.setAttribute('dir', 'ltr');
      htmlEl && htmlEl.setAttribute('lang', 'en');
    }

    document.querySelectorAll('.lang-option').forEach(function (el) {
      el.classList.toggle('active-lang', el.dataset.lang === lang);
    });

    if (switcher) {
      switcher.classList.remove('open');
      btn && btn.setAttribute('aria-expanded', 'false');
    }

    /* ── Render JSON-driven page content (home page sections) ── */
    renderPageContent(lang);

    document.dispatchEvent(new CustomEvent('milLangChange', { detail: lang }));
  }

    /* ══════════════════════════════════════════════════════
     UNIVERSAL PAGE LANGUAGE RENDERER
     Handles EVERY page. Two mechanisms work together:

     1. data-lang-* attributes on any element:
        <h2 data-lang-en="About Us" data-lang-ar="من نحن" ...>About Us</h2>
        → textContent is swapped to the active language.

     2. data-html-lang-* attributes for rich HTML bodies:
        <div data-html-lang-en="<p>…</p>" data-html-lang-ar="<p>…</p>">…</div>
        → innerHTML is swapped.

     3. Explicit mil-* id elements on the home page (existing behaviour).
  ══════════════════════════════════════════════════════ */
  function renderPageContent(lang) {
    var RTL = ['ar', 'ur', 'fa'];
    var isRtl = RTL.indexOf(lang) !== -1;
    var rtlBodyStyle = isRtl
      ? 'font-family:"Amiri",serif;direction:rtl;text-align:right;font-size:1.05rem;line-height:2;'
      : '';
    var rtlInlineStyle = isRtl ? 'font-family:"Amiri",serif;direction:rtl;' : '';

    /* ── 1. Plain-text lang swap: data-lang-en / data-lang-ar / … ── */
    document.querySelectorAll('[data-lang-en]').forEach(function(el) {
      var val = el.getAttribute('data-lang-' + lang) || el.getAttribute('data-lang-en') || '';
      el.textContent = val;
      /* apply RTL style only to elements that have an RTL variant */
      if (el.getAttribute('data-lang-ar') || el.getAttribute('data-lang-ur') || el.getAttribute('data-lang-fa')) {
        el.style.cssText = isRtl ? rtlInlineStyle : '';
      }
    });

    /* ── 1b. js-lang-hide-en: visible only when language ≠ EN ──────
       Used for Arabic/Urdu script names that should not appear when
       English is the active language.
       Also switches text content via data-lang-* if present.
    ── */
    document.querySelectorAll('.js-lang-hide-en').forEach(function(el) {
      if (lang === 'en') {
        el.style.display = 'none';
      } else {
        el.style.display = '';
        /* Swap text if the element carries data-lang-* attributes */
        var val = el.getAttribute('data-lang-' + lang) || el.getAttribute('data-lang-ur') || '';
        if (val) {
          el.textContent = val;
          el.style.cssText = 'font-family:"Amiri",serif;direction:rtl;';
        }
      }
    });

    /* ── 2. Rich HTML lang swap: data-html-lang-en / data-html-lang-ar / … ── */
    document.querySelectorAll('[data-html-lang-en]').forEach(function(el) {
      var html = el.getAttribute('data-html-lang-' + lang) || el.getAttribute('data-html-lang-en') || '';
      el.innerHTML = html;
      el.style.cssText = isRtl ? rtlBodyStyle : '';
    });

    /* ── 3. Home page explicit elements (page-content-data JSON) ── */
    var scriptEl = document.getElementById('page-content-data');
    if (scriptEl) {
      var data;
      try { data = JSON.parse(scriptEl.textContent); } catch(e) { data = null; }
      if (data) {
        function pick(obj, field) {
          return (obj && (obj[field + '_' + lang] || obj[field + '_en'])) || '';
        }

        /* Hero name */
        var heroName = document.getElementById('mil-hero-name');
        if (heroName) {
          var nameMap = { en:'Madrasah Madinatul Ilm', ar:'مدرسة مدينة العلم', ur:'مدرسہ مدینۃ العلم', fa:'مدرسه مدینةالعلم' };
          heroName.textContent = nameMap[lang] || nameMap.en;
          heroName.style.cssText = isRtl ? 'font-family:"Amiri",serif;direction:rtl;font-size:2.6rem;' : '';
        }

        /* Hero subtitle */
        var subtitleMap = { en:'Centre of Faqāhat — Governed by Muhammadiyah Trust', ar:'مركز الفقاهة — تحت إشراف المحمدية تراست', ur:'مرکزِ فقاہت — محمدیہ ٹرسٹ کے زیرِ نگرانی', fa:'مرکز فقاهت — زیر نظر محمدیه تراست' };
        var heroSub = document.getElementById('mil-hero-subtitle');
        if (heroSub) { heroSub.textContent = subtitleMap[lang] || subtitleMap.en; heroSub.style.cssText = rtlInlineStyle; }

        /* Hero tagline */
        var heroTagline = document.getElementById('mil-hero-tagline');
        if (heroTagline) {
          var tmp = document.createElement('div'); tmp.innerHTML = pick(data.welcome, 'body');
          var words = (tmp.textContent || '').replace(/\s+/g,' ').trim().split(' ');
          heroTagline.textContent = words.slice(0,25).join(' ') + (words.length>25?'…':'');
          heroTagline.style.cssText = rtlInlineStyle;
        }

        /* Hero buttons */
        var btnLabels = { about:{en:'About Us',ar:'من نحن',ur:'ہمارے بارے میں',fa:'درباره ما'}, lessons:{en:'Explore Lessons',ar:'استكشف الدروس',ur:'اسباق دیکھیں',fa:'بررسی درس‌ها'} };
        var btnA = document.getElementById('mil-btn-about');    if (btnA) btnA.textContent = btnLabels.about[lang]   || btnLabels.about.en;
        var btnL = document.getElementById('mil-btn-lessons');  if (btnL) btnL.textContent = btnLabels.lessons[lang] || btnLabels.lessons.en;

        /* Welcome / Mission / Vision (mil-* ids) */
        function setId(id, text, html) {
          var el = document.getElementById(id);
          if (!el) return;
          if (html !== undefined) { el.innerHTML = html; el.style.cssText = html ? rtlBodyStyle : ''; }
          else                    { el.textContent = text; el.style.cssText = text ? rtlInlineStyle : ''; }
        }
        setId('mil-welcome-title', pick(data.welcome, 'title'));
        setId('mil-welcome-body',  undefined, pick(data.welcome, 'body'));
        setId('mil-mission-title', pick(data.mission, 'title'));
        setId('mil-mission-body',  undefined, pick(data.mission, 'body'));
        setId('mil-vision-title',  pick(data.vision, 'title'));
        setId('mil-vision-body',   undefined, pick(data.vision, 'body'));
      }
    }

    /* ── 4. Navbar universal labels ── */
    var NAV = {
      'nav-home':          { en:'Home',         ar:'الرئيسية',     ur:'ہوم',           fa:'خانه' },
      'nav-quran':         { en:'Quran',         ar:'القرآن',       ur:'قرآن',           fa:'قرآن' },
      'nav-sharia':        { en:'Sharia Matters',ar:'الشريعة',     ur:'شریعت',          fa:'شریعت' },
      'nav-announcements': { en:'Announcements', ar:'الإعلانات',   ur:'اعلانات',        fa:'اطلاعیه‌ها' },
      'nav-lessons':       { en:'Lessons',       ar:'الدروس',      ur:'اسباق',          fa:'درس‌ها' },
      'nav-books':         { en:'Books & Articles',ar:'الكتب',    ur:'کتب',             fa:'کتاب‌ها' },
      'nav-ask':           { en:'Ask a Scholar', ar:'اسأل عالماً', ur:'عالم سے پوچھیں', fa:'از عالم بپرسید' },
      'nav-partner':       { en:'Be A Partner',  ar:'كن شريكاً',   ur:'شراکت دار بنیں', fa:'شریک باشید' },
      'nav-contact':       { en:'Contact Us',    ar:'اتصل بنا',    ur:'رابطہ کریں',      fa:'تماس' }
    };
    Object.keys(NAV).forEach(function(id) {
      var el = document.getElementById(id);
      if (el) el.textContent = NAV[id][lang] || NAV[id].en;
    });
  }

  /* Restore saved preference on load */
  applyLang(localStorage.getItem('mil_lang') || 'en');

  /* Option click handlers */
  document.querySelectorAll('.lang-option').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      applyLang(this.dataset.lang);
    });
  });
})();
