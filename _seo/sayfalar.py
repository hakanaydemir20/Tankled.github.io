"""Hizmet, hakkimizda ve iletisim sayfalari: icerik burada, sayfalar kendi klasorlerine uretilir.

Calistirmak icin: python3 -B _seo/seo.py  (seo.py once bu sayfalari uretir, sonra SEO etiketlerini yazar.)
"""

from urllib.parse import quote

import blog

KOK = blog.KOK
# ----------------------------------------------------------------- isletme bilgileri
# Bos birakilan alanlar sitede gosterilmez. Doldurup `python3 -B _seo/seo.py` calistirin;
# adres/saat/fiyat tum sayfalara ve Google'in okudugu yapisal veriye birebir ayni islenir.
ISLETME = {
    "sokak": "100. Yıl Blv.",          # ornek: "1234. Cadde No: 5"  (Google Isletme Profili ile birebir ayni)
    "posta_kodu": "06374",     # ornek: "06374"
    "saatler": [("Pazartesi-Cumartesi", "Mo-Sa", "10:00", "16:00")],        # ornek: [("Pazartesi-Cuma", "Mo-Fr", "09:00", "18:00"), ("Cumartesi", "Sa", "10:00", "16:00")]
    "fiyat_baslangic": "1.300",  # ornek: "2.500"  -> "Fiyatlar 2.500 TL'den başlar"
    "kurulus_yili": "",     # ornek: "2021"
    "usta_hikayesi": """<h2>Hikâyemiz</h2>
<p>Tankled'ın temelinde, imalat sektöründe <strong>on yılı aşan üretim tecrübesi</strong> ve bir mühendisin titizliği var. Akvaryuma bir tutku olarak, hobi olarak başladık. Ama çok geçmeden raflardaki akvaryumların bize yetmediğini fark ettik: Çoğu, içi doldurulmayı bekleyen cansız bir cam kutudan ibaretti.</p>
<p>Biz başka bir şey istiyorduk. Her köşesi doğal, nefes alan, bulunduğu mekânla bütünleşen ve bir kez baktığınızda gözünüzü ayıramadığınız <strong>yaşayan bir obje</strong>. Bu fikrin peşinden giderek <strong>altı ay süren bir Ar-Ge ve geliştirme süreci</strong> yürüttük. Oranlardan ahşap birleşimlerine, buhar kapağının sürgüsünden ışığın renk sıcaklığına kadar her detayı mühendislik disipliniyle tasarladık, prototipledik ve defalarca test ettik.</p>
<p>Bu sürecin sonunda ortaya <a href="../betta-akvaryumu/">Betta Serisi</a> çıktı: Estetiği işlevden, zanaati mühendislikten ayırmayan bir tasarım.</p>
<h2>Her parça, elde ve tek tek</h2>
<p>Bugün <strong>Ankara Ostim</strong>'deki atölyemizde her parçayı en ince dokunuşlarla, her detayını düşünerek, elimizle ve özenle üretiyoruz. Seri üretim yapmıyoruz; çünkü her ahşabın damarı farklı ve her parça kendi karakterini taşımayı hak ediyor.</p>
FOTO_YER_ATOLYE""",    # hakkimizda sayfasi icin birkac cumlelik HTML paragraf
}

# Yalnizca GERCEK musteri yorumlari (Google yorumlarindan izinle alinmis). Bos ise bolum gosterilmez.
# ornek: {"ad": "Ayşe K.", "metin": "...", "kaynak": "Google"}
YORUMLAR = []

# Hizmet sayfalarindaki foto galerileri (assets/ altindaki gercek urun fotograflari)
GALERI_MOBILYALI = [
    ("assets/galeri/urun-isik-3000k-45-derece.jpg", "Mobilyalı akvaryum 3000K sıcak ışıkta, bitkili kurulum"),
    ("assets/galeri/urun-bicim-02-sol-45.jpg", "Ahşap gövdeli akvaryum sol çapraz açı"),
    ("assets/galeri/urun-detay-11-ahsap-damari-arka.jpg", "Doğal masif ahşap gövdenin damar dokusu"),
    ("assets/galeri/urun-bicim-09-ust-kapak-tepeden.jpg", "Sürgülü buhar kapağı, tepeden görünüm"),
    ("assets/galeri/urun-isik-6500k-onden.jpg", "6500K gün ışığında taş düzenli kurulum"),
    ("assets/galeri/urun-bicim-06-tam-arka.jpg", "Ahşap gövdenin arka görünümü"),
]
GALERI_BETTA = [
    ("assets/galeri/urun-bicim-01-tam-onden.jpg", "Betta Serisi önden görünüm"),
    ("assets/galeri/urun-isik-3000k-onden.jpg", "Betta Serisi 3000K sıcak ışık"),
    ("assets/galeri/urun-isik-4500k-onden.jpg", "Betta Serisi 4500K nötr ışık"),
    ("assets/galeri/urun-isik-6500k-onden.jpg", "Betta Serisi 6500K gün ışığı"),
    ("assets/galeri/urun-bicim-04-tam-sag-yan.jpg", "Betta Serisi yan profil ve ışık düğmesi"),
    ("assets/galeri/urun-bicim-07-yuksekten-45.jpg", "Betta Serisi yukarıdan çapraz açı"),
]


