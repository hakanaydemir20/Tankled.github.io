// Tankled 3D akvaryum sahnesi.
// Birim: 1 = 1 cm. x = uzunluk, y = yükseklik, z = derinlik (ön yüz +z).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

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

function disposeTree(obj) {
  obj.traverse(o => {
    if (o.geometry) o.geometry.dispose();
    if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => { m.map?.dispose(); m.bumpMap?.dispose(); m.dispose(); });
  });
}

/* ---------- Zemin görünümleri ---------- */

// grain: tane yarıçapı (doku pikseli), tile: dokunun kapladığı cm, tas: üstüne serpilen taşlar [min, max] cm
const ZEMIN_GORUNUM = {
  aquasoil:     { base: '#2b2420', palette: ['#3a302a', '#1f1a17', '#4a3d33', '#2e2622', '#56463a'], grain: 3.2, tile: 8 },
  katmanli:     { base: '#c9b28a', palette: ['#d8c39c', '#b89d72', '#e3d4b3', '#a88d64', '#8d7a5c'], grain: 1.6, tile: 6, alt: 'aquasoil' },
  kil:          { base: '#7a3f2a', palette: ['#8c4a31', '#6b3322', '#9a5a3c', '#5e2e1f', '#a8653f'], grain: 3.4, tile: 8 },
  'dere-kumu':  { base: '#c9b28a', palette: ['#d8c39c', '#b89d72', '#e3d4b3', '#a88d64', '#8d7a5c'], grain: 1.6, tile: 6 },
  silis:        { base: '#e9e4d8', palette: ['#f4f1ea', '#dcd6c8', '#ffffff', '#cfc8b8', '#e2dccd'], grain: 1.4, tile: 6 },
  bazalt:       { base: '#262626', palette: ['#1b1b1b', '#333333', '#2a2a2a', '#444444', '#3a3a3a'], grain: 1.5, tile: 6 },
  'renkli-kum': { base: '#d9c8a8', palette: ['#e05a5a', '#4f86d9', '#f2c14e', '#5bbf6a', '#b86bd6', '#f28ec0', '#ffffff'], grain: 1.9, tile: 6 },
  mercan:       { base: '#efe9df', palette: ['#f7f3ec', '#e8dfd0', '#ffffff', '#e3d5c2', '#f0c9b5'], grain: 2.6, tile: 7 },
  cakil:        { base: '#8f887c', palette: ['#a39b8e', '#7c756a', '#b8b0a2', '#6b655c', '#9c8a74'], grain: 4, tile: 12, tas: [0.7, 1.5],
                  tasRenk: ['#a39b8e', '#7c756a', '#b8b0a2', '#6b655c', '#9c8a74', '#c2b7a3'] },
  lav:          { base: '#4a2620', palette: ['#5e2e24', '#3b2420', '#6f3a2c', '#2a1a17', '#7a4030'], grain: 4, tile: 12, tas: [0.8, 1.9],
                  tasRenk: ['#6b3326', '#3b2420', '#7a3b2c', '#4f2a22', '#2e1d19'] },
  ponza:        { base: '#d3ccbd', palette: ['#dcd6c9', '#c8c0af', '#e6e1d6', '#bdb4a2', '#d9d2c2'], grain: 4, tile: 12, tas: [0.6, 1.4],
                  tasRenk: ['#dcd6c9', '#c8c0af', '#e6e1d6', '#bdb4a2', '#cfc6b3'] },
  yok:          null,
};

