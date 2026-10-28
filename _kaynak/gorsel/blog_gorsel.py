"""Blog yazilari ve ana sayfadaki "Kullanim alanlari" kartlari icin Gemini ile gorsel uretir.

Cikti: assets/blog/<slug>.webp ve assets/kullanim/<ad>.webp (1200x900, 4:3 WebP).
Gorsel varsa site uretici (_seo/seo.py) onu otomatik kullanir; yoksa mevcut fotograf kalir.

Calistirma (anahtar GEMINI_API_KEY ortam degiskeninden ya da ../tankled-otomasyon/.env'den okunur):
    python3 _kaynak/gorsel/blog_gorsel.py              # eksik gorselleri uret
    python3 _kaynak/gorsel/blog_gorsel.py teraryum-nasil-yapilir --yeniden
    python3 -B _seo/seo.py                             # sayfalari yeni gorsellerle yeniden uret

Urunun gorundugu sahnelerde gercek urun fotografi referans olarak gonderilir; boylece Gemini
Tankled tasarimini (ahsap gövde, cam hazne, ust LED) degistirmeden yeni bir ortama yerlestirir.
"""
import base64, io, json, os, pathlib, sys, urllib.request, concurrent.futures as cf
from PIL import Image, ImageOps

SITE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SITE / "_seo"))
import blog  # noqa: E402

MODEL = "gemini-3.1-flash-image"
# Urunu her acidan dogru cizsin diye birden fazla gercek urun fotografi gonderilir
REFERANSLAR = [SITE / "assets/galeri" / ad for ad in (
    "urun-bicim-01-tam-onden.jpg", "urun-bicim-02-sol-45.jpg", "urun-isik-3000k-45-derece.jpg")]
URUN = ("Keep the product from the reference photo exactly as it is: a small handmade square glass tank "
        "with a natural solid wood base and a wooden top cap with an integrated LED light. Do not change its "
        "shape, proportions or materials and do not add any logo or text to it. ")


def anahtar() -> str:
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"].strip()
    env = SITE.parent / "tankled-otomasyon" / ".env"
    for satir in env.read_text(encoding="utf-8").splitlines() if env.exists() else []:
        if satir.startswith("GEMINI_API_KEY="):
            return satir.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY bulunamadi (ortam degiskeni ya da ../tankled-otomasyon/.env).")


OLCEK = ("It is a SMALL object, about 14 x 14 x 20 cm, roughly twice the height of a single coffee mug, "
         "so show it at true scale next to a few everyday objects (never stacked cups). ")

