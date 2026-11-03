"""Clase Reserva: integra cliente, servicio, duracion y estado."""

from enum import Enum

from cliente import Cliente
from entidad import EntidadBase
from excepciones import (
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from registro import obtener_logger
from servicios import Servicio


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"
    FALLIDA = "Fallida"


class Reserva(EntidadBase):
    def __init__(self, cliente, servicio, horas):
        if cliente is None or servicio is None or horas is None:
            raise ParametroFaltanteError("La reserva requiere cliente, servicio y horas")
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Cliente o servicio con tipo incorrecto")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no esta disponible")
        try:
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as error:
            # Encadenamiento de excepciones: se conserva la causa original
            raise ReservaInvalidaError("Duracion invalida para la reserva") from error
        super().__init__("RES")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = EstadoReserva.PENDIENTE
        self._costo_total = None
        self._log = obtener_logger()

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def horas(self):
        return self._horas

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self) -> bool:
        if self._estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado.value}"
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' ya no esta disponible"
            )
        self._estado = EstadoReserva.CONFIRMADA
        self._log.info("Reserva %s confirmada", self.id)
        return True

    def cancelar(self) -> bool:
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado.value}"
            )
        self._estado = EstadoReserva.CANCELADA
        self._log.info("Reserva %s cancelada", self.id)
        return True

    def procesar(self, impuesto=None, descuento=None) -> float:
        """Calcula el costo final. Usa try/except/else/finally."""
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas confirmadas (estado actual: {self._estado.value})"
            )
        try:
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except ErrorSoftwareFJ as error:
            self._estado = EstadoReserva.FALLIDA
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva {self.id}"
            ) from error
        else:
            self._costo_total = costo
            self._estado = EstadoReserva.PROCESADA
            self._log.info("Reserva %s procesada. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            self._log.info("Fin del intento de procesamiento de %s", self.id)

    def describir(self) -> str:
        total = f" | total ${self._costo_total:,.0f}" if self._costo_total else ""
        return (f"Reserva {self.id}: {self._cliente.nombre} -> {self._servicio.nombre} "
                f"({self._horas} h) [{self._estado.value}]{total}")
    