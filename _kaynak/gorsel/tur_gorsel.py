"""Sitedeki balik ve bitki kartlari icin eksik gorselleri Gemini ile uretir (4:3, 800x600 JPEG)."""
import io, re, sys, pathlib, concurrent.futures as cf
from PIL import Image, ImageOps
sys.path.insert(0, "/Users/aydemirs/Desktop/BEYZA Aİ/tankled-otomasyon")
from src.gemini import GeminiIstemci
from google.genai import types

SITE = pathlib.Path("/Users/aydemirs/Desktop/BEYZA Aİ/Tankled.github.io")
env = {k: v.strip() for k, v in (l.split("=", 1) for l in open("/Users/aydemirs/Desktop/BEYZA Aİ/tankled-otomasyon/.env", encoding="utf-8").read().splitlines() if "=" in l and not l.startswith("#"))}
ist = GeminiIstemci(env["GEMINI_API_KEY"])

def ogeler(data):
    s = (SITE / data).read_text()
    cat = None; sonuc = []
    for m in re.finditer(r"id: '([^']+)',\s*title|foto: '([^']+)', ad: '([^']+)', latin: '([^']+)'.*?aciklama: '((?:[^'\\]|\\.)*)'", s, re.S):
        if m.group(1): cat = m.group(1)
        else: sonuc.append((cat, m.group(2), m.group(3), m.group(4), m.group(5).replace("\\'", "'")))
    return sonuc

ORTAM = {
    "paludaryum": "growing in a lush, humid paludarium or terrarium on moss and wood, out of water",
    "omurgasiz": "in a planted freshwater aquarium, macro photography",
}
def istem(tur, cat, ad, latin, aciklama):
    if tur == "balik":
        yer = "on damp moss and wood in a paludarium, partly out of water" if cat == "paludaryum" else ORTAM.get(cat, "swimming in a natural planted freshwater aquarium")
        konu = f"a single healthy {latin} ({ad})" if cat not in ("nano",) else f"a small group of healthy {latin} ({ad})"
    else:
        yer = ORTAM["paludaryum"] if cat == "paludaryum" else "growing underwater in a natural planted freshwater aquarium"
        konu = f"the aquarium plant {latin} ({ad})"
    return (f"Realistic high-quality nature photograph of {konu}, {yer}. Accurate species appearance: {aciklama} "
            "The subject is centered, sharp and true to life, natural colors, soft light, shallow depth of field, "
            "clean background. Horizontal 4:3 framing. No text, no labels, no watermark, no people.")

def uret(is_):
    tur, klasor, (cat, foto, ad, latin, aciklama) = is_
    hedef = SITE / klasor / f"{foto}.jpg"
    if hedef.exists() and "--yeniden" not in sys.argv: return foto, "var"
    try:
        c = ist._istemci.models.generate_content(
            model="gemini-3.1-flash-image", contents=istem(tur, cat, ad, latin, aciklama),
            config=types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="4:3")))
        veri = next(p.inline_data.data for p in c.candidates[0].content.parts if getattr(p, "inline_data", None))
        im = ImageOps.fit(Image.open(io.BytesIO(veri)).convert("RGB"), (800, 600), Image.LANCZOS)
        hedef.parent.mkdir(parents=True, exist_ok=True)
        im.save(hedef, "JPEG", quality=82, optimize=True, progressive=True)
        return foto, "ok"
    except Exception as e:
        return foto, f"HATA {e}"[:120]

isler = [("balik", "assets/baliklar", o) for o in ogeler("assets/baliklar-data.js")]
isler += [("bitki", "assets/bitkiler", o) for o in ogeler("assets/bitkiler-data.js")]
secili = [a for a in sys.argv[1:] if not a.startswith("--")]
if secili: isler = [i for i in isler if i[2][1] in secili]
with cf.ThreadPoolExecutor(4) as ex:
    for foto, d in ex.map(uret, isler):
        if d != "var": print(foto, d, flush=True)
