"""Clase abstracta Servicio y tres servicios especializados."""

from abc import abstractmethod

from entidad import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)


def numero_positivo(valor, campo: str) -> float:
    """Valida que 'valor' sea un numero > 0 (rechaza None, bool y texto)."""
    if valor is None:
        raise ParametroFaltanteError(f"Falta el parametro '{campo}'")
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ServicioInvalidoError(f"'{campo}' debe ser numerico, recibido: {valor!r}")
    if valor <= 0:
        raise ServicioInvalidoError(f"'{campo}' debe ser mayor que 0, recibido: {valor}")
    return float(valor)


class Servicio(EntidadBase):
    """Clase abstracta base de todos los servicios."""

    IVA = 0.19

    def __init__(self, nombre, tarifa_hora):
        if nombre is None or not str(nombre).strip():
            raise ServicioInvalidoError("El servicio requiere un nombre")
        tarifa = numero_positivo(tarifa_hora, "tarifa_hora")
        super().__init__("SRV")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = tarifa
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("'disponible' debe ser True o False")
        self._disponible = valor

    # ---- metodos abstractos (se sobrescriben en cada servicio) ----
    @abstractmethod
    def calcular_costo_base(self, horas) -> float:
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, horas) -> None:
        """Lanza ServicioInvalidoError si la duracion no es valida."""

    # ---- metodos sobrecargados (parametros opcionales) ----
    def calcular_costo(self, horas, impuesto=None, descuento=None) -> float:
        """Variantes: calcular_costo(h) | (h, impuesto) | (h, descuento=d) | (h, i, d)."""
        self.validar_parametros(horas)
        costo = self.calcular_costo_base(horas)
        if descuento is not None:
            if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) \
                    or not 0 <= descuento < 1:
                raise CalculoInconsistenteError(
                    f"Descuento invalido: {descuento!r} (debe estar entre 0 y 1)"
                )
            costo -= costo * descuento
        if impuesto is not None:
            if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) \
                    or not 0 <= impuesto <= 1:
                raise CalculoInconsistenteError(
                    f"Impuesto invalido: {impuesto!r} (debe estar entre 0 y 1)"
                )
            costo += costo * impuesto
        if costo <= 0:
            raise CalculoInconsistenteError(f"Costo final inconsistente: {costo}")
        return round(costo, 2)

    def calcular_costo_con_iva(self, horas) -> float:
        return self.calcular_costo(horas, impuesto=self.IVA)

    def calcular_costo_con_descuento(self, horas, descuento, impuesto=None) -> float:
        return self.calcular_costo(horas, impuesto=impuesto, descuento=descuento)


class ReservaSala(Servicio):
    """Reserva de salas: recargo del 15% si la capacidad supera 20 personas."""

    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        cap = numero_positivo(capacidad, "capacidad")
        if cap != int(cap) or cap > 200:
            raise ServicioInvalidoError("La capacidad debe ser un entero entre 1 y 200")
        self._capacidad = int(cap)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar_parametros(self, horas) -> None:
        h = numero_positivo(horas, "horas")
        if h > 12:
            raise ServicioInvalidoError("Una sala no se puede reservar por mas de 12 horas")

    def calcular_costo_base(self, horas) -> float:
        costo = self._tarifa_hora * horas
        return costo * 1.15 if self._capacidad > 20 else costo

    def describir(self) -> str:
        return (f"[Sala] {self.id} {self.nombre} - capacidad {self._capacidad} - "
                f"${self._tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: tarifa por hora mas un cargo fijo de manejo."""

    def __init__(self, nombre, tarifa_hora, tipo_equipo, cargo_manejo=0.0):
        super().__init__(nombre, tarifa_hora)
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise ServicioInvalidoError("Debe indicar el tipo de equipo")
        if isinstance(cargo_manejo, bool) or not isinstance(cargo_manejo, (int, float)) \
                or cargo_manejo < 0:
            raise ServicioInvalidoError("El cargo de manejo debe ser un numero >= 0")
        self._tipo_equipo = str(tipo_equipo).strip()
        self._cargo_manejo = float(cargo_manejo)

    def validar_parametros(self, horas) -> None:
        h = numero_positivo(horas, "horas")
        if h > 72:
            raise ServicioInvalidoError("Un equipo no se puede alquilar por mas de 72 horas")

    def calcular_costo_base(self, horas) -> float:
        return self._tarifa_hora * horas + self._cargo_manejo

    def describir(self) -> str:
        return (f"[Equipo] {self.id} {self.nombre} ({self._tipo_equipo}) - "
                f"${self._tarifa_hora:,.0f}/h + manejo ${self._cargo_manejo:,.0f}")


class AsesoriaEspecializada(Servicio):
    """Asesorias: la tarifa se multiplica segun el nivel del asesor."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        if not especialidad or not str(especialidad).strip():
            raise ServicioInvalidoError("Debe indicar la especialidad")
        nivel = str(nivel).strip().lower()
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel '{nivel}' no existe. Opciones: {', '.join(self.NIVELES)}"
            )
        self._especialidad = str(especialidad).strip()
        self._nivel = nivel

    def validar_parametros(self, horas) -> None:
        h = numero_positivo(horas, "horas")
        if h > 8:
            raise ServicioInvalidoError("Una asesoria no puede durar mas de 8 horas")

    def calcular_costo_base(self, horas) -> float:
        return self._tarifa_hora * self.NIVELES[self._nivel] * horas

    def describir(self) -> str:
        return (f"[Asesoria] {self.id} {self.nombre} - {self._especialidad} "
                f"({self._nivel}) - ${self._tarifa_hora:,.0f}/h base")