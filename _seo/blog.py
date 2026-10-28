"""Tankled blog yazilari: icerik burada, sayfalar blog/ altina uretilir.

Yeni yazi eklemek icin YAZILAR listesine bir sozluk ekleyip calistirin:
    python3 _seo/seo.py
(seo.py once bu dosyayla blog sayfalarini uretir, sonra SEO etiketlerini ve site haritasini yazar.)
"""

from pathlib import Path

KOK = Path(__file__).resolve().parent.parent

BLOG_BASLIK = "Akvaryum Blogu: Ankara'dan Rehberler ve Fikirler | Tankled"
BLOG_ACIKLAMA = ("Mobilyalı akvaryum, betta ve nano akvaryum kurulumu, bakım ipuçları ve Ankara'da akvaryum "
                 "seçimi üzerine Tankled atölyesinden rehber yazıları.")

YAZILAR = [
    {
        "slug": "teraryum-nasil-yapilir",
        "baslik": "Teraryum Nasıl Yapılır? Adım Adım Kapalı Teraryum | Tankled",
        "h1": "Teraryum nasıl yapılır? Adım adım kapalı teraryum rehberi",
        "aciklama": "Kapalı teraryum nasıl yapılır? Drenaj katmanı, aktif karbon, toprak, bitki seçimi ve nem "
                    "dengesiyle evde kendi kendine yaşayan bir teraryum kurun.",
        "tarih": "2026-10-27",
        "gorsel": "assets/g-gecko.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Ahşap gövdeli kapalı teraryum, orman zemini ve yosunlar",
        "etiketler": ["teraryum nasıl yapılır", "kapalı teraryum", "teraryum yapımı"],
        "govde": """
<p><strong>Teraryum</strong>, camla çevrili küçük bir bahçedir. Kapalı bir teraryumda bitkilerin terlediği su camda yoğuşur ve yeniden toprağa döner; böylece neredeyse hiç sulama gerektirmeyen, kendi kendine yaşayan bir mini ekosistem oluşur. Bu rehberde <strong>teraryum nasıl yapılır</strong> sorusunu adım adım cevaplıyoruz.</p>

<h2>Gerekenler</h2>
<ul>
  <li>Kapaklı cam hazne (Tankled ürünlerinde sürgülü buhar kapağı bu iş için idealdir)</li>
  <li>Drenaj katmanı: kil topu, ponza ya da ince çakıl</li>
  <li>Aktif karbon (koku ve küf oluşumunu azaltır)</li>
  <li>Ayırıcı katman: tül, file ya da kuru yosun</li>
  <li>Teraryum toprağı: torf, hindistan cevizi lifi ve perlit karışımı</li>
  <li>Nem seven küçük bitkiler, yosun, taş ve kökler</li>
</ul>

<h2>1. Drenaj katmanını oluşturun</h2>
<p>Cam haznenin drenaj deliği olmadığı için fazla su dipte birikir. Tabana 2–3 cm kil topu ya da çakıl sererek bu suyun toprağa geri çıkmasını ve kökleri çürütmesini önleyin.</p>

<h2>2. Aktif karbon ve ayırıcı</h2>
<p>Drenajın üzerine ince bir kat aktif karbon serpin. Ardından toprağın drenaja karışmasını engellemek için bir tül ya da kuru yosun katmanı yerleştirin.</p>

<h2>3. Toprak ve yerleşim</h2>
<p>4–6 cm teraryum toprağını arkası yüksek, önü alçak olacak şekilde eğimli serin. Önce taş ve kökleri yerleştirip "manzarayı" kurun, ardından bitkileri büyükten küçüğe doğru dikin.</p>

<h2>4. Bitki seçimi</h2>
<p>Kapalı teraryum için yavaş büyüyen ve yüksek nemi seven bitkiler seçin: fittonia, peperomia prostrata, pilea, selaginella, küçük eğrelti türleri ve yosunlar. Ayrıntılar için <a href="../teraryum-bitkileri-ve-bakimi/">teraryum bitkileri ve bakımı</a> yazımıza ve <a href="../../bitkiler/">bitkiler rehberimize</a> bakın.</p>

<h2>5. İlk sulama ve nem dengesi</h2>
<p>Toprağı bir püskürtücüyle nemlendirin; su dibe göllenmemeli. Kapağı kapatın ve ilk günlerde camı gözlemleyin: Sabahları hafif buğu normaldir. Cam sürekli damlalarla kaplıysa kapağı birkaç saat aralayın; hiç buğu yoksa biraz su püskürtün.</p>

<h2>6. Işık</h2>
<p>Teraryumu doğrudan güneşe koymayın; cam, içeriyi hızla ısıtır. Dolaylı gün ışığı ya da günde 6–8 saat LED ışık yeterlidir. Tankled gövdelerindeki 6500K ışık tonu bitkiler için, 3000K tonu ise akşamları dekoratif bir <a href="../dekoratif-abajur-fikirleri/">abajur</a> etkisi için tasarlandı.</p>

<p>Hazır, ahşap gövdeli ve ışıklı bir teraryum arıyorsanız <a href="../../teraryum/">teraryum sayfamıza</a> göz atın. Tankled ürünleri akvaryum, teraryum, abajur ve <a href="../isikli-bitki-saksisi/">bitki saksısı</a> olarak kullanılabilir.</p>
""",
    },
    {
        "slug": "teraryum-bitkileri-ve-bakimi",
        "baslik": "Teraryum Bitkileri ve Teraryum Bakımı Rehberi | Tankled",
        "h1": "Teraryum bitkileri ve teraryum bakımı: en kolay türler",
        "aciklama": "Teraryum bitkileri hangileri? Kapalı ve açık teraryum için en uygun bitkiler, teraryum bakımı, "
                    "sulama, ışık, küf ve buğu sorunlarına çözümler.",
        "tarih": "2026-10-27",
        "gorsel": "assets/paludarium.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Yosun ve tropikal bitkilerle dolu teraryum",
        "etiketler": ["teraryum bitkileri", "teraryum bakımı", "sukulent teraryum"],
        "govde": """
<p>Bir teraryumun uzun ömürlü olması, büyük ölçüde doğru <strong>teraryum bitkileri</strong>ni seçmeye bağlıdır. Kapalı ve açık teraryumlar çok farklı ortamlardır; birinde mutlu olan bitki diğerinde çabucak çürüyebilir. İşte iki tür için de en kolay bitkiler ve pratik <strong>teraryum bakımı</strong> ipuçları.</p>

<h2>Kapalı (nemli) teraryum bitkileri</h2>
<ul>
  <li><strong>Fittonia (sinir otu):</strong> Renkli damarlı yapraklarıyla teraryumların yıldızı; nemi çok sever.</li>
  <li><strong>Selaginella:</strong> Yumuşak, eğrelti benzeri dokusuyla doğal bir orman zemini görüntüsü verir.</li>
  <li><strong>Peperomia prostrata ve pilea:</strong> Küçük yapraklı, yavaş büyüyen türlerdir.</li>
  <li><strong>Küçük eğreltiler (ör. pteris):</strong> Arka plana yükseklik katar.</li>
  <li><strong>Yosunlar:</strong> Zemini kaplar, nemi dengeler.</li>
</ul>

<h2>Açık (kuru) teraryum bitkileri</h2>
<ul>
  <li><strong>Sukulentler:</strong> Echeveria, haworthia, sedum gibi türler; düşük nem ve bol ışık ister.</li>
  <li><strong>Kaktüsler:</strong> Kumlu, hızlı süzülen toprak ve iyi havalandırma gerekir.</li>
  <li><strong>Tillandsia (hava bitkisi):</strong> Toprak istemez; haftada bir püskürtme ya da kısa süreli suya batırma yeterlidir.</li>
</ul>
<p>Sukulent ve kaktüsleri kapalı teraryuma koymayın: yüksek nem köklerini çürütür. Bunlar için kapağı açık tutun ya da ürünü <a href="../isikli-bitki-saksisi/">ışıklı bitki saksısı</a> olarak kullanın.</p>

<h2>Teraryum bakımı</h2>
<ul>
  <li><strong>Sulama:</strong> Kapalı teraryumda aylarca sulama gerekmeyebilir; toprak kuruyunca hafifçe püskürtün. Açık teraryumda sukulentleri toprak tamamen kuruyunca sulayın.</li>
  <li><strong>Buğu:</strong> Camın sürekli buğulu olması fazla nemin işaretidir; kapağı birkaç saat aralayın.</li>
  <li><strong>Küf:</strong> Beyaz pamuksu küf görürseniz o kısmı alın ve havalandırmayı artırın. Aktif karbon katmanı küf riskini azaltır.</li>
  <li><strong>Budama:</strong> Cama değen ya da hızla uzayan dalları kesin; çürüyen yaprakları hemen çıkarın.</li>
  <li><strong>Işık:</strong> Doğrudan güneş yerine dolaylı ışık ya da LED kullanın.</li>
</ul>

<p>Kendi teraryumunuzu kurmak için <a href="../teraryum-nasil-yapilir/">teraryum nasıl yapılır</a> rehberimizi okuyun; uygun bitkileri <a href="../../bitkiler/">bitkiler rehberimizde</a> "teraryum ve paludaryum" filtresiyle bulun. Ahşap gövdeli, ışıklı teraryumlarımızı <a href="../../teraryum/">teraryum sayfamızda</a> inceleyebilirsiniz.</p>
""",
    },
    {
        "slug": "dekoratif-abajur-fikirleri",
        "baslik": "Dekoratif Abajur Fikirleri: Ahşap ve Işıklı Abajur | Tankled",
        "h1": "Dekoratif abajur fikirleri: içinde yaşam olan ahşap abajur",
        "aciklama": "Salon ve yatak odası için dekoratif abajur fikirleri: ahşap abajur, sıcak ışık tonu seçimi ve "
                    "içinde bitki ya da akvaryum olan yaşayan abajur tasarımı.",
        "tarih": "2026-10-27",
        "gorsel": "assets/galeri/urun-isik-3000k-45-derece.jpg", "gorsel_g": 750, "gorsel_y": 1000,
        "gorsel_alt": "3000K sıcak ışıkta ahşap gövdeli dekoratif abajur",
        "etiketler": ["dekoratif abajur", "ahşap abajur", "abajur modelleri"],
        "govde": """
<p>Bir <strong>abajur</strong>, odanın havasını tavan lambasından çok daha fazla belirler. Doğru yerde, doğru tonda bir abajur; salonu sıcak bir sohbet köşesine, yatak odasını dinlendirici bir sığınağa dönüştürür. Bu yazıda <strong>dekoratif abajur</strong> seçerken dikkat etmeniz gerekenleri ve sıradan bir lambadan çok daha fazlasını sunan "yaşayan abajur" fikrini anlatıyoruz.</p>

<h2>1. Işık tonu: Kelvin değerine bakın</h2>
<ul>
  <li><strong>2700–3000K (sıcak beyaz):</strong> Abajurlar için ideal; mum ışığına yakın, dinlendirici.</li>
  <li><strong>4000–4500K (nötr beyaz):</strong> Okuma ve çalışma köşeleri için.</li>
  <li><strong>6500K (gün ışığı):</strong> Bitkiler için faydalı, ancak akşam saatlerinde soğuk ve uyarıcıdır.</li>
</ul>
<p>Birden fazla ton sunan bir abajur, gün içinde farklı ihtiyaçlara uyum sağlar.</p>

<h2>2. Malzeme: ahşap abajurun sıcaklığı</h2>
<p><strong>Ahşap abajur</strong>, metal ya da plastiğe göre çok daha sıcak bir görünüm verir ve doğal tonlu mobilyalarla kolayca uyum sağlar. Her ahşabın damar deseni farklı olduğu için iki ahşap abajur birbirinin aynısı olmaz; bu da onu seri üretim bir lambadan ayırır.</p>

<h2>3. Yaşayan abajur: içinde doğa olan ışık</h2>
<p>Tankled ürünleri, ahşap gövde ve cam hazneyi üç ışık tonlu LED ile birleştirir. İçine bitki, yosun ya da bir betta balığı koyduğunuzda abajur, ışığıyla birlikte içindeki mini doğayı da sergiler. 3000K sıcak ışıkta akşamları dekoratif bir abajur, 6500K'de gündüz bitkiler için büyüme ışığı olarak çalışır. Aynı ürünü <a href="../../betta-akvaryumu/">akvaryum</a>, <a href="../../teraryum/">teraryum</a> ya da <a href="../isikli-bitki-saksisi/">bitki saksısı</a> olarak da kullanabilirsiniz.</p>

<h2>4. Abajur nereye konur?</h2>
<ul>
  <li><strong>Salon:</strong> Koltuk yanındaki sehpa ya da konsol; göz hizasının biraz altında.</li>
  <li><strong>Yatak odası:</strong> Komodin üzerinde, yatağa göre yumuşak ve dolaylı ışık.</li>
  <li><strong>Çalışma odası:</strong> Masanın köşesinde, ekrana yansımayacak açıda.</li>
  <li><strong>Antre:</strong> Eve girerken karşılayan sıcak bir ışık noktası.</li>
</ul>

<h2>5. Hediye olarak abajur</h2>
<p>El yapımı, ahşap ve içinde yaşam olan bir abajur; ev hediyesi, yeni iş yeri ya da doğum günü için akılda kalıcı bir seçimdir. Yatak odasında kullanımı için <a href="../gece-lambasi-olarak-isikli-teraryum/">gece lambası olarak ışıklı teraryum</a> yazımıza bakın.</p>
""",
    },
    {
        "slug": "gece-lambasi-olarak-isikli-teraryum",
        "baslik": "Gece Lambası Fikirleri: Işıklı Teraryum Lamba | Tankled",
        "h1": "Gece lambası fikirleri: yatak odası için ışıklı teraryum lamba",
        "aciklama": "Yatak odası ve çocuk odası için dekoratif gece lambası fikirleri: sıcak ışıklı teraryum lamba, "
                    "ahşap gece lambası ve uykuya uygun ışık tonu seçimi.",
        "tarih": "2026-10-27",
        "gorsel": "assets/galeri/urun-isik-3000k-45-derece.jpg", "gorsel_g": 750, "gorsel_y": 1000,
        "gorsel_alt": "Sıcak ışıklı teraryum lamba yatak odasında gece lambası olarak",
        "etiketler": ["gece lambası", "dekoratif gece lambası", "teraryum lamba"],
        "govde": """
<p>İyi bir <strong>gece lambası</strong>, karanlıkta yolunuzu bulmanızı sağlarken uykunuzu bölmeyecek kadar yumuşak olmalıdır. Sıradan bir priz lambası bu işi görür; ama yatak odasının dekorasyonuna hiçbir şey katmaz. İçinde bitkilerin ya da yosunların olduğu, ahşap gövdeli ışıklı bir <strong>teraryum lamba</strong> ise hem gece lambası hem de odanın en dikkat çeken objesi olabilir.</p>

<h2>Uyku için doğru ışık tonu</h2>
<p>Akşam saatlerinde mavi ağırlıklı soğuk ışık uyanıklığı artırabilir. Bu yüzden gece lambası olarak <strong>3000K ve altı sıcak beyaz</strong> tonları tercih edin ve ışığı doğrudan göze değil, çevreye yayılacak şekilde konumlandırın. Tankled ürünlerindeki 3000K ton, tam da bu kullanım için tasarlandı.</p>

<h2>Neden ışıklı teraryum?</h2>
<ul>
  <li><strong>Yumuşak ve dolaylı ışık:</strong> Işık bitkilerin ve camın arasından süzülerek yayılır.</li>
  <li><strong>Yaşayan dekor:</strong> İçindeki yosun ve bitkiler her gün biraz değişir; odaya canlılık katar.</li>
  <li><strong>Sessiz:</strong> Filtre ya da motor yoktur; yatak odası için idealdir.</li>
  <li><strong>Az bakım:</strong> Kapalı teraryum aylarca sulama istemeyebilir. Kurulum için <a href="../teraryum-nasil-yapilir/">teraryum nasıl yapılır</a> rehberimize bakın.</li>
</ul>

<h2>Çocuk odasında gece lambası</h2>
<p>Çocuk odasında gece lambası olarak ışıklı teraryum kullanacaksanız ürünü çocuğun ulaşamayacağı bir rafa koyun ve kabloyu sabitleyin. İçine dikenli ya da zehirli olabilecek bitkiler yerine fittonia, pilea ve yosun gibi zararsız türleri seçin. Bitkilerin büyüdüğünü izlemek çocuklar için doğayı tanımanın keyifli bir yoludur.</p>

<h2>Gündüz bitki ışığı, gece abajur</h2>
<p>Üç ışık tonlu bir teraryum lamba gündüz 6500K ile bitkilerin büyümesini destekler, akşam 4500K ile okuma ışığı, gece 3000K ile gece lambası olur. Böylece tek bir ürün, gün boyu farklı görevler üstlenir. Diğer kullanım fikirleri için <a href="../dekoratif-abajur-fikirleri/">dekoratif abajur fikirleri</a> ve <a href="../isikli-bitki-saksisi/">ışıklı bitki saksısı</a> yazılarımıza göz atın.</p>

<p>Tankled'ın ahşap gövdeli, ışıklı ürünlerini <a href="../../teraryum/">teraryum</a> ve <a href="../../betta-akvaryumu/">Betta Serisi</a> sayfalarımızda inceleyebilirsiniz.</p>
""",
    },
    {
        "slug": "isikli-bitki-saksisi",
        "baslik": "Işıklı Bitki Saksısı: Sukulent ve Kaktüs Saksısı | Tankled",
        "h1": "Işıklı bitki saksısı: sukulent ve kaktüs için cam saksı",
        "aciklama": "Işıklı bitki saksısı ile ışık almayan köşelerde bile sukulent ve kaktüs yetiştirin. Cam saksıda "
                    "drenaj, toprak, sulama ve LED ışık süresi rehberi.",
        "tarih": "2026-10-27",
        "gorsel": "assets/g-betta-bos.webp", "gorsel_g": 1086, "gorsel_y": 1448,
        "gorsel_alt": "Ahşap gövdeli ışıklı cam bitki saksısı",
        "etiketler": ["bitki saksısı", "sukulent saksısı", "ışıklı saksı"],
        "govde": """
<p>Evde bitki yetiştirmenin en büyük engeli ışıktır. Kuzeye bakan odalar, ofis masaları ve kitaplık rafları çoğu bitki için fazla karanlıktır. <strong>Işıklı bitki saksısı</strong>, kendi LED aydınlatmasıyla bu sorunu çözer ve bitkinizi pencereden bağımsız hâle getirir. Bu yazıda cam gövdeli, ışıklı bir saksıda <strong>sukulent</strong> ve kaktüs yetiştirmenin püf noktalarını anlatıyoruz.</p>

<h2>1. Drenaj: cam saksının altın kuralı</h2>
<p>Cam saksılarda drenaj deliği yoktur; fazla su dipte birikir ve kökleri çürütür. Bu yüzden tabana 2–3 cm kil topu, ponza ya da çakıl serin. Üzerine ince bir kat aktif karbon eklemek koku ve küfü önler.</p>

<h2>2. Toprak</h2>
<p>Sukulent ve kaktüsler için hızlı süzülen bir karışım kullanın: kaktüs toprağı, perlit ve ince ponza. Normal saksı toprağı suyu fazla tutar.</p>

<h2>3. Sulama</h2>
<p>Drenajsız saksıda en sık yapılan hata fazla sulamadır. Toprak tamamen kuruduktan sonra, tabana göllenmeyecek kadar az su verin; kışın sulamayı seyrekleştirin. Şüphede kaldığınızda sulamayın: sukulentler kuraklığa, çürümeden çok daha iyi dayanır.</p>

<h2>4. Işık süresi ve tonu</h2>
<p>Sukulentler bol ışık ister. Penceresiz bir köşede 6500K gün ışığı tonunda günde 8–10 saat aydınlatma, renklerin canlı kalmasını ve bitkinin ışığa doğru uzayıp şeklini bozmamasını sağlar. Akşamları 3000K tona geçerek saksıyı aynı zamanda bir <a href="../dekoratif-abajur-fikirleri/">dekoratif abajur</a> olarak kullanabilirsiniz.</p>

<h2>5. Havalandırma</h2>
<p>Sukulentler kuru havayı sever; kapalı bir cam içinde nem birikir. Kapağı açık tutun ya da sürgülü kapağı aralık bırakın. Nem seven bitkiler için ise kapağı kapatarak saksıyı bir <a href="../teraryum-nasil-yapilir/">kapalı teraryuma</a> dönüştürebilirsiniz.</p>

<h2>Bu saksıda neler yetişir?</h2>
<ul>
  <li><strong>Sukulentler:</strong> Haworthia, echeveria, sedum, crassula</li>
  <li><strong>Küçük kaktüsler:</strong> Mammillaria, gymnocalycium</li>
  <li><strong>Hava bitkileri:</strong> Tillandsia (toprak gerektirmez)</li>
  <li><strong>Gölge seven yapraklılar:</strong> Pilea, peperomia, küçük pothos çelikleri</li>
</ul>

<p>Ofis ve çalışma masası için uygun bitkiler hakkında <a href="../masa-ustu-bitki-saksisi-ofis/">masaüstü bitki saksısı</a> yazımıza bakın. Tankled ürünleri aynı zamanda <a href="../../betta-akvaryumu/">akvaryum</a> ve <a href="../../teraryum/">teraryum</a> olarak da kullanılabilir.</p>
""",
    },
    {
        "slug": "masa-ustu-bitki-saksisi-ofis",
        "baslik": "Masaüstü Bitki Saksısı: Ofis Bitkileri Rehberi | Tankled",
        "h1": "Masaüstü bitki saksısı: ofis ve çalışma masası için bitkiler",
        "aciklama": "Ofis ve çalışma masası için masaüstü bitki saksısı fikirleri: az ışıkta yaşayan ofis bitkileri, "
                    "ışıklı saksı ile bakım ve kurumsal hediye önerileri.",
        "tarih": "2026-10-27",
        "gorsel": "assets/g-betta-studio.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Çalışma masasında ahşap gövdeli ışıklı bitki saksısı",
        "etiketler": ["masaüstü bitki saksısı", "ofis bitkileri", "masa bitkisi"],
        "govde": """
<p>Çalışma masasındaki küçük bir bitki, ekran başında geçen saatleri daha yeşil ve daha sakin kılar. Ancak ofisler çoğu zaman pencereden uzak, klimalı ve az ışıklı ortamlardır; bu da pek çok bitki için zorlu bir yaşam alanı demektir. Doğru bitki ve doğru <strong>masaüstü bitki saksısı</strong> ile bu sorun kolayca aşılır.</p>

<h2>Az ışıkta yaşayan ofis bitkileri</h2>
<ul>
  <li><strong>Pothos (salon sarmaşığı):</strong> Çok dayanıklıdır, az ışıkta bile büyür.</li>
  <li><strong>Peperomia:</strong> Küçük boyu ve etli yapraklarıyla masa için idealdir.</li>
  <li><strong>Pilea:</strong> Yuvarlak yapraklarıyla modern bir görünüm verir.</li>
  <li><strong>Fittonia:</strong> Renkli yapraklıdır; nemi sevdiği için kapalı bir cam içinde en iyi hâlini alır.</li>
  <li><strong>Java yosunu ve marimo:</strong> Su içinde yaşayan, neredeyse bakım istemeyen yeşillikler.</li>
</ul>
<p>Daha fazla bitkiyi ışık ve bakım ihtiyaçlarıyla <a href="../../bitkiler/">bitkiler rehberimizde</a> bulabilirsiniz.</p>

<h2>Neden ışıklı saksı?</h2>
<p>Ofiste en büyük sorun ışık eksikliğidir. Kendi LED aydınlatması olan bir saksı, bitkinin ihtiyaç duyduğu ışığı pencereye bağlı kalmadan sağlar. Mesai bitiminde ışığı kapatmanız ya da bir zamanlayıcıya bağlamanız yeterlidir. Cam gövde ise klimanın kurutucu etkisinden bitkiyi korur ve nemi dengeler.</p>

<h2>Masaüstü saksı seçerken</h2>
<ul>
  <li><strong>Boyut:</strong> Klavye ve ekranın yanına sığacak kompakt bir ölçü (ör. 14 × 14 cm taban).</li>
  <li><strong>Su taşmasına karşı güvenlik:</strong> Drenajlı düzen ve kapalı tabanlı cam, masaya su sızmasını önler.</li>
  <li><strong>Görünüm:</strong> Ahşap gövde, ofis mobilyalarıyla doğal bir uyum sağlar.</li>
  <li><strong>Çok amaçlılık:</strong> Aynı ürün akşamları <a href="../dekoratif-abajur-fikirleri/">abajur</a>, isterseniz <a href="../../betta-akvaryumu/">betta akvaryumu</a> olarak da kullanılabilir.</li>
</ul>

<h2>Kurumsal hediye olarak bitki saksısı</h2>
<p>El yapımı, ahşap gövdeli ve içinde canlı bir bitki olan ışıklı saksı; yeni ofis açılışları, çalışanlara ve iş ortaklarına verilecek hediyeler için akılda kalıcı ve uzun ömürlü bir seçimdir. Toplu siparişler için <a href="../../iletisim/">bizimle iletişime geçebilirsiniz</a>.</p>

<p>Sukulent ve kaktüs yetiştirmenin ayrıntıları için <a href="../isikli-bitki-saksisi/">ışıklı bitki saksısı</a> rehberimizi okuyun.</p>
""",
    },
    {
        "slug": "bitkili-akvaryum-kurulumu",
        "baslik": "Bitkili Akvaryum Nasıl Kurulur? Bitki Seçimi | Tankled",
        "h1": "Bitkili akvaryum nasıl kurulur? Akvaryum bitkisi seçimi ve bakım",
        "aciklama": "Bitkili akvaryum kurulumu: zemin, ışık, gübre ve CO₂; yeni başlayanlar için en kolay akvaryum "
                    "bitkileri ve su bitkileri, yerleşim ve bakım ipuçları.",
        "tarih": "2026-10-27",
        "gorsel": "assets/planted.webp", "gorsel_g": 896, "gorsel_y": 1195,
        "gorsel_alt": "Canlı akvaryum bitkileriyle kurulmuş bitkili akvaryum",
        "etiketler": ["bitkili akvaryum", "akvaryum bitkisi", "su bitkisi"],
        "govde": """
<p><strong>Bitkili akvaryum</strong>, canlı akvaryum bitkilerinin balıklar kadar önemli olduğu, doğal bir su altı bahçesidir. Bitkiler yalnızca güzel görünmez: suyu temizler, oksijen üretir, yosunla besin için rekabet eder ve balıklara saklanma alanı sağlar. Bu rehberde bitkili akvaryumun nasıl kurulacağını ve hangi <strong>akvaryum bitkisi</strong>nin size uygun olduğunu adım adım anlatıyoruz.</p>

<h2>Low-tech mi, high-tech mi?</h2>
<ul>
  <li><strong>Low-tech bitkili akvaryum:</strong> CO₂ tüpü kullanılmaz; düşük-orta ışık ve yavaş büyüyen bitkilerle kurulur. Bakımı kolaydır, yeni başlayanlar için idealdir.</li>
  <li><strong>High-tech bitkili akvaryum:</strong> Güçlü ışık, CO₂ ve düzenli gübreleme gerektirir. Halı bitkileri ve kırmızı bitkiler gibi zor türler hızla büyür, ancak dengeyi kurmak deneyim ister.</li>
</ul>

<h2>1. Zemin: bitkilerin besin deposu</h2>
<p>Köklerinden beslenen bitkiler (cryptocoryne, kılıç otu, halı bitkileri) için besinli akvaryum toprağı en iyi seçimdir. Köklerini taşa ve köke tutturan anubias, java eğreltisi ve bucephalandra gibi bitkiler için ise zemin önemli değildir. Zemin türlerini <a href="../akvaryum-kumu-ve-zemin/">akvaryum kumu ve zemin seçimi</a> yazımızda karşılaştırdık.</p>

<h2>2. Işık</h2>
<p>Bitkiler için 6500K civarı gün ışığı tonu idealdir. Günde 6–8 saat aydınlatma yeterlidir; daha uzun süre yosun sorununa yol açar. Bir zamanlayıcı kullanmak ışık süresini sabit tutar.</p>

<h2>3. Yeni başlayanlar için en kolay akvaryum bitkileri</h2>
<ul>
  <li><strong>Anubias nana:</strong> Çok az ışıkla yaşar, taşa bağlanır, neredeyse bakım istemez.</li>
  <li><strong>Java eğreltisi:</strong> Dayanıklı, köke bağlanan bir su bitkisi.</li>
  <li><strong>Java yosunu:</strong> Taş ve köklerin üzerinde doğal bir görünüm oluşturur; karidesler sever.</li>
  <li><strong>Cryptocoryne wendtii:</strong> Zemine dikilen, yavaş büyüyen ön-orta plan bitkisi.</li>
  <li><strong>Hygrophila polysperma ve limnophila:</strong> Hızlı büyüyen sap bitkileri; yosunla en iyi rekabet edenler.</li>
  <li><strong>Salvinia ve limnobium:</strong> Yüzey (yüzen) su bitkileri; fazla besini hızla tüketir.</li>
</ul>
<p>Tüm bitkileri ışık, sıcaklık, pH ve zorluk derecesiyle <a href="../../bitkiler/">akvaryum bitkileri rehberimizde</a> filtreleyebilirsiniz.</p>

<h2>4. Yerleşim: ön, orta ve arka plan</h2>
<p>Kısa bitkileri (halı bitkileri, cryptocoryne) öne, orta boyları (anubias, bucephalandra) taş ve köklerin çevresine, uzun sap bitkilerini (vallisneria, rotala, limnophila) arkaya yerleştirin. Bu düzen derinlik hissi verir ve tüm bitkilerin ışık almasını sağlar.</p>

<h2>5. Gübre ve CO₂</h2>
<p>Low-tech akvaryumda balık atıkları ve haftalık az miktarda sıvı gübre çoğu zaman yeterlidir. Kök bitkileri için zemine kök tableti eklenebilir. CO₂ yalnızca güçlü ışık kullanılan high-tech sistemlerde gerekir.</p>

<h2>6. İlk haftalar ve bakım</h2>
<p>Bitkiler ilk haftalarda yeni ortama alışırken bazı yaprakların erimesi normaldir. Akvaryumu bol bitkiyle başlatmak, su döngüsü sırasında yosun riskini azaltır. Düzenli budama ve haftalık su değişimi için <a href="../nano-akvaryum-bakimi/">bakım rutinimize</a> bakın; doğru filtreyi seçmek için <a href="../akvaryum-filtresi-ve-pompasi/">akvaryum filtresi ve pompası rehberimizi</a> okuyun.</p>

<p>Tankled akvaryumları, üç ışık tonlu LED aydınlatmasıyla bitkili low-tech kurulumlar için tasarlanmıştır. Ankara'daki atölyemizden bitkileri yerleştirilmiş hazır kurulum için <a href="../../iletisim/">bize ulaşın</a>.</p>
""",
    },
    {
        "slug": "akvaryum-filtresi-ve-pompasi",
        "baslik": "Akvaryum Filtresi ve Pompası Nasıl Seçilir? | Tankled",
        "h1": "Akvaryum filtresi ve akvaryum pompası nasıl seçilir?",
        "aciklama": "Akvaryum filtresi türleri (sünger, iç, askı, dış filtre), akvaryum pompası ve hava motoru farkı, "
                    "doğru debi hesabı ve filtre bakımı rehberi.",
        "tarih": "2026-10-27",
        "gorsel": "assets/lagoon.webp", "gorsel_g": 896, "gorsel_y": 1195,
        "gorsel_alt": "Temiz ve berrak sulu akvaryum",
        "etiketler": ["akvaryum filtresi", "akvaryum pompası", "akvaryum hava motoru"],
        "govde": """
<p>Berrak ve sağlıklı bir akvaryumun kalbi <strong>akvaryum filtresi</strong>dir. Filtre yalnızca suyu görünür kirden arındırmaz; asıl görevi, balık atıklarından oluşan zehirli amonyağı ve nitriti daha zararsız nitrata çeviren faydalı bakterilere yuva olmaktır. Bu yazıda filtre türlerini, <strong>akvaryum pompası</strong> ile hava motoru arasındaki farkı ve doğru seçimi anlatıyoruz.</p>

<h2>Filtrasyonun üç türü</h2>
<ul>
  <li><strong>Mekanik:</strong> Sünger ve elyaf, yüzen partikülleri tutar.</li>
  <li><strong>Biyolojik:</strong> Seramik halka ve gözenekli malzemeler, faydalı bakterilere yaşam alanı sağlar. En önemli filtrasyon türüdür.</li>
  <li><strong>Kimyasal:</strong> Aktif karbon gibi malzemeler, renk ve koku yapan maddeleri ya da ilaç kalıntılarını temizler; sürekli gerekmez.</li>
</ul>

<h2>Akvaryum filtresi türleri</h2>
<ul>
  <li><strong>Sünger filtre:</strong> Bir hava motoruyla çalışır; ucuz, güvenli ve akıntısı zayıftır. Betta, karides ve nano akvaryumlar için idealdir.</li>
  <li><strong>İç filtre:</strong> Akvaryumun içine vantuzla yapışır; küçük ve orta akvaryumlar için pratiktir.</li>
  <li><strong>Askı (şelale) filtre:</strong> Akvaryumun kenarına asılır; bakımı kolaydır ve içeride yer kaplamaz.</li>
  <li><strong>Dış (kanister) filtre:</strong> Dolabın içinde durur; yüksek kapasiteli ve sessizdir. Büyük ve bitkili akvaryumlar için en iyi seçenektir.</li>
</ul>

<h2>Akvaryum pompası ile hava motoru arasındaki fark</h2>
<p><strong>Akvaryum pompası</strong> (su pompası) suyu hareket ettirir: filtrelerin içinde bulunur ya da akıntı oluşturmak için ayrıca kullanılır. <strong>Hava motoru</strong> ise suya hava kabarcığı verir; sünger filtreleri çalıştırır ve yüzeyi hareketlendirerek oksijen alışverişini artırır. Bitkili ve az stoklu akvaryumlarda iyi çalışan bir filtre çoğu zaman yeterlidir; kalabalık akvaryumlarda ve sıcak yaz günlerinde ek havalandırma faydalıdır.</p>

<h2>Doğru debi (saatlik akış) nasıl hesaplanır?</h2>
<p>Genel bir kural olarak filtrenin saatlik debisi, akvaryum hacminin <strong>4–6 katı</strong> olmalıdır. Örneğin 60 litrelik bir akvaryum için 240–360 litre/saat debili bir filtre uygundur. Ancak betta gibi uzun yüzgeçli balıklar ve karidesler güçlü akıntıdan hoşlanmaz; bu durumda akış ayarlı ya da sünger filtre tercih edin. Akvaryumunuzun litresini <a href="../../akvaryum-olustur/">3D tasarım aracımızla</a> hesaplayabilirsiniz.</p>

<h2>Filtre bakımı: en sık yapılan hata</h2>
<p>Filtre süngerini musluk suyuyla yıkamak, içindeki faydalı bakterileri öldürür ve akvaryumda ani amonyak yükselmesine yol açabilir. Süngeri her zaman su değişimi sırasında çektiğiniz akvaryum suyunda hafifçe sıkın. Filtre malzemesinin tamamını aynı anda değiştirmeyin; biyolojik malzemeyi yıllarca kullanabilirsiniz.</p>

<h2>Sessizlik ve yerleşim</h2>
<p>Yatak odası ve çalışma odasındaki akvaryumlar için sessiz çalışan filtre seçin. Filtrenin giriş borusuna bir ön sünger takmak, karideslerin ve yavru balıkların emilmesini önler. Diğer ekipmanların ne işe yaradığını <a href="../../malzemeler/">akvaryum malzemeleri rehberimizde</a>, zemin seçimini <a href="../akvaryum-kumu-ve-zemin/">akvaryum kumu ve zemin</a> yazımızda bulabilirsiniz.</p>
""",
    },
    {
        "slug": "akvaryum-kumu-ve-zemin",
        "baslik": "Akvaryum Kumu ve Zemin Seçimi Rehberi | Tankled",
        "h1": "Akvaryum kumu ve zemin seçimi: hangi zemin hangi akvaryuma?",
        "aciklama": "Akvaryum kumu, çakıl ve besinli akvaryum toprağı karşılaştırması: bitkili akvaryum, betta ve "
                    "karides için doğru zemin, kalınlık ve yıkama ipuçları.",
        "tarih": "2026-10-27",
        "gorsel": "assets/abyss.webp", "gorsel_g": 896, "gorsel_y": 1190,
        "gorsel_alt": "Kum ve taş zeminli akvaryum düzeni",
        "etiketler": ["akvaryum kumu", "akvaryum zemini", "akvaryum toprağı"],
        "govde": """
<p>Zemin, akvaryumun hem görünümünü hem de biyolojik dengesini belirler. Yanlış seçilen zemin bitkilerin büyümesini engelleyebilir, su değerlerini değiştirebilir ya da dipte yaşayan balıklara zarar verebilir. Bu rehberde <strong>akvaryum kumu</strong>, çakıl ve akvaryum toprağını karşılaştırıyoruz.</p>

<h2>1. Akvaryum kumu</h2>
<p>İnce taneli akvaryum kumu doğal bir görünüm sağlar ve corydoras, kuhli gibi zemini eşeleyen balıklar için en güvenli seçenektir. Kum besin içermez; bu yüzden kök bitkileri için kök tableti eklenmelidir. Çok ince kum zamanla sıkışabilir; ince-orta tane boyu tercih edin. İnşaat kumu ya da deniz kumu kullanmayın: içerdiği kireç ve tuz su değerlerini değiştirir.</p>

<h2>2. Akvaryum çakılı</h2>
<p>Çakıl kolay temizlenir ve su akışına izin verir. Ancak aralarında yem artıkları birikebilir ve keskin kenarlı çakıl dip balıklarının bıyıklarına zarar verebilir. Yuvarlak kenarlı, nötr (kireç içermeyen) çakıl seçin.</p>

<h2>3. Besinli akvaryum toprağı</h2>
<p><a href="../bitkili-akvaryum-kurulumu/">Bitkili akvaryum</a> için en iyi seçenektir. Bitkilere besin sağlar ve suyu hafif yumuşatıp pH'ı düşürür; bu da karidesler ve pek çok tropikal balık için faydalıdır. İlk haftalarda bir miktar amonyak salabileceği için balık eklemeden önce su döngüsünün tamamlanması önemlidir.</p>

<h2>Hangi akvaryuma hangi zemin?</h2>
<ul>
  <li><strong>Bitkili akvaryum:</strong> Besinli akvaryum toprağı ya da altta besin katmanı, üstte kum.</li>
  <li><strong>Betta akvaryumu:</strong> Bitkili ise akvaryum toprağı, yalnızca epifit bitkiler (anubias, java eğreltisi) varsa ince kum.</li>
  <li><strong>Karides akvaryumu:</strong> pH'ı düşük tutan akvaryum toprağı.</li>
  <li><strong>Corydoras ve dip balıkları:</strong> İnce, yuvarlak taneli akvaryum kumu.</li>
  <li><strong>Paludaryum ve teraryum:</strong> Drenaj katmanı (kil topları) üzerinde toprak karışımı.</li>
</ul>

<h2>Zemin kalınlığı</h2>
<p>Bitkili akvaryumda zemin önde 3–4 cm, arkada 6–8 cm olacak şekilde eğimli yapılır; bu hem kök bitkilerine yer açar hem de derinlik hissi verir. Bitkisiz akvaryumlarda 2–3 cm yeterlidir.</p>

<h2>Yıkama ve yerleştirme</h2>
<p>Kum ve çakılı, su berraklaşana kadar bir kovada yıkayın. Akvaryum toprağı ise genellikle yıkanmaz; paketin üzerindeki talimata uyun. Suyu doldururken zemini dağıtmamak için suyu bir tabağın ya da poşetin üzerine yavaşça dökün.</p>

<p>Zemin, filtre ve diğer malzemelerin tam listesi için <a href="../../malzemeler/">akvaryum malzemeleri rehberimize</a>, zemine uygun bitkiler için <a href="../../bitkiler/">akvaryum bitkileri rehberimize</a> bakın. Doğru filtreyi seçmek için <a href="../akvaryum-filtresi-ve-pompasi/">akvaryum filtresi ve pompası</a> yazımızı okuyun.</p>
""",
    },
    {
        "slug": "akvaryum-fiyatlari",
        "baslik": "Akvaryum Fiyatları 2026: Fiyatı Ne Belirler? | Tankled",
        "h1": "Akvaryum fiyatları 2026: akvaryumun fiyatını neler belirler?",
        "aciklama": "Akvaryum fiyatları 2026: hazır ve el yapımı akvaryum, mobilyalı akvaryum ve kurulum maliyetini "
                    "belirleyen ölçü, cam, malzeme ve ekipman kalemleri.",
        "tarih": "2026-10-27",
        "gorsel": "assets/g-betta-bright.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Aydınlık bir salonda ahşap gövdeli akvaryum",
        "etiketler": ["akvaryum fiyatları", "mobilyalı akvaryum fiyatları", "akvaryum maliyeti"],
        "govde": """
<p>"Akvaryum fiyatları ne kadar?" sorusunun tek bir cevabı yoktur. Aynı litredeki iki akvaryum arasında, cam kalitesine, gövde malzemesine, ekipmana ve işçiliğe göre büyük fark olabilir. Bu yazıda 2026'da bir akvaryumun toplam maliyetini oluşturan kalemleri tek tek açıklıyoruz; böylece aldığınız teklifleri doğru karşılaştırabilirsiniz.</p>

<h2>1. Akvaryumun kendisi: ölçü ve cam</h2>
<p>Fiyatı belirleyen ilk etken hacimdir; ancak litre büyüdükçe yalnızca cam miktarı değil, gereken cam kalınlığı da artar. Kenarları rodajlı (zımparalı) cam, düzgün ve kabarcıksız silikon işçiliği ve ekstra şeffaf (beyaz) cam gibi tercihler fiyatı yükseltir ama akvaryumun ömrünü ve görünümünü doğrudan etkiler.</p>

<h2>2. Gövde: sehpa mı, mobilyalı akvaryum mu?</h2>
<p>Hazır bir akvaryuma ayrıca sehpa almak çoğu zaman ilk bakışta ucuz görünür. <a href="../../mobilyali-akvaryum/">Mobilyalı akvaryum</a>da ise gövde akvaryumla birlikte tasarlanır; MDF, kontrplak ya da masif ahşap seçimi fiyatı belirler. Masif tik gibi neme dayanıklı ağaçlar daha pahalıdır ancak nemli ortamda yıllarca şeklini korur.</p>

<h2>3. Ekipman</h2>
<ul>
  <li><strong>Filtre:</strong> Sünger, iç ya da dış filtre; akvaryum hacmine göre seçilir.</li>
  <li><strong>Isıtıcı:</strong> Tropikal balıklar (ör. betta) için şarttır.</li>
  <li><strong>Aydınlatma:</strong> Bitkili akvaryumda kaliteli LED, maliyetin önemli bir kısmıdır.</li>
  <li><strong>Test kiti ve su şartlandırıcı:</strong> Küçük ama vazgeçilmez kalemlerdir.</li>
</ul>
<p>Hangi ekipmanın gerçekten gerekli olduğunu <a href="../../malzemeler/">malzemeler rehberimizde</a> anlattık.</p>

<h2>4. Zemin, hardscape ve bitkiler</h2>
<p>Besinli akvaryum toprağı, doğal taş ve kökler, canlı bitkiler toplam maliyeti etkiler. Low-tech bir kurulum (CO₂ tüpü olmadan, yavaş büyüyen bitkilerle) hem kurulumda hem de bakımda daha ekonomiktir.</p>

<h2>5. Canlılar</h2>
<p>Balık ve karides fiyatları türe göre değişir; ancak toplam bütçede genellikle en küçük kalemdir. Önemli olan, akvaryum hacmine uygun tür ve sayı seçmektir; <a href="../../baliklar/">balıklar rehberimiz</a> bu konuda yol gösterir.</p>

<h2>6. Kurulum ve işçilik</h2>
<p>Hazır kurulum (zemin, bitki yerleşimi, ekipman montajı ve ilk su döngüsü desteği) isteyip istemediğiniz de fiyatı değiştirir. Özellikle ilk akvaryumunuzsa hazır kurulum, deneme-yanılma ile kaybedilecek bitki ve canlı maliyetini azaltır.</p>

<h2>Teklifleri karşılaştırırken sorun</h2>
<ul>
  <li>Cam kalınlığı ve silikon işçiliği nasıl?</li>
  <li>Gövde hangi malzemeden ve ağırlığı taşımak için tasarlanmış mı?</li>
  <li>Fiyata kapak, aydınlatma ve ekipman dahil mi?</li>
  <li>Kurulum ve sonrasında destek var mı?</li>
</ul>
<p>Ankara'da mobilyalı ya da <a href="../../ozel-olcu-akvaryum/">özel ölçü akvaryum</a> için net fiyat almak isterseniz alanınızın ölçüsünü bize gönderin; Ostim'deki atölyemizden size özel teklif hazırlayalım.</p>
""",
    },
    {
        "slug": "ankara-akvaryum-bakim-hizmeti",
        "baslik": "Ankara Akvaryum Bakım Hizmeti: Neler Yapılır? | Tankled",
        "h1": "Ankara'da akvaryum bakım hizmeti: neler yapılır, ne sıklıkla?",
        "aciklama": "Ankara'da akvaryum bakım hizmeti alırken nelere dikkat etmeli? Su değişimi, filtre ve cam "
                    "temizliği, bitki budama ve su testi: bakımın kapsamı ve sıklığı.",
        "tarih": "2026-10-26",
        "gorsel": "assets/g-betta-studio.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Bakımlı, bitkili ahşap gövdeli akvaryum",
        "etiketler": ["akvaryum bakım hizmeti", "akvaryum bakımı Ankara", "akvaryum temizliği"],
        "govde": """
<p>Bir akvaryumun uzun yıllar sağlıklı kalması, düzenli bakıma bağlıdır. Zamanı olmayanlar, ofis ve mağazalar ya da büyük akvaryum sahipleri için <strong>akvaryum bakım hizmeti</strong> iyi bir çözümdür. Bu yazıda Ankara'da akvaryum bakım hizmeti alırken bakımın neleri kapsaması gerektiğini ve ne sıklıkla yapılması gerektiğini anlatıyoruz.</p>

<h2>Profesyonel bakımın kapsamı</h2>
<ul>
  <li><strong>Kısmi su değişimi:</strong> Suyun %20–30'unun zemindeki artıklarla birlikte sifonlanması ve şartlandırılmış, aynı sıcaklıkta suyla yenilenmesi.</li>
  <li><strong>Cam temizliği:</strong> İç camlardaki yosunun, dış camdaki kireç lekelerinin temizlenmesi.</li>
  <li><strong>Filtre bakımı:</strong> Süngerin akvaryum suyunda çalkalanması; faydalı bakterileri öldürmemek için musluk suyu kullanılmaması.</li>
  <li><strong>Bitki bakımı:</strong> Budama, çürüyen yaprakların alınması, gerekiyorsa gübre takviyesi.</li>
  <li><strong>Su testi:</strong> Amonyak, nitrit, nitrat, pH ve KH ölçümü ve sonuca göre öneri.</li>
  <li><strong>Ekipman kontrolü:</strong> Isıtıcı, filtre ve aydınlatmanın düzgün çalıştığının kontrolü.</li>
  <li><strong>Canlı kontrolü:</strong> Hastalık belirtileri ve beslenme düzeninin gözden geçirilmesi.</li>
</ul>

<h2>Ne sıklıkla bakım gerekir?</h2>
<p>Ev akvaryumlarında haftalık kısa bakım ve aylık kapsamlı bakım genellikle yeterlidir. Küçük (nano) akvaryumlarda su değerleri daha hızlı değiştiği için düzenlilik daha da önemlidir. Kendiniz yapmak isterseniz <a href="../nano-akvaryum-bakimi/">nano akvaryum bakım rutinimiz</a> adım adım yol gösterir.</p>

<h2>Bakım ihtiyacını azaltmanın yolları</h2>
<ul>
  <li><strong>Low-tech kurulum:</strong> Yavaş büyüyen bitkiler ve düşük-orta ışık, budama ve gübre ihtiyacını azaltır.</li>
  <li><strong>Doğru stok:</strong> Akvaryuma hacminden fazla balık koymamak su kalitesini korur.</li>
  <li><strong>Kapak:</strong> Buhar kapağı buharlaşmayı azaltır, su eklemeyi seyrekleştirir.</li>
  <li><strong>Az yem:</strong> Artık yem, su kalitesini en hızlı bozan etkendir.</li>
</ul>

<h2>Bakım hizmeti seçerken</h2>
<p>Bakım yapacak kişinin su testi yapıp yapmadığını, kendi ekipmanını getirip getirmediğini, canlılara ve bitkilere dair bilgi verip vermediğini sorun. Sabit bir bakım takvimi ve her ziyaretten sonra kısa bir rapor, akvaryumunuzun durumunu takip etmenizi kolaylaştırır.</p>

<p>Tankled olarak Ankara Ostim'deki atölyemizde ürettiğimiz akvaryumları low-tech, az bakım isteyen sistemler olarak tasarlıyoruz. Akvaryumunuzun bakımıyla ilgili sorularınız için <a href="../../iletisim/">bize ulaşabilirsiniz</a>.</p>
""",
    },
    {
        "slug": "akvaryum-sehpasi-olculeri",
        "baslik": "Akvaryum Sehpası Ölçüleri ve Seçimi Rehberi | Tankled",
        "h1": "Akvaryum sehpası ölçüleri: doğru sehpa nasıl seçilir?",
        "aciklama": "Akvaryum sehpası ölçüleri nasıl belirlenir? Akvaryum ağırlığı, sehpa yüksekliği, taşıma "
                    "kapasitesi ve malzeme seçimi için pratik rehber.",
        "tarih": "2026-10-25",
        "gorsel": "assets/g-crab.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Ahşap gövde üzerinde paludaryum detayı",
        "etiketler": ["akvaryum sehpası", "akvaryum sehpası ölçüleri", "akvaryum dolabı"],
        "govde": """
<p>Akvaryum sehpası, akvaryumun en çok ihmal edilen ama en kritik parçasıdır. Su dolu bir akvaryum çok ağırdır ve yükü tüm tabanına eşit dağıtılmalıdır. Bu rehberde <strong>akvaryum sehpası ölçüleri</strong>ni nasıl belirleyeceğinizi ve doğru sehpayı nasıl seçeceğinizi anlatıyoruz.</p>

<h2>1. Önce ağırlığı hesaplayın</h2>
<p>Su, litre başına yaklaşık 1 kg gelir. Buna cam, zemin, taş ve kök ağırlığı eklenir. Pratik bir kural olarak dolu bir akvaryumun ağırlığını <strong>litre × 1,2–1,5 kg</strong> olarak düşünebilirsiniz. Örneğin 100 litrelik bir akvaryum 120–150 kg civarındadır. Akvaryumunuzun litresini <a href="../../akvaryum-olustur/">3D akvaryum tasarım aracımızla</a> hesaplayabilirsiniz.</p>

<h2>2. Sehpa üst yüzeyi akvaryum tabanından küçük olmamalı</h2>
<p>Sehpanın üst yüzeyi, akvaryumun taban ölçüsüne eşit ya da biraz büyük olmalıdır. Akvaryum tabanının sehpadan taşması, camda gerilmeye ve zamanla çatlamaya yol açabilir. Üst yüzey tamamen düz ve terazide olmalıdır; küçük bir eğim bile camın köşelerine yük bindirir.</p>

<h2>3. Yükseklik: izleme açısına göre</h2>
<p>Akvaryumun ortası, oturduğunuzda göz hizanıza yakın olmalıdır. Salonda koltuktan izlenecek akvaryumlar için sehpa yüksekliği genellikle 60–80 cm arasında tercih edilir; ayakta izlenecek ya da konsol üstündeki akvaryumlarda daha yüksek olabilir. Çok yüksek sehpalar ise bakım sırasında akvaryumun içine uzanmayı zorlaştırır.</p>

<h2>4. Malzeme ve dayanıklılık</h2>
<ul>
  <li><strong>Sıradan mobilya:</strong> Akvaryum yükü için tasarlanmamıştır; zamanla esneyebilir.</li>
  <li><strong>MDF/sunta:</strong> Ekonomiktir ancak su ve nemle şişebilir.</li>
  <li><strong>Metal:</strong> Çok sağlamdır; üst tablanın düzlüğüne dikkat edilmelidir.</li>
  <li><strong>Masif ahşap:</strong> Sağlam ve dekoratiftir; tik gibi neme dayanıklı ağaçlar uzun ömürlüdür.</li>
</ul>

<h2>5. Dolap ve kablo düzeni</h2>
<p>Kapaklı bir akvaryum dolabı; filtre, yem ve test kitini saklamanızı, kabloları gizlemenizi sağlar. Dolabın arkasında kablolar ve hortumlar için delik ya da boşluk bırakılmalıdır.</p>

<h2>En kolay çözüm: mobilyalı akvaryum</h2>
<p>Sehpa ile akvaryumu ayrı ayrı seçmek yerine ikisini birlikte tasarlamak, ölçü uyumsuzluğu ve taşıma kapasitesi sorunlarını baştan ortadan kaldırır. <a href="../../mobilyali-akvaryum/">Mobilyalı akvaryum</a> sayfamızda modellerimizi, <a href="../../ozel-olcu-akvaryum/">özel ölçü akvaryum</a> sayfamızda ölçünüze göre üretim sürecini inceleyebilirsiniz.</p>
""",
    },
    {
        "slug": "ankara-akvaryum-rehberi",
        "baslik": "Akvaryum Ankara: Doğru Akvaryumu Seçme Rehberi | Tankled",
        "h1": "Ankara'da akvaryum alırken bilmeniz gereken her şey",
        "aciklama": "Ankara'da akvaryum mu arıyorsunuz? Ölçü, cam, aydınlatma, mobilyalı akvaryum ve kurulum "
                    "seçeneklerini karşılaştırın; Ostim atölyemizden ipuçları.",
        "tarih": "2026-10-27",
        "gorsel": "assets/g-lineup.webp", "gorsel_g": 1122, "gorsel_y": 1402,
        "gorsel_alt": "Ankara atölyesinde üretilen Tankled el yapımı akvaryum koleksiyonu",
        "etiketler": ["akvaryum Ankara", "Ankara akvaryumcu", "el yapımı akvaryum"],
        "govde": """
<p><strong>Akvaryum Ankara</strong> aramasıyla karşınıza çıkan seçenekler genellikle iki gruba ayrılır: hazır seri üretim cam tanklar satan mağazalar ve ölçüye göre üretim yapan atölyeler. Hangisinin size uygun olduğu; evinizdeki alana, ayırabileceğiniz bakım zamanına ve akvaryumun salonunuzda nasıl görünmesini istediğinize bağlıdır. Bu rehberde Ankara'da akvaryum alırken dikkat etmeniz gereken noktaları, Ostim'deki atölyemizde müşterilerimize en sık anlattığımız sırayla topladık.</p>

<h2>1. Önce yeri, sonra akvaryumu seçin</h2>
<p>Akvaryum, doğrudan güneş almayan, kalorifer peteğine ve kapıya yakın olmayan, sağlam bir zemine konmalıdır. Su dolu bir akvaryum litre başına yaklaşık bir kilogram ağırlık demektir; 60 litrelik bir kurulum zemin, taş ve camla birlikte 80 kilogramı rahatlıkla geçer. Bu yüzden akvaryumu koyacağınız mobilyanın bu yüke uygun olması şarttır. Akvaryumu ve gövdesini birlikte düşünen <a href="../mobilyali-akvaryum-nedir/">mobilyalı akvaryum</a> modelleri bu sorunu baştan çözer.</p>

<h2>2. Hacmi canlılara göre belirleyin</h2>
<p>"Hangi balığı istiyorum?" sorusu akvaryum hacmini belirler. Tek bir betta ya da bir grup karides için küçük, bitkili bir akvaryum yeterliyken sürü halinde yüzen tetra ve rasboralar daha uzun bir yüzme alanı ister. Karar vermeden önce <a href="../../baliklar/">balıklar rehberimizden</a> türlerin minimum hacim ihtiyaçlarına bakabilir, <a href="../../akvaryum-olustur/">3D akvaryum tasarım aracımızla</a> litre hesabını anında yapabilirsiniz.</p>

<h2>3. Cam, silikon ve işçilik kalitesine bakın</h2>
<p>Ankara'da akvaryum alırken çoğu kişi yalnızca fiyata ve ölçüye bakar; oysa uzun ömrü belirleyen camın kalınlığı, silikon işçiliği ve kenar bitişleridir. İyi bir akvaryumda silikon hatları düzgün ve kabarcıksızdır, cam kenarları rodajlıdır ve kapak buharı içeride tutar. El yapımı akvaryumlarda bu detayları üretim sırasında görebilir, ölçüyü evinize göre değiştirebilirsiniz.</p>

<h2>4. Aydınlatma: bitkiler ve atmosfer için</h2>
<p>Bitkili bir akvaryum için LED aydınlatma hem bitki büyümesini hem de odadaki atmosferi belirler. Tankled Betta Serisi'nde 3000K (sıcak), 4500K (nötr) ve 6500K (gün ışığı) olmak üzere üç ışık tonu bulunur; akşam sıcak ışıkla dekoratif bir abajur gibi, gündüz 6500K ile bitkiler için ideal bir ortam sağlar. Hangi bitkinin ne kadar ışık istediğini <a href="../../bitkiler/">bitkiler rehberimizde</a> bulabilirsiniz.</p>

<h2>5. Kurulum ve ilk haftalar</h2>
<p>Akvaryumu aldığınız gün balık eklemek en sık yapılan hatadır. Zemin, bitkiler ve filtre yerleştikten sonra suyun biyolojik olarak olgunlaşması (azot döngüsü) birkaç hafta sürer. Adım adım süreç için <a href="../betta-akvaryumu-kurulumu/">betta akvaryumu kurulum rehberimize</a> ve <a href="../../malzemeler/">malzemeler sayfamıza</a> göz atın.</p>

<h2>Ankara'da hazır mı, ölçüye göre mi?</h2>
<p>Hazır akvaryumlar hızlı ve ekonomiktir, ancak evinizdeki boşluğa ya da mobilyalarınıza uymayabilir. Ölçüye göre üretilen bir akvaryum ise duvar nişine, TV ünitesine ya da yatak odasındaki bir komodine tam oturacak şekilde tasarlanabilir. Tankled olarak Ankara Ostim'deki atölyemizde doğal masif ahşap gövdeli akvaryum, teraryum ve paludaryumları tek tek üretiyoruz; Ankara içinde atölyemize gelip ürünleri yerinde görebilir, Tüm modellerimizi Türkiye'nin 81 iline kargoyla gönderiyoruz; yurt dışına da kargo yapılabilir.</p>

<h2>Kısa kontrol listesi</h2>
<ul>
  <li>Akvaryumun duracağı yer ve taşıyacağı ağırlık belli mi?</li>
  <li>Bakacağınız canlılar ve ihtiyaç duydukları hacim belli mi?</li>
  <li>Cam ve silikon işçiliği, kapak ve aydınlatma kalitesi kontrol edildi mi?</li>
  <li>İlk haftalardaki su olgunlaşma süreci planlandı mı?</li>
</ul>
""",
    },
    {
        "slug": "mobilyali-akvaryum-nedir",
        "baslik": "Mobilyalı Akvaryum Nedir? Salon İçin Seçim Rehberi | Tankled",
        "h1": "Mobilyalı akvaryum nedir? Evinize uygun modeli seçme rehberi",
        "aciklama": "Mobilyalı akvaryum; akvaryum ile dolap, sehpa ya da konsolu tek parça birleştirir. Çeşitleri, "
                    "avantajları, ölçü ve malzeme seçimi bu rehberde.",
        "tarih": "2026-10-24",
        "gorsel": "assets/about.webp", "gorsel_g": 893, "gorsel_y": 1600,
        "gorsel_alt": "Ahşap gövdeli mobilyalı akvaryum bir yaşam alanında",
        "etiketler": ["mobilyalı akvaryum", "akvaryum mobilyası", "dekoratif akvaryum"],
        "govde": """
<p><strong>Mobilyalı akvaryum</strong>, cam haznenin bir dolap, sehpa, konsol, TV ünitesi ya da ahşap bir gövdeyle birlikte tasarlandığı akvaryum türüdür. Klasik akvaryumda önce tank alınır, sonra ona uyan bir sehpa aranır; mobilyalı akvaryumda ise ikisi baştan tek bir parça olarak düşünülür. Sonuç, salonda "teknik bir cihaz" yerine bir tasarım objesi gibi duran, kabloları ve ekipmanı gizlenmiş bir yaşam alanıdır.</p>

<h2>Mobilyalı akvaryum çeşitleri</h2>
<ul>
  <li><strong>Dolaplı akvaryum:</strong> Alt kısımda filtre, ısıtıcı ve yem gibi malzemelerin saklandığı kapaklı bir dolap bulunur.</li>
  <li><strong>Sehpa akvaryum:</strong> Orta sehpanın ya da yan sehpanın içine yerleştirilen, üstten izlenen akvaryumlardır.</li>
  <li><strong>TV ünitesi ve konsol akvaryum:</strong> Salonun ana duvarında mobilya bütünlüğünü bozmadan yer alır.</li>
  <li><strong>Masaüstü ahşap gövdeli akvaryum:</strong> Çalışma masası, komodin ya da kitaplık için tasarlanan kompakt modellerdir. Tankled Betta Serisi bu gruba girer.</li>
</ul>

<h2>Neden mobilyalı akvaryum tercih edilir?</h2>
<p>En önemli neden <strong>güvenliktir</strong>: Su dolu bir akvaryum çok ağırdır ve sıradan bir sehpa bu yükü uzun süre taşımak için tasarlanmamıştır. Akvaryuma özel üretilen gövde, ağırlığı düzgün dağıtır ve zamanla esneme yapmaz. İkinci neden <strong>görünümdür</strong>: kablolar, hortumlar ve filtre gözden kaybolur; akvaryum evin geri kalan mobilyalarıyla aynı dili konuşur. Üçüncüsü ise <strong>kullanım kolaylığıdır</strong>: bakım malzemeleri akvaryumun hemen yanında, düzenli biçimde saklanır.</p>

<h2>Malzeme seçimi: neden masif ahşap?</h2>
<p>Mobilyalı akvaryumlarda en sık kullanılan malzemeler MDF, kontrplak ve masif ahşaptır. Akvaryum çevresi nemli bir ortam olduğu için suya ve buhara dayanıklılık belirleyicidir. Tik ağacı, doğal yağ oranı yüksek olduğu için tekne yapımında da kullanılan, neme karşı dirençli bir ağaçtır. Tankled akvaryumlarının gövdesi eşsiz doğal çam ahşaptan ya da Endonezya'dan ithal doğal desenli ağaçtan üretilir ve tik yağıyla korunur; her parçanın damar deseni farklı olduğu için iki ürün birbirinin aynısı olmaz. Ahşap gövdeli modeller hakkında daha fazla fikir için <a href="../ahsap-akvaryum-fikirleri/">ahşap akvaryum fikirleri</a> yazımıza bakabilirsiniz.</p>

<h2>Mobilyalı akvaryum alırken nelere dikkat edilmeli?</h2>
<ol>
  <li><strong>Ölçü:</strong> Akvaryumun konacağı alanı ölçün; bakım için üstte en az 15–20 cm boşluk bırakın.</li>
  <li><strong>Taşıma kapasitesi:</strong> Gövdenin dolu akvaryumun ağırlığını taşıyacak şekilde üretildiğinden emin olun.</li>
  <li><strong>Havalandırma ve kapak:</strong> Buhar kapağı suyun buharlaşmasını ve ahşabın nemlenmesini azaltır.</li>
  <li><strong>Ekipman yeri:</strong> Filtre, ısıtıcı ve aydınlatmanın kablolarının nereden geçeceğini önceden planlayın.</li>
  <li><strong>Işık:</strong> Bitkili bir kurulum düşünüyorsanız ayarlanabilir LED aydınlatma büyük avantajdır.</li>
</ol>

<h2>Ankara'da mobilyalı akvaryum yaptırmak</h2>
<p>Ankara'da mobilyalı akvaryum arayanlar için en büyük avantaj ürünü üretildiği atölyede görebilmektir. Tankled olarak Ankara Ostim'deki atölyemizde ölçüye göre özel tasarım yapıyoruz: evinizdeki nişe, TV ünitesine ya da çalışma masanıza uygun ölçüyü birlikte belirliyor, malzemeyi ve ışık tonunu sizinle seçiyoruz. Ankara'da akvaryum seçerken nelere dikkat etmeniz gerektiğini <a href="../ankara-akvaryum-rehberi/">Ankara akvaryum rehberimizde</a> ayrıntılı anlattık.</p>
""",
    },
    {
        "slug": "betta-akvaryumu-kurulumu",
        "baslik": "Betta Akvaryumu Nasıl Kurulur? Adım Adım Rehber | Tankled",
        "h1": "Betta akvaryumu nasıl kurulur? Adım adım rehber",
        "aciklama": "Betta balığı için akvaryum kurulumu: hacim, sıcaklık, filtre, bitki seçimi ve su döngüsü. "
                    "Yeni başlayanlar için adım adım betta akvaryumu rehberi.",
        "tarih": "2026-10-20",
        "gorsel": "assets/g-betta-cozy.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Bitkili betta akvaryumu sıcak ışıklı bir oturma odasında",
        "etiketler": ["betta akvaryumu", "beta balığı bakımı", "akvaryum kurulumu"],
        "govde": """
<p>Betta (beta balığı ya da Siyam savaşçı balığı), renkleri ve uzun yüzgeçleriyle en sevilen akvaryum balıklarından biridir. Ancak "küçük bir kavanozda yaşar" efsanesi doğru değildir: sağlıklı bir betta için ısıtılmış, filtreli ve bitkili bir akvaryum gerekir. Bu rehberde bir <strong>betta akvaryumu</strong>nu baştan sona nasıl kuracağınızı adım adım anlatıyoruz.</p>

<h2>Betta için temel su değerleri</h2>
<ul>
  <li><strong>Sıcaklık:</strong> 24–28 °C (tropikal bir balıktır, oda sıcaklığı çoğu zaman yetmez)</li>
  <li><strong>pH:</strong> 6,5–7,5</li>
  <li><strong>Akıntı:</strong> Zayıf; uzun yüzgeçli bettalar güçlü akıntıda yorulur</li>
  <li><strong>Arkadaş:</strong> Erkek bettalar birbirine karşı saldırgandır; aynı akvaryuma iki erkek konmaz</li>
</ul>
<p>Farklı betta türlerinin (halfmoon, crowntail, plakat) özelliklerini <a href="../../baliklar/">balıklar rehberimizde</a> karşılaştırabilirsiniz.</p>

<h2>Adım 1: Akvaryumu ve yerini seçin</h2>
<p>Betta için kapaklı bir akvaryum seçin; bettalar zıplayabilir ve yüzeyden hava soludukları için kapak altındaki sıcak, nemli hava onlara iyi gelir. Hacim büyüdükçe su değerleri daha kararlı olur ve bakım kolaylaşır; küçük hacimlerde ise su değişimlerini daha sık yapmanız gerekir. Akvaryumu doğrudan güneş almayan, sabit bir yere koyun.</p>

<h2>Adım 2: Zemin ve hardscape</h2>
<p>Bitki yetiştirecekseniz besinli bir akvaryum toprağı, yalnızca anubias ve java eğreltisi gibi köklerini taşa/köke tutturan bitkiler kullanacaksanız ince kum ya da çakıl yeterlidir. Kök ve taşların keskin kenarı olmamasına dikkat edin; betta yüzgeçleri kolay yırtılır.</p>

<h2>Adım 3: Bitkiler</h2>
<p>Canlı bitkiler suyu temizler, bettaya saklanma alanı sağlar ve yosunla rekabet eder. Yeni başlayanlar için önerilerimiz: anubias nana, java eğreltisi, java yosunu, cryptocoryne wendtii ve yüzey için salvinia ya da limnobium. Betta, yüzeye yakın geniş yapraklarda dinlenmeyi sever. Tüm bitkilerin ışık ve bakım ihtiyaçları için <a href="../../bitkiler/">bitkiler rehberine</a> bakın.</p>

<h2>Adım 4: Filtre, ısıtıcı ve ışık</h2>
<p>Akıntıyı düşük tutan bir sünger filtre ya da akış ayarlı bir iç filtre, bettalar için en uygun seçenektir. Ayarlanabilir bir ısıtıcıyla suyu 26 °C civarında sabitleyin. Bitkiler için günde 6–8 saat ışık yeterlidir; daha uzun süre yosun sorununa yol açar. Ekipmanların ne işe yaradığını <a href="../../malzemeler/">malzemeler ve kurulum rehberimizde</a> ayrıntılı anlattık.</p>

<h2>Adım 5: Su döngüsü (en önemli adım)</h2>
<p>Akvaryumu suyla doldurduktan sonra su şartlandırıcı ekleyin ve balık koymadan önce filtrenin olgunlaşmasını bekleyin. Bu süreçte faydalı bakteriler, balık atıklarından oluşan zehirli amonyağı ve nitriti daha zararsız nitrata çevirir. Döngü genellikle 3–6 hafta sürer; bir test kitiyle amonyak ve nitrit sıfıra indiğinde betta eklenebilir.</p>

<h2>Adım 6: Bettayı akvaryuma alıştırma</h2>
<p>Bettayı poşetiyle birlikte 15–20 dakika akvaryum suyunun üzerinde yüzdürün ki sıcaklıklar eşitlensin. Ardından poşete azar azar akvaryum suyu ekleyip balığı nazikçe akvaryuma alın; mağaza suyunu akvaryuma dökmeyin.</p>

<h2>Bakım rutini</h2>
<ul>
  <li>Günde 1–2 kez, birkaç dakikada bitireceği kadar betta yemi verin.</li>
  <li>Haftada bir suyun yaklaşık %20–30'unu şartlandırılmış, aynı sıcaklıkta suyla değiştirin.</li>
  <li>Filtre süngerini musluk suyuyla değil, akvaryumdan aldığınız suyla çalkalayın.</li>
</ul>
<p>Haftalık bakımın ayrıntıları için <a href="../nano-akvaryum-bakimi/">nano akvaryum bakımı</a> yazımıza da göz atın. Hazır bir betta akvaryumu arıyorsanız, Ankara'daki atölyemizde üretilen ahşap gövdeli, sürgülü buhar kapaklı ve üç ışık tonlu <a href="../../#products">Tankled Betta Serisi</a>'ni inceleyebilirsiniz.</p>
""",
    },
    {
        "slug": "ahsap-akvaryum-fikirleri",
        "baslik": "Ahşap Akvaryum Fikirleri ve Akvaryum Dekorasyonu | Tankled",
        "h1": "Ahşap akvaryum fikirleri: akvaryumu dekorasyonun parçası yapın",
        "aciklama": "Ahşap gövdeli akvaryum, akvaryum dolabı ve dekoratif akvaryum fikirleri: salon, çalışma odası "
                    "ve yatak odası için ilham veren yerleşim önerileri.",
        "tarih": "2026-10-16",
        "gorsel": "assets/g-paludarium-stand.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Ahşap ve metal ayaklı dekoratif paludaryum",
        "etiketler": ["ahşap akvaryum", "dekoratif akvaryum", "akvaryum dekorasyonu"],
        "govde": """
<p>Akvaryum yalnızca balıkların yaşadığı bir cam kutu değil, bir odanın atmosferini tek başına değiştirebilen bir dekorasyon öğesidir. Ahşap gövdeli bir akvaryum ise bu etkiyi iki katına çıkarır: doğal malzeme, suyun ve bitkilerin canlılığıyla birleşince ortaya mobilya ile doğa arasında bir parça çıkar. İşte evinizde <strong>dekoratif akvaryum</strong> kullanmak için ilham verecek fikirler.</p>

<h2>1. Salonda odak noktası: konsol ya da TV ünitesi akvaryumu</h2>
<p>Salonda akvaryumu duvara dayalı bir konsolun ya da TV ünitesinin parçası yapmak, onu odanın odak noktasına dönüştürür. Ahşap tonunu salondaki diğer mobilyalarla aynı seçerseniz akvaryum "sonradan eklenmiş" gibi durmaz. Bu tip <a href="../mobilyali-akvaryum-nedir/">mobilyalı akvaryum</a> çözümlerinde ekipmanlar gövdenin içinde saklanır.</p>

<h2>2. Çalışma masasında nano akvaryum</h2>
<p>Küçük, bitkili bir nano akvaryum ya da betta akvaryumu çalışma masasında hem göz dinlendirir hem de bitkilerin yeşiliyle ofis ortamını yumuşatır. Kompakt ahşap gövdeli modeller kitaplık rafına ya da masanın köşesine kolayca sığar. Bakımın nasıl yapıldığını <a href="../nano-akvaryum-bakimi/">nano akvaryum bakımı</a> yazımızda anlattık.</p>

<h2>3. Yatak odasında abajur yerine akvaryum</h2>
<p>Sıcak (3000K) ışıklı bir akvaryum, akşamları bir abajur kadar yumuşak bir ışık verir. Tankled Betta Serisi'nin üç ışık tonu bu yüzden tasarlandı: gündüz bitkiler için gün ışığı, akşam dinlendirici sıcak ışık. Sessiz çalışan bir filtre seçmek yatak odasında önemlidir.</p>

<h2>4. Akvaryum yerine paludaryum ya da teraryum</h2>
<p>Ahşap gövdeli bir hazne yalnızca akvaryum olarak kullanılmak zorunda değildir. Su ve kara bölümü bir arada olan bir paludaryum, yengeç ve küçük amfibiler için; tamamen kara olan bir teraryum ise sukulentler, eğreltiler ya da gecko gibi egzotik hayvanlar için harika bir yaşam alanı olur. Paludaryuma uygun bitkileri <a href="../../bitkiler/">bitkiler rehberimizde</a> filtreleyebilirsiniz.</p>

<h2>5. Doğal tema: taş, kök ve yosun</h2>
<p>Ahşap gövdenin sıcaklığını içeride de sürdürmek için doğal bir aquascape kurun: bir iki büyük taş, kıvrımlı bir kök ve üzerine bağlanmış java yosunu ya da anubias. Bu düzen az bakım ister ve gövdeyle uyum içinde durur.</p>

<h2>Ahşap akvaryumda dikkat edilmesi gerekenler</h2>
<ul>
  <li><strong>Neme dayanıklı ağaç seçin:</strong> Tik gibi doğal yağ içeren ağaçlar nemli ortamda daha uzun ömürlüdür.</li>
  <li><strong>Yüzey koruması:</strong> Ahşabın düzenli yağlanması rengini ve dayanıklılığını korur.</li>
  <li><strong>Buhar kapağı:</strong> Suyun buharlaşmasını ve ahşabın sürekli nem almasını önler.</li>
  <li><strong>Suyu dökmeden bakım:</strong> Su değişimini hortumla yapmak gövdeye su sıçramasını engeller.</li>
</ul>

<p>Kendi akvaryumunuzu tasarlamadan önce ölçüleri, ışığı ve bitkileri <a href="../../akvaryum-olustur/">3D akvaryum tasarım aracımızda</a> deneyebilir, gerçek kurulumlardan örnekleri <a href="../../galeri/">galeride</a> görebilirsiniz. Ankara'da ölçüye göre ahşap akvaryum yaptırmak için Ostim'deki atölyemizle iletişime geçebilirsiniz.</p>
""",
    },
    {
        "slug": "nano-akvaryum-bakimi",
        "baslik": "Nano Akvaryum Bakımı: Haftalık Bakım Rutini | Tankled",
        "h1": "Nano akvaryum bakımı: 15 dakikalık haftalık rutin",
        "aciklama": "Nano akvaryum bakımı nasıl yapılır? Su değişimi, filtre temizliği, bitki budama ve yosun "
                    "kontrolü için kolay haftalık ve aylık bakım rutini.",
        "tarih": "2026-10-12",
        "gorsel": "assets/g-betta-moss.webp", "gorsel_g": 1195, "gorsel_y": 1600,
        "gorsel_alt": "Yosun dekorlu bitkili nano akvaryum",
        "etiketler": ["nano akvaryum", "akvaryum bakımı", "low tech akvaryum"],
        "govde": """
<p>Nano akvaryumlar (genellikle 30 litrenin altındaki akvaryumlar) az yer kaplar ve evin her köşesine uyum sağlar. Ancak küçük su hacmi, değerlerin hızlı değişebileceği anlamına gelir; bu yüzden düzenli ve kısa bir bakım rutini, büyük ve seyrek bakımdan çok daha etkilidir. İyi haber şu: doğru kurulmuş, bitkili, low-tech bir <strong>nano akvaryum</strong>un bakımı haftada 15 dakikayı geçmez.</p>

<h2>Günlük: 1 dakika</h2>
<ul>
  <li>Canlıları kısaca gözden geçirin: yüzgeçler açık mı, iştah normal mi?</li>
  <li>Isıtıcının çalıştığını ve sıcaklığın sabit olduğunu kontrol edin.</li>
  <li>Az yem verin; nano akvaryumda artık yem, su kalitesini en hızlı bozan etkendir.</li>
</ul>

<h2>Haftalık: 15 dakika</h2>
<ol>
  <li><strong>Camı temizleyin:</strong> Bir yosun kazıyıcı ya da sünger ile ön camdaki ince yosun tabakasını alın.</li>
  <li><strong>Su değişimi:</strong> Suyun %20–30'unu bir hortumla zemine yakın yerden çekin; bu sırada zemindeki artıkları da toplamış olursunuz.</li>
  <li><strong>Yeni suyu hazırlayın:</strong> Musluk suyunu su şartlandırıcıyla klordan arındırın ve akvaryumla aynı sıcaklığa getirin.</li>
  <li><strong>Yavaşça doldurun:</strong> Zemini dağıtmamak için suyu bir tabağın ya da elinizin üzerine dökün.</li>
</ol>

<h2>Aylık: 30 dakika</h2>
<ul>
  <li><strong>Filtre bakımı:</strong> Süngeri, su değişiminde çektiğiniz akvaryum suyunda hafifçe sıkın. Musluk suyu, filtredeki faydalı bakterileri öldürür.</li>
  <li><strong>Bitki budama:</strong> Hızlı büyüyen bitkilerin uçlarını kesin, çürüyen yaprakları alın, yüzey bitkilerini seyreltin.</li>
  <li><strong>Su testi:</strong> Bir test kitiyle nitrat, pH ve KH değerlerine bakın; değerler değişiyorsa su değişimi oranını ayarlayın.</li>
</ul>

<h2>Yosun sorunu nasıl önlenir?</h2>
<p>Nano akvaryumlarda yosunun üç ana nedeni vardır: fazla ışık, fazla yem ve az bitki. Aydınlatmayı günde 6–8 saatle sınırlayın, yemi azaltın ve hızlı büyüyen bitki (ör. hygrophila, limnophila, salvinia) ekleyin. Amano karidesi, nerit salyangozu ve otocinclus gibi temizlikçi canlılar da yosun kontrolüne yardımcı olur; uygun türleri <a href="../../baliklar/">balıklar rehberimizde</a> bulabilirsiniz.</p>

<h2>Low-tech nano akvaryum neden kolaydır?</h2>
<p>Low-tech akvaryum; CO₂ tüpü ve yoğun gübreleme kullanmadan, düşük-orta ışıkta yavaş büyüyen bitkilerle kurulan sistemdir. Bitkiler yavaş büyüdüğü için budama ve gübre ihtiyacı azdır, sistem dengeye kendiliğinden yaklaşır. Low-tech için uygun bitkileri <a href="../../bitkiler/">bitkiler rehberinde</a> "low tech" filtresiyle görebilirsiniz.</p>

<h2>Yeni başlıyorsanız</h2>
<p>Henüz akvaryumunuzu kurmadıysanız önce <a href="../betta-akvaryumu-kurulumu/">betta akvaryumu kurulum rehberimizi</a> okuyun; aynı adımlar tüm nano akvaryumlar için geçerlidir. Tankled Betta Serisi gibi buhar kapaklı ve ayarlanabilir ışıklı bir nano akvaryum, buharlaşmayı azaltıp ışık süresini kontrol etmeyi kolaylaştırarak bakımı daha da basitleştirir. Ankara'da nano akvaryum ve kurulum seti için bizimle iletişime geçebilirsiniz.</p>
""",
    },
]

