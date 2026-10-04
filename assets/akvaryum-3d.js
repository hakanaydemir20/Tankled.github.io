// Tankled 3D akvaryum sahnesi — gerçekçi render.
// Birim: 1 = 1 cm. x = uzunluk, y = yükseklik, z = derinlik (ön yüz +z).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { SimplexNoise } from 'three/addons/math/SimplexNoise.js';
import { mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';

/* ---------- Yardımcılar ---------- */

function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const lerp = (a, b, t) => a + (b - a) * t;
const between = (r, [a, b]) => lerp(a, b, r());
const hashStr = s => [...String(s)].reduce((h, c) => (Math.imul(h, 31) + c.charCodeAt(0)) >>> 0, 7);
const clamp = THREE.MathUtils.clamp;

function disposeTree(obj) {
  obj.traverse(o => {
    if (o.geometry && !o.geometry.userData.shared) o.geometry.dispose();
    if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => { if (!m.userData.shared) m.dispose(); });
  });
}

function canvasTexture(w, h, draw, { repeat = true, srgb = true } = {}) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  if (repeat) t.wrapS = t.wrapT = THREE.RepeatWrapping;
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

// Gri tonlu bir yükseklik tuvalinden normal haritası üretir (dikişsiz)
function normalFromCanvas(src, strength = 2) {
  const w = src.width, h = src.height;
  const d = src.getContext('2d').getImageData(0, 0, w, h).data;
  const H = (x, y) => d[(((y + h) % h) * w + ((x + w) % w)) * 4] / 255;
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const ctx = c.getContext('2d'), out = ctx.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = (H(x - 1, y) - H(x + 1, y)) * strength, dy = (H(x, y - 1) - H(x, y + 1)) * strength;
    const len = Math.hypot(dx, dy, 1), i = (y * w + x) * 4;
    out.data[i] = (dx / len * 0.5 + 0.5) * 255;
    out.data[i + 1] = (dy / len * 0.5 + 0.5) * 255;
    out.data[i + 2] = (1 / len * 0.5 + 0.5) * 255;
    out.data[i + 3] = 255;
  }
  ctx.putImageData(out, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

/* ---------- Su altı shader eklentileri ---------- */

// Tüm su altı malzemeleri bu ortak değerleri kullanır
const U = {
  uTime: { value: 0 },
  uWaterTop: { value: 30 },
  uFloor: { value: 0 },
  uCaustic: { value: 0.32 },
  uLightView: { value: new THREE.Vector3(0, 1, 0) },
  uSway: { value: 0.0009 },
};

const CAUSTIC_GLSL = `
float tkCaustic(vec2 p, float t) {
  vec2 i = p; float c = 1.0; float inten = 0.005;
  for (int n = 0; n < 4; n++) {
    float tt = t * (1.0 - (3.5 / float(n + 1)));
    i = p + vec2(cos(tt - i.x) + sin(tt + i.y), sin(tt - i.y) + cos(tt + i.x));
    float sx = sin(i.x + tt), cy = cos(i.y + tt);
    sx = sign(sx) * max(abs(sx), 1e-3); cy = sign(cy) * max(abs(cy), 1e-3);
    c += 1.0 / max(length(vec2(p.x / (sx / inten), p.y / (cy / inten))), 1e-3);
  }
  c /= 4.0;
  c = 1.17 - pow(max(c, 0.0), 1.4);
  return clamp(pow(abs(c), 8.0), 0.0, 1.0);
}`;

// opts: { caustics, sway, translucent, gradient: [c0, c1] }
function underwater(mat, opts = {}) {
  const { caustics = true, sway = false, translucent = false, gradient = null } = opts;
  const c0 = gradient ? new THREE.Color(gradient[0]) : null, c1 = gradient ? new THREE.Color(gradient[1]) : null;
  mat.customProgramCacheKey = () => `tk-${caustics}-${sway}-${translucent}-${!!gradient}`;
  mat.onBeforeCompile = sh => {
    Object.assign(sh.uniforms, U);
    if (gradient) { sh.uniforms.c0 = { value: c0 }; sh.uniforms.c1 = { value: c1 }; }
    const defs = `${caustics ? '#define TK_CAUSTICS\n' : ''}${sway ? '#define TK_SWAY\n' : ''}${translucent ? '#define TK_TRANSLUCENT\n' : ''}${gradient ? '#define TK_GRADIENT\n' : ''}`;
    sh.vertexShader = defs + sh.vertexShader
      .replace('#include <common>', `#include <common>
uniform float uTime; uniform float uFloor; uniform float uSway;
varying vec3 vWPos;
#ifdef TK_GRADIENT
attribute vec3 t; varying float vT;
#endif`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>
#ifdef TK_GRADIENT
vT = t.x;
#endif`)
      .replace('#include <project_vertex>', `
vec4 tkW = vec4(transformed, 1.0);
#ifdef USE_INSTANCING
tkW = instanceMatrix * tkW;
#endif
tkW = modelMatrix * tkW;
#ifdef TK_SWAY
float tkH = max(0.0, tkW.y - uFloor);
float tkS = tkH * tkH * uSway;
tkW.x += sin(uTime * 1.1 + tkW.x * 0.12 + tkW.z * 0.07) * tkS;
tkW.z += cos(uTime * 0.9 + tkW.z * 0.15 + tkW.x * 0.05) * tkS * 0.7;
#endif
vWPos = tkW.xyz;
vec4 mvPosition = viewMatrix * tkW;
gl_Position = projectionMatrix * mvPosition;`);
    sh.fragmentShader = defs + sh.fragmentShader
      .replace('#include <common>', `#include <common>
uniform float uTime; uniform float uWaterTop; uniform float uCaustic; uniform vec3 uLightView;
varying vec3 vWPos;
#ifdef TK_GRADIENT
uniform vec3 c0; uniform vec3 c1; varying float vT;
#endif
${CAUSTIC_GLSL}`)
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', `vec4 diffuseColor = vec4( diffuse, opacity );
#ifdef TK_GRADIENT
diffuseColor.rgb *= mix(c0, c1, smoothstep(0.1, 1.0, vT));
#endif`)
      .replace('#include <opaque_fragment>', `
#ifdef TK_CAUSTICS
if (vWPos.y < uWaterTop) {
  float tkC = tkCaustic(vWPos.xz * 0.13 + vec2(3.0), uTime * 0.45);
  float tkUp = clamp(dot(normal, uLightView), 0.0, 1.0);
  outgoingLight += diffuseColor.rgb * tkC * uCaustic * (0.25 + 0.75 * tkUp);
  float tkD = clamp((uWaterTop - vWPos.y) / 70.0, 0.0, 1.0);
  outgoingLight *= mix(vec3(1.0), vec3(0.82, 0.95, 0.96), tkD);
}
#endif
#ifdef TK_TRANSLUCENT
float tkB = clamp(-dot(normal, uLightView), 0.0, 1.0);
outgoingLight += diffuseColor.rgb * tkB * 0.5;
#endif
#include <opaque_fragment>`);
  };
  return mat;
}

/* ---------- Zemin görünümleri ---------- */

// mm: gerçek tane boyutu (mm), tas: üstüne serpilen taşlar [min, max] cm
const TILE_CM = 20; // doku karosunun kapladığı alan (cm); büyük tutulur ki tekrar fark edilmesin
const ZEMIN_GORUNUM = {
  aquasoil:     { base: '#2b2420', palette: ['#3a302a', '#1f1a17', '#4a3d33', '#2e2622', '#56463a'], mm: 2.6 },
  katmanli:     { base: '#c9b28a', palette: ['#d8c39c', '#b89d72', '#e3d4b3', '#a88d64', '#8d7a5c'], mm: 0.9, alt: 'aquasoil' },
  kil:          { base: '#7a3f2a', palette: ['#8c4a31', '#6b3322', '#9a5a3c', '#5e2e1f', '#a8653f'], mm: 3 },
  'dere-kumu':  { base: '#c9b28a', palette: ['#d8c39c', '#b89d72', '#e3d4b3', '#a88d64', '#8d7a5c'], mm: 0.9 },
  silis:        { base: '#e9e4d8', palette: ['#f4f1ea', '#dcd6c8', '#ffffff', '#cfc8b8', '#e2dccd'], mm: 0.7 },
  bazalt:       { base: '#262626', palette: ['#1b1b1b', '#333333', '#2a2a2a', '#444444', '#3a3a3a'], mm: 0.8 },
  'renkli-kum': { base: '#d9c8a8', palette: ['#e05a5a', '#4f86d9', '#f2c14e', '#5bbf6a', '#b86bd6', '#f28ec0', '#ffffff'], mm: 1.3 },
  mercan:       { base: '#efe9df', palette: ['#f7f3ec', '#e8dfd0', '#ffffff', '#e3d5c2', '#f0c9b5'], mm: 1.6 },
  cakil:        { base: '#8f887c', palette: ['#a39b8e', '#7c756a', '#b8b0a2', '#6b655c', '#9c8a74'], mm: 3.5, tas: [0.7, 1.5],
                  tasRenk: ['#a39b8e', '#7c756a', '#b8b0a2', '#6b655c', '#9c8a74', '#c2b7a3'] },
  lav:          { base: '#4a2620', palette: ['#5e2e24', '#3b2420', '#6f3a2c', '#2a1a17', '#7a4030'], mm: 4, tas: [0.8, 1.9],
                  tasRenk: ['#6b3326', '#3b2420', '#7a3b2c', '#4f2a22', '#2e1d19'] },
  ponza:        { base: '#d3ccbd', palette: ['#dcd6c9', '#c8c0af', '#e6e1d6', '#bdb4a2', '#d9d2c2'], mm: 3.5, tas: [0.6, 1.4],
                  tasRenk: ['#dcd6c9', '#c8c0af', '#e6e1d6', '#bdb4a2', '#cfc6b3'] },
  yok:          null,
};

const grainCache = new Map();
// Zemin dokusu: renk haritası + aynı tanelerden üretilen yumuşak normal haritası (dikişsiz, TILE_CM kaplar)
function grainTextures(key) {
  if (grainCache.has(key)) return grainCache.get(key);
  const g = ZEMIN_GORUNUM[key];
  const size = 1024, pxPerCm = size / TILE_CM;
  const color = document.createElement('canvas'), height = document.createElement('canvas');
  color.width = color.height = height.width = height.height = size;
  const cx = color.getContext('2d'), hx = height.getContext('2d');
  cx.fillStyle = g.base; cx.fillRect(0, 0, size, size);
  hx.fillStyle = '#404040'; hx.fillRect(0, 0, size, size);
  const r = rng(hashStr(key));
  const wrap = (x, y, rad, fn) => {
    for (const dx of [0, size, -size]) for (const dy of [0, size, -size]) {
      if (x + dx + rad < 0 || x + dx - rad > size || y + dy + rad < 0 || y + dy - rad > size) continue;
      fn(x + dx, y + dy);
    }
  };
  // Taneler: gerçek boyutuna göre
  const rad0 = Math.max(1.1, (g.mm / 10) * pxPerCm / 2);
  const n = Math.min(90000, Math.round((size * size) / (rad0 * rad0 * 2.6)));
  for (let i = 0; i < n; i++) {
    const x = r() * size, y = r() * size, rad = rad0 * (0.6 + r() * 0.8), ang = r() * Math.PI, sq = 0.7 + r() * 0.3;
    const col = g.palette[Math.floor(r() * g.palette.length)];
    wrap(x, y, rad, (px, py) => {
      cx.fillStyle = col;
      cx.beginPath(); cx.ellipse(px, py, rad, rad * sq, ang, 0, Math.PI * 2); cx.fill();
      hx.fillStyle = `rgb(${150 + (r() * 60) | 0},${150 + (r() * 60) | 0},${150 + (r() * 60) | 0})`;
      hx.beginPath(); hx.ellipse(px, py, rad * 0.9, rad * sq * 0.9, ang, 0, Math.PI * 2); hx.fill();
    });
  }
  // Ton lekeleri: ıslak/kuru, koyu/açık bölgeler (tekrarı gizler)
  for (let i = 0; i < 26; i++) {
    const x = r() * size, y = r() * size, rad = size * (0.08 + r() * 0.18), dark = r() > 0.5;
    wrap(x, y, rad, (px, py) => {
      const gr = cx.createRadialGradient(px, py, 0, px, py, rad);
      gr.addColorStop(0, dark ? 'rgba(20,15,10,.06)' : 'rgba(255,250,240,.05)');
      gr.addColorStop(1, 'rgba(0,0,0,0)');
      cx.fillStyle = gr; cx.fillRect(px - rad, py - rad, rad * 2, rad * 2);
    });
  }
  // Yükseklik haritasını yumuşat → normal haritası titreşmesin
  const soft = document.createElement('canvas');
  soft.width = soft.height = size;
  const sx = soft.getContext('2d');
  sx.filter = 'blur(1.2px)';
  sx.drawImage(height, 0, 0);
  const map = new THREE.CanvasTexture(color);
  map.wrapS = map.wrapT = THREE.RepeatWrapping;
  map.colorSpace = THREE.SRGBColorSpace;
  map.anisotropy = 8;
  const normal = normalFromCanvas(soft, 1.6);
  normal.anisotropy = 8;
  const res = { map, normal };
  grainCache.set(key, res);
  return res;
}

/* ---------- Taş ve kökler ---------- */

// Akvaryumcularda satılan taş ve kök türleri. "not": suya etkisi (satıcı ve hobi bilgisine göre genel davranış)
export const HARDSCAPE = [
  { id: 'seiryu', tur: 'tas', ad: 'Seiryu taşı', renk: '#7b8388',
    aciklama: 'Mavi-gri, keskin hatlı ve beyaz damarlı. Iwagumi düzenlerinin klasiği.', not: 'Suyu hafifçe sertleştirir; pH ve KH biraz yükselir.' },
  { id: 'ejderha', tur: 'tas', ad: 'Ejderha taşı (Ohko)', renk: '#a8825a',
    aciklama: 'Kil renginde, bol gözenekli ve oyuklu doğal kaya.', not: 'Suyu etkilemez.' },
  { id: 'lav-tasi', tur: 'tas', ad: 'Lav taşı', renk: '#4a2a24',
    aciklama: 'Koyu kızıl-siyah, hafif ve gözenekli; yosun ve bitki tutturmak için ideal.', not: 'Suyu etkilemez.' },
  { id: 'nehir-tasi', tur: 'tas', ad: 'Dere / nehir taşı', renk: '#9c9486',
    aciklama: 'Suyla yuvarlanmış pürüzsüz doğal taşlar; bir adet 3–5 taşlık küme.', not: 'Genelde suyu etkilemez; kireçli olanlar sertleştirebilir.' },
  { id: 'kayrak', tur: 'tas', ad: 'Kayrak (arduvaz) taşı', renk: '#4c5156',
    aciklama: 'İnce katmanlı, yassı koyu gri taş; teras ve basamak düzenleri için.', not: 'Suyu etkilemez.' },
  { id: 'pagoda', tur: 'tas', ad: 'Pagoda taşı', renk: '#7d7466',
    aciklama: 'Yatay katmanlı, çizgili gri-kahve taş; dağ silueti düzenleri için.', not: 'Suyu etkilemez.' },
  { id: 'taslasmis-agac', tur: 'tas', ad: 'Taşlaşmış ağaç', renk: '#8a5a3a',
    aciklama: 'Ağaç dokusunu koruyan taşlaşmış odun; sıcak kahve-turuncu tonlar.', not: 'Genelde suyu etkilemez.' },
  { id: 'orumcek-koku', tur: 'odun', ad: 'Örümcek kökü (Spider wood)', renk: '#a8825c',
    aciklama: 'İnce, çok dallı açık kahve kök; ağaç ve orman düzenleri için.', not: 'İlk haftalarda yüzebilir, suyu hafif renklendirebilir; önceden suda bekletin.' },
  { id: 'red-moor', tur: 'odun', ad: 'Red moor kökü', renk: '#6a3a2a',
    aciklama: 'Kızıl-kahve, ince ve yoğun dallı kök; çalı ve ağaç görünümü verir.', not: 'Tanen salar; suyu çay rengine çevirebilir, pH biraz düşer.' },
  { id: 'malezya', tur: 'odun', ad: 'Malezya kütüğü', renk: '#4a3324',
    aciklama: 'Koyu kahve, ağır ve kalın gövdeli kütük; hemen batar.', not: 'Tanen salar; suyu çay rengine çevirebilir, pH biraz düşer.' },
  { id: 'mangrov', tur: 'odun', ad: 'Mangrov kökü', renk: '#3f2c20',
    aciklama: 'Kıvrımlı, çok köklü koyu kahve kök; doğal bataklık görünümü.', not: 'Tanen salar; önceden suda bekletin.' },
  { id: 'talawa', tur: 'odun', ad: 'Talawa kökü', renk: '#2f2520',
    aciklama: 'Çok koyu, sert, ağır ve kıvrımlı kök; uzun ömürlü.', not: 'Az tanen salar; hemen batar.' },
  { id: 'manzanita', tur: 'odun', ad: 'Manzanita dalı', renk: '#7a4533',
    aciklama: 'Kızıl kabuklu, pürüzsüz ve ağaç gibi dallanan dal.', not: 'İlk haftalarda yüzebilir; tanen salımı azdır.' },
];

const simplex = new SimplexNoise({ random: rng(4242) });
const fbm = (x, y, z, oct = 4) => {
  let s = 0, a = 0.5, f = 1;
  for (let i = 0; i < oct; i++) { s += a * simplex.noise3d(x * f, y * f, z * f); a *= 0.5; f *= 2.03; }
  return s;
};

// Taş görünüm ayarları: şekil (amp, freq, ridged, scale) ve renk fonksiyonu (p = birim küre noktası)
const TAS_STIL = {
  'seiryu': { amp: 0.34, freq: 1.5, ridged: true, scale: [1.05, 0.95, 0.85],
    color: (p, n, c) => { const v = Math.abs(simplex.noise3d(p.x * 3.2, p.y * 3.2 + 7, p.z * 3.2)); return v < 0.045 ? c.set('#d9dedc') : c.set('#6d767b').offsetHSL(0, 0, n * 0.12); } },
  'ejderha': { amp: 0.26, freq: 1.8, ridged: true, pits: true, scale: [1.2, 0.8, 1.0],
    color: (p, n, c) => simplex.noise3d(p.x * 6, p.y * 6, p.z * 6) > 0.5 ? c.set('#4a3524') : c.set('#a37d55').offsetHSL(0, 0, n * 0.15) },
  'lav-tasi': { amp: 0.2, freq: 2.6, ridged: false, pits: true, scale: [1.1, 0.8, 1.0],
    color: (p, n, c) => c.set(simplex.noise3d(p.x * 14, p.y * 14, p.z * 14) > 0.2 ? '#2d1c19' : '#6b3226').offsetHSL(0, 0, n * 0.08) },
  'nehir-tasi': { amp: 0.05, freq: 1.0, ridged: false, scale: [1.2, 0.6, 0.9], smooth: true,
    color: (p, n, c, hue) => c.set(hue).offsetHSL(0, 0, n * 0.1 + simplex.noise3d(p.x * 5, p.y * 5, p.z * 5) * 0.03) },
  'kayrak': { amp: 0.08, freq: 1.3, ridged: false, scale: [1.35, 0.22, 0.95],
    color: (p, n, c) => c.set('#4c5156').offsetHSL(0, 0, Math.sin(p.y * 40 + n * 4) * 0.03 + n * 0.05) },
  'pagoda': { amp: 0.2, freq: 1.4, ridged: true, scale: [1.0, 1.15, 0.8],
    color: (p, n, c) => c.set(Math.sin(p.y * 22 + n * 3) > 0.2 ? '#8a8072' : '#5a5247').offsetHSL(0, 0, n * 0.06) },
  'taslasmis-agac': { amp: 0.1, freq: 1.2, ridged: false, scale: [1.7, 0.6, 0.6],
    color: (p, n, c) => { const b = Math.sin(p.z * 18 + p.y * 10 + n * 5); return c.set(b > 0.5 ? '#b0723e' : b > -0.3 ? '#8a5a3a' : '#6e6258').offsetHSL(0, 0, n * 0.05); } },
};
const NEHIR_RENK = ['#9c9486', '#8a8378', '#b3a894', '#7b766f', '#a39580'];

const rockMats = new Map();
function rockMaterial() {
  if (!rockMats.has('rock')) {
    const m = underwater(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.92, metalness: 0 }), { caustics: true });
    m.userData.shared = true;
    rockMats.set('rock', m);
  }
  return rockMats.get('rock');
}

