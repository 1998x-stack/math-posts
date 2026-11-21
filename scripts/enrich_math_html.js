"use strict";
// Converts ONLY explicitly reviewed formula snippets. One-pass matching avoids reprocessing inserted markup.
const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const SUB={"₀":"0","₁":"1","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9","₊":"+","₋":"-","ₐ":"a","ₑ":"e","ₕ":"h","ᵢ":"i","ⱼ":"j","ₖ":"k","ₗ":"l","ₘ":"m","ₙ":"n","ₒ":"o","ₚ":"p","ᵣ":"r","ₛ":"s","ₜ":"t","ᵤ":"u","ᵥ":"v","ₓ":"x"};
const SUP={"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9","⁺":"+","⁻":"-"};
const tok=/(?:\d+(?:\.\d+)?[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]*|[A-Za-z]+[₀₁₂₃₄₅₆₇₈₉₊₋ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ]*[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]*|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+|[πλαβγθλμΔΣε∞∑∏√≤≥≠≈∈∉⊥∥→↔×·⋯…−+=*/^_(),.:;{}\[\]|<>±°∠-])/g;
const ops=new Set(["=","+","-","−","≤","≥","≠","≈","∈","∉","⊥","∥","→","↔","×","·","⋯","…",":",",",";","<",">","±","°","∠"]);
function toMath(expr,label){
 const e=expr.replace(/&lt;/g,"<").replace(/&gt;/g,">").replace(/&amp;/g,"&").replace(/\s+/g,"");
 const ts=e.match(tok)||[];if(ts.join("")!==e)throw Error("unsupported: "+expr+" / "+ts.join(""));let i=0;
 const mi=s=>"<mi>"+esc(s)+"</mi>", mn=s=>"<mn>"+esc(s)+"</mn>",mo=s=>"<mo>"+esc(s)+"</mo>";
 const script=(s,map)=>"<mrow>"+[...s].map(c=>{const v=map[c]||c;return /^\d$/.test(v)?mn(v):["+","-"].includes(v)?mo(v):mi(v)}).join("")+"</mrow>";
 function atom(){
  const t=ts[i++];if(!t)throw Error("incomplete: "+expr);let base="";
  if(["(","[","{"].includes(t)){const close={"(":")","[":"]","{":"}"}[t],inner=seq(close);if(ts[i]!==close)throw Error("unbalanced: "+expr);i++;base="<mrow>"+mo(t)+inner+mo(close)+"</mrow>"}
  else if(t==="|"){const inner=seq("|");if(ts[i]!=="|")throw Error("unbalanced abs: "+expr);i++;base="<mrow>"+mo("|")+inner+mo("|")+"</mrow>"}
  else if(t==="√")base="<msqrt>"+atom()+"</msqrt>";
  else if(/^\d/.test(t)){const m=t.match(/^(\d+(?:\.\d+)?)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]*)$/);base=mn(m[1]);if(m[2])base="<msup>"+base+script(m[2],SUP)+"</msup>"}
  else if(/^[A-Za-z]+/.test(t)){
   const m=t.match(/^([A-Za-z]+)([₀₁₂₃₄₅₆₇₈₉₊₋ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ]*)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]*)$/),name=m[1];
   if(name==="C"&&ts[i]==="("&&/^\d+$/.test(ts[i+1]||"")&&ts[i+2]===","&&/^\d+$/.test(ts[i+3]||"")&&ts[i+4]===")"){base='<msubsup><mi mathvariant="normal">C</mi>'+mn(ts[i+3])+mn(ts[i+1])+"</msubsup>";i+=5}
   else base=["sin","cos","tan","arctan","log","ln","min","max","det"].includes(name)?'<mi mathvariant="normal">'+name+"</mi>":mi(name);
   if(m[2])base="<msub>"+base+script(m[2],SUB)+"</msub>";
   if(m[3])base="<msup>"+base+script(m[3],SUP)+"</msup>";
  } else base=["π","λ","μ","θ","α","β","γ","Δ"].includes(t)?mi(t):mo(t);
  while(i<ts.length&&(["^","_"].includes(ts[i])||/^[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+$/.test(ts[i]))){
    if(/^[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+$/.test(ts[i]))base="<msup>"+base+script(ts[i++],SUP)+"</msup>";
    else {const op=ts[i++],item=atom();base=op==="^"?"<msup>"+base+item+"</msup>":"<msub>"+base+item+"</msub>"}
  }return base;
 }
 function seq(stop){const out=[];while(i<ts.length&&ts[i]!==stop){if(ts[i]==="/"){i++;const d=atom(),n=out.pop()||mn("1");out.push("<mfrac>"+n+d+"</mfrac>")}else if(ops.has(ts[i]))out.push(mo(ts[i++]));else out.push(atom())}return out.join("")}
 const inner=seq(null);if(i!==ts.length)throw Error("unparsed: "+expr);
 return '<math class="math-inline" aria-label="'+esc(label||"数学关系："+e)+'"><mrow>'+inner+"</mrow></math>";
}
function upgrade(html,list){
 const fs=[...new Set(list)].sort((a,b)=>b.length-a.length);if(!fs.length)return {html,count:0,unmatched:[]};
 const by=new Map(fs.map(x=>[x,toMath(x)]));
 const escapeRe=x=>x.replace(/[.*+?^$()|{}\[\]\\]/g,"\\$&");
 const re=new RegExp("(?<![A-Za-z0-9₀-₉⁰-⁹])("+fs.map(escapeRe).join("|")+")(?![A-Za-z0-9₀-₉⁰-⁹./^])","g");
 const counts=Object.fromEntries(fs.map(x=>[x,0]));const stack=[],skips=new Set(["math","svg","script","style","code","pre","head","textarea"]);
 const out=html.split(/(<[^>]+>)/g).map(part=>{
  if(part.startsWith("<")){const m=part.match(/^<\s*(\/?)\s*([A-Za-z0-9:-]+)/);if(m&&skips.has(m[2].toLowerCase())){const name=m[2].toLowerCase();if(m[1]){const j=stack.lastIndexOf(name);if(j>=0)stack.splice(j,1)}else if(!/\/\s*>$/.test(part))stack.push(name)}return part}
  return stack.length?part:part.replace(re,x=>{counts[x]++;return by.get(x)});
 }).join("");
 return {html:out,count:Object.values(counts).reduce((a,b)=>a+b,0),unmatched:fs.filter(x=>!counts[x]),counts};
}
module.exports={toMath,upgrade};
