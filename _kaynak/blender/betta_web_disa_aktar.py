"""betta_gercekci.blend -> web icin hafif, animasyonlu GLB.

Prosedurel (dugum tabanli) desenler glTF'e gecmedigi icin her parcanin rengi
resim dokusuna pisirilir; yuzgeclerde saydamlik dokunun alfa kanalina yazilir.
Kullanim:  Blender -b betta_gercekci.blend --python betta_web_disa_aktar.py -- CIKTI.glb
"""

import sys

import bpy

CIKTI = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else bpy.path.abspath("//betta.glb")
sahne = bpy.context.scene
sahne.render.engine = "CYCLES"
sahne.cycles.samples = 16
sahne.cycles.device = "CPU"
sahne.render.bake.margin = 8


def dugumler(mat):
    return mat.node_tree.nodes, mat.node_tree.links


def bake_et(obj, tur, boyut, ad, renk_uzayi="sRGB", alfa_kanali=False):
    """Nesnenin malzemesini verilen turde bir resme pisirir."""
    img = bpy.data.images.new(ad, boyut, boyut, alpha=alfa_kanali, float_buffer=False)
    img.colorspace_settings.name = renk_uzayi
    mat = obj.active_material
    n, _ = dugumler(mat)
    hedef = n.new("ShaderNodeTexImage")
    hedef.image = img
    n.active = hedef
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if tur == "DIFFUSE":
        bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, use_clear=True)
    else:
        bpy.ops.object.bake(type=tur, use_clear=True)
    n.remove(hedef)
    return img


def alfa_pisir(obj, boyut):
    """Alpha girdisini gecici olarak isimaya baglayip EMIT ile pisirir."""
    mat = obj.active_material
    n, l = dugumler(mat)
    bsdf = n["Principled BSDF"]
    kaynak = bsdf.inputs["Alpha"].links[0].from_socket if bsdf.inputs["Alpha"].links else None
    yay = n.new("ShaderNodeEmission")
    cikis = n["Material Output"]
    eski = cikis.inputs["Surface"].links[0].from_socket
    if kaynak:
        l.new(kaynak, yay.inputs["Color"])
    else:
        yay.inputs["Color"].default_value = (1, 1, 1, 1)
    l.new(yay.outputs["Emission"], cikis.inputs["Surface"])
    eski_alfa = mat.surface_render_method if hasattr(mat, "surface_render_method") else None
    img = bake_et(obj, "EMIT", boyut, obj.name + "_alfa", "Non-Color")
    l.new(eski, cikis.inputs["Surface"])
    n.remove(yay)
    return img


def birlestir(renk, alfa, ad):
    """RGB + tek kanalli alfa -> RGBA resim."""
    w, h = renk.size
    p = list(renk.pixels)
    a = list(alfa.pixels)
    for i in range(0, len(p), 4):
        p[i + 3] = a[i]
    yeni = bpy.data.images.new(ad, w, h, alpha=True)
    yeni.pixels = p
    return yeni


def basit_malzeme(ad, renk_img, metal, puruz, normal_img=None, saydam=False):
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    n, l = dugumler(m)
    b = n["Principled BSDF"]
    t = n.new("ShaderNodeTexImage"); t.image = renk_img
    l.new(t.outputs["Color"], b.inputs["Base Color"])
    if saydam:
        l.new(t.outputs["Alpha"], b.inputs["Alpha"])
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
        m.use_backface_culling = False
    if normal_img is not None:
        nt = n.new("ShaderNodeTexImage"); nt.image = normal_img
        nm = n.new("ShaderNodeNormalMap")
        l.new(nt.outputs["Color"], nm.inputs["Color"])
        l.new(nm.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = puruz
    return m


# kalinlik ve alt bolum degistiricileri webde gereksiz (ve sekil anahtarli agda uygulanamaz)
for o in sahne.objects:
    if o.type == "MESH":
        for mod in list(o.modifiers):
            o.modifiers.remove(mod)

for o in [o for o in sahne.objects if o.type == "MESH"]:
    ad = o.name
    if ad.startswith("Betta_Govde"):
        renk = bake_et(o, "DIFFUSE", 1024, "govde_renk")
        normal = bake_et(o, "NORMAL", 1024, "govde_normal", "Non-Color")
        yeni = basit_malzeme("govde", renk, 0.45, 0.4, normal_img=normal)
    elif ad.startswith("Goz"):
        renk = bake_et(o, "DIFFUSE", 256, ad + "_renk")
        yeni = basit_malzeme("goz", renk, 0.0, 0.08)
    else:  # yuzgecler
        boyut = 1024 if ad in ("Kuyruk", "Sirt_Yuzgeci", "Anal_Yuzgec") else 256
        renk = bake_et(o, "DIFFUSE", boyut, ad + "_renk")
        alfa = alfa_pisir(o, boyut)
        rgba = birlestir(renk, alfa, ad + "_rgba")
        yeni = basit_malzeme("yuzgec_" + ad, rgba, 0.0, 0.35, saydam=True)
    o.data.materials.clear()
    o.data.materials.append(yeni)

bpy.ops.export_scene.gltf(
    filepath=CIKTI, export_format="GLB", export_animations=True, export_animation_mode="SCENE",
    export_force_sampling=True, export_morph=True, export_apply=False, export_cameras=False,
    export_lights=False, export_vertex_color="NONE", export_image_format="WEBP",
    export_frame_range=True,
)
print("GLB:", CIKTI)
