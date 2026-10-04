"""Gercekci halfmoon betta (mavi govde, maviden beyaza acilan yuzgecler) - Blender 5.x

Blender'da: Scripting sekmesi > Open > bu dosya > Run Script.
Terminalden:  Blender -b --factory-startup --python betta_gercekci.py
Cikti: ayni klasore betta_gercekci.blend ve betta_gercekci.glb (yuzme animasyonlu).
"""

import math
import os
import random
from math import pi, sin, cos

import bpy
from mathutils import Matrix, Vector, noise

KLASOR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.expanduser("~/Downloads")
CIKTI_BLEND = os.path.join(KLASOR, "betta_gercekci.blend")
CIKTI_GLB = os.path.join(KLASOR, "betta_gercekci.glb")
KARE = 72  # 3 sn @24fps, kesintisiz dongu
random.seed(7)

if bpy.app.background:
    bpy.ops.wm.read_factory_settings(use_empty=True)
else:
    # Blender penceresinde: arayuzu bozmadan sahneyi ve onceki verileri temizle
    for koleksiyon in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.lights,
                       bpy.data.cameras, bpy.data.actions, bpy.data.worlds):
        for blok in list(koleksiyon):
            koleksiyon.remove(blok)
sahne = bpy.context.scene


# ------------------------------------------------------------------ yardimcilar
def fcurveler(action):
    if action is None:
        return []
    if hasattr(action, "fcurves"):
        return list(action.fcurves)
    sonuc = []
    for katman in action.layers:
        for serit in katman.strips:
            for torba in serit.channelbags:
                sonuc.extend(torba.fcurves)
    return sonuc


def dongu_yap(id_blok, interpolasyon="SINE"):
    ad = getattr(id_blok, "animation_data", None)
    for fc in fcurveler(ad.action if ad else None):
        for kp in fc.keyframe_points:
            kp.interpolation = interpolasyon
        if not any(m.type == "CYCLES" for m in fc.modifiers):
            fc.modifiers.new("CYCLES")


def girdi(dugum, *adlar):
    for ad in adlar:
        if ad in dugum.inputs:
            return dugum.inputs[ad]
    return None


def nesne(ad, mesh):
    obj = bpy.data.objects.new(ad, mesh)
    sahne.collection.objects.link(obj)
    return obj


