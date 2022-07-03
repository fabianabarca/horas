import h from '../h';
import { formatDate } from '../utils';
export default function Days(_ref) {
  var values = _ref.values,
      size = _ref.size,
      space = _ref.space,
      padX = _ref.padX,
      padY = _ref.padY,
      colorFun = _ref.colorFun,
      _onClick = _ref.onClick,
      onHover = _ref.onHover;
  return h("g", null, values.map(function (v, i) {
    var s = size + space * 2;
    var x = padX + i * s + space;
    var y0 = padY + space;
    return h("g", null, v.map(function (d) {
      return h("rect", {
        "class": "cg-day",
        x: x,
        y: d.day * s + y0,
        width: size,
        height: size,
        fill: colorFun(d),
        "data-count": d.count,
        "data-date": formatDate(d.date),
        onClick: function onClick() {
          return _onClick(d);
        },
        onMouseOver: function onMouseOver() {
          return onHover(d);
        }
      });
    }));
  }));
}