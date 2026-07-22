const measurements = {
  legal: { name:"ECO Legal Serif", corpus:"Corpus jurídico en español, Regular, 11 pt; comparado con Source Serif 4.", rows:[["Base",97.5711,2.4289],["Plus",95.1666,4.8334],["Max",92.1311,7.8689]] },
  academic: { name:"ECO Academic Sans", corpus:"Corpus académico en español, Regular, 11 pt; comparado con Lato.", rows:[["Base",97.6840,2.3160],["Plus",95.1091,4.8909],["Max",92.1028,7.8972]] },
  arial: { name:"ECO Arial Compatible Sans", corpus:"Corpus académico en español, Regular, 11 pt; comparado con Arimo.", rows:[["Base",97.7053,2.2947],["Plus",95.0488,4.9512],["Max",92.1737,7.8263]] }
};
const format = value => value.toLocaleString('es-CL',{minimumFractionDigits:2,maximumFractionDigits:2});
function renderData(key) { const data=measurements[key]; document.querySelector('#resultsTable').innerHTML=data.rows.map(row=>`<tr><td>${row[0]}</td><td>${format(row[1])} %</td><td>${format(row[2])} %</td></tr>`).join(''); document.querySelector('#dataCaption').textContent=data.corpus; document.querySelectorAll('.data-choice').forEach(button=>button.classList.toggle('active',button.dataset.dataFamily===key)); }
document.querySelectorAll('.data-choice').forEach(button=>button.addEventListener('click',()=>renderData(button.dataset.dataFamily)));
const sampleText={legal:'Toda modificación deberá constar por escrito y será válida desde su firma.',academic:'La evidencia clara hace que las buenas ideas lleguen más lejos.',arial:'Documentos de oficina con métricas compatibles y una presencia directa.'};
document.querySelectorAll('.specimen-controls button').forEach(button=>button.addEventListener('click',()=>{ const key=button.dataset.family; const text=document.querySelector('#specimenText'); text.textContent=sampleText[key]; text.className='specimen-text '+key+'-text'; document.querySelectorAll('.specimen-controls button').forEach(item=>item.classList.toggle('selected',item===button)); }));
renderData('legal');
