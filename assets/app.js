// Data-driven: memuat data/wallpapers.json agar entri baru dari auto-update
// langsung tampil tanpa edit HTML. Halaman juga sudah berisi kartu statis
// (pre-rendered oleh scripts/generate.py) untuk SEO / Google.
(function () {
  var grid = document.getElementById('wallpaper-grid');
  var search = document.getElementById('search');
  var count = document.getElementById('count');
  if (!grid) return;
  var all = [];
  var activeCat = grid.getAttribute('data-category') || 'all';

  function card(w) {
    var el = document.createElement('article');
    el.className = 'card';
    el.innerHTML =
      '<img loading="lazy" src="' + w.image + '" alt="' + w.title + '" width="720" height="1280">' +
      '<div class="card-body"><span class="badge">' + w.category + '</span>' +
      '<h3>' + w.title + '</h3><p>' + w.description + '</p>' +
      '<p class="meta">' + w.resolution + ' &middot; ' + (w.date || '') + '</p>' +
      // Download ASLI: tautan langsung ke file gambar. Bukan redirect iklan.
      '<a class="btn" href="' + w.full + '" download="' + w.slug + '.jpg" target="_blank" rel="noopener">Download Wallpaper</a></div>';
    return el;
  }
  function render(list) {
    grid.innerHTML = '';
    list.forEach(function (w, i) {
      grid.appendChild(card(w));
      // Slot iklan in-feed (kosong sampai kode Adsterra ditempel di HTML statis)
      if (i === 5) {
        var ad = document.createElement('div');
        ad.className = 'ad-slot';
        ad.innerHTML = '<span class="ad-label">Iklan</span>';
        grid.appendChild(ad);
      }
    });
    if (count) count.textContent = list.length + ' wallpaper';
  }
  function filtered() {
    var q = search ? search.value.toLowerCase() : '';
    return all.filter(function (w) {
      var okCat = activeCat === 'all' || w.category === activeCat;
      var okQ = !q || (w.title + ' ' + w.description + ' ' + w.tags).toLowerCase().indexOf(q) !== -1;
      return okCat && okQ;
    });
  }
  fetch('data/wallpapers.json').then(function (r) { return r.json(); }).then(function (data) {
    all = data;
    render(filtered());
  }).catch(function () {
    // Jika fetch gagal (mis. dibuka via file://), kartu statis di HTML tetap tampil.
    if (count) count.textContent = grid.querySelectorAll('.card').length + ' wallpaper';
  });
  if (search) search.addEventListener('input', function () { render(filtered()); });
  document.querySelectorAll('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.filters button').forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
      activeCat = b.getAttribute('data-filter');
      render(filtered());
    });
  });
  // Salin emoji (halaman Emoji)
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy');
      if (navigator.clipboard) navigator.clipboard.writeText(t);
      b.textContent = 'Disalin!';
      setTimeout(function () { b.textContent = 'Salin Emoji'; }, 1500);
    });
  });
})();
