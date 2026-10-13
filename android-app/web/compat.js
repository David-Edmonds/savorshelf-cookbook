/* JSON recipe-state compatibility for WebView 80–97. Native structuredClone wins. */
(function(root){'use strict';
 if(!Object.hasOwn)Object.defineProperty(Object,'hasOwn',{value:function(o,k){return Object.prototype.hasOwnProperty.call(o,k);},configurable:true,writable:true});
 if(!root.structuredClone)root.structuredClone=function(input){
  var seen=new Map();
  function copy(x){
   if(x===null||typeof x!=='object'){if(typeof x==='function'||typeof x==='symbol')throw new TypeError('Unsupported state value');return x;}
   if(seen.has(x))return seen.get(x);
   if(x instanceof Date)return new Date(x.getTime());
   if(!Array.isArray(x)&&Object.getPrototypeOf(x)!==Object.prototype&&Object.getPrototypeOf(x)!==null)throw new TypeError('Only plain recipe state is supported');
   var out=Array.isArray(x)?new Array(x.length):{};seen.set(x,out);
   Object.keys(x).forEach(function(k){Object.defineProperty(out,k,{value:copy(x[k]),enumerable:true,writable:true,configurable:true});});return out;
  }
  return copy(input);
 };
})(typeof globalThis!=='undefined'?globalThis:window);