# ------------------------------------------------------------------ malzemeler
def govde_malzemesi():
    """Tek tek pullar: pul ortasi koyu, kenari parlak kobalt; hafif yanardoner."""
    m = bpy.data.materials.new("Betta govde")
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    bsdf = n["Principled BSDF"]
    renk = n.new("ShaderNodeVertexColor"); renk.layer_name = "renk"
    koord = n.new("ShaderNodeTexCoord")
    olcek = n.new("ShaderNodeMapping"); olcek.inputs["Scale"].default_value = (5.5, 7.5, 7.5)
    l.new(koord.outputs["Object"], olcek.inputs["Vector"])
    # pul kenari maskesi
    vor = n.new("ShaderNodeTexVoronoi"); vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Randomness"].default_value = 0.35
    l.new(olcek.outputs["Vector"], vor.inputs["Vector"])
    kenar = n.new("ShaderNodeMapRange")
    kenar.inputs["From Min"].default_value = 0.0
    kenar.inputs["From Max"].default_value = 0.035
    kenar.inputs["To Min"].default_value = 1.0
    kenar.inputs["To Max"].default_value = 0.0
    l.new(vor.outputs["Distance"], kenar.inputs["Value"])
    # pul basina hafif renk farki
    vor2 = n.new("ShaderNodeTexVoronoi"); vor2.inputs["Randomness"].default_value = 0.35
    l.new(olcek.outputs["Vector"], vor2.inputs["Vector"])
    fark = n.new("ShaderNodeMix"); fark.data_type = "RGBA"; fark.blend_type = "OVERLAY"
    fark.inputs[0].default_value = 0.08
    l.new(renk.outputs["Color"], fark.inputs[6])
    l.new(vor2.outputs["Color"], fark.inputs[7])
    # kenarlari parlak kobalt yap
    parlak = n.new("ShaderNodeMix"); parlak.data_type = "RGBA"; parlak.blend_type = "MIX"
    parlak.inputs[7].default_value = (0.08, 0.36, 1.0, 1)
    carp = n.new("ShaderNodeMath"); carp.operation = "MULTIPLY"; carp.inputs[1].default_value = 0.55
    l.new(kenar.outputs["Result"], carp.inputs[0])
    l.new(carp.outputs["Value"], parlak.inputs[0])
    l.new(fark.outputs[2], parlak.inputs[6])
    l.new(parlak.outputs[2], bsdf.inputs["Base Color"])
    # pul kabartmasi: ortasi hafif sisik
    kabart = n.new("ShaderNodeBump")
    kabart.inputs["Strength"].default_value = 0.15
    kabart.inputs["Distance"].default_value = 0.02
    l.new(vor.outputs["Distance"], kabart.inputs["Height"])
    l.new(kabart.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Metallic"].default_value = 0.5
    bsdf.inputs["Roughness"].default_value = 0.38
    for ad, deger in (("Coat Weight", 0.12), ("Coat Roughness", 0.3),
                      ("Thin Film Thickness", 250.0), ("Thin Film IOR", 1.33)):
        if girdi(bsdf, ad):
            girdi(bsdf, ad).default_value = deger
    return m


def yuzgec_malzemesi():
    """Ince isinli, uclari saydam ve saçakli, arkadan isik alan ipeksi yuzgec."""
    m = bpy.data.materials.new("Betta yuzgec")
    m.use_nodes = True
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    if hasattr(m, "use_backface_culling"):
        m.use_backface_culling = False
    n, l = m.node_tree.nodes, m.node_tree.links
    bsdf = n["Principled BSDF"]
    renk = n.new("ShaderNodeVertexColor"); renk.layer_name = "renk"
    uv = n.new("ShaderNodeUVMap")
    ayir = n.new("ShaderNodeSeparateXYZ")
    l.new(uv.outputs["UV"], ayir.inputs["Vector"])
    # yuzgec isinlari: 13 ana isin, uca dogru 2 -> 4 -> 8'e catallanir (gercek betta gibi)
    def mat(op, a=None, b=None, deger=None):
        d = n.new("ShaderNodeMath"); d.operation = op
        for i, g in enumerate((a, b)):
            if isinstance(g, (int, float)):
                d.inputs[i].default_value = g
            elif g is not None:
                l.new(g, d.inputs[i])
        return d.outputs["Value"]
    kirpik = n.new("ShaderNodeTexNoise"); kirpik.inputs["Scale"].default_value = 6.0
    l.new(uv.outputs["UV"], kirpik.inputs["Vector"])
    u_bozuk = mat("ADD", ayir.outputs["X"], mat("MULTIPLY", kirpik.outputs["Fac"], 0.012))
    kat = mat("POWER", 2.0, mat("FLOOR", mat("MULTIPLY", ayir.outputs["Y"], 3.2)))
    isin_sayisi = mat("MULTIPLY", kat, 13.0 * pi)
    dalga_deger = mat("ABSOLUTE", mat("SINE", mat("MULTIPLY", u_bozuk, isin_sayisi)))
    isin = n.new("ShaderNodeValToRGB")
    isin.color_ramp.elements[0].position = 0.0
    isin.color_ramp.elements[0].color = (1, 1, 1, 1)
    isin.color_ramp.elements[1].position = 0.22
    isin.color_ramp.elements[1].color = (0.62, 0.72, 0.9, 1)
    ters = n.new("ShaderNodeMath"); ters.operation = "SUBTRACT"; ters.inputs[0].default_value = 1.0
    l.new(dalga_deger, ters.inputs[1])
    l.new(ters.outputs["Value"], isin.inputs["Fac"])
    carp = n.new("ShaderNodeMix"); carp.data_type = "RGBA"; carp.blend_type = "MULTIPLY"
    carp.inputs[0].default_value = 0.8
    l.new(renk.outputs["Color"], carp.inputs[6])
    l.new(isin.outputs["Color"], carp.inputs[7])
    l.new(carp.outputs[2], bsdf.inputs["Base Color"])
    # saydamlik: dipte opak, kenara dogru ince; en uçta saçakli (yirtik) kenar
    temel = n.new("ShaderNodeMapRange")
    temel.inputs["To Min"].default_value = 0.97
    temel.inputs["To Max"].default_value = 0.45
    l.new(ayir.outputs["Y"], temel.inputs["Value"])
    sacak_gurultu = n.new("ShaderNodeTexNoise")
    sacak_gurultu.inputs["Scale"].default_value = 60.0
    sacak_gurultu.inputs["Detail"].default_value = 4.0
    sacak_olcek = n.new("ShaderNodeMapping"); sacak_olcek.inputs["Scale"].default_value = (1.0, 0.08, 1.0)
    l.new(uv.outputs["UV"], sacak_olcek.inputs["Vector"])
    l.new(sacak_olcek.outputs["Vector"], sacak_gurultu.inputs["Vector"])
    uc = n.new("ShaderNodeMapRange")          # v 0.84..1.0 arasinda 0..1
    uc.inputs["From Min"].default_value = 0.84
    uc.inputs["From Max"].default_value = 1.0
    l.new(ayir.outputs["Y"], uc.inputs["Value"])
    esik = n.new("ShaderNodeMath"); esik.operation = "GREATER_THAN"
    l.new(sacak_gurultu.outputs["Fac"], esik.inputs[0])
    l.new(uc.outputs["Result"], esik.inputs[1])
    alfa = n.new("ShaderNodeMath"); alfa.operation = "MULTIPLY"
    l.new(temel.outputs["Result"], alfa.inputs[0])
    l.new(esik.outputs["Value"], alfa.inputs[1])
    l.new(alfa.outputs["Value"], bsdf.inputs["Alpha"])
    bsdf.inputs["Roughness"].default_value = 0.30
    for ad, deger in (("Transmission Weight", 0.0), ("Subsurface Weight", 0.0),
                      ("Sheen Weight", 0.6), ("Sheen Roughness", 0.3), ("Coat Weight", 0.15)):
        if girdi(bsdf, ad):
            girdi(bsdf, ad).default_value = deger
    # arkadan isik almis gibi hafif kendi parlakligi
    if girdi(bsdf, "Emission Color"):
        l.new(carp.outputs[2], girdi(bsdf, "Emission Color"))
        girdi(bsdf, "Emission Strength").default_value = 0.06
    return m


def duz_malzeme(ad, renk, metal=0.0, puruz=0.3):
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = puruz
    return m


GOVDE = govde_malzemesi()
YUZGEC = yuzgec_malzemesi()

KOYU_MAVI = Vector((0.004, 0.025, 0.20))
PARLAK_MAVI = Vector((0.012, 0.110, 0.62))
ACIK_MAVI = Vector((0.30, 0.56, 0.98))
BEYAZ = Vector((0.80, 0.90, 1.0))


def renk_gecisi(v, koyu=0.30, acik=0.62):
    """v: 0 dip -> 1 kenar. Mavi dipten beyaz kenara."""
    if v < koyu:
        return KOYU_MAVI.lerp(PARLAK_MAVI, v / koyu)
    if v < acik:
        return PARLAK_MAVI.lerp(ACIK_MAVI, (v - koyu) / (acik - koyu))
    return ACIK_MAVI.lerp(BEYAZ, min(1, (v - acik) / (1 - acik)))


# ------------------------------------------------------------------ govde
UZUNLUK = 1.12


def _profil(t):
    """t: 0 kuyruk sapi ... 1 burun. Ust yukseklik, alt yukseklik, yari genislik, orta cizgi.

    Profil burunda sifira inmez (kesit kuresi uc kismi yuvarlatir) -> kut, organik bas.
    En kalin yer t~0.6 (gogus yuzgecinin arkasi).
    """
    t = min(1.0, max(0.0, t))
    f = sin(pi * t * 0.82) ** 0.8                        # t=1'de ~0.6: kut bas
    karin = 1 + 0.10 * sin(pi * min(1.0, max(0.0, (t - 0.30) / 0.45)))
    ust = 0.07 + 0.37 * f
    alt = (0.07 + 0.39 * f) * karin
    gen = 0.05 + 0.25 * f
    orta = 0.04 * max(0.0, (t - 0.80) / 0.20) ** 2 - 0.015 * sin(pi * t)  # agiz hafif yukari
    return ust, alt, gen, orta


def govde_olustur():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=72, ring_count=48, radius=1)
    g = bpy.context.object
    g.name = "Betta_Govde"
    g.rotation_euler = (0, pi / 2, 0)                # kutuplar x ekseninde: burun ve kuyruk sapi
    bpy.ops.object.transform_apply(rotation=True)
    me = g.data
    renkler = me.color_attributes.new("renk", "FLOAT_COLOR", "POINT")
    for v in me.vertices:
        x, y, z = v.co
        r = max(1e-6, (y * y + z * z) ** 0.5)
        cy, cz = y / r, z / r                        # kesit cemberindeki yon
        kesit = (1 - min(1.0, x * x)) ** (0.5 if x > 0 else 0.35)  # bas kubbe, kuyruk sapi silindirik
        t = (x + 1) / 2
        ust, alt, gen, orta = _profil(t)
        yuk = ust if cz > 0 else alt
        # yumusak, organik dalgalanma (simetrik plastik gorunumu kirar)
        d = 1 + 0.015 * noise.noise(Vector((x * 3, y * 3, z * 3)))
        yeni = Vector((x * UZUNLUK, cy * gen * kesit * d, cz * yuk * kesit * d + orta))
        v.co = yeni
        # renk: bas ve sirt koyu, karin/yanlar parlak mavi
        k = 0.55 + 0.45 * max(0.0, cz)
        bas = max(0.0, (x - 0.45) / 0.55)
        c = PARLAK_MAVI.lerp(KOYU_MAVI, min(1, 0.30 + 0.65 * bas + 0.25 * max(0, cz)))
        c = c * (0.85 + 0.3 * k)
        sx = x * UZUNLUK
        if 0.42 < sx + 0.08 * cz * cz < 0.48:          # solungac kapagi kenari
            c = c * 0.4
        if sx > 1.02 and -0.35 < cz < 0.05:            # agiz cizgisi
            c = c * 0.3
        renkler.data[v.index].color = (*c, 1)
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(GOVDE)
    sub = g.modifiers.new("Puruzsuz", "SUBSURF"); sub.levels = 1; sub.render_levels = 2
    # yuzme kivrimi: govdenin arka yarisi yana bukulur (S hareketi)
    g.shape_key_add(name="Basis")
    for ad, yon in (("Kivrim_Sol", 1), ("Kivrim_Sag", -1)):
        sk = g.shape_key_add(name=ad)
        for nokta in sk.data:
            x = nokta.co.x
            if x < 0.2:
                k = ((0.2 - x) / 1.32) ** 2
                nokta.co.y += yon * 0.22 * k
                nokta.co.x += -0.03 * k
    return g


