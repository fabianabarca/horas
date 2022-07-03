export default function render(vnode, ctx, e) {
  var tag = vnode.tag,
      props = vnode.props,
      children = vnode.children;

  if (tag === 'svg') {
    var width = props.width,
        height = props.height;
    ctx.width = width;
    ctx.height = height;
  }

  if (tag === 'rect') {
    var x = props.x,
        y = props.y,
        _width = props.width,
        _height = props.height,
        fill = props.fill,
        onClick = props.onClick; // From https://github.com/canvg/canvg

    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + _width, y);
    ctx.lineTo(x + _width, y + _height);
    ctx.lineTo(x, y + _height);
    ctx.lineTo(x, y);

    if (e && onClick && ctx.isPointInPath(e.x, e.y)) {
      onClick();
    }

    ctx.closePath();

    if (fill) {
      ctx.fillStyle = fill;
    }

    ctx.fill();
  }

  if (tag === 'text') {
    var _x = props.x,
        _y = props.y,
        style = props.style;

    if (style) {
      ctx.fillStyle = style.fill;
      var BL = {
        central: 'middle',
        middle: 'middle',
        hanging: 'hanging',
        alphabetic: 'alphabetic',
        ideographic: 'ideographic'
      };
      var AL = {
        start: 'start',
        middle: 'center',
        end: 'end'
      };
      ctx.textBaseline = BL[style['dominant-baseline']] || 'alphabetic';
      ctx.textAlign = AL[style['text-anchor']] || 'start';
      ctx.font = "".concat(style['font-weight'] || '', " ").concat(style['font-size'], " ").concat(style['font-family']);
    }

    ctx.fillText(children.join(''), _x, _y);
  }

  children.forEach(function (v) {
    if (typeof v !== 'string') {
      render(v, ctx, e);
    }
  });
}