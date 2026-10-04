# Betta 3D modeli (Blender 5.x)

- `betta_gercekci.py`: modeli, malzemeleri ve 3 sn yüzme döngüsünü kurar → `betta_gercekci.blend`
- `betta_web_disa_aktar.py`: dokuları pişirip web için animasyonlu GLB üretir

Güncelleme:
```bash
Blender -b --factory-startup --python betta_gercekci.py
Blender -b betta_gercekci.blend --python betta_web_disa_aktar.py -- ../../assets/modeller/betta.glb
```
Sayfa (`assets/akvaryum-3d.js`) `assets/modeller/betta.glb` dosyasını yükler; yoksa kodla çizilen betta kullanılır.
Boyut ayarı: `BETTA_OLCEK`.
