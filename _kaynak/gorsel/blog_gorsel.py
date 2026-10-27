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
REFERANS = SITE / "assets/galeri/urun-bicim-01-tam-onden.jpg"
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


# (hedef dosya, urun gorunsun mu, sahne)
SAHNE = {
    # blog yazilari
    "teraryum-nasil-yapilir": (True, "used as a closed terrarium with layered drainage pebbles, soil, moss, a small fern and fittonia, on a wooden workbench with terrarium tools"),
    "teraryum-bitkileri-ve-bakimi": (False, "close-up of terrarium plants: pink and green fittonia, selaginella, small ferns and cushion moss inside a glass terrarium, droplets on the glass"),
    "dekoratif-abajur-fikirleri": (True, "used as a decorative table lamp glowing with warm 3000K light, holding moss and small plants, on a side table next to a linen sofa in a cozy living room at dusk"),
    "gece-lambasi-olarak-isikli-teraryum": (True, "used as a night light on a bedside table in a calm dark bedroom, glowing softly with warm light through moss and plants, a book and bed linen beside it"),
    "isikli-bitki-saksisi": (True, "used as an illuminated planter with succulents and a small cactus on a pebble drainage layer, LED on, on a shelf in a room corner without windows"),
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
    # ana sayfa kullanim kartlari
    "kullanim/akvaryum": (True, "as a planted aquarium with a red betta fish, warm cozy living room background"),
    "kullanim/teraryum": (True, "as a closed forest terrarium with moss, ferns and a small piece of wood, condensation on the glass"),
    "kullanim/abajur": (True, "as a glowing decorative table lamp with warm light in a dim elegant room, moss inside"),
    "kullanim/bitki-saksisi": (True, "as an illuminated succulent planter with echeveria and haworthia on a pebble layer, LED on, minimal desk"),
}


def istem(urun: bool, sahne: str) -> str:
    on = (URUN + "Place this product in a new scene: the product is " + sahne) if urun else ("Show " + sahne)
    return (on + ". Realistic high-end interior and nature photography, natural colors, soft light, shallow depth "
            "of field, horizontal 4:3 framing. No text, no labels, no watermark, no people's faces.")


def uret(ad: str, ist_anahtar: str) -> str:
    urun, sahne = SAHNE[ad]
    hedef = (SITE / "assets" / (ad if "/" in ad else f"blog/{ad}")).with_suffix(".webp")
    if hedef.exists() and "--yeniden" not in sys.argv:
        return "var"
    parcalar = [{"text": istem(urun, sahne)}]
    if urun:
        parcalar.append({"inline_data": {"mime_type": "image/jpeg",
                                         "data": base64.b64encode(REFERANS.read_bytes()).decode()}})
    govde = json.dumps({"contents": [{"parts": parcalar}],
                        "generationConfig": {"responseModalities": ["IMAGE"],
                                             "imageConfig": {"aspectRatio": "4:3"}}}).encode()
    istek = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=govde, headers={"Content-Type": "application/json", "x-goog-api-key": ist_anahtar})
    try:
        with urllib.request.urlopen(istek, timeout=180) as y:
            cevap = json.load(y)
        veri = next(p["inlineData"]["data"] for p in cevap["candidates"][0]["content"]["parts"] if "inlineData" in p)
        im = ImageOps.fit(Image.open(io.BytesIO(base64.b64decode(veri))).convert("RGB"), (1200, 900), Image.LANCZOS)
        hedef.parent.mkdir(parents=True, exist_ok=True)
        im.save(hedef, "WEBP", quality=80, method=6)
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
