(() => {
const $=s=>document.querySelector(s),all=s=>[...document.querySelectorAll(s)],root=document.documentElement;
const data=JSON.parse($('#public-data').textContent);
const basePath=data.basePath||'';
const save=(k,v,session=false)=>{try{(session?sessionStorage:localStorage).setItem(k,v);}catch{}};
const text=(s,v)=>{const el=$(s);if(el)el.textContent=v;};
const press=(s,active)=>all(s).forEach(b=>b.setAttribute('aria-pressed',String(b===active)));
function theme(){const dark=root.dataset.theme==='dark';text('.theme-toggle',dark?'☼':'☾');$('.theme-toggle').setAttribute('aria-label',`Switch to ${dark?'light':'dark'} theme`);}
$('.theme-toggle').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';save('af-theme',root.dataset.theme);theme();});theme();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',e=>{try{if(!localStorage.getItem('af-theme')){root.dataset.theme=e.matches?'dark':'light';theme();}}catch{}});
function motion(){const paused=root.dataset.motion==='paused';text('.motion-toggle',paused?'Resume motion':'Pause motion');$('.motion-toggle').setAttribute('aria-pressed',String(paused));}
$('.motion-toggle').addEventListener('click',()=>{root.dataset.motion=root.dataset.motion==='paused'?'running':'paused';save('af-motion',root.dataset.motion);motion();});motion();
const menu=$('.menu-toggle'),header=$('.site-header');
const setMenu=open=>{menu.setAttribute('aria-expanded',String(open));header.classList.toggle('menu-open',open);};
menu.addEventListener('click',()=>setMenu(menu.getAttribute('aria-expanded')!=='true'));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){setMenu(false);menu.focus();}});
document.addEventListener('click',e=>{if(!header.contains(e.target))setMenu(false);});
$('#main-nav').addEventListener('click',e=>{if(e.target.closest('a'))setMenu(false);});
new ResizeObserver(()=>root.style.setProperty('--header',`${header.offsetHeight}px`)).observe(header);
// Progressive enhancement: content remains visible without JS or motion support.
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)');
const revealTargets=all('.section-heading,.hero-graph,.foundation-card,.role-preview a,.comparison-models article,.editorial-grid article,.four-steps>li,.roadmap-list li,.evolution>span');
let revealObserver;
const showAll=()=>{revealTargets.forEach(el=>el.classList.add('is-visible'));revealObserver?.disconnect();};
if('IntersectionObserver' in window && !reduceMotion.matches && root.dataset.motion!=='paused'){
 revealObserver=new IntersectionObserver(entries=>{entries.forEach(({target,isIntersecting})=>{if(isIntersecting){target.classList.add('is-visible');revealObserver.unobserve(target);}});},{threshold:.08,rootMargin:'0px 0px -20px 0px'});
 revealTargets.forEach(el=>{if(el.getBoundingClientRect().top>=innerHeight){el.classList.add('reveal-ready');const siblings=[...el.parentElement.children].filter(c=>revealTargets.includes(c));el.style.setProperty('--reveal-delay',`${Math.min(siblings.indexOf(el),3)*65}ms`);revealObserver.observe(el);}else el.classList.add('is-visible');});
}
reduceMotion.addEventListener('change',e=>{if(e.matches)showAll();});
$('.motion-toggle').addEventListener('click',()=>{if(root.dataset.motion==='paused')showAll();});
document.addEventListener('focusin',e=>{e.target.closest('.reveal-ready')?.classList.add('is-visible');});
let scrollFrame=false;
const updateScroll=()=>{scrollFrame=false;const height=root.scrollHeight-innerHeight;header.style.setProperty('--scroll-progress',String(height>0?Math.max(0,Math.min(1,scrollY/height)):0));header.classList.toggle('is-scrolled',scrollY>24);};
addEventListener('scroll',()=>{if(!scrollFrame){scrollFrame=true;requestAnimationFrame(updateScroll);}},{passive:true});
addEventListener('resize',updateScroll);updateScroll();
// Retain the original public hash destination without modifying product links.
if(location.hash==='#solution')document.getElementById('how-it-works')?.scrollIntoView();
function selectRole(i){const r=data.roles[i];press('[data-org-role]',$(`[data-org-role="${i}"]`));text('#org-name',r.name);$('#org-image').src=basePath+'/assets/'+r.image;$('#org-image').alt=r.name+' bot';text('#org-state',r.state);$('#org-state').classList.toggle('available',i===0);for(const key of ['goal','skills','tools','permissions','team','activity','approval'])text('#org-'+key,r[key]);}
all('[data-org-role]').forEach(b=>b.addEventListener('click',()=>selectRole(Number(b.dataset.orgRole))));
all('button[data-department]').forEach(b=>b.addEventListener('click',()=>{press('button[data-department]',b);const matches=all('[data-org-role]').filter(r=>{r.hidden=r.dataset.team!==b.dataset.department;return !r.hidden;});selectRole(Number(matches[0].dataset.orgRole));}));
let step=0;function selectStep(i){step=i;const w=data.workflow[i];press('[data-workflow]',$(`[data-workflow="${i}"]`));text('#workflow-title',w[0]);text('#workflow-state',w[1]);text('#workflow-description',w[2]);text('#workflow-next',i===data.workflow.length-1?'Restart walkthrough':'Next step');}
all('[data-workflow]').forEach(b=>b.addEventListener('click',()=>selectStep(Number(b.dataset.workflow))));$('#workflow-next')?.addEventListener('click',()=>selectStep((step+1)%data.workflow.length));
if($('.workflow-detail'))$('.workflow-detail').setAttribute('aria-live','polite');
const reasons=['Generating a plan does not mutate an external system.','Read-only context is allowed for assigned projects.','Read-only context is allowed for assigned projects.','Browser execution can affect a target environment and must be approved.','Creating an issue is an external write.','Publishing repository changes requires human approval.','The QA employee cannot deploy to production.','Actions without an explicit rule are denied.'];
all('[data-policy]').forEach(b=>b.addEventListener('click',()=>{const i=Number(b.dataset.policy),p=data.policy[i];press('[data-policy]',b);text('#policy-title',p[1]);text('#policy-outcome',p[2].replaceAll('_',' '));$('#policy-outcome').className='decision '+p[2].toLowerCase();text('#policy-availability',p[3]);text('#policy-reason',reasons[i]);}));
all('[data-capability]').forEach(b=>b.addEventListener('click',()=>{const c=data.capabilities[Number(b.dataset.capability)];press('[data-capability]',b);text('#capability-name',c[0]);text('#capability-status',c[1]);text('#capability-copy',c[2]);}));
// Catalog and native dialog preserve the previous search/reset/focus behavior.
if($('#agent-search')){
 const cards=all('.workforce-card'),search=$('#agent-search'),expand=$('#show-all');let department='All',expanded=false;
 const filter=()=>{const query=search.value.trim().toLowerCase(),matches=cards.filter(c=>(department==='All'||c.dataset.department===department)&&c.dataset.search.includes(query)),limit=expanded||query||department!=='All'?Infinity:9;cards.forEach(c=>c.hidden=true);matches.slice(0,limit).forEach(c=>c.hidden=false);text('#catalog-count',`Showing ${Math.min(matches.length,limit)} of ${matches.length} matching roles`);$('#catalog-empty').hidden=matches.length!==0;expand.hidden=!!query||department!=='All'||matches.length<=9;expand.textContent=expanded?'Show featured roles':'Explore all 55 roles';expand.setAttribute('aria-expanded',String(expanded));all('[data-department-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.departmentFilter===department)));save('af-catalog',JSON.stringify({department,query:search.value,expanded}),true);};
 try{const state=JSON.parse(sessionStorage.getItem('af-catalog'));if(state){if(all('[data-department-filter]').some(b=>b.dataset.departmentFilter===state.department))department=state.department;search.value=state.query||'';expanded=!!state.expanded;}}catch{}
 search.addEventListener('input',filter);all('[data-department-filter]').forEach(b=>b.addEventListener('click',()=>{department=b.dataset.departmentFilter;filter();}));$('#clear-filters').addEventListener('click',()=>{department='All';search.value='';expanded=false;filter();search.focus();});expand.addEventListener('click',()=>{expanded=!expanded;filter();if(!expanded)search.scrollIntoView({block:'center'});});filter();
 const dialog=$('#role-dialog');let opener;
 cards.forEach(card=>card.querySelector('.role-details').addEventListener('click',e=>{opener=e.currentTarget;$('#role-image').src=card.querySelector('.bot-portrait img').getAttribute('src');$('#role-image').alt=card.dataset.name+' employee bot';text('#role-title',card.querySelector('h3').textContent);text('#role-character',card.dataset.name);text('#role-category',card.dataset.department);text('#role-availability',card.querySelector('.role-status').textContent);text('#role-output',card.querySelector('.role-output').textContent);dialog.showModal();}));
 $('#close-role').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>opener?.focus());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 $('#role-next').addEventListener('click',()=>{save('af-role-inquiry',$('#role-title').textContent,true);dialog.close();});
}
$('#copy-commands')?.addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#demo-commands').textContent);text('#copy-status','Commands copied.');}catch{text('#copy-status','Select the commands to copy them manually.');}});
const form=$('#inquiry-form');if(form){
 try{const role=sessionStorage.getItem('af-role-inquiry');if(role){form.querySelector('textarea').value=`I'd like to discuss the ${role} workflow.`;sessionStorage.removeItem('af-role-inquiry');}}catch{}
 let prepared='';form.addEventListener('submit',e=>{e.preventDefault();if(!form.reportValidity())return;const values=new FormData(form),subject=`Agents Foundry — ${values.get('interest')} inquiry`,body=`${values.get('message').trim()}${values.get('name').trim()?'\n\nFrom: '+values.get('name').trim():''}`;prepared=`To: akki77parekh@gmail.com\nSubject: ${subject}\n\n${body}`;text('#draft-text',body);$('#send-mail').href=`mailto:akki77parekh@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;$('#send-gmail').href=`https://mail.google.com/mail/?view=cm&fs=1&to=akki77parekh%40gmail.com&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;$('#inquiry-draft').hidden=false;text('#inquiry-status','Draft prepared. Not sent.');$('#inquiry-draft').focus();});
 $('#copy-inquiry').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(prepared);text('#inquiry-status','Message and recipient copied. Paste into your email service to send.');}catch{text('#draft-text',prepared);text('#inquiry-status','Select the text above and copy it manually.');}});$('#edit-inquiry').addEventListener('click',()=>form.querySelector('textarea').focus());
}
})();
