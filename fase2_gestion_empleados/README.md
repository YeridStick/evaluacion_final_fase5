# Fase 2: Abstracción y Diseño - Gestión de Nómina

Este proyecto consiste en una aplicación de escritorio desarrollada en Python para la empresa **"Constructora Mejor"**. La aplicación permite gestionar el pago de nómina de los empleados mediante un proceso de abstracción de datos y programación orientada a objetos.

## 📋 Características

- **Seguridad**: Control de acceso mediante contraseña genérica enmascarada.
- **Gestión de Empleados**: Registro de identificación, nombre, género, cargo y días laborados.
- **Cálculo Automático**: Determinación del salario por día según el cargo seleccionado y cálculo del total a pagar.
- **Reportes**: Generación de un resumen detallado con la información del trabajador.
- **Persistencia en Excel**: Guardado automático de datos en archivo estático (`empleados.xlsx`), permitiendo edición manual y carga masiva.
- **Gestión Avanzada**: Funciones para editar y eliminar registros directamente desde la aplicación.

## 🛠️ Tecnologías y Requerimientos

- **Lenguaje**: Python 3.x.
- **IDE**: Visual Studio Code.
- **Interfaz Gráfica**: Tkinter.
- **Persistencia**: Pandas y Openpyxl (Manejo de archivos Excel).
- **Paradigma**: Programación Orientada a Objetos (POO).

## Instalación y Ejecución

1. Asegúrate de tener Python instalado.
2. Clona este repositorio o descarga el archivo .zip.
3. Abre la carpeta del proyecto en Visual Studio Code.
4. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```

## Acceso a la Aplicación

 Para ingresar a la interfaz de registro, utilice la siguiente credencial:
- **Contraseña**: 4682

## Persistencia de Datos
La aplicación utiliza un archivo de Excel estático llamado `empleados.xlsx` ubicado en la raíz del proyecto para almacenar de forma permanente la información de los empleados. Esto permite consultar, editar o eliminar registros incluso después de cerrar la aplicación.

## Estructura de la Abstracción

El corazón de la aplicación es la clase pública `GestionEmpleados`, la cual encapsula los atributos del trabajador y el método para el cálculo de nómina basado en la siguiente lógica:

| Cargo | Salario por Día |
| :--- | :--- |
| Servicios Generales | $ 40.000 |
| Administrativo | $ 50.000 |
| Electricista | $ 60.000 |
| Mecánico | $ 80.000 |
| Soldador | $ 90.000 |

## Propuestas de Mejora (Visión del Desarrollador)

Para una versión más robusta y profesional de esta aplicación, se proponen las siguientes mejoras:

### 1. Robustez y Seguridad
- **Framework Web**: Migrar a frameworks como FastAPI o Flask para implementar una API robusta que maneje autenticación mediante **JWT (JSON Web Tokens)**.
- **Seguridad de Credenciales**: Eliminar contraseñas en código (hardcoded) y almacenarlas con hashing seguro en una base de datos.
- **Auditoría de Acceso**: Implementar una tabla de registros (logs) en la base de datos para controlar fechas y horas de acceso.

### 2. Gestión de Datos y Persistencia
- **Base de Datos Relacional**: Utilizar un motor como SQLite o PostgreSQL para mantener un registro histórico de empleados, evitando la pérdida de datos al cerrar la aplicación.
- **Listado y Búsqueda**: Añadir una sección de consulta para listar empleados activos e inactivos, con búsqueda aproximada por nombre o número de identificación.
- **Historial de Reintegro**: Mantener datos de empleados que ya no laboran para facilitar procesos futuros de reintegro o consultar antecedentes internos.

### 3. Flexibilidad en Nómina y Contratación
- **Tipos de Contrato**: Ampliar la lógica para manejar contratos por obra, prestación de servicios o por horas, ajustando el pago de forma dinámica.
- **Compensaciones Adicionales**: Incluir cálculos para horas extras, bonificaciones por esfuerzo y otros recargos legales.
- **Módulo de Facturación**: Integrar un sistema de facturación o generación de colillas de pago (prendas) más avanzado.

### 4. Experiencia de Usuario e Identidad
- **Diseño Personalizado**: Ajustar la interfaz con una identidad visual más cercana a la marca de la constructora (colores corporativos, logos y tipografía específica).
- **Sistema de Mensajería**: Implementar un módulo de comunicación interna para notificaciones o avisos entre el personal administrativo.

## Autor

- **Nombre**: Yerid Stick Ramirez Guzman
- **Curso**: Estructura de Datos - UNAD
- **Código del Curso**: 301305
