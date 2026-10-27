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

import blog
import sayfalar

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
        "baslik": "Akvaryum Ankara | Mobilyalı ve El Yapımı Akvaryum | Tankled",
        "aciklama": "Ankara Ostim atölyemizde doğal ahşaptan mobilyalı akvaryum ve el yapımı dekoratif akvaryum: "
                    "betta, nano akvaryum, teraryum, paludaryum. Ölçüye özel üretim.",
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
        "baslik": "Akvaryum Bitkileri ve Su Bitkileri Rehberi | Tankled",
        "aciklama": "Bitkili akvaryum için akvaryum bitkisi ve su bitkisi rehberi: anubias, java yosunu, halı "
                    "bitkileri. Işık, sıcaklık, pH ve bakım bilgileriyle doğru seçim.",
        "kirinti": [("Akvaryum Bitkileri", "bitkiler/")],
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
        "baslik": "Akvaryum Malzemeleri: Filtre, Pompa, Kum, Isıtıcı | Tankled",
        "aciklama": "Akvaryum filtresi, akvaryum pompası, akvaryum kumu, ısıtıcı ve su şartlandırıcı ne işe yarar? "
                    "Adım adım akvaryum kurulum ve malzeme rehberi.",
        "kirinti": [("Akvaryum Malzemeleri", "malzemeler/")],
    },
    {
        "dosya": "akvaryum-olustur/index.html", "yol": "akvaryum-olustur/", "oncelik": "0.7", "siklik": "monthly",
        "baslik": "3D Akvaryum Tasarla ve Litre Hesapla | Tankled",
        "aciklama": "Akvaryumunuzu 3 boyutlu tasarlayın: model ve ölçüleri seçin, litre ve ışık ihtiyacını hesaplayın, "
                    "zemin ve bitkileri yerleştirip sonucu anında görün.",
        "kirinti": [("3D Akvaryum Tasarımı", "akvaryum-olustur/")],
    },
]

for _s in sayfalar.SAYFALAR:
    SAYFALAR.append({
        "dosya": f"{_s['yol']}index.html", "yol": _s["yol"],
        "oncelik": "0.9" if _s["tur"] == "hizmet" else "0.6", "siklik": "monthly",
        "baslik": _s["baslik"], "aciklama": _s["aciklama"], "tur": _s["tur"], "sayfa": _s,
        "kirinti": [(_s["kisa"], _s["yol"])],
    })
SAYFALAR.append({
    "dosya": "blog/index.html", "yol": "blog/", "oncelik": "0.8", "siklik": "weekly",
    "baslik": blog.BLOG_BASLIK, "aciklama": blog.BLOG_ACIKLAMA, "tur": "blog",
    "kirinti": [("Blog", "blog/")],
})
for _y in blog.YAZILAR:
    SAYFALAR.append({
        "dosya": f"blog/{_y['slug']}/index.html", "yol": f"blog/{_y['slug']}/", "oncelik": "0.7",
        "siklik": "monthly", "baslik": _y["baslik"], "aciklama": _y["aciklama"], "tur": "yazi", "yazi": _y,
        "kirinti": [("Blog", "blog/"), (_y["h1"], f"blog/{_y['slug']}/")],
    })

# Yalnizca yonlendirme yapan sayfa: dizine eklenmesin, asil sayfayi gostersin.
YONLENDIRMELER = [("akvaryum-hesaplama/index.html", "akvaryum-olustur/")]