CSS = """
  :root{--green:#5c7a5a;--green-deep:#43603f;--green-dark:#33492f;--cream:#f4f1e9;--sand:#cbb98f;--sand-deep:#b8a371;
    --ink:#2b3329;--muted:#6f7a68;--on-green:#f3f1e7;--radius-sm:18px;--ease:cubic-bezier(.22,.61,.36,1)}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--cream);color:var(--ink);font-family:'Poppins',sans-serif;font-weight:300;line-height:1.75;
    -webkit-font-smoothing:antialiased;min-height:100vh;display:flex;flex-direction:column}
  h1,h2,h3{font-weight:700;line-height:1.2;letter-spacing:-.02em;color:var(--green-dark)}
  h1{font-size:clamp(28px,5vw,44px)}
  a{color:inherit;text-decoration:none}
  img{max-width:100%;height:auto;display:block}
  .wrap{max-width:1180px;margin:0 auto;padding:0 16px;width:100%}
  .eyebrow{font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:var(--sand-deep);font-weight:600;margin-bottom:12px;display:inline-block}
  header{border-bottom:1px solid rgba(67,96,63,.1);background:var(--cream)}
  .nav{max-width:1180px;margin:0 auto;padding:0 16px;display:flex;align-items:center;justify-content:space-between;gap:16px;height:96px}
  .logo img{height:64px;width:auto}
  .back{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;color:var(--green-deep);
    padding:10px 20px;border-radius:100px;border:1.5px solid rgba(67,96,63,.25);transition:background .3s,border-color .3s;white-space:nowrap}
  .back:hover{border-color:var(--green);background:rgba(92,122,90,.08)}
  main{flex:1;padding:44px 0 80px}
  .kirinti{font-size:13px;color:var(--muted);margin-bottom:22px}
  .kirinti a{color:var(--green-deep)} .kirinti a:hover{text-decoration:underline}
  .intro{text-align:center;max-width:720px;margin:0 auto}
  .intro p{color:var(--muted);margin-top:12px}
  .liste{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;margin-top:40px}
  .kart{background:#fff;border-radius:var(--radius-sm);overflow:hidden;box-shadow:0 14px 30px -26px rgba(51,73,47,.6);
    display:flex;flex-direction:column;transition:transform .4s var(--ease)}
  .kart:hover{transform:translateY(-4px)}
  .kart img{width:100%;aspect-ratio:4/3;object-fit:cover}
  .kart .ic{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px}
  .kart h2{font-size:19px}
  .kart p{color:var(--muted);font-size:14px}
  .kart .devam{color:var(--green-deep);font-weight:600;font-size:14px;margin-top:4px}
  .meta{font-size:13px;color:var(--muted)}
  article{max-width:760px;margin:0 auto}
  article .kapak{border-radius:var(--radius-sm);margin:26px 0 30px;width:100%;max-height:520px;object-fit:cover}
  article h2{font-size:clamp(21px,3vw,26px);margin:36px 0 12px}
  article p,article li{font-size:16.5px;margin-bottom:14px}
  article ul,article ol{padding-left:22px;margin-bottom:14px}
  article li{margin-bottom:8px}
  article p a,article li a{color:var(--green-deep);font-weight:500;text-decoration:underline;text-underline-offset:3px}
  article strong{font-weight:600;color:var(--green-dark)}
  .etiketler{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .etiketler span{font-size:12px;padding:5px 12px;border-radius:100px;background:rgba(92,122,90,.12);color:var(--green-deep)}
  .cta{margin:44px 0 0;padding:28px;border-radius:var(--radius-sm);background:var(--green);color:var(--on-green)}
  .cta h2{color:var(--on-green);margin:0 0 8px;font-size:22px}
  .cta p{color:#cdd6c5;margin-bottom:16px}
  .btn{display:inline-flex;align-items:center;gap:8px;padding:13px 26px;border-radius:100px;background:var(--sand);
    color:var(--green-dark);font-weight:600;font-size:14px;letter-spacing:.03em;margin:4px 8px 4px 0}
  .ilgili{margin-top:44px}
  .ilgili h2{font-size:22px;margin-bottom:6px}
  .ilgili .liste{margin-top:18px}
  .foto-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:8px 0 16px}
  .foto-grid img{width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;border-radius:12px}
  @media(max-width:560px){.foto-grid{grid-template-columns:repeat(2,1fr)}}
  .foto-yer{aspect-ratio:3/4;border:2px dashed rgba(67,96,63,.3);border-radius:12px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:6px;padding:10px;text-align:center;background:rgba(92,122,90,.05)}
  .foto-yer span{font-size:13px;color:var(--muted)} .foto-yer figcaption{font-size:12px;color:var(--green-deep);font-weight:500}
  footer{padding:24px 0;font-size:13px;color:var(--muted);text-align:center;border-top:1px solid rgba(67,96,63,.1)}
  @media(max-width:560px){.nav{height:76px} .logo img{height:48px} .back{padding:9px 14px} main{padding:30px 0 60px}}
"""

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def tarih_tr(t: str) -> str:
    y, a, g = t.split("-")
    return f"{int(g)} {AYLAR[int(a) - 1]} {y}"


