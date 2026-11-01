/* jerlash : effets pixel tramés (Bayer 8x8). Script classique, sans dépendance, sans réseau. */
(function () {
  var BAYER = [0,32,8,40,2,34,10,42,48,16,56,24,50,18,58,26,12,44,4,36,14,46,6,38,60,28,52,20,62,30,54,22,
               3,35,11,43,1,33,9,41,51,19,59,27,49,17,57,25,15,47,7,39,13,45,5,37,63,31,55,23,61,29,53,21];

  function hash(x, y, s) {
    var h = (x * 374761393 + y * 668265263 + s * 2147483647) | 0;
    h = (h ^ (h >>> 13)) * 1274126177 | 0;
    return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
  }
  function smooth(t) { return t * t * (3 - 2 * t); }
  function noise(x, y, s) {
    var x0 = Math.floor(x), y0 = Math.floor(y), fx = smooth(x - x0), fy = smooth(y - y0);
    var a = hash(x0, y0, s), b = hash(x0 + 1, y0, s), c = hash(x0, y0 + 1, s), d = hash(x0 + 1, y0 + 1, s);
    return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy;
  }
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  /* Champs scalaires : x, y en cellules ; w, h taille de la grille ; t temps en secondes. Retour 0..1. */
  var FIELDS = {
    orbe: function (x, y, w, h, t, o) {
      var r = Math.min(w, h) * (o.size || 0.38), cx = w * (o.cx == null ? 0.66 : o.cx), cy = h * (o.cy == null ? 0.5 : o.cy);
      var dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy) / r;
      if (d > 1) return 0;
      var lx = x - cx + r * 0.38 + Math.sin(t * 0.4) * r * 0.08, ly = y - cy + r * 0.38;
      return clamp(0.1 + 0.9 * (1 - Math.sqrt(lx * lx + ly * ly) / (r * 1.9)));
    },
    nuage: function (x, y, w, h, t, o) {
      var s = o.seed || 7, n = noise(x / 20 + t * 0.05, y / 20, s) * 0.65 + noise(x / 8, y / 8 - t * 0.08, s + 1) * 0.35;
      var e = Math.min(x, w - x, y, h - y) / (Math.min(w, h) * 0.45);
      return clamp((n - 0.35) * 1.6 + clamp(1 - e) * 0.5);
    },
    horizon: function (x, y, w, h, t, o) {
      var n = noise(x / 26 + t * 0.06, y / 26, o.seed || 11);
      return clamp((y / h) * 1.15 - 0.25 + (n - 0.5) * 0.55);
    },
    onde: function (x, y, w, h, t, o) {
      var v = Math.sin(x / 9 + t * 0.6) * 0.5 + Math.sin((x + y) / 17 - t * 0.3) * 0.5;
      return clamp(0.5 + v * 0.45 * (1 - y / h) + (y / h - 0.5) * 0.6);
    }
  };

  function cssColor(el, v) {
    if (!v) return null;
    if (v.charAt(0) === '#' || v.indexOf('(') > 0) return v;
    var c = getComputedStyle(el).getPropertyValue('--' + v.replace(/^--/, '')).trim();
    return c || v;
  }

  /**
   * pixelField(target, options) : dessine un fond pixel tramé dans un <canvas> qui remplit target.
   * options : field ('orbe'|'nuage'|'horizon'|'onde'), fg, bg (nom de token ou couleur), cell (px),
   * animate (bool), pointer (bool), seed, size, cx, cy, invert (bool).
   * Retourne { redraw, destroy }.
   */
  function pixelField(target, options) {
    var o = Object.assign({ field: 'orbe', fg: 'brique', bg: 'paper', cell: 6, animate: false, pointer: false }, options || {});
    var canvas = target.tagName === 'CANVAS' ? target : target.querySelector('canvas.ia-pixel__canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'ia-pixel__canvas';
      canvas.setAttribute('aria-hidden', 'true');
      target.insertBefore(canvas, target.firstChild);
    }
    var host = canvas === target ? canvas.parentNode : target;
    var ctx = canvas.getContext('2d');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var raf = 0, last = 0, t0 = performance.now(), px = -1e9, py = -1e9, alive = true;
    var f = FIELDS[o.field] || FIELDS.orbe;

    function draw(now) {
      var W = host.clientWidth, H = host.clientHeight;
      if (!W || !H) return;
      var dpr = window.devicePixelRatio || 1, cell = Math.max(2, +o.cell || 6);
      if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) {
        canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var fg = cssColor(host, o.fg), bg = cssColor(host, o.bg);
      ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = fg;
      var w = Math.ceil(W / cell), h = Math.ceil(H / cell), t = ((now || t0) - t0) / 1000;
      var pcx = px / cell, pcy = py / cell, pr = Math.min(w, h) * 0.22;
      for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
          var v = f(x, y, w, h, t, o);
          if (o.pointer) {
            var dx = x - pcx, dy = y - pcy, d2 = (dx * dx + dy * dy) / (pr * pr);
            if (d2 < 1) v = clamp(v + (1 - d2) * 0.6);
          }
          if (o.invert) v = 1 - v;
          if (v > BAYER[(y & 7) * 8 + (x & 7)] / 64) ctx.fillRect(x * cell, y * cell, cell, cell);
        }
      }
    }
    function loop(now) {
      if (!alive) return;
      if (now - last > 80) { draw(now); last = now; }
      raf = requestAnimationFrame(loop);
    }
    function redraw() { draw(performance.now()); }

    var ro = window.ResizeObserver ? new ResizeObserver(redraw) : null;
    if (ro) ro.observe(host);
    var mo = new MutationObserver(redraw);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });
    function onMove(e) { var r = host.getBoundingClientRect(); px = e.clientX - r.left; py = e.clientY - r.top; if (!o.animate || reduce) redraw(); }
    function onLeave() { px = py = -1e9; if (!o.animate || reduce) redraw(); }
    if (o.pointer && !reduce) { host.addEventListener('pointermove', onMove); host.addEventListener('pointerleave', onLeave); }

    if (o.animate && !reduce) raf = requestAnimationFrame(loop); else redraw();

    return {
      redraw: redraw,
      destroy: function () {
        alive = false; cancelAnimationFrame(raf); if (ro) ro.disconnect(); mo.disconnect();
        host.removeEventListener('pointermove', onMove); host.removeEventListener('pointerleave', onLeave);
      }
    };
  }

  /* Monte tous les éléments [data-pixel] sous root. Attributs : data-pixel (champ), data-fg, data-bg, data-cell, data-animate, data-pointer. */
  function mountPixelFields(root) {
    var els = (root || document).querySelectorAll('[data-pixel]'), out = [];
    for (var i = 0; i < els.length; i++) {
      var el = els[i], d = el.dataset;
      var cell = d.cell;
      if (cell && isNaN(+cell)) cell = parseFloat(getComputedStyle(el).getPropertyValue('--' + cell)) || 6;
      out.push(pixelField(el, {
        field: d.pixel || 'orbe', fg: d.fg || 'brique', bg: d.bg || 'paper', cell: +cell || 6,
        animate: d.animate === 'true', pointer: d.pointer === 'true', invert: d.invert === 'true',
        seed: d.seed ? +d.seed : undefined
      }));
    }
    return out;
  }

  window.IAvocat = { pixelField: pixelField, mountPixelFields: mountPixelFields, fields: Object.keys(FIELDS) };
})();