# (hedef dosya, urun gorunsun mu, sahne)
SAHNE = {
    # blog yazilari
    "teraryum-nasil-yapilir": (True, "used as a closed terrarium with layered drainage pebbles, soil, moss, a small fern and fittonia, on a wooden workbench with terrarium tools"),
    "teraryum-bitkileri-ve-bakimi": (False, "close-up of terrarium plants: pink and green fittonia, selaginella, small ferns and cushion moss inside a glass terrarium, droplets on the glass"),
    # Kullanici geri bildirimi (2026-10-28): karanlik/kasvetli, isik etkisi yok, ic karisik -> yeniden yazildi
    "dekoratif-abajur-fikirleri": (True, OLCEK + "used as a decorative table lamp in the evening: the room's main lights are off, "
        "the product's warm 3000K LED is the hero light, casting a soft warm pool of light on a walnut side table and a gentle glow "
        "on the wall behind. Inside the glass only a few smooth river stones and a small tuft of moss, very minimal and tidy. "
        "A ceramic mug and a hardcover book beside it, a linen armchair softly blurred. Cozy, elegant, magazine-quality interior photo"),
    "gece-lambasi-olarak-isikli-teraryum": (True, OLCEK + "used as a night light on a bedside table at night: the bedroom is dark and "
        "calm, the product glows with a soft warm amber light that softly illuminates the nightstand, a folded book and the edge of "
        "crisp white bed linen. Inside the glass a neat little moss landscape with one small fern. Peaceful, inviting, high-end "
        "lifestyle photo with deep shadows but a clearly visible, beautiful glow"),
    "isikli-bitki-saksisi": (True, OLCEK + "used as a bright illuminated planter on a light oak desk in a sunny Scandinavian room: "
        "inside the glass a tidy, healthy arrangement of three echeveria succulents and one small cactus on white pebbles, LED on. "
        "Bright natural daylight, clean white wall, a small notebook and a pencil next to it. Fresh, airy, premium product photo"),
    "masa-ustu-bitki-saksisi-ofis": (True, "used as a desktop planter with a small pothos and peperomia on a modern office desk next to a laptop and a coffee mug, LED on"),
    "bitkili-akvaryum-kurulumu": (False, "a lush low-tech planted freshwater aquarium with anubias, java fern, cryptocoryne and stem plants, driftwood and stones, natural light"),
    "akvaryum-filtresi-ve-pompasi": (False, "a clean small planted aquarium with a sponge filter producing gentle bubbles, crystal clear water, close-up"),
    "akvaryum-kumu-ve-zemin": (False, "macro view of aquarium substrate layers seen through glass: nutrient aqua soil, fine sand and smooth pebbles with small carpeting plants"),
    "akvaryum-fiyatlari": (True, "as a handmade aquarium product shot on a wooden table in a bright minimalist living room, planted with a red betta fish"),
    "ankara-akvaryum-bakim-hizmeti": (False, "hands cleaning the inside glass of a small planted aquarium with a magnetic algae scraper, siphon hose and a water test kit next to it"),
    "akvaryum-sehpasi-olculeri": (False, "a medium planted aquarium standing on a solid wooden cabinet stand in a modern living room, measuring tape on the cabinet"),
    "ankara-akvaryum-rehberi": (True, "several of these handmade aquariums of different sizes displayed in a warm craftsman workshop with wooden workbenches"),
    "mobilyali-akvaryum-nedir": (True, "integrated into a wooden living room console as a furniture piece, planted aquarium with a betta fish, warm interior design"),
    "betta-akvaryumu-kurulumu": (True, "as a planted betta aquarium with a vivid blue and red halfmoon betta fish, driftwood, anubias and floating plants, on a study desk"),
    "ahsap-akvaryum-fikirleri": (True, "on a wooden bookshelf among books and ceramics as a decorative planted aquarium, Scandinavian interior"),
    "nano-akvaryum-bakimi": (True, "as a nano aquarium with shrimp and moss on a kitchen counter, a small water jug and fish food beside it"),
    # galeri sahneleri (assets/galeri/<ad>.webp) -> uretildikten sonra galeri/index.html'e kart olarak eklenir
    "galeri/sahne-balkon-bitkili": (True, OLCEK + "as a planted aquarium on a small teak side table on a sunny city balcony with potted herbs, golden hour light"),
    "galeri/sahne-mutfak-tezgahi": (True, OLCEK + "as an illuminated herb and moss planter on a white marble kitchen counter beside a cutting board and a bowl of lemons, morning light"),
    "galeri/sahne-otel-resepsiyonu": (True, OLCEK + "as a decorative planted aquarium on a boutique hotel reception desk with brass details, warm elegant lighting"),
    "galeri/sahne-magaza-vitrini": (True, OLCEK + "as a display piece with a single succulent on a minimalist boutique shop shelf next to ceramics, soft spotlight"),
    "galeri/sahne-restoran-masasi": (True, OLCEK + "as a glowing table lamp with smooth stones inside on a restaurant table set for dinner, candle-like warm ambience"),
    "galeri/sahne-toplanti-odasi": (True, OLCEK + "as a planted betta aquarium on a long oak meeting table in a bright modern office meeting room, notebooks and glasses of water"),
    "galeri/sahne-bahce-masasi": (True, OLCEK + "as a moss terrarium on a weathered wooden garden table outdoors, lush greenery softly blurred, soft overcast light"),
    "galeri/sahne-gekko-yuvasi": (True, OLCEK + "as a small dry habitat with bark, moss and a tiny leopard gecko inside, on a wooden shelf in a calm room"),
    # ana sayfa kullanim kartlari
    "kullanim/akvaryum": (True, "as a planted aquarium with a red betta fish, warm cozy living room background"),
    "kullanim/teraryum": (True, "as a closed forest terrarium with moss, ferns and a small piece of wood, condensation on the glass"),
    "kullanim/abajur": (True, OLCEK + "as a glowing decorative table lamp in the evening: warm 3000K light pools on a walnut side table "
        "and the wall, only a few smooth stones and a tuft of moss inside, tidy and elegant, cozy living room softly blurred"),
    "kullanim/bitki-saksisi": (True, OLCEK + "as a bright illuminated planter with three echeveria succulents on white pebbles, LED on, "
        "on a light oak desk in bright daylight, clean minimal styling"),
}


