function algebraScene(id,u){
u=Math.max(0,Math.min(1,Number(u)||0));
const W=760,H=390, v=[],teal="#147f80",blue="#2768b0",orange="#d27452",purple="#7a64b6",ink="#273e46",muted="#668088";
const fmt=x=>Math.abs(x)<1e-9?"0":Number(x).toFixed(Math.abs(x)>=100?0:Math.abs(x)>=10?2:4).replace(/\.?0+$/,"");
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");
const L=(x1,y1,x2,y2,col=muted,w=2,dash=false)=>v.push(`<line x1="${x1.toFixed(2)}" y1="${y1.toFixed(2)}" x2="${x2.toFixed(2)}" y2="${y2.toFixed(2)}" stroke="${col}" stroke-width="${w}" ${dash?'stroke-dasharray="5 5"':""}/>`);
const T=(s,x,y,col=ink,size=17)=>v.push(`<text x="${x.toFixed(2)}" y="${y.toFixed(2)}" fill="${col}" font-size="${size}" font-weight="500">${esc(s)}</text>`);
const P=(x,y,r=5,col=teal)=>v.push(`<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${r}" fill="${col}" stroke="white" stroke-width="1.8"/>`);
const R=(x,y,w,h,fill="#f2f8f5",stroke="none")=>v.push(`<rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${Math.max(0,w).toFixed(2)}" height="${Math.max(0,h).toFixed(2)}" rx="5" fill="${fill}" stroke="${stroke}"/>`);
const curve=(fn,lo,hi,ylo,yhi,col=teal)=>{const xx=x=>65+(x-lo)/(hi-lo)*620,yy=y=>313-(y-ylo)/(yhi-ylo)*238;const chunks=[];let active=[];for(let k=0;k<=240;k++){const x=lo+(hi-lo)*k/240,y=fn(x);if(Number.isFinite(y)&&y>ylo-10*(yhi-ylo)&&y<yhi+10*(yhi-ylo)){active.push((active.length?"L":"M")+xx(x).toFixed(2)+" "+yy(y).toFixed(2));}else{if(active.length)chunks.push(active.join(" "));active=[]}}if(active.length)chunks.push(active.join(" "));for(const d of chunks)v.push(`<path d="${d}" fill="none" stroke="${col}" stroke-width="2.9" stroke-linejoin="round" stroke-linecap="round"/>`);return {x:xx,y:yy};};
const chart=(lo,hi,ylo,yhi)=>{const x=x=>65+(x-lo)/(hi-lo)*620,y=y=>313-(y-ylo)/(yhi-ylo)*238;R(48,46,657,284,"#fff");if(lo<=0&&hi>=0)L(x(0),65,x(0),326,"#c3d4d1",1.4);if(ylo<=0&&yhi>=0)L(49,y(0),707,y(0),"#c3d4d1",1.4);return{x,y}};
const bar=(x,y,value,max,label,col)=>{const len=Math.max(2,Math.abs(value)/max*480),sign=value<0?"−":"";R(x,y,len,21,col);T(label+"  "+sign+fmt(Math.abs(value)),x+8,y-6,ink,15);};
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1];
const title=["","韦达与对称多项式","牛顿恒等式与幂和","因式与余数定理","拉格朗日插值","函数方程：加法结构","复数旋转","单位根与对称筛选","切比雪夫多项式","线性递推与特征根","矩阵递推与快速幂","有限差分与求和","多项式恒等式与构造"][id];
let metric="",description="";
if(id===1){
 const roots=[-2,0.7,-1.4+3.4*u],p=roots.reduce((a,b)=>a+b,0),q=roots[0]*roots[1]+roots[0]*roots[2]+roots[1]*roots[2],r=roots.reduce((a,b)=>a*b,1);
 const ax=chart(-3,3,-1,1);L(65,196,685,196,ink,1.5);roots.forEach((x,j)=>{P(ax.x(x),196,7,[teal,blue,orange][j]);T(["x","y","z"][j],ax.x(x)+8,178,[teal,blue,orange][j]);});
 T("交换根的标签不会改变 p、q、r",80,90);T("p = x+y+z",80,277,muted);T("q = xy+yz+zx",280,277,muted);T("r = xyz",510,277,muted);
 metric=`p=${fmt(p)}；q=${fmt(q)}；r=${fmt(r)}；检验：x²+y²+z²=${fmt(p*p-2*q)}`;description="三根位置改变时，三种基本对称量由相同的根集合计算";
}
if(id===2){
 const roots=[1,2,-1.5+3*u],p=roots.reduce((a,b)=>a+b,0),q=roots[0]*roots[1]+roots[0]*roots[2]+roots[1]*roots[2],r=roots.reduce((a,b)=>a*b,1),s=[p,roots.reduce((a,b)=>a+b*b,0),roots.reduce((a,b)=>a+b*b*b,0)];
 R(76,45,610,258,"#fff");T("同一组三根的前 3 个幂和",92,84);s.forEach((x,j)=>{const L0=Math.min(500,Math.abs(x)/32*500);R(100,125+62*j,L0,24,[teal,blue,orange][j]);T("s"+(j+1)+" = "+fmt(x),110,115+62*j,ink,16)});
 metric=`s₃=${fmt(s[2])}；p·s₂−q·s₁+3r=${fmt(p*s[1]-q*s[0]+3*r)}；残差=${fmt(s[2]-(p*s[1]-q*s[0]+3*r))}`;description="根幂和 s1 s2 s3 随动根变化，牛顿恒等式左右始终一致";
}
if(id===3){
 const f=x=>(x-1)*(x-2)*(x-3),a=-.2+4.5*u,ax=chart(-.6,4.2,-7,7);
 const mapped=curve(f,-.6,4.2,-7,7,teal);[1,2,3].forEach(x=>{P(mapped.x(x),mapped.y(0),6,orange);T("x="+x,mapped.x(x)-17,mapped.y(0)+28,muted,15)});
 P(mapped.x(a),mapped.y(f(a)),7,blue);L(mapped.x(a),mapped.y(0),mapped.x(a),mapped.y(f(a)),blue,1.8,true);T("a",mapped.x(a)+10,mapped.y(0)-11,blue);
 metric=`a=${fmt(a)}，f(a)=${fmt(f(a))}；除以(x−a)的余数=${fmt(f(a))}`;description="多项式曲线与所选横坐标 a 的函数值，恰等于一次式除法的余数";
}
if(id===4){
 const y2=1+8*u,coef=(y2-3)/2,linear=(5-y2)/2,f=x=>coef*x*x+linear*x+1;
 const plot=chart(-.45,2.5,-3,11);curve(f,-.45,2.5,-3,11,teal);[[0,1],[1,2],[2,y2]].forEach((q,j)=>{P(plot.x(q[0]),plot.y(q[1]),7,[blue,purple,orange][j]);T("P("+q[0]+")",plot.x(q[0])+9,plot.y(q[1])-10,ink,14)});
 metric=`P(x)=${fmt(coef)}x²+(${fmt(linear)})x+1；三个节点残差=0`;description="拉格朗日插值曲线穿过三个互异横坐标的节点，拖动第三个纵坐标不改变前两个节点";
}
if(id===5){
 const c=.5+2.7*u,x=1.2,y=1.8;R(65,80,600,232,"#fff");T("拆成 x 和 y 后，输出仍可相加",95,110);const unit=125;
 R(96,144,unit*x,39,blue);R(96+unit*x,144,unit*y,39,orange);R(96,229,unit*(x+y),39,teal);
 T("f(x)",98,170,"white");T("f(y)",98+unit*x,170,"white");T("f(x+y)",98,255,"white");
 metric=`c=${fmt(c)}；f(x)+f(y)=${fmt(c*x+c*y)}；f(x+y)=${fmt(c*(x+y))}；残差=0`;description="任取线性函数 f(t)=ct，它保持加法；这只是连续柯西方程解的实例";
}
if(id===6){
 const a=[1.2,0.6],theta=(.08+1.82*u)*Math.PI,b=[a[0]*Math.cos(theta)-a[1]*Math.sin(theta),a[0]*Math.sin(theta)+a[1]*Math.cos(theta)],cx=364,cy=195,scale=97;
 v.push(`<circle cx="${cx}" cy="${cy}" r="${(Math.hypot(...a)*scale).toFixed(2)}" fill="none" stroke="#cadcda" stroke-width="1.6" stroke-dasharray="5 5"/>`);L(115,cy,645,cy,muted,1.4);L(cx,48,cx,343,muted,1.4);const plot=z=>[cx+scale*z[0],cy-scale*z[1]];const q=plot(a),t=plot(b);L(cx,cy,...q,blue,3);L(cx,cy,...t,orange,3);P(...q,7,blue);P(...t,7,orange);T("z",q[0]+12,q[1]-9,blue);T("eⁱθz",t[0]+12,t[1]-9,orange);
 metric=`旋转角 θ=${fmt(theta*180/Math.PI)}°；|z|=${fmt(Math.hypot(...a))}；|eⁱθz|=${fmt(Math.hypot(...b))}`;description="复平面中乘单位复数只改变有向角，不改变模长";
}
if(id===7){
 const n=3+Math.round(6*u),cx=350,cy=188,R0=119;
 v.push(`<circle cx="${cx}" cy="${cy}" r="${R0}" fill="none" stroke="#bcd5d0" stroke-width="2"/>`);L(cx-R0-35,cy,cx+R0+35,cy,"#bcd5d0",1);L(cx,cy-R0-35,cx,cy+R0+35,"#bcd5d0",1);
 const pts=Array.from({length:n},(_,k)=>[cx+R0*Math.cos(2*Math.PI*k/n),cy-R0*Math.sin(2*Math.PI*k/n)]);
 v.push(`<polygon points="${pts.map(z=>z.map(y=>y.toFixed(2)).join(",")).join(" ")}" fill="rgba(20,127,128,.05)" stroke="${teal}" stroke-width="2.5"/>`);
 pts.forEach((q,k)=>{L(cx,cy,...q,blue,1);P(...q,5,k===0?orange:teal);if(k===0)T("1",q[0]+8,q[1]-8,orange,16)});
 const sumRe=Array.from({length:n},(_,k)=>Math.cos(2*Math.PI*3*k/n)).reduce((a,b)=>a+b,0),sumIm=Array.from({length:n},(_,k)=>Math.sin(2*Math.PI*3*k/n)).reduce((a,b)=>a+b,0);
 T("单位根均匀分布在圆周上",85,45);metric=`n=${n}；|∑ωᵏ|≈0；|∑ω³ᵏ|=${fmt(Math.hypot(sumRe,sumIm))}（n整除3时为n）`;description="n 个单位根呈正 n 边形；幂和由 n 是否整除指数 3 决定";
}
if(id===8){
 const theta=Math.PI*u,x=Math.cos(theta),t3=4*x*x*x-3*x,p=chart(-1.1,1.1,-1.3,1.3);curve(z=>z,-1.1,1.1,-1.3,1.3,"#849d9a");curve(z=>2*z*z-1,-1.1,1.1,-1.3,1.3,blue);curve(z=>4*z*z*z-3*z,-1.1,1.1,-1.3,1.3,teal);P(p.x(x),p.y(t3),8,orange);T("T₁",604,82,muted,14);T("T₂",604,102,blue,14);T("T₃",604,122,teal,14);
 metric=`x=cosθ=${fmt(x)}；T₃(x)=${fmt(t3)}；cos(3θ)=${fmt(Math.cos(3*theta))}`;description="切比雪夫第三多项式 T3 在区间[-1,1]三次交替振荡，并等于三倍角余弦";
}
if(id===9){
 const k=Math.round(7*u),f=n=>2**n-1,p=chart(0,7.5,0,135);for(let j=0;j<=7;j++){const x=p.x(j),y=p.y(f(j));P(x,y,j===k?8:5,j===k?orange:teal);if(j<7)L(x,y,p.x(j+1),p.y(f(j+1)),"#b7ccc8",1.5)}T("aₙ=2ⁿ−1，特征根 1 与 2",95,55);metric=`n=${k}；aₙ=${f(k)}；aₙ₊₂−3aₙ₊₁+2aₙ=${f(k+2)-3*f(k+1)+2*f(k)}`;description="二阶线性递推的解由两个特征根的指数列线性组合构成";
}
if(id===10){
 const n=1+Math.round(10*u),F=[0,1];for(let k=2;k<=n+2;k++)F.push(F[k-1]+F[k-2]);
 R(84,62,590,250,"#fff");T("矩阵更新  Mⁿ",105,111,ink,21);const entries=[[F[n+1],F[n]],[F[n],F[n-1]]];[[0,0],[0,1],[1,0],[1,1]].forEach(([i,j])=>{const x=300+j*140,y=151+i*80;R(x-40,y-29,100,61,i===j?"#e7f4ef":"#e8f0f9");T(String(entries[i][j]),x,y+10,i===j?teal:blue,24)});
 T("n = "+n,110,174,orange,19);const det=entries[0][0]*entries[1][1]-entries[0][1]*entries[1][0];metric=`Fₙ=${F[n]}；Fₙ₊₁=${F[n+1]}；det(Mⁿ)=${det}；(−1)ⁿ=${(-1)**n}`;description="斐波那契矩阵 M 的 n 次方四个元素依次由相邻斐波那契数构成";
}
if(id===11){
 const k=Math.round(6*u),n=8,R0=42,top=90;
 T("aₙ=n²",70,75,teal);T("Δaₙ=2n+1",70,163,blue);T("Δ²aₙ=2",70,254,orange);
 for(let j=0;j<n;j++){const x=180+j*67;const fill=j===k?"#d9f3e8":"#f2f8f5";R(x,86,55,46,fill);T(String(j*j),x+17,115,ink,17);if(j<n-1){R(x,174,55,46,j===k?"#e8f0fb":"#f2f8f5");T(String(2*j+1),x+17,202,blue,17)}if(j<n-2){R(x,266,55,46,j===k?"#fff1e5":"#f8f4f0");T("2",x+22,295,orange,17)}}
 metric=`n=${k}；aₙ=${k*k}；Δaₙ=${2*k+1}；Δ²aₙ=2`;description="平方数的一阶差分为奇数列，二阶差分是常数 2";
}
if(id===12){
 const x=1+Math.round(4*u),y=1+Math.round(2*u),lhs=x**4+4*y**4,A=x*x-2*x*y+2*y*y,B=x*x+2*x*y+2*y*y;
 R(80,60,600,258,"#fff");T("把两个四次幂变成两个二次因子",104,100,ink,20);R(108,148,231,71,"#e9f4f1");R(406,148,231,71,"#eaf0fa");T("因子 A = "+A,126,194,teal,23);T("因子 B = "+B,422,194,blue,23);T("A × B",305,270,orange,20);
 metric=`x=${x}, y=${y}；x⁴+4y⁴=${lhs}；A·B=${A*B}；差=${lhs-A*B}`;description="Sophie Germain 恒等式构造两个正的二次因子，乘积恒等于四次式";
}
const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(description)}"><title>${esc(title)}</title><desc>${esc(description)}</desc><rect width="${W}" height="${H}" rx="13" fill="#fbfefd"/>${v.join("")}</svg>`;
if(!Number.isFinite(u)||/NaN|Infinity/.test(svg+metric))throw Error("Non-finite SVG scene "+id);
return{svg,metric,title,description};
}
"use strict";
document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll("[data-algebra-lesson]").forEach(root=>{
    const id=Number(root.dataset.algebraLesson),slider=root.querySelector('input[type="range"]'),stage=root.querySelector("[data-stage]"),metric=root.querySelector("[data-metric]"),state=root.querySelector("[data-state]"),reset=root.querySelector("button");
    function update(){const u=Number(slider.value)/100,view=algebraScene(id,u);stage.innerHTML=view.svg;metric.textContent=view.metric;state.textContent="参数 "+Math.round(u*100)+"% · "+view.title;}
    slider.addEventListener("input",update);reset.addEventListener("click",()=>{slider.value="50";update()});update();
  });
});
