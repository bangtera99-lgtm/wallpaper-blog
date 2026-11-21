# Wallpaper HP Gratis — Blog Statis untuk GitHub Pages

Blog download wallpaper HP gratis — bilingual (Bahasa Indonesia + English),
SEO-ready, mobile-first. Tanpa build step: file HTML/CSS/JS statis,
langsung tayang di GitHub Pages.

Target SEO: Indonesia + US/global. Kategori Indonesia menargetkan pencarian
Bahasa Indonesia; 15 kategori baru berbahasa Inggris menargetkan pencarian
global/US yang paling dicari (sunset, galaxy, ocean, city lights, forest,
minimal, neon, mountain, anime, cyberpunk, space, cars, technology, nature,
abstract, animals).

**Penting — download jujur:** setiap kartu wallpaper punya tombol
**Download Wallpaper** yang mengarah langsung ke file gambar aslinya
(Unsplash, `w=1080`). Tidak ada tombol download palsu yang me-redirect
ke iklan. Iklan Adsterra hanya Popunder + Smart Link (Direct Link) yang
diberi label “Iklan”, terpisah dari tombol download.

## Isi repo

| File / folder | Fungsi |
|---|---|
| `index.html` | Beranda — grid wallpaper, pencarian, filter kategori, SEO ID + EN |
| `categories/*.html` | Halaman SEO tiap kategori (21 halaman: 5 ID + 15 EN + emoji) |
| `assets/style.css`, `assets/app.js` | Desain + pencarian/filter (memuat `data/wallpapers.json`) |
| `data/wallpapers.json` | 66 wallpaper starter (sudah tayang) |
| `data/pool.json` | 60 wallpaper cadangan untuk auto-update harian (= 10 hari @ 6/hari) |
| `data/emoji.json` | 6 paket Emoji / Stiker WA |
| `scripts/generate.py` | Generator: render ulang semua halaman + mode `--daily` |
| `.github/workflows/daily-update.yml` | Cron harian 01:00 UTC — tambah 6 wallpaper, commit otomatis |
| `sitemap.xml`, `feed.xml`, `robots.txt` | SEO: sitemap (22 URL), RSS, robots |

Kategori Indonesia: **Aesthetic (8), Anime (6), Islami (7), Pemandangan Alam (8),
Hewan Lucu (7)** = 36 wallpaper starter, plus 6 paket Emoji/Stiker WA.

Kategori Inggris (baru, 2026-11-21): **Sunset (5), Galaxy (5), Ocean (4),
City Lights (5), Forest (4), Minimal (4), Neon (5), Mountain (4),
Cyberpunk (4), Space (4), Cars (5), Technology (4), Nature (4),
Abstract (5), Animals (4)** = 66 wallpaper baru (30 starter + 36 pool).
Total starter: 66 wallpaper. Total pool: 60 wallpaper.

Semua gambar Unsplash baru sudah diverifikasi dengan HEAD request (HTTP 200)
sebelum dipakai; ID yang 404 dibuang (9 ID dibuang dari 103 kandidat).

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

## 2. Iklan Adsterra yang dipakai

Hanya **Popunder + Smart Link (Direct Link)** — tidak ada slot banner
(banner 728x90, in-feed, dan sidebar sengaja dihapus 2026-11-21 atas
permintaan Putela, termasuk penyisipan slot kosong di `assets/app.js`).

| Iklan | Letak |
|---|---|
| **Popunder** | Script di `<head>` setiap halaman (template `AD_HEAD` di `scripts/generate.py`) |
| **Smart Link / Direct Link** | Link teks berlabel “Iklan” — “Lihat Penawaran Sponsor” — di footer setiap halaman. **Jangan** ditempel di tombol Download. Tombol Download harus tetap ke gambar asli. |

Jangan menempel kode yang sama di semua penempatan — satu kode untuk satu
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

**Stok pool:** 60 entri = 10 hari auto-update (6/hari). Sebelum habis,
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

## 4. SEO yang sudah disiapkan

- Meta description, Open Graph, Twitter Card, dan JSON-LD
  (`CollectionPage` + `ImageObject`) di setiap halaman.
- Judul + deskripsi Bahasa Indonesia per wallpaper ID, dan judul +
  deskripsi English yang kaya kata kunci per wallpaper EN
  (mis. “Sunset Mountain Wallpaper HD for iPhone”).
- Halaman kategori EN memakai `<html lang="en">`, H1 dan meta title
  Inggris (“Sunset Wallpaper for iPhone & Android — Free HD Download”).
- Beranda punya dua bagian SEO: Bahasa Indonesia (“Cara Download
  Wallpaper HP Gratis”) dan English (“Free HD Wallpapers for iPhone &
  Android — Trending Now”) yang menautkan ke 15 kategori trending.
- URL kategori yang jelas (`/categories/sunset.html`, dst.).
- `sitemap.xml` (22 URL, diperbarui tiap generate), `robots.txt`, RSS `feed.xml`.
- Desain mobile-first, gambar `loading="lazy"`, tanpa build step.

## Lisensi gambar

Gambar bersumber dari Unsplash (lisensi gratis, bebas dipakai).
Untuk pemakaian pribadi; cantumkan kredit Unsplash bila memungkinkan.
