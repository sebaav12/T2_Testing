# Tarea 2 - Análisis Dinámico
**IIC3745 Testing - UC 2024-1**

Implementación de técnicas de análisis dinámico: instrumentación, rastreo y muestreo.

## Instrumentación
Archivo: `instrumentor/profile.py`

Métricas implementadas:
- **Frecuencia**: Número de veces que se llama cada función
- **Callers**: Funciones que invocan a cada función
- **Cacheable**: Identifica funciones candidatas para implementar caché

```bash
cd instrumentor
python3 profile.py code1
```

Salida esperada:
```
fun freq cache callers
main 1 1 []
foo 1 1 ['main']
bar 2 0 ['foo']
```

## Rastreo
Archivo: `tracer/coverage_tracer.py`

Métrica implementada:
- **Frecuencia de líneas**: Líneas ejecutadas y cuántas veces

```bash
cd tracer
python3 tracer.py code2
```

Salida esperada:
```
fun line freq
factorial 2 1
factorial 4 1
factorial 5 4
factorial 6 3
factorial 7 3
factorial 8 1
```

## Muestreo
Archivo: `sampler/profile.py`

Métrica implementada:
- **Call Context Tree**: Tiempo de ejecución por contexto de llamada

```bash
cd sampler
python3 profile.py code1
```

Salida esperada:
```
total (7 seconds)
_bootstrap (7 seconds)
_bootstrap_inner (7 seconds)
run (7 seconds)
execute_script (7 seconds)
<module>(6 seconds)
main (6 seconds)
foo (6 seconds)
bar (1 seconds)
zoo (3 seconds)
bar (1 seconds)
```

## Archivos de Prueba
Carpeta `input_code/` contiene archivos de prueba para cada herramienta.

## Requisitos
- Python 3.10
- Librerías nativas utilizadas en el código base

