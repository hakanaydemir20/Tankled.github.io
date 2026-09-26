# Tankled 3D modelleri

"Akvaryumunuzu Oluşturun" sayfası (`akvaryum-olustur/`) bu klasördeki modelleri kullanır.
Bir model dosyası yüklenene kadar o seri sayfada "3D model yakında" olarak görünür; yüklendiğinde otomatik seçilebilir olur.

## Dosya adları

| Dosya | Seri |
|---|---|
| `betta-serisi.glb` | Betta Serisi |
| `nano-serisi.glb` | Nano Serisi |
| `paludarium-serisi.glb` | Paludarium Serisi |

## Dışa aktarma (Blender, SketchUp, Fusion 360 vb.)

- Biçim: **glTF Binary (.glb)**, dokular dosyanın içine gömülü olarak.
- **Draco sıkıştırmasını kapatın** (şu an desteklenmiyor).
- Modeli gerçek ölçüsünde dışa aktarın. Varsayılan birim **metre** kabul edilir (Blender varsayılanı). Farklıysa aşağıdaki `olcek` değerini değiştirin.
- Camın içini boş bırakın: zemin, su ve bitkiler sayfa tarafından camın içine yerleştirilir.
- Dosya boyutunu makul tutun (ideal olarak 10 MB altı), yoksa sayfa yavaş açılır.

## Ayarlar

Ölçüler `akvaryum-olustur/index.html` içindeki `MODELLER` listesinde:

- `ic`: camın **iç** ölçüsü (cm): uzunluk `L`, derinlik `W`, yükseklik `H`
- `icTaban`: modelin en alt noktasından cam içindeki tabana yükseklik (cm); ör. ahşap kaide 3 cm ise `3`
- `su`: su yüksekliği (cm), boş bırakılırsa camın 2 cm altı
- `olcek`: model birimini cm'ye çevirir; metre = `100`, santimetre = `1`, milimetre = `0.1`

Model yüklendikten sonra zemin ya da bitkiler camla hizalı görünmüyorsa bu değerleri düzeltmek yeterlidir.
