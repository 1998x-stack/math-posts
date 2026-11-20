/* Three.js math scenes for Q04 / Q05 / Q13 / Q17.
 * Pinned MIT dependency: https://github.com/mrdoob/three.js/tree/r160
 * Network/WebGL failure must leave the independently authored SVG visible.
 */
const CDN = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
const nodes = [...document.querySelectorAll('[data-three-scene]')];
if (nodes.length) {
  import(CDN).then(THREE => nodes.forEach(node => {
    try { mount(THREE, node); }
    catch (error) {
      node.dataset.ready = 'false';
      const output = node.querySelector('.scene-readout');
      if (output) output.textContent = '当前显示静态 SVG 图解；三维场景不可用。';
      console.warn('[math3d] fallback:', error);
    }
  })).catch(error => {
    nodes.forEach(node => {
      node.dataset.ready = 'false';
      const output = node.querySelector('.scene-readout');
      if (output) output.textContent = 'Three.js 未载入，继续显示完整 SVG 图解。';
    });
    console.warn('[math3d] CDN offline; SVG fallback active:', error);
  });
}
function mount(T, root) {
  const type = root.dataset.threeScene;
  const canvas = root.querySelector('canvas');
  if (!canvas || !window.WebGLRenderingContext) throw new Error('WebGL unavailable');
  const scene = new T.Scene(); scene.background = new T.Color('#f0f8f5');
  const camera = new T.PerspectiveCamera(40, 1, .05, 200);
  camera.up.set(0, 0, 1);
  const renderer = new T.WebGLRenderer({canvas, alpha:false, antialias:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  const ambient = new T.AmbientLight(0xffffff, .75);scene.add(ambient);
  const light = new T.DirectionalLight(0xffffff, 1);light.position.set(4, 5, 8);scene.add(light);
  const blue = new T.MeshStandardMaterial({color:0x88c6bf,transparent:true,opacity:.27,side:T.DoubleSide,depthWrite:false});
  const orange = new T.MeshStandardMaterial({color:0xe5a476,transparent:true,opacity:.40,side:T.DoubleSide,depthWrite:false});
  const edgeMaterial = new T.LineBasicMaterial({color:0x217d86});
  const auxMaterial = new T.LineBasicMaterial({color:0xd17853});
  const meshMaterial = new T.MeshStandardMaterial({color:0xd97655});
  const V = (x,y,z) => new T.Vector3(x,y,z);
  function line(a,b,material=edgeMaterial) {
    const g = new T.BufferGeometry().setFromPoints([a,b]);
    const o = new T.Line(g,material);scene.add(o);return o;
  }
  function ball(p,r=.045,color=0xd97655) {
    const o = new T.Mesh(new T.SphereGeometry(r,14,10),new T.MeshStandardMaterial({color}));
    o.position.copy(p);scene.add(o);return o;
  }
  function shape(vertices,material) {
    const g=new T.BufferGeometry().setFromPoints(vertices);
    const mesh = new T.Mesh(g,material);
    // Each supplied face is triangulated explicitly.
    scene.add(mesh);return mesh;
  }
  function triangle(a,b,c,material) {
    const g = new T.BufferGeometry();
    g.setAttribute('position',new T.Float32BufferAttribute([...a.toArray(),...b.toArray(),...c.toArray()],3));
    g.computeVertexNormals();
    const m=new T.Mesh(g,material);scene.add(m);
  }
  // Axes have fixed, math-coordinate directions (z is vertical in this project).
  const xAxis=new T.LineBasicMaterial({color:0xb66d5a}), yAxis=new T.LineBasicMaterial({color:0x6595c3}), zAxis=new T.LineBasicMaterial({color:0x409879});
  line(V(0,0,0),V(1.6,0,0),xAxis);line(V(0,0,0),V(0,1.6,0),yAxis);line(V(0,0,0),V(0,0,1.6),zAxis);
  const sliders=[...root.querySelectorAll('input[data-param]')];
  const output=root.querySelector('.scene-readout');
  let dynamic=null,center=V(0.4,0.4,0.4),radius=4,yaw=.7,pitch=.6;
  const setOutput=s=>{ if(output)output.textContent=s; };
  if(type==='cube'){
    const cube=new T.Mesh(new T.BoxGeometry(1,1,1),blue);cube.position.set(.5,.5,.5);scene.add(cube);
    const edges=new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(1,1,1)),edgeMaterial);
    edges.position.copy(cube.position);scene.add(edges);
    const A=V(0,0,1),C=V(1,1,1);ball(A);ball(C);
    const p=ball(V(.5,.5,0),.065);
    const pa=line(p.position,A,auxMaterial),pc=line(p.position,C,auxMaterial);
    function update(){const x=+sliders.find(s=>s.dataset.param==='x').value,y=+sliders.find(s=>s.dataset.param==='y').value;
      p.position.set(x,y,0);
      pa.geometry.dispose();pc.geometry.dispose();
      pa.geometry=new T.BufferGeometry().setFromPoints([p.position,A]);
      pc.geometry=new T.BufferGeometry().setFromPoints([p.position,C]);
      const value=(x-.5)**2+(y-.5)**2+.5;
      setOutput('P=('+x.toFixed(2)+','+y.toFixed(2)+',0)；PA·PC='+value.toFixed(4)+'；范围 [0.5,1]');render();
    }
    sliders.forEach(s=>s.addEventListener('input',update));
    center=V(.5,.5,.5);radius=3.1;dynamic=update;
  } else if(type==='sphere'){
    const sphere=new T.Mesh(new T.SphereGeometry(1,48,24),blue);scene.add(sphere);
    const wire=new T.LineSegments(new T.EdgesGeometry(new T.SphereGeometry(1,16,8)),edgeMaterial);scene.add(wire);
    const q=ball(V(1,0,0),.07);
    function update(){const phi=+sliders[0].value*Math.PI*2, theta=+sliders[1].value*Math.PI;
      q.position.set(Math.sin(theta)*Math.cos(phi),Math.sin(theta)*Math.sin(phi),Math.cos(theta));
      setOutput('球半径 r=3：体积 V=36π；表面积 S=36π。滑块改变观察的球面点。');render();}
    sliders.forEach(s=>s.addEventListener('input',update));radius=3.4;dynamic=update;
  } else if(type==='skew'){
    const plane=new T.Mesh(new T.PlaneGeometry(2.6,2.6),blue);plane.position.set(.5,.4,-.015);scene.add(plane);
    line(V(0,-.9,0),V(0,1.6,0),edgeMaterial); // l
    line(V(-.6,-.15,.8),V(1.5,1.1,.8),auxMaterial); // m, skew to l
    const p=ball(V(.5,.5,0),.065);
    function update(){const x=+sliders[0].value,y=+sliders[1].value;
      p.position.set(x,y,0);const dl=x;
      const k=.6,h=.8,d2=Math.sqrt(((y-.6*x)**2)/(1+.6*.6)+h*h);
      setOutput('平面点 P=('+x.toFixed(2)+','+y.toFixed(2)+')；到 l 距离='+dl.toFixed(3)+'，到 m 距离≈'+d2.toFixed(3));render();}
    sliders.forEach(s=>s.addEventListener('input',update));center=V(.25,.3,.35);radius=3.8;dynamic=update;
  } else if(type==='tetra'){
    const D=V(0,0,0),A=V(-Math.sqrt(3),0,0),B=V(0,1,0),C=V(-Math.sqrt(3),2,0),P=V(0,0,1);
    triangle(A,B,C,blue);triangle(P,A,B,orange);
    [[A,B],[B,C],[C,A],[P,A],[P,B],[P,C]].forEach(([a,b])=>line(a,b,edgeMaterial));
    line(D,P,auxMaterial);line(D,A,auxMaterial);line(D,B,auxMaterial);
    [D,A,B,C,P].forEach((p,i)=>ball(p,.052,i===4?0xd56c47:0x277a88));
    center=V(-.7,.75,.3);radius=4.7;
    sliders.forEach(s=>{s.closest('label').hidden=true;});
    setOutput('D 为正交投影点。二面角 P−AB−C 是钝角，cos θ = −√21/7。拖动模型观察。');
  }
  function pose(){const cp=Math.cos(pitch),sp=Math.sin(pitch);
    camera.position.set(center.x+radius*cp*Math.cos(yaw),center.y+radius*cp*Math.sin(yaw),center.z+radius*sp);
    camera.lookAt(center);}
  function resize(){const w=Math.max(280,Math.floor(root.clientWidth-24)),ht=Math.max(240,Math.min(380,Math.round(w*.56)));
    renderer.setSize(w,ht,false);camera.aspect=w/ht;camera.updateProjectionMatrix();render();}
  function render(){pose();renderer.render(scene,camera);}
  let down=null;
  canvas.style.touchAction='none';
  canvas.addEventListener('pointerdown',event=>{down={x:event.clientX,y:event.clientY};canvas.setPointerCapture(event.pointerId);});
  canvas.addEventListener('pointermove',event=>{if(!down)return;
    yaw+=(event.clientX-down.x)*.008;pitch=Math.min(1.45,Math.max(-1.2,pitch+(down.y-event.clientY)*.008));
    down={x:event.clientX,y:event.clientY};render();});
  canvas.addEventListener('pointerup',()=>{down=null;});canvas.addEventListener('pointercancel',()=>{down=null;});
  canvas.addEventListener('wheel',event=>{event.preventDefault();radius=Math.min(15,Math.max(1.7,radius*(event.deltaY>0?1.08:.92)));render();},{passive:false});
  const reset=root.querySelector('[data-reset]');
  if(reset)reset.addEventListener('click',()=>{yaw=.7;pitch=.6;radius=type==='tetra'?4.7:type==='skew'?3.8:type==='cube'?3.1:3.4;render();});
  root.dataset.ready='true';
  resize();if(dynamic)dynamic();
  window.addEventListener('resize',resize);
  if('ResizeObserver' in window)new ResizeObserver(resize).observe(root);
}
