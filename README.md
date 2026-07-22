# ECO Type

ECO Type es una colección de tipografías para documentos legales, académicos y de oficina. Publica el método, los resultados y los límites de cada medición; ninguna cifra representa una garantía de consumo físico de tinta.

## Fuente estrella: ECO Sumiha Beta

**ECO Sumiha Beta 0.5** es una sans humanista original de Shiro Labs, construida desde cero con trazos continuos y sin perforaciones visibles. Frente a Arimo Regular, la simulación rasterizada a 11 pt y 600 dpi estima 20,01 % menos cobertura negra en el corpus legal, 19,71 % en el académico y 19,79 % en oficina: **19,84 % de promedio aritmético**.

La fuente no tiene pruebas de laboratorio. El resultado no equivale a miligramos de tinta, rendimiento de cartuchos, velocidad de impresión ni reducción ambiental garantizada. La fórmula, los corpus y el procedimiento están publicados en [`ECO-SUMIHA-METHOD.md`](ECO-SUMIHA-METHOD.md).

La beta se distribuye sin costo para uso personal, académico y evaluación interna bajo la [`Shiro Labs ECO Sumiha Free Beta License 1.0`](LICENSES/ECO-SUMIHA-BETA-LICENSE.txt). No autoriza producción comercial, redistribución, modificación ni embedding. Las versiones futuras o derechos comerciales podrán ofrecerse mediante pago. “ECO Sumiha” es un nombre provisional sujeto a búsqueda formal de marcas.

## Familias derivadas abiertas

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

ECO Tempura, ECO Karubi y ECO Arare son modificaciones distribuidas bajo SIL Open Font License 1.1. ECO Sumiha utiliza una licencia beta propietaria distinta. Consulta el texto OFL en [`LICENSES/OFL-1.1.txt`](LICENSES/OFL-1.1.txt) y los avisos de atribución en:

- [`LICENSES/NOTICE-Source-Serif-4.txt`](LICENSES/NOTICE-Source-Serif-4.txt)
- [`LICENSES/NOTICE-Lato.txt`](LICENSES/NOTICE-Lato.txt)
- [`LICENSES/NOTICE-Arimo.txt`](LICENSES/NOTICE-Arimo.txt)

Los nombres reservados de las fuentes base no se usan como nombres de familia de los archivos ECO. No se han modificado ni redistribuido Times New Roman, Arial, Calibri, Cambria o Garamond.

Los paquetes de `releases/` incluyen las cuatro variantes de estilo, el aviso de atribución correspondiente y el texto OFL 1.1. Usa esos paquetes al redistribuir una familia.

## Reconstrucción

Ejecuta `build_eco_fonts.py` para las familias derivadas y `build_sumiha_universal.py` para ECO Sumiha. Las dependencias del generador original están declaradas en `requirements-font-build.txt`. Verifica Sumiha con `measure_sumiha_universal.py` y las familias derivadas con `verify_eco_fonts.py`.

## Sitio y calculadora

Abre [`showcase/index.html`](showcase/index.html) para la presentación local y `calculadora-tinta.html` para la simulación de cobertura de una hoja.