// Tek bir taş: gürültüyle şekillenmiş küre, alt kısmı zemine gömülecek şekilde düzleştirilmiş
function buildRock(stil, size, r, hue) {
  const st = TAS_STIL[stil];
  let geo = new THREE.IcosahedronGeometry(1, st.smooth ? 4 : 5);
  geo.deleteAttribute('normal'); geo.deleteAttribute('uv');
  geo = mergeVertices(geo); // yüzeyler pürüzsüz gölgelensin (köşeli görünmesin)
  const pos = geo.attributes.position, colors = new Float32Array(pos.count * 3);
  const seed = r() * 100, p = new THREE.Vector3(), c = new THREE.Color();
  for (let i = 0; i < pos.count; i++) {
    p.fromBufferAttribute(pos, i).normalize();
    let n = fbm(p.x * st.freq + seed, p.y * st.freq, p.z * st.freq);
    if (st.ridged) n = 0.5 - Math.abs(n);
    let rad = 1 + n * st.amp * 2;
    if (st.pits && simplex.noise3d(p.x * 7 + seed, p.y * 7, p.z * 7) > 0.55) rad -= 0.06;
    let y = p.y * rad * st.scale[1];
    if (y < -0.3 * st.scale[1]) y = -0.3 * st.scale[1] + (y + 0.3 * st.scale[1]) * 0.1;
    pos.setXYZ(i, p.x * rad * st.scale[0], y, p.z * rad * st.scale[2]);
    st.color(p, n, c, hue);
    colors[i * 3] = c.r; colors[i * 3 + 1] = c.g; colors[i * 3 + 2] = c.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, rockMaterial());
  m.scale.setScalar(size);
  m.castShadow = m.receiveShadow = true;
  return m;
}

/* Kökler: sivrilen eğri borulardan dallar */
const barkTex = () => canvasTexture(64, 256, (x, w, h) => {
  x.fillStyle = '#b8b8b8'; x.fillRect(0, 0, w, h);
  const r = rng(77);
  for (let i = 0; i < 90; i++) {
    x.strokeStyle = r() > 0.5 ? 'rgba(255,255,255,.35)' : 'rgba(0,0,0,.35)';
    x.lineWidth = 0.5 + r() * 2;
    const px = r() * w;
    x.beginPath(); x.moveTo(px, 0);
    for (let y = 0; y <= h; y += 16) x.lineTo(px + Math.sin(y * 0.05 + i) * 3, y);
    x.stroke();
  }
});
let barkCache = null;

function taperedTube(curve, r0, r1, radial = 8, tubular = 24) {
  const geo = new THREE.TubeGeometry(curve, tubular, 1, radial, false);
  const pos = geo.attributes.position, p = new THREE.Vector3(), v = new THREE.Vector3();
  for (let i = 0; i <= tubular; i++) {
    const t = i / tubular, c = curve.getPointAt(t), rad = lerp(r0, r1, Math.pow(t, 0.8));
    for (let j = 0; j <= radial; j++) {
      const k = i * (radial + 1) + j;
      v.fromBufferAttribute(pos, k).sub(c).multiplyScalar(rad * (0.9 + 0.2 * Math.sin(j * 1.7 + i)));
      p.copy(c).add(v);
      pos.setXYZ(k, p.x, p.y, p.z);
    }
  }
  geo.computeVertexNormals();
  // uç kapağı yerine ucu sivri bırakıyoruz; tabandaki açıklık zemine gömülür
  return geo;
}

// Doğal bir dal eğrisi: yön boyunca rastgele sapmalarla
function branchCurve(r, start, dir, len, jitter) {
  const pts = [start.clone()];
  const d = dir.clone().normalize(), p = start.clone();
  for (let i = 1; i <= 4; i++) {
    d.add(new THREE.Vector3((r() - 0.5) * jitter, (r() - 0.5) * jitter * 0.6, (r() - 0.5) * jitter)).normalize();
    p.addScaledVector(d, len / 4);
    pts.push(p.clone());
  }
  return new THREE.CatmullRomCurve3(pts);
}

const ODUN_STIL = {
  'orumcek-koku': { kol: [7, 12], egim: [20, 70], boy: [0.55, 1.0], r0: 0.75, r1: 0.12, alt: 2, jitter: 0.9 },
  'red-moor': { kol: [10, 16], egim: [15, 75], boy: [0.45, 0.95], r0: 0.5, r1: 0.08, alt: 3, jitter: 1.0 },
  'malezya': { yatay: true, kol: [1, 1], boy: [0.55, 0.7], r0: 2.4, r1: 1.2, alt: 1, altKisa: true, jitter: 0.5 },
  'mangrov': { yatay: true, kol: [1, 1], boy: [0.6, 0.75], r0: 1.5, r1: 0.5, kok: [6, 9], alt: 1, jitter: 0.6 },
  'talawa': { kol: [2, 3], egim: [35, 65], boy: [0.6, 0.9], r0: 1.5, r1: 0.35, alt: 1, jitter: 1.3 },
  'manzanita': { agac: true, kol: [1, 1], boy: [0.4, 0.45], r0: 1.1, r1: 0.6, alt: 3, jitter: 0.5 },
};