# ------------------------------------------------------------------ yuzgec ureteci
def yuzgec(ad, kok, dis, nv=18, firfir=0.10, firfir_sik=11, koyu=0.30, acik=0.62, kalinlik=0.004):
    """kok: dip noktalari (govdeye bitisik), dis: kenar noktalari; ikisi de ayni sayida (XZ duzlemi).

    Yuzgec XZ duzleminde uzanir; y yonunde kenara dogru buyuyen dalga (firfir) eklenir.
    """
    nu = len(kok) - 1
    kosleler, yuzler, uvler, renkler = [], [], [], []
    for j in range(nv + 1):
        v = j / nv
        for i in range(nu + 1):
            u = i / nu
            a, b = Vector(kok[i]), Vector(dis[i])
            # kenari tirtikli/dalgali yap
            kenar = 1 + 0.035 * sin(u * pi * firfir_sik * 2.3) * v ** 3
            p = a.lerp(b, v * kenar)
            n = noise.noise(Vector((u * 6, v * 3, 0.5)))
            p.y += (firfir * v ** 1.6) * (sin(u * pi * firfir_sik) + 0.45 * n)
            kosleler.append(p)
            uvler.append((u, v))
            renkler.append(renk_gecisi(v, koyu, acik))
    for j in range(nv):
        for i in range(nu):
            s = j * (nu + 1) + i
            yuzler.append((s, s + 1, s + nu + 2, s + nu + 1))
    me = bpy.data.meshes.new(ad)
    me.from_pydata([tuple(p) for p in kosleler], [], yuzler)
    uvk = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvk.data[li].uv = uvler[me.loops[li].vertex_index]
    rk = me.color_attributes.new("renk", "FLOAT_COLOR", "POINT")
    for i, c in enumerate(renkler):
        rk.data[i].color = (*c, 1)
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(YUZGEC)
    obj = nesne(ad, me)
    obj.modifiers.new("Kalinlik", "SOLIDIFY").thickness = kalinlik
    obj.modifiers.new("Puruzsuz", "SUBSURF").levels = 1

    # yuzme dalgasi: kenara dogru artan, u boyunca ilerleyen dalga (2 sekil anahtari, ters fazli)
    obj.shape_key_add(name="Basis")
    for anahtar_adi, faz in (("Dalga_A", 0.0), ("Dalga_B", pi)):
        sk = obj.shape_key_add(name=anahtar_adi)
        for idx, nokta in enumerate(sk.data):
            j, i = divmod(idx, nu + 1)
            u, v = i / nu, j / nv
            nokta.co.y += 0.12 * v ** 1.8 * sin(u * pi * 2.2 + faz)
            nokta.co.z += 0.03 * v ** 2 * cos(u * pi * 2.2 + faz)
    return obj, nu, nv


