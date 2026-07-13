
(() => {
  "use strict";
  const root=document.documentElement, body=document.body;
  const set=(key,on)=>localStorage.setItem(key,on?"1":"0");
  const get=key=>localStorage.getItem(key)==="1";
  function apply(){body.classList.toggle("high-contrast",get("pd-contrast"));body.classList.toggle("links-underlined",get("pd-links"));root.classList.toggle("font-large",get("pd-font"));
    [["contrast-toggle","pd-contrast"],["font-toggle","pd-font"],["links-toggle","pd-links"]].forEach(([id,key])=>{const el=document.getElementById(id);if(el)el.setAttribute("aria-pressed",String(get(key)));});}
  function bind(id,key){document.getElementById(id)?.addEventListener("click",()=>{set(key,!get(key));apply();});}
  apply();bind("contrast-toggle","pd-contrast");bind("font-toggle","pd-font");bind("links-toggle","pd-links");
  const search=document.getElementById("resource-search"), category=document.getElementById("resource-category"), format=document.getElementById("resource-format"), clear=document.getElementById("resource-clear"), empty=document.getElementById("resource-empty");
  function filter(){const q=(search?.value||"").toLowerCase(),c=category?.value||"",f=format?.value||"";let shown=0;document.querySelectorAll("#resource-list .resource-card").forEach(card=>{const ok=(!q||card.textContent.toLowerCase().includes(q))&&(!c||card.dataset.category===c)&&(!f||card.dataset.format===f);card.hidden=!ok;if(ok)shown++;});if(empty)empty.hidden=shown>0;}
  [search,category,format].forEach(el=>el?.addEventListener("input",filter));clear?.addEventListener("click",()=>{if(search)search.value="";if(category)category.value="";if(format)format.value="";filter();});
})();