def fiyat_cumlesi() -> str:
    f = ISLETME["fiyat_baslangic"]
    return f"<p><strong>Fiyatlar {f} TL'den başlar</strong> (hazır <a href=\"../betta-akvaryumu/\">Betta Serisi</a>; Nano Serisi 2.500 TL'den başlar). Özel ölçüde fiyat; ölçü, malzeme ve kuruluma göre belirlenir.</p>" if f else ""


def adres_metni() -> str:
    ilce = f"{ISLETME['posta_kodu']} Yenimahalle".strip()
    return ", ".join(p for p in [ISLETME["sokak"], "Ostim", ilce, "Ankara"] if p)


def saatler_html() -> str:
    if not ISLETME["saatler"]:
        return "<li><strong>Çalışma saatleri:</strong> Atölye ziyaretleri için lütfen önceden haber verin.</li>"
    return "<li><strong>Çalışma saatleri:</strong> " + ", ".join(f"{g} {a}–{k}" for g, _, a, k in ISLETME["saatler"]) + "</li>"


def foto_yer(kutular: list) -> str:
    """Henuz eklenmemis gercek fotograflar icin bos kutular. Fotograf gelince GALERI listelerine tasiyin."""
    return ('<div class="foto-grid">' + "".join(
        f'<figure class="foto-yer"><!-- {dosya} --><span>Fotoğraf eklenecek</span><figcaption>{alt}</figcaption></figure>'
        for dosya, alt in kutular) + "</div>")


def foto_grid(fotolar: list, onek: str) -> str:
    return ('<div class="foto-grid">' + "".join(
        f'<img src="{onek}{y}" alt="{alt}" width="750" height="1000" loading="lazy" />' for y, alt in fotolar) + "</div>")


WA = "https://wa.me/905312172006?text=Merhaba%20Tankled%2C%20bilgi%20almak%20istiyorum."