SSS = [
    ("Ankara dışına ve yurt dışına kargo yapıyor musunuz?",
     "Evet. Tüm modellerimizi Türkiye'nin 81 iline kargoyla gönderiyoruz; yurt dışına da kargo yapılabilir. "
     "Ayrıntılar için telefon ya da WhatsApp üzerinden bize ulaşabilirsiniz."),
    ("Tankled akvaryum fiyatları ne kadar?",
     "Betta Serisi 1.300 TL'den (doğal çam ahşap), Özel Betta Serisi 1.500 TL'den (Endonezya ithal ağaç), "
     "Nano Serisi 2.500 TL'den başlayan fiyatlarla sunulur. Özel ölçüde fiyat; ölçü, malzeme ve kuruluma göre belirlenir."),
    ("Ankara'da akvaryum nereden alabilirim?",
     "Tankled'in atölyesi Ankara Ostim'dedir. El yapımı ve mobilyalı akvaryumlarımızı atölyede görebilir, "
     "telefon ya da WhatsApp üzerinden bilgi alabilirsiniz. Tüm modellerimizi Türkiye'nin 81 iline kargoyla gönderiyoruz."),
    ("Mobilyalı akvaryum nedir?",
     "Mobilyalı akvaryum, cam haznenin dolap, sehpa, konsol ya da ahşap bir gövdeyle birlikte tasarlandığı "
     "akvaryumdur. Ağırlığı güvenle taşır, kablo ve ekipmanı gizler ve evin dekorasyonuyla bütünleşir."),
    ("Tankled akvaryumları nerede üretiliyor?",
     "Tankled akvaryumları Ankara Ostim'deki atölyemizde, elde ve tek tek üretilir. Her parçanın ahşap "
     "damarı farklı olduğu için her ürün kendine özgüdür."),
    ("Betta Serisi'nin ölçüleri ve malzemeleri nelerdir?",
     "Betta Serisi 14 × 14 × 20 cm ölçülerindedir. Standart seride gövde eşsiz doğal çam ahşaptan (1.300 TL), "
     "Özel Betta Serisi'nde Endonezya'dan ithal, doğal desenli ağaçtan (1.500 TL) üretilir; "
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
    bilgi = sayfalar.ISLETME
    veri = {
        "@type": "Store",
        "@id": url("#isletme"),
        "name": MARKA,
        "alternateName": "Tankled Aquarium",
        "description": "Ankara Ostim'de doğal masif ahşaptan mobilyalı akvaryum, el yapımı dekoratif akvaryum, "
                       "teraryum ve paludaryum üreten atölye.",
        "url": url(""),
        "logo": url("assets/icon-512.png"),
        "image": [url(KAPAK), url("assets/hero.webp")],
        "email": EPOSTA,
        "telephone": TELEFON,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ", ".join(p for p in [bilgi["sokak"], "Ostim"] if p),
            "addressLocality": "Yenimahalle",
            "addressRegion": "Ankara",
            "addressCountry": "TR",
        },
        "areaServed": [{"@type": "City", "name": "Ankara"}, {"@type": "Country", "name": "Türkiye"}],
        "sameAs": [INSTAGRAM],
        "knowsAbout": ["akvaryum", "dekoratif abajur", "bitki saksısı", "bitkili akvaryum", "akvaryum bitkileri", "akvaryum filtresi", "akvaryum kumu", "mobilyalı akvaryum", "el yapımı akvaryum", "ahşap akvaryum", "betta akvaryumu", "nano akvaryum", "teraryum", "paludaryum", "aquascape"],
    }
    if bilgi["posta_kodu"]:
        veri["address"]["postalCode"] = bilgi["posta_kodu"]
    if bilgi["saatler"]:
        gunler = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday", "Fr": "Friday",
                  "Sa": "Saturday", "Su": "Sunday"}
        sira = list(gunler)

        def gun_listesi(kod: str) -> list[str]:
            bas, _, son = kod.partition("-")
            return [gunler[g] for g in sira[sira.index(bas):sira.index(son or bas) + 1]]
        veri["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": gun_listesi(kod), "opens": a, "closes": k}
            for _, kod, a, k in bilgi["saatler"]]
    if bilgi["fiyat_baslangic"]:
        veri["priceRange"] = f"{bilgi['fiyat_baslangic']} TL+"
    if bilgi["kurulus_yili"]:
        veri["foundingDate"] = bilgi["kurulus_yili"]
    return veri


