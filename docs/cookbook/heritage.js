/* Optional cooking labels, never inferred personal identity. */
(function(root){'use strict';
const groups={
 'African and African diaspora':['Akan','Amhara','Edo','Ewe','Fulani','Hausa','Igbo','Mandinka','Oromo','Somali','Swahili','Wolof','Yoruba','Zulu','Cape Malay','Afro-Caribbean','African American','Gullah Geechee'],
 'Indigenous Americas and Caribbean':['Cherokee','Choctaw','Diné (Navajo)','Haudenosaunee','Inuit','Mapuche','Maya','Nahua','Quechua','Garifuna','Taíno'],
 'Latin American regional and diaspora':['Oaxacan','Yucatecan','Bajan','Boricua / Puerto Rican diaspora','Cajun','Louisiana Creole','Tex-Mex','Nikkei (Japanese-Peruvian)','Chifa (Chinese-Peruvian)'],
 'Middle Eastern and North African':['Amazigh','Assyrian','Armenian','Coptic','Druze','Kurdish','Levantine','Palestinian','Persian','Bedouin'],
 'South and Central Asian':['Bengali','Gujarati','Kashmiri','Konkani','Malayali','Marathi','Punjabi','Sindhi','Tamil','Telugu','Parsi','Pashtun','Uyghur','Tibetan','Newar'],
 'East and Southeast Asian':['Cantonese','Hakka','Hokkien','Sichuan','Teochew','Hmong','Khmer','Javanese','Minangkabau','Sundanese','Peranakan','Ilocano','Kapampangan','Maranao','Cham','Okinawan','Korean American'],
 'European regional and diaspora':['Basque','Breton','Catalan','Galician','Occitan','Sámi','Sicilian','Sardinian','Romani','Italian American','Greek diaspora'],
 'Jewish culinary traditions':['Ashkenazi Jewish','Sephardic Jewish','Mizrahi Jewish','Ethiopian Jewish'],
 'Pacific peoples':['Māori','Native Hawaiian','Samoan','Tongan','CHamoru','Kanak']
};
const norm=s=>String(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/\s+/g,' ').trim();
const catalog=Object.entries(groups).flatMap(([region,names])=>names.map(name=>({name,region,target:50})));
const aliases={'navajo':'Diné (Navajo)','dine':'Diné (Navajo)','gullah':'Gullah Geechee','geechee':'Gullah Geechee','berber':'Amazigh','maori':'Māori','chamorro':'CHamoru','cantonese cuisine':'Cantonese','hakka cuisine':'Hakka'};
function labels(values){if(!Array.isArray(values)||values.length>20)throw Error('Use up to 20 traditions.');const out=[],seen=new Set();for(const raw of values){if(typeof raw!=='string')throw Error('Tradition names must be text.');let name=raw.trim().replace(/\s+/g,' ');if(!name)continue;if(name.length>80||/[\u0000-\u001f\u007f]/.test(name))throw Error('Use a tradition name of 1–80 characters.');const n=norm(name);name=aliases[n]||catalog.find(c=>norm(c.name)===n)?.name||name;if(!seen.has(norm(name))){seen.add(norm(name));out.push(name);}}return out;}
const api={catalog,norm,labels};if(typeof module!=='undefined')module.exports=api;else root.CookingHeritage=api;
})(typeof window!=='undefined'?window:globalThis);
