/* Keep essential actions visible; progressively reveal secondary controls. */
(function(){'use strict';
const oldCreator=creator,oldShopping=shopping,oldSettings=settings;
function fold(label,nodes,open=false){const d=document.createElement('details');d.className='flow-options';d.open=open;const summary=document.createElement('summary');summary.textContent=label;d.append(summary,...nodes);return d;}
creator=function(){const d=document.createElement('div');d.innerHTML=oldCreator();const dairy=d.querySelector('#maker-dairy')?.closest('label'),avoid=d.querySelector('#maker-avoid')?.closest('label');if(dairy&&avoid){const grid=dairy.parentElement;const options=fold('Preferences & ingredients to leave out',[dairy,avoid],makerDairy!=='regular'||!!makerAvoid);grid.after(options);}return d.innerHTML;};
shopping=function(){const d=document.createElement('div');d.innerHTML=oldShopping();const done=[...d.querySelectorAll('.list-item.done')];if(done.length){const parent=done[0].parentElement;parent.append(fold('Collected items ('+done.length+')',done));}const batches=[...d.querySelectorAll('.batch')];if(batches.length){const parent=batches[0].parentElement;const group=fold('Recipes on this list ('+batches.length+')',batches);parent.replaceWith(group);}return d.innerHTML;};
settings=function(){const d=document.createElement('div');d.innerHTML=oldSettings();const extra=d.querySelector('[data-action="ai-settings"]');if(extra)extra.replaceWith(fold('Advanced connection',[extra.cloneNode(true)]));const beta=[...d.querySelectorAll('section.panel')].find(p=>p.querySelector('h2')?.textContent==='Privacy & beta testing');if(beta)beta.replaceWith(fold('Help & troubleshooting',[...beta.childNodes].filter(n=>n.nodeName!=='H2')));return d.innerHTML;};
render();
})();
