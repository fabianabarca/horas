import h from '../h';
var MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
export default function Months(_ref) {
  var styles = _ref.styles,
      values = _ref.values,
      size = _ref.size,
      space = _ref.space,
      padX = _ref.padX,
      padY = _ref.padY;
  var s = size + space * 2;
  var s2 = s * 2;
  var months = [];
  values.forEach(function (group, i) {
    group.forEach(function (d, j) {
      if (j === 0 && d.day === 0) {
        var month = d.date.getMonth();
        var x = i * s + padX + space;
        var last = months.slice(-1).pop();

        if (!last || month !== last.month && x - last.x > s2) {
          months.push({
            month: month,
            x: x
          });
        }
      }
    });
  });
  return h("g", null, months.map(function (v, i) {
    return h("text", {
      key: i,
      x: v.x,
      y: padY / 2,
      style: styles.text
    }, MONTH[v.month]);
  }));
}