def yay(merkez, yaricap, aci0, aci1, adet, olcek_z=1.0, dalga=0.0, dalga_sik=0):
    cx, cz = merkez
    sonuc = []
    for i in range(adet + 1):
        t = i / adet
        a = math.radians(aci0 + (aci1 - aci0) * t)
        r = yaricap * (1 + dalga * sin(t * pi * dalga_sik))
        sonuc.append((cx + r * cos(a), 0.0, cz + r * sin(a) * olcek_z))
    return sonuc


def cizgi(p0, p1, adet):
    return [tuple(Vector(p0).lerp(Vector(p1), i / adet)) for i in range(adet + 1)]


govde = govde_olustur()
A = 40  # yuzgec kenar cozunurlugu

# kuyruk: kuyruk sapindan acilan dev yarim ay (90 dereceden 270 dereceye)
kuyruk_kok = cizgi((-0.95, 0, 0.20), (-0.95, 0, -0.20), A)
kuyruk_dis = yay((-1.0, 0.0), 1.75, 92, 268, A, olcek_z=1.0, dalga=0.05, dalga_sik=9)
kuyruk, *_ = yuzgec("Kuyruk", kuyruk_kok, kuyruk_dis, firfir=0.16, firfir_sik=13, koyu=0.38, acik=0.66)