function buildWood(stil, I, r, color) {
  const st = ODUN_STIL[stil];
  const H = Math.min((I.waterTop - I.y0) * 0.78, 38);
  const g = new THREE.Group();
  if (!barkCache) { barkCache = barkTex(); barkCache.colorSpace = THREE.SRGBColorSpace; }
  const mat = underwater(new THREE.MeshStandardMaterial({ color, map: barkCache, roughness: 0.95, bumpMap: barkCache, bumpScale: 1.5 }), { caustics: true });
  const tips = [];
  const add = (curve, r0, r1) => {
    const m = new THREE.Mesh(taperedTube(curve, r0, r1), mat);
    m.castShadow = m.receiveShadow = true;
    g.add(m);
  };
  const grow = (start, dir, len, r0, r1, depth) => {
    const curve = branchCurve(r, start, dir, len, st.jitter);
    add(curve, r0, r1);
    const end = curve.getPointAt(1);
    tips.push(end);
    if (depth <= 0) return;
    const kids = st.altKisa ? 2 : 1 + Math.floor(r() * 2);
    for (let k = 0; k < kids; k++) {
      const t = 0.45 + r() * 0.45, from = curve.getPointAt(t), tan = curve.getTangentAt(t);
      const side = new THREE.Vector3(r() - 0.5, 0.4 + r() * 0.5, r() - 0.5).normalize();
      const nd = tan.clone().lerp(side, 0.6).normalize();
      grow(from, nd, len * (st.altKisa ? 0.25 : 0.55 + r() * 0.2), lerp(r0, r1, t) * 0.7, r1 * 0.6, depth - 1);
    }
  };

  if (st.yatay) {
    const span = Math.min(I.L * 0.5, 45);
    const a = r() * Math.PI;
    const dir = new THREE.Vector3(Math.cos(a), 0.18, Math.sin(a) * 0.4);
    const start = dir.clone().multiplyScalar(-span / 2).setY(st.r0 * 0.5);
    const curve = branchCurve(r, start, dir, span, st.jitter);
    add(curve, st.r0, st.r1);
    for (let k = 0; k < (st.kok ? between(r, st.kok) : 3); k++) {
      const t = 0.1 + r() * 0.8, from = curve.getPointAt(t);
      const d = st.kok ? new THREE.Vector3(r() - 0.5, -0.6, r() - 0.5) : new THREE.Vector3(r() - 0.5, 0.8, r() - 0.5);
      if (st.kok) {
        const c = branchCurve(r, from, d, 6 + r() * 8, 0.7);
        add(c, st.r1 * 0.9, 0.1);
      } else {
        grow(from, d, H * between(r, [0.2, 0.35]), st.r1 * 0.9, 0.3, st.alt - 1);
      }
    }
    if (st.kok) for (let k = 0; k < 3; k++) {
      const t = 0.3 + r() * 0.5;
      grow(curve.getPointAt(t), new THREE.Vector3(r() - 0.5, 1, r() - 0.5), H * 0.35, st.r1 * 0.8, 0.12, 1);
    }
  } else if (st.agac) {
    const trunk = branchCurve(r, new THREE.Vector3(0, -0.5, 0), new THREE.Vector3(0.15, 1, 0.05), H * 0.42, 0.25);
    add(trunk, st.r0, st.r1);
    const top = trunk.getPointAt(1);
    for (let k = 0; k < 3 + Math.floor(r() * 2); k++) {
      const a = (k / 4) * Math.PI * 2 + r();
      grow(top, new THREE.Vector3(Math.cos(a), 1.1, Math.sin(a) * 0.6), H * 0.4, st.r1, 0.12, st.alt - 1);
    }
  } else {
    const n = Math.round(between(r, st.kol));
    for (let k = 0; k < n; k++) {
      const a = r() * Math.PI * 2, tilt = THREE.MathUtils.degToRad(between(r, st.egim));
      const dir = new THREE.Vector3(Math.sin(tilt) * Math.cos(a), Math.cos(tilt), Math.sin(tilt) * Math.sin(a) * 0.6);
      grow(new THREE.Vector3((r() - 0.5) * 3, -0.3, (r() - 0.5) * 2), dir, H * between(r, st.boy), st.r0, st.r1, st.alt - 1);
    }
  }
  // Akvaryumun iç sınırlarına sığdır
  const box = new THREE.Box3().setFromObject(g);
  const size = box.getSize(new THREE.Vector3());
  const fit = Math.min(1, (I.L - 4) / size.x, (I.W - 4) / size.z, (I.waterTop - I.y0 - 2) / Math.max(1, size.y));
  g.scale.setScalar(fit);
  g.userData.tips = tips.map(t => t.multiplyScalar(fit));
  g.userData.radius = Math.max(size.x, size.z) * fit / 2;
  return g;
}

/* ---------- Bitki modelleri ---------- */

// tip: rozet | serit | govde | hali | yosun | yuzen | top
// taban: 'tas' | 'kutuk' → epifit bitkiler taş ya da kütük üzerinde; akvaryumda taş/kök varsa onların üzerine tutturulur
const BITKI_3D = {
  'anubias-nana':        { tip: 'rozet', adet: 9, boy: [4, 7], en: 0.55, egim: [35, 70], renk: '#2f5a2c', uc: '#3f7036', taban: 'tas' },
  'anubias-barteri':     { tip: 'rozet', adet: 9, boy: [10, 16], en: 0.5, egim: [25, 60], renk: '#2f5a2c', uc: '#3f7036', taban: 'tas' },
  'anubias-coffeefolia': { tip: 'rozet', adet: 9, boy: [8, 12], en: 0.5, egim: [30, 60], renk: '#34552c', uc: '#7a4a2b', taban: 'tas' },
  'java-egreltisi':      { tip: 'rozet', adet: 11, boy: [12, 20], en: 0.17, egim: [10, 40], renk: '#3a6630', uc: '#5b8a3f', taban: 'kutuk' },
  'bolbitis':            { tip: 'rozet', adet: 10, boy: [10, 16], en: 0.32, egim: [20, 55], renk: '#23462a', uc: '#2f5a33', taban: 'kutuk' },
  'java-yosunu':         { tip: 'yosun', boy: [3, 5], renk: '#3e6b2e', uc: '#5a8a3a', taban: 'kutuk' },
  'christmas-yosunu':    { tip: 'yosun', boy: [3, 5], renk: '#355f2a', uc: '#4f8036', taban: 'kutuk' },
  'cryptocoryne-wendtii':{ tip: 'rozet', adet: 12, boy: [7, 11], en: 0.3, egim: [20, 55], renk: '#55572c', uc: '#7a4a2a', dalga: true },
  'bucephalandra':       { tip: 'rozet', adet: 10, boy: [3, 5], en: 0.4, egim: [30, 65], renk: '#34493a', uc: '#6b3f52', taban: 'tas' },
  'amazon-kilicotu':     { tip: 'rozet', adet: 14, boy: [20, 34], en: 0.22, egim: [15, 50], renk: '#3f7a36', uc: '#5a9446' },
  'vallisneria':         { tip: 'serit', adet: 12, boy: [30, 55], en: 1.0, renk: '#4f8a3a', uc: '#76a84e' },
  'aponogeton':          { tip: 'serit', adet: 9, boy: [25, 42], en: 1.6, dalga: true, renk: '#4f873a', uc: '#79a652' },
  'limnophila-sessiliflora': { tip: 'govde', sap: 6, boy: [28, 40], ara: 1.1, yaprak: 8, yBoy: 2.2, yEn: 0.09, renk: '#6fa243', uc: '#8cc04f' },
  'hygrophila-polysperma':   { tip: 'govde', sap: 5, boy: [25, 35], ara: 1.4, yaprak: 2, yBoy: 2.6, yEn: 0.42, renk: '#5f8f3d', uc: '#8aa84a' },
  'hygrophila-difformis':    { tip: 'govde', sap: 5, boy: [20, 30], ara: 1.6, yaprak: 2, yBoy: 3.2, yEn: 0.55, renk: '#6c9d44', uc: '#86b451' },
  'egeria-densa':            { tip: 'govde', sap: 6, boy: [30, 50], ara: 0.7, yaprak: 4, yBoy: 1.8, yEn: 0.2, renk: '#447d36', uc: '#5f9c43' },
  'hornwort':                { tip: 'govde', sap: 5, boy: [30, 50], ara: 1.0, yaprak: 8, yBoy: 2.0, yEn: 0.06, renk: '#355f2c', uc: '#4c7c37' },
  'salvinia':            { tip: 'yuzen', yaprak: 22, yBoy: 0.9, yuvarlak: 0.75, renk: '#6f9c3f', uc: '#86b24c' },
  'limnobium':           { tip: 'yuzen', yaprak: 10, yBoy: 1.6, yuvarlak: 1, kok: true, renk: '#4f8a3a', uc: '#5f9c43' },
  'marimo':              { tip: 'top', boy: [2, 3], renk: '#3a7430' },
  'monte-carlo':         { tip: 'hali', yBoy: 0.4, yuvarlak: 1, yukseklik: 1.6, renk: '#5fb043', uc: '#76c754' },
  'hc-cuba':             { tip: 'hali', yBoy: 0.25, yuvarlak: 0.9, yukseklik: 1.2, renk: '#6cc24b', uc: '#86d85f' },
  'glossostigma':        { tip: 'hali', yBoy: 0.45, yuvarlak: 0.6, yukseklik: 2, renk: '#5aab42', uc: '#72c252' },
  'utricularia-graminifolia': { tip: 'hali', yBoy: 1.2, yuvarlak: 0.12, yukseklik: 2.2, renk: '#6cbf4a', uc: '#8bd765' },
  'riccia':              { tip: 'yosun', boy: [2, 3.5], renk: '#7ec84c', uc: '#9ade64', taban: 'tas' },
  'cuce-saz':            { tip: 'serit', adet: 45, boy: [3, 6], en: 0.12, yayilim: 2.2, renk: '#5aa33e', uc: '#86c45a' },
  'staurogyne-repens':   { tip: 'govde', sap: 7, boy: [4, 6], ara: 0.6, yaprak: 2, yBoy: 1.5, yEn: 0.4, yayilim: 2.5, renk: '#4f9a3a', uc: '#6db64b' },
  'pogostemon-helferi':  { tip: 'rozet', adet: 16, boy: [3, 5], en: 0.2, egim: [55, 85], renk: '#5d8f36', uc: '#79aa45', dalga: true },
  'hydrocotyle-tripartita': { tip: 'hali', yBoy: 0.55, yuvarlak: 1, yukseklik: 3, renk: '#5fae40', uc: '#7ac650' },
  'hemianthus-micranthemoides': { tip: 'govde', sap: 8, boy: [15, 25], ara: 0.6, yaprak: 3, yBoy: 0.7, yEn: 0.45, renk: '#6cb143', uc: '#8ccc58' },
  'rotala-rotundifolia': { tip: 'govde', sap: 7, boy: [22, 32], ara: 0.9, yaprak: 2, yBoy: 1.3, yEn: 0.35, renk: '#6f9d45', uc: '#d9707a' },
  'rotala-hra':          { tip: 'govde', sap: 7, boy: [22, 32], ara: 0.9, yaprak: 2, yBoy: 1.3, yEn: 0.35, renk: '#b86a3a', uc: '#e0553b' },
  'rotala-wallichii':    { tip: 'govde', sap: 7, boy: [22, 32], ara: 0.8, yaprak: 8, yBoy: 1.3, yEn: 0.06, renk: '#a0606b', uc: '#e46a8a' },
  'ludwigia-repens':     { tip: 'govde', sap: 5, boy: [22, 32], ara: 1.4, yaprak: 2, yBoy: 2.2, yEn: 0.55, renk: '#7d3b32', uc: '#b0463b' },
  'ludwigia-palustris':  { tip: 'govde', sap: 5, boy: [22, 32], ara: 1.4, yaprak: 2, yBoy: 2.0, yEn: 0.5, renk: '#6e7a3a', uc: '#b04a3b' },
  'alternanthera-mini':  { tip: 'govde', sap: 6, boy: [6, 10], ara: 0.7, yaprak: 2, yBoy: 1.5, yEn: 0.4, renk: '#6f2233', uc: '#9b2e45' },
  'bacopa-caroliniana':  { tip: 'govde', sap: 5, boy: [22, 32], ara: 1.3, yaprak: 2, yBoy: 2.0, yEn: 0.5, renk: '#6f9a4a', uc: '#b07a4a' },
  'cabomba':             { tip: 'govde', sap: 6, boy: [28, 40], ara: 1.1, yaprak: 10, yBoy: 2.0, yEn: 0.05, renk: '#72a646', uc: '#8cc056' },
};

// Yerleşim bilgisinden (ör. "Orta / arka") akvaryumdaki derinlik aralığını çıkarır: 0 = ön cam, 1 = arka cam
function zone(yerlesim) {
  const s = yerlesim.toLocaleLowerCase('tr');
  if (s.startsWith('yüzer')) return { yuzen: true };
  if (s.includes('halı')) return { z: [0.05, 0.35] };
  const bands = { 'ön': [0.05, 0.35], 'orta': [0.35, 0.65], 'arka': [0.65, 0.95], 'kütük': [0.3, 0.7] };
  const parts = s.split('/').map(x => x.trim().split(' ')[0]).filter(x => bands[x]);
  if (!parts.length) return { z: [0.2, 0.8] };
  return { z: [Math.min(...parts.map(p => bands[p][0])), Math.max(...parts.map(p => bands[p][1]))] };
}

