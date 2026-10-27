# Tankled sitesi: Claude için notlar

Statik site (GitHub Pages, `main` dalı). SEO etiketleri, blog, hizmet sayfaları ve site haritası
`_seo/seo.py` ile üretilir; içerik `_seo/blog.py` (blog) ve `_seo/sayfalar.py` (hizmet/hakkımızda/iletişim,
işletme bilgileri) içindedir. Üretilen HTML'i elle düzenleme; kaynağı düzenleyip `python3 -B _seo/seo.py` çalıştır.
Ayrıntılar: `_seo/SEO-REHBERI.md`, `_kaynak/gorsel/BENIOKU.md`.

## YAPILACAKLAR (Mac'te proje çekildiğinde sırayla yap)

Kullanıcı "projeyi çek" dediğinde önce `git pull`, sonra aşağıdaki açık maddeleri kullanıcıya hatırlat
ve onayını alarak yap. Biten maddeyi bu listeden sil ve commit et.

### 1. Blog ve kullanım kartı görsellerini Gemini ile üret
Bulut oturumunda Gemini anahtarı olmadığı için yapılamadı. Mac'te anahtar
`../tankled-otomasyon/.env` içindeki `GEMINI_API_KEY`'den otomatik okunur.

```bash
python3 _kaynak/gorsel/blog_gorsel.py     # 17 blog kapağı + 4 kullanım kartı (assets/blog, assets/kullanim)
```

- Üretilen her görseli aç ve kontrol et: ürün tasarımı (ahşap gövde, cam hazne, üst LED) bozulmuş mu,
  yazı/logo/filigran var mı, sahne yazının konusuyla uyumlu mu? Kötü olanı yeniden üret:
  `python3 _kaynak/gorsel/blog_gorsel.py <slug> --yeniden` (kart için `kullanim/abajur` gibi).
- Sonra `python3 -B _seo/seo.py` çalıştır; sayfalar yeni görselleri otomatik kullanır.
- Blog yazılarına ve kullanım kartlarına küçük bir "Bazı görseller yapay zekâ ile üretilmiş temsilî
  görsellerdir." notu ekle (bitkiler sayfasındaki gibi).
- Görselleri kullanıcıya gösterip onay aldıktan sonra commit et, push et ve `main`'e al.

### 2. Kullanıcıdan gelecek gerçek fotoğrafları yerleştir
Hakkımızda ve Betta sayfalarında "Fotoğraf eklenecek" kutuları var (`_seo/sayfalar.py` → `foto_yer`).
Kutulardaki HTML yorumunda önerilen dosya adı yazıyor (ör. `assets/hakkimizda/tankled-atolye-ostim-ankara.webp`).
Fotoğraflar gelince WebP'ye çevir, bu adlarla kaydet ve kutuların yerine gerçek görselleri koy.

### 3. Kullanıcıdan beklenen bilgiler (gelince `_seo/sayfalar.py` → `ISLETME` / `YORUMLAR`)
- Atölyenin açık adresi (sokak, no, posta kodu; Ostim, Yenimahalle, Ankara) ve çalışma saatleri
- Gerçek müşteri yorumları (izinli; uydurma yorum ekleme)
- Endonezya'dan gelen özel seri ağacının adı (tik mi?) ve "tik yağı ile korumalı" bilgisinin doğruluğu

### 4. Bilinen hata
Ana sayfada `assets/aydinlatma-bari.jpg` görseli eksik (kırık görsel). Kullanıcıdan görseli iste ya da referansı kaldır.

## Bilinen işletme bilgileri (değiştirme, her yerde birebir aynı olmalı)
- Atölye: Ostim, Yenimahalle, Ankara · Tel: +90 531 217 2006 · tankledaquarium@gmail.com
- Betta Serisi 1.300 TL (doğal çam ahşap), Özel Betta Serisi 1.500 TL (Endonezya ithal ağaç), Nano Serisi 2.500 TL'den
- Türkiye'nin 81 iline ve yurt dışına kargo
- Ürünler akvaryum, teraryum, abajur ve bitki saksısı olarak kullanılabilir
