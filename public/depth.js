(() => {
const root=document.documentElement;
const finePointer=matchMedia('(hover: hover) and (pointer: fine)');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const targets=[...document.querySelectorAll('.foundation-card,.role-preview a,.workforce-card,.hero-visual')];
const enabled=()=>finePointer.matches && !reduced.matches && root.dataset.motion!=='paused' && innerWidth>900;
const reset=el=>{el.classList.remove('depth-active');for(const key of ['--depth-x','--depth-y','--light-x','--light-y'])el.style.removeProperty(key);};
const states=new Map();
targets.forEach(el=>{
 const scene=el.classList.contains('hero-visual');
 const surface=scene?el.querySelector('.hero-depth-scene'):el;
 if(!surface)return;
 if(!scene)el.classList.add('depth-card');
 let bounds,frame=0,point;
 const clear=()=>{cancelAnimationFrame(frame);frame=0;bounds=null;reset(surface);};
 states.set(el,clear);
 el.addEventListener('pointerenter',e=>{if(enabled()&&e.pointerType==='mouse')bounds=el.getBoundingClientRect();});
 el.addEventListener('pointermove',e=>{
  if(!enabled()||e.pointerType!=='mouse'||el.matches(':focus-within'))return;
  bounds ||= el.getBoundingClientRect();
  point={x:Math.max(0,Math.min(1,(e.clientX-bounds.left)/bounds.width)),y:Math.max(0,Math.min(1,(e.clientY-bounds.top)/bounds.height))};
  if(frame)return;
  frame=requestAnimationFrame(()=>{frame=0;if(!enabled())return clear();const tilt=scene?5:3;surface.style.setProperty('--depth-x',`${((.5-point.y)*tilt).toFixed(2)}deg`);surface.style.setProperty('--depth-y',`${((point.x-.5)*tilt).toFixed(2)}deg`);surface.style.setProperty('--light-x',`${(point.x*100).toFixed(1)}%`);surface.style.setProperty('--light-y',`${(point.y*100).toFixed(1)}%`);surface.classList.add('depth-active');});
 });
 for(const event of ['pointerleave','pointercancel','focusin'])el.addEventListener(event,clear);
});
const resetAll=()=>states.forEach(clear=>clear());
finePointer.addEventListener('change',resetAll);reduced.addEventListener('change',resetAll);
document.querySelector('.motion-toggle')?.addEventListener('click',resetAll);
addEventListener('resize',resetAll);addEventListener('scroll',resetAll,{passive:true});
document.addEventListener('visibilitychange',()=>{if(document.hidden)resetAll();});
})();
