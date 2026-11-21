#!/usr/bin/env python3
"""
Generator blog wallpaper statis untuk GitHub Pages.

- Tanpa --daily: hanya me-render ulang index.html, categories/*.html,
  sitemap.xml dan feed.xml dari data/wallpapers.json (+ emoji.json).
- Dengan --daily: pindahkan 6 entri pertama dari data/pool.json ke
  data/wallpapers.json (tanpa duplikat, berdasarkan id), beri tanggal hari
  ini, simpan kembali kedua file, lalu render ulang semuanya.
  Dipakai oleh .github/workflows/daily-update.yml (cron 01:00 UTC).

GANTI SITE_URL di bawah dengan URL GitHub Pages kamu, contoh:
  https://bangtera99-lgtm.github.io/wallpaper-blog
"""
import argparse
import html
import json
import pathlib
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_URL = "https://bangtera99-lgtm.github.io/wallpaper-blog"  # <-- GANTI INI
SITE_NAME = "Wallpaper HP Gratis"
SITE_DESC = "Download wallpaper HP gratis HD: aesthetic, anime, islami, pemandangan alam, dan hewan lucu. Semua wallpaper bisa diunduh langsung, tanpa daftar."

CATEGORIES = {
    "aesthetic": ("Aesthetic", "Wallpaper aesthetic pastel, gradient, abstrak, dan minimalis untuk HP."),
    "anime": ("Anime", "Wallpaper anime aesthetic, karakter, dan ilustrasi untuk HP Android dan iPhone."),
    "islami": ("Islami", "Wallpaper Islami masjid, kaligrafi, dan arsitektur masjid yang menenangkan."),
    "pemandangan": ("Pemandangan Alam", "Wallpaper pemandangan alam: danau, gunung, hutan, pantai, dan sunset."),
    "hewan": ("Hewan Lucu", "Wallpaper hewan lucu: kucing, anjing, hamster, dan hewan menggemaskan lainnya."),
    "emoji": ("Emoji / Stiker WA", "Emoji dan stiker WA lucu yang bisa disalin langsung untuk WhatsApp."),
    # --- New global / US trending categories (English SEO, added 2026-11-21) ---
    "sunset": ("Sunset", "Free HD sunset wallpapers for iPhone and Android — golden hour, sunset skies, beaches and mountains."),
    "galaxy": ("Galaxy", "Free HD galaxy wallpapers for iPhone and Android — nebula, Milky Way, stars and deep space."),
    "ocean": ("Ocean", "Free HD ocean wallpapers for iPhone and Android — waves, beaches and blue sea."),
    "city-lights": ("City Lights", "Free HD city lights wallpapers for iPhone and Android — night skylines, streets and urban lights."),
    "forest": ("Forest", "Free HD forest wallpapers for iPhone and Android — green forests, sunlight and misty trees."),
    "minimal": ("Minimal", "Free HD minimal wallpapers for iPhone and Android — clean, simple and elegant designs."),
    "neon": ("Neon", "Free HD neon wallpapers for iPhone and Android — glowing neon lights, gaming and city neon."),
    "mountain": ("Mountain", "Free HD mountain wallpapers for iPhone and Android — peaks, lakes, snow and valleys."),
    "cyberpunk": ("Cyberpunk", "Free HD cyberpunk wallpapers for iPhone and Android — futuristic neon cities and sci-fi vibes."),
    "space": ("Space", "Free HD space wallpapers for iPhone and Android — stars, moon, planets and outer space."),
    "cars": ("Cars", "Free HD car wallpapers for iPhone and Android — sports cars, classic cars and race cars."),
    "technology": ("Technology", "Free HD technology wallpapers for iPhone and Android — circuits, tech and digital designs."),
    "nature": ("Nature", "Free HD nature wallpapers for iPhone and Android — flowers, green scenery and beautiful nature."),
    "abstract": ("Abstract", "Free HD abstract wallpapers for iPhone and Android — colorful abstract art and gradients."),
    "animals": ("Animals", "Free HD animal wallpapers for iPhone and Android — cute pets and wild animals."),
}

# Categories whose pages are in English (US/global SEO)
EN_CATEGORIES = {"sunset", "galaxy", "ocean", "city-lights", "forest", "minimal",
                 "neon", "mountain", "cyberpunk", "space", "cars", "technology",
                 "nature", "abstract", "animals"}

def load(name):
    p = ROOT / "data" / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []

def save(name, data):
    (ROOT / "data" / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def esc(s):
    return html.escape(str(s), quote=True)

# --- Slot iklan Adsterra (jujur, diberi label) ---
AD_HEAD = """<!-- ADSTERRA: POPUNDER — dipasang 2026-11-21 dari kode Putela -->
<script data-cfasync="false" src="https://accountut.com/1/18afe249b73f75bdec1c11a3d446102b"></script>
"""
# Slot banner dihapus 2026-11-21 atas permintaan Putela — hanya Popunder + Direct Link (Smart Link) yang dipakai.
AD_BANNER = ""
AD_INFEED = ""
AD_SIDEBAR = ""

def card(w, prefix=""):
    return f"""<article class="card">
<img loading="lazy" src="{esc(w['image'])}" alt="{esc(w['title'])}" width="720" height="1280">
<div class="card-body"><span class="badge">{esc(CATEGORIES.get(w['category'], (w['category'], ''))[0])}</span>
<h3>{esc(w['title'])}</h3><p>{esc(w['description'])}</p>
<p class="meta">{esc(w['resolution'])} &middot; {esc(w.get('date',''))}</p>
<a class="btn" href="{esc(w['full'])}" download="{esc(w['slug'])}.jpg" target="_blank" rel="noopener">Download Wallpaper</a></div>
</article>"""

def nav(prefix, active=""):
    links = "".join(
        f'<a href="{prefix}categories/{slug}.html" class="{"active" if slug == active else ""}">{label}</a>'
        for slug, (label, _) in CATEGORIES.items()
    )
    return f'<nav class="cat"><a href="{prefix}index.html">Beranda</a>{links}</nav>'

def json_ld(items):
    import json as j
    data = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": SITE_NAME, "description": SITE_DESC, "inLanguage": "id",
        "hasPart": [{"@type": "ImageObject", "name": w["title"], "contentUrl": w["full"],
                     "description": w["description"]} for w in items[:10]],
    }
    return '<script type="application/ld+json">\n' + j.dumps(data, ensure_ascii=False, indent=2) + '\n</script>'

def page(title, desc, body, prefix="", canonical="", items=None, extra_head="", lang="id"):
    items = items or []
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{esc(canonical or SITE_URL + '/')}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical or SITE_URL + '/')}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{prefix}assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)}" href="{prefix}feed.xml">
{AD_HEAD}
{json_ld(items)}
{extra_head}
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="{prefix}index.html">Wallpaper <span>HP Gratis</span></a>
<p class="tagline">Download wallpaper HP gratis HD — aesthetic, anime, islami, pemandangan, hewan lucu.</p>
{nav(prefix)}
</div></header>
{AD_BANNER}
<main class="wrap">
{body}
</main>
<footer><div class="wrap">
<p>{esc(SITE_NAME)} — semua wallpaper di situs ini gratis diunduh untuk pemakaian pribadi. Gambar bersumber dari Unsplash (lisensi gratis). Iklan yang tampil diberi label “Iklan”.</p>
<p><span class="ad-label">Iklan</span> <a href="https://ardance.org/4/1341fb6a63df060c86c10f188e0db24c" target="_blank" rel="noopener sponsored nofollow">Lihat Penawaran Sponsor</a></p>
<p><a href="{prefix}sitemap.xml">Sitemap</a> &middot; <a href="{prefix}feed.xml">RSS</a> &middot; <a href="{prefix}index.html">Beranda</a></p>
</div></footer>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
"""

def seo_section():
    return """<section class="seo">
<h2>Cara Download Wallpaper HP Gratis</h2>
<p>Pilih wallpaper yang kamu suka, lalu klik tombol <strong>Download Wallpaper</strong>. Gambar akan terbuka dalam ukuran penuh (1080x1920) dan bisa langsung disimpan ke galeri HP kamu — tanpa daftar, tanpa aplikasi tambahan. Semua wallpaper di halaman ini gratis untuk pemakaian pribadi.</p>
<h2>Kategori Wallpaper Paling Dicari</h2>
<ul>
<li><strong>Wallpaper Aesthetic</strong> — pastel, gradient, abstrak, dan minimalis untuk tampilan HP yang bersih.</li>
<li><strong>Wallpaper Anime</strong> — anime aesthetic dan ilustrasi untuk penggemar anime.</li>
<li><strong>Wallpaper Islami</strong> — masjid dan nuansa Islami yang menenangkan.</li>
<li><strong>Wallpaper Pemandangan Alam</strong> — danau, gunung, hutan, pantai, dan sunset.</li>
<li><strong>Wallpaper Hewan Lucu</strong> — kucing, anjing, dan hamster yang menggemaskan.</li>
<li><strong>Emoji / Stiker WA</strong> — emoji lucu yang bisa disalin langsung untuk WhatsApp.</li>
</ul>
<p>Blog ini diperbarui setiap hari dengan wallpaper baru. Gunakan kolom pencarian di atas untuk mencari tema favoritmu, misalnya “kucing”, “masjid”, atau “sunset”.</p>
</section>"""

def seo_section_en(prefix=""):
    links = "".join(
        f'<li><strong><a href="{prefix}categories/{s}.html">{l} Wallpaper</a></strong> — {d}</li>'
        for s, (l, d) in CATEGORIES.items() if s in EN_CATEGORIES
    )
    return f"""<section class="seo">