# tur: "hizmet" -> Service, "hakkimizda" -> AboutPage, "iletisim" -> ContactPage yapisal verisi
SAYFALAR = [
    {
        "yol": "mobilyali-akvaryum/", "tur": "hizmet", "kisa": "Mobilyalı Akvaryum",
        "hizmet": "Mobilyalı akvaryum üretimi",
        "baslik": "Mobilyalı Akvaryum Ankara | Ahşap Gövdeli Akvaryum | Tankled",
        "aciklama": "Ankara Ostim atölyemizde doğal masif ahşaptan mobilyalı akvaryum üretiyoruz: konsol, sehpa, "
                    "TV ünitesi ve masaüstü modeller, ölçüye özel tasarım.",
        "h1": "Mobilyalı akvaryum: Ankara'da el yapımı, ahşap gövdeli",
        "gorsel": "assets/about.webp", "gorsel_g": 893, "gorsel_y": 1600,
        "gorsel_alt": "Doğal masif ahşap gövdeli mobilyalı akvaryum salonda",
        "govde": """
<p>Tankled <strong>mobilyalı akvaryum</strong>ları, cam hazne ile ahşap gövdenin baştan birlikte tasarlandığı, Ankara Ostim'deki atölyemizde elde üretilen akvaryumlardır. Akvaryum, salonunuzda teknik bir cihaz gibi değil; konsolunuz, sehpanız ya da kitaplığınızla aynı dili konuşan bir mobilya gibi durur.</p>

<h2>Neden mobilyalı akvaryum?</h2>
<ul>
  <li><strong>Güvenli taşıma:</strong> Gövde, su dolu akvaryumun ağırlığını taşıyacak şekilde üretilir; sıradan bir sehpanın zamanla esneme riski yoktur.</li>
  <li><strong>Gizli ekipman:</strong> Kablolar, aydınlatma ve bakım malzemeleri gövdenin içinde kalır.</li>
  <li><strong>Dekorasyonla bütünlük:</strong> Ahşap tonu ve ölçü, evinizdeki mobilyalara göre seçilir.</li>
  <li><strong>Kolay bakım:</strong> Buhar kapağı ve ayarlanabilir LED ışık, buharlaşmayı ve yosunu azaltır.</li>
</ul>

<h2>Modeller</h2>
<ul>
  <li><strong>Masaüstü mobilyalı akvaryum:</strong> Çalışma masası, komodin ve raflar için. Örnek: <a href="../betta-akvaryumu/">Betta Serisi</a> (14 × 14 × 20 cm).</li>
  <li><strong>Konsol ve TV ünitesi akvaryum:</strong> Salonun ana duvarı için, ölçüye göre.</li>
  <li><strong>Sehpa akvaryum:</strong> Orta ya da yan sehpanın içine yerleştirilen, üstten izlenen modeller.</li>
  <li><strong>Teraryum ve paludaryum gövdeleri:</strong> Aynı ahşap gövde, <a href="../teraryum/">teraryum</a> ya da <a href="../paludaryum/">paludaryum</a> olarak da kurulabilir.</li>
</ul>

<h2>Fotoğraflar</h2>
FOTO_MOBILYALI
<p>Daha fazla kurulum için <a href="../galeri/">galeriye</a> bakın.</p>

<h2>Malzeme: doğal masif ahşap</h2>
<p>Gövdelerimizde iki seçenek sunuyoruz: sıcak tonlu, <strong>eşsiz doğal çam ahşap</strong> ve <strong>Endonezya'dan ithal edilen, eşi benzeri olmayan doğal desenlere sahip özel ağaç</strong>. Akvaryum çevresi nemli bir ortam olduğu için yüzey tik yağıyla korunur. Her parçanın damar deseni farklı olduğu için iki ürün birbirinin aynısı olmaz.</p>

<h2>Nasıl sipariş verilir?</h2>
<ol>
  <li>Akvaryumun duracağı yeri ve ölçüsünü bize iletin (fotoğraf yeterli).</li>
  <li>Birlikte model, ahşap ve ışık tonunu seçelim; <a href="../akvaryum-olustur/">3D tasarım aracımızla</a> ön izleme yapabilirsiniz.</li>
  <li>Atölyemizde üretim yapılır; isterseniz hazır kurulum (zemin, bitki, filtre) ile teslim ederiz.</li>
</ol>
<p>Ölçüye özel üretimin ayrıntıları için <a href="../ozel-olcu-akvaryum/">özel ölçü akvaryum</a> sayfamıza, seçim ipuçları için <a href="../blog/mobilyali-akvaryum-nedir/">mobilyalı akvaryum nedir</a> yazımıza bakın.</p>
""",
    },
    {
        "yol": "ozel-olcu-akvaryum/", "tur": "hizmet", "kisa": "Özel Ölçü Akvaryum",
        "hizmet": "Özel ölçü akvaryum üretimi",
        "baslik": "Özel Ölçü Akvaryum Yaptırma Ankara | Tankled",
        "aciklama": "Ankara'da özel ölçü akvaryum yaptırın: nişe, konsola ya da TV ünitesine tam oturan, masif "
                    "ahşap gövdeli el yapımı akvaryum. Adım adım sipariş süreci.",
        "h1": "Özel ölçü akvaryum: evinize göre tasarlanır, Ankara'da üretilir",
        "gorsel": "assets/galeri/urun-bicim-10-uzaktan-tam-govde.jpg", "gorsel_g": 750, "gorsel_y": 1000,
        "gorsel_alt": "Ölçüye özel üretilmiş ahşap gövdeli akvaryum tam görünüm",
        "govde": """
<p>Hazır akvaryumlar çoğu zaman evinizdeki boşluğa ya da mobilyalarınıza tam uymaz. <strong>Özel ölçü akvaryum</strong> ise duvar nişine, TV ünitesine, konsolun üstüne ya da bir köşeye santimi santimine oturacak şekilde tasarlanır. Tankled olarak tüm akvaryumlarımızı Ankara Ostim'deki atölyemizde elde üretiyoruz; bu yüzden ölçü, ahşap, ışık ve kapak detaylarını size göre değiştirebiliyoruz.</p>

<h2>Neleri size göre belirliyoruz?</h2>
<ul>
  <li><strong>Ölçü ve hacim:</strong> Genişlik, derinlik, yükseklik; bakmak istediğiniz canlılara uygun litre.</li>
  <li><strong>Gövde:</strong> Doğal masif ahşap gövde, yüzey yağı ve renk tonu.</li>
  <li><strong>Aydınlatma:</strong> 3000K sıcak, 4500K nötr ve 6500K gün ışığı LED seçenekleri.</li>
  <li><strong>Kullanım:</strong> Akvaryum, <a href="../paludaryum/">paludaryum</a> ya da <a href="../teraryum/">teraryum</a>.</li>
  <li><strong>Kurulum:</strong> Boş teslim ya da zemin, bitki ve ekipmanla hazır kurulum.</li>
</ul>

<h2>Sipariş süreci</h2>
<ol>
  <li><strong>Ön görüşme:</strong> Telefon, WhatsApp ya da <a href="../iletisim/">iletişim formu</a> ile alanın ölçüsünü ve fotoğrafını paylaşırsınız.</li>
  <li><strong>Tasarım:</strong> Ölçü, malzeme ve ışığı birlikte belirleriz. <a href="../akvaryum-olustur/">3D akvaryum tasarım aracımızla</a> litre ve ışık ihtiyacını önceden görebilirsiniz.</li>
  <li><strong>Üretim:</strong> Akvaryum atölyemizde tek tek üretilir; silikon ve cam işçiliği kontrol edilir.</li>
  <li><strong>Teslim ve kurulum:</strong> İsterseniz hazır kurulumla teslim ederiz; ilk haftalarda bakım konusunda destek veririz.</li>
</ol>

<h2>Fiyat</h2>
FIYAT
<p>Özel ölçü akvaryumun fiyatı; ölçüye, cam kalınlığına, gövde malzemesine ve hazır kurulum isteyip istemediğinize göre belirlenir. Alanınızın ölçüsünü gönderin, size net teklif hazırlayalım.</p>

<h2>Ölçü seçerken dikkat edilecekler</h2>
<p>Su dolu bir akvaryum litre başına yaklaşık bir kilogram ağırlık demektir; zemin ve taşlarla bu ağırlık artar. Akvaryumun üstünde bakım için 15–20 cm boşluk bırakın, doğrudan güneş alan ve kaloriferin hemen yanındaki yerlerden kaçının. Daha fazla ipucu için <a href="../blog/ankara-akvaryum-rehberi/">Ankara'da akvaryum seçme rehberimizi</a> okuyun.</p>
""",
    },
    {
        "yol": "betta-akvaryumu/", "tur": "hizmet", "kisa": "Betta Akvaryumu",
        "hizmet": "Betta akvaryumu",
        "baslik": "Betta Akvaryumu: Ahşap Gövdeli Betta Serisi | Tankled",
        "aciklama": "Tankled Betta Serisi: 14 × 14 × 20 cm, doğal masif ahşap gövde, sürgülü buhar kapağı ve üç "
                    "ışık tonlu LED. Ankara'da el yapımı betta akvaryumu.",
        "h1": "Betta akvaryumu: Tankled Betta Serisi",
        "gorsel": "assets/g-betta-cozy.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Tankled Betta Serisi betta akvaryumu oturma odasında",
        "govde": """
<p><strong>Betta Serisi</strong>, betta balığı için tasarladığımız, Ankara'daki atölyemizde doğal masif ahşaptan elde üretilen kompakt bir akvaryumdur. Çalışma masası, komodin ya da kitaplık rafı için idealdir; akşamları sıcak ışığıyla bir abajur gibi, gündüz gün ışığı tonuyla bitkili bir mini doğa gibi görünür.</p>

<h2>Teknik özellikler</h2>
<ul>
  <li><strong>Ölçü:</strong> 14 × 14 × 20 cm</li>
  <li><strong>Gövde:</strong> Doğal çam ahşap ya da Endonezya'dan ithal doğal desenli ağaç (Özel Betta Serisi); yüzey tik yağıyla korunur</li>
  <li><strong>Kapak:</strong> Sürgülü buhar kapağı (buharlaşmayı azaltır, bettanın zıplamasını önler)</li>
  <li><strong>Aydınlatma:</strong> 3000K, 4500K ve 6500K olmak üzere üç ışık tonlu LED</li>
  <li><strong>Elektrik:</strong> 220V</li>
  <li><strong>Sistem:</strong> Low-tech; CO₂ ve yoğun gübre gerektirmez</li>
</ul>

<h2>Seriler ve fiyatlar</h2>
<ul>
  <li><strong>Betta Serisi: 1.300 TL.</strong> Sıcak tonlu, eşsiz doğal çam ahşap gövde.</li>
  <li><strong>Özel Betta Serisi: 1.500 TL.</strong> Endonezya'dan ithal edilen, eşi benzeri olmayan doğal desenlere sahip, bambaşka bir ağaç. Her gövdenin deseni tektir.</li>
</ul>
FOTO_YER_SERI
<h2>Kargo</h2>
<p>Tüm modellerimizi Türkiye'nin 81 iline kargoyla gönderiyoruz; yurt dışına da kargo yapılabilir. Akvaryum, ahşap gövde ve cam hazne güvenli şekilde paketlenir.</p>
<h2>Tek tasarım, dört kullanım</h2>
<p>Betta Serisi yalnızca bir akvaryum değil, ihtiyacınıza göre dönüşen bir yaşam alanıdır:</p>
<ul>
  <li><strong>Akvaryum:</strong> Betta, karides ya da bitkili nano akvaryum.</li>
  <li><strong>Teraryum:</strong> Yosun ve tropikal bitkilerle kapalı bir mini orman. <a href="../blog/teraryum-nasil-yapilir/">Teraryum nasıl yapılır?</a></li>
  <li><strong>Abajur ve gece lambası:</strong> 3000K sıcak ışığıyla salonda dekoratif abajur, yatak odasında gece lambası. <a href="../blog/dekoratif-abajur-fikirleri/">Dekoratif abajur fikirleri</a></li>
  <li><strong>Bitki saksısı:</strong> Kendi LED ışığıyla penceresiz köşede bile sukulent ve kaktüs yetiştirin. <a href="../blog/isikli-bitki-saksisi/">Işıklı bitki saksısı rehberi</a></li>
</ul>
<p>Ayrıca egzotik hayvan yuvası ya da aksesuar kutusu olarak da kullanılabilir. Uygun canlıları <a href="../baliklar/">balıklar rehberimizde</a>, bitkileri <a href="../bitkiler/">bitkiler rehberimizde</a> bulabilirsiniz.</p>

<h2>Hazır kurulum seti</h2>
<p>Talep üzerine Betta Serisi'ni zemin, canlı bitkiler ve ekipmanla hazır kurulmuş olarak teslim ediyoruz. Kendiniz kurmak isterseniz <a href="../blog/betta-akvaryumu-kurulumu/">betta akvaryumu kurulum rehberimiz</a> ve <a href="../blog/nano-akvaryum-bakimi/">nano akvaryum bakım rutinimiz</a> adım adım yol gösterir.</p>

<h2>Fotoğraflar</h2>
FOTO_BETTA
<p>Betta Serisi'nin farklı açılardan ve üç ışık tonunda görüntülerini <a href="../galeri/">galeride</a> inceleyebilirsiniz. Daha büyük ya da farklı ölçüde bir model isterseniz <a href="../ozel-olcu-akvaryum/">özel ölçü akvaryum</a> sayfamıza bakın.</p>
""",
    },
    {
        "yol": "teraryum/", "tur": "hizmet", "kisa": "Teraryum",
        "hizmet": "Teraryum üretimi",
        "baslik": "Teraryum Ankara: El Yapımı Ahşap Teraryum | Tankled",
        "aciklama": "Ankara'da el yapımı teraryum: doğal masif ahşap gövdeli, ışıklı ve kapaklı teraryumlar. "
                    "Bitki teraryumu ve gecko gibi egzotik hayvanlar için yaşam alanı.",
        "h1": "Teraryum: Ankara'da el yapımı, ahşap gövdeli",
        "gorsel": "assets/g-gecko.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Orman temalı ahşap gövdeli teraryum",
        "govde": """
<p><strong>Teraryum</strong>, bitkilerin ya da küçük kara hayvanlarının yaşadığı, camla çevrili bir mini ekosistemdir. Tankled teraryumları, akvaryumlarımızla aynı doğal masif ahşap gövde ve LED aydınlatmayla Ankara Ostim'deki atölyemizde elde üretilir.</p>

<h2>Teraryum türleri</h2>
<ul>
  <li><strong>Kapalı (tropikal) bitki teraryumu:</strong> Yüksek nem seven fittonia, eğrelti, selaginella ve yosunlarla kurulur; kendi nem döngüsünü oluşturur.</li>
  <li><strong>Açık (kuru) teraryum:</strong> Sukulent ve kaktüs gibi kuru ortam bitkileri için havalandırmalı düzen.</li>
  <li><strong>Hayvan teraryumu:</strong> Gecko gibi küçük egzotik hayvanlar için; türün sıcaklık ve nem ihtiyacına göre planlanır.</li>
</ul>

<h2>Neden ahşap gövdeli teraryum?</h2>
<p>Ahşap gövde, teraryumu bir dekorasyon objesine dönüştürür ve LED aydınlatmayı gizler. Tik yağıyla korunan ahşap yüzey nemli ortama dayanıklıdır; üç ışık tonu (3000K, 4500K, 6500K) hem bitkilerin ihtiyacını karşılar hem de akşamları yumuşak bir ortam ışığı sağlar.</p>

<h2>Bakım</h2>
<p>Kurulum ve bitki seçimi için <a href="../blog/teraryum-nasil-yapilir/">teraryum nasıl yapılır</a> ve <a href="../blog/teraryum-bitkileri-ve-bakimi/">teraryum bitkileri ve bakımı</a> rehberlerimize bakın. Aynı ahşap gövdeli teraryum akşamları sıcak ışığıyla bir <a href="../blog/gece-lambasi-olarak-isikli-teraryum/">gece lambası</a> olarak da kullanılabilir.</p>
<p>Kapalı bitki teraryumları çok az bakım ister: ara sıra püskürtme, kuruyan yaprakların alınması ve cam yoğuşması fazlaysa kapağın kısa süre açılması yeterlidir. Teraryuma uygun bitkileri <a href="../bitkiler/">bitkiler rehberimizde</a> bulabilirsiniz.</p>

<p>Su ve kara bölümünü bir arada istiyorsanız <a href="../paludaryum/">paludaryum</a> sayfamıza, ölçüye özel üretim için <a href="../ozel-olcu-akvaryum/">özel ölçü</a> sayfamıza bakın.</p>
""",
    },
    {
        "yol": "paludaryum/", "tur": "hizmet", "kisa": "Paludaryum",
        "hizmet": "Paludaryum üretimi",
        "baslik": "Paludaryum Ankara: El Yapımı Paludaryum | Tankled",
        "aciklama": "Su ve kara bölümü bir arada: Ankara'da el yapımı paludaryum. Yengeç, karides ve bitkiler "
                    "için ahşap gövdeli, ışıklı paludaryum kurulumları.",
        "h1": "Paludaryum: su ve karanın bir arada olduğu yaşam alanı",
        "gorsel": "assets/g-paludarium-open.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Ön açılır camlı el yapımı paludaryum",
        "govde": """
<p><strong>Paludaryum</strong>, bir bölümü su, bir bölümü kara olan; akvaryum ile teraryumu birleştiren yaşam alanıdır. Nehir kıyısı, bataklık ya da yağmur ormanı zemini gibi doğal ortamları evinize taşır. Tankled paludaryumları Ankara Ostim'deki atölyemizde elde üretilir.</p>

<h2>Paludaryumda neler yaşar?</h2>
<ul>
  <li><strong>Canlılar:</strong> Vampir yengeç ve kızıl yengeç gibi yarı karasal türler, karidesler, salyangozlar ve küçük balıklar. Türlere <a href="../baliklar/">balıklar rehberimizden</a> bakabilirsiniz.</li>
  <li><strong>Su bitkileri:</strong> Anubias, java eğreltisi, bucephalandra, cryptocoryne.</li>
  <li><strong>Kara ve nem bitkileri:</strong> Fittonia, pothos, philodendron, bromelya, tillandsia, yosunlar. Tüm bitkileri <a href="../bitkiler/">bitkiler rehberimizde</a> "paludaryum" filtresiyle görebilirsiniz.</li>
</ul>

<h2>Tankled paludaryum özellikleri</h2>
<ul>
  <li>Doğal masif ahşap gövde ve metal ayaklı modeller</li>
  <li>Bakımı kolaylaştıran ön açılır cam seçeneği</li>
  <li>Bitkiler için ayarlanabilir LED aydınlatma</li>
  <li>Ölçüye özel üretim ve hazır kurulum</li>
</ul>

<h2>Bakım ipuçları</h2>
<p>Paludaryumda nem yüksek tutulur; su bölümünde haftalık kısmi su değişimi, kara bölümünde ara sıra püskürtme ve budama yeterlidir. Yarı karasal yengeçler kaçmaya meyillidir, bu yüzden kapağın sıkı kapanması önemlidir.</p>

<p>Paludaryum fikirleri için <a href="../blog/ahsap-akvaryum-fikirleri/">ahşap akvaryum fikirleri</a> yazımıza, kara ağırlıklı bir düzen için <a href="../teraryum/">teraryum</a> sayfamıza bakın.</p>
""",
    },
    {
        "yol": "hakkimizda/", "tur": "hakkimizda", "kisa": "Hakkımızda",
        "baslik": "Hakkımızda: Ankara Ostim Akvaryum Atölyesi | Tankled",
        "aciklama": "Tankled, Ankara Ostim'de doğal masif ahşaptan mobilyalı akvaryum, teraryum ve paludaryum "
                    "üreten bir el yapımı akvaryum atölyesidir. Hikayemiz ve yaklaşımımız.",
        "h1": "Hakkımızda: Ankara'da el yapımı akvaryum atölyesi",
        "gorsel": "assets/g-lineup.webp", "gorsel_g": 1122, "gorsel_y": 1402,
        "gorsel_alt": "Tankled atölyesinde üretilen akvaryum koleksiyonu",
        "govde": """
<p>Tankled, bir akvaryumun yalnızca bir cam kap değil; mekânın ruhunu değiştiren, yaşayan bir tasarım nesnesi olabileceği inancıyla doğdu. <strong>Ankara Ostim</strong>'deki atölyemizde akvaryum, teraryum ve paludaryumları doğal masif ahşaptan, elde ve tek tek üretiyoruz.</p>

HIKAYE
<h2>Yaklaşımımız</h2>
<ul>
  <li><strong>Tasarım odaklı:</strong> Her parça mimari bir obje gibi, bulunacağı mekânla birlikte düşünülür.</li>
  <li><strong>El işçiliği:</strong> Gövde, cam ve aydınlatma atölyemizde tek tek hazırlanır ve kontrol edilir. Her parçanın ahşap damarı farklı olduğu için her ürün kendine özgüdür.</li>
  <li><strong>Sorumlu üretim:</strong> Doğaya saygılı, geri dönüştürülebilir malzemeler kullanırız.</li>
  <li><strong>Kolay bakım:</strong> Ürünlerimiz low-tech sistemlerdir; sürekli bakım ve teknik bilgi gerektirmez.</li>
</ul>

<h2>Neler üretiyoruz?</h2>
<ul>
  <li><a href="../mobilyali-akvaryum/">Mobilyalı akvaryum</a></li>
  <li><a href="../betta-akvaryumu/">Betta akvaryumu (Betta Serisi)</a></li>
  <li><a href="../ozel-olcu-akvaryum/">Özel ölçü akvaryum</a></li>
  <li><a href="../teraryum/">Teraryum</a> ve <a href="../paludaryum/">paludaryum</a></li>
</ul>

<h2>Bilgi paylaşımı</h2>
<p>Akvaryumun keyifli olması doğru bilgiyle başlar. Bu yüzden <a href="../bitkiler/">bitkiler</a>, <a href="../baliklar/">balıklar</a> ve <a href="../malzemeler/">malzemeler</a> rehberlerimizi ve <a href="../blog/">blog yazılarımızı</a> herkesin kullanımına açık tutuyoruz.</p>

<h2>Atölyemizi ziyaret edin</h2>
<p>Ürünlerimizi Ankara Ostim'deki atölyemizde yerinde görebilirsiniz. Ziyaret öncesinde <a href="../iletisim/">iletişim sayfamızdan</a> bize ulaşmanızı öneririz.</p>
""",
    },
    {
        "yol": "iletisim/", "tur": "iletisim", "kisa": "İletişim",
        "baslik": "İletişim: Tankled Akvaryum Atölyesi Ostim, Ankara",
        "aciklama": "Tankled iletişim: Ostim, Yenimahalle, Ankara. Telefon +90 531 217 2006, WhatsApp ve e-posta. "
                    "Mobilyalı ve özel ölçü akvaryum için bize ulaşın.",
        "h1": "İletişim: Ankara Ostim'deki atölyemize ulaşın",
        "gorsel": None,
        "govde": """
<p>Mobilyalı akvaryum, özel ölçü akvaryum, betta akvaryumu, teraryum ya da paludaryum için bize aşağıdaki kanallardan ulaşabilirsiniz. Alanınızın ölçüsünü ve bir fotoğrafını paylaşırsanız size en uygun seçeneği birlikte belirleyelim.</p>

<h2>İletişim bilgileri</h2>
<ul>
  <li><strong>Atölye adresi:</strong> ADRES</li>
  SAATLER
  <li><strong>Kargo:</strong> Türkiye'nin 81 iline ve yurt dışına</li>
  <li><strong>Telefon:</strong> <a href="tel:+905312172006">+90 531 217 2006</a></li>
  <li><strong>WhatsApp:</strong> <a href="WA_LINK" target="_blank" rel="noopener">WhatsApp ile yazın</a></li>
  <li><strong>E-posta:</strong> <a href="mailto:tankledaquarium@gmail.com">tankledaquarium@gmail.com</a></li>
  <li><strong>Instagram:</strong> <a href="https://www.instagram.com/tankled.akvaryum/" target="_blank" rel="noopener">@tankled.akvaryum</a></li>
</ul>
<p>Atölye ziyaretleri için önceden haber vermenizi rica ederiz. Mesajlarınıza en kısa sürede dönüş yapıyoruz.</p>

<h2>Konum</h2>
<iframe title="Tankled atölyesi konumu: Ostim, Yenimahalle, Ankara" src="HARITA" width="100%" height="360" style="border:0;border-radius:18px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>

<h2>Göndermeden önce</h2>
<p>Ne istediğinizden emin değilseniz <a href="../akvaryum-olustur/">3D akvaryum tasarım aracımızla</a> ölçü ve ışığı deneyebilir, <a href="../galeri/">galeride</a> örnek kurulumlara, <a href="../blog/">blogda</a> rehber yazılarımıza göz atabilirsiniz.</p>
""",
    },
]