// Yaprak damar dokusu (gri tonlu; bitki rengiyle çarpılır)
let leafTex = null;
function leafTexture() {
  if (leafTex) return leafTex;
  leafTex = canvasTexture(128, 256, (x, w, h) => {
    const g = x.createLinearGradient(0, 0, w, 0);
    g.addColorStop(0, '#9c9c9c'); g.addColorStop(0.2, '#dcdcdc'); g.addColorStop(0.5, '#f2f2f2'); g.addColorStop(0.8, '#dcdcdc'); g.addColorStop(1, '#9c9c9c');
    x.fillStyle = g; x.fillRect(0, 0, w, h);
    x.strokeStyle = 'rgba(255,255,255,.95)'; x.lineWidth = 3;
    x.beginPath(); x.moveTo(w / 2, h); x.lineTo(w / 2, 0); x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.55)'; x.lineWidth = 1.3;
    for (let y = h - 14; y > 10; y -= 17) {
      for (const s of [-1, 1]) {
        x.beginPath(); x.moveTo(w / 2, y);
        x.quadraticCurveTo(w / 2 + s * w * 0.25, y - 10, w / 2 + s * w * 0.48, y - 30); x.stroke();
      }
    }
    const r = rng(9);
    for (let i = 0; i < 700; i++) { x.fillStyle = `rgba(${r() > 0.5 ? '255,255,255' : '0,0,0'},.06)`; x.fillRect(r() * w, r() * h, 2, 2); }
  }, { repeat: false });
  return leafTex;
}

// Yaprak geometrisi: taban (0,0,0), uç +y yönünde; kıvrım +z yönüne
const leafCache = new Map();
function leafGeometry(width, curl = 0.25, wave = false) {
  const key = `${width.toFixed(3)}|${curl}|${wave}`;
  if (leafCache.has(key)) return leafCache.get(key);
  const w = width / 2;
  const shape = new THREE.Shape();
  shape.moveTo(0, 0);
  shape.bezierCurveTo(w * 1.2, 0.25, w * 1.1, 0.75, 0, 1);
  shape.bezierCurveTo(-w * 1.1, 0.75, -w * 1.2, 0.25, 0, 0);
  const geo = new THREE.ShapeGeometry(shape, 10);
  const pos = geo.attributes.position, uv = geo.attributes.uv;
  const t = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i), x = pos.getX(i);
    // kıvrım + orta damar boyunca hafif V + kenar dalgası
    pos.setZ(i, curl * y * y + Math.abs(x) * 0.25 + (wave ? Math.sin(y * 22 + x * 3) * 0.035 * Math.abs(x / (w || 1)) : 0));
    uv.setXY(i, x / (width || 1) + 0.5, y);
    t[i * 3] = t[i * 3 + 1] = t[i * 3 + 2] = y;
  }
  geo.setAttribute('t', new THREE.BufferAttribute(t, 3));
  geo.computeVertexNormals();
  geo.userData.shared = true;
  leafCache.set(key, geo);
  return geo;
}

function leafMaterial(base, tip, { sway = true, textured = true } = {}) {
  const m = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: 0.5, metalness: 0, map: textured ? leafTexture() : null });
  return underwater(m, { caustics: true, sway, translucent: true, gradient: [base, tip] });
}

// Aynı geometriyi çok sayıda kopyalamak için InstancedMesh üretir
function instanced(geo, mat, mats, colorJitter = 0.12, r = Math.random) {
  const mesh = new THREE.InstancedMesh(geo, mat, mats.length);
  const col = new THREE.Color();
  mats.forEach((m, i) => {
    mesh.setMatrixAt(i, m);
    const k = 1 - colorJitter / 2 + r() * colorJitter;
    mesh.setColorAt(i, col.setRGB(k, k, k));
  });
  mesh.instanceMatrix.needsUpdate = true;
  mesh.castShadow = true;
  return mesh;
}

const _q = new THREE.Quaternion(), _e = new THREE.Euler(), _v = new THREE.Vector3(), _s = new THREE.Vector3();
function mat4(x, y, z, rx, ry, rz, sx, sy = sx, sz = sx) {
  return new THREE.Matrix4().compose(_v.set(x, y, z), _q.setFromEuler(_e.set(rx, ry, rz, 'YXZ')), _s.set(sx, sy, sz));
}

// Bir bitki kümesi oluşturur. maxH: suyun altında kalabileceği en fazla yükseklik (cm). base: epifitlerin tutunacağı hazır taş/kök varsa true
function buildPlant(foto, r, maxH, { attached = false } = {}) {
  const d = BITKI_3D[foto];
  const g = new THREE.Group();
  if (!d) return g;
  const mat = leafMaterial(d.renk, d.uc || d.renk);
  let baseY = 0;

  if (d.taban && !attached) {
    if (d.taban === 'tas') {
      const rock = buildRock('seiryu', 1.6 + r() * 1.2, r);
      rock.position.y = 0.3;
      g.add(rock);
      baseY = 1.4;
    } else {
      const I = { L: 30, W: 20, y0: 0, waterTop: 14 };
      const w = buildWood('malezya', I, r, '#4a3324');
      w.scale.multiplyScalar(0.45);
      g.add(w);
      baseY = 1.6;
    }
  }

  if (d.tip === 'rozet') {
    const mats = [];
    for (let i = 0; i < d.adet; i++) {
      const len = Math.min(between(r, d.boy), maxH * 0.9);
      const tilt = THREE.MathUtils.degToRad(between(r, d.egim));
      mats.push(mat4((r() - 0.5) * 0.8, baseY, (r() - 0.5) * 0.8, tilt, r() * Math.PI * 2, (r() - 0.5) * 0.3, len));
    }
    g.add(instanced(leafGeometry(d.en, 0.25, !!d.dalga), mat, mats, 0.18, r));
  } else if (d.tip === 'serit') {
    const mats = [], spread = d.yayilim || 1.2;
    for (let i = 0; i < d.adet; i++) {
      const len = Math.min(between(r, d.boy), maxH * 0.97);
      const p = new THREE.Vector3((r() - 0.5) * spread * 2, 0, (r() - 0.5) * spread);
      const q = new THREE.Quaternion().setFromEuler(new THREE.Euler(THREE.MathUtils.degToRad(r() * 18), r() * Math.PI * 2, 0, 'YXZ'));
      mats.push(new THREE.Matrix4().compose(p, q, new THREE.Vector3(d.en, len, len * 0.6)));
    }
    g.add(instanced(leafGeometry(1, 0.18, !!d.dalga), mat, mats, 0.15, r));
  } else if (d.tip === 'govde') {
    const stemMats = [], leafMats = [], spread = d.yayilim || 2.6;
    const golden = Math.PI * (3 - Math.sqrt(5));
    for (let s = 0; s < d.sap; s++) {
      const h = Math.min(between(r, d.boy), maxH * 0.92);
      const sx = (r() - 0.5) * spread * 2, sz = (r() - 0.5) * spread;
      const lean = (r() - 0.5) * 0.14, leanDir = r() * Math.PI * 2;
      stemMats.push(mat4(sx + Math.sin(leanDir) * lean * h / 2, h / 2, sz + Math.cos(leanDir) * lean * h / 2, lean * Math.cos(leanDir), 0, -lean * Math.sin(leanDir), 1, h, 1));
      const nodes = Math.max(2, Math.floor(h / d.ara));
      for (let n = 1; n <= nodes; n++) {
        const y = (n / nodes) * h, k = y / h;
        const x = sx + Math.sin(leanDir) * lean * y, z = sz + Math.cos(leanDir) * lean * y;
        const size = d.yBoy * (0.55 + 0.45 * Math.min(1, k * 2.5)) * (k > 0.92 ? 0.7 : 1);
        for (let l = 0; l < d.yaprak; l++) {
          const yaw = (l / d.yaprak) * Math.PI * 2 + n * golden;
          leafMats.push(mat4(x, y, z, THREE.MathUtils.degToRad(55 + r() * 25 - k * 20), yaw, 0, size));
        }
      }
    }
    const stemMat = underwater(new THREE.MeshStandardMaterial({ color: d.renk, roughness: 0.7 }), { caustics: true, sway: true });
    g.add(instanced(new THREE.CylinderGeometry(0.1, 0.13, 1, 5), stemMat, stemMats, 0.1, r));
    const leaves = instanced(leafGeometry(d.yEn * 2, 0.15), leafMaterial('#ffffff', '#ffffff'), leafMats, 0.1, r);
    // yaprak rengi sap boyunca tabandan uca geçsin
    const c0 = new THREE.Color(d.renk), c1 = new THREE.Color(d.uc), tint = new THREE.Color();
    leafMats.forEach((m, i) => {
      const y = new THREE.Vector3().setFromMatrixPosition(m).y;
      const k = Math.pow(Math.min(1, y / (maxH * 0.8)), 1.5);
      leaves.setColorAt(i, tint.copy(c0).lerp(c1, k).multiplyScalar(0.92 + r() * 0.16));
    });
    g.add(leaves);
  } else if (d.tip === 'yosun') {
    // ince lif kümeleri
    const n = 520, mats = [];
    const rx = 4 + r() * 2, rz = 2.5 + r(), ry = between(r, d.boy) * 0.55;
    for (let i = 0; i < n; i++) {
      const a = r() * Math.PI * 2, u = Math.sqrt(r());
      const x = Math.cos(a) * rx * u, z = Math.sin(a) * rz * u, y = baseY + ry * Math.sqrt(Math.max(0, 1 - u * u)) * (0.4 + r() * 0.6);
      mats.push(mat4(x, y, z, r() * 3, r() * 6, r() * 3, 0.5 + r() * 0.5));
    }
    const mesh = instanced(leafGeometry(0.22, 0.2), leafMaterial(d.renk, d.uc, { textured: false }), mats, 0.3, r);
    g.add(mesh);
  } else if (d.tip === 'top') {
    const geo = new THREE.IcosahedronGeometry(1, 4);
    const pos = geo.attributes.position;
    for (let j = 0; j < pos.count; j++) {
      const k = 1 + (r() - 0.5) * 0.08;
      pos.setXYZ(j, pos.getX(j) * k, pos.getY(j) * k, pos.getZ(j) * k);
    }
    geo.computeVertexNormals();
    const mm = underwater(new THREE.MeshStandardMaterial({ color: d.renk, roughness: 1 }), { caustics: true });
    const n = 1 + Math.floor(r() * 2);
    for (let i = 0; i < n; i++) {
      const s = between(r, d.boy);
      const m = new THREE.Mesh(geo, mm);
      m.scale.setScalar(s);
      m.position.set(i * s * 2.1, s * 0.9, (r() - 0.5) * 2);
      m.castShadow = true;
      g.add(m);
    }
  }
  return g;
}

// Yüzen bitki: su yüzeyine yatay yapraklar
function buildFloating(foto, r) {
  const d = BITKI_3D[foto];
  const g = new THREE.Group();
  const mats = [];
  for (let i = 0; i < d.yaprak; i++) {
    const a = r() * Math.PI * 2, rad = Math.sqrt(r()) * 4;
    mats.push(mat4(Math.cos(a) * rad, 0.05 + r() * 0.1, Math.sin(a) * rad, -Math.PI / 2 + (r() - 0.5) * 0.2, r() * Math.PI * 2, 0, d.yBoy));
  }
  const geo = new THREE.CircleGeometry(0.5, 14);
  geo.scale(d.yuvarlak, 1, 1);
  geo.translate(0, 0.5, 0);
  geo.setAttribute('t', new THREE.BufferAttribute(new Float32Array(geo.attributes.position.count * 3).fill(0.5), 3));
  g.add(instanced(geo, leafMaterial(d.renk, d.uc, { sway: false }), mats, 0.2, r));
  if (d.kok) {
    const rootMat = new THREE.MeshStandardMaterial({ color: '#d9cfb8', roughness: 1 });
    const rm = [];
    for (let i = 0; i < d.yaprak * 2; i++) {
      const L = 4 + r() * 6;
      rm.push(mat4((r() - 0.5) * 7, -L / 2, (r() - 0.5) * 7, (r() - 0.5) * 0.2, 0, (r() - 0.5) * 0.2, 1, L, 1));
    }
    g.add(instanced(new THREE.CylinderGeometry(0.03, 0.03, 1, 3), rootMat, rm, 0.1, r));
  }
  return g;
}

/* ---------- Balıklar ---------- */

