/* ── Theme ── */
(function () {
  const saved = localStorage.getItem('theme') || 'day';
  document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', () => {

  /* page fade-in */
  document.body.classList.add('page-enter');

  /* smooth nav transitions */
  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('http') || link.target === '_blank') return;
    link.addEventListener('click', e => {
      e.preventDefault();
      document.body.classList.remove('page-enter');
      document.body.classList.add('page-exit');
      setTimeout(() => { window.location.href = href; }, 280);
    });
  });

  /* ── Theme toggle ── */
  const toggle = document.getElementById('theme-toggle');
  const html   = document.documentElement;

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    if (toggle) toggle.querySelector('.theme-icon').textContent = theme === 'night' ? '☀️' : '🌙';
    if (theme === 'night') spawnFireflies();
    else clearFireflies();
    const doodle = document.getElementById('toggle-doodle');
    if (doodle) doodle.textContent = theme === 'night' ? 'day mode ↗' : 'night mode ↗';
  }

  if (toggle) {
    const current = html.getAttribute('data-theme') || 'day';
    toggle.querySelector('.theme-icon').textContent = current === 'night' ? '☀️' : '🌙';
    toggle.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'night' ? 'day' : 'night';
      applyTheme(next);
    });
  }

  /* Initial state on load */
  const initTheme = html.getAttribute('data-theme');
  if (toggle) toggle.querySelector('.theme-icon').textContent = initTheme === 'night' ? '☀️' : '🌙';
  if (initTheme === 'night') spawnFireflies();
  const doodle = document.getElementById('toggle-doodle');
  if (doodle) {
    doodle.textContent = initTheme === 'night' ? 'day mode ↗' : 'night mode ↗';
  }
  generateStars();


  /* ── Stars ── */
  function generateStars() {
    const container = document.getElementById('stars-container');
    if (!container) return;
    for (let i = 0; i < 120; i++) {
      const s = document.createElement('div');
      s.className = 'star';
      const size = Math.random() * 2.5 + 0.5;
      s.style.cssText = `
        width:${size}px; height:${size}px;
        left:${Math.random() * 100}%;
        top:${Math.random() * 65}%;
        animation-duration:${2 + Math.random() * 4}s;
        animation-delay:${Math.random() * 4}s;
        opacity:${Math.random() * 0.6 + 0.2};
      `;
      container.appendChild(s);
    }
  }

  /* ── Fireflies ── */
  function spawnFireflies() {
    const container = document.getElementById('fireflies-container');
    if (!container || container.children.length > 0) return;
    for (let i = 0; i < 30; i++) {
      const f = document.createElement('div');
      f.className = 'firefly';
      const dx = (Math.random() - 0.5) * 60;
      const dy = -(Math.random() * 60 + 10);
      f.style.cssText = `
        left:${Math.random() * 100}%;
        top:${40 + Math.random() * 50}%;
        --fx:${dx}px; --fy:${dy}px;
        animation-duration:${3 + Math.random() * 5}s;
        animation-delay:${Math.random() * 5}s;
        width:${2 + Math.random() * 3}px;
        height:${2 + Math.random() * 3}px;
      `;
      container.appendChild(f);
    }
  }

  function clearFireflies() {
    const container = document.getElementById('fireflies-container');
    if (container) container.innerHTML = '';
  }

  /* ── Back to top ── */
  const topBtn = document.getElementById('back-to-top');
  if (topBtn) {
    window.addEventListener('scroll', () => {
      topBtn.classList.toggle('visible', window.scrollY > 300);
    }, { passive: true });
    topBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── Auto slug in post form ── */
  const titleInput = document.getElementById('id_title');
  const slugInput  = document.getElementById('id_slug');
  if (titleInput && slugInput) {
    titleInput.addEventListener('input', () => {
      if (slugInput.dataset.touched) return;
      slugInput.value = titleInput.value.toLowerCase().trim()
        .replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
    });
    slugInput.addEventListener('input', () => { slugInput.dataset.touched = '1'; });
  }

  /* ── Social links manager (settings page) ── */
  const socialContainer = document.getElementById('social-links-container');
  const socialsInput    = document.getElementById('socials-data-input');
  if (socialContainer && socialsInput) {
    let links = JSON.parse(socialsInput.value || '[]');
    renderLinks();

    document.getElementById('add-social-btn').addEventListener('click', () => {
      links.push({ label: '', url: '', visible: true });
      renderLinks();
    });

    function renderLinks() {
      socialContainer.innerHTML = '';
      links.forEach((link, i) => {
        const row = document.createElement('div');
        row.className = 'social-row';
        row.innerHTML = `
          <input type="text" value="${esc(link.label)}" placeholder="Label (e.g. Twitter)" data-i="${i}" data-f="label">
          <input type="text" value="${esc(link.url)}"   placeholder="https://..." data-i="${i}" data-f="url">
          <label class="toggle-vis">
            <input type="checkbox" ${link.visible ? 'checked' : ''} data-i="${i}" data-f="visible">
            Visible
          </label>
          <button type="button" class="rm-btn" data-i="${i}" title="Remove">×</button>
        `;
        socialContainer.appendChild(row);
      });
      socialContainer.querySelectorAll('input[data-f]').forEach(el => {
        el.addEventListener('input', () => updateLink(el));
        el.addEventListener('change', () => updateLink(el));
      });
      socialContainer.querySelectorAll('.rm-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          links.splice(+btn.dataset.i, 1);
          renderLinks();
        });
      });
      syncJSON();
    }

    function updateLink(el) {
      const i = +el.dataset.i;
      const field = el.dataset.f;
      links[i][field] = field === 'visible' ? el.checked : el.value;
      syncJSON();
    }

    function syncJSON() {
      socialsInput.value = JSON.stringify(links);
    }

    function esc(str) {
      return String(str || '').replace(/"/g, '&quot;').replace(/</g, '&lt;');
    }
  }
});
