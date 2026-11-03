"""Clase abstracta que representa las entidades generales del sistema."""

import itertools
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Base abstracta de Cliente, Servicio y Reserva.

    Genera un identificador unico y obliga a las clases hijas a
    implementar describir().
    """

    _contador = itertools.count(1)

    def __init__(self, prefijo: str):
        self._id = f"{prefijo}-{next(EntidadBase._contador):04d}"

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripcion legible de la entidad."""

    def __str__(self) -> str:
        return self.describir()