def iskelet(baslik: str, aciklama: str, onek: str, govde: str) -> str:
    # <!-- SEO --> blogu ve baslik/aciklama seo.py tarafindan yeniden yazilir.
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{baslik}</title>
<meta name="description" content="{aciklama}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="nav">
    <a href="{onek}" class="logo" aria-label="Tankled ana sayfa"><img src="{onek}assets/logo.png" alt="Tankled Aquarium" width="164" height="64" /></a>
    <a href="{onek}#contact" class="back">İletişim</a>
  </div>
</header>
<main>
  <div class="wrap">
{govde}
  </div>
</main>
<footer></footer>
<script>document.getElementById('year')&&(document.getElementById('year').textContent=new Date().getFullYear())</script>
</body>
</html>
"""


def kart(y: dict, onek: str, yazi_onek: str, baslik_etiketi: str = "h2") -> str:
    return (f'<a class="kart" href="{yazi_onek}{y["slug"]}/">'
            f'<img src="{onek}{y["gorsel"]}" alt="{y["gorsel_alt"]}" width="{y["gorsel_g"]}" height="{y["gorsel_y"]}" loading="lazy" />'
            f'<div class="ic"><span class="meta"><time datetime="{y["tarih"]}">{tarih_tr(y["tarih"])}</time></span>'
            f'<{baslik_etiketi}>{y["h1"]}</{baslik_etiketi}><p>{y["aciklama"]}</p>'
            f'<span class="devam">Devamını oku →</span></div></a>')


def _uretilmis_gorseller() -> None:
    """_kaynak/gorsel/blog_gorsel.py ile uretilen assets/blog/<slug>.webp varsa kapak olarak onu kullan."""
    for y in YAZILAR:
        if (KOK / "assets" / "blog" / f"{y['slug']}.webp").exists():
            y.update(gorsel=f"assets/blog/{y['slug']}.webp", gorsel_g=1200, gorsel_y=900)


_uretilmis_gorseller()


def sirali() -> list[dict]:
    return sorted(YAZILAR, key=lambda y: y["tarih"], reverse=True)


def uret() -> None:
    onek = "../"
    kartlar = "\n".join("      " + kart(y, onek, "") for y in sirali())
    govde = f"""    <nav class="kirinti" aria-label="Sayfa yolu"><a href="{onek}">Ana sayfa</a> › Blog</nav>
    <div class="intro">
      <span class="eyebrow">Tankled Blog</span>
      <h1>Akvaryum blogu: Ankara atölyemizden rehberler</h1>
      <p>Mobilyalı akvaryum seçiminden betta ve nano akvaryum kurulumuna, bakım rutinlerinden dekorasyon fikirlerine kadar Ankara Ostim'deki atölyemizde edindiğimiz deneyimleri paylaşıyoruz.</p>
    </div>
    <div class="liste">
{kartlar}
    </div>"""
    hedef = KOK / "blog" / "index.html"
    hedef.parent.mkdir(exist_ok=True)
    hedef.write_text(iskelet(BLOG_BASLIK, BLOG_ACIKLAMA, onek, govde), encoding="utf-8")

    onek = "../../"
    for y in YAZILAR:
        ilgili = [d for d in sirali() if d["slug"] != y["slug"]][:3]
        ilgili_html = "\n".join("        " + kart(d, onek, "../", "h3") for d in ilgili)
        etiketler = "".join(f"<span>{e}</span>" for e in y["etiketler"])
        govde = f"""    <article>
      <nav class="kirinti" aria-label="Sayfa yolu"><a href="{onek}">Ana sayfa</a> › <a href="../">Blog</a> › {y["h1"]}</nav>
      <span class="eyebrow">Tankled Blog</span>
      <h1>{y["h1"]}</h1>
      <p class="meta" style="margin-top:12px">Tankled Atölye · <time datetime="{y["tarih"]}">{tarih_tr(y["tarih"])}</time></p>
      <div class="etiketler">{etiketler}</div>
      <img class="kapak" src="{onek}{y["gorsel"]}" alt="{y["gorsel_alt"]}" width="{y["gorsel_g"]}" height="{y["gorsel_y"]}" />
{y["govde"].strip()}
      <section class="cta">
        <h2>Ankara'da el yapımı akvaryum</h2>
        <p>Ostim'deki atölyemizde doğal masif ahşaptan mobilyalı ve dekoratif akvaryumlar üretiyoruz. Türkiye'nin 81 iline ve yurt dışına kargo yapıyoruz. Ölçünüze özel tasarım için bize ulaşın.</p>
        <a class="btn" href="https://wa.me/905312172006?text=Merhaba%20Tankled%2C%20bilgi%20almak%20istiyorum." target="_blank" rel="noopener">WhatsApp ile yazın</a>
        <a class="btn" href="{onek}#products">Koleksiyonu inceleyin</a>
      </section>
      <section class="ilgili">
        <h2>Diğer yazılar</h2>
        <div class="liste">
{ilgili_html}
        </div>
      </section>
    </article>"""
        hedef = KOK / "blog" / y["slug"] / "index.html"
        hedef.parent.mkdir(parents=True, exist_ok=True)
        hedef.write_text(iskelet(y["baslik"], y["aciklama"], onek, govde), encoding="utf-8")


if __name__ == "__main__":
    uret()
