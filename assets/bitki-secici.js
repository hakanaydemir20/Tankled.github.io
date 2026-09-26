// Tankled bitki seçici: akvaryum hacmi, ışık, zemin ve CO₂ bilgisine göre uygun bitkileri listeler.
// Kullanım: TankledBitkiSecici.mount(elemen, { litre }) — assets/bitkiler-data.js'ten sonra yüklenmelidir.
(function () {
  const PHOTO_BASE = '../assets/bitkiler/';
  const PLANTS_PAGE = '../bitkiler/';

  // Bitkinin ihtiyaç duyduğu en düşük ışık (lümen / litre)
  const LIGHT_MIN = { 'Düşük': 0, 'Düşük–orta': 0, 'Orta': 30, 'Orta–yüksek': 40, 'Yüksek': 50 };
  const tankLevel = lmL => lmL < 30 ? 'Düşük' : lmL < 50 ? 'Orta' : 'Yüksek';

  // tur: eşleştirme kuralını belirler
  //   besleyici = tüm bitkiler için uygun
  //   kil       = besin tutar, kökten beslenenlere iyi; tane iri olduğu için halı zor yayılır
  //   kum       = besin içermez; kökten beslenenlere tablet, halıya ince tane + tablet gerekir
  //   iri       = çakıl/taş; halı bitkileri tutunamaz, kökten beslenenlere tablet gerekir
  //   yok       = yalnızca bağlanan ve yüzen bitkiler
  // sert: true = suyu sertleştirir, pH'ı yükseltir
  const SUBSTRATES = [
    { grup: 'Besleyici zeminler', items: [
      { value: 'aquasoil', tur: 'besleyici', label: 'Akvaryum toprağı (aquasoil)',
        desc: 'Besin içeren granül toprak. Halı ve kökten beslenen bitkiler için en iyi seçim; suyu hafif yumuşatır.' },
      { value: 'katmanli', tur: 'besleyici', label: 'Besleyici alt katman + kum/çakıl üst katman',
        desc: 'Altta besleyici katman, üstte kum ya da çakıl. Hem bitki beslenir hem doğal bir görünüm elde edilir.' },
      { value: 'kil', tur: 'kil', label: 'Pişmiş kil granül (Flourite vb.)',
        desc: 'Demir içeren, çözünmeyen kil granül. Kökten beslenen bitkilere iyi gelir, uzun yıllar kullanılır.' },
    ] },
    { grup: 'Kumlar', items: [
      { value: 'dere-kumu', tur: 'kum', label: 'Dere kumu',
        desc: 'Doğal, yuvarlak taneli kum. Besin içermez; kökten beslenen bitkilere tablet gübre verin.' },
      { value: 'silis', tur: 'kum', label: 'Silis (kuvars) kumu',
        desc: 'Suyu etkilemeyen, temiz kum. Besin içermez; kökten beslenen bitkilere tablet gübre verin.' },
      { value: 'bazalt', tur: 'kum', label: 'Siyah bazalt kumu',
        desc: 'Suyu etkilemeyen koyu renkli kum; bitkilerin rengini öne çıkarır. Besin içermez.' },
      { value: 'renkli-kum', tur: 'kum', label: 'Renkli / dekoratif kum',
        desc: 'Boyalı dekoratif kum. Besin içermez; bitki yetiştirmek için tablet gübre gerekir.' },
      { value: 'mercan', tur: 'kum', sert: true, label: 'Mercan / aragonit kumu',
        desc: 'Suyu sertleştirir ve pH’ı 8’in üzerine çıkarır. Yumuşak su seven bitkiler için uygun değildir.' },
    ] },
    { grup: 'Çakıl ve taş', items: [
      { value: 'cakil', tur: 'iri', label: 'Akvaryum / dere çakılı',
        desc: 'İri taneli çakıl. Halı bitkileri tutunamaz; kökten beslenenlere tablet gübre verin.' },
      { value: 'lav', tur: 'iri', label: 'Lav kırığı (volkanik taş)',
        desc: 'Gözenekli, hafif volkanik taş; bakteriler ve kökler için iyi bir yuva. Halı bitkileri için fazla iri.' },
      { value: 'ponza', tur: 'iri', label: 'Ponza taşı',
        desc: 'Çok hafif, gözenekli taş. Genelde alt katman olarak kullanılır; halı bitkileri için fazla iri.' },
    ] },
    { grup: 'Diğer', items: [
      { value: 'yok', tur: 'yok', label: 'Zemin yok (çıplak cam)',
        desc: 'Yalnızca taşa/kütüğe bağlanan ve yüzen bitkiler yetiştirilebilir.' },
    ] },
  ];
  const SUBSTRATE = Object.fromEntries(SUBSTRATES.flatMap(g => g.items).map(s => [s.value, s]));
  const phMax = p => parseFloat(String(p.bilgi[2]).split('–').pop().replace(',', '.'));

  const LEAF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 5-14 14-14 0 9-6 14-14 14z"/><path d="M5 19 14 10"/></svg>';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (n, d = 0) => n.toLocaleString('tr-TR', { maximumFractionDigits: d });

  function match({ litre, lumen, zemin, co2 }) {
    const lmL = lumen / litre;
    const level = tankLevel(lmL);
    const uygun = [], dikkat = [];

    (window.TANKLED_BITKILER || []).forEach(cat => cat.plants.forEach(p => {
      if (!p.zemin) return; // paludaryum (kara) bitkileri akvaryuma önerilmez
      const light = p.bilgi[0], co2Need = p.bilgi[4];
      if (lmL < LIGHT_MIN[light]) return;
      if (co2Need === 'Şart' && !co2) return;
      const sub = SUBSTRATE[zemin] || SUBSTRATE.aquasoil;
      if (sub.tur === 'yok' && p.zemin !== 'serbest') return;
      if (sub.tur === 'iri' && p.zemin === 'hali') return;

      const notes = [];
      if (co2Need === 'Önerilir' && !co2) notes.push('CO₂ ile daha iyi gelişir');
      if ((sub.tur === 'kum' || sub.tur === 'iri') && p.zemin === 'kok') notes.push('Köke tablet gübre verin');
      if (sub.tur === 'kum' && p.zemin === 'hali') notes.push('İnce kum ve kök tableti ister; aquasoil daha iyi sonuç verir');
      if (sub.tur === 'kil' && p.zemin === 'hali') notes.push('Tane iri olduğu için halı yavaş yayılır');
      if (sub.sert && phMax(p) < 8) notes.push('Mercan kumu pH’ı yükseltir; bu bitki daha yumuşak suyu sever');
      if (litre < 40 && p.buyuk) notes.push('Bu hacim için büyük kalabilir');
      if (lmL >= 50 && light === 'Düşük') notes.push('Güçlü ışıkta yosunlanabilir; gölgeye yerleştirin');

      (notes.length ? dikkat : uygun).push({ p, cat, notes });
    }));

    const warnings = [];
    if (lmL >= 50 && !co2) warnings.push('Işığınız güçlü ama CO₂ yok: bu dengesizlik yosun riskini artırır. Işığı kısmayı ya da CO₂ eklemeyi düşünün.');
    if ((SUBSTRATE[zemin] || {}).sert) warnings.push('Mercan / aragonit kumu suyu sertleştirir ve pH’ı yükseltir. Çoğu akvaryum bitkisi yumuşak suyu sever; bitkili akvaryumda nötr bir zemin tercih edin.');
    if (lmL < 15) warnings.push('Işığınız çok zayıf: bitkiler zor büyür. En az 20 lm/L önerilir.');
    return { lmL, level, uygun, dikkat, warnings };
  }

  const CSS = `
  .bs{display:grid;gap:18px}
  .bs-form{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
  .bs-field{display:grid;gap:6px;font-size:13px;color:var(--muted);min-width:0}
  .bs-field input,.bs-field select{width:100%;min-width:0;background:var(--cream);border:1.5px solid rgba(67,96,63,.15);border-radius:14px;
    color:var(--ink);font-family:inherit;font-size:16px;font-weight:500;padding:11px 13px;min-height:50px;transition:border-color .25s}
  .bs-field input:focus,.bs-field select:focus{outline:none;border-color:var(--green)}
  .bs-hint{font-size:12px;color:var(--muted)}
  .bs-toggle{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  .bs-toggle label{position:relative;cursor:pointer}
  .bs-toggle input{position:absolute;opacity:0;pointer-events:none}
  .bs-toggle span{display:grid;place-items:center;min-height:50px;border-radius:14px;border:1.5px solid rgba(67,96,63,.15);background:var(--cream);
    font-size:15px;font-weight:500;color:var(--ink);transition:all .2s}
  .bs-toggle input:checked + span{background:var(--green);border-color:var(--green);color:var(--on-green)}
  .bs-toggle input:focus-visible + span{outline:2px solid var(--green);outline-offset:2px}
  .bs-summary{background:var(--green);color:var(--on-green);border-radius:var(--radius-sm);padding:16px 20px;display:flex;flex-wrap:wrap;gap:6px 22px;align-items:baseline}
  .bs-summary b{font-size:22px;font-weight:700}
  .bs-summary span{font-size:13px;color:var(--on-green-muted)}
  .bs-warn{background:rgba(203,185,143,.25);color:#6b5b30;border-radius:14px;padding:12px 16px;font-size:13.5px}
  .bs-empty{color:var(--muted);font-size:14px;text-align:center;padding:14px}
  .bs-group h4{font-size:15px;font-weight:600;color:var(--green-dark);margin-bottom:10px;display:flex;align-items:center;gap:8px}
  .bs-group h4 small{font-size:12px;font-weight:600;background:rgba(67,96,63,.12);border-radius:100px;padding:1px 9px;color:var(--green-deep)}
  .bs-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
  .bs-item{display:grid;grid-template-columns:52px 1fr;gap:12px;align-items:center;background:var(--cream);border-radius:14px;padding:9px;
    transition:background .2s;color:inherit}
  .bs-item:hover{background:rgba(92,122,90,.14)}
  .bs-photo{width:52px;height:52px;border-radius:10px;overflow:hidden;background:rgba(92,122,90,.14);display:grid;place-items:center;color:var(--green)}
  .bs-photo img{width:100%;height:100%;object-fit:cover}
  .bs-photo svg{width:26px;height:26px;opacity:.7}
  .bs-name{font-size:14px;font-weight:600;color:var(--green-dark);line-height:1.3}
  .bs-meta{font-size:12px;color:var(--muted);line-height:1.4}
  .bs-note{font-size:12px;color:#7a6a3f;line-height:1.4;margin-top:2px}
  @media(max-width:560px){ .bs-form{grid-template-columns:1fr 1fr;gap:10px} .bs-wide{grid-column:1 / -1} .bs-list{grid-template-columns:1fr} }
  `;

  function injectCss() {
    if (document.getElementById('bs-css')) return;
    const st = document.createElement('style');
    st.id = 'bs-css';
    st.textContent = CSS;
    document.head.appendChild(st);
  }

  let uid = 0;
  function mount(root, opts = {}) {
    injectCss();
    const id = 'bs' + (++uid);
    root.innerHTML = `
      <div class="bs">
        <div class="bs-form">
          <label class="bs-field">Akvaryum hacmi (litre)
            <input type="number" id="${id}-l" min="0" step="1" inputmode="decimal" placeholder="ör. 60">
          </label>
          <label class="bs-field">Işık gücü (lümen)
            <input type="number" id="${id}-lm" min="0" step="50" inputmode="decimal" placeholder="ör. 1500">
          </label>
          <label class="bs-field bs-wide">Zemin tipi
            <select id="${id}-z">${SUBSTRATES.map(g => `<optgroup label="${g.grup}">${g.items.map(s => `<option value="${s.value}">${s.label}</option>`).join('')}</optgroup>`).join('')}</select>
            <span class="bs-hint" id="${id}-zd"></span>
          </label>
          <div class="bs-field bs-wide">CO₂ sistemi
            <div class="bs-toggle" role="radiogroup" aria-label="CO₂ sistemi">
              <label><input type="radio" name="${id}-co2" value="yok" checked><span>Yok</span></label>
              <label><input type="radio" name="${id}-co2" value="var"><span>Var</span></label>
            </div>
          </div>
        </div>
        <p class="bs-hint">Işık gücünü armatürünüzün kutusunda ya da ürün sayfasında “lm” olarak bulabilirsiniz.</p>
        <div id="${id}-out" aria-live="polite"></div>
      </div>`;

    const $ = s => root.querySelector(s);
    const litreEl = $(`#${id}-l`), lumenEl = $(`#${id}-lm`), zeminEl = $(`#${id}-z`), out = $(`#${id}-out`);
    let litreTouched = false;

    const item = ({ p, cat, notes }) => `
      <a class="bs-item" href="${PLANTS_PAGE}#p-${p.foto}">
        <span class="bs-photo"><img src="${PHOTO_BASE}${p.foto}.jpg" alt="" loading="lazy"></span>
        <span>
          <span class="bs-name">${esc(p.ad)}</span><br>
          <span class="bs-meta">${esc(cat.tab)} · ${esc(p.zorluk)} · ${esc(p.bilgi[5])}</span>
          ${notes.map(n => `<span class="bs-note">• ${esc(n)}</span>`).join('<br>')}
        </span>
      </a>`;

    let lastKey = null;
    function render() {
      const litre = parseFloat(litreEl.value) || 0, lumen = parseFloat(lumenEl.value) || 0;
      const co2Val = root.querySelector(`input[name="${id}-co2"]:checked`).value;
      // Değerler değişmediyse listeyi yeniden çizme (aksi halde "change" olayı tıklanan bağlantıyı siler)
      const key = [litre, lumen, zeminEl.value, co2Val].join('|');
      if (key === lastKey) return;
      lastKey = key;
      root.querySelector(`#${id}-zd`).textContent = (SUBSTRATE[zeminEl.value] || {}).desc || '';
      if (litre <= 0 || lumen <= 0) {
        out.innerHTML = '<p class="bs-empty">Akvaryum hacmini ve ışık gücünü girin; uygun bitkiler burada listelenecek.</p>';
        return;
      }
      const co2 = co2Val === 'var';
      const r = match({ litre, lumen, zemin: zeminEl.value, co2 });
      const group = (title, list) => list.length ? `
        <div class="bs-group"><h4>${title} <small>${list.length}</small></h4><div class="bs-list">${list.map(item).join('')}</div></div>` : '';

      out.innerHTML = `
        <div class="bs" style="gap:14px">
          <div class="bs-summary"><b>${fmt(r.lmL)} lm/L</b><span>Işık seviyeniz: ${r.level}</span><span>${fmt(r.uygun.length + r.dikkat.length)} uygun bitki</span></div>
          ${r.warnings.map(w => `<div class="bs-warn">${esc(w)}</div>`).join('')}
          ${group('Uygun bitkiler', r.uygun)}
          ${group('Dikkat ederek kullanılabilir', r.dikkat)}
          ${r.uygun.length + r.dikkat.length ? '' : '<p class="bs-empty">Bu koşullara uyan bitki bulunamadı. Işığı artırmayı, CO₂ eklemeyi ya da besleyici zemin kullanmayı deneyin.</p>'}
        </div>`;
      out.querySelectorAll('.bs-photo img').forEach(img => {
        const fallback = () => { img.parentElement.innerHTML = LEAF; };
        if (img.complete && img.naturalWidth === 0) fallback();
        else img.addEventListener('error', fallback);
      });
    }

    litreEl.addEventListener('input', () => { litreTouched = true; });
    root.addEventListener('input', render);
    root.addEventListener('change', render);

    const api = {
      // Hesaplama sayfası hacmi otomatik doldurur; kullanıcı elle değiştirdiyse dokunmaz.
      setLitre(v) {
        if (litreTouched) return;
        litreEl.value = v > 0 ? Math.round(v * 10) / 10 : '';
        render();
      },
    };
    if (opts.litre) api.setLitre(opts.litre); else render();
    return api;
  }

  window.TankledBitkiSecici = { mount, match, SUBSTRATES };
})();
