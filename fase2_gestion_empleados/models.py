from datetime import date

# Tabla de cargos y valores por día de trabajo
CARGOS_VALORES = {
    "Servicios Generales": 40000,
    "Administrativo":      50000,
    "Electricista":        60000,
    "Mecánico":            80000,
    "Soldador":            90000,
}

class GestionEmpleados:
    """
    Clase pública que almacena los datos de un empleado y
    proporciona el método de cálculo de nómina.

    Atributos
    ---------
    identificacion : str
        Número de identificación del empleado.
    nombre_completo : str
        Nombre completo del empleado.
    genero : str
        Género del empleado ('Masculino' | 'Femenino').
    cargo : str
        Cargo laboral del empleado.
    valor_dia : int
        Valor en pesos colombianos del día de trabajo según el cargo.
    dias_laborados : int
        Cantidad de días laborados en el periodo.
    fecha_registro : date
        Fecha en que se registró el empleado (generada automáticamente).
    total_pagar : int
        Total calculado a pagar al empleado.
    """

    def __init__(
        self,
        identificacion: str,
        nombre_completo: str,
        genero: str,
        cargo: str,
        dias_laborados: int,
    ) -> None:
        self.identificacion: str  = identificacion
        self.nombre_completo: str = nombre_completo
        self.genero: str          = genero
        self.cargo: str           = cargo
        self.valor_dia: int       = CARGOS_VALORES.get(cargo, 0)
        self.dias_laborados: int  = dias_laborados
        self.fecha_registro: date = date.today()
        self.total_pagar: int     = 0

    # ------------------------------------------------------------------
    # Método principal de cálculo
    # ------------------------------------------------------------------
    def calcular_nomina(self) -> int:
        """
        Calcula el total a pagar al empleado.

        Fórmula
        -------
            total_pagar = valor_dia  *  dias_laborados

        Returns
        -------
        int
            Valor total a pagar en pesos colombianos.
        """
        self.total_pagar = self.valor_dia * self.dias_laborados
        return self.total_pagar

    # ------------------------------------------------------------------
    # Representación textual (útil para depuración)
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"GestionEmpleados("
            f"id={self.identificacion!r}, "
            f"nombre={self.nombre_completo!r}, "
            f"cargo={self.cargo!r}, "
            f"dias={self.dias_laborados}, "
            f"total=${self.total_pagar:,}"
            f")"
        )