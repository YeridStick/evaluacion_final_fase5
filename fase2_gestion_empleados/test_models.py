"""
test_models.py — Pruebas unitarias para GestionEmpleados
Ejecutar con:  python -m pytest test_models.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models import GestionEmpleados, CARGOS_VALORES


class TestCargosValores:
    def test_todos_los_cargos_definidos(self):
        cargos = ["Servicios Generales", "Administrativo",
                  "Electricista", "Mecánico", "Soldador"]
        for c in cargos:
            assert c in CARGOS_VALORES, f"Cargo '{c}' no encontrado"

    def test_valores_correctos(self):
        assert CARGOS_VALORES["Servicios Generales"] == 40_000
        assert CARGOS_VALORES["Administrativo"]      == 50_000
        assert CARGOS_VALORES["Electricista"]        == 60_000
        assert CARGOS_VALORES["Mecánico"]            == 80_000
        assert CARGOS_VALORES["Soldador"]            == 90_000


class TestGestionEmpleados:
    def _empleado(self, cargo="Mecánico", dias=12):
        return GestionEmpleados(
            identificacion  = "7719110",
            nombre_completo = "Hernando Arbey Robles",
            genero          = "Masculino",
            cargo           = cargo,
            dias_laborados  = dias,
        )

    def test_atributos_iniciales(self):
        emp = self._empleado()
        assert emp.identificacion  == "7719110"
        assert emp.nombre_completo == "Hernando Arbey Robles"
        assert emp.genero          == "Masculino"
        assert emp.cargo           == "Mecánico"
        assert emp.valor_dia       == 80_000
        assert emp.dias_laborados  == 12
        assert emp.total_pagar     == 0          # sin calcular aún

    def test_calcular_nomina_mecanico_12_dias(self):
        emp = self._empleado(cargo="Mecánico", dias=12)
        total = emp.calcular_nomina()
        assert total == 960_000                  # 80000 × 12

    def test_calcular_nomina_soldador_30_dias(self):
        emp = self._empleado(cargo="Soldador", dias=30)
        total = emp.calcular_nomina()
        assert total == 2_700_000               # 90000 × 30

    def test_calcular_nomina_servicios_1_dia(self):
        emp = self._empleado(cargo="Servicios Generales", dias=1)
        total = emp.calcular_nomina()
        assert total == 40_000

    def test_formula_general(self):
        for cargo, valor_dia in CARGOS_VALORES.items():
            for dias in (1, 5, 15, 30):
                emp = self._empleado(cargo=cargo, dias=dias)
                assert emp.calcular_nomina() == valor_dia * dias

    def test_fecha_registro_no_nula(self):
        from datetime import date
        emp = self._empleado()
        assert emp.fecha_registro == date.today()

    def test_repr(self):
        emp = self._empleado()
        emp.calcular_nomina()
        r = repr(emp)
        assert "GestionEmpleados" in r
        assert "Mecánico" in r