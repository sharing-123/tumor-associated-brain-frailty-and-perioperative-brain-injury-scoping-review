const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

const PALETTES = [
  { tubes: ["#2dd4bf", "#5aa9ff", "#f0b13a"], lights: ["#2dd4bf", "#ef6a57", "#5aa9ff", "#f0b13a"] },
  { tubes: ["#f0b13a", "#ef6a57", "#2dd4bf"], lights: ["#f0b13a", "#5aa9ff", "#ef6a57", "#2dd4bf"] },
  { tubes: ["#5aa9ff", "#a78bfa", "#2dd4bf"], lights: ["#5aa9ff", "#2dd4bf", "#f0b13a", "#ef6a57"] },
  { tubes: ["#ef6a57", "#f0b13a", "#5aa9ff"], lights: ["#ef6a57", "#2dd4bf", "#a78bfa", "#f0b13a"] }
];

async function startTubes() {
  const canvas = document.getElementById("tubes");
  if (!canvas || reduce) return;
  try {
    const mod = await import("./vendor/tubes1.min.js");
    const TubesCursor = mod.default;
    let idx = 0;
    const app = TubesCursor(canvas, {
      tubes: {
        colors: PALETTES[0].tubes,
        lights: { intensity: 160, colors: PALETTES[0].lights }
      }
    });
    const hero = document.querySelector(".hero");
    hero.addEventListener("click", (e) => {
      if (e.target.closest("a, button")) return;
      idx = (idx + 1) % PALETTES.length;
      app.tubes.setColors(PALETTES[idx].tubes);
      app.tubes.setLightsColors(PALETTES[idx].lights);
    });
  } catch (err) {
    canvas.style.display = "none";
  }
}

function counters() {
  const els = document.querySelectorAll("[data-count]");
  const run = (el) => {
    const end = Number(el.dataset.count);
    const suffix = el.dataset.suffix || "";
    if (reduce || end === 0) {
      el.textContent = end + suffix;
      return;
    }
    const t0 = performance.now();
    const dur = 1400;
    const tick = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * e) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        run(en.target);
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.4 });
  els.forEach((el) => io.observe(el));
}

function reveal() {
  const els = document.querySelectorAll(".reveal");
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add("in");
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.12 });
  els.forEach((el, i) => {
    el.style.transitionDelay = (i % 4) * 60 + "ms";
    io.observe(el);
  });
}

function glow() {
  const g = document.getElementById("glow");
  if (!g || reduce) return;
  let x = -400, y = -400, tx = -400, ty = -400;
  addEventListener("pointermove", (e) => { tx = e.clientX; ty = e.clientY; });
  const loop = () => {
    x += (tx - x) * 0.12;
    y += (ty - y) * 0.12;
    g.style.left = x + "px";
    g.style.top = y + "px";
    requestAnimationFrame(loop);
  };
  loop();
}

function tabs() {
  const btns = document.querySelectorAll(".tab");
  btns.forEach((b) => b.addEventListener("click", () => {
    btns.forEach((o) => o.setAttribute("aria-selected", String(o === b)));
    document.querySelectorAll(".panel").forEach((p) => p.classList.toggle("on", p.id === b.dataset.panel));
    dispatchEvent(new Event("resize"));
  }));
}

function lightbox() {
  const dlg = document.getElementById("lightbox");
  const img = document.getElementById("lbImg");
  document.querySelectorAll(".shot").forEach((s) => s.addEventListener("click", () => {
    img.src = s.dataset.src;
    dlg.showModal();
  }));
  dlg.addEventListener("click", () => dlg.close());
}

function copyCite() {
  const btn = document.getElementById("copyBtn");
  const txt = document.getElementById("citeText");
  btn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(txt.textContent);
      btn.textContent = "Copied";
      setTimeout(() => { btn.textContent = "Copy citation"; }, 1600);
    } catch (e) {
      btn.textContent = "Select and copy";
    }
  });
}

startTubes();
counters();
reveal();
glow();
tabs();
lightbox();
copyCite();
