(function () {
  var root = document.documentElement;

  /* ---- 라이트/다크 전환 ---- */
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var cur = root.getAttribute('data-theme');
      if (!cur) {
        cur = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      var next = cur === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('wt-theme', next); } catch (e) {}
    });
  }

  /* ---- 검색 ---- */
  var btn = document.getElementById('searchBtn');
  var panel = document.getElementById('searchPanel');
  var input = document.getElementById('searchInput');
  var out = document.getElementById('searchResults');
  var data = null;
  var base = (document.querySelector('link[rel="alternate"]') || {}).href || '';
  var baseurl = base ? base.replace(/\/feed\.xml.*$/, '') : '';

  function load() {
    if (data) return Promise.resolve(data);
    return fetch(baseurl + '/search.json')
      .then(function (r) { return r.json(); })
      .then(function (j) { data = j; return j; })
      .catch(function () { data = []; return data; });
  }

  function render(q) {
    if (!out) return;
    q = (q || '').trim().toLowerCase();
    if (!q) { out.innerHTML = ''; return; }
    var hits = (data || []).filter(function (p) {
      return (p.title + ' ' + p.summary + ' ' + p.tags + ' ' + p.category).toLowerCase().indexOf(q) > -1;
    }).slice(0, 12);
    if (!hits.length) {
      out.innerHTML = '<p style="padding:12px;color:var(--muted);font-size:14px">검색 결과가 없습니다.</p>';
      return;
    }
    out.innerHTML = hits.map(function (p) {
      return '<a href="' + p.url + '">' + p.title + '<small>' + p.category + ' · ' + p.date + '</small></a>';
    }).join('');
  }

  if (btn && panel) {
    btn.addEventListener('click', function () {
      panel.hidden = !panel.hidden;
      if (!panel.hidden) { load().then(function () { input.focus(); }); }
    });
  }
  if (input) {
    input.addEventListener('input', function () { load().then(function () { render(input.value); }); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { panel.hidden = true; }
    });
  }

  /* ---- 모바일 카테고리 메뉴 토글 ---- */
  var menuBtn = document.getElementById('menuBtn');
  var catnav = document.getElementById('catnav');
  if (menuBtn && catnav) {
    menuBtn.addEventListener('click', function () {
      catnav.classList.toggle('open');
    });
  }
})();
