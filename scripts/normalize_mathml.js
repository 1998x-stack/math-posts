"use strict";
/** Repair reviewed MathML tokens where implicit multiplication was
 * accidentally fused into one identifier. Operates ONLY inside <math>.
 * This is a narrow correction pass, never a symbolic algebra solver.
 */
const mathID=(s)=>'<mi>'+s+'</mi>';
const normal=(s)=>'<mi mathvariant="normal">'+s+'</mi>';
const product=parts=>parts.map(x=>["sin","cos","tan","ln","log","max","min"].includes(x)?normal(x):mathID(x)).join("");
const products={
 "sinxcosx":["sin","x","cos","x"],"sinx":["sin","x"],"cosx":["cos","x"],
 "lnx":["ln","x"],"lnm":["ln","m"],"alnx":["a","ln","x"],
 "xe":["x","e"],"ax":["a","x"],"mx":["m","x"],"iz":["i","z"],
 "qa":["q","a"],"nd":["n","d"],"ab":["a","b"],"bi":["b","i"],
 "rl":["r","l"],"kx":["k","x"],"tx":["t","x"],"my":["m","y"],"ms":["m","s"],
 "km":["k","m"],"sy":["s","y"],"cx":["c","x"],"hx":["h","x"],
 "kh":["k","h"],"khx":["k","h","x"],"ay":["a","y"],"py":["p","y"],
 "smn":["s","m","n"],"uvs":["u","v","s"],"uv":["u","v"],
 "uk":["u","k"],"mn":["m","n"],"maxL":["max","L"]
};
function normalize(html) {
 let changes=0;const corrected=html.replace(/<math\b[\s\S]*?<\/math>/gi, block=>{
  let s=block;
  const replacement=(re,fn)=>{s=s.replace(re,(...args)=>{changes++;return fn(...args)})};
  replacement(/<mfrac><mn>12<\/mn><mi>undefined<\/mi><\/mfrac>/g,()=>'<mfrac><mn>1</mn><mn>2</mn></mfrac>');
  replacement(/<msub><mi>proj<\/mi><mi>ba<\/mi><\/msub>/g,()=>'<msub>'+normal('proj')+mathID('b')+'</msub>'+mathID('a'));
  replacement(/<msub><mi>F<\/mi><mi>h([AB])<\/mi><\/msub>/g,(_,letter)=>'<msub>'+mathID('F')+mathID('h')+'</msub>'+mathID(letter));
  replacement(/<mi>(kPA|kPB|kTR|kTS|kAB)<\/mi>/g,(_,t)=>'<msub>'+mathID('k')+'<mrow>'+mathID(t[1])+mathID(t[2])+'</mrow></msub>');
  replacement(/<msup><mi>(ax|xe)<\/mi>(<mrow>[\s\S]*?<\/mrow>|<mi>[^<]*<\/mi>|<mn>[^<]*<\/mn>)<\/msup>/g,(_,token,exponent)=>mathID(token[0])+'<msup>'+mathID(token[1])+exponent+'</msup>');
  replacement(/<mi>([A-Za-z]+)<\/mi>/g,(all,name)=>Object.hasOwn(products,name)?product(products[name]):all);
  replacement(/<mi>vertex<\/mi>|<mi>mid<\/mi>/g,(all)=>'<mtext>'+all.slice(4,-5)+'</mtext>');
  if(s.includes('<mi>undefined</mi>'))throw Error("Undefined MathML token remains");
  return s;
 });
 return {html:corrected,changes:corrected===html?0:changes};
}
module.exports={normalize};
