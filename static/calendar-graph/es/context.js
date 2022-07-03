export default function createContext(dom) {
  var canvas = typeof dom === 'string' ? document.querySelector(dom) : dom;
  var ctx = canvas.getContext('2d');
  var backingStore = ctx.webkitBackingStorePixelRatio || ctx.mozBackingStorePixelRatio || ctx.msBackingStorePixelRatio || ctx.oBackingStorePixelRatio || ctx.backingStorePixelRatio || 1;
  var ratio = (window.devicePixelRatio || 1) / backingStore;
  ['width', 'height'].forEach(function (key) {
    Object.defineProperty(ctx, key, {
      get: function get() {
        return canvas[key] / ratio;
      },
      set: function set(v) {
        canvas[key] = v * ratio;
        canvas.style[key] = "".concat(v, "px");
        ctx.scale(ratio, ratio);
      },
      enumerable: true,
      configurable: true
    });
  });
  canvas.addEventListener('click', function (e) {
    if (!ctx.onClick) return;
    var rect = canvas.getBoundingClientRect();
    ctx.onClick({
      x: (e.clientX - rect.left) * ratio,
      y: (e.clientY - rect.top) * ratio
    });
  });
  return ctx;
}