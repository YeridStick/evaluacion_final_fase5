import pandas as pd
import os
from datetime import date
from config import EXCEL_FILE
from models import GestionEmpleados

class DataManager:
    """Clase para gestionar la persistencia de datos en Excel."""

    @staticmethod
    def _get_columns():
        return [
            "Identificación", "Nombre", "Género", "Cargo", 
            "Días Laborados", "Fecha Registro", "Valor Día", "Total a Pagar"
        ]

    @staticmethod
    def inicializar_excel():
        """Crea el archivo Excel con encabezados si no existe."""
        if not os.path.exists(EXCEL_FILE):
            df = pd.DataFrame(columns=DataManager._get_columns())
            df.to_excel(EXCEL_FILE, index=False)

    @staticmethod
    def guardar_empleado(empleado: GestionEmpleados):
        """Guarda un nuevo empleado en el archivo Excel."""
        DataManager.inicializar_excel()
        
        # Asegurar que el cálculo de nómina esté hecho
        empleado.calcular_nomina()
        
        # Cargar datos existentes
        df = pd.read_excel(EXCEL_FILE)
        
        # Preparar nueva fila
        nueva_fila = {
            "Identificación": empleado.identificacion,
            "Nombre": empleado.nombre_completo,
            "Género": empleado.genero,
            "Cargo": empleado.cargo,
            "Días Laborados": empleado.dias_laborados,
            "Fecha Registro": empleado.fecha_registro,
            "Valor Día": empleado.valor_dia,
            "Total a Pagar": empleado.total_pagar
        }
        
        # Concatenar y guardar
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

    @staticmethod
    def existe_empleado(identificacion):
        """Verifica si un empleado con esa ID ya existe en el Excel."""
        if not os.path.exists(EXCEL_FILE):
            return False
        
        df = pd.read_excel(EXCEL_FILE)
        # Convertir a string para comparación robusta
        ids = df["Identificación"].astype(str).tolist()
        return str(identificacion) in ids

    @staticmethod
    def cargar_empleados():
        """Retorna una lista de diccionarios con todos los empleados."""
        if not os.path.exists(EXCEL_FILE):
            return []
        
        df = pd.read_excel(EXCEL_FILE)
        return df.to_dict('records')

    @staticmethod
    def eliminar_empleado(identificacion):
        """Elimina un empleado del Excel por su identificación."""
        if not os.path.exists(EXCEL_FILE):
            return
        
        df = pd.read_excel(EXCEL_FILE)
        # Filtrar fuera el empleado con esa ID
        df["Identificación"] = df["Identificación"].astype(str)
        df = df[df["Identificación"] != str(identificacion)]
        df.to_excel(EXCEL_FILE, index=False)

    @staticmethod
    def actualizar_empleado(empleado: GestionEmpleados):
        """Actualiza los datos de un empleado existente."""
        if not os.path.exists(EXCEL_FILE):
            return

        # Asegurar cálculo actualizado
        empleado.calcular_nomina()

        df = pd.read_excel(EXCEL_FILE)
        df["Identificación"] = df["Identificación"].astype(str)
        
        # Buscar el índice
        idx = df.index[df["Identificación"] == str(empleado.identificacion)].tolist()
        
        if idx:
            i = idx[0]
            df.at[i, "Nombre"]         = empleado.nombre_completo
            df.at[i, "Género"]         = empleado.genero
            df.at[i, "Cargo"]          = empleado.cargo
            df.at[i, "Días Laborados"] = empleado.dias_laborados
            df.at[i, "Valor Día"]      = empleado.valor_dia
            df.at[i, "Total a Pagar"]  = empleado.total_pagar
            # La fecha se mantiene la original o se actualiza según se prefiera
            df.to_excel(EXCEL_FILE, index=False)
