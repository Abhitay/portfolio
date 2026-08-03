/* Shared behaviour for every page. Each block is guarded, so a page only runs
   what its markup actually contains. Loaded with `defer`, so the DOM is ready. */

/* ---------- Google Analytics ---------- */
/* Self-exclusion: open the site once with ?ga=off to stop this browser being
   counted (it remembers via localStorage); ?ga=on undoes it. Must run before
   config, since gtag reads the disable flag when the page_view fires. */
(function () {
  const flag = new URLSearchParams(location.search).get('ga');
  if (flag === 'off') localStorage.setItem('ga-off', '1');
  if (flag === 'on') localStorage.removeItem('ga-off');
  if (localStorage.getItem('ga-off')) window['ga-disable-G-6V9RNG3QS4'] = true;
})();

window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-6V9RNG3QS4');

/* The three portfolio actions GA can't infer on its own: resume opened, a
   contact link used, a case study opened. Enhanced Measurement (a GA4 dashboard
   toggle) already covers page views, scroll, and outbound/file clicks. */
document.addEventListener('click', (e) => {
  const a = e.target.closest('a');
  if (!a) return;
  if (a.getAttribute('href')?.endsWith('.pdf')) gtag('event', 'resume_open');
  else if (a.closest('.hero-contact, #contact')) gtag('event', 'contact_click', { link_text: a.textContent.trim() });
  else if (a.classList.contains('work-item')) gtag('event', 'case_study_open', { case_study: a.querySelector('h3')?.textContent.trim() });
});

/* ---------- Active nav link ---------- */
(function () {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('nav .right a[href^="#"]');
  if (!sections.length || !navLinks.length) return;

  const highlight = () => {
    let current = '';
    sections.forEach(section => {
      const top = section.offsetTop - 100;
      if (window.scrollY >= top && window.scrollY < top + section.clientHeight) {
        current = section.id;
      }
    });
    navLinks.forEach(link => link.classList.toggle('active', link.getAttribute('href') === `#${current}`));
  };

  window.addEventListener('scroll', highlight, { passive: true });
  highlight();
})();

