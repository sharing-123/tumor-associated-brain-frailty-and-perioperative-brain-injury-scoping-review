(function () {
  if (!window.THREE || !window.EVIDENCE) return;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const D = window.EVIDENCE;

  function makeScene(canvas) {
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 200);
    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const key = new THREE.DirectionalLight(0xffffff, 0.9);
    key.position.set(6, 10, 8);
    scene.add(key);
    const rim = new THREE.PointLight(0x2dd4bf, 0.8, 60);
    rim.position.set(-8, -4, 6);
    scene.add(rim);
    const group = new THREE.Group();
    scene.add(group);
    const st = { rx: -0.25, ry: 0.5, dist: 22, drag: false, lx: 0, ly: 0, auto: !reduce, visible: true };
    canvas.addEventListener("pointerdown", (e) => { st.drag = true; st.auto = false; st.lx = e.clientX; st.ly = e.clientY; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener("pointerup", () => { st.drag = false; });
    canvas.addEventListener("pointermove", (e) => {
      if (!st.drag) return;
      st.ry += (e.clientX - st.lx) * 0.006;
      st.rx = Math.max(-1.2, Math.min(1.2, st.rx + (e.clientY - st.ly) * 0.006));
      st.lx = e.clientX;
      st.ly = e.clientY;
    });
    canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      st.dist = Math.max(12, Math.min(34, st.dist + e.deltaY * 0.02));
    }, { passive: false });
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
    return { renderer, scene, camera, group, st, resize };
  }

  function label(text, color, size) {
    const c = document.createElement("canvas");
    c.width = 512; c.height = 96;
    const x = c.getContext("2d");
    x.font = "500 " + (size || 38) + "px 'Fira Sans', sans-serif";
    x.fillStyle = color || "#c9d6e6";
    x.textAlign = "center";
    x.textBaseline = "middle";
    x.fillText(text, 256, 48);
    const t = new THREE.CanvasTexture(c);
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false }));
    s.scale.set(5, 0.94, 1);
    return s;
  }

  function shareColor(s) {
    if (s === null) return 0x8c9aa5;
    if (s >= 0.75) return 0x2dd4bf;
    if (s >= 0.25) return 0xf0b13a;
    return 0x8c9aa5;
  }

  function evidenceMap() {
    const canvas = document.getElementById("map3d");
    const tip = document.getElementById("tip");
    const S = makeScene(canvas);
    const nR = D.rows.length, nC = D.cols.length;
    const gx = 2.9, gy = 1.55;
    const meshes = [];
    D.cells.forEach((c) => {
      if (!c.n) return;
      const r = 0.28 + Math.sqrt(c.n) * 0.2;
      const depth = c.share === null ? 0 : (c.share - 0.5) * 3.2;
      const m = new THREE.Mesh(
        new THREE.SphereGeometry(r, 36, 28),
        new THREE.MeshStandardMaterial({ color: shareColor(c.share), roughness: 0.35, metalness: 0.15, transparent: true, opacity: 0.92 })
      );
      m.position.set((c.j - (nC - 1) / 2) * gx, ((nR - 1) / 2 - c.i) * gy, depth);
      m.userData = { c, base: m.position.z, r, ph: Math.random() * 6.28 };
      S.group.add(m);
      meshes.push(m);
    });
    D.cols.forEach((t, j) => {
      const s = label(t, "#e8eef6", 40);
      s.position.set((j - (nC - 1) / 2) * gx, ((nR - 1) / 2 + 1.1) * gy, 0);
      S.group.add(s);
    });
    D.rows.forEach((t, i) => {
      const s = label(t, "#8fa2b8", 34);
      s.position.set(-((nC - 1) / 2) * gx - 4.2, ((nR - 1) / 2 - i) * gy, 0);
      S.group.add(s);
    });
    const grid = new THREE.GridHelper(20, 20, 0x1a2639, 0x111b2b);
    grid.position.y = -((nR - 1) / 2) * gy - 1.4;
    S.group.add(grid);

    const ray = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let hover = null;
    canvas.addEventListener("pointermove", (e) => {
      const b = canvas.getBoundingClientRect();
      mouse.set(((e.clientX - b.left) / b.width) * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1);
      ray.setFromCamera(mouse, S.camera);
      const hit = ray.intersectObjects(meshes)[0];
      hover = hit ? hit.object : null;
      if (hover) {
        const c = hover.userData.c;
        const list = c.studies.slice(0, 8).join("; ");
        const more = c.studies.length > 8 ? " and " + (c.studies.length - 8) + " more" : "";
        const sh = c.share === null ? "not graded" : Math.round(c.share * 100) + "% at level 2";
        tip.innerHTML = "<b>" + D.rows[c.i] + "</b><br>" + D.cols[c.j] + " &middot; " + c.n + " studies &middot; " + sh + "<br><span>" + list + more + "</span>";
        tip.style.display = "block";
        const sb = canvas.parentElement.getBoundingClientRect();
        tip.style.left = Math.min(e.clientX - sb.left + 14, sb.width - 310) + "px";
        tip.style.top = (e.clientY - sb.top + 14) + "px";
        canvas.style.cursor = "pointer";
      } else {
        tip.style.display = "none";
        canvas.style.cursor = "";
      }
    });
    canvas.addEventListener("pointerleave", () => { hover = null; tip.style.display = "none"; });

    let fRow = -1, fCol = -1;
    window.EVMAP = { setFilter: function (r, c) { fRow = r; fCol = c; } };
    let t = 0;
    function frame() {
      requestAnimationFrame(frame);
      if (!S.st.visible || !canvas.clientWidth) return;
      t += 0.016;
      if (S.st.auto) S.st.ry += 0.0028;
      S.group.rotation.y = S.st.ry;
      S.group.rotation.x = S.st.rx;
      S.camera.position.set(0, 0, S.st.dist);
      S.camera.lookAt(0, 0, 0);
      meshes.forEach((m) => {
        const c = m.userData.c;
        const on = (fRow < 0 || c.i === fRow) && (fCol < 0 || c.j === fCol);
        m.material.opacity += ((on ? 0.92 : 0.1) - m.material.opacity) * 0.12;
        const k = m === hover ? 1.18 : (fRow >= 0 && c.i === fRow && on ? 1.12 : 1);
        m.scale.lerp(new THREE.Vector3(k, k, k), 0.15);
        if (!reduce) m.position.z = m.userData.base + Math.sin(t * 0.9 + m.userData.ph) * 0.12;
      });
      S.renderer.render(S.scene, S.camera);
    }
    frame();
  }

  function twoHit() {
    const canvas = document.getElementById("hit3d");
    const S = makeScene(canvas);
    S.st.dist = 20;
    S.st.rx = -0.18;
    const pts = [];
    for (let i = 0; i <= 80; i++) {
      const u = i / 80;
      pts.push(new THREE.Vector3(-9 + u * 18, Math.sin(u * Math.PI * 2.2) * 1.3, Math.cos(u * Math.PI * 1.6) * 1.8));
    }
    const curve = new THREE.CatmullRomCurve3(pts);
    const tube = new THREE.Mesh(
      new THREE.TubeGeometry(curve, 240, 0.09, 12, false),
      new THREE.MeshStandardMaterial({ color: 0x1f3550, roughness: 0.5 })
    );
    S.group.add(tube);

    const nodes = [
      { u: 0.14, color: 0xf0b13a, text: "First hit: the tumor", r: 0.95 },
      { u: 0.52, color: 0xef6a57, text: "Second hit: perioperative injury", r: 0.95 },
      { u: 0.9, color: 0x2dd4bf, text: "Delirium, decline, deficit", r: 0.95 }
    ];
    const orbs = nodes.map((n) => {
      const p = curve.getPoint(n.u);
      const m = new THREE.Mesh(
        new THREE.SphereGeometry(n.r, 40, 32),
        new THREE.MeshStandardMaterial({ color: n.color, roughness: 0.3, metalness: 0.2, emissive: n.color, emissiveIntensity: 0.25 })
      );
      m.position.copy(p);
      const halo = new THREE.Mesh(
        new THREE.TorusGeometry(n.r * 1.5, 0.03, 8, 64),
        new THREE.MeshBasicMaterial({ color: n.color, transparent: true, opacity: 0.55 })
      );
      halo.position.copy(p);
      const l = label(n.text, "#e8eef6", 34);
      l.position.set(p.x, p.y + 2.2, p.z);
      S.group.add(m, halo, l);
      return { m, halo, p };
    });

    const N = 140;
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(N * 3);
    const seeds = Array.from({ length: N }, () => ({ u: Math.random(), s: 0.05 + Math.random() * 0.1, o: new THREE.Vector3((Math.random() - 0.5) * 0.9, (Math.random() - 0.5) * 0.9, (Math.random() - 0.5) * 0.9) }));
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const dots = new THREE.Points(geo, new THREE.PointsMaterial({ color: 0xbfe9f5, size: 0.11, transparent: true, opacity: 0.9, depthWrite: false }));
    S.group.add(dots);

    let t = 0;
    function frame() {
      requestAnimationFrame(frame);
      if (!S.st.visible || !canvas.clientWidth) return;
      t += 0.016;
      if (S.st.auto) S.st.ry = Math.sin(t * 0.25) * 0.55;
      S.group.rotation.y = S.st.ry;
      S.group.rotation.x = S.st.rx;
      S.camera.position.set(0, 0, S.st.dist);
      S.camera.lookAt(0, 0, 0);
      seeds.forEach((s, i) => {
        if (!reduce) s.u = (s.u + s.s * 0.01) % 1;
        const p = curve.getPoint(s.u);
        pos[i * 3] = p.x + s.o.x;
        pos[i * 3 + 1] = p.y + s.o.y;
        pos[i * 3 + 2] = p.z + s.o.z;
      });
      geo.attributes.position.needsUpdate = true;
      orbs.forEach((o, i) => {
        const k = 1 + Math.sin(t * 1.6 + i) * 0.05;
        o.m.scale.setScalar(k);
        o.halo.rotation.x = t * 0.6 + i;
        o.halo.rotation.y = t * 0.4;
      });
      S.renderer.render(S.scene, S.camera);
    }
    frame();
  }

  evidenceMap();
  twoHit();
})();
