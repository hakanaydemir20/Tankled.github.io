# Tür görselleri

Balıklar ve Bitkiler sayfalarında görseli olmayan türler için Gemini ile görsel üretir (800x600 JPEG).
Veri dosyasına yeni tür eklendikten sonra:

```bash
cd ../tankled-otomasyon && .venv/bin/python ../Tankled.github.io/_kaynak/gorsel/tur_gorsel.py
```

Belirli bir türü yeniden üretmek: `... tur_gorsel.py neon-tetra --yeniden`
