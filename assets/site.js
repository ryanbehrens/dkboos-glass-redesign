// Shared behaviour for every page

// nav state
const nav=document.getElementById('nav');
if(nav){
  const onScroll=()=>nav.classList.toggle('scrolled',scrollY>60);
  addEventListener('scroll',onScroll,{passive:true});onScroll();
}

// services dropdown (click for touch / keyboard, hover handled in CSS)
document.querySelectorAll('.has-drop>button').forEach(b=>{
  b.addEventListener('click',e=>{e.stopPropagation();const p=b.parentElement;const o=p.classList.toggle('open');b.setAttribute('aria-expanded',o)});
});
addEventListener('click',()=>document.querySelectorAll('.has-drop.open').forEach(p=>{p.classList.remove('open');p.querySelector('button').setAttribute('aria-expanded','false')}));

// mobile menu
(()=>{
  const btn=document.getElementById('menuBtn'),menu=document.getElementById('mobileMenu');
  if(!btn||!menu)return;
  const set=o=>{document.body.classList.toggle('menu-open',o);btn.setAttribute('aria-expanded',o);menu.setAttribute('aria-hidden',!o)};
  btn.addEventListener('click',()=>set(!document.body.classList.contains('menu-open')));
  menu.addEventListener('click',e=>{if(e.target.closest('a'))set(false)});
  addEventListener('keydown',e=>{if(e.key==='Escape')set(false)});
})();

// reveal on scroll
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transitionDelay=(i%4)*80+'ms';io.observe(el)});

// open/closed indicator (Pacific time)
(()=>{try{
  const el=document.getElementById('openText');if(!el)return;
  const now=new Date(new Date().toLocaleString('en-US',{timeZone:'America/Los_Angeles'}));
  const d=now.getDay(),h=now.getHours();const open=d>0&&d<6&&h>=8&&h<17;
  el.textContent=(open?'Open now':'Closed now')+' · Mon–Fri 8–5 · 1206 Franz St SE, Lacey';
  if(!open)document.querySelectorAll('.dot').forEach(d=>d.style.background='#9fd3ef');
}catch(e){}})();

// pre-select a project type from ?type= on the contact page
(()=>{const t=new URLSearchParams(location.search).get('type');if(!t)return;
  const box=document.querySelector(`.picks input[data-type="${t}"]`);if(box){document.querySelectorAll('.picks input').forEach(i=>i.checked=false);box.checked=true}})();

// form demo
const form=document.getElementById('form');
if(form)form.addEventListener('submit',e=>{e.preventDefault();document.getElementById('formBody').style.display='none';document.getElementById('sent').style.display='block'});
