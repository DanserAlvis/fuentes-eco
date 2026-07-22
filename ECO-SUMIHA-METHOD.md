# ECO Sumiha Beta 0.5 — medición y límites

ECO Sumiha es una tipografía original de Shiro Labs construida mediante un esqueleto propio de trazos continuos. No deriva de Arimo ni copia los contornos de otra fuente. Arimo Regular se utiliza únicamente como referencia de comparación por su uso habitual en documentos y sus métricas compatibles con Arial.

## Resultado estimado

La comparación rasterizada a 11 pt y 600 dpi produce:

| Corpus | Menor cobertura negra simulada frente a Arimo Regular |
|---|---:|
| Legal | 20,01 % |
| Académico | 19,71 % |
| Oficina | 19,79 % |
| Promedio aritmético | 19,84 % |

## Cálculo exacto

1. Se renderiza exactamente el mismo texto con ECO Sumiha Beta y Arimo Regular mediante FreeType/Pillow.
2. Cada imagen se genera en escala de grises a 11 pt y 600 dpi sobre fondo blanco.
3. Para cada píxel se calcula su equivalente negro como `(255 - valor_gris) / 255`.
4. La cobertura total es la suma de los equivalentes negros de todos los píxeles. Los solapamientos rasterizados cuentan una sola vez.
5. El resultado se calcula como `100 × (1 - cobertura_Sumiha / cobertura_Arimo)`.
6. El promedio publicado es la media aritmética de los tres corpus.

El script [`measure_sumiha_universal.py`](https://github.com/DanserAlvis/fuentes-eco/blob/main/measure_sumiha_universal.py) reproduce el cálculo y contiene los textos completos empleados.

## Qué significa y qué no significa

La cifra describe una **estimación de cobertura negra rasterizada**, no miligramos de tinta, rendimiento de cartuchos, velocidad de impresión ni reducción de huella ambiental. ECO Sumiha todavía **no tiene pruebas de laboratorio ni ensayos físicos controlados**. La impresora, el controlador, la resolución, el tramado, el papel, la absorción, el tóner o tinta y la configuración de calidad pueden cambiar el resultado real.

Antes de usarla en producción se recomienda imprimir el mismo documento con ambas fuentes y medir el resultado en el equipo, papel y configuración de destino.

## Estado de la beta

- Regular 0.5 Beta.
- 122 caracteres Unicode, con español básico.
- Sin Bold, Italic ni kerning por pares terminado.
- Licencia gratuita para uso personal, académico y evaluación interna; no autoriza producción comercial ni redistribución.
- “ECO Sumiha” es un nombre comercial provisional sujeto a búsqueda formal de marcas.
