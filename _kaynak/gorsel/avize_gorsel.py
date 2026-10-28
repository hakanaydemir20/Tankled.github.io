"""Tankled imza avize icin Gemini ile salon sahneleri uretir -> assets/avize/<ad>.webp (1024x768).

Gercek avize fotograflari (_kaynak/gorsel/avize-ref/) referans gonderilir; avizenin bicimi korunur,
yalnizca ortam degisir.
    ../tankled-otomasyon/.venv/bin/python _kaynak/gorsel/avize_gorsel.py [ad ...] [--yeniden]
"""
import base64, io, json, pathlib, sys, urllib.request
from PIL import Image, ImageOps
from blog_gorsel import GERCEKCI, MODEL, SITE, anahtar

REF = sorted((SITE / "_kaynak/gorsel/avize-ref").glob("*.jpg"))
AVIZE = ("Keep the ceiling light from the reference photos exactly as it is: a rectangular open frame "
         "made of natural pine wood slats with a continuous white LED strip on its underside, hung flush "
         "close to the ceiling by four very thin steel wires from a small slim black rectangular driver box "
         "mounted on the ceiling. Do not change its shape, proportions, wood color or materials, do not add "
         "glass, fabric, bulbs, logos or text. ")
SAHNE = {
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


def uret(ad: str, k: str) -> str:
    hedef = SITE / "assets/avize" / f"{ad}.webp"
    if hedef.exists() and "--yeniden" not in sys.argv:
        return "var"
    metin = (AVIZE + "The reference photos show the same real product. Place this exact ceiling light in a new "
             "scene: " + SAHNE[ad] + ". Show the whole light at realistic size (about 60 x 40 cm) on a normal "
             "2.7 m ceiling. " + GERCEKCI + "Horizontal 4:3 framing. No text, no labels, no watermark, no people.")
    parcalar = [{"text": metin}] + [{"inline_data": {"mime_type": "image/jpeg",
                                    "data": base64.b64encode(r.read_bytes()).decode()}} for r in REF]
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
    for ad in [a for a in sys.argv[1:] if not a.startswith("--")] or list(SAHNE):
        print(ad, uret(ad, k), flush=True)