# sirt yuzgeci: sirt boyunca kok, yukari ve geriye kuyruga dogru buyuk yelpaze
sirt_kok = [(-0.05 - 1.00 * t, 0, 0.30 - 0.22 * t * t) for t in (i / A for i in range(A + 1))]
sirt_dis = [(-0.45 - 1.55 * t, 0, 1.05 + 0.55 * sin(pi * t) - 0.15 * t) for t in (i / A for i in range(A + 1))]
sirt, *_ = yuzgec("Sirt_Yuzgeci", sirt_kok, sirt_dis, firfir=0.12, firfir_sik=10, koyu=0.50, acik=0.80)

# anal yuzgec: karin boyunca uzun kok, asagi ve geriye genis perde
anal_kok = [(0.25 - 1.30 * t, 0, -0.26 + 0.16 * t * t) for t in (i / A for i in range(A + 1))]
anal_dis = [(-0.05 - 1.95 * t, 0, -1.30 - 0.45 * sin(pi * t)) for t in (i / A for i in range(A + 1))]
anal, *_ = yuzgec("Anal_Yuzgec", anal_kok, anal_dis, firfir=0.14, firfir_sik=12, koyu=0.40, acik=0.68)

# karin yuzgecleri: bas altinda iki ince, uzun, sarkik yuzgec
karinlar = []
for yan in (-1, 1):
    kk = cizgi((0.52, yan * 0.08, -0.33), (0.40, yan * 0.08, -0.33), 8)
    dd = cizgi((0.30, yan * 0.20, -1.05), (0.12, yan * 0.20, -0.95), 8)
    k, *_ = yuzgec(f"Karin_Yuzgeci_{'S' if yan < 0 else 'D'}", kk, dd, nv=10, firfir=0.03, firfir_sik=3, koyu=0.5, acik=0.85)
    karinlar.append(k)

