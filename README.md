# ECO Type

ECO Type es una colección de fuentes abiertas derivadas para documentos legales, académicos y de oficina. Las variantes ECO reducen el área de contorno rellenado de los glifos sin cambiar los avances, el kerning ni las métricas verticales del diseño de partida.

## Familias

- **ECO Tempura Serif** deriva de Source Serif 4. Está pensada para lectura extensa, contratos e informes.
- **ECO Karubi Sans** deriva de Lato. Está pensada para documentos académicos e informes.
- **ECO Arare Sans** deriva de Arimo. Está pensada para documentos de oficina. Arimo mantiene métricas de avance compatibles con Arial; ECO Arare Sans es una familia independiente, no afiliada ni respaldada por Microsoft.

Cada familia incluye Regular, Italic, Bold y Bold Italic, en tres niveles:

- **Base**: contracción geométrica de 1,2 %.
- **Plus**: contracción geométrica de 2,5 %.
- **Max**: contracción geométrica de 4,0 %. Requiere una prueba con la impresora y el papel de destino.

Los niveles no prometen un porcentaje universal de tinta ni una mayor velocidad de impresión. En el corpus y método indicados abajo, la reducción medida del área de contorno es aproximadamente 2,3–2,4 % (Base), 4,8–5,0 % (Plus) y 7,8–7,9 % (Max). El consumo físico depende además del controlador, resolución, tramado, tinta/tóner y papel.

## Medición reproducible

`measure_savings.py` compara el área rellenada de los contornos de textos españoles representativos, en Regular a 11 pt, frente a la fuente abierta de partida. No mide miligramos de tinta física ni rendimiento de cartuchos. `calculadora-tinta.html` simula la cobertura rasterizada de una hoja y solo estima masa si se proporciona un factor calibrado para la impresora.

## Licencias y avisos

Las fuentes ECO son modificaciones distribuidas bajo SIL Open Font License 1.1. Consulta el texto completo en [`LICENSES/OFL-1.1.txt`](LICENSES/OFL-1.1.txt) y los avisos de atribución en:

- [`LICENSES/NOTICE-Source-Serif-4.txt`](LICENSES/NOTICE-Source-Serif-4.txt)
- [`LICENSES/NOTICE-Lato.txt`](LICENSES/NOTICE-Lato.txt)
- [`LICENSES/NOTICE-Arimo.txt`](LICENSES/NOTICE-Arimo.txt)

Los nombres reservados de las fuentes base no se usan como nombres de familia de los archivos ECO. No se han modificado ni redistribuido Times New Roman, Arial, Calibri, Cambria o Garamond.

Los paquetes de `releases/` incluyen las cuatro variantes de estilo, el aviso de atribución correspondiente y el texto OFL 1.1. Usa esos paquetes al redistribuir una familia.

## Reconstrucción

Ejecuta `build_eco_fonts.py` con FontTools instalado. Las fuentes base variables de Source Serif 4 y Arimo están incluidas para reproducibilidad; Lato se toma de la instalación local de Windows. Verifica los resultados con `verify_eco_fonts.py`.

## Sitio y calculadora

Abre [`showcase/index.html`](showcase/index.html) para la presentación local y `calculadora-tinta.html` para la simulación de cobertura de una hoja.