const textureCache = new Map();
function grainTexture(key) {
  if (textureCache.has(key)) return textureCache.get(key);
  const g = ZEMIN_GORUNUM[key];
  const size = 256, c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  ctx.fillStyle = g.base;
  ctx.fillRect(0, 0, size, size);
  const r = rng(hashStr(key));
  const n = Math.round((size * size) / (g.grain * g.grain * 2.2));
  for (let i = 0; i < n; i++) {
    const x = r() * size, y = r() * size, rad = g.grain * (0.55 + r() * 0.9);
    ctx.fillStyle = g.palette[Math.floor(r() * g.palette.length)];
    ctx.beginPath();
    // kenarlarda da çiz ki doku dikişsiz tekrarlansın
    for (const [dx, dy] of [[0, 0], [size, 0], [-size, 0], [0, size], [0, -size]]) {
      ctx.moveTo(x + dx + rad, y + dy);
      ctx.ellipse(x + dx, y + dy, rad, rad * (0.7 + r() * 0.3), r() * Math.PI, 0, Math.PI * 2);
    }
    ctx.fill();
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  textureCache.set(key, tex);
  return tex;
}

/* ---------- Bitki modelleri ---------- */

// tip: rozet | serit | govde | hali | yosun | yuzen | top
// taban: 'tas' | 'kutuk' → epifit bitkiler bir taş ya da kütük üzerinde gösterilir
const BITKI_3D = {
  'anubias-nana':        { tip: 'rozet', adet: 9, boy: [4, 7], en: 0.55, egim: [35, 70], renk: '#2f5a2c', uc: '#3f7036', taban: 'tas' },
  'anubias-barteri':     { tip: 'rozet', adet: 9, boy: [10, 16], en: 0.5, egim: [25, 60], renk: '#2f5a2c', uc: '#3f7036', taban: 'tas' },
  'anubias-coffeefolia': { tip: 'rozet', adet: 9, boy: [8, 12], en: 0.5, egim: [30, 60], renk: '#34552c', uc: '#7a4a2b', taban: 'tas' },
  'java-egreltisi':      { tip: 'rozet', adet: 11, boy: [12, 20], en: 0.17, egim: [10, 40], renk: '#3a6630', uc: '#5b8a3f', taban: 'kutuk' },
  'bolbitis':            { tip: 'rozet', adet: 10, boy: [10, 16], en: 0.32, egim: [20, 55], renk: '#23462a', uc: '#2f5a33', taban: 'kutuk' },
  'java-yosunu':         { tip: 'yosun', boy: [3, 5], renk: '#3e6b2e', uc: '#5a8a3a', taban: 'kutuk' },
  'christmas-yosunu':    { tip: 'yosun', boy: [3, 5], renk: '#355f2a', uc: '#4f8036', taban: 'kutuk' },
  'cryptocoryne-wendtii':{ tip: 'rozet', adet: 12, boy: [7, 11], en: 0.3, egim: [20, 55], renk: '#55572c', uc: '#7a4a2a' },
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
  'pogostemon-helferi':  { tip: 'rozet', adet: 16, boy: [3, 5], en: 0.2, egim: [55, 85], renk: '#5d8f36', uc: '#79aa45' },
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
  const geo = new THREE.ShapeGeometry(shape, 6);
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i), x = pos.getX(i);
    pos.setZ(i, curl * y * y + (wave ? Math.sin(y * 18) * 0.02 : 0) + Math.abs(x) * 0.15);
    colors[i * 3] = colors[i * 3 + 1] = colors[i * 3 + 2] = y; // renk geçişi için 0..1
  }
  geo.setAttribute('t', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  leafCache.set(key, geo);
  return geo;
}

// Taban → uç renk geçişi yapan yaprak malzemesi
function leafMaterial(base, tip) {
  const m = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: 0.65, metalness: 0 });
  const c0 = new THREE.Color(base), c1 = new THREE.Color(tip);
  m.onBeforeCompile = sh => {
    sh.uniforms.c0 = { value: c0 };
    sh.uniforms.c1 = { value: c1 };
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nattribute vec3 t;\nvarying float vT;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvT = t.x;');
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\nuniform vec3 c0; uniform vec3 c1; varying float vT;')
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', 'vec4 diffuseColor = vec4( mix(c0, c1, smoothstep(0.1, 1.0, vT)) * diffuse, opacity );');
  };
  return m;
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
  return mesh;
}

const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _v = new THREE.Vector3(), _s = new THREE.Vector3();
function mat4(x, y, z, rx, ry, rz, sx, sy = sx, sz = sx) {
  return new THREE.Matrix4().compose(_v.set(x, y, z), _q.setFromEuler(_e.set(rx, ry, rz, 'YXZ')), _s.set(sx, sy, sz));
}

