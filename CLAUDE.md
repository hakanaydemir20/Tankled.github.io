# Tankled sitesi: Claude için notlar

Statik site (GitHub Pages, `main` dalı). SEO etiketleri, blog, hizmet sayfaları ve site haritası
`_seo/seo.py` ile üretilir; içerik `_seo/blog.py` (blog) ve `_seo/sayfalar.py` (hizmet/hakkımızda/iletişim,
işletme bilgileri) içindedir. Üretilen HTML'i elle düzenleme; kaynağı düzenleyip `python3 -B _seo/seo.py` çalıştır.
Ayrıntılar: `_seo/SEO-REHBERI.md`, `_kaynak/gorsel/BENIOKU.md`.

## YAPILACAKLAR (Mac'te proje çekildiğinde sırayla yap)

Kullanıcı "projeyi çek" dediğinde önce `git pull`, sonra aşağıdaki açık maddeleri kullanıcıya hatırlat
ve onayını alarak yap. Biten maddeyi bu listeden sil ve commit et.

### 1. Gemini görselleri — TAMAMLANDI (2026-10-28)
Tüm blog kapakları, kullanım kartları ve galeri sahneleri üretildi (son 16'sı 1K, 1024×768).
Kullanıcı kararları: "yapay zekâ ile üretilmiştir" notu EKLENMEZ; maliyet için 1K yeterli; üretmeden önce
adet/konu tablosu sunup onay al. Açık karar: şu 8 görselde istem hatasıyla üst üste fincan var, kullanıcı onay
verirse (`--yeniden`, istem düzeltildi) yeniden üret: blog/gece-lambasi-olarak-isikli-teraryum, kullanim/abajur,
kullanim/bitki-saksisi, galeri/sahne-{balkon-bitkili,mutfak-tezgahi,restoran-masasi,toplanti-odasi,bahce-masasi}.

### 2. Kullanıcıdan gelecek gerçek fotoğrafları yerleştir
Hakkımızda ve Betta sayfalarında "Fotoğraf eklenecek" kutuları var (`_seo/sayfalar.py` → `foto_yer`).
Kutulardaki HTML yorumunda önerilen dosya adı yazıyor (ör. `assets/hakkimizda/tankled-atolye-ostim-ankara.webp`).
Fotoğraflar gelince WebP'ye çevir, bu adlarla kaydet ve kutuların yerine gerçek görselleri koy.

### 3. Kullanıcıdan beklenen bilgiler (gelince `_seo/sayfalar.py` → `ISLETME` / `YORUMLAR`)
- Gerçek müşteri yorumları (izinli; uydurma yorum ekleme)
- Endonezya'dan gelen özel seri ağacının adı (tik mi?) ve "tik yağı ile korumalı" bilgisinin doğruluğu

### 4. Hosting'e yüklenmeyi bekleyenler
Kullanıcı kararı (2026-10-29): geliştirmeler önce yalnızca GitHub demo sitesine; kullanıcı söyleyince hosting'e
(DirectAdmin dosya yöneticisi, zip yükle + aç). Bekleyen: İmza Avize kartı, aydınlatma barı görselleri ve 30–40 cm stok bilgisi, Betta/Nano/Paludarium
kart slaytları, galeriye eklenen 6 görsel (assets/avize, assets/lamba, index.html, galeri/index.html).

## Bilinen işletme bilgileri (değiştirme, her yerde birebir aynı olmalı)
- Atölye: Ostim OSB, 100. Yıl Blv., 06374 Yenimahalle/Ankara (Google profiliyle aynı) · Pzt–Cmt 10:00–16:00, Pazar kapalı · Tel: +90 531 217 2006 · tankledaquarium@gmail.com
- Betta Serisi (doğal çam ahşap), Özel Betta Serisi (Endonezya ithal ağaç), Nano Serisi. SİTEDE FİYAT YAZILMAZ (kullanıcı kararı 2026-10-28): "Sipariş için WhatsApp'tan ulaşın" denir; yapısal veride de fiyat yok
- Türkiye'nin 81 iline ve yurt dışına kargo
- Ürünler akvaryum, teraryum, abajur ve bitki saksısı olarak kullanılabilir