def uret() -> None:
    onek = "../"
    for s in SAYFALAR:
        if s["gorsel"]:
            boyut = f' width="{s["gorsel_g"]}" height="{s["gorsel_y"]}"' if s["gorsel_g"] else ""
            kapak = f'      <img class="kapak" src="{onek}{s["gorsel"]}" alt="{s["gorsel_alt"]}"{boyut} />\n'
        else:
            kapak = ""
        hikaye = ""
        if ISLETME["kurulus_yili"]:
            hikaye += f"<p>{ISLETME['kurulus_yili']} yılından bu yana Ankara'da el yapımı akvaryum üretiyoruz.</p>\n"
        if ISLETME["usta_hikayesi"]:
            hikaye += ISLETME["usta_hikayesi"] + "\n"
        harita = "https://www.google.com/maps?q=" + quote("Tankled, " + adres_metni()) + "&amp;output=embed"
        icerik = (s["govde"].strip().replace("WA_LINK", WA).replace("FOTO_MOBILYALI", foto_grid(GALERI_MOBILYALI, onek))
                  .replace("FOTO_BETTA", foto_grid(GALERI_BETTA, onek)).replace("FIYAT", fiyat_cumlesi())
                  .replace("HIKAYE", hikaye)
                  .replace("FOTO_YER_ATOLYE", foto_yer([
                      ("assets/hakkimizda/tankled-atolye-ostim-ankara.webp", "Ostim'deki atölyemiz"),
                      ("assets/hakkimizda/el-yapimi-akvaryum-uretim.webp", "Elde üretim süreci"),
                      ("assets/hakkimizda/betta-serisi-ar-ge-prototip.webp", "Betta Serisi Ar-Ge ve prototipler")]))
                  .replace("FOTO_YER_SERI", foto_yer([
                      ("assets/betta/betta-serisi-cam-ahsap.webp", "Betta Serisi: doğal çam ahşap"),
                      ("assets/betta/ozel-betta-serisi-endonezya-agac.webp", "Özel Betta Serisi: Endonezya ağacı"),
                      ("assets/betta/ozel-betta-serisi-ahsap-desen.webp", "Özel seri doğal ahşap deseni")])).replace("ADRES", adres_metni()).replace("SAATLER", saatler_html())
                  .replace("HARITA", harita))
        govde = f"""    <article>
      <nav class="kirinti" aria-label="Sayfa yolu"><a href="{onek}">Ana sayfa</a> › {s["kisa"]}</nav>
      <span class="eyebrow">Tankled · Ankara</span>
      <h1>{s["h1"]}</h1>
{kapak}{icerik}
      <section class="cta">
        <h2>Ankara'da el yapımı akvaryum</h2>
        <p>Ostim'deki atölyemizde doğal masif ahşaptan mobilyalı ve dekoratif akvaryumlar üretiyoruz. Türkiye'nin 81 iline ve yurt dışına kargo yapıyoruz. Ölçünüze özel tasarım için bize ulaşın.</p>
        <a class="btn" href="{WA}" target="_blank" rel="noopener">WhatsApp ile yazın</a>
        <a class="btn" href="tel:+905312172006">Hemen arayın</a>
      </section>
    </article>"""
        hedef = KOK / s["yol"] / "index.html"
        hedef.parent.mkdir(exist_ok=True)
        hedef.write_text(blog.iskelet(s["baslik"], s["aciklama"], onek, govde), encoding="utf-8")


if __name__ == "__main__":
    uret()