<h2>Free HD Wallpapers for iPhone &amp; Android — Trending Now</h2>
<p>Looking for a free HD wallpaper for your phone? Pick any wallpaper below and tap <strong>Download Wallpaper</strong>. Every image opens in full size (1080x1920) and saves straight to your gallery — no sign-up, no extra app. New wallpapers are added every day.</p>
<h2>Trending Wallpaper Topics</h2>
<ul>
{links}
</ul>
<p>Popular searches right now: sunset wallpaper, galaxy wallpaper, ocean wallpaper, city lights wallpaper, forest wallpaper, minimal wallpaper, neon wallpaper, mountain wallpaper, anime wallpaper and cyberpunk wallpaper. Use the search box above to find your favorite theme — try “sunset”, “galaxy”, “ocean” or “neon”.</p>
</section>"""

def render(wallpapers, emoji):
    # Beranda
    latest = sorted(wallpapers, key=lambda x: x.get("date", ""), reverse=True)
    cards = "\n".join(card(w) for w in latest)
    cat_links = "".join(
        f'<li><a href="categories/{s}.html">Wallpaper {l}</a> — {d}</li>'
        for s, (l, d) in CATEGORIES.items() if s != "emoji"
    )
    emoji_preview = "".join(
        f'<div class="emoji-card"><div class="emoji-big">{esc(e["emoji"])}</div><h3>{esc(e["name"])}</h3><p>{esc(e["description"])}</p></div>'
        for e in emoji[:4]
    )
    body = f"""<h1>Download Wallpaper HP Gratis HD</h1>
<p class="lead">{esc(SITE_DESC)}</p>
<input id="search" class="search" type="search" placeholder="Cari wallpaper: kucing, sunset, galaxy, neon, ocean..." aria-label="Cari wallpaper">
<div class="filters">
<button data-filter="all" class="active">Semua</button>
{''.join(f'<button data-filter="{s}">{l}</button>' for s, (l, _) in CATEGORIES.items() if s != "emoji")}
</div>
<p class="meta" id="count">{len(latest)} wallpaper</p>
<div class="layout"><div>
<div class="grid" id="wallpaper-grid" data-category="all">
{cards}
</div>
{AD_INFEED}
</div><aside>{AD_SIDEBAR}
<section class="seo"><h2>Kategori</h2><ul>{cat_links}</ul></section>
</aside></div>
<h2>Emoji &amp; Stiker WA</h2>
<div class="emoji-grid">{emoji_preview}</div>
<p><a href="categories/emoji.html">Lihat semua emoji &amp; stiker WA &rarr;</a></p>
{seo_section()}
{seo_section_en()}"""
    (ROOT / "index.html").write_text(
        page("Download Wallpaper HP Gratis HD — Aesthetic, Anime, Islami | " + SITE_NAME,
             SITE_DESC, body, prefix="", canonical=SITE_URL + "/", items=latest), encoding="utf-8")

    # Halaman kategori
    for slug, (label, cdesc) in CATEGORIES.items():
        if slug == "emoji":
            e_cards = "".join(
                f'<div class="emoji-card"><div class="emoji-big">{esc(e["emoji"])}</div>'
                f'<h3>{esc(e["name"])}</h3><p>{esc(e["description"])}</p>'
                f'<button class="copy-btn" data-copy="{esc(e["emoji"])}">Salin Emoji</button></div>'
                for e in emoji)
            body_c = f"""<h1>Emoji &amp; Stiker WA Lucu — Salin Gratis</h1>