def yapisal_veri(sayfa: dict) -> list[dict]:
    if sayfa["yol"] == "":
        return [{
            "@context": "https://schema.org",
            "@graph": [
                isletme(),
                {"@type": "WebSite", "@id": url("#site"), "url": url(""), "name": MARKA,
                 "inLanguage": "tr-TR", "publisher": {"@id": url("#isletme")}},
                {"@type": "Product", "name": "Tankled Betta Serisi",
                 "description": "Doğal masif ahşap gövdeli, sürgülü buhar kapaklı, üç ışık tonlu LED aydınlatmalı "
                                "14 × 14 × 20 cm el yapımı akvaryum. Teraryum, dekoratif abajur ve bitki saksısı "
                                "olarak da kullanılabilir.",
                 "brand": {"@type": "Brand", "name": MARKA},
                 "manufacturer": {"@id": url("#isletme")},
                 "material": "Doğal çam ahşap / Endonezya ithal doğal desenli ağaç, cam",
                 "offers": {"@type": "AggregateOffer", "priceCurrency": "TRY", "lowPrice": "1300",
                            "highPrice": "1500", "offerCount": "2", "availability": "https://schema.org/InStock",
                            "url": url("betta-akvaryumu/"), "seller": {"@id": url("#isletme")}},
                 "image": [url("assets/galeri/urun-bicim-01-tam-onden.jpg"), url("assets/galeri/urun-bicim-02-sol-45.jpg")],
                 "additionalProperty": [
                     {"@type": "PropertyValue", "name": "Ölçü", "value": "14 × 14 × 20 cm"},
                     {"@type": "PropertyValue", "name": "Aydınlatma", "value": "3000K / 4500K / 6500K LED"},
                     {"@type": "PropertyValue", "name": "Elektrik", "value": "220V"}]},
                {"@type": "Product", "name": "Tankled Nano Serisi",
                 "description": "Doğal masif ahşap gövdeli, menteşeli üst kapaklı, sürgülü buhar camlı, üç ışık tonlu "
                                "LED aydınlatmalı 25 × 25 × 30 cm el yapımı nano akvaryum.",
                 "brand": {"@type": "Brand", "name": MARKA},
                 "manufacturer": {"@id": url("#isletme")},
                 "image": [url("assets/lagoon.webp")],
                 "offers": {"@type": "Offer", "priceCurrency": "TRY", "price": "2500",
                            "availability": "https://schema.org/InStock", "url": url("#products"),
                            "seller": {"@id": url("#isletme")}},
                 "additionalProperty": [
                     {"@type": "PropertyValue", "name": "Ölçü", "value": "25 × 25 × 30 cm"},
                     {"@type": "PropertyValue", "name": "Aydınlatma", "value": "3000K / 4500K / 6500K LED"},
                     {"@type": "PropertyValue", "name": "Elektrik", "value": "220V"}]},
                {"@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": s, "acceptedAnswer": {"@type": "Answer", "text": c}}
                    for s, c in SSS]},
            ],
        }]
    if sayfa.get("tur") == "blog":
        ekstra = {"@context": "https://schema.org", "@type": "Blog", "@id": url("blog/#blog"), "url": url("blog/"),
                  "name": "Tankled Blog", "description": sayfa["aciklama"], "inLanguage": "tr-TR",
                  "publisher": {"@id": url("#isletme")},
                  "blogPost": [{"@type": "BlogPosting", "headline": y["h1"], "url": url(f"blog/{y['slug']}/"),
                                "datePublished": y["tarih"]} for y in blog.sirali()]}
    elif sayfa.get("tur") == "yazi":
        y = sayfa["yazi"]
        ekstra = {"@context": "https://schema.org", "@type": "BlogPosting",
                  "mainEntityOfPage": {"@type": "WebPage", "@id": url(sayfa["yol"])},
                  "headline": y["h1"], "description": y["aciklama"], "image": [url(y["gorsel"])],
                  "datePublished": y["tarih"], "dateModified": y["tarih"], "inLanguage": "tr-TR",
                  "keywords": ", ".join(y["etiketler"]),
                  "author": {"@type": "Organization", "name": MARKA, "url": url("")},
                  "publisher": {"@type": "Organization", "name": MARKA,
                                "logo": {"@type": "ImageObject", "url": url("assets/icon-512.png")}},
                  "isPartOf": {"@id": url("blog/#blog")}}
    elif sayfa.get("tur") == "hizmet":
        ekstra = {"@context": "https://schema.org", "@type": "Service", "name": sayfa["sayfa"]["hizmet"],
                  "serviceType": sayfa["sayfa"]["hizmet"], "description": sayfa["aciklama"], "url": url(sayfa["yol"]),
                  "image": url(sayfa["sayfa"]["gorsel"]), "provider": isletme(),
                  "areaServed": [{"@type": "City", "name": "Ankara"}, {"@type": "Country", "name": "Türkiye"}]}
    elif sayfa.get("tur") in ("hakkimizda", "iletisim"):
        ekstra = {"@context": "https://schema.org",
                  "@type": "AboutPage" if sayfa["tur"] == "hakkimizda" else "ContactPage",
                  "name": sayfa["baslik"], "description": sayfa["aciklama"], "url": url(sayfa["yol"]),
                  "inLanguage": "tr-TR", "about": isletme()}
    else:
        ekstra = None
    ogeler = [{"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": url("")}]
    for i, (ad, yol) in enumerate(sayfa["kirinti"], start=2):
        ogeler.append({"@type": "ListItem", "position": i, "name": ad, "item": url(yol)})
    kirinti = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ogeler}
    return [ekstra, kirinti] if ekstra else [kirinti]


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
        f'<meta property="og:type" content="{"article" if sayfa.get("tur") == "yazi" else "website"}" />',
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
    if sayfa.get("tur") == "yazi":
        satirlar.append(f'<meta property="article:published_time" content="{sayfa["yazi"]["tarih"]}" />')
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