/* ---------- Mobile nav toggle ---------- */
(function () {
  const navRight = document.querySelector('nav .right');
  const navToggle = document.querySelector('.nav-toggle');
  const navLinksWrap = document.querySelector('.nav-links');
  if (!navRight || !navToggle || !navLinksWrap) return;

  navToggle.addEventListener('click', () => {
    const isOpen = navRight.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navLinksWrap.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navRight.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

/* ---------- Nav hairline: hidden while the hero fills the viewport ----------
   Pages without a full-height hero (the case studies) keep it on permanently. */
(function () {
  const nav = document.querySelector('nav');
  if (!nav) return;

  if (!document.querySelector('.hero-home')) {
    nav.classList.add('scrolled');
    return;
  }

  const setBorder = () => nav.classList.toggle('scrolled', window.scrollY > 12);
  window.addEventListener('scroll', setBorder, { passive: true });
  setBorder();
})();

/* ---------- "Best viewed on desktop" prompt before opening a dense case study ---------- */
(function () {
  const caseStudyLinks = document.querySelectorAll(
    'a[href*="feature-impact.html"], a[href*="growth-allocation.html"], a[href*="ai-insights-copilot.html"], ' +
    'a[href*="hybrid-retrieval-eval-harness.html"], a[href*="human-gated-agent-orchestration.html"], ' +
    'a[href*="semantic-caching-tradeoff.html"], a[href*="finetuned-guarded-text-to-sql.html"]'
  );
  if (!caseStudyLinks.length) return;

  const isMobile = () => window.matchMedia('(max-width: 768px)').matches;
  let pendingHref = null;
  let overlay = null;
  let toast = null;

  const closeToast = () => {
    overlay?.classList.remove('show');
    toast?.classList.remove('show');
    pendingHref = null;
  };

  const ensureToast = () => {
    if (overlay && toast) return;
    overlay = document.createElement('div');
    overlay.className = 'toast-overlay';
    toast = document.createElement('div');
    toast.className = 'toast-banner';
    toast.innerHTML = `
      <div class="toast-title">Best viewed on desktop</div>
      <div class="toast-text">These case studies are easier to read on a larger screen. Continue on mobile?</div>
      <div class="toast-buttons">
        <button class="btn-secondary" type="button" data-toast-cancel>Cancel</button>
        <button class="btn-primary" type="button" data-toast-continue>Continue</button>
      </div>
    `;
    overlay.appendChild(toast);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', e => { if (e.target === overlay) closeToast(); });
    toast.querySelector('[data-toast-cancel]')?.addEventListener('click', closeToast);
    toast.querySelector('[data-toast-continue]')?.addEventListener('click', () => {
      if (pendingHref) window.location.href = pendingHref;
      closeToast();
    });
  };

  caseStudyLinks.forEach(link => {
    link.addEventListener('click', e => {
      if (!isMobile()) return;
      e.preventDefault();
      pendingHref = link.href;
      ensureToast();
      overlay.classList.add('show');
      toast.classList.add('show');
    });
  });
})();

/* ---------- Magnet scroll: the first downward scroll glides the whole hero out
   to the next section in one motion (and snaps back up near the top). ---------- */
(function () {
  const first = document.querySelector('#projects');
  const navEl = document.querySelector('nav');
  const hero = document.querySelector('.hero-home');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!first || !navEl || !hero || reduceMotion) return;

  let animating = false;
  const targetTop = () =>
    Math.max(0, first.getBoundingClientRect().top + window.scrollY - navEl.offsetHeight);

  const glideTo = (y) => {
    animating = true;
    window.scrollTo({ top: y, behavior: 'smooth' });
    setTimeout(() => { animating = false; }, 780);
  };

  window.addEventListener('wheel', (e) => {
    if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    const t = targetTop();
    if (animating) { e.preventDefault(); return; }
    if (e.deltaY > 0 && window.scrollY < t - 40) {
      e.preventDefault();
      glideTo(t);
    } else if (e.deltaY < 0 && window.scrollY > 30 && window.scrollY < t + 60) {
      e.preventDefault();
      glideTo(0);
    }
  }, { passive: false });
})();

/* ---------- Margin rail: the section label inks in as you read past it ---------- */
(function () {
  const rails = document.querySelectorAll('.rail');
  if (!rails.length) return;

  const update = () => {
    const h = window.innerHeight;

    rails.forEach(rail => {
      const r = rail.getBoundingClientRect();
      /* How far the bottom edge of the screen has travelled into the section:
         0 when it touches the section's top, 1 when it reaches its bottom. One
         measure for every section, tall or short — the label fills as much as
         the reader has scrolled past. */
      const p = (h - r.top) / r.height;
      rail.style.setProperty('--fill', Math.min(1, Math.max(0, p)) * 100 + '%');
    });
  };

  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  update();
})();

/* ---------- Earlier experience: condensed rows that unfold ----------
   The toggle is built here rather than in the markup, so a visitor without
   scripting is never left with a dead control — they just get the full list. */
(function () {
  const wrap = document.querySelector('#early-experience');
  const list = wrap?.querySelector('.early-list');
  const eyebrow = wrap?.querySelector('.sub-eyebrow');
  if (!wrap || !list || !eyebrow) return;

  const count = list.querySelectorAll('.experience-card').length;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'early-toggle';
  btn.setAttribute('aria-controls', list.id);
  eyebrow.insertAdjacentElement('afterend', btn);

  const label = (condensed) => {
    btn.textContent = condensed ? `Show ${count} earlier roles` : 'Hide earlier roles';
    btn.setAttribute('aria-expanded', String(!condensed));
  };

  wrap.classList.add('is-condensed');
  label(true);

  let animating = false;

  btn.addEventListener('click', () => {
    if (animating) return;

    const from = list.offsetHeight;
    const condensed = wrap.classList.toggle('is-condensed');
    label(condensed);
    if (reduceMotion) return;

    const to = list.offsetHeight;
    animating = true;
    if (!condensed) wrap.classList.add('is-unfolding');

    list.style.overflow = 'hidden';
    list.style.height = from + 'px';
    void list.offsetHeight; /* flush, so the height below is a change to animate from */
    list.style.transition = 'height 0.42s cubic-bezier(0.22, 1, 0.36, 1)';
    list.style.height = to + 'px';

    const settle = () => {
      if (!animating) return;
      animating = false;
      ['height', 'overflow', 'transition'].forEach(p => list.style.removeProperty(p));
      wrap.classList.remove('is-unfolding');
    };

    list.addEventListener('transitionend', function onEnd(e) {
      if (e.target !== list || e.propertyName !== 'height') return;
      list.removeEventListener('transitionend', onEnd);
      settle();
    });
    setTimeout(settle, 700);
  });
})();

/* ---------- Soft reveal: a section's content fades + rises in as it enters view ----------
   Section headers (.section-eyebrow) are deliberately excluded so they stay put. */
(function () {
  const revealSelector =
    '.sub-eyebrow, .work-item, .experience-card, .research-item, .media-feature, .edu-detail, #contact p, .contact-links';
  const targets = document.querySelectorAll(revealSelector);
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!targets.length || reduceMotion || !('IntersectionObserver' in window)) return;

  targets.forEach(el => el.classList.add('reveal'));

  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll(revealSelector).forEach((el, i) => {
        el.style.transitionDelay = Math.min(i * 70, 350) + 'ms';
        el.classList.add('is-visible');
      });
      obs.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });

  document.querySelectorAll('section[id]').forEach(sec => io.observe(sec));
})();
