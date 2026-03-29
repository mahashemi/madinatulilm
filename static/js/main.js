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

    // Keyboard close
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
