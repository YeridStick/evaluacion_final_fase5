# Desarrollo de la actividad Fase 3 - Estructura de Datos

## 1. Síntesis del problema

La aplicación debe controlar afiliados de la Caja de Compensación “Compensándote” mediante una interfaz gráfica en Python. Debe incluir login, captura de datos del afiliado, cálculo automático de la tarifa de afiliación y manejo de tres estructuras lineales: pila, cola y lista.

  

## 2. Tabla de abstracción propuesta

  

| Clase / visibilidad                  | Propiedades / atributos                                                                                                                                                                     | Estructura                  | Métodos                                                                                                                                                                                                                                     |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Public class EstructuraDatosAfiliado | tipo_identificacion:str, numero_identificacion:str, nombre_completo:str, ingresos_actuales:float, servicio_deseado:str, modalidad_empleo:str, tarifa_afiliacion:float, fecha_afiliacion:str | Aplica a Pila, Cola y Lista | almacenar_datos()                                                                                                                                                                                                                           |
| Public class GestorAfiliados         | pila:list, cola:deque, lista:list                                                                                                                                                           | Pila, Cola, Lista           | registrar(), eliminar(), obtener_estructura(), generar_reporte()                                                                                                                                                                            |
| Public class LoginWindow             | password_var:StringVar                                                                                                                                                                      | No aplica                   | mostrar_acerca_de(), validar_ingreso()                                                                                                                                                                                                      |
| Public class MainWindow              | estructura_var, tipo_id_var, numero_id_var, nombre_var, ingresos_var, servicio_var, modalidad_var, tarifa_var, fecha_var, ver_estructura_var, reporte_var                                   | Pila, Cola, Lista           | crear_formulario(), crear_tabla(), validar_solo_numeros(), validar_solo_letras(), calcular_tarifa_base(), calcular_tarifa(), validar_campos(), registrar(), limpiar_campos(), actualizar_treeview(), mostrar_reporte(), eliminar_registro() |

  

## 3. Reglas funcionales implementadas

- Login con clave: `Caja`

- Menú “Acerca de”

- Registro con tipo de estructura: Pila, Cola o Lista

- Validación de identificación numérica

- Validación de nombre solo con letras

- Validación de ingresos numéricos

- Cálculo automático de tarifa

- Registro en memoria principal, sin base de datos

- Treeview para visualizar registros

- Reporte:

  - Pila: suma de tarifas

  - Cola: cantidad de registros

  - Lista: promedio de ingresos

- Eliminar:

  - Pila: desapilar

  - Cola: desencolar

  - Lista: eliminar por número de identificación

  

## 4. Cómo ejecutar

1. Guardar el archivo `.py`

2. Abrir terminal en la carpeta

3. Ejecutar:

   ```bash

   python Fase3YeridStickRamirezGuzman.py

   ```

  
