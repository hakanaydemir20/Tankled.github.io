# Tankled SEO Rehberi

## Sitede yapılanlar (teknik SEO)
- Her sayfaya anahtar kelimeli başlık (≤60 karakter) ve açıklama (≤160 karakter)
- Canonical, robots, Open Graph (WhatsApp/Instagram önizlemesi), Twitter kartı, favicon
- Yapısal veri (schema.org): Store (Ankara/Ostim, telefon, e-posta, Instagram), WebSite,
  Product (Betta Serisi), FAQPage (ana sayfadaki SSS), alt sayfalarda BreadcrumbList
- Ana sayfaya görünür "Sıkça Sorulan Sorular" bölümü (yapısal veriyle aynı metin)
- `sitemap.xml`, `robots.txt`, `404.html`
- Görseller WebP'ye çevrildi: ana sayfa ~30 MB → ~2 MB; boyut (width/height) eklendi
- Rehber sayfaları (bitkiler, balıklar, malzemeler, galeri) arası iç bağlantılar

Tüm etiketler `_seo/seo.py` içinden yönetilir. Başlık/açıklama değiştirmek için orayı
düzenleyip çalıştırın:
```bash
python3 _seo/seo.py
```

## Alan adı alındığında (zorunlu)
1. GitHub → Tankled.github.io → Settings → Pages → Custom domain: `alanadiniz.com`
   (depoya `CNAME` dosyası eklenir), "Enforce HTTPS" işaretleyin.
2. `_seo/seo.py` içinde `SITE = "https://alanadiniz.com"` yapıp `python3 _seo/seo.py` çalıştırın.
3. `404.html` içindeki `/Tankled.github.io/` yollarını `/` yapın.
4. Not: `robots.txt` ancak alan adının kökünde çalışır; github.io alt klasöründeyken Google onu okumaz.

## Siteden bağımsız, sıralamayı en çok etkileyen işler (sizin yapmanız gerekenler)
Google'da "akvaryum Ankara" gibi aramalarda öne çıkmak için teknik SEO tek başına yetmez.
Yerel aramalarda en büyük etken **Google İşletme Profili**dir.

1. **Google İşletme Profili** (en önemli): https://business.google.com
   - Kategori: "Akvaryum mağazası" / "Evcil hayvan malzemeleri mağazası"
   - Adres (Ostim, Ankara), telefon, web sitesi, çalışma saatleri, ürün fotoğrafları
   - Bilgiler sitedekiyle **birebir aynı** olsun (isim, adres, telefon)
   - Haftada 1 gönderi ve fotoğraf ekleyin
2. **Müşteri yorumları:** Her satıştan sonra Google yorumu isteyin; yorumlara cevap verin.
3. **Google Search Console:** https://search.google.com/search-console
   - Siteyi ekleyin, `sitemap.xml` gönderin, "URL denetimi" ile ana sayfayı dizine ekletin.
4. **Bing Webmaster Tools:** https://www.bing.com/webmasters (Search Console'dan içe aktarılabilir).
5. **Bağlantılar (backlink):** Akvaryum forumları, Ankara yerel rehberleri, Instagram/YouTube
   açıklamaları, e-ticaret pazar yeri mağaza sayfaları, Ostim firma rehberi.
6. **Düzenli içerik:** Rehber sayfalarına yeni bitki/balık ekleyin; "betta akvaryumu nasıl kurulur",
   "nano akvaryum bakımı" gibi blog yazıları uzun vadede en çok trafik getiren kaynaktır.
7. **Fotoğraflar:** Balık sayfası kartlarına gerçek fotoğraf ekleyin (`assets/baliklar/README.md`).

## Gerçekçi beklenti
"Akvaryum" tek kelimesi Türkiye'de çok rekabetlidir (büyük pet mağazaları, pazar yerleri).
Hedef öncelikle "el yapımı akvaryum", "ahşap akvaryum", "betta akvaryumu", "akvaryum Ankara",
"dekoratif akvaryum" gibi daha belirli aramalar olmalı. Yeni bir sitenin sıralama kazanması
genellikle 3-6 ay sürer.
