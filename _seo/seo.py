"""Tankled sitesinin SEO etiketlerini, site haritasini ve robots.txt'yi uretir.

Alan adi alindiginda yalnizca SITE degerini degistirip calistirin:
    python3 _seo/seo.py

Her sayfanin <head> bolumundeki <!-- SEO --> ... <!-- /SEO --> blogu yeniden yazilir;
baslik ve aciklama da buradaki degerlerle guncellenir. (_seo klasoru GitHub Pages'te
yayinlanmaz.)
"""

import json
import re
from datetime import date
from pathlib import Path

# ----------------------------------------------------------------- ayarlar
SITE = "https://hakanaydemir20.github.io/Tankled.github.io"  # sonda / yok
MARKA = "Tankled"
INSTAGRAM = "https://www.instagram.com/tankled.akvaryum/"
EPOSTA = "tankledaquarium@gmail.com"
TELEFON = "+90 531 217 2006"
KAPAK = "assets/og-kapak.jpg"

KOK = Path(__file__).resolve().parent.parent

SAYFALAR = [
    {
        "dosya": "index.html", "yol": "", "oncelik": "1.0", "siklik": "weekly",
        "baslik": "El Yapımı Dekoratif Akvaryum | Ankara | Tankled",
        "aciklama": "Ankara'daki atölyemizde masif tik ahşaptan el yapımı dekoratif akvaryumlar: "
                    "betta akvaryumu, nano akvaryum, teraryum ve paludaryum. Özel tasarım yapılır.",
        "kirinti": [],
    },
    {
        "dosya": "galeri/index.html", "yol": "galeri/", "oncelik": "0.7", "siklik": "monthly",
        "baslik": "Akvaryum Galerisi: El Yapımı Akvaryum Fotoğrafları | Tankled",
        "aciklama": "Tankled Betta Serisi ve el yapımı akvaryum, teraryum ve paludaryum kurulumlarından "
                    "fotoğraflar: farklı açılar, üç ışık tonu ve yaşam alanları.",
        "kirinti": [("Galeri", "galeri/")],
    },
    {
        "dosya": "bitkiler/index.html", "yol": "bitkiler/", "oncelik": "0.8", "siklik": "monthly",
        "baslik": "Akvaryum Bitkileri Rehberi: Low Tech ve Paludaryum | Tankled",
        "aciklama": "Akvaryum ve paludaryum bitkileri rehberi: anubias, java yosunu, halı bitkileri. "
                    "Işık, sıcaklık, pH ve bakım bilgileriyle doğru bitkiyi seçin.",
        "kirinti": [("Bitkiler", "bitkiler/")],
    },
    {
        "dosya": "baliklar/index.html", "yol": "baliklar/", "oncelik": "0.8", "siklik": "monthly",
        "baslik": "Akvaryum Balıkları Rehberi: Betta, Nano, Karides | Tankled",
        "aciklama": "Betta, neon tetra, rasbora, corydoras, karides ve salyangoz: akvaryum balıkları "
                    "rehberi. Boyut, sıcaklık, pH, akvaryum hacmi ve beslenme bilgileri.",
        "kirinti": [("Balıklar", "baliklar/")],
    },
    {
        "dosya": "malzemeler/index.html", "yol": "malzemeler/", "oncelik": "0.8", "siklik": "monthly",
        "baslik": "Akvaryum Kurulumu ve Malzemeleri: Adım Adım Rehber | Tankled",
        "aciklama": "Akvaryum nasıl kurulur? Filtre, ısıtıcı, zemin, su şartlandırıcı ve test kiti ne işe yarar, "
                    "hangisi gerekli? Adım adım akvaryum kurulum rehberi.",
        "kirinti": [("Malzemeler ve Kurulum", "malzemeler/")],
    },
    {
        "dosya": "akvaryum-olustur/index.html", "yol": "akvaryum-olustur/", "oncelik": "0.7", "siklik": "monthly",
        "baslik": "3D Akvaryum Tasarla ve Litre Hesapla | Tankled",
        "aciklama": "Akvaryumunuzu 3 boyutlu tasarlayın: model ve ölçüleri seçin, litre ve ışık ihtiyacını hesaplayın, "
                    "zemin ve bitkileri yerleştirip sonucu anında görün.",
        "kirinti": [("3D Akvaryum Tasarımı", "akvaryum-olustur/")],
    },
]

# Yalnizca yonlendirme yapan sayfa: dizine eklenmesin, asil sayfayi gostersin.
YONLENDIRMELER = [("akvaryum-hesaplama/index.html", "akvaryum-olustur/")]