function rockMesh(r, size, color = '#7d7a72') {
  const geo = new THREE.IcosahedronGeometry(1, 1);
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const k = 0.75 + r() * 0.45;
    pos.setXYZ(i, pos.getX(i) * k, pos.getY(i) * k * 0.7, pos.getZ(i) * k);
  }
  geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color, roughness: 0.95, flatShading: true }));
  m.scale.setScalar(size);
  return m;
}

function woodMesh(r, len) {
  const g = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: '#5a4030', roughness: 0.9 });
  const main = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.4, len, 7), mat);
  main.rotation.z = Math.PI / 2 - 0.35;
  main.position.y = len * 0.15;
  g.add(main);
  const br = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.8, len * 0.45, 6), mat);
  br.position.set(len * 0.1, len * 0.3, 0.3);
  br.rotation.z = -0.6;
  g.add(br);
  g.rotation.y = r() * Math.PI;
  return g;
}

// Bir bitki kümesi oluşturur. maxH: suyun altında kalabileceği en fazla yükseklik (cm)
function buildPlant(foto, r, maxH) {
  const d = BITKI_3D[foto];
  const g = new THREE.Group();
  if (!d) return g;
  const mat = leafMaterial(d.renk, d.uc || d.renk);
  let baseY = 0;

  if (d.taban === 'tas') {
    const rock = rockMesh(r, 2.2 + r() * 1.5);
    rock.position.y = 0.6;
    g.add(rock);
    baseY = 1.8;
  } else if (d.taban === 'kutuk') {
    const w = woodMesh(r, 9 + r() * 5);
    g.add(w);
    baseY = 2.2;
  }

  if (d.tip === 'rozet') {
    const mats = [];
    for (let i = 0; i < d.adet; i++) {
      const len = Math.min(between(r, d.boy), maxH * 0.9);
      const tilt = THREE.MathUtils.degToRad(between(r, d.egim));
      mats.push(mat4((r() - 0.5) * 0.8, baseY, (r() - 0.5) * 0.8, tilt, r() * Math.PI * 2, (r() - 0.5) * 0.3, len));
    }
    g.add(instanced(leafGeometry(d.en, 0.25), mat, mats, 0.15, r));
  } else if (d.tip === 'serit') {
    const mats = [], spread = d.yayilim || 1.2;
    for (let i = 0; i < d.adet; i++) {
      const len = Math.min(between(r, d.boy), maxH * 0.95);
      mats.push(mat4((r() - 0.5) * spread * 2, 0, (r() - 0.5) * spread, THREE.MathUtils.degToRad(r() * 18), r() * Math.PI * 2, 0, d.en, len, len));
    }
    // şerit: genişliği sabit (cm), boyu ölçeklenir → genişliği 1 birimlik yaprağı x ekseninde en kadar ölçekle
    const geo = leafGeometry(1, 0.18, !!d.dalga);
    const mesh = instanced(geo, mat, mats.map(m => {
      const p = new THREE.Vector3(), q = new THREE.Quaternion(), s = new THREE.Vector3();
      m.decompose(p, q, s);
      return new THREE.Matrix4().compose(p, q, new THREE.Vector3(d.en, s.y, s.y * 0.6));
    }), 0.15, r);
    g.add(mesh);
  } else if (d.tip === 'govde') {
    const stemMats = [], leafMats = [], spread = d.yayilim || 2.6;
    for (let s = 0; s < d.sap; s++) {
      const h = Math.min(between(r, d.boy), maxH * 0.92);
      const sx = (r() - 0.5) * spread * 2, sz = (r() - 0.5) * spread;
      const lean = (r() - 0.5) * 0.12, leanDir = r() * Math.PI * 2;
      stemMats.push(mat4(sx + Math.sin(leanDir) * lean * h / 2, h / 2, sz + Math.cos(leanDir) * lean * h / 2, lean * Math.cos(leanDir), 0, -lean * Math.sin(leanDir), 1, h, 1));
      const nodes = Math.max(2, Math.floor(h / d.ara));
      for (let n = 1; n <= nodes; n++) {
        const y = (n / nodes) * h, k = y / h;
        const x = sx + Math.sin(leanDir) * lean * y, z = sz + Math.cos(leanDir) * lean * y;
        const size = d.yBoy * (0.55 + 0.45 * Math.min(1, k * 2.5)) * (k > 0.92 ? 0.7 : 1);
        for (let l = 0; l < d.yaprak; l++) {
          const yaw = (l / d.yaprak) * Math.PI * 2 + n * 0.9;
          leafMats.push(mat4(x, y, z, THREE.MathUtils.degToRad(55 + r() * 25 - k * 15), yaw, 0, size));
        }
      }
    }
    const stemMat = new THREE.MeshStandardMaterial({ color: d.renk, roughness: 0.8 });
    g.add(instanced(new THREE.CylinderGeometry(0.1, 0.13, 1, 5), stemMat, stemMats, 0.1, r));
    // yaprak rengi yüksekliğe göre tabandan uca geçsin: her yaprağın rengini sapa göre ayarla
    const leaves = instanced(leafGeometry(d.yEn * 2, 0.15), leafMaterial(d.renk, d.renk), leafMats, 0.1, r);
    const tint = new THREE.Color(), c0 = new THREE.Color(d.renk), c1 = new THREE.Color(d.uc);
    leafMats.forEach((m, i) => {
      const y = new THREE.Vector3().setFromMatrixPosition(m).y;
      const k = Math.pow(Math.min(1, y / (maxH * 0.8)), 1.5);
      tint.copy(c0).lerp(c1, k);
      leaves.setColorAt(i, new THREE.Color(tint.r / c0.r || 1, tint.g / c0.g || 1, tint.b / c0.b || 1));
    });
    g.add(leaves);
  } else if (d.tip === 'hali') {
    // hali ayrıca büyük bir alana yayılır; burada yalnızca küme merkezi döner, yayılım sahnede yapılır
    g.userData.hali = d;
  } else if (d.tip === 'yosun') {
    const mossMat = new THREE.MeshStandardMaterial({ color: d.renk, roughness: 1, flatShading: true });
    const n = 10 + Math.floor(r() * 6);
    for (let i = 0; i < n; i++) {
      const geo = new THREE.IcosahedronGeometry(1, 1);
      const pos = geo.attributes.position;
      for (let j = 0; j < pos.count; j++) {
        const k = 0.8 + r() * 0.4;
        pos.setXYZ(j, pos.getX(j) * k, pos.getY(j) * k, pos.getZ(j) * k);
      }
      geo.computeVertexNormals();
      const m = new THREE.Mesh(geo, i % 3 ? mossMat : new THREE.MeshStandardMaterial({ color: d.uc, roughness: 1, flatShading: true }));
      const s = between(r, d.boy) * 0.45;
      m.scale.set(s, s * 0.6, s);
      m.position.set((r() - 0.5) * 6, baseY + s * 0.2 + r() * 1.2, (r() - 0.5) * 3);
      g.add(m);
    }
  } else if (d.tip === 'top') {
    const geo = new THREE.IcosahedronGeometry(1, 3);
    const pos = geo.attributes.position;
    for (let j = 0; j < pos.count; j++) {
      const k = 1 + (r() - 0.5) * 0.12;
      pos.setXYZ(j, pos.getX(j) * k, pos.getY(j) * k, pos.getZ(j) * k);
    }
    geo.computeVertexNormals();
    const n = 1 + Math.floor(r() * 2);
    for (let i = 0; i < n; i++) {
      const s = between(r, d.boy);
      const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: d.renk, roughness: 1, flatShading: true }));
      m.scale.setScalar(s);
      m.position.set(i * s * 2.1, s * 0.9, (r() - 0.5) * 2);
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
  const geo = new THREE.CircleGeometry(0.5, 12);
  geo.scale(d.yuvarlak, 1, 1);
  geo.translate(0, 0.5, 0);
  const t = new Float32Array(geo.attributes.position.count * 3).fill(0.5);
  geo.setAttribute('t', new THREE.BufferAttribute(t, 3));
  g.add(instanced(geo, leafMaterial(d.renk, d.uc), mats, 0.2, r));
  if (d.kok) {
    const rootMat = new THREE.MeshStandardMaterial({ color: '#d9cfb8', roughness: 1 });
    const rm = [];
    for (let i = 0; i < d.yaprak; i++) {
      const L = 4 + r() * 6;
      rm.push(mat4((r() - 0.5) * 7, -L / 2, (r() - 0.5) * 7, (r() - 0.5) * 0.2, 0, (r() - 0.5) * 0.2, 1, L, 1));
    }
    g.add(instanced(new THREE.CylinderGeometry(0.03, 0.03, 1, 3), rootMat, rm, 0.1, r));
  }
  return g;
}

