import h from '../h';
import { diffDays, formatDate, noop, today, oneYearAgo, rectColor } from '../utils';
import Days from './Days';
import Months from './Months';
import DayTitles from './DayTitles';
import getStyles from './styles';
export default function Graph(_ref) {
  var _ref$data = _ref.data,
      data = _ref$data === void 0 ? [] : _ref$data,
      _ref$onClick = _ref.onClick,
      onClick = _ref$onClick === void 0 ? noop : _ref$onClick,
      _ref$colorFun = _ref.colorFun,
      colorFun = _ref$colorFun === void 0 ? rectColor : _ref$colorFun,
      _ref$startDate = _ref.startDate,
      startDate = _ref$startDate === void 0 ? oneYearAgo() : _ref$startDate,
      _ref$endDate = _ref.endDate,
      endDate = _ref$endDate === void 0 ? today() : _ref$endDate,
      _ref$size = _ref.size,
      size = _ref$size === void 0 ? 12 : _ref$size,
      _ref$space = _ref.space,
      space = _ref$space === void 0 ? 1 : _ref$space,
      _ref$padX = _ref.padX,
      padX = _ref$padX === void 0 ? 20 : _ref$padX,
      _ref$padY = _ref.padY,
      padY = _ref$padY === void 0 ? 20 : _ref$padY,
      _ref$styleOptions = _ref.styleOptions,
      styleOptions = _ref$styleOptions === void 0 ? {} : _ref$styleOptions,
      _ref$onHover = _ref.onHover,
      onHover = _ref$onHover === void 0 ? noop : _ref$onHover;
  var values = [];
  var days = diffDays(startDate, endDate);
  var dataTmp = data.reduce(function (memo, v) {
    memo[v.date] = v.count;
    return memo;
  }, {}); // Compute values

  var group = 0;

  for (var i = 0; i <= days; i += 1) {
    var date = new Date(startDate);
    date.setDate(date.getDate() + i);
    var day = date.getDay();
    var count = dataTmp[formatDate(date)] || 0;

    if (day === 0 && i !== 0 || i === 0) {
      values.push([]);
      group += 1;
    }

    values[group - 1].push({
      count: count,
      date: date,
      day: day
    });
  }

  var s = size + space * 2;
  var width = group * s + padX * 2;
  var height = 7 * s + padY + 10;
  var box = "0 0 ".concat(width, " ").concat(height);
  var styles = getStyles(styleOptions);
  var attrs = {
    styles: styles,
    values: values,
    size: size,
    space: space,
    colorFun: colorFun,
    padX: padX,
    padY: padY,
    onClick: onClick,
    onHover: onHover
  };
  return h("svg", {
    width: width,
    height: height,
    viewBox: box
  }, h("rect", {
    x: 0,
    y: 0,
    width: width,
    height: height,
    fill: "#fff"
  }), h(Days, attrs), h(Months, attrs), h(DayTitles, attrs));
}