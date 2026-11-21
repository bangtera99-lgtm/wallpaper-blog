# Wallpaper HP Gratis — Blog Statis untuk GitHub Pages

Blog download wallpaper HP gratis (Bahasa Indonesia, SEO-ready, mobile-first).
Tanpa build step: file HTML/CSS/JS statis, langsung tayang di GitHub Pages.

**Penting — download jujur:** setiap kartu wallpaper punya tombol
**Download Wallpaper** yang mengarah langsung ke file gambar aslinya
(Unsplash, `w=1080`). Tidak ada tombol download palsu yang me-redirect
ke iklan. Iklan Adsterra dipasang di slot yang diberi label “Iklan”,
terpisah dari tombol download.

## Isi repo

| File / folder | Fungsi |
|---|---|
| `index.html` | Beranda — grid wallpaper, pencarian, filter kategori, SEO |
| `categories/*.html` | Halaman SEO tiap kategori: `aesthetic`, `anime`, `islami`, `pemandangan`, `hewan`, `emoji` |
| `assets/style.css`, `assets/app.js` | Desain + pencarian/filter (memuat `data/wallpapers.json`) |
| `data/wallpapers.json` | 36 wallpaper starter (sudah tayang) |
| `data/pool.json` | 24 wallpaper cadangan untuk auto-update harian |
| `data/emoji.json` | 6 paket Emoji / Stiker WA |
| `scripts/generate.py` | Generator: render ulang semua halaman + mode `--daily` |
| `.github/workflows/daily-update.yml` | Cron harian 01:00 UTC — tambah 6 wallpaper, commit otomatis |
| `sitemap.xml`, `feed.xml`, `robots.txt` | SEO: sitemap, RSS, robots |

Kategori: **Aesthetic (8), Anime (6), Islami (7), Pemandangan Alam (8),
Hewan Lucu (7)** = 36 wallpaper starter, plus 6 paket Emoji/Stiker WA.

## 1. Cara mengaktifkan GitHub Pages

1. Hubungkan GitHub kamu ke Muse, lalu buat repo baru — saran nama:
   `wallpaper-blog` (boleh nama lain, tapi ingat: nama repo memengaruhi URL).
2. Push semua file di folder ini ke repo itu (branch `main`, folder root).
3. Di GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main, folder: /(root) → Save.**
4. Tunggu 1–2 menit. Blog tayang di:
   `https://USERNAME.github.io/wallpaper-blog/`
   (ganti `USERNAME` dengan username GitHub kamu).
5. **Wajib:** ganti `SITE_URL` di `scripts/generate.py` (baris atas) dan di
   `robots.txt` dengan URL asli itu, lalu jalankan sekali:
   `python scripts/generate.py` dan push lagi. Ini supaya sitemap,
   canonical, dan RSS memakai URL yang benar.

## 2. Tempat menempel kode Adsterra

Semua slot sudah ditandai di HTML dengan komentar
`<!-- ADSTERRA: ... — paste code here -->`. Cari komentar itu di
`index.html` dan `categories/*.html` (atau lebih mudah: edit template
di `scripts/generate.py`, lalu jalankan ulang generatornya).

| Slot | Letak | Kode Adsterra yang ditempel |
|---|---|---|
| **Popunder / Social Bar** | Blok `ADSTERRA: POPUNDER / SOCIAL BAR` di `<head>` setiap halaman | Script Popunder atau Social Bar dari dashboard Adsterra → Websites → Social Bar / Popunder |
| **Banner 728x90** | `ADSTERRA: BANNER 728x90` — tepat di bawah header | Kode banner Adsterra ukuran 728x90 (di HP otomatis menyesuaikan lebar) |
| **In-feed / Native** | `ADSTERRA: IN-FEED / NATIVE BANNER` — di tengah grid wallpaper | Kode Native Ads / banner Adsterra |
| **Sidebar** | `ADSTERRA: SIDEBAR BANNER` — kolom kanan (desktop) | Kode banner Adsterra (mis. 300x250) |
| **Direct Link** | **Jangan** ditempel di tombol Download. Kalau mau memakai Direct Link, buat tombol/link teks terpisah yang jelas, mis. di footer atau di bawah grid, dengan label “Sponsor” / “Iklan”. Tombol Download harus tetap ke gambar asli. | Direct Link Adsterra (Websites → Direct Link) |

Catatan: saat menempel kode, hapus baris placeholder di dalam slot itu.
Jangan menempel kode yang sama di semua slot — satu kode untuk satu
penempatan, sesuai yang dibuat di dashboard Adsterra.

## 3. Cara kerja auto-update harian

1. GitHub Actions berjalan tiap hari pukul **01:00 UTC (08:00 WIB)**
   (file `.github/workflows/daily-update.yml`, bisa juga dijalankan
   manual lewat tab **Actions → Run workflow**).
2. `scripts/generate.py --daily` mengambil **6 entri pertama**
   dari `data/pool.json`, memindahkannya ke `data/wallpapers.json`
   (cek duplikat berdasarkan `id`, memberi tanggal hari ini),
   lalu me-render ulang `index.html`, semua halaman kategori,
   `sitemap.xml`, dan `feed.xml`.
3. Workflow meng-commit dan push hasilnya kembali ke repo.
   GitHub Pages membangun ulang otomatis — wallpaper baru langsung tampil.

**Stok pool:** 24 entri = 4 hari auto-update (6/hari). Sebelum habis,
tambahkan entri baru ke `data/pool.json` dengan format yang sama
(`id`, `slug`, `title`, `category`, `description`, `tags`,
`resolution`, `unsplash_id`, `image`, `full`, `date` boleh kosong).
Gambar memakai URL Unsplash `images.unsplash.com` yang sudah
terverifikasi hidup (HTTP 200) saat blog ini dibuat. Kalau menambah
gambar sendiri, cek dulu URL-nya benar-benar bisa dibuka.

Jalankan manual di komputer:
```bash
python scripts/generate.py          # render ulang saja
python scripts/generate.py --daily  # tambah 6 dari pool + render ulang
```

## 4. Yang masih harus Putela lakukan sebelum push

- [ ] Hubungkan akun GitHub ke Muse (saat ini **belum terhubung**).
- [ ] Pilih / beri tahu nama repo, mis. `wallpaper-blog`.
- [ ] Ganti `SITE_URL` di `scripts/generate.py` dan `robots.txt`
      dengan URL GitHub Pages yang sebenarnya.
- [ ] (Opsional) Tempel kode Adsterra di slot-slot di atas — blog
      tetap jalan tanpa iklan, jadi ini bisa belakangan.
- [ ] Setelah repo dibuat, beri tahu Muse agar file-file ini di-push.

## 5. SEO yang sudah disiapkan

- Meta description, Open Graph, Twitter Card, dan JSON-LD
  (`CollectionPage` + `ImageObject`) di setiap halaman.
- Judul + deskripsi Bahasa Indonesia per wallpaper, tag kata kunci,
  URL kategori yang jelas (`/categories/aesthetic.html`, dst.).
- `sitemap.xml` (diperbarui tiap generate), `robots.txt`, RSS `feed.xml`.
- Desain mobile-first, gambar `loading="lazy"`, tanpa build step.

## Lisensi gambar

Gambar bersumber dari Unsplash (lisensi gratis, bebas dipakai).
Untuk pemakaian pribadi; cantumkan kredit Unsplash bila memungkinkan.
