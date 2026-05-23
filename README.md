# Evaluacion final - Estructura de Datos (UNAD)

Aplicacion integradora de la Fase 5.  
Este modulo lanza las fases 2, 3 y 4 sin reescribir su logica interna.

## Archivo principal

- `.\evaluacion_final\evaluacion_final.py`

## Ejecucion (PowerShell)

Desde la raiz del proyecto (`C:\Users\yerid\Downloads\evaluacion_final`):

```powershell
python .\evaluacion_final\evaluacion_final.py
```

Tambien funciona entrando a la carpeta `evaluacion_final` y ejecutando:

```powershell
python .\evaluacion_final.py
```

## Acceso

- Contrasena del integrador: `8246`
- Si la contrasena es incorrecta, se muestra mensaje de error.

## Menu principal

1. Abrir Fase 2 - Gestion de empleados  
   Archivo ejecutado: `fase2_gestion_empleados\main.py`
2. Abrir Fase 3 - Estructuras lineales  
   Archivo ejecutado: `fase3_data_structure\Fase3YeridStickRamirezGuzman.py`
3. Abrir Fase 4 - Arbol binario  
   Archivo ejecutado: `fase4_arbol_binario\Fase4YeridRamirez.py`
4. Salir

## Como se lanzan las fases

- Se usa `subprocess.Popen` con `sys.executable`.
- Cada fase se abre como proceso independiente.
- Se valida que el archivo exista antes de ejecutarlo.
- Se usa `cwd` apuntando a la carpeta de cada fase para que funcionen imports y archivos relativos.

## Integracion de logins internos

Para evitar doble login al abrir desde el integrador:

- Se envia argumento: `--from-integrator`
- Se envia variable de entorno: `RUN_FROM_INTEGRATOR=true`

Si cada fase se ejecuta sola, mantiene su comportamiento original.

## Dependencias de Fase 2

La Fase 2 usa `pandas` y `openpyxl`.

Si aparece `ModuleNotFoundError: No module named 'pandas'`, instala en el mismo Python que use el integrador:

```powershell
<ruta_python_del_integrador> -m pip install --user pandas openpyxl
```

Ejemplo:

```powershell
C:\Python314\python.exe -m pip install --user pandas openpyxl
```