/* ---------- Sahne ---------- */

export function createAquarium(container, { onModelError } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.5, 5000);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.9;
  controls.maxPolarAngle = THREE.MathUtils.degToRad(95);
  controls.enablePan = false;

  scene.add(new THREE.HemisphereLight('#ffffff', '#b8a98a', 1.2));
  const sun = new THREE.DirectionalLight('#fff6e8', 1.8);
  sun.position.set(30, 120, 60);
  scene.add(sun);
  const fill = new THREE.DirectionalLight('#dfefff', 0.5);
  fill.position.set(-60, 30, 80);
  scene.add(fill);

  // Zemindeki yumuşak gölge
  const shadowTex = (() => {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const x = c.getContext('2d'), gr = x.createRadialGradient(64, 64, 4, 64, 64, 64);
    gr.addColorStop(0, 'rgba(40,50,35,.35)');
    gr.addColorStop(1, 'rgba(40,50,35,0)');
    x.fillStyle = gr;
    x.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  })();
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false }));
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.05;
  scene.add(floor);

  const root = new THREE.Group();
  scene.add(root);
  let tankGroup = null, contentGroup = null;

  const state = {
    model: { tip: 'kutu', L: 60, W: 30, H: 36, cam: 0.6 },
    interior: null, // { L, W, H, y0, waterTop }
    zemin: 'aquasoil', kalinlik: 5,
    plants: [], seed: 1,
  };

  /* --- Zemin yüksekliği --- */
  function surfaceY(x, z) {
    const I = state.interior;
    if (!I || state.zemin === 'yok' || !ZEMIN_GORUNUM[state.zemin]) return I ? I.y0 : 0;
    const back = THREE.MathUtils.clamp((I.W / 2 - z) / I.W, 0, 1); // 0 ön, 1 arka
    const t = state.kalinlik;
    const bumps = Math.sin(x * 0.21 + state.seed) * 0.25 + Math.sin(z * 0.33 + x * 0.07 + state.seed * 2) * 0.2;
    return I.y0 + t * (0.85 + 0.75 * back * back) + bumps * Math.min(1, t / 3);
  }

  /* --- Akvaryum gövdesi --- */
  function glassMaterial() {
    return new THREE.MeshStandardMaterial({ color: '#d7eef0', transparent: true, opacity: 0.16, roughness: 0.05, metalness: 0.1, depthWrite: false, side: THREE.DoubleSide });
  }

  function buildBoxTank() {
    const { L, W, H, cam } = state.model;
    const g = new THREE.Group();
    const glass = glassMaterial();
    const edgeMat = new THREE.LineBasicMaterial({ color: '#5f7d7a', transparent: true, opacity: 0.55 });
    const panes = [
      [L, cam, W, 0, cam / 2, 0],               // taban
      [L, H, cam, 0, H / 2, W / 2 - cam / 2],   // ön
      [L, H, cam, 0, H / 2, -W / 2 + cam / 2],  // arka
      [cam, H, W - cam * 2, L / 2 - cam / 2, H / 2, 0],
      [cam, H, W - cam * 2, -L / 2 + cam / 2, H / 2, 0],
    ];
    panes.forEach(([sx, sy, sz, x, y, z]) => {
      const geo = new THREE.BoxGeometry(sx, sy, sz);
      const m = new THREE.Mesh(geo, glass);
      m.position.set(x, y, z);
      m.renderOrder = 3;
      g.add(m);
      const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo), edgeMat);
      e.position.copy(m.position);
      e.renderOrder = 4;
      g.add(e);
    });
    // Silikon köşeler
    const sil = new THREE.MeshStandardMaterial({ color: '#2d3a36', roughness: 0.6, transparent: true, opacity: 0.55 });
    for (const [x, z] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(0.35, H - cam, 0.35), sil);
      m.position.set(x * (L / 2 - cam - 0.17), cam + (H - cam) / 2, z * (W / 2 - cam - 0.17));
      g.add(m);
    }
    state.interior = { L: L - cam * 2, W: W - cam * 2, H: H - cam, y0: cam, waterTop: H - 2 };
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
    g.add(model);
    const ic = cfg.ic;
    const y0 = cfg.icTaban ?? 0;
    state.interior = { L: ic.L, W: ic.W, H: ic.H, y0, waterTop: y0 + (cfg.su ?? ic.H - 2) };
    // Model kendi camını içermiyorsa ince bir cam kutu ekle
    if (cfg.camEkle) {
      const glass = new THREE.Mesh(new THREE.BoxGeometry(ic.L, ic.H, ic.W), glassMaterial());
      glass.position.y = y0 + ic.H / 2;
      glass.renderOrder = 3;
      g.add(glass);
    }
    return g;
  }

  /* --- İçerik: zemin, su, bitkiler --- */
  function buildSubstrate(g) {
    const I = state.interior, look = ZEMIN_GORUNUM[state.zemin];
    if (!look) return;
    const nx = 48, nz = 24;
    const top = new THREE.PlaneGeometry(I.L, I.W, nx, nz);
    top.rotateX(-Math.PI / 2);
    const pos = top.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setY(i, surfaceY(pos.getX(i), pos.getZ(i)));
    top.computeVertexNormals();
    const uv = top.attributes.uv;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / look.tile, pos.getZ(i) / look.tile);
    const tex = grainTexture(state.zemin);
    const mat = new THREE.MeshStandardMaterial({ map: tex, bumpMap: tex, bumpScale: 0.6, roughness: 1 });
    g.add(new THREE.Mesh(top, mat));

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
      const lk = ZEMIN_GORUNUM[key];
      const verts = [], uvs = [], idx = [];
      sides.forEach(pts => {
        const start = verts.length / 3;
        let run = 0;
        pts.forEach(([x, z, y], i) => {
          if (i) run += Math.hypot(x - pts[i - 1][0], z - pts[i - 1][1]);
          const yb = yFrom, yt = yTo === null ? y : Math.min(y, yTo);
          verts.push(x, yb, z, x, yt, z);
          uvs.push(run / lk.tile, yb / lk.tile, run / lk.tile, yt / lk.tile);
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
      const t = grainTexture(key);
      g.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: t, roughness: 1, side: THREE.DoubleSide })));
    };
    if (look.alt) {
      layer(look.alt, I.y0, altY);
      layer(state.zemin, altY, null);
    } else {
      layer(state.zemin, I.y0, null);
    }

    // İri zeminler: üzerine taşlar
    if (look.tas) {
      const r = rng(state.seed * 7 + 3);
      const avg = (look.tas[0] + look.tas[1]) / 2;
      const count = Math.min(5000, Math.round((I.L * I.W) / (avg * avg) * 0.55));
      const geo = new THREE.IcosahedronGeometry(1, 0);
      const mats = [];
      for (let i = 0; i < count; i++) {
        const s = between(r, look.tas) / 2;
        const x = (r() - 0.5) * (I.L - s * 2), z = (r() - 0.5) * (I.W - s * 2);
        mats.push(mat4(x, surfaceY(x, z) + s * 0.1, z, r() * 3, r() * 3, r() * 3, s * (0.8 + r() * 0.5), s * (0.55 + r() * 0.3), s * (0.8 + r() * 0.5)));
      }
      const mesh = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ roughness: 0.95, flatShading: true }), mats.length);
      const col = new THREE.Color();
      mats.forEach((m, i) => {
        mesh.setMatrixAt(i, m);
        mesh.setColorAt(i, col.set(look.tasRenk[Math.floor(r() * look.tasRenk.length)]));
      });
      g.add(mesh);
    }
  }

  function buildWater(g) {
    const I = state.interior;
    const h = I.waterTop - I.y0;
    const water = new THREE.Mesh(new THREE.BoxGeometry(I.L - 0.1, h, I.W - 0.1),
      new THREE.MeshStandardMaterial({ color: '#8fc9d4', transparent: true, opacity: 0.13, roughness: 0.1, depthWrite: false }));
    water.position.y = I.y0 + h / 2;
    water.renderOrder = 1;
    g.add(water);
    const surf = new THREE.Mesh(new THREE.PlaneGeometry(I.L - 0.1, I.W - 0.1),
      new THREE.MeshStandardMaterial({ color: '#bfe4ea', transparent: true, opacity: 0.35, roughness: 0.05, metalness: 0.2, depthWrite: false, side: THREE.DoubleSide }));
    surf.rotation.x = -Math.PI / 2;
    surf.position.y = I.waterTop;
    surf.renderOrder = 2;
    g.add(surf);
  }

  function buildPlants(g) {
    const I = state.interior;
    const r = rng(state.seed * 131 + 17);
    const placed = [];
    const margin = 3;

    const pickSpot = (zr, radius) => {
      let best = null, bestD = -Infinity;
      for (let t = 0; t < 24; t++) {
        const x = (r() - 0.5) * Math.max(0, I.L - radius * 2 - margin);
        const z = I.W / 2 - between(r, zr) * I.W;
        const zc = THREE.MathUtils.clamp(z, -I.W / 2 + radius + 1, I.W / 2 - radius - 1);
        const d = placed.reduce((m, p) => Math.min(m, Math.hypot(p.x - x, p.z - zc) - p.r - radius), 999);
        if (d > bestD) { bestD = d; best = { x, z: zc }; }
      }
      placed.push({ ...best, r: radius });
      return best;
    };

    // Önce iri (arka) bitkiler, sonra öndekiler yerleşsin
    const items = [];
    state.plants.forEach(({ plant, adet }) => { for (let i = 0; i < adet; i++) items.push(plant); });
    const zOf = p => zone(p.bilgi[5]).z?.[0] ?? 0;
    items.sort((a, b) => zOf(b) - zOf(a));

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
      if (zn.yuzen) zn.z = [0.05, 0.4]; // ör. Riccia: taşa bağlı halde ön bölgede gösterilir
      if (d.tip === 'hali') {
        // halı: ön bölgede geniş bir alana yayılan minik yapraklar
        const pw = Math.min(I.L * 0.45, 30), pd = Math.min(I.W * 0.35, 14);
        const c = pickSpot(zn.z, Math.min(pw, pd) / 2);
        const n = Math.min(2600, Math.round(pw * pd * 7));
        const mats = [];
        for (let i = 0; i < n; i++) {
          const a = r() * Math.PI * 2, rad = Math.sqrt(r());
          const x = THREE.MathUtils.clamp(c.x + Math.cos(a) * rad * pw / 2, -I.L / 2 + 0.5, I.L / 2 - 0.5);
          const z = THREE.MathUtils.clamp(c.z + Math.sin(a) * rad * pd / 2, -I.W / 2 + 0.5, I.W / 2 - 0.5);
          const h = r() * d.yukseklik * (1 - rad * 0.5);
          mats.push(mat4(x, surfaceY(x, z) + h, z, -Math.PI / 2 + (r() - 0.5) * 1.2, r() * Math.PI * 2, 0, d.yBoy * (0.7 + r() * 0.6)));
        }
        const geo = d.yuvarlak < 0.3 ? leafGeometry(0.15, 0.1) : new THREE.CircleGeometry(0.5, 8).scale(d.yuvarlak, 1, 1).translate(0, 0.5, 0);
        if (!geo.attributes.t) geo.setAttribute('t', new THREE.BufferAttribute(new Float32Array(geo.attributes.position.count * 3).fill(0.6), 3));
        const mesh = instanced(geo, leafMaterial(d.renk, d.uc), mats, 0.25, r);
        if (d.yuvarlak < 0.3) mats.forEach((m, i) => mesh.setMatrixAt(i, m.multiply(new THREE.Matrix4().makeRotationX(Math.PI / 2 - 0.3))));
        g.add(mesh);
        return;
      }
      const radius = d.tip === 'govde' ? 3.5 : d.tip === 'rozet' ? Math.min(between(r, d.boy) * 0.6, 12) : d.taban === 'kutuk' ? 7 : 4;
      const spot = pickSpot(zn.z || [0.3, 0.7], radius);
      const y = surfaceY(spot.x, spot.z);
      const plant = buildPlant(p.foto, r, Math.max(3, I.waterTop - y - 1));
      plant.position.set(spot.x, y - (d.taban ? 0.4 : 0.2), spot.z);
      plant.rotation.y = r() * Math.PI * 2;
      g.add(plant);
    });
  }

  function rebuildContent() {
    if (contentGroup) { root.remove(contentGroup); disposeTree(contentGroup); }
    contentGroup = new THREE.Group();
    if (state.interior) {
      buildSubstrate(contentGroup);
      buildPlants(contentGroup);
      buildWater(contentGroup);
    }
    root.add(contentGroup);
  }

  function frame() {
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y * 1.3, size.z);
    floor.scale.set(size.x * 1.6 + 10, size.z * 2.2 + 10, 1);
    controls.target.copy(center);
    const dist = maxDim / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2))) * 1.35 / Math.min(1, camera.aspect * 0.9);
    const dir = new THREE.Vector3(0.55, 0.38, 1).normalize();
    camera.position.copy(center).addScaledVector(dir, dist);
    controls.minDistance = maxDim * 0.6;
    controls.maxDistance = dist * 3;
    camera.near = Math.max(0.1, dist / 200);
    camera.far = dist * 10;
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
    rebuildContent();
    const key = [state.model.tip, state.model.L, state.model.W, state.model.H].join('|');
    if (key !== lastSizeKey) { lastSizeKey = key; frame(); }
  }

  /* --- Döngü --- */
  const resize = () => {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(container);
  resize();

  renderer.domElement.addEventListener('pointerdown', () => { controls.autoRotate = false; api.onAutoRotate?.(false); });
  renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });

  const api = {
    onAutoRotate: null,
    async setModel(m) { state.model = { ...m }; await rebuildTank(); },
    get interior() { return state.interior; },
    setSubstrate(zemin, kalinlik) { state.zemin = zemin; state.kalinlik = kalinlik; rebuildContent(); },
    setPlants(list) { state.plants = list; rebuildContent(); },
    shuffle() { state.seed = (state.seed * 16807 + 11) % 2147483647; rebuildContent(); return state.seed; },
    setSeed(s) { state.seed = s; },
    get seed() { return state.seed; },
    setAutoRotate(on) { controls.autoRotate = on; },
    resetView() { frame(); },
    snapshot() { renderer.render(scene, camera); return renderer.domElement.toDataURL('image/png'); },
    avgSubstrate() {
      const I = state.interior;
      if (!I || state.zemin === 'yok') return 0;
      let s = 0, n = 0;
      for (let i = 0; i <= 10; i++) for (let j = 0; j <= 6; j++) { s += surfaceY(lerp(-I.L / 2, I.L / 2, i / 10), lerp(-I.W / 2, I.W / 2, j / 6)) - I.y0; n++; }
      return s / n;
    },
    has3D: foto => !!BITKI_3D[foto],
  };
  return api;
}
