(function () {
  if (!window.THREE || !window.EVIDENCE) return;
  const D = window.EVIDENCE;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const state = { tumor: 0.15, insult: 0.05 };
  const canvas = document.getElementById("brain3d");
  if (!canvas) return;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0, 0.2, 7.2);

  const N = 14000;
  const pos = new Float32Array(N * 3);
  const seed = new Float32Array(N);
  const hemi = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const side = i % 2 ? 1 : -1;
    const u = Math.random(), v = Math.random();
    const th = u * Math.PI * 2;
    const ph = Math.acos(2 * v - 1);
    const r = 0.97 + Math.random() * 0.04;
    let x = Math.sin(ph) * Math.cos(th) * 0.95 * r;
    const y = Math.cos(ph) * 0.95 * r;
    const z = Math.sin(ph) * Math.sin(th) * 1.25 * r;
    x = x * 0.62 + side * 0.34;
    const g = 1 + 0.09 * Math.sin(x * 7.5) * Math.sin(y * 6.5 + 1.3) * Math.sin(z * 7);
    pos[i * 3] = x * 1.5 * g;
    pos[i * 3 + 1] = y * 1.35 * g;
    pos[i * 3 + 2] = z * 1.45 * g;
    seed[i] = Math.random();
    hemi[i] = side;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("aSeed", new THREE.BufferAttribute(seed, 1));
  geo.setAttribute("aHemi", new THREE.BufferAttribute(hemi, 1));

  const mat = new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    uniforms: {
      uTime: { value: 0 },
      uTumor: { value: state.tumor },
      uInsult: { value: state.insult },
      uPx: { value: renderer.getPixelRatio() }
    },
    vertexShader: [
      "uniform float uTime;uniform float uTumor;uniform float uInsult;uniform float uPx;",
      "attribute float aSeed;attribute float aHemi;varying vec3 vC;varying float vA;",
      "float hash(vec3 p){return fract(sin(dot(p,vec3(12.9898,78.233,37.719)))*43758.5453);}",
      "void main(){",
      "vec3 p=position;",
      "vec3 tc=vec3(1.05,.55,.35);",
      "float d=distance(p,tc);",
      "float mass=smoothstep(1.35,.0,d);",
      "float wob=sin(uTime*(1.2+aSeed*2.)+aSeed*40.)*.5+.5;",
      "p+=normalize(p+.001)*(mass*uTumor*.28+uInsult*(wob-.4)*.22);",
      "p+=vec3(sin(uTime*.6+aSeed*20.),cos(uTime*.5+aSeed*17.),sin(uTime*.4+aSeed*9.))*.012*(1.+uInsult*5.);",
      "vec3 base=vec3(.18,.83,.75);",
      "vec3 amber=vec3(.94,.69,.23);",
      "vec3 red=vec3(.94,.42,.34);",
      "vec3 c=mix(base,amber,mass*uTumor*1.4);",
      "c=mix(c,red,clamp(uInsult*(.35+.65*wob)*(.4+.6*(1.-mass*.0)),0.,1.));",
      "vC=c;vA=.85+.5*(mass*uTumor)+.25*uInsult*wob;",
      "vec4 mv=modelViewMatrix*vec4(p,1.);",
      "gl_PointSize=(3.4+mass*uTumor*3.+uInsult*1.6)*uPx*(5./-mv.z);",
      "gl_Position=projectionMatrix*mv;",
      "}"
    ].join("\n"),
    fragmentShader: [
      "varying vec3 vC;varying float vA;",
      "void main(){vec2 c=gl_PointCoord-.5;float d=length(c);if(d>.5)discard;",
      "float a=smoothstep(.5,.0,d)*vA;gl_FragColor=vec4(vC,a);}"
    ].join("\n")
  });
  const brain = new THREE.Points(geo, mat);
  brain.position.y = 0.55;
  scene.add(brain);

  const st = { ry: 0.6, rx: 0.1, drag: false, lx: 0, ly: 0, auto: !reduce, visible: true };
  canvas.addEventListener("pointerdown", (e) => { st.drag = true; st.auto = false; st.lx = e.clientX; st.ly = e.clientY; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener("pointerup", () => { st.drag = false; });
  canvas.addEventListener("pointermove", (e) => {
    if (!st.drag) return;
    st.ry += (e.clientX - st.lx) * 0.007;
    st.rx = Math.max(-0.9, Math.min(0.9, st.rx + (e.clientY - st.ly) * 0.007));
    st.lx = e.clientX;
    st.ly = e.clientY;
  });
  new IntersectionObserver((en) => { st.visible = en[0].isIntersecting; }).observe(canvas);
  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  addEventListener("resize", resize);
  resize();

  const target = { tumor: state.tumor, insult: state.insult };
  const sT = document.getElementById("sTumor");
  const sI = document.getElementById("sInsult");
  const readout = document.getElementById("readout");
  const tag = document.getElementById("stateTag");

  function describe() {
    const t = target.tumor, i = target.insult;
    let head, body;
    if (t < 0.25 && i < 0.25) {
      head = "Reserve intact";
      body = "No major tumor effect and little operative load. The brain sits near its baseline.";
    } else if (t >= 0.25 && i < 0.25) {
      head = "First hit only";
      body = "Mass effect, edema and local inflammation reduce reserve. Cognition was impaired before surgery in 8 of 8 studies that tested it.";
    } else if (t < 0.25 && i >= 0.25) {
      head = "Second hit on a healthy brain";
      body = "New diffusion-weighted lesions followed 18.8% to 45.7% of resections, and S100B, GFAP and NfL rose after surgery.";
    } else {
      head = "Both hits";
      body = "The tumor lowers reserve and surgery adds injury. No core study has tested whether the two hits interact, which is the main gap this review names.";
    }
    tag.textContent = head;
    readout.textContent = body;
  }
  function bind(el, key) {
    el.addEventListener("input", () => {
      target[key] = Number(el.value) / 100;
      document.querySelectorAll(".preset").forEach((b) => b.classList.remove("on"));
      describe();
    });
  }
  bind(sT, "tumor");
  bind(sI, "insult");
  document.querySelectorAll(".preset").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll(".preset").forEach((o) => o.classList.toggle("on", o === b));
    target.tumor = Number(b.dataset.t) / 100;
    target.insult = Number(b.dataset.i) / 100;
    sT.value = b.dataset.t;
    sI.value = b.dataset.i;
    describe();
  }));
  describe();

  let t = 0;
  function frame() {
    requestAnimationFrame(frame);
    if (!st.visible || !canvas.clientWidth) return;
    t += 0.016;
    state.tumor += (target.tumor - state.tumor) * 0.06;
    state.insult += (target.insult - state.insult) * 0.06;
    mat.uniforms.uTime.value = t;
    mat.uniforms.uTumor.value = state.tumor;
    mat.uniforms.uInsult.value = state.insult;
    if (st.auto) st.ry += 0.003;
    brain.rotation.y = st.ry;
    brain.rotation.x = st.rx;
    renderer.render(scene, camera);
  }
  frame();

  const rowsEl = document.getElementById("barRows");
  const chips = document.getElementById("chips");
  const listEl = document.getElementById("studyList");
  let col = -1;
  D.cols.forEach((name, j) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.textContent = name;
    b.addEventListener("click", () => select(col === j ? -1 : j));
    chips.appendChild(b);
  });
  const all = document.createElement("button");
  all.type = "button";
  all.className = "chip on";
  all.textContent = "All tumors";
  all.addEventListener("click", () => select(-1));
  chips.prepend(all);

  function counts() {
    return D.rows.map((_, i) => {
      const cells = D.cells.filter((c) => c.i === i && (col < 0 || c.j === col));
      const n = cells.reduce((a, c) => a + c.n, 0);
      const studies = [].concat(...cells.map((c) => c.studies));
      return { i, n, studies };
    });
  }
  let picked = -1;
  function draw() {
    const data = counts();
    const max = Math.max(1, ...data.map((d) => d.n));
    rowsEl.innerHTML = "";
    data.forEach((d) => {
      const el = document.createElement("button");
      el.type = "button";
      el.className = "bar" + (picked === d.i ? " on" : "");
      el.innerHTML = '<span class="bl">' + D.rows[d.i] + '</span><span class="bt"><i style="width:0"></i></span><span class="bn">' + d.n + "</span>";
      el.addEventListener("click", () => { picked = picked === d.i ? -1 : d.i; draw(); list(data); });
      rowsEl.appendChild(el);
      requestAnimationFrame(() => requestAnimationFrame(() => { el.querySelector("i").style.width = (d.n / max) * 100 + "%"; }));
    });
    list(data);
    if (window.EVMAP) window.EVMAP.setFilter(picked, col);
  }
  function list(data) {
    const d = picked >= 0 ? data[picked] : null;
    if (!d) {
      listEl.innerHTML = "<span>Select a row to list its studies.</span>";
      return;
    }
    const uniq = Array.from(new Set(d.studies));
    listEl.innerHTML = "<b>" + D.rows[d.i] + "</b><span> &middot; " + uniq.length + " studies</span><p>" + (uniq.join("; ") || "No core study in this selection.") + "</p>";
  }
  function select(j) {
    col = j;
    chips.querySelectorAll(".chip").forEach((c, k) => c.classList.toggle("on", k === j + 1));
    draw();
  }
  draw();
})();
