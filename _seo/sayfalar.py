"""Hizmet, hakkimizda ve iletisim sayfalari: icerik burada, sayfalar kendi klasorlerine uretilir.

Calistirmak icin: python3 -B _seo/seo.py  (seo.py once bu sayfalari uretir, sonra SEO etiketlerini yazar.)
"""

import blog

KOK = blog.KOK
WA = "https://wa.me/905312172006?text=Merhaba%20Tankled%2C%20bilgi%20almak%20istiyorum."

# tur: "hizmet" -> Service, "hakkimizda" -> AboutPage, "iletisim" -> ContactPage yapisal verisi
SAYFALAR = [
    {
        "yol": "mobilyali-akvaryum/", "tur": "hizmet", "kisa": "Mobilyalı Akvaryum",
        "hizmet": "Mobilyalı akvaryum üretimi",
        "baslik": "Mobilyalı Akvaryum Ankara | Ahşap Gövdeli Akvaryum | Tankled",
        "aciklama": "Ankara Ostim atölyemizde masif tik ahşaptan mobilyalı akvaryum üretiyoruz: konsol, sehpa, "
                    "TV ünitesi ve masaüstü modeller, ölçüye özel tasarım.",
        "h1": "Mobilyalı akvaryum: Ankara'da el yapımı, ahşap gövdeli",
        "gorsel": "assets/about.webp", "gorsel_g": 893, "gorsel_y": 1600,
        "gorsel_alt": "Masif tik ahşap gövdeli mobilyalı akvaryum salonda",
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

<h2>Malzeme: masif tik ahşap</h2>
<p>Akvaryum çevresi nemli bir ortamdır. Bu yüzden gövdelerimizde, doğal yağ oranı yüksek ve neme dayanıklı olduğu için tekne yapımında da kullanılan masif tik ahşabı tercih ediyoruz. Yüzey tik yağıyla korunur; her parçanın damar deseni farklı olduğu için iki ürün birbirinin aynısı olmaz.</p>

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
  <li><strong>Gövde:</strong> Masif tik ahşap gövde, yüzey yağı ve renk tonu.</li>
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

<h2>Ölçü seçerken dikkat edilecekler</h2>
<p>Su dolu bir akvaryum litre başına yaklaşık bir kilogram ağırlık demektir; zemin ve taşlarla bu ağırlık artar. Akvaryumun üstünde bakım için 15–20 cm boşluk bırakın, doğrudan güneş alan ve kaloriferin hemen yanındaki yerlerden kaçının. Daha fazla ipucu için <a href="../blog/ankara-akvaryum-rehberi/">Ankara'da akvaryum seçme rehberimizi</a> okuyun.</p>
""",
    },
    {
        "yol": "betta-akvaryumu/", "tur": "hizmet", "kisa": "Betta Akvaryumu",
        "hizmet": "Betta akvaryumu",
        "baslik": "Betta Akvaryumu: Ahşap Gövdeli Betta Serisi | Tankled",
        "aciklama": "Tankled Betta Serisi: 14 × 14 × 20 cm, masif tik ahşap gövde, sürgülü buhar kapağı ve üç "
                    "ışık tonlu LED. Ankara'da el yapımı betta akvaryumu.",
        "h1": "Betta akvaryumu: Tankled Betta Serisi",
        "gorsel": "assets/g-betta-cozy.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Tankled Betta Serisi betta akvaryumu oturma odasında",
        "govde": """
<p><strong>Betta Serisi</strong>, betta balığı için tasarladığımız, Ankara'daki atölyemizde masif tik ahşaptan elde üretilen kompakt bir akvaryumdur. Çalışma masası, komodin ya da kitaplık rafı için idealdir; akşamları sıcak ışığıyla bir abajur gibi, gündüz gün ışığı tonuyla bitkili bir mini doğa gibi görünür.</p>

<h2>Teknik özellikler</h2>
<ul>
  <li><strong>Ölçü:</strong> 14 × 14 × 20 cm</li>
  <li><strong>Gövde:</strong> Tik yağıyla korunan masif tik ahşap</li>
  <li><strong>Kapak:</strong> Sürgülü buhar kapağı (buharlaşmayı azaltır, bettanın zıplamasını önler)</li>
  <li><strong>Aydınlatma:</strong> 3000K, 4500K ve 6500K olmak üzere üç ışık tonlu LED</li>
  <li><strong>Elektrik:</strong> 220V</li>
  <li><strong>Sistem:</strong> Low-tech; CO₂ ve yoğun gübre gerektirmez</li>
</ul>

<h2>Yalnızca betta için değil</h2>
<p>Aynı ürün bitkili bir nano akvaryum, karides akvaryumu, <a href="../teraryum/">teraryum</a>, sukulent saksısı ya da dekoratif bir abajur olarak da kullanılabilir. Uygun canlıları <a href="../baliklar/">balıklar rehberimizde</a>, bitkileri <a href="../bitkiler/">bitkiler rehberimizde</a> bulabilirsiniz.</p>

<h2>Hazır kurulum seti</h2>
<p>Talep üzerine Betta Serisi'ni zemin, canlı bitkiler ve ekipmanla hazır kurulmuş olarak teslim ediyoruz. Kendiniz kurmak isterseniz <a href="../blog/betta-akvaryumu-kurulumu/">betta akvaryumu kurulum rehberimiz</a> ve <a href="../blog/nano-akvaryum-bakimi/">nano akvaryum bakım rutinimiz</a> adım adım yol gösterir.</p>

<h2>Fotoğraflar</h2>
<p>Betta Serisi'nin farklı açılardan ve üç ışık tonunda görüntülerini <a href="../galeri/">galeride</a> inceleyebilirsiniz. Daha büyük ya da farklı ölçüde bir model isterseniz <a href="../ozel-olcu-akvaryum/">özel ölçü akvaryum</a> sayfamıza bakın.</p>
""",
    },
    {
        "yol": "teraryum/", "tur": "hizmet", "kisa": "Teraryum",
        "hizmet": "Teraryum üretimi",
        "baslik": "Teraryum Ankara: El Yapımı Ahşap Teraryum | Tankled",
        "aciklama": "Ankara'da el yapımı teraryum: masif tik ahşap gövdeli, ışıklı ve kapaklı teraryumlar. "
                    "Bitki teraryumu ve gecko gibi egzotik hayvanlar için yaşam alanı.",
        "h1": "Teraryum: Ankara'da el yapımı, ahşap gövdeli",
        "gorsel": "assets/g-gecko.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Orman temalı ahşap gövdeli teraryum",
        "govde": """
<p><strong>Teraryum</strong>, bitkilerin ya da küçük kara hayvanlarının yaşadığı, camla çevrili bir mini ekosistemdir. Tankled teraryumları, akvaryumlarımızla aynı masif tik ahşap gövde ve LED aydınlatmayla Ankara Ostim'deki atölyemizde elde üretilir.</p>

<h2>Teraryum türleri</h2>
<ul>
  <li><strong>Kapalı (tropikal) bitki teraryumu:</strong> Yüksek nem seven fittonia, eğrelti, selaginella ve yosunlarla kurulur; kendi nem döngüsünü oluşturur.</li>
  <li><strong>Açık (kuru) teraryum:</strong> Sukulent ve kaktüs gibi kuru ortam bitkileri için havalandırmalı düzen.</li>
  <li><strong>Hayvan teraryumu:</strong> Gecko gibi küçük egzotik hayvanlar için; türün sıcaklık ve nem ihtiyacına göre planlanır.</li>
</ul>

<h2>Neden ahşap gövdeli teraryum?</h2>
<p>Ahşap gövde, teraryumu bir dekorasyon objesine dönüştürür ve LED aydınlatmayı gizler. Tik ahşap nemli ortama dayanıklıdır; üç ışık tonu (3000K, 4500K, 6500K) hem bitkilerin ihtiyacını karşılar hem de akşamları yumuşak bir ortam ışığı sağlar.</p>

<h2>Bakım</h2>
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
  <li>Masif tik ahşap gövde ve metal ayaklı modeller</li>
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
        "aciklama": "Tankled, Ankara Ostim'de masif tik ahşaptan mobilyalı akvaryum, teraryum ve paludaryum "
                    "üreten bir el yapımı akvaryum atölyesidir. Hikayemiz ve yaklaşımımız.",
        "h1": "Hakkımızda: Ankara'da el yapımı akvaryum atölyesi",
        "gorsel": "assets/g-lineup.webp", "gorsel_g": 1122, "gorsel_y": 1402,
        "gorsel_alt": "Tankled atölyesinde üretilen akvaryum koleksiyonu",
        "govde": """
<p>Tankled, bir akvaryumun yalnızca bir cam kap değil; mekânın ruhunu değiştiren, yaşayan bir tasarım nesnesi olabileceği inancıyla doğdu. <strong>Ankara Ostim</strong>'deki atölyemizde akvaryum, teraryum ve paludaryumları masif tik ahşaptan, elde ve tek tek üretiyoruz.</p>

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
  <li><strong>Atölye:</strong> Ostim, Yenimahalle, Ankara</li>
  <li><strong>Telefon:</strong> <a href="tel:+905312172006">+90 531 217 2006</a></li>
  <li><strong>WhatsApp:</strong> <a href="WA_LINK" target="_blank" rel="noopener">WhatsApp ile yazın</a></li>
  <li><strong>E-posta:</strong> <a href="mailto:tankledaquarium@gmail.com">tankledaquarium@gmail.com</a></li>
  <li><strong>Instagram:</strong> <a href="https://www.instagram.com/tankled.akvaryum/" target="_blank" rel="noopener">@tankled.akvaryum</a></li>
</ul>
<p>Atölye ziyaretleri için önceden haber vermenizi rica ederiz. Mesajlarınıza en kısa sürede dönüş yapıyoruz.</p>

<h2>Konum</h2>
<iframe title="Tankled atölyesi konumu: Ostim, Yenimahalle, Ankara" src="https://www.google.com/maps?q=Ostim%2C%20Yenimahalle%2C%20Ankara&amp;output=embed" width="100%" height="360" style="border:0;border-radius:18px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>

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
        govde = f"""    <article>
      <nav class="kirinti" aria-label="Sayfa yolu"><a href="{onek}">Ana sayfa</a> › {s["kisa"]}</nav>
      <span class="eyebrow">Tankled · Ankara</span>
      <h1>{s["h1"]}</h1>
{kapak}{s["govde"].strip().replace("WA_LINK", WA)}
      <section class="cta">
        <h2>Ankara'da el yapımı akvaryum</h2>
        <p>Ostim'deki atölyemizde masif tik ahşaptan mobilyalı ve dekoratif akvaryumlar üretiyoruz. Ölçünüze özel tasarım için bize ulaşın.</p>
        <a class="btn" href="{WA}" target="_blank" rel="noopener">WhatsApp ile yazın</a>
        <a class="btn" href="tel:+905312172006">Hemen arayın</a>
      </section>
    </article>"""
        hedef = KOK / s["yol"] / "index.html"
        hedef.parent.mkdir(exist_ok=True)
        hedef.write_text(blog.iskelet(s["baslik"], s["aciklama"], onek, govde), encoding="utf-8")


if __name__ == "__main__":
    uret()
