"""Aydinlatma urunleri (imza avize, akvaryum aydinlatma bari) icin Gemini ile sahne uretir
-> assets/<urun>/<ad>.webp (1024x768).

Gercek urun fotograflari (_kaynak/gorsel/<urun>-ref/) referans gonderilir; urunun bicimi korunur,
yalnizca ortam degisir.
    ../tankled-otomasyon/.venv/bin/python _kaynak/gorsel/urun_gorsel.py avize|lamba [ad ...] [--yeniden]
"""
import base64, io, json, pathlib, sys, urllib.request
from PIL import Image, ImageOps
from blog_gorsel import GERCEKCI, MODEL, SITE, anahtar

AVIZE = ("Keep the ceiling light from the reference photos exactly as it is: a rectangular open frame "
         "made of natural pine wood slats with a continuous white LED strip on its underside, hung flush "
         "close to the ceiling by four very thin steel wires from a small slim black rectangular driver box "
         "mounted on the ceiling. Do not change its shape, proportions, wood color or materials, do not add "
         "glass, fabric, bulbs, logos or text. ")
SAHNE_AVIZE = {
    "salon-modern": "a modern Turkish apartment living room in the evening: light beige sofa, grey rug, "
                    "low walnut coffee table, the ceiling light centered above the seating area and switched on "
                    "with a warm 3000K glow, soft ambient lamp light",
    "yemek-alani": "an open plan dining area: solid wood dining table with six upholstered chairs, the ceiling "
                   "light centered directly above the table and switched on with a neutral 4500K light, "
                   "plates and a small vase on the table, calm late afternoon",
    "salon-iskandinav": "a bright Scandinavian bohemian living room in daylight: large window with linen "
                        "curtains, green indoor plants, rattan armchair, light oak floor, the ceiling light "
                        "centered on the ceiling and switched on at a dimmed soft level",
}

LAMBA = ("Keep the aquarium LED light bar from the reference photos exactly as it is: a long slim brushed "
         "aluminium bar with a white LED strip on its underside, held at both ends by matte black clip-on "
         "holders that rest on the top glass edges of a rimless glass aquarium. Do not change its shape, "
         "proportions, colors or materials and do not add any logo or text to it. ")
SAHNE_LAMBA = {
    "yakin-cekim": "a close-up, three-quarter view of the light bar mounted on the top edge of a rimless planted "
                   "aquarium; the black end holder and the slim aluminium body are sharp and in focus, the "
                   "bright white light falls into the water and reflects on the surface, plants softly blurred",
    "bitkili-akvaryum": "a lush planted aquascape aquarium on a wooden cabinet in a living room in the evening; "
                        "the light bar on top is switched on and is the sharp focal point in the foreground, "
                        "the room behind is softly blurred with warm ambient light",
    "calisma-odasi": "a modern home office: a small rimless nano aquarium with green plants and small tetras on "
                     "a light wooden console next to a desk, the light bar on top switched on with crisp 6500K "
                     "daylight white light, clearly visible and highlighted",
}
URUNLER = {
    "avize": (AVIZE, SAHNE_AVIZE, "Show the whole light at realistic size (about 60 x 40 cm) on a normal 2.7 m ceiling. "),
    "lamba": (LAMBA, SAHNE_LAMBA, "The bar spans the full width of the aquarium at realistic scale. "),
}


def uret(urun: str, ad: str, k: str) -> str:
    tarif, sahneler, olcek = URUNLER[urun]
    ref = sorted((SITE / f"_kaynak/gorsel/{urun}-ref").glob("*.jpg"))
    hedef = SITE / f"assets/{urun}" / f"{ad}.webp"
    if hedef.exists() and "--yeniden" not in sys.argv:
        return "var"
    metin = (tarif + "The reference photos show the same real product. Place this exact product in a new "
             "scene: " + sahneler[ad] + ". " + olcek + GERCEKCI + "Horizontal 4:3 framing. No text, no labels, no watermark, no people.")
    parcalar = [{"text": metin}] + [{"inline_data": {"mime_type": "image/jpeg",
                                    "data": base64.b64encode(r.read_bytes()).decode()}} for r in ref]
    govde = json.dumps({"contents": [{"parts": parcalar}],
                        "generationConfig": {"responseModalities": ["IMAGE"],
                                             "imageConfig": {"aspectRatio": "4:3", "imageSize": "1K"}}}).encode()
    istek = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=govde, headers={"Content-Type": "application/json", "x-goog-api-key": k})
    try:
        with urllib.request.urlopen(istek, timeout=300) as y:
            cevap = json.load(y)
        veri = next(p["inlineData"]["data"] for p in cevap["candidates"][0]["content"]["parts"] if "inlineData" in p)
        im = ImageOps.fit(Image.open(io.BytesIO(base64.b64decode(veri))).convert("RGB"), (1024, 768), Image.LANCZOS)
        hedef.parent.mkdir(parents=True, exist_ok=True)
        im.save(hedef, "WEBP", quality=84, method=6)
        return "ok"
    except Exception as e:  # noqa: BLE001
        return f"HATA {e}"[:200]


if __name__ == "__main__":
    k = anahtar()
    urun, *adlar = [a for a in sys.argv[1:] if not a.startswith("--")]
    for ad in adlar or list(URUNLER[urun][1]):
        print(ad, uret(urun, ad, k), flush=True)
