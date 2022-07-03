function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function addChild(c, childNodes) {
  if (c === null || c === undefined) return;

  if (typeof c === 'string' || typeof c === 'number') {
    childNodes.push(c.toString());
  } else if (Array.isArray(c)) {
    for (var i = 0; i < c.length; i++) {
      addChild(c[i], childNodes);
    }
  } else {
    childNodes.push(c);
  }
}

export default function h(tag, props) {
  var childNodes = [];

  for (var _len = arguments.length, children = new Array(_len > 2 ? _len - 2 : 0), _key = 2; _key < _len; _key++) {
    children[_key - 2] = arguments[_key];
  }

  addChild(children, childNodes);

  if (typeof tag === 'function') {
    return tag(_objectSpread(_objectSpread({}, props), {}, {
      children: childNodes
    }));
  }

  return {
    tag: tag,
    props: props,
    children: childNodes
  };
}