def ana_sayfa_bloklari() -> None:
    """Ana sayfadaki son blog yazisi kartlarini ve (varsa) musteri yorumlarini uretir."""
    yol = KOK / "index.html"
    s = yol.read_text(encoding="utf-8")
    kartlar = "\n".join(
        f'      <a class="blog-kart reveal" href="blog/{y["slug"]}/"><img src="{y["gorsel"]}" alt="{esc(y["gorsel_alt"])}" '
        f'width="{y["gorsel_g"]}" height="{y["gorsel_y"]}" loading="lazy"/><div><h3>{y["h1"]}</h3><p>{y["aciklama"]}</p></div></a>'
        for y in blog.sirali()[:3])
    s = re.sub(r'(<!-- BLOG -->.*?<div class="blog-liste">\n).*?(\n    </div>)', lambda m: m.group(1) + kartlar + m.group(2), s, count=1, flags=re.S)
    if sayfalar.YORUMLAR:
        ogeler = "\n".join(
            f'      <figure class="yorum reveal"><blockquote>“{esc(y["metin"])}”</blockquote>'
            f'<figcaption>{esc(y["ad"])} · {esc(y.get("kaynak", "Google"))}</figcaption></figure>'
            for y in sayfalar.YORUMLAR)
        bolum = ('<section class="section" id="yorumlar">\n  <div class="wrap">\n    <div class="sec-head reveal">\n'
                 '      <span class="eyebrow">Müşteri Yorumları</span>\n      <h2>Müşterilerimiz ne diyor?</h2>\n    </div>\n'
                 f'    <div class="blog-liste">\n{ogeler}\n    </div>\n  </div>\n</section>')
    else:
        bolum = ""
    s = re.sub(r"<!-- YORUMLAR -->.*?<!-- /YORUMLAR -->", lambda _: f"<!-- YORUMLAR -->{bolum}<!-- /YORUMLAR -->", s, count=1, flags=re.S)
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


ALT_BAGLANTILAR = [("Ana sayfa", ""), ("Mobilyalı Akvaryum", "mobilyali-akvaryum/"), ("Hakkımızda", "hakkimizda/"), ("İletişim", "iletisim/"), ("Galeri", "galeri/"), ("Bitkiler", "bitkiler/"), ("Balıklar", "baliklar/"),
                   ("Malzemeler", "malzemeler/"), ("3D Tasarım", "akvaryum-olustur/"), ("Blog", "blog/"), ("Instagram", INSTAGRAM)]


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
    blog.uret()
    sayfalar.uret()
    for s in SAYFALAR:
        sayfa_isle(s)
        alt_bilgi(s)
    sss_bolumu()
    ana_sayfa_bloklari()
    for d, h in YONLENDIRMELER:
        yonlendirme_isle(d, h)
    site_haritasi()
    print(f"{len(SAYFALAR)} sayfa, sitemap.xml ve robots.txt guncellendi -> {SITE}")