# gogus yuzgecleri: solungac arkasinda kucuk, seffaf
for yan in (-1, 1):
    kk = cizgi((0.50, yan * 0.27, 0.02), (0.50, yan * 0.27, -0.10), 8)
    dd = yay((0.50, -0.04), 0.26, 150, 205, 8)
    dd = [(x, yan * 0.33, z) for x, _, z in dd]
    yuzgec(f"Gogus_Yuzgeci_{'S' if yan < 0 else 'D'}", kk, dd, nv=8, firfir=0.0, firfir_sik=4, koyu=0.1, acik=0.3)

gogusler = [o for o in sahne.objects if o.name.startswith("Gogus_Yuzgeci")]

# gozler: govde yuzeyine gomulu; gozbebegi, koyu mavi iris, ince altin halka, islak kornea
def goz_malzemesi():
    m = bpy.data.materials.new("Goz")
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    b = n["Principled BSDF"]
    kd = n.new("ShaderNodeTexCoord")
    ay = n.new("ShaderNodeSeparateXYZ")
    l.new(kd.outputs["Object"], ay.inputs["Vector"])
    # bakis yonu y; x-z duzleminde merkeze uzaklik
    def m_(op, a, b_=None):
        d = n.new("ShaderNodeMath"); d.operation = op
        l.new(a, d.inputs[0])
        if isinstance(b_, (int, float)):
            d.inputs[1].default_value = b_
        elif b_ is not None:
            l.new(b_, d.inputs[1])
        return d.outputs["Value"]
    uzak = m_("SQRT", m_("ADD", m_("MULTIPLY", ay.outputs["X"], ay.outputs["X"]), m_("MULTIPLY", ay.outputs["Z"], ay.outputs["Z"])))
    oran = m_("DIVIDE", uzak, GOZ_YARICAP)
    rampa = n.new("ShaderNodeValToRGB")
    e = rampa.color_ramp.elements
    e[0].position, e[0].color = 0.0, (0.0, 0.0, 0.0, 1)
    e[1].position, e[1].color = 0.42, (0.0, 0.0, 0.0, 1)
    for poz, renk in ((0.47, (0.006, 0.02, 0.07, 1)), (0.74, (0.012, 0.05, 0.16, 1)),
                      (0.78, (0.40, 0.32, 0.10, 1)), (0.81, (0.02, 0.03, 0.08, 1))):
        yeni = e.new(poz); yeni.color = renk
    l.new(oran, rampa.inputs["Fac"])
    l.new(rampa.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.5
    for ad, deger in (("Coat Weight", 0.6), ("Coat Roughness", 0.06), ("Coat IOR", 1.33)):
        if girdi(b, ad):
            girdi(b, ad).default_value = deger
    return m


GOZ_YARICAP = 0.085
GOZ_MAT = goz_malzemesi()
_ust, _alt, _gen, _orta = _profil((0.86 / UZUNLUK + 1) / 2)
for yan in (-1, 1):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=GOZ_YARICAP,
                                         location=(0.86, yan * (_gen - 0.035), 0.06 + _orta))
    goz = bpy.context.object; goz.name = f"Goz_{yan}"; goz.data.materials.append(GOZ_MAT)
    goz.scale = (1.0, 0.55, 1.0)
    for p in goz.data.polygons: p.use_smooth = True
    goz.modifiers.new("Puruzsuz", "SUBSURF").levels = 1
    # gozun etrafinda hafif koyu goz cukuru gibi gorunsun diye goz biraz one egik
    goz.rotation_euler = (0, 0, yan * -0.12)