SSS = [
    ("Tankled akvaryumları nerede üretiliyor?",
     "Tankled akvaryumları Ankara Ostim'deki atölyemizde, elde ve tek tek üretilir. Her parçanın ahşap "
     "damarı farklı olduğu için her ürün kendine özgüdür."),
    ("Betta Serisi'nin ölçüleri ve malzemeleri nelerdir?",
     "Betta Serisi 14 × 14 × 20 cm ölçülerindedir. Gövdesi tik yağıyla korunan masif tik ahşaptır; "
     "sürgülü buhar kapaklı cam hazne ve 3000K, 4500K ve 6500K olmak üzere üç ışık tonlu LED aydınlatma bulunur."),
    ("Tankled ürünleri yalnızca akvaryum olarak mı kullanılır?",
     "Hayır. Aynı ürün betta akvaryumu, bitkili akvaryum, teraryum, egzotik hayvan yuvası, sukulent saksısı, "
     "aksesuar kutusu ya da abajur olarak kullanılabilir."),
    ("Akvaryumun bakımı zor mu?",
     "Betta Serisi low-tech bir sistemdir; sürekli bakım ve teknik bilgi gerektirmez. Talep üzerine hazır "
     "kurulum seti de sunuyoruz."),
    ("Özel ölçü ya da tasarım yaptırabilir miyim?",
     "Evet. İletişim formundan ya da telefonla bize ulaşarak hayalinizdeki akvaryumu birlikte tasarlayabiliriz."),
    ("Akvaryuma hangi bitki ve balıkları koyabilirim?",
     "Bitkiler, Balıklar ve Malzemeler rehberlerimizde akvaryumunuza uygun canlıları, bakım koşullarını ve "
     "adım adım kurulumu bulabilirsiniz."),
]


# ----------------------------------------------------------------- yardimcilar
def url(yol: str) -> str:
    return f"{SITE}/{yol}"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def isletme() -> dict:
    return {
        "@type": "Store",
        "@id": url("#isletme"),
        "name": MARKA,
        "alternateName": "Tankled Aquarium",
        "description": "Ankara'da masif tik ahşaptan el yapımı dekoratif akvaryum, teraryum ve paludaryum atölyesi.",
        "url": url(""),
        "logo": url("assets/icon-512.png"),
        "image": [url(KAPAK), url("assets/hero.webp")],
        "email": EPOSTA,
        "telephone": TELEFON,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Ostim",
            "addressLocality": "Yenimahalle",
            "addressRegion": "Ankara",
            "addressCountry": "TR",
        },
        "areaServed": [{"@type": "City", "name": "Ankara"}, {"@type": "Country", "name": "Türkiye"}],
        "sameAs": [INSTAGRAM],
        "knowsAbout": ["akvaryum", "betta akvaryumu", "nano akvaryum", "teraryum", "paludaryum", "aquascape"],
    }


def yapisal_veri(sayfa: dict) -> list[dict]:
    if sayfa["yol"] == "":
        return [{
            "@context": "https://schema.org",
            "@graph": [
                isletme(),
                {"@type": "WebSite", "@id": url("#site"), "url": url(""), "name": MARKA,
                 "inLanguage": "tr-TR", "publisher": {"@id": url("#isletme")}},
                {"@type": "Product", "name": "Tankled Betta Serisi",
                 "description": "Masif tik ahşap gövdeli, sürgülü buhar kapaklı, üç ışık tonlu LED aydınlatmalı "
                                "14 × 14 × 20 cm el yapımı akvaryum.",
                 "brand": {"@type": "Brand", "name": MARKA},
                 "manufacturer": {"@id": url("#isletme")},
                 "material": "Masif tik ahşap, cam",
                 "image": [url("assets/galeri/urun-bicim-01-tam-onden.jpg"), url("assets/galeri/urun-bicim-02-sol-45.jpg")],
                 "additionalProperty": [
                     {"@type": "PropertyValue", "name": "Ölçü", "value": "14 × 14 × 20 cm"},
                     {"@type": "PropertyValue", "name": "Aydınlatma", "value": "3000K / 4500K / 6500K LED"},
                     {"@type": "PropertyValue", "name": "Elektrik", "value": "220V"}]},
                {"@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": s, "acceptedAnswer": {"@type": "Answer", "text": c}}
                    for s, c in SSS]},
            ],
        }]
    ogeler = [{"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": url("")}]
    for i, (ad, yol) in enumerate(sayfa["kirinti"], start=2):
        ogeler.append({"@type": "ListItem", "position": i, "name": ad, "item": url(yol)})
    return [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ogeler}]


def blok(sayfa: dict, onek: str) -> str:
    adres = url(sayfa["yol"])
    satirlar = [
        "<!-- SEO -->",
        f'<link rel="canonical" href="{adres}" />',
        '<meta name="robots" content="index, follow, max-image-preview:large" />',
        '<meta name="theme-color" content="#5c7a5a" />',
        '<meta name="geo.region" content="TR-06" />',
        '<meta name="geo.placename" content="Ankara" />',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{onek}assets/favicon-32.png" />',
        f'<link rel="apple-touch-icon" href="{onek}assets/apple-touch-icon.png" />',
        '<meta property="og:type" content="website" />',
        f'<meta property="og:site_name" content="{MARKA}" />',
        '<meta property="og:locale" content="tr_TR" />',
        f'<meta property="og:title" content="{esc(sayfa["baslik"])}" />',
        f'<meta property="og:description" content="{esc(sayfa["aciklama"])}" />',
        f'<meta property="og:url" content="{adres}" />',
        f'<meta property="og:image" content="{url(KAPAK)}" />',
        '<meta property="og:image:width" content="1200" />',
        '<meta property="og:image:height" content="630" />',
        '<meta name="twitter:card" content="summary_large_image" />',
    ]
    for veri in yapisal_veri(sayfa):
        satirlar.append('<script type="application/ld+json">'
                        + json.dumps(veri, ensure_ascii=False, separators=(",", ":")) + "</script>")
    satirlar.append("<!-- /SEO -->")
    return "\n".join(satirlar)


