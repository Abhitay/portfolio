/* Shared behaviour for every page. Each block is guarded, so a page only runs
   what its markup actually contains. Loaded with `defer`, so the DOM is ready. */

/* ---------- Google Analytics ---------- */
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-6V9RNG3QS4');

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

/* ---------- Magnet scroll: the first downward scroll glides the whole hero out
   to the next section in one motion (and snaps back up near the top). ---------- */
(function () {
  const first = document.querySelector('#experience');
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

/* ---------- Flash the target section when an internal link is clicked ---------- */
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', function () {
    const target = document.getElementById(this.getAttribute('href').slice(1));
    if (!target) return;
    document.querySelectorAll('.highlight-flash').forEach(el => el.classList.remove('highlight-flash'));
    setTimeout(() => {
      target.classList.add('highlight-flash');
      setTimeout(() => target.classList.remove('highlight-flash'), 3000);
    }, 100);
  });
});

/* ---------- "Best viewed on desktop" prompt before opening a dense case study ---------- */
(function () {
  const caseStudyLinks = document.querySelectorAll(
    'a[href*="feature-impact.html"], a[href*="growth-allocation.html"], a[href*="ai-insights-copilot.html"]'
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

/* ---------- Collapsible "On this page" side index ---------- */
(function () {
  const sideIndex = document.querySelector('.side-index.collapsible');
  const sideToggle = sideIndex?.querySelector('.side-index-toggle');
  const sideBody = sideIndex?.querySelector('.side-index-body');
  const sideClose = sideIndex?.querySelector('.side-index-close');
  if (!sideIndex || !sideToggle || !sideBody) return;

  const sideMedia = window.matchMedia('(max-width: 768px)');

  const openPanel = () => {
    sideIndex.classList.add('open');
    sideToggle.setAttribute('aria-expanded', 'true');
    sideBody.hidden = false;
  };

  const closePanel = () => {
    sideIndex.classList.remove('open');
    sideToggle.setAttribute('aria-expanded', 'false');
    if (sideMedia.matches) {
      setTimeout(() => {
        if (!sideIndex.classList.contains('open')) sideBody.hidden = true;
      }, 180);
    } else {
      sideBody.hidden = true;
    }
  };

  sideToggle.addEventListener('click', e => {
    e.preventDefault();
    sideIndex.classList.contains('open') ? closePanel() : openPanel();
  });

  sideClose?.addEventListener('click', closePanel);
  sideIndex.addEventListener('mouseenter', () => { if (!sideMedia.matches) openPanel(); });
  sideIndex.addEventListener('mouseleave', () => { if (!sideMedia.matches) closePanel(); });
  sideMedia.addEventListener('change', () => { sideBody.hidden = !sideIndex.classList.contains('open'); });
})();

/* ---------- Soft reveal: a section's content fades + rises in as it enters view ----------
   Section headers (.section-eyebrow) are deliberately excluded so they stay put. */
(function () {
  const revealSelector =
    '.sub-eyebrow, .work-item, .experience-card, .research-item, .impact-list, .media-feature, .edu-detail, #contact p, .contact-links';
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
