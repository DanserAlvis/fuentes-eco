const measurements = {
  sumiha: { corpus:"Cobertura rasterizada en escala de grises frente a Arimo Regular; 11 pt, 600 dpi. Promedio aritmético: 19,84 %. Estimación sin pruebas de laboratorio.", rows:[["Legal",79.99,20.01],["Académico",80.29,19.71],["Oficina",80.21,19.79]] },
  legal: { corpus:"Corpus jurídico en español, Regular, 11 pt; comparación con Source Serif 4.", rows:[["Base",97.5711,2.4289],["Plus",95.1666,4.8334],["Max",92.1311,7.8689]] },
  academic: { corpus:"Corpus académico en español, Regular, 11 pt; comparación con Lato.", rows:[["Base",97.6840,2.3160],["Plus",95.1091,4.8909],["Max",92.1028,7.8972]] },
  arare: { corpus:"Corpus académico en español, Regular, 11 pt; comparación con Arimo.", rows:[["Base",97.7053,2.2947],["Plus",95.0488,4.9512],["Max",92.1737,7.8263]] }
};
const format = value => value.toLocaleString('es-CL',{minimumFractionDigits:2,maximumFractionDigits:2});
function renderData(key) { const data=measurements[key]; document.querySelector('#resultsTable').innerHTML=data.rows.map(row=>`<tr><td>${row[0]}</td><td>${format(row[1])} %</td><td>${format(row[2])} %</td></tr>`).join(''); document.querySelector('#dataCaption').textContent=data.corpus; document.querySelectorAll('.data-choice').forEach(button=>button.classList.toggle('active',button.dataset.dataFamily===key)); }
document.querySelectorAll('.data-choice').forEach(button=>button.addEventListener('click',()=>renderData(button.dataset.dataFamily)));
const sampleText={sumiha:'La evidencia clara hace que las buenas ideas lleguen más lejos.',legal:'Toda modificación deberá constar por escrito y será válida desde su firma.',academic:'La evidencia clara hace que las buenas ideas lleguen más lejos.',arare:'Documentos de oficina con una presencia clara y una familia independiente.'};
document.querySelectorAll('.specimen-controls button').forEach(button=>button.addEventListener('click',()=>{ const key=button.dataset.family; const text=document.querySelector('#specimenText'); text.textContent=sampleText[key]; text.className='specimen-text '+key+'-text'; document.querySelectorAll('.specimen-controls button').forEach(item=>item.classList.toggle('selected',item===button)); }));
renderData('sumiha');