// Balık türleri ve bakım kuralları (sayfa uygunluk kontrolünde de kullanır).
// minLitre: altında önerilmez · rahatLitre: altında not düşülür · suru: önerilen en az sürü sayısı · maxAdet: en fazla adet
// boy: yetişkin boyu (cm) · bolge: yüzdüğü su katmanı (0 = zemin, 1 = yüzey)
export const BALIKLAR = [
  { id: 'betta', ad: 'Beta balığı', latin: 'Betta splendens', boy: 6, minLitre: 20, maxAdet: 1, sicaklik: '24–28 °C',
    aciklama: 'Uzun, dalgalı yüzgeçli, renkli labirent balığı. Su yüzeyinden hava da solur; sakin akıntı sever.',
    not: 'Tek erkek beta bulundurulur; iki erkek dövüşür.', bolge: [0.55, 0.92] },
  { id: 'neon', ad: 'Neon tetra', latin: 'Paracheirodon innesi', boy: 3.5, minLitre: 40, rahatLitre: 54, suru: 6, sicaklik: '22–26 °C',
    aciklama: 'Parlak mavi şeritli, arkası kırmızı küçük balık. Sürü halinde, orta su katmanında yüzer.',
    not: 'En az 6’lı sürü halinde bulundurun; tek başına strese girer.', bolge: [0.35, 0.7] },
  { id: 'lepistes', ad: 'Lepistes (Guppy)', latin: 'Poecilia reticulata', boy: 4, minLitre: 30, sicaklik: '22–28 °C',
    aciklama: 'Renkli yelpaze kuyruklu, hareketli ve canlı doğuran balık.',
    not: 'Erkek ve dişi bir aradaysa hızla çoğalır.', bolge: [0.5, 0.9] },
  { id: 'koridoras', ad: 'Panda koridoras', latin: 'Corydoras panda', boy: 4.5, minLitre: 40, rahatLitre: 54, suru: 6, sicaklik: '22–26 °C',
    aciklama: 'Zeminde bıyıklarıyla yiyecek arayan, barışçıl ve sürü halinde yaşayan dip balığı.',
    not: 'Sürü halinde (en az 6) bulundurun; bıyıkları için ince kum zemin tercih edilir.', bolge: [0, 0.12] },
];

