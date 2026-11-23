gsap.registerPlugin(MotionPathPlugin);
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const FPS=30, DUR=14.4;
const tl=gsap.timeline({paused:true});
window.tl=tl;
// deterministic rng
function rnd(seed){let x=Math.sin(seed*127.1+311.7)*43758.5453;return x-Math.floor(x);}
const TICKS=[],CLICKS=[],WHOOSH=[];

/* ---------------- section visibility ---------------- */
gsap.set('#sChalk,#sUI',{autoAlpha:0});gsap.set('#sChalk',{filter:'blur(0px) brightness(1)'});
tl.set('#sDark',{autoAlpha:0},3.9).set('#sChalk',{autoAlpha:1},3.9);
tl.set('#ch20',{autoAlpha:0},0).set('#ch19',{autoAlpha:0},5.1).set('#ch20',{autoAlpha:1},5.1);
tl.set('#sChalk',{autoAlpha:0},7.9);

/* ---------------- S1 hook ---------------- */
const slabs=$('#slabs');
const SL=[];
for(let i=0;i<9;i++){const d=document.createElement('div');d.className='slab';
 const c=[ '#ff1f3a','#00e1ff','#ffffff'][i%3];
 d.style.cssText+=`top:${560+rnd(i)*420}px;width:${180+rnd(i+20)*380}px;height:${30+rnd(i+40)*60}px;background:${c};opacity:.0`;
 slabs.appendChild(d);SL.push(d);}