def sayfa_isle(sayfa: dict) -> None:
    yol = KOK / sayfa["dosya"]
    s = yol.read_text(encoding="utf-8")
    onek = "../" * sayfa["dosya"].count("/")
    s = re.sub(r"<title>.*?</title>", f"<title>{sayfa['baslik']}</title>", s, count=1, flags=re.S)
    aciklama = f'<meta name="description" content="{esc(sayfa["aciklama"])}" />'
    if re.search(r'<meta name="description"[^>]*>', s):
        s = re.sub(r'<meta name="description"[^>]*>', aciklama, s, count=1)
    else:
        s = s.replace("</title>", "</title>\n" + aciklama, 1)
    s = re.sub(r"\n?<!-- SEO -->.*?<!-- /SEO -->", "", s, flags=re.S)
    s = s.replace(aciklama, aciklama + "\n" + blok(sayfa, onek), 1)
    yol.write_text(s, encoding="utf-8")


def yonlendirme_isle(dosya: str, hedef: str) -> None:
    yol = KOK / dosya
    s = yol.read_text(encoding="utf-8")
    s = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{url(hedef)}" />', s)
    if 'name="robots"' not in s:
        s = s.replace("<title>", '<meta name="robots" content="noindex, follow" />\n<title>', 1)
    yol.write_text(s, encoding="utf-8")


def sss_bolumu() -> None:
    """Ana sayfadaki gorunur SSS bolumunu yapisal veriyle ayni metinden uretir."""
    yol = KOK / "index.html"
    s = yol.read_text(encoding="utf-8")
    sorular = "\n".join(
        f"      <details><summary>{esc(soru)}</summary><p>{esc(cevap)}</p></details>" for soru, cevap in SSS)
    bolum = (
        '<!-- SSS -->\n<section class="section" id="sss">\n  <div class="wrap">\n'
        '    <div class="sec-head reveal">\n      <span class="eyebrow">Sıkça Sorulan Sorular</span>\n'
        "      <h2>Akvaryum hakkında merak edilenler</h2>\n    </div>\n"
        f'    <div class="faq reveal">\n{sorular}\n    </div>\n  </div>\n</section>\n<!-- /SSS -->')
    s = re.sub(r"<!-- SSS -->.*?<!-- /SSS -->", lambda _: bolum, s, count=1, flags=re.S)
    yol.write_text(s, encoding="utf-8")


ALT_BAGLANTILAR = [("Ana sayfa", ""), ("Galeri", "galeri/"), ("Bitkiler", "bitkiler/"), ("Balıklar", "baliklar/"),
                   ("Malzemeler", "malzemeler/"), ("3D Tasarım", "akvaryum-olustur/"), ("Instagram", INSTAGRAM)]


def alt_bilgi(sayfa: dict) -> None:
    """Alt sayfalarin alt bilgisine rehberler arasi baglantilar ekler (ic baglanti)."""
    if sayfa["yol"] == "":
        return
    yol = KOK / sayfa["dosya"]
    s = yol.read_text(encoding="utf-8")
    onek = "../" * sayfa["dosya"].count("/")
    baglantilar = " · ".join(
        f'<a href="{h if h.startswith("http") else onek + h}"'
        + (' target="_blank" rel="noopener"' if h.startswith("http") else "") + f">{ad}</a>"
        for ad, h in ALT_BAGLANTILAR if h != sayfa["yol"])
    yeni = (f'<footer><nav class="alt-nav" style="margin-bottom:6px">{baglantilar}</nav>'
            f'© <span id="year"></span> Tankled · El yapımı akvaryum, Ankara</footer>')
    s, n = re.subn(r"<footer>.*?</footer>", lambda _: yeni, s, count=1, flags=re.S)
    if n:
        yol.write_text(s, encoding="utf-8")


def site_haritasi() -> None:
    bugun = date.today().isoformat()
    ogeler = "".join(
        f"  <url><loc>{url(s['yol'])}</loc><lastmod>{bugun}</lastmod>"
        f"<changefreq>{s['siklik']}</changefreq><priority>{s['oncelik']}</priority></url>\n"
        for s in SAYFALAR)
    (KOK / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ogeler + "</urlset>\n",
        encoding="utf-8")
    (KOK / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /ig/\n\n" f"Sitemap: {url('sitemap.xml')}\n", encoding="utf-8")


if __name__ == "__main__":
    for s in SAYFALAR:
        sayfa_isle(s)
        alt_bilgi(s)
    sss_bolumu()
    for d, h in YONLENDIRMELER:
        yonlendirme_isle(d, h)
    site_haritasi()
    print(f"{len(SAYFALAR)} sayfa, sitemap.xml ve robots.txt guncellendi -> {SITE}")