def pivot(obj, nokta):
    """Nesnenin merkezini (donme noktasini) verilen noktaya tasir."""
    nokta = Vector(nokta)
    obj.data.transform(Matrix.Translation(-nokta))
    if obj.data.shape_keys:
        for kb in obj.data.shape_keys.key_blocks:
            for v in kb.data:
                v.co -= nokta
    obj.location = nokta


pivot(kuyruk, (-0.95, 0, 0))
pivot(sirt, (-0.30, 0, 0.30))
pivot(anal, (-0.20, 0, -0.26))
for gog in gogusler:
    pivot(gog, (0.50, 0.27 if gog.name.endswith("D") else -0.27, -0.04))

# hepsini govdeye bagla
for o in list(sahne.objects):
    if o is not govde and o.type == "MESH":
        o.parent = govde

# ------------------------------------------------------------------ animasyon
def dalga_anim(obj, kayma=0):
    sk = obj.data.shape_keys.key_blocks
    for f in range(1, KARE + 2, 4):
        t = (f - 1 + kayma) / KARE * 2 * pi
        sk["Dalga_A"].value = max(0.0, sin(t))
        sk["Dalga_B"].value = max(0.0, -sin(t))
        sk["Dalga_A"].keyframe_insert("value", frame=f)
        sk["Dalga_B"].keyframe_insert("value", frame=f)
    dongu_yap(obj.data.shape_keys, "BEZIER")


for i, o in enumerate(sahne.objects):
    if o.data and getattr(o.data, "shape_keys", None) and "Dalga_A" in o.data.shape_keys.key_blocks:
        dalga_anim(o, kayma=i * 4)

ADIM = 3


def dongu_anahtarla(f, faz):
    return sin((f - 1) / KARE * 2 * pi + faz)


govde_kb = govde.data.shape_keys.key_blocks
for f in range(1, KARE + 2, ADIM):
    s0 = dongu_anahtarla(f, 0.0)
    # govde S kivrimi
    govde_kb["Kivrim_Sol"].value = max(0.0, s0)
    govde_kb["Kivrim_Sag"].value = max(0.0, -s0)
    govde_kb["Kivrim_Sol"].keyframe_insert("value", frame=f)
    govde_kb["Kivrim_Sag"].keyframe_insert("value", frame=f)
    # kuyruk gecikmeli ve daha genis salinir (dalga kuyruga dogru akar)
    kuyruk.rotation_euler = (0.0, 0.04 * dongu_anahtarla(f, -1.6), 0.30 * dongu_anahtarla(f, -1.1))
    kuyruk.keyframe_insert("rotation_euler", frame=f)
    sirt.rotation_euler = (0.06 * dongu_anahtarla(f, -0.6), 0.0, 0.10 * dongu_anahtarla(f, -0.7))
    sirt.keyframe_insert("rotation_euler", frame=f)
    anal.rotation_euler = (-0.06 * dongu_anahtarla(f, -0.8), 0.0, 0.10 * dongu_anahtarla(f, -0.9))
    anal.keyframe_insert("rotation_euler", frame=f)
    # tum govde: hafif yon degistirme ve suzulme
    govde.rotation_euler = (0.0, 0.03 * dongu_anahtarla(f, 0.5), 0.06 * dongu_anahtarla(f, 0.6))
    govde.location = (0.0, 0.0, 0.05 * dongu_anahtarla(f, 1.2))
    govde.keyframe_insert("rotation_euler", frame=f)
    govde.keyframe_insert("location", frame=f)
    # gogus yuzgecleri: dongude 4 kez, hizli cirpma
    for gog in gogusler:
        yon = 1 if gog.name.endswith("D") else -1
        gog.rotation_euler = (0.0, 0.0, yon * 0.25 * dongu_anahtarla(f * 4, 0.0))
        gog.keyframe_insert("rotation_euler", frame=f)
