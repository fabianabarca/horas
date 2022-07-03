function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

var NS = 'http://www.w3.org/2000/svg';
var doc = document;

function applyProperties(node, props) {
  Object.keys(props).forEach(function (k) {
    var v = props[k];

    if (k === 'style' && _typeof(v) === 'object') {
      Object.keys(v).forEach(function (sk) {
        // eslint-disable-next-line
        node.style[sk] = v[sk];
      });
    } else if (k === 'onClick') {
      if (typeof v === 'function') {
        node.addEventListener('click', v);
      }
    } else if (k === 'onMouseOver') {
      if (typeof v === 'function') {
        node.addEventListener('mouseover', v);
      }
    } else {
      node.setAttribute(k, v);
    }
  });
}

export default function render(vnode, ctx) {
  var tag = vnode.tag,
      props = vnode.props,
      children = vnode.children;
  var node = doc.createElementNS(NS, tag);

  if (props) {
    applyProperties(node, props);
  }

  children.forEach(function (v) {
    node.appendChild(typeof v === 'string' ? doc.createTextNode(v) : render(v, ctx));
  });
  return node;
}