// Balık gövdesi: +x yönüne bakan, kuyruğa doğru incelen elipsoit; renkler tepe noktası rengiyle
function fishBody(len, height, width, colorFn) {
  let geo = new THREE.SphereGeometry(1, 28, 18);
  geo.deleteAttribute('uv');
  geo = mergeVertices(geo);
  const pos = geo.attributes.position, col = new Float32Array(pos.count * 3), c = new THREE.Color();
  for (let i = 0; i < pos.count; i++) {
    let x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    const taper = x < 0 ? 1 + x * 0.72 : 1 - x * x * 0.18; // kuyruğa doğru incelir, burun yuvarlak
    y *= taper; z *= taper;
    const u = (x + 1) / 2, v = y; // u: kuyruk(0) → baş(1), v: -1 alt … 1 üst
    colorFn(c, u, v, z);
    pos.setXYZ(i, x * len / 2, y * height / 2, z * width / 2);
    col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  geo.computeVertexNormals();
  return geo;
}

function finShape(points) {
  const sh = new THREE.Shape();
  sh.moveTo(points[0][0], points[0][1]);
  for (let i = 1; i < points.length; i++) sh.lineTo(points[i][0], points[i][1]);
  const geo = new THREE.ShapeGeometry(sh);
  return geo;
}

function finMat(color, opacity = 0.8) {
  return new THREE.MeshStandardMaterial({ color, transparent: true, opacity, side: THREE.DoubleSide, roughness: 0.5, depthWrite: false });
}

// Blender'da modellenen, kendi yüzme animasyonu olan betta (assets/modeller/betta.glb).
// Yüklenemezse aşağıdaki kodla çizilen betta kullanılır.
const BETTA_GLB = '../assets/modeller/betta.glb';
const BETTA_OLCEK = 1.8;   // Blender birimi -> cm (kuyruk dahil ~7 cm)
let bettaGLB = null;
const bettaHazir = new GLTFLoader().loadAsync(BETTA_GLB).then(gltf => {
  gltf.scene.traverse(o => {
    if (o.geometry) o.geometry.userData.shared = true;   // sahne yenilenirken silinmesin
    if (o.material) {
      o.material.userData.shared = true;
      if (o.material.transparent) { o.material.depthWrite = false; o.material.side = THREE.DoubleSide; }
    }
    if (o.isMesh) o.castShadow = true;
  });
  bettaGLB = gltf;
  return gltf;
}).catch(e => { console.warn('Betta modeli yüklenemedi, çizim kullanılıyor:', e); return null; });

// Renk seçenekleri: modelin dokusu maviyi taşır; diğer renkler ton döndürülerek elde edilir
// (beyaz yüzgeç uçları beyaz kalır). derece: mavi tonundan döndürme açısı.
const BETTA_RENKLERI = [
  { ad: 'mavi', derece: 0 },
  { ad: 'kırmızı', derece: 125 },
];
const bettaMalzemeleri = new Map(); // derece -> {asil malzeme uuid -> tonlu kopya}

function tonluMalzeme(mat, derece) {
  if (!derece || /goz/i.test(mat.name)) return mat;      // gözler renk değiştirmez
  let cache = bettaMalzemeleri.get(derece);
  if (!cache) bettaMalzemeleri.set(derece, cache = new Map());
  if (cache.has(mat.uuid)) return cache.get(mat.uuid);
  const m = mat.clone();
  m.userData.shared = true;
  const aci = THREE.MathUtils.degToRad(derece);
  m.onBeforeCompile = sh => {
    sh.uniforms.uTon = { value: aci };
    sh.fragmentShader = 'uniform float uTon;\n' + sh.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
      { const vec3 k = vec3(0.57735);
        float c = cos(uTon), s = sin(uTon);
        diffuseColor.rgb = diffuseColor.rgb * c + cross(k, diffuseColor.rgb) * s + k * dot(k, diffuseColor.rgb) * (1.0 - c); }`);
  };
  m.customProgramCacheKey = () => 'betta-ton-' + derece;
  cache.set(mat.uuid, m);
  return m;
}

function bettaModeli(r) {
  const outer = new THREE.Group(), g = new THREE.Group();
  g.rotation.y = -Math.PI / 2; // model +x'e bakıyor; lookAt +z kullandığı için çevir
  outer.add(g);
  const model = bettaGLB.scene.clone(true);
  model.scale.setScalar(BETTA_OLCEK);
  const renk = BETTA_RENKLERI[Math.floor(r() * BETTA_RENKLERI.length)];
  if (renk.derece) model.traverse(o => { if (o.isMesh) o.material = tonluMalzeme(o.material, renk.derece); });
  g.add(model);
  const mixer = new THREE.AnimationMixer(model);
  bettaGLB.animations.forEach(c => mixer.clipAction(c).play());
  mixer.setTime(r() * 3);           // her betta farklı fazda yüzsün
  outer.userData.tail = new THREE.Object3D(); // kuyruk hareketi animasyonda
  outer.userData.inner = g;
  outer.userData.len = 6;
  outer.userData.mixer = mixer;
  return outer;
}

// Tek bir balık modeli; group.userData.tail kuyruk pivotu (yüzerken sallanır)
function buildFishModel(id, r) {
  if (id === 'betta' && bettaGLB) return bettaModeli(r);
  const outer = new THREE.Group(), g = new THREE.Group();
  g.rotation.y = -Math.PI / 2; // model +x'e bakıyor; lookAt +z kullandığı için çevir
  outer.add(g);
  const bodyMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.35, metalness: 0.15 });
  const tail = new THREE.Group();
  let L = 4;
  if (id === 'betta') {
    const palettes = [['#8e0f1f', '#c3182c', '#3a2a8f'], ['#1d3fa3', '#2e6fd8', '#8a1a3a'], ['#5a1a8c', '#8a2fc4', '#c3182c'], ['#b3121e', '#e0382a', '#f2c14e']];
    const [c0, c1, c2] = palettes[Math.floor(r() * palettes.length)];
    L = 4.6;
    const body = new THREE.Mesh(fishBody(L, 1.5, 1.0, (c, u, v) => c.set(c0).lerp(new THREE.Color(c1), clamp(0.5 + v * 0.4 + u * 0.2, 0, 1))), bodyMat);
    g.add(body);
    const fm = finMat(c1, 0.88), fm2 = finMat(c2, 0.82);
    // uzun, dalgalı kuyruk ve sırt/anal yüzgeçleri
    const tailGeo = finShape([[0, 0.3], [-1.8, 1.9], [-3.6, 2.2], [-4.2, 0.2], [-3.8, -2.0], [-2.0, -2.4], [0, -0.4]]);
    const tm = new THREE.Mesh(tailGeo, fm); tail.add(tm);
    tail.position.x = -L / 2 + 0.2;
    g.add(tail);
    const dorsal = new THREE.Mesh(finShape([[0.6, 0.55], [-0.4, 1.8], [-2.2, 1.9], [-2.3, 0.45]]), fm2);
    const anal = new THREE.Mesh(finShape([[1.0, -0.5], [-0.2, -2.3], [-2.3, -2.6], [-2.3, -0.4]]), fm);
    g.add(dorsal, anal);
    g.userData.wave = [dorsal, anal];
    const pect = new THREE.Mesh(finShape([[0, 0], [-0.9, 0.3], [-0.9, -0.3]]), finMat('#f3d8d8', 0.4));
    pect.position.set(1.0, -0.15, 0.52); g.add(pect);
  } else if (id === 'neon') {
    L = 3.2;
    const body = new THREE.Mesh(fishBody(L, 0.8, 0.5, (c, u, v) => {
      if (v > 0.05 && v < 0.35 && u > 0.18) c.set('#27c8ff').lerp(new THREE.Color('#5ef0ff'), (v - 0.05) * 2);
      else if (v <= 0.05 && u < 0.55) c.set('#e0263a');
      else if (v >= 0.35) c.set('#5b6246');
      else c.set('#d9dfe3');
    }), bodyMat);
    g.add(body);
    const tm = new THREE.Mesh(finShape([[0, 0.12], [-0.7, 0.5], [-0.55, 0], [-0.7, -0.5], [0, -0.12]]), finMat('#e9eef0', 0.35));
    tail.add(tm); tail.position.x = -L / 2 + 0.1; g.add(tail);
    const dorsal = new THREE.Mesh(finShape([[0.1, 0.3], [-0.2, 0.62], [-0.45, 0.3]]), finMat('#e9eef0', 0.35));
    g.add(dorsal);
  } else if (id === 'lepistes') {
    const tails = [['#ff7a1a', '#2b6fd8'], ['#2b6fd8', '#f2c14e'], ['#e0382a', '#1b1b1b'], ['#f2c14e', '#8a2fc4']];
    const [t0, t1] = tails[Math.floor(r() * tails.length)];
    L = 2.6;
    const body = new THREE.Mesh(fishBody(L, 0.75, 0.5, (c, u, v) => c.set('#b8c2c6').lerp(new THREE.Color(u < 0.35 ? t0 : '#d8dde0'), u < 0.35 ? 0.6 : clamp(-v, 0, 0.5))), bodyMat);
    g.add(body);
    const tm = new THREE.Mesh(finShape([[0, 0.2], [-1.2, 1.1], [-1.9, 0.6], [-2.0, 0], [-1.9, -0.6], [-1.2, -1.1], [0, -0.2]]), finMat(t0, 0.85));
    const spot = new THREE.Mesh(finShape([[-0.8, 0.5], [-1.6, 0.7], [-1.7, -0.3], [-0.9, -0.2]]), finMat(t1, 0.8));
    spot.position.z = 0.01;
    tail.add(tm, spot); tail.position.x = -L / 2 + 0.1; g.add(tail);
    const dorsal = new THREE.Mesh(finShape([[0, 0.3], [-0.4, 0.8], [-0.9, 0.3]]), finMat(t0, 0.7));
    g.add(dorsal);
  } else if (id === 'koridoras') {
    L = 3.8;
    const body = new THREE.Mesh(fishBody(L, 1.4, 1.05, (c, u, v, z) => {
      const eye = u > 0.78 && v > -0.1 && v < 0.6;          // gözdeki siyah bant
      const back = u > 0.35 && u < 0.6 && v > 0.45;         // sırt lekesi
      const tailSpot = u < 0.12;                             // kuyruk sapı lekesi
      c.set(eye || back || tailSpot ? '#1c1a1a' : v < -0.4 ? '#f3ece6' : '#e9d9cf');
    }), bodyMat);
    body.scale.y = 0.9;
    g.add(body);
    const tm = new THREE.Mesh(finShape([[0, 0.2], [-0.9, 0.7], [-0.75, 0], [-0.9, -0.7], [0, -0.2]]), finMat('#e9e2dc', 0.6));
    tail.add(tm); tail.position.x = -L / 2 + 0.15; g.add(tail);
    const dorsal = new THREE.Mesh(finShape([[0.4, 0.55], [0.1, 1.35], [-0.4, 0.6]]), finMat('#1c1a1a', 0.85));
    g.add(dorsal);
    // bıyıklar
    const bm = new THREE.MeshStandardMaterial({ color: '#e9d9cf', roughness: 0.6 });
    for (const zz of [-0.18, 0.18]) {
      const w = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.35, 4), bm);
      w.position.set(L / 2 - 0.05, -0.4, zz); w.rotation.z = 0.8; g.add(w);
    }
    g.userData.dip = true;
  }
  // gözler
  const eyeMat = new THREE.MeshStandardMaterial({ color: '#0d0d0d', roughness: 0.15, metalness: 0.3 });
  const eyeR = L * 0.055;
  for (const zz of [-1, 1]) {
    const e = new THREE.Mesh(new THREE.SphereGeometry(eyeR, 10, 8), eyeMat);
    e.position.set(L * 0.36, L * 0.05, zz * L * 0.1);
    g.add(e);
  }
  outer.traverse(o => { if (o.isMesh) o.castShadow = true; });
  outer.userData.tail = tail;
  outer.userData.inner = g;
  outer.userData.len = L;
  return outer;
}

/* ---------- Ortam: arka plan, kaide, lamba ---------- */

function backgroundTexture() {
  return canvasTexture(16, 512, (x, w, h) => {
    const g = x.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#f7f6f0'); g.addColorStop(0.55, '#eceee4'); g.addColorStop(1, '#d9dccd');
    x.fillStyle = g; x.fillRect(0, 0, w, h);
  }, { repeat: false });
}

let woodTopTex = null;
function woodTexture() {
  if (woodTopTex) return woodTopTex;
  woodTopTex = canvasTexture(512, 128, (x, w, h) => {
    x.fillStyle = '#a77b53'; x.fillRect(0, 0, w, h);
    const r = rng(12);
    for (let i = 0; i < 70; i++) {
      x.strokeStyle = `rgba(${r() > 0.5 ? '70,40,20' : '200,160,110'},${0.08 + r() * 0.18})`;
      x.lineWidth = 0.6 + r() * 2.2;
      const y0 = r() * h;
      x.beginPath(); x.moveTo(0, y0);
      for (let px = 0; px <= w; px += 16) x.lineTo(px, y0 + Math.sin(px * 0.01 + i) * 4 + Math.sin(px * 0.05 + i * 2) * 1.5);
      x.stroke();
    }
  });
  return woodTopTex;
}

// Tankled alüminyum aydınlatma barı (6500K)
function buildLampBar(L, W, H) {
  const g = new THREE.Group();
  const alu = new THREE.MeshStandardMaterial({ color: '#c8ccce', metalness: 1, roughness: 0.32 });
  const len = L * 0.92, y = H + 7;
  const bar = new THREE.Mesh(new THREE.BoxGeometry(len, 1.1, 5), alu);
  bar.position.y = y;
  bar.castShadow = false; // ışığın kaynağı olduğu için zemine gölge düşürmesin
  g.add(bar);
  const led = new THREE.Mesh(new THREE.PlaneGeometry(len - 2, 3.2), new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: '#f2f6ff', emissiveIntensity: 3.2 }));
  led.rotation.x = Math.PI / 2;
  led.position.y = y - 0.56;
  g.add(led);
  for (const s of [-1, 1]) {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.5, 7.4, 1.2), alu);
    leg.position.set(s * (len / 2 - 2), H + 3.3, -W / 2 + 0.6);
    g.add(leg);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, W / 2 + 0.2), alu);
    arm.position.set(s * (len / 2 - 2), y - 0.2, -W / 4 + 0.3);
    g.add(arm);
  }
  return g;
}

/* ---------- Sahne ---------- */

export function createAquarium(container, { onModelError, onQuality } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.92;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);
  RectAreaLightUniformsLib.init();

  const scene = new THREE.Scene();
  scene.background = backgroundTexture();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.45;

  const camera = new THREE.PerspectiveCamera(35, 1, 0.5, 5000);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.7;
  controls.maxPolarAngle = THREE.MathUtils.degToRad(92);
  controls.enablePan = false;

  scene.add(new THREE.HemisphereLight('#ffffff', '#b8a98a', 0.35));
  const sun = new THREE.DirectionalLight('#f4f7ff', 1.3);
  sun.castShadow = true;
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.04;
  scene.add(sun, sun.target);
  const fill = new THREE.DirectionalLight('#fff4e6', 0.35);
  fill.position.set(-80, 40, 120);
  scene.add(fill);
  const area = new THREE.RectAreaLight('#f3f6ff', 6, 10, 4);
  scene.add(area);

  // Zemin: yumuşak temas gölgesi + gölge alan düzlem
  const shadowTex = canvasTexture(128, 128, (x) => {
    const gr = x.createRadialGradient(64, 64, 4, 64, 64, 64);
    gr.addColorStop(0, 'rgba(40,50,35,.32)'); gr.addColorStop(1, 'rgba(40,50,35,0)');
    x.fillStyle = gr; x.fillRect(0, 0, 128, 128);
  }, { repeat: false, srgb: false });
  const contact = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false }));
  contact.rotation.x = -Math.PI / 2;
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.ShadowMaterial({ opacity: 0.14 }));
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(contact, floor);

  const root = new THREE.Group();
  scene.add(root);
  let tankGroup = null, contentGroup = null;
  let waterSurface = null, particles = null;

  const state = {
    model: { tip: 'kutu', L: 60, W: 30, H: 36, cam: 0.6 },
    interior: null, // { L, W, H, y0, waterTop }
    zemin: 'aquasoil', kalinlik: 5,
    plants: [], hardscape: [], fish: [], seed: 1,
    quality: 'yuksek',
  };

  /* --- Post-processing --- */
  let composer = null, bloom = null;
  function buildComposer() {
    const w = Math.max(1, container.clientWidth), h = Math.max(1, container.clientHeight);
    const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: 4 });
    composer = new EffectComposer(renderer, rt);
    composer.addPass(new RenderPass(scene, camera));
    // Not: ortam gölgesi (GTAO) zemin kesitinde çizgi/şerit izleri bıraktığı için kullanılmıyor
    bloom = new UnrealBloomPass(new THREE.Vector2(w, h), 0.35, 0.5, 1.1); // yalnızca lamba gibi parlak (HDR) kaynaklar parlasın
    composer.addPass(bloom);
    composer.addPass(new OutputPass());
  }

  function applyQuality() {
    const hi = state.quality === 'yuksek';
    renderer.setPixelRatio(hi ? Math.min(window.devicePixelRatio, 2) : 1);
    sun.shadow.mapSize.set(hi ? 2048 : 1024, hi ? 2048 : 1024);
    if (sun.shadow.map) { sun.shadow.map.dispose(); sun.shadow.map = null; }
    if (hi && !composer) buildComposer();
    resize();
  }

  /* --- Zemin yüksekliği --- */
  function surfaceY(x, z) {
    const I = state.interior;
    if (!I || state.zemin === 'yok' || !ZEMIN_GORUNUM[state.zemin]) return I ? I.y0 : 0;
    const back = clamp((I.W / 2 - z) / I.W, 0, 1); // 0 ön, 1 arka
    const t = state.kalinlik;
    // düzensiz, yumuşak dalgalanma (düzenli sinüs çizgileri yerine)
    const bumps = fbm(x * 0.03 + state.seed * 3.1, z * 0.045, state.seed * 0.37, 2) * 0.6;
    return I.y0 + t * (0.85 + 0.75 * back * back) + bumps * Math.min(1, t / 4);
  }

  /* --- Akvaryum gövdesi --- */
  // Cam: yalnızca yansımaları ekler (additive), içeriği süt gibi örtmez
  const glassMat = new THREE.MeshPhysicalMaterial({
    color: '#000000', roughness: 0.03, metalness: 0, clearcoat: 0.25, clearcoatRoughness: 0.03, envMapIntensity: 0.45,
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide,
  });
  const glassEdgeMat = new THREE.MeshPhysicalMaterial({ color: '#86c4b0', transparent: true, opacity: 0.6, roughness: 0.05, clearcoat: 1, depthWrite: false });
  const siliconeMat = new THREE.MeshStandardMaterial({ color: '#1e2422', roughness: 0.4, transparent: true, opacity: 0.8 });

  function buildBoxTank() {
    const { L, W, H, cam } = state.model;
    const g = new THREE.Group();
    const panes = [
      [L, cam, W, 0, cam / 2, 0],               // taban
      [L, H, cam, 0, H / 2, W / 2 - cam / 2],   // ön
      [L, H, cam, 0, H / 2, -W / 2 + cam / 2],  // arka
      [cam, H, W - cam * 2, L / 2 - cam / 2, H / 2, 0],
      [cam, H, W - cam * 2, -L / 2 + cam / 2, H / 2, 0],
    ];
    panes.forEach(([sx, sy, sz, x, y, z]) => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(sx, sy, sz), glassMat);
      m.position.set(x, y, z);
      m.renderOrder = 5;
      m.userData.noAO = true;
      g.add(m);
    });
    // Camın kenarları (gerçek camda yeşilimsi görünür) ve siyah silikon
    const e = cam * 1.02;
    const edges = [
      ...[[1, 1], [1, -1], [-1, 1], [-1, -1]].map(([sx, sz]) => [e, H, e, sx * (L / 2 - e / 2), H / 2, sz * (W / 2 - e / 2)]),
      [L, e, e, 0, H - e / 2, W / 2 - e / 2], [L, e, e, 0, H - e / 2, -W / 2 + e / 2],
      [e, e, W, L / 2 - e / 2, H - e / 2, 0], [e, e, W, -L / 2 + e / 2, H - e / 2, 0],
    ];
    edges.forEach(([sx, sy, sz, x, y, z]) => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(sx, sy, sz), glassEdgeMat);
      m.position.set(x, y, z);
      m.renderOrder = 6;
      m.userData.noAO = true;
      g.add(m);
    });
    const s = 0.35;
    [[1, 1], [1, -1], [-1, 1], [-1, -1]].forEach(([sx, sz]) => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(s, H - cam, s), siliconeMat);
      m.position.set(sx * (L / 2 - cam - s / 2), cam + (H - cam) / 2, sz * (W / 2 - cam - s / 2));
      m.userData.noAO = true;
      g.add(m);
    });
    // Ahşap kaide
    const wood = woodTexture();
    wood.repeat.set(Math.max(1, L / 60), 1);
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(L + 8, 4, W + 8), new THREE.MeshStandardMaterial({ map: wood, roughness: 0.55, metalness: 0 }));
    plinth.position.y = -2;
    plinth.receiveShadow = plinth.castShadow = true;
    g.add(plinth);
    g.add(buildLampBar(L, W, H));
    state.interior = { L: L - cam * 2, W: W - cam * 2, H: H - cam, y0: cam, waterTop: H - 2, floorY: -4 };
    return g;
  }

  const loader = new GLTFLoader();
  const modelCache = new Map();
  async function buildCustomTank(cfg) {
    let gltf = modelCache.get(cfg.dosya);
    if (!gltf) {
      gltf = await loader.loadAsync(cfg.dosya);
      modelCache.set(cfg.dosya, gltf);
    }
    const g = new THREE.Group();
    const model = gltf.scene.clone(true);
    model.scale.setScalar(cfg.olcek ?? 100);
    const box = new THREE.Box3().setFromObject(model);
    const c = box.getCenter(new THREE.Vector3());
    model.position.set(-c.x, -box.min.y, -c.z);
    model.traverse(o => {
      if (!o.isMesh) return;
      o.castShadow = o.receiveShadow = true;
      if (o.material?.transparent) o.userData.noAO = true;
    });
    g.add(model);
    const ic = cfg.ic;
    const y0 = cfg.icTaban ?? 0;
    state.interior = { L: ic.L, W: ic.W, H: ic.H, y0, waterTop: y0 + (cfg.su ?? ic.H - 2), floorY: 0 };
    if (cfg.camEkle) {
      const glass = new THREE.Mesh(new THREE.BoxGeometry(ic.L, ic.H, ic.W), glassMat);
      glass.position.y = y0 + ic.H / 2;
      glass.renderOrder = 5;
      glass.userData.noAO = true;
      g.add(glass);
    }
    return g;
  }

  /* --- İçerik: zemin, taş/kök, bitkiler, su --- */
  function substrateMaterial(key, { side = false } = {}) {
    const { map, normal } = grainTextures(key);
    const m = side
      // Cam arkasından görünen kesit: sıkışmış/ıslak, biraz daha koyu; normal haritası yok (çizgi oluşmasın)
      ? new THREE.MeshStandardMaterial({ map, color: '#cfc7bd', roughness: 1, metalness: 0, side: THREE.DoubleSide })
      : new THREE.MeshStandardMaterial({ map, normalMap: normal, normalScale: new THREE.Vector2(0.35, 0.35), roughness: 0.95, metalness: 0 });
    return underwater(m, { caustics: !side });
  }

  function buildSubstrate(g) {
    const I = state.interior, look = ZEMIN_GORUNUM[state.zemin];
    if (!look) return;
    const nx = 64, nz = 32;
    const top = new THREE.PlaneGeometry(I.L, I.W, nx, nz);
    top.rotateX(-Math.PI / 2);
    const pos = top.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setY(i, surfaceY(pos.getX(i), pos.getZ(i)));
    top.computeVertexNormals();
    const uv = top.attributes.uv;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / TILE_CM, pos.getZ(i) / TILE_CM);
    const topMesh = new THREE.Mesh(top, substrateMaterial(state.zemin));
    topMesh.receiveShadow = true;
    g.add(topMesh);

    // Yan yüzler: cam arkasından görünen zemin kesiti
    const sides = [];
    const edge = (x0, z0, x1, z1, n) => {
      const pts = [];
      for (let i = 0; i <= n; i++) {
        const x = lerp(x0, x1, i / n), z = lerp(z0, z1, i / n);
        pts.push([x, z, surfaceY(x, z)]);
      }
      sides.push(pts);
    };
    edge(-I.L / 2, I.W / 2, I.L / 2, I.W / 2, nx);
    edge(I.L / 2, -I.W / 2, -I.L / 2, -I.W / 2, nx);
    edge(I.L / 2, I.W / 2, I.L / 2, -I.W / 2, nz);
    edge(-I.L / 2, -I.W / 2, -I.L / 2, I.W / 2, nz);
    const altY = look.alt ? I.y0 + state.kalinlik * 0.45 : null;
    const layer = (key, yFrom, yTo) => {
      const verts = [], uvs = [], idx = [];
      sides.forEach(pts => {
        const start = verts.length / 3;
        let run = 0;
        pts.forEach(([x, z, y], i) => {
          if (i) run += Math.hypot(x - pts[i - 1][0], z - pts[i - 1][1]);
          const yb = yFrom, yt = yTo === null ? y : Math.min(y, yTo);
          verts.push(x, yb, z, x, yt, z);
          uvs.push(run / TILE_CM, yb / TILE_CM, run / TILE_CM, yt / TILE_CM);
        });
        for (let i = 0; i < pts.length - 1; i++) {
          const a = start + i * 2;
          idx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3);
        }
      });
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
      geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
      geo.setIndex(idx);
      geo.computeVertexNormals();
      const sideMesh = new THREE.Mesh(geo, substrateMaterial(key, { side: true }));
      sideMesh.userData.noAO = true;
      g.add(sideMesh);
    };
    if (look.alt) {
      layer(look.alt, I.y0, altY);
      layer(state.zemin, altY, null);
    } else {
      layer(state.zemin, I.y0, null);
    }

    // İri zeminler: üzerine gerçek taş taneleri
    if (look.tas) {
      const r = rng(state.seed * 7 + 3);
      const avg = (look.tas[0] + look.tas[1]) / 2;
      const count = Math.min(6000, Math.round((I.L * I.W) / (avg * avg) * 0.6));
      const geo = new THREE.IcosahedronGeometry(1, 1);
      const p = geo.attributes.position;
      for (let i = 0; i < p.count; i++) { const k = 0.85 + ((i * 7919) % 13) / 60; p.setXYZ(i, p.getX(i) * k, p.getY(i) * k, p.getZ(i) * k); }
      geo.computeVertexNormals();
      const mats = [];
      for (let i = 0; i < count; i++) {
        const s = between(r, look.tas) / 2;
        const x = (r() - 0.5) * (I.L - s * 2), z = (r() - 0.5) * (I.W - s * 2);
        mats.push(mat4(x, surfaceY(x, z) - s * 0.15, z, r() * 3, r() * 3, r() * 3, s * (0.8 + r() * 0.5), s * (0.5 + r() * 0.3), s * (0.8 + r() * 0.5)));
      }
      const mesh = new THREE.InstancedMesh(geo, underwater(new THREE.MeshStandardMaterial({ roughness: 0.9 }), { caustics: true }), mats.length);
      const col = new THREE.Color();
      mats.forEach((m, i) => {
        mesh.setMatrixAt(i, m);
        mesh.setColorAt(i, col.set(look.tasRenk[Math.floor(r() * look.tasRenk.length)]));
      });
      mesh.castShadow = mesh.receiveShadow = true;
      g.add(mesh);
    }
  }

  function buildWater(g) {
    const I = state.interior;
    const h = I.waterTop - I.y0;
    // Arka camda buzlu arka plan filmi etkisi
    const hazeTex = canvasTexture(8, 256, (x, w, hh) => {
      const gr = x.createLinearGradient(0, 0, 0, hh);
      gr.addColorStop(0, 'rgba(244,250,250,.85)'); gr.addColorStop(1, 'rgba(196,222,220,.7)');
      x.fillStyle = gr; x.fillRect(0, 0, w, hh);
    }, { repeat: false });
    const haze = new THREE.Mesh(new THREE.PlaneGeometry(I.L - 0.2, h), new THREE.MeshBasicMaterial({ map: hazeTex, transparent: true, opacity: 0.55, depthWrite: false }));
    haze.position.set(0, I.y0 + h / 2, -I.W / 2 + 0.15);
    haze.renderOrder = 1;
    haze.userData.noAO = true;
    g.add(haze);
    // Su yüzeyi: hareketli dalgacıklar ve yansıma
    if (!buildWater.normal) {
      const hc = document.createElement('canvas');
      hc.width = hc.height = 256;
      const x = hc.getContext('2d'), img = x.createImageData(256, 256);
      for (let yy = 0; yy < 256; yy++) for (let xx = 0; xx < 256; xx++) {
        const u = xx / 256 * Math.PI * 2, v = yy / 256 * Math.PI * 2;
        const hv = Math.sin(u * 3 + Math.sin(v * 2) * 1.5) * 0.4 + Math.sin(v * 5 + u) * 0.3 + Math.sin((u + v) * 7) * 0.15 + Math.sin((u - v) * 4) * 0.2;
        const k = (hv * 0.5 + 0.5) * 255, i = (yy * 256 + xx) * 4;
        img.data[i] = img.data[i + 1] = img.data[i + 2] = k; img.data[i + 3] = 255;
      }
      x.putImageData(img, 0, 0);
      buildWater.normal = normalFromCanvas(hc, 4);
    }
    const nm = buildWater.normal;
    nm.repeat.set(I.L / 25, I.W / 25);
    waterSurface = new THREE.Mesh(new THREE.PlaneGeometry(I.L - 0.1, I.W - 0.1),
      new THREE.MeshPhysicalMaterial({ color: '#000000', roughness: 0.04, metalness: 0, normalMap: nm, normalScale: new THREE.Vector2(0.35, 0.35), envMapIntensity: 0.9, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
    waterSurface.rotation.x = -Math.PI / 2;
    waterSurface.position.y = I.waterTop;
    waterSurface.renderOrder = 3;
    waterSurface.userData.noAO = true;
    g.add(waterSurface);
    // Suda süzülen ince partiküller
    const n = Math.min(400, Math.round(I.L * I.W * h / 180));
    const pp = new Float32Array(n * 3);
    const r = rng(99);
    for (let i = 0; i < n; i++) { pp[i * 3] = (r() - 0.5) * (I.L - 2); pp[i * 3 + 1] = I.y0 + r() * h; pp[i * 3 + 2] = (r() - 0.5) * (I.W - 2); }
    const pg = new THREE.BufferGeometry();
    pg.setAttribute('position', new THREE.BufferAttribute(pp, 3));
    particles = new THREE.Points(pg, new THREE.PointsMaterial({ color: '#ffffff', size: 0.12, transparent: true, opacity: 0.35, depthWrite: false }));
    particles.userData = { noAO: true, bounds: { L: I.L - 2, W: I.W - 2, y0: I.y0, h } };
    g.add(particles);
  }

  // Yerleştirme: çakışmayı azaltmak için en boş noktayı seç
  function spotPicker(r) {
    const I = state.interior, placed = [];
    const pick = (zr, radius) => {
      let best = null, bestD = -Infinity;
      for (let t = 0; t < 24; t++) {
        const x = (r() - 0.5) * Math.max(0, I.L - radius * 2 - 3);
        const z = clamp(I.W / 2 - between(r, zr) * I.W, -I.W / 2 + radius + 1, I.W / 2 - radius - 1);
        const d = placed.reduce((m, p) => Math.min(m, Math.hypot(p.x - x, p.z - z) - p.r - radius), 999);
        if (d > bestD) { bestD = d; best = { x, z }; }
      }
      placed.push({ ...best, r: radius });
      return best;
    };
    return pick;
  }

  function buildHardscape(g, pick, r) {
    const I = state.interior, anchors = [];
    const baseSize = clamp(Math.min(I.L, I.W, I.H) * 0.26, 3, 16);
    state.hardscape.forEach(({ def, adet }) => {
      for (let k = 0; k < adet; k++) {
        if (def.tur === 'tas') {
          if (def.id === 'nehir-tasi') {
            const c = pick([0.25, 0.8], baseSize * 0.9);
            const n = 3 + Math.floor(r() * 3);
            for (let i = 0; i < n; i++) {
              const s = baseSize * (0.25 + r() * 0.3);
              const m = buildRock('nehir-tasi', s, r, NEHIR_RENK[Math.floor(r() * NEHIR_RENK.length)]);
              const x = c.x + (r() - 0.5) * baseSize * 1.4, z = c.z + (r() - 0.5) * baseSize * 0.8;
              m.position.set(x, surfaceY(x, z) + s * 0.05, z);
              m.rotation.y = r() * Math.PI * 2;
              g.add(m);
              anchors.push(new THREE.Vector3(x, surfaceY(x, z) + s * 0.55, z));
            }
          } else if (def.id === 'kayrak') {
            const c = pick([0.3, 0.85], baseSize);
            const n = 2 + Math.floor(r() * 2);
            let y = surfaceY(c.x, c.z);
            for (let i = 0; i < n; i++) {
              const s = baseSize * (1 - i * 0.22);
              const m = buildRock('kayrak', s, r);
              m.position.set(c.x + (r() - 0.5) * 2, y, c.z + (r() - 0.5) * 1.5);
              m.rotation.set((r() - 0.5) * 0.15, r() * Math.PI, (r() - 0.5) * 0.15);
              g.add(m);
              y += s * 0.32;
            }
            anchors.push(new THREE.Vector3(c.x, y, c.z));
          } else {
            const s = baseSize * (0.8 + r() * 0.45);
            const c = pick([0.3, 0.85], s);
            const m = buildRock(def.id, s, r);
            const y = surfaceY(c.x, c.z) - s * 0.12;
            m.position.set(c.x, y, c.z);
            m.rotation.y = r() * Math.PI * 2;
            g.add(m);
            const st = TAS_STIL[def.id];
            anchors.push(new THREE.Vector3(c.x, y + s * st.scale[1] * 0.9, c.z));
          }
        } else {
          const w = buildWood(def.id, I, r, def.renk);
          const c = pick([0.35, 0.8], Math.min(w.userData.radius, I.L / 3));
          w.position.set(c.x, surfaceY(c.x, c.z) - 0.4, c.z);
          w.rotation.y = (r() - 0.5) * 0.8;
          g.add(w);
          w.updateMatrixWorld(true);
          // dalların uçları epifit bitkiler için tutunma noktası
          w.userData.tips.filter((_, i) => i % 2 === 0).slice(0, 6).forEach(t => anchors.push(t.clone().applyMatrix4(w.matrixWorld).sub(g.position)));
        }
      }
    });
    return anchors;
  }

  function buildPlants(g, pick, r, anchors) {
    const I = state.interior;
    const items = [];
    state.plants.forEach(({ plant, adet }) => { for (let i = 0; i < adet; i++) items.push(plant); });
    const zOf = p => zone(p.bilgi[5]).z?.[0] ?? 0;
    items.sort((a, b) => zOf(b) - zOf(a));
    let anchorIdx = 0;

    items.forEach(p => {
      const d = BITKI_3D[p.foto];
      if (!d) return;
      const zn = zone(p.bilgi[5]);
      if (d.tip === 'yuzen') {
        const f = buildFloating(p.foto, r);
        f.position.set((r() - 0.5) * Math.max(0, I.L - 10), I.waterTop, (r() - 0.5) * Math.max(0, I.W - 10));
        g.add(f);
        return;
      }
      if (zn.yuzen) zn.z = [0.05, 0.4];
      if (d.tip === 'hali') {
        const pw = Math.min(I.L * 0.45, 30), pd = Math.min(I.W * 0.35, 14);
        const c = pick(zn.z, Math.min(pw, pd) / 2);
        const n = Math.min(3200, Math.round(pw * pd * 8));
        const mats = [];
        for (let i = 0; i < n; i++) {
          const a = r() * Math.PI * 2, rad = Math.sqrt(r());
          const x = clamp(c.x + Math.cos(a) * rad * pw / 2, -I.L / 2 + 0.5, I.L / 2 - 0.5);
          const z = clamp(c.z + Math.sin(a) * rad * pd / 2, -I.W / 2 + 0.5, I.W / 2 - 0.5);
          const h = r() * d.yukseklik * (1 - rad * 0.5);
          mats.push(mat4(x, surfaceY(x, z) + h, z, -Math.PI / 2 + (r() - 0.5) * 1.2, r() * Math.PI * 2, 0, d.yBoy * (0.7 + r() * 0.6)));
        }
        let geo;
        if (d.yuvarlak < 0.3) geo = leafGeometry(0.15, 0.1);
        else {
          geo = new THREE.CircleGeometry(0.5, 10).scale(d.yuvarlak, 1, 1).translate(0, 0.5, 0);
          geo.setAttribute('t', new THREE.BufferAttribute(new Float32Array(geo.attributes.position.count * 3).fill(0.6), 3));
        }
        const mesh = instanced(geo, leafMaterial(d.renk, d.uc, { textured: d.yuvarlak < 0.3 }), mats, 0.28, r);
        if (d.yuvarlak < 0.3) mats.forEach((m, i) => mesh.setMatrixAt(i, m.multiply(new THREE.Matrix4().makeRotationX(Math.PI / 2 - 0.3))));
        mesh.receiveShadow = true;
        g.add(mesh);
        return;
      }
      // Epifitler: akvaryumda taş/kök varsa onların üzerine tutunsun
      if (d.taban && anchors.length) {
        const a = anchors[anchorIdx++ % anchors.length];
        const plant = buildPlant(p.foto, r, Math.max(3, I.waterTop - a.y - 1), { attached: true });
        plant.position.set(a.x + (r() - 0.5) * 1.5, a.y - 0.6, a.z + (r() - 0.5) * 1.5);
        plant.rotation.y = r() * Math.PI * 2;
        g.add(plant);
        return;
      }
      const radius = d.tip === 'govde' ? 3.5 : d.tip === 'rozet' ? Math.min(between(r, d.boy) * 0.6, 12) : d.taban === 'kutuk' ? 7 : 4;
      const spot = pick(zn.z || [0.3, 0.7], radius);
      const y = surfaceY(spot.x, spot.z);
      const plant = buildPlant(p.foto, r, Math.max(3, I.waterTop - y - 1));
      plant.position.set(spot.x, y - (d.taban ? 0.4 : 0.2), spot.z);
      plant.rotation.y = r() * Math.PI * 2;
      g.add(plant);
    });
  }

  // Yüzen balıklar: her biri bölgesi içinde rastgele hedeflere doğru yumuşakça yüzer
  let swimmers = [];
  function buildFish(g) {
    const I = state.interior;
    swimmers = [];
    const r = rng(state.seed * 71 + 9);
    const water = I.waterTop - I.y0;
    const schools = {};
    state.fish.forEach(({ def, adet }) => {
      for (let k = 0; k < adet; k++) {
        const m = buildFishModel(def.id, r);
        const [b0, b1] = def.bolge;
        const f = {
          def, obj: m, speed: def.id === 'betta' ? 2.2 : def.id === 'koridoras' ? 2.4 : 4.5,
          pos: new THREE.Vector3((r() - 0.5) * (I.L - 8), I.y0 + water * between(r, [b0, b1]) + 1, (r() - 0.5) * (I.W - 6)),
          target: new THREE.Vector3(), phase: r() * 10, wait: 0,
          zone: [b0, b1], offset: new THREE.Vector3((r() - 0.5) * 6, (r() - 0.5) * 2.5, (r() - 0.5) * 4),
        };
        if (def.suru) { schools[def.id] = schools[def.id] || { target: new THREE.Vector3(), timer: 0 }; f.school = schools[def.id]; }
        m.position.copy(f.pos);
        g.add(m);
        swimmers.push(f);
      }
    });
    swimmers.forEach(f => pickTarget(f, r));
    Object.values(schools).forEach(sc => { sc.target.copy(swimmers.find(f => f.school === sc).pos); });
    buildFish.r = r;
  }
  function pickTarget(f, r = Math.random) {
    const I = state.interior, water = I.waterTop - I.y0, m = f.obj.userData.len + 1.5;
    const x = (r() - 0.5) * Math.max(1, I.L - m * 2), z = (r() - 0.5) * Math.max(1, I.W - m * 2);
    const floor = surfaceY(x, z);
    let y = I.y0 + water * between(r, f.zone);
    y = clamp(y, floor + (f.obj.userData.inner.userData.dip ? 0.9 : 3), I.waterTop - 1.5);
    f.target.set(x, y, z);
  }
  const _dir = new THREE.Vector3(), _look = new THREE.Object3D(), _goal = new THREE.Vector3();
  function updateFish(dt, t) {
    if (!swimmers.length) return;
    const I = state.interior;
    const schoolsSeen = new Set();
    swimmers.forEach(f => {
      if (f.school && !schoolsSeen.has(f.school)) {
        schoolsSeen.add(f.school);
        f.school.timer -= dt;
        if (f.school.timer <= 0) { const tmp = { ...f, target: f.school.target }; pickTarget(tmp); f.school.timer = 4 + Math.random() * 4; }
      }
      _goal.copy(f.school ? f.school.target : f.target);
      if (f.school) _goal.add(f.offset);
      if (f.wait > 0) { f.wait -= dt; _goal.copy(f.pos); }
      _dir.subVectors(_goal, f.pos);
      const d = _dir.length();
      if (!f.school && d < 1.5) {
        pickTarget(f);
        if (f.def.id === 'betta' || f.def.id === 'koridoras') f.wait = 1 + Math.random() * 2.5; // arada durup dinlensin
      }
      const sp = f.wait > 0 ? 0.3 : f.speed * (0.7 + 0.3 * Math.sin(t * 0.7 + f.phase));
      if (d > 0.05) f.pos.addScaledVector(_dir.normalize(), Math.min(d, sp * dt));
      // akvaryum içinde kal
      const m = f.obj.userData.len / 2 + 0.5;
      f.pos.x = clamp(f.pos.x, -I.L / 2 + m, I.L / 2 - m);
      f.pos.z = clamp(f.pos.z, -I.W / 2 + m, I.W / 2 - m);
      f.pos.y = clamp(f.pos.y, surfaceY(f.pos.x, f.pos.z) + 0.8, I.waterTop - 1);
      f.obj.position.copy(f.pos);
      // yüzme yönüne yumuşak dönüş
      if (d > 0.3 && f.wait <= 0) {
        _look.position.copy(f.pos);
        _look.lookAt(f.pos.x + _dir.x, f.pos.y + _dir.y * 0.4, f.pos.z + _dir.z);
        f.obj.quaternion.slerp(_look.quaternion, Math.min(1, dt * 2.5));
      }
      // kuyruk ve yüzgeç hareketi
      const beat = f.wait > 0 ? 2 : f.def.id === 'neon' ? 12 : 7;
      f.obj.userData.tail.rotation.y = Math.sin(t * beat + f.phase) * (f.def.id === 'betta' ? 0.35 : 0.45);
      if (f.obj.userData.mixer) f.obj.userData.mixer.update(dt * (f.wait > 0 ? 0.6 : 1));
      const inner = f.obj.userData.inner;
      inner.rotation.x = Math.sin(t * beat * 0.5 + f.phase) * 0.04;
      (inner.userData.wave || []).forEach((w, i) => { w.rotation.x = Math.sin(t * 2.2 + f.phase + i) * 0.12; });
    });
  }

  function rebuildContent() {
    if (contentGroup) { root.remove(contentGroup); disposeTree(contentGroup); }
    contentGroup = new THREE.Group();
    waterSurface = particles = null;
    const I = state.interior;
    if (I) {
      U.uWaterTop.value = I.waterTop;
      U.uFloor.value = I.y0 + state.kalinlik;
      buildSubstrate(contentGroup);
      const r = rng(state.seed * 131 + 17);
      const pick = spotPicker(r);
      const anchors = buildHardscape(contentGroup, pick, rng(state.seed * 53 + 5));
      buildPlants(contentGroup, pick, r, anchors);
      buildWater(contentGroup);
      buildFish(contentGroup);
    }
    root.add(contentGroup);
  }
  // betta modeli sahne kurulduktan sonra yüklenirse balıkları onunla yeniden kur
  bettaHazir.then(gltf => { if (gltf && state.fish?.some(f => f.def.id === 'betta')) rebuildContent(); });

  function fitLights() {
    const I = state.interior;
    if (!I) return;
    const top = state.model.tip === 'kutu' ? state.model.H + 6.4 : I.waterTop + 12;
    area.width = I.L * 0.88;
    area.height = Math.max(3, I.W * 0.18);
    area.intensity = 3.5;
    area.position.set(0, top, 0);
    area.lookAt(0, 0, 0);
    const span = Math.max(I.L, I.W) * 0.75 + 10;
    sun.position.set(span * 0.25, I.waterTop + 120, span * 0.35);
    sun.target.position.set(0, I.y0, 0);
    const cam = sun.shadow.camera;
    cam.left = cam.bottom = -span; cam.right = cam.top = span;
    cam.near = 1; cam.far = 400;
    cam.updateProjectionMatrix();
    floor.position.y = I.floorY;
    floor.scale.set(span * 1.8, span * 1.8, 1); // gölge düzlemi ufka uzanmasın
    contact.position.y = I.floorY + 0.02;
  }

  function frame() {
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y * 1.3, size.z);
    contact.scale.set(size.x * 1.5 + 10, size.z * 2 + 10, 1);
    controls.target.copy(center);
    const dist = maxDim / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2))) * 1.3 / Math.min(1, camera.aspect * 0.9);
    const dir = new THREE.Vector3(0.45, 0.17, 1).normalize();
    camera.position.copy(center).addScaledVector(dir, dist);
    controls.minDistance = maxDim * 0.35;
    controls.maxDistance = dist * 3;
    camera.near = Math.max(0.1, dist / 300);
    camera.far = dist * 12;
    camera.updateProjectionMatrix();
    controls.update();
  }

  let lastSizeKey = '';
  async function rebuildTank() {
    if (tankGroup) { root.remove(tankGroup); disposeTree(tankGroup); tankGroup = null; }
    try {
      tankGroup = state.model.tip === 'kutu' ? buildBoxTank() : await buildCustomTank(state.model);
    } catch (err) {
      onModelError?.(err);
      state.model = { tip: 'kutu', L: 60, W: 30, H: 36, cam: 0.6 };
      tankGroup = buildBoxTank();
    }
    root.add(tankGroup);
    fitLights();
    rebuildContent();
    const key = [state.model.tip, state.model.L, state.model.W, state.model.H].join('|');
    if (key !== lastSizeKey) { lastSizeKey = key; frame(); }
  }

  /* --- Döngü --- */
  function resize() {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    if (composer) {
      composer.setPixelRatio(renderer.getPixelRatio());
      composer.setSize(w, h);
    }
  }
  new ResizeObserver(resize).observe(container);
  applyQuality();

  renderer.domElement.addEventListener('pointerdown', () => { controls.autoRotate = false; api.onAutoRotate?.(false); });

  const clock = new THREE.Clock();
  const up = new THREE.Vector3();
  let fpsFrames = 0, fpsTime = 0, fpsChecked = false;
  function render() {
    if (state.quality === 'yuksek' && composer) composer.render();
    else renderer.render(scene, camera);
  }
  renderer.setAnimationLoop(() => {
    const dt = Math.min(clock.getDelta(), 0.1);
    U.uTime.value += dt;
    controls.update();
    up.set(0, 1, 0).transformDirection(camera.matrixWorldInverse);
    U.uLightView.value.copy(up);
    if (waterSurface) waterSurface.material.normalMap.offset.set(U.uTime.value * 0.012, U.uTime.value * 0.007);
    updateFish(dt, U.uTime.value);
    if (particles) {
      const a = particles.geometry.attributes.position, b = particles.userData.bounds;
      for (let i = 0; i < a.count; i++) {
        let y = a.getY(i) + dt * 0.25 * (0.3 + ((i * 37) % 10) / 10);
        if (y > b.y0 + b.h) y = b.y0;
        a.setY(i, y);
        a.setX(i, a.getX(i) + Math.sin(U.uTime.value * 0.5 + i) * dt * 0.05);
      }
      a.needsUpdate = true;
    }
    render();
    // İlk saniyelerde kare hızı düşükse kaliteyi otomatik dengeliye al
    if (!fpsChecked && state.quality === 'yuksek') {
      fpsFrames++; fpsTime += dt;
      if (fpsTime > 3) {
        fpsChecked = true;
        if (fpsFrames / fpsTime < 22) { api.setQuality('dengeli'); onQuality?.('dengeli', true); }
      }
    }
  });

  const api = {
    onAutoRotate: null,
    async setModel(m) { state.model = { ...m }; await rebuildTank(); },
    get interior() { return state.interior; },
    setSubstrate(zemin, kalinlik) { state.zemin = zemin; state.kalinlik = kalinlik; rebuildContent(); },
    setPlants(list) { state.plants = list; rebuildContent(); },
    setHardscape(list) { state.hardscape = list; rebuildContent(); },
    setFish(list) { state.fish = list; rebuildContent(); },
    setAll({ zemin, kalinlik, plants, hardscape, fish }) {
      if (zemin !== undefined) { state.zemin = zemin; state.kalinlik = kalinlik; }
      if (plants) state.plants = plants;
      if (hardscape) state.hardscape = hardscape;
      if (fish) state.fish = fish;
      rebuildContent();
    },
    shuffle() { state.seed = (state.seed * 16807 + 11) % 2147483647; rebuildContent(); return state.seed; },
    setSeed(s) { state.seed = s; },
    get seed() { return state.seed; },
    setAutoRotate(on) { controls.autoRotate = on; },
    setQuality(q) { state.quality = q; fpsChecked = true; applyQuality(); },
    get quality() { return state.quality; },
    resetView() { frame(); },
    snapshot() { render(); return renderer.domElement.toDataURL('image/png'); },
    avgSubstrate() {
      const I = state.interior;
      if (!I || state.zemin === 'yok') return 0;
      let s = 0, n = 0;
      for (let i = 0; i <= 10; i++) for (let j = 0; j <= 6; j++) { s += surfaceY(lerp(-I.L / 2, I.L / 2, i / 10), lerp(-I.W / 2, I.W / 2, j / 6)) - I.y0; n++; }
      return s / n;
    },
    has3D: foto => !!BITKI_3D[foto],
  };
  // Mobil ve dokunmatik cihazlarda dengeli kaliteyle başla
  if (matchMedia('(pointer: coarse)').matches || container.clientWidth < 700) api.setQuality('dengeli');
  return api;
}