GERCEKCI = (
    "Ultra-realistic photograph, indistinguishable from a real camera photo: shot on a full-frame camera "
    "with a 35mm or 50mm lens at f/2.8, natural window light with soft shadows, true-to-life textures "
    "(real wood grain, glass reflections, water clarity, leaf veins), subtle real-world imperfections, "
    "accurate scale and perspective, natural white balance and restrained colors. "
    "Not CGI, not 3D render, not illustration, no plastic look, no oversaturation, no HDR halo. "
)


def istem(urun: bool, sahne: str) -> str:
    on = (URUN + "The reference photos show the same real product from several angles. Place this product "
          "in a new scene: the product is " + sahne) if urun else ("Show " + sahne)
    return (on + ". " + GERCEKCI + "Horizontal 4:3 framing. No text, no labels, no watermark, no people's faces.")


def uret(ad: str, ist_anahtar: str) -> str:
    urun, sahne = SAHNE[ad]
    hedef = (SITE / "assets" / (ad if "/" in ad else f"blog/{ad}")).with_suffix(".webp")
    if hedef.exists() and "--yeniden" not in sys.argv:
        return "var"
    parcalar = [{"text": istem(urun, sahne)}]
    if urun:
        for ref in REFERANSLAR:
            parcalar.append({"inline_data": {"mime_type": "image/jpeg",
                                             "data": base64.b64encode(ref.read_bytes()).decode()}})
    govde = json.dumps({"contents": [{"parts": parcalar}],
                        "generationConfig": {"responseModalities": ["IMAGE"],
                                             "imageConfig": {"aspectRatio": "4:3", "imageSize": "1K"}}}).encode()
    istek = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=govde, headers={"Content-Type": "application/json", "x-goog-api-key": ist_anahtar})
    try:
        with urllib.request.urlopen(istek, timeout=300) as y:
            cevap = json.load(y)
        veri = next(p["inlineData"]["data"] for p in cevap["candidates"][0]["content"]["parts"] if "inlineData" in p)
        im = ImageOps.fit(Image.open(io.BytesIO(base64.b64decode(veri))).convert("RGB"), (1024, 768), Image.LANCZOS)
        hedef.parent.mkdir(parents=True, exist_ok=True)
        im.save(hedef, "WEBP", quality=84, method=6)
        return "ok"
    except Exception as e:  # noqa: BLE001
        return f"HATA {e}"[:160]


if __name__ == "__main__":
    eksik = set(y["slug"] for y in blog.YAZILAR) - set(SAHNE)
    if eksik:
        print("Uyari: sahnesi tanimli olmayan yazilar:", ", ".join(sorted(eksik)))
    secili = [a for a in sys.argv[1:] if not a.startswith("--")] or list(SAHNE)
    k = anahtar()
    with cf.ThreadPoolExecutor(4) as ex:
        for ad, durum in zip(secili, ex.map(lambda a: uret(a, k), secili)):
            print(f"{ad}: {durum}", flush=True)