<p class="lead">Kumpulan emoji dan stiker WA lucu: cinta, hewan, semangat, makanan, dan liburan. Klik “Salin Emoji”, lalu tempel di WhatsApp.</p>
<div class="emoji-grid">{e_cards}</div>
{AD_INFEED}
{AD_SIDEBAR}
{seo_section()}"""
            items_c = []
            page_title = f"Wallpaper {label} untuk HP — Download Gratis HD | {SITE_NAME}"
            page_desc = f"Download wallpaper {label.lower()} untuk HP gratis HD. {cdesc}"
            page_lang = "id"
        else:
            items_c = [w for w in wallpapers if w["category"] == slug]
            items_c = sorted(items_c, key=lambda x: x.get("date", ""), reverse=True)
            cards_c = "\n".join(card(w, prefix="../") for w in items_c)
            res = esc(items_c[0]['resolution']) if items_c else '1080x1920'
            if slug in EN_CATEGORIES:
                body_c = f"""<h1>{esc(label)} Wallpaper for Phone — Free HD Download</h1>
<p class="lead">{esc(cdesc)} All {esc(label.lower())} wallpapers below are free to download in {res} resolution for iPhone and Android.</p>
<p class="meta">{len(items_c)} {esc(label.lower())} wallpapers</p>
<div class="grid" id="wallpaper-grid" data-category="{slug}">
{cards_c}
</div>
{AD_INFEED}
{AD_SIDEBAR}
{seo_section_en("../")}"""
                page_title = f"{label} Wallpaper for iPhone & Android — Free HD Download | {SITE_NAME}"
                page_desc = f"Download free {label.lower()} wallpaper for iPhone and Android in HD. {cdesc}"
                page_lang = "en"
            else:
                body_c = f"""<h1>Wallpaper {esc(label)} untuk HP — Download Gratis HD</h1>
<p class="lead">{esc(cdesc)} Semua wallpaper {esc(label.lower())} di bawah ini gratis diunduh dalam resolusi {res}.</p>
<p class="meta">{len(items_c)} wallpaper {esc(label.lower())}</p>
<div class="grid" id="wallpaper-grid" data-category="{slug}">
{cards_c}
</div>
{AD_INFEED}
{AD_SIDEBAR}
{seo_section()}"""
                page_title = f"Wallpaper {label} untuk HP — Download Gratis HD | {SITE_NAME}"
                page_desc = f"Download wallpaper {label.lower()} untuk HP gratis HD. {cdesc}"
                page_lang = "id"
        (ROOT / "categories" / f"{slug}.html").write_text(
            page(page_title, page_desc,
                 body_c, prefix="../", canonical=f"{SITE_URL}/categories/{slug}.html", items=items_c, lang=page_lang),
            encoding="utf-8")

    # sitemap.xml
    today = date.today().isoformat()
    urls = [(SITE_URL + "/", today)] + [
        (f"{SITE_URL}/categories/{s}.html", today) for s in CATEGORIES
    ]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in urls:
        sm.append(f"  <url><loc>{esc(u)}</loc><lastmod>{d}</lastmod><changefreq>daily</changefreq></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    # feed.xml (RSS)
    rss_items = ""
    for w in latest[:20]:
        rss_items += (f"<item><title>{esc(w['title'])}</title><link>{SITE_URL}/#{esc(w['slug'])}</link>"
                      f"<description>{esc(w['description'])}</description>"
                      f"<pubDate>{esc(w.get('date',''))}</pubDate><guid>{SITE_URL}/#{esc(w['slug'])}</guid></item>\n")
    rss = (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
           f"<title>{esc(SITE_NAME)}</title><link>{SITE_URL}/</link>"
           f"<description>{esc(SITE_DESC)}</description><language>id</language>\n{rss_items}</channel></rss>\n")
    (ROOT / "feed.xml").write_text(rss, encoding="utf-8")
    print(f"Rendered: index + {len(CATEGORIES)} category pages, sitemap, feed. Total wallpapers: {len(wallpapers)}")

def daily_update():
    wallpapers = load("wallpapers.json")
    pool = load("pool.json")
    if not pool:
        print("Pool habis — tambahkan entri baru ke data/pool.json agar auto-update bisa lanjut.")
        return wallpapers
    existing = {w["id"] for w in wallpapers}
    today = date.today().isoformat()
    added = 0
    while pool and added < 6:
        item = pool.pop(0)
        if item["id"] in existing:
            continue
        item["date"] = today
        wallpapers.append(item)
        existing.add(item["id"])
        added += 1
    save("wallpapers.json", wallpapers)
    save("pool.json", pool)
    print(f"Daily update: +{added} wallpaper baru (tanggal {today}). Sisa pool: {len(pool)}")
    return wallpapers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--daily", action="store_true", help="Tambah 6 wallpaper dari pool, lalu render ulang")
    args = ap.parse_args()
    wallpapers = daily_update() if args.daily else load("wallpapers.json")
    emoji = load("emoji.json")
    render(wallpapers, emoji)

if __name__ == "__main__":
    main()