SL.forEach((d,i)=>{tl.fromTo(d,{x:-600+rnd(i+60)*300,opacity:.95},{x:600+rnd(i+80)*500,opacity:0,duration:.28,ease:'power2.in',immediateRender:true},0.0+rnd(i+90)*0.12);});
gsap.set('#L1 .w',{opacity:0});
tl.set('#L1 .w',{opacity:1},0.06);
gsap.set('#L2',{y:70,opacity:0,filter:'blur(14px)'});gsap.set('#L3',{y:80,opacity:0,filter:'blur(16px)'});
tl.to('#L2',{y:0,opacity:1,filter:'blur(0px)',duration:.32,ease:'expo.out'},1.46);
tl.to('#L3',{y:0,opacity:1,filter:'blur(0px)',duration:.3,ease:'expo.out'},2.18);
tl.fromTo('#L3w',{scale:1.12},{scale:1,duration:.5,ease:'expo.out',immediateRender:false},2.18);
gsap.set('#strike',{scaleX:0});
tl.to('#strike',{scaleX:1,duration:.22,ease:'power3.out'},2.6);TICKS.push(2.62);
tl.fromTo('#hook',{scale:1},{scale:1.035,duration:2.8,ease:'none',transformOrigin:'540px 900px',immediateRender:false},0);
/* ---------------- S2 三道坎 ---------------- */
tl.to('#hook',{scale:.5,y:-330,duration:.42,ease:'expo.inOut',transformOrigin:'540px 560px'},2.8);
gsap.set('.kan',{opacity:0,y:140,scale:.82});
tl.to('.kan',{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.5)',stagger:.1},3.04);
tl.to('#k1,#k2',{opacity:.35,scale:.94,duration:.3,ease:'power2.out'},3.42);
tl.to('#k3',{scale:1.07,duration:.35,ease:'back.out(2)'},3.42);
tl.to('#k3 .ring',{opacity:1,duration:.2},3.42);TICKS.push(3.44);
tl.to('#sDark .glow',{x:120,y:-80,duration:3.9,ease:'none'},0);

/* ---------------- S19 chapter ---------------- */
WHOOSH.push([3.86,.5]);
gsap.set('#chT',{clipPath:'inset(0% 72% 0% 0%)'});
tl.to('#chT',{clipPath:'inset(0% 0% 0% 0%)',duration:.34,ease:'power2.out'},3.9);
gsap.set('#prog .pg',{opacity:.3,y:24});
tl.to('#prog .pg',{opacity:1,y:0,duration:.3,ease:'expo.out',stagger:.04},3.9);
tl.fromTo('#ch19',{scale:1},{scale:1.04,duration:1.2,ease:'none',immediateRender:false},3.9);
tl.fromTo('#pg3',{scale:1},{scale:1.12,duration:.3,ease:'back.out(2)',immediateRender:false},4.35);
/* ---------------- S20 pain ---------------- */
gsap.set('#pT',{clipPath:'inset(45% 0% 0% 0%)',y:30});
tl.to('#pT',{clipPath:'inset(0% 0% 0% 0%)',y:0,duration:.4,ease:'expo.out'},5.1);
gsap.set('#pA,#pB',{opacity:0,y:80,scale:.9});
gsap.set('#pA,#pB',{opacity:.55});tl.to('#pA',{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.4)'},5.1);
tl.to('#pB',{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.4)'},5.2);
$$('.dr').forEach((p,i)=>{const L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L;
  tl.to(p,{strokeDashoffset:0,duration:.5,ease:'power2.inOut'},5.14+(i<3?0:0.1)+(i%3)*0.07);});
gsap.set('#labA,#labB',{opacity:0,y:30});
tl.to('#labA',{opacity:1,y:0,duration:.4,ease:'expo.out'},5.5);
tl.to('#labB',{opacity:1,y:0,duration:.4,ease:'expo.out'},5.6);
['xA1','xA2','xB1','xB2'].forEach(id=>{const p=document.getElementById(id);p.style.opacity=0;const L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L;});
function cross(px,a,b,t0){
  tl.set('#'+a+',#'+b,{opacity:1},t0);
  tl.to('#'+a,{strokeDashoffset:0,duration:.14,ease:'power2.out'},t0);
  tl.to('#'+b,{strokeDashoffset:0,duration:.14,ease:'power2.out'},t0+.12);
  tl.to('#'+px+' > svg:first-child, #'+px+' .lab',{opacity:.35,duration:.2},t0+.05);
  tl.fromTo('#'+px,{x:0},{keyframes:{x:[0,-14,12,-7,4,0]},duration:.3,immediateRender:false},t0+.02);
  TICKS.push(t0+.02);
}
cross('pA','xA1','xA2',6.56);
cross('pB','xB1','xB2',7.44);
tl.fromTo('#ch20',{scale:1},{scale:1.04,duration:2.5,ease:'none',immediateRender:false},5.1);
// zoom-through out of chalk
tl.to('#sChalk',{scale:1.4,filter:'blur(18px) brightness(1.3)',duration:.26,ease:'power2.in'},7.6);
WHOOSH.push([7.58,.6]);

/* ---------------- S21 UI ---------------- */
tl.set('#sUI',{autoAlpha:1},7.82);
tl.fromTo('#sUI',{opacity:0},{opacity:1,duration:.06,immediateRender:false},7.82);
tl.fromTo('#sUI',{scale:1.25,filter:'blur(14px)'},{scale:1,filter:'blur(0px)',duration:.38,ease:'expo.out',immediateRender:false},7.82);
tl.to('#b1',{x:200,y:160,duration:6.6,ease:'sine.inOut'},7.8);
tl.to('#b2',{x:-220,y:-120,duration:6.6,ease:'sine.inOut'},7.8);
// camera states for #page
const CAM={
 E0:{transformOrigin:'420px 520px',x:60,y:540,scale:1.3,rotationX:32,rotationY:-22,rotationZ:9},
 E1:{transformOrigin:'400px 520px',x:60,y:500,scale:1.38,rotationX:26,rotationY:-15,rotationZ:6},
 ZA:{transformOrigin:'341px 366px',x:199,y:520,scale:2.55,rotationX:0,rotationY:0,rotationZ:0},
 ZV:{transformOrigin:'425px 695px',x:115,y:240,scale:2.42,rotationX:0,rotationY:0,rotationZ:0},
};
gsap.set('#page',CAM.E0);
tl.to('#page',{...CAM.E1,duration:1.15,ease:'sine.out'},7.8);
tl.to('#page',{...CAM.ZA,duration:.42,ease:'power3.inOut'},8.95);
// map markers
const pbA=$('#pbA rect'),pbV=$('#pbV rect');
tl.to(pbA,{strokeDashoffset:0,duration:.3,ease:'power2.inOut'},8.36);TICKS.push(8.4);
tl.to(pbV,{strokeDashoffset:0,duration:.3,ease:'power2.inOut'},8.6);TICKS.push(8.64);
tl.to('#pbA,#pbV',{opacity:0,duration:.18},8.95);
const pills=$('#pills');
function mkPill(n,txt){const d=document.createElement('div');d.className='pill';d.innerHTML=`<span class="num">${n}</span>${txt}`;pills.appendChild(d);return d;}
const P1=mkPill('1','创建数字分身'),P2=mkPill('2','创建我的声音');
gsap.set([P1,P2],{opacity:0,scale:.6});
tl.to(P1,{opacity:1,scale:1,duration:.4,ease:'back.out(2)'},8.42);
tl.to(P2,{opacity:1,scale:1,duration:.4,ease:'back.out(2)'},8.66);
tl.to([P1,P2],{opacity:0,scale:.9,duration:.18},8.95);
// HUD
gsap.set('#brand',{opacity:0});gsap.set('#brandT',{y:90});
tl.set('#brand',{opacity:1},7.98);
tl.to('#brandT',{y:0,duration:.45,ease:'expo.out'},8.0);
tl.fromTo('#brand svg',{scale:0,rotation:-90},{scale:1,rotation:0,duration:.5,ease:'back.out(1.8)',immediateRender:false},7.98);
tl.to('#brandT',{y:-90,duration:.2,ease:'power2.in'},8.9);tl.to('#brand svg',{scale:0,duration:.18},8.9);tl.set('#brand',{opacity:0},9.1);
gsap.set('#modT',{y:90});gsap.set('#modP',{scale:0});
tl.set('#mod',{opacity:1},9.08);
tl.to('#modP',{scale:1,duration:.4,ease:'back.out(2)'},9.08);
tl.to('#modT',{y:0,duration:.45,ease:'expo.out'},9.12);
tl.set('#disc',{color:'rgba(255,255,255,.62)'},0);
tl.set('#disc',{color:'rgba(20,26,36,.55)'},7.78);
// card hover
tl.to('#cardA',{borderColor:'#2058d9',boxShadow:'0 0 0 3px rgba(32,88,217,.15)',backgroundColor:'#f5f8ff',duration:.12},9.14);

/* measure helpers */
function rectAt(t,sel){tl.seek(t,false);const r=$(sel).getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height,cx:r.left+r.width/2,cy:r.top+r.height/2};}
const CUR=$('#cur');
gsap.set(CUR,{x:980,y:1700,opacity:0});
function curMove(t0,dur,to,bend=0.18){
  tl.to(CUR,{duration:dur,ease:'power2.inOut',motionPath:{path:[{x:to.via?to.via.x:null,y:to.via?to.via.y:null},{x:to.x,y:to.y}].filter(p=>p.x!==null),curviness:1.2}},t0);
}
function click(t,x,y){
  tl.to(CUR,{scale:.82,duration:.07,ease:'power2.out'},t).to(CUR,{scale:1,duration:.16,ease:'back.out(3)'},t+.07);
  tl.set('#rip',{left:x,top:y,scale:.2,opacity:1},t+.02).to('#rip',{scale:1.1,opacity:0,duration:.42,ease:'expo.out'},t+.02);
  CLICKS.push(t);
}
// click on avatar card
const pA=rectAt(9.4,'#cardA .ptile');
tl.to(CUR,{opacity:1,duration:.15},8.82);
tl.fromTo(CUR,{x:960,y:1560},{x:pA.cx-4,y:pA.cy-2,duration:.42,ease:'power3.inOut',immediateRender:false},8.84);
click(9.24,pA.cx,pA.cy);
const cA=rectAt(9.31,'#cardA');
// card expands into dialog A (clip reveal, content already laid out → no blank frame)
function reveal(sel,c,t0,dur,top,h){
  const ins=`inset(${c.y-top}px ${1030-(c.x+c.w)}px ${top+h-(c.y+c.h)}px ${c.x-50}px round 26px)`;
  tl.set(sel,{opacity:1,clipPath:ins},t0);
  tl.to(sel,{clipPath:'inset(0px 0px 0px 0px round 40px)',duration:dur,ease:'expo.inOut'},t0);
  tl.set(sel,{clipPath:'none'},t0+dur+.01);
}
reveal('#dA',cA,9.3,.34,300,1740);
tl.to('#shade',{opacity:1,duration:.3},9.3);
tl.fromTo('#cam',{filter:'blur(0px)'},{filter:'blur(7px)',duration:.3,immediateRender:false},9.3);
gsap.set('#dA .st',{y:36,opacity:.4});
tl.to('#dA .st',{opacity:1,y:0,duration:.36,ease:'expo.out',stagger:.03},9.32);
// cursor to scan button
tl.to(CUR,{x:900,y:820,duration:.5,ease:'power3.inOut'},9.5);
tl.to('#up1',{borderColor:'#2058d9',borderStyle:'solid',backgroundColor:'#f4f8ff',duration:.15},9.95);
tl.to('#scanBtn',{backgroundColor:'#1a49b8',duration:.12},9.98);
// red box on scan button (dialog-local → screen)
const RB=$('#rb'),RBR=$('#rbR'),RBS=$('#rbS');
function rbox(t0,t1,sel,pad=14,when){
  const r=rectAt(when||t0+.05,sel);
  const w=r.w+pad*2,h=r.h+pad*2;
  tl.set(RB,{left:r.x-pad,top:r.y-pad,width:w,height:h,opacity:1},t0);
  tl.set(RBS,{attr:{width:w,height:h}},t0);
  tl.set(RBR,{attr:{x:0,y:0,width:w,height:h},strokeDashoffset:1},t0);
  tl.to(RBR,{strokeDashoffset:0,duration:.32,ease:'power2.inOut'},t0);
  tl.to(RB,{opacity:0,duration:.15},t1);
  TICKS.push(t0+.05);
}
rbox(9.72,10.22,'#scanBtn',14,9.95);
tl.to(CUR,{opacity:0,duration:.15},10.2);
// scroll dialog A to photos
tl.to('#dA',{y:-620,duration:.44,ease:'power3.inOut'},10.22);
WHOOSH.push([10.22,.18]);
// generate effect
tl.fromTo('#arrow',{x:0,scale:1},{keyframes:{x:[0,10,0,10,0],scale:[1,1.25,1,1.25,1]},duration:.6,immediateRender:false},10.46);
tl.set('#scan',{opacity:1},10.55);
tl.fromTo('#veil',{clipPath:'inset(0% 0% 0% 0%)'},{clipPath:'inset(100% 0% 0% 0%)',duration:.5,ease:'power1.inOut',immediateRender:false},10.55);
tl.fromTo('#scan',{yPercent:-100},{yPercent:0,duration:.5,ease:'power1.inOut',immediateRender:false},10.55);
tl.to('#scan',{opacity:0,duration:.15},11.05);
tl.to('#plOut',{color:'#2058d9',duration:.2},11.0);
rbox(11.08,11.55,'#phOut',14,11.1);
tl.fromTo('#dA',{scale:1},{scale:1.02,duration:1.2,ease:'none',transformOrigin:'50% 40%',immediateRender:false},10.6);

/* ---------------- S22 voice ---------------- */
tl.to('#dA',{y:-2300,duration:.4,ease:'power3.in'},11.54);
tl.to('#shade',{opacity:0,duration:.3},11.6);
tl.to('#cam',{filter:'blur(0px)',duration:.3},11.6);
tl.to('#cardA',{borderColor:'#e0e4e7',boxShadow:'0 0 0 0px rgba(32,88,217,0)',backgroundColor:'#fafcfe',duration:.1},11.6);
tl.to('#page',{...CAM.ZV,duration:.42,ease:'power3.inOut'},11.58);
WHOOSH.push([11.54,.35]);
tl.to('#modP',{scale:0,duration:.14},11.72);
tl.to('#modT',{y:-90,duration:.22,ease:'power2.in'},11.72);
tl.set('#modP',{innerText:'模块②'},11.86).set('#modT',{innerText:'创建我的声音',y:90},11.86);
tl.to('#modP',{scale:1,duration:.35,ease:'back.out(2)'},11.86);
tl.to('#modT',{y:0,duration:.4,ease:'expo.out'},11.9);
const pV=rectAt(12.05,'#cardV .ptile');
tl.set(CUR,{x:860,y:1330},11.8);
tl.to(CUR,{opacity:1,duration:.12},11.82);
tl.to(CUR,{x:pV.cx-4,y:pV.cy-2,duration:.3,ease:'power3.inOut'},11.86);
tl.to('#cardV',{borderColor:'#2058d9',boxShadow:'0 0 0 3px rgba(32,88,217,.15)',backgroundColor:'#f5f8ff',duration:.1},12.08);
click(12.16,pV.cx,pV.cy);
const cV=rectAt(12.22,'#cardV');
reveal('#dB',cV,12.22,.32,300,1160);
tl.to('#shade',{opacity:1,duration:.28},12.22);
tl.to('#cam',{filter:'blur(7px)',duration:.28},12.22);
gsap.set('#dB .sb2',{opacity:.4,y:36});
tl.to('#dB .sb2',{opacity:1,y:0,duration:.36,ease:'expo.out',stagger:.025},12.24);
tl.to(CUR,{x:880,y:1340,duration:.4,ease:'power3.inOut'},12.3);
// reading sweep
$$('#ta .ln b').forEach((b,i)=>{tl.to(b,{width:'100%',duration:.11,ease:'none'},12.5+i*.1);});
// press record
const rB=rectAt(13.0,'#recBtn');
tl.to(CUR,{x:rB.cx+40,y:rB.cy-6,duration:.22,ease:'power3.inOut'},12.74);
click(12.98,rB.cx+44,rB.cy);
tl.to('#recBtn',{backgroundColor:'#1a49b8',duration:.1},12.99);
tl.to('#ta .ln',{opacity:0,duration:.14},13.0);
tl.to('#wave',{opacity:1,duration:.14},13.02);
gsap.set('#ring',{scale:.5});
tl.to('#ring',{opacity:1,scale:1,duration:.4,ease:'back.out(1.7)'},13.02);
tl.to('#ringP',{strokeDashoffset:0,duration:.55,ease:'power1.inOut'},13.08);
tl.to(CUR,{opacity:0,duration:.2},13.3);
tl.fromTo('#ringOK',{scale:0,opacity:0},{scale:1,opacity:1,duration:.35,ease:'back.out(2.2)',immediateRender:false},13.88);TICKS.push(13.9);
tl.fromTo('#ring',{scale:1},{keyframes:{scale:[1,1.06,1]},duration:.3,immediateRender:false},13.88);
tl.fromTo('#dB',{scale:1},{scale:1.02,duration:1.3,ease:'none',transformOrigin:'50% 50%',immediateRender:false},13.1);
tl.to('#stage',{duration:.01},DUR);

/* wave bars */
const W=$('#wave');const NB=34;const bars=[];
for(let i=0;i<NB;i++){const b=document.createElement('div');b.className='abs';b.style.cssText=`left:${i*(804/NB)+3}px;width:${804/NB-9}px;border-radius:12px;background:linear-gradient(180deg,#7aa2f4,#2058d9)`;W.appendChild(b);bars.push(b);}

/* subtitles */
const CUES=[[2.8,3.9,'是这三道坎'],[5.1,6.4,'第三道坎 出镜'],[6.4,7.9,'不想露脸 也没空拍'],[7.9,9.3,'Sphere的数字分身'],[9.3,11.8,'传1张照片 生成形象'],[11.8,12.88,'读一段文字'],[12.88,14.41,'录15秒 克隆声音']];
const STX=$('#stx'),SBAR=$('#sbar');let lastCue=null;
function updateSubs(t){
  const c=CUES.find(c=>t>=c[0]&&t<c[1]);
  if(!c){STX.textContent='';SBAR.style.opacity=0;return;}
  if(STX.textContent!==c[2])STX.textContent=c[2];
  const a=Math.min(1,(t-c[0])/0.1);STX.style.opacity=a;
  const w=STX.getBoundingClientRect().width;
  SBAR.style.width=(w+30)+'px';SBAR.style.opacity=(t>=7.9?1:0)*a;
}
function update(t){
  // glitch hook L1
  const L1=$('#L1');const r=L1.querySelector('.r'),c=L1.querySelector('.c'),w=L1.querySelector('.w');
  if(t>=0.06&&t<0.56){const k=1-(t-0.06)/0.5;const f=Math.floor(t*60);
    const o=22*k+6*k*rnd(f);r.style.transform=`translateX(${-o}px)`;c.style.transform=`translateX(${o}px)`;
    r.style.opacity=c.style.opacity=Math.min(1,k*1.6);
    const a=rnd(f+3)*80,b=a+10+rnd(f+5)*60;w.style.clipPath=k>0.25?`polygon(0 0,100% 0,100% ${a}%,${(rnd(f+7)-.5)*30}% ${a}%,${(rnd(f+7)-.5)*30}% ${b}%,100% ${b}%,100% 100%,0 100%)`:'none';
    w.style.transform=`translateX(${(rnd(f+9)-.5)*40*k}px)`;
  } else {r.style.opacity=c.style.opacity=0;w.style.clipPath='none';w.style.transform='none';}
  // subtle glitch on L3 entry
  // wave
  if(t>=13.0){const frozen=t>=13.88;const tt=frozen?13.88:t;
    bars.forEach((b,i)=>{const env=Math.sin(Math.PI*(i+0.5)/NB);let a=frozen?env*(0.55+0.45*Math.abs(Math.sin(i*1.3))):env*(0.25+0.75*Math.abs(Math.sin(tt*11+i*0.9)*Math.cos(tt*5.3+i*0.37)));
      const h=Math.max(18,a*270);b.style.height=h+'px';b.style.top=(140-h/2)+'px';});}
  // ring number
  const p=Math.max(0,Math.min(1,(t-13.08)/0.55));const e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
  $('#ringNum').textContent=Math.round(15*(p<=0?0:(p>=1?1:(1-Math.cos(Math.PI*p))/2)));
  // pills follow cards (projected)
  if(t>=8.3&&t<9.2){const a=$('#cardA').getBoundingClientRect(),v=$('#cardV').getBoundingClientRect();
    const w1=P1.offsetWidth,w2=P2.offsetWidth;P1.style.left=Math.min(a.right+18,1040-w1)+'px';P1.style.top=(a.top+a.height*0.30-42)+'px';
    P2.style.left=Math.min(v.right+18,1040-w2)+'px';P2.style.top=Math.max(v.bottom+14,a.top+a.height*0.30+70)+'px';}
  // grain
  const f=Math.floor(t*FPS);$('#grain').style.backgroundPosition=`${Math.floor(rnd(f)*512)}px ${Math.floor(rnd(f+1)*512)}px`;
  updateSubs(t);
}
window.seek=function(t){tl.seek(t,false);update(t);};
window.META={TICKS,CLICKS,WHOOSH,DUR,FPS};
tl.seek(0);