for nesne_ in (govde, kuyruk, sirt, anal, *gogusler):
    dongu_yap(nesne_, "BEZIER")
dongu_yap(govde.data.shape_keys, "BEZIER")

# ------------------------------------------------------------------ sahne, isik, kamera
sahne.frame_start, sahne.frame_end = 1, KARE
sahne.render.fps = 24
motorlar = {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
sahne.render.engine = "CYCLES"
sahne.cycles.samples = 128
sahne.cycles.use_denoising = True
sahne.cycles.max_bounces = 8
sahne.cycles.transparent_max_bounces = 32
sahne.render.use_motion_blur = False
try:
    tercih = bpy.context.preferences.addons["cycles"].preferences
    tercih.compute_device_type = "METAL"
    tercih.get_devices()
    for cihaz in tercih.devices:
        cihaz.use = True
    sahne.cycles.device = "GPU"
except Exception as hata:
    print("GPU secilemedi, CPU kullaniliyor:", hata)
if hasattr(sahne, "eevee"):  # pencere onizlemesi (Material Preview) icin
    sahne.eevee.taa_samples = 32
    sahne.eevee.taa_render_samples = 128
sahne.render.resolution_x, sahne.render.resolution_y = 1480, 980
sahne.view_settings.view_transform = "AgX" if "AgX" in [v.identifier for v in type(sahne.view_settings).bl_rna.properties["view_transform"].enum_items] else "Filmic"
sahne.view_settings.look = "AgX - Medium High Contrast" if sahne.view_settings.view_transform == "AgX" else "None"

dunya = bpy.data.worlds.new("Siyah")
dunya.use_nodes = True
dunya.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
sahne.world = dunya

kamera_veri = bpy.data.cameras.new("Kamera")
kamera_veri.lens = 58
kamera = nesne("Kamera", kamera_veri)
kamera.location = (-0.55, 9.4, 0.15)
kamera.rotation_euler = (Vector((-0.55, 0, -0.10)) - kamera.location).to_track_quat("-Z", "Y").to_euler()
sahne.camera = kamera


def isik(ad, konum, guc, renk, boyut):
    veri = bpy.data.lights.new(ad, "AREA")
    veri.energy, veri.color, veri.size = guc, renk, boyut
    veri.shape = "DISK"
    o = nesne(ad, veri)
    o.location = konum
    o.rotation_euler = (Vector((-0.3, 0, 0)) - Vector(konum)).to_track_quat("-Z", "Y").to_euler()
    return o


isik("Ana_softbox", (1.5, 5.0, 3.5), 1100, (1.0, 0.98, 0.95), 4.0)
isik("Arka_kontur", (-3.5, -3.0, 2.0), 2600, (0.75, 0.88, 1.0), 3.0)
isik("Alt_dolgu", (0.5, 3.5, -3.0), 380, (0.6, 0.8, 1.0), 3.0)

sahne.frame_set(1)

# ------------------------------------------------------------------ kaydet
if not bpy.app.background:
    print("Model yeniden kuruldu (canli)")
    raise SystemExit  # pencerede: kaydetme, sadece goster
bpy.ops.wm.save_as_mainfile(filepath=CIKTI_BLEND)
try:
    bpy.ops.export_scene.gltf(filepath=CIKTI_GLB, export_format="GLB", export_animations=True,
                              export_morph=True, export_apply=True, export_cameras=False, export_lights=False)
except Exception as hata:  # glTF eklentisi kapaliysa .blend yine kaydedilir
    print("GLB disa aktarilamadi:", hata)
print("Kaydedildi:", CIKTI_BLEND)
