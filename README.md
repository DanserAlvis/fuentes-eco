# Fuentes ECO para documentos legales y académicos

`dist/` contiene tres familias para impresión sobria de contratos, informes y tesis:

- **ECO Legal Serif**: serif de lectura larga, basada en Source Serif 4.
- **ECO Academic Sans**: sans serif limpia para informes, basada en Lato.
- **ECO Arial Compatible Sans**: sans serif inspirada en la proporción y métricas de Arial, basada en Arimo (alternativa abierta compatible métricamente; no es Arial).

Cada familia incluye Regular, Italic, Bold y Bold Italic, en tres niveles:

- **Base**: 1,2 % de contracción; ahorro nominal de cobertura de **2,39 %**.
- **Plus**: 2,5 % de contracción; ahorro nominal de cobertura de **4,94 %**.
- **Max**: 4,0 % de contracción; ahorro nominal de cobertura de **7,84 %**. Puede percibirse en impresoras nítidas o papeles lisos.

Instala los `.ttf` con clic derecho → **Instalar para todos los usuarios**, y selecciónalas por su nombre de familia en Word, LibreOffice o LaTeX. No instales simultáneamente Base, Plus y Max de una misma familia si no necesitas compararlas: son familias separadas para evitar cambiar accidentalmente el nivel ECO.

## Diseño ECO

Cada contorno se contrae alrededor de su origen óptico. El avance, kerning y métricas verticales no cambian, de modo que un documento existente no se redistribuye. La reducción nominal de cobertura es:

`ahorro = 1 − (1 − 0,012)^2 = 2,39 %`

En impresión láser o inkjet de oficina, el punto suele ganar aproximadamente 15–40 μm sobre el contorno ideal. A 10–12 pt, la contracción aplicada equivale aproximadamente a 10–13 μm: es menor que esa expansión habitual y por eso conserva una apariencia prácticamente normal. Las impresoras y papeles varían: realiza una prueba con tu modelo antes de una tirada jurídica crítica.

La reducción de cobertura puede disminuir el uso de tóner/tinta y el tiempo de secado en inkjet, pero no asegura más páginas por minuto: esa velocidad está dominada por el mecanismo de la impresora y por la complejidad de cada página.

## Límites responsables

No se modificaron Times New Roman, Arial, Calibri, Cambria ni Garamond: sus licencias propietarias no autorizan crear redistribuciones ECO. ECO Arial Compatible Sans ofrece una alternativa abierta inspirada en Arial, pero conserva su propio nombre; estas familias no sustituyen silenciosamente fuentes instaladas.

Para reconstruir las fuentes: instala FontTools y ejecuta `build_eco_fonts.py`. El script conserva la fuente original y reproduce el proceso.

## Licencias y atribución

- ECO Legal Serif deriva de [Source Serif 4](https://github.com/adobe-fonts/source-serif), distribuida bajo SIL Open Font License 1.1.
- ECO Academic Sans deriva de [Lato](https://github.com/latofonts/lato), distribuida bajo SIL Open Font License 1.1.
- ECO Arial Compatible Sans deriva de [Arimo](https://fonts.google.com/specimen/Arimo), distribuida bajo SIL Open Font License 1.1.

Las familias ECO se distribuyen bajo SIL Open Font License 1.1. Los nombres de familia reservados de las fuentes originales no se usan en los archivos resultantes.

## Presentación y mediciones

Abre [`showcase/index.html`](showcase/index.html) para ver la presentación del proyecto, descargar las familias y consultar los resultados medidos. Los porcentajes se generan de forma reproducible con `measure_savings.py`: compara el área rellenada de los contornos de textos representativos en español contra la fuente abierta de origen. No equivalen por sí solos a miligramos de tinta física; para ello utiliza `calculadora-tinta.html` con el factor de calibración de tu impresora.
