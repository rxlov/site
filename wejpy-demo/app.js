(() => {
  "use strict";

  const track = document.querySelector("[data-track]");
  const stage = document.querySelector("[data-stage]");
  const video = document.querySelector("[data-video]");
  const canvas = document.querySelector("[data-canvas]");
  const ctx = canvas.getContext("2d");
  const badgeText = document.querySelector("[data-badge-text]");
  const pctEl = document.querySelector("[data-pct]");
  const hud = document.querySelector(".hud");
  const segs = [...document.querySelectorAll("[data-seg]")];
  const chapters = [...document.querySelectorAll("[data-chapter]")];
  const hudItems = [...document.querySelectorAll("[data-hud]")];

  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const CLIP_SRC = "media/hero.mp4";

  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smooth = (t) => t * t * (3 - 2 * t);
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const rgb = (c, a = 1) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;

  let mode = "placeholder"; // "placeholder" | "video"
  let target = 0;
  let current = 0;
  let raf = 0;
  let activeChapter = -1;

  /* ------------------------------------------------------------------
     Scroll progress of the pinned track (0..1)
  ------------------------------------------------------------------ */
  function readProgress() {
    const rect = track.getBoundingClientRect();
    const total = track.offsetHeight - window.innerHeight;
    return total > 0 ? clamp(-rect.top / total) : 0;
  }

  /* ------------------------------------------------------------------
     Video mode: scrub currentTime. Falls back to canvas if no clip.
  ------------------------------------------------------------------ */
  function applyVideo() {
    if (mode !== "video" || !isFinite(video.duration) || video.seeking) return;
    const t = clamp(current) * video.duration;
    if (Math.abs(video.currentTime - t) > 1 / 120) video.currentTime = Math.min(t, video.duration - 0.001);
  }
  video.addEventListener("seeked", applyVideo);

  function enableVideo() {
    mode = "video";
    document.body.dataset.source = "video";
    applyVideo();
    // iOS only allows seeking after a user-initiated play/pause.
    const unlock = () => {
      video.play().then(() => video.pause()).catch(() => {});
      window.removeEventListener("touchstart", unlock);
    };
    window.addEventListener("touchstart", unlock, { passive: true, once: true });
  }

  video.addEventListener(
    "loadedmetadata",
    () => { if (isFinite(video.duration) && video.duration > 0) enableVideo(); },
    { once: true }
  );
  video.addEventListener(
    "error",
    () => {
      mode = "placeholder";
      document.body.dataset.source = "placeholder";
      badgeText.textContent = "Podgląd zastępczy · brak klipu media/hero.mp4";
    },
    { once: true }
  );
  video.src = CLIP_SRC;

  /* ------------------------------------------------------------------
     Placeholder scene: miękkie opary i światło per rozdział.
     Bez produktów i bez ludzi. Deterministyczne względem postępu,
     więc przewijanie w obie strony daje ten sam obraz.
  ------------------------------------------------------------------ */
  const PAL = [
    { bg0: hex("#07070f"), bg1: hex("#2a1b63"), glow: hex("#7a5cff"), mist: hex("#cfc6ff") },
    { bg0: hex("#04100f"), bg1: hex("#0d4a45"), glow: hex("#4df0c0"), mist: hex("#c4fff0") },
    { bg0: hex("#07070f"), bg1: hex("#1b2a5c"), glow: hex("#8fd0ff"), mist: hex("#dff1ff") },
  ];
  const KEYS = [1 / 6, 1 / 2, 5 / 6];

  function palette(p) {
    let a = 0, b = 0, f = 0;
    if (p <= KEYS[0]) { a = b = 0; }
    else if (p >= KEYS[2]) { a = b = 2; }
    else {
      a = p < KEYS[1] ? 0 : 1;
      b = a + 1;
      f = smooth(clamp((p - KEYS[a]) / (KEYS[b] - KEYS[a])));
    }
    const out = {};
    for (const k of Object.keys(PAL[0])) out[k] = PAL[a][k].map((v, i) => lerp(v, PAL[b][k][i], f));
    return out;
  }

  const hash = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };
  const PLUMES = Array.from({ length: 16 }, (_, i) => ({
    x: hash(i + 1), y: hash(i + 40), r: 0.14 + hash(i + 90) * 0.22, a: 0.05 + hash(i + 130) * 0.09,
    sp: 0.5 + hash(i + 170) * 1.6, ph: hash(i + 210) * 6.28,
  }));

  let dpr = 1;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    const h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
  }

  function drawScene(p) {
    const W = canvas.width, H = canvas.height;
    const pal = palette(p);

    // tło
    let g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, rgb(pal.bg0));
    g.addColorStop(1, rgb(pal.bg1));
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    ctx.globalCompositeOperation = "lighter";

    // duża poświata, przesuwa się z postępem
    const gx = W * (0.78 - p * 0.35), gy = H * 0.42;
    g = ctx.createRadialGradient(gx, gy, 0, gx, gy, W * 0.55);
    g.addColorStop(0, rgb(pal.glow, 0.34));
    g.addColorStop(1, rgb(pal.glow, 0));
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // opary: powoli płyną w lewo i unoszą się
    for (const m of PLUMES) {
      const x = ((((m.x - p * m.sp * 0.9) % 1.3) + 1.3) % 1.3 - 0.15) * W;
      const y = H * (0.3 + m.y * 0.55) - Math.sin(p * 9 * m.sp + m.ph) * H * 0.04;
      const r = m.r * W;
      g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, rgb(pal.mist, m.a));
      g.addColorStop(0.5, rgb(pal.glow, m.a * 0.45));
      g.addColorStop(1, rgb(pal.glow, 0));
      ctx.fillStyle = g;
      ctx.fillRect(x - r, y - r, r * 2, r * 2);
    }

    ctx.globalCompositeOperation = "source-over";

    // powierzchnia stołu z delikatnym odbiciem
    const fy = H * 0.74;
    g = ctx.createLinearGradient(0, fy, 0, H);
    g.addColorStop(0, rgb(pal.bg1, 0.55));
    g.addColorStop(1, rgb(pal.bg0, 0.95));
    ctx.fillStyle = g;
    ctx.fillRect(0, fy, W, H - fy);
    ctx.fillStyle = rgb(pal.glow, 0.2);
    ctx.fillRect(0, fy, W, Math.max(1, dpr));

    // linie ruchu kamery po powierzchni
    ctx.lineWidth = Math.max(1, dpr);
    for (let i = 0; i < 12; i++) {
      const f = i / 11;
      const y = fy + 6 * dpr + f * f * (H - fy);
      const speed = 600 + f * 4200;
      const len = W * (0.08 + f * 0.3);
      const x0 = ((((-p * speed * dpr) + i * 311) % (W + len)) + (W + len)) % (W + len) - len;
      ctx.strokeStyle = rgb(pal.glow, 0.05 + f * 0.1);
      ctx.beginPath();
      ctx.moveTo(x0, y);
      ctx.lineTo(x0 + len, y);
      ctx.stroke();
    }

    // przejście światła, jedno na rozdział
    const sweep = (p * 3) % 1;
    const bx = lerp(-0.4, 1.3, sweep) * W;
    g = ctx.createLinearGradient(bx - W * 0.16, 0, bx + W * 0.16, 0);
    g.addColorStop(0, rgb(pal.glow, 0));
    g.addColorStop(0.5, rgb(pal.mist, 0.1));
    g.addColorStop(1, rgb(pal.glow, 0));
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
  }

  /* ------------------------------------------------------------------
     HUD + chapters
  ------------------------------------------------------------------ */
  function updateUI(p) {
    const pct = Math.round(p * 100);
    pctEl.textContent = String(pct).padStart(3, "0");
    hud.setAttribute("aria-valuenow", String(pct));
    segs.forEach((el, i) => {
      el.style.transform = `scaleX(${clamp(p * 3 - i).toFixed(4)})`;
    });
    const idx = p >= 2 / 3 ? 2 : p >= 1 / 3 ? 1 : 0;
    if (idx !== activeChapter) {
      activeChapter = idx;
      chapters.forEach((el, i) => {
        el.classList.toggle("is-active", i === idx);
        el.setAttribute("aria-hidden", i === idx ? "false" : "true");
      });
      hudItems.forEach((el, i) => el.classList.toggle("is-active", i === idx));
      stage.dataset.chapter = String(idx);
    }
    stage.dataset.progress = p.toFixed(3);
  }

  function render() {
    if (mode === "video") applyVideo();
    else drawScene(current);
    updateUI(current);
  }

  /* ------------------------------------------------------------------
     Smoothing loop: runs only while current != target
  ------------------------------------------------------------------ */
  function tick() {
    raf = 0;
    const d = target - current;
    current = reduceMotion || Math.abs(d) < 0.0004 ? target : current + d * 0.14;
    render();
    if (current !== target) raf = requestAnimationFrame(tick);
  }
  const topbar = document.querySelector(".topbar");
  function updateTopbar() {
    topbar.classList.toggle("is-solid", track.getBoundingClientRect().bottom < 72);
  }
  function kick() {
    target = readProgress();
    updateTopbar();
    if (!raf) raf = requestAnimationFrame(tick);
  }

  window.addEventListener("scroll", kick, { passive: true });
  window.addEventListener("resize", () => { resize(); kick(); render(); });

  resize();
  target = current = readProgress();
  updateTopbar();
  render();


  // wspólna bramka 18+ (common.js) informuje o zamknięciu, wtedy przeliczamy scenę
  document.addEventListener("wejpy:gate", (e) => { if (!e.detail.open) kick(); });
})();
