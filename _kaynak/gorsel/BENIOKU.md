# Tür görselleri

Balıklar ve Bitkiler sayfalarında görseli olmayan türler için Gemini ile görsel üretir (800x600 JPEG).
Veri dosyasına yeni tür eklendikten sonra:

```bash
cd ../tankled-otomasyon && .venv/bin/python ../Tankled.github.io/_kaynak/gorsel/tur_gorsel.py
```

Belirli bir türü yeniden üretmek: `... tur_gorsel.py neon-tetra --yeniden`

# Blog ve kullanım alanı görselleri

17 blog yazısı ve ana sayfadaki 4 "Kullanım alanları" kartı için Gemini ile 1200x900 WebP üretir
(`assets/blog/<slug>.webp`, `assets/kullanim/<ad>.webp`). Ürünün göründüğü sahnelerde gerçek ürün
fotoğrafı referans olarak gönderilir, böylece Tankled tasarımı korunur. Ek paket gerekmez (Pillow yeterli).

```bash
python3 _kaynak/gorsel/blog_gorsel.py        # eksikleri üret (GEMINI_API_KEY ya da ../tankled-otomasyon/.env)
python3 -B _seo/seo.py                       # sayfalar yeni görselleri otomatik kullanır
```

Beğenilmeyen bir görseli yeniden üretmek: `python3 _kaynak/gorsel/blog_gorsel.py abajur-slug --yeniden`
(kullanım kartları için ad: `kullanim/abajur`). Sahne tarifleri betikteki `SAHNE` sözlüğündedir.
