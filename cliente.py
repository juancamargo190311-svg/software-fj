"""Clase Cliente con validaciones robustas y datos personales encapsulados."""

import re

from entidad import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    def __init__(self, nombre, documento, email, telefono):
        # Los setters validan; si algo falla no se consume ningun ID.
        self.nombre = nombre
        self._documento = self._validar_documento(documento)
        self.email = email
        self.telefono = telefono
        super().__init__("CLI")

    # --- documento: solo lectura (no se puede modificar luego) ---
    @staticmethod
    def _validar_documento(valor) -> str:
        if valor is None:
            raise ParametroFaltanteError("El documento es obligatorio")
        valor = str(valor).strip()
        if not (valor.isdigit() and 6 <= len(valor) <= 12):
            raise ClienteInvalidoError(
                f"Documento invalido '{valor}': debe tener 6 a 12 digitos"
            )
        return valor

    @property
    def documento(self) -> str:
        return self._documento

    # --- nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El nombre es obligatorio")
        valor = str(valor).strip()
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError(
                f"Nombre invalido '{valor}': minimo 3 letras, sin numeros ni simbolos"
            )
        self._nombre = valor

    # --- email ---
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El email es obligatorio")
        valor = str(valor).strip()
        if not _EMAIL.match(valor):
            raise ClienteInvalidoError(f"Email invalido: '{valor}'")
        self._email = valor

    # --- telefono ---
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El telefono es obligatorio")
        valor = str(valor).strip()
        if not (valor.isdigit() and 7 <= len(valor) <= 10):
            raise ClienteInvalidoError(
                f"Telefono invalido '{valor}': debe tener 7 a 10 digitos"
            )
        self._telefono = valor

    def describir(self) -> str:
        return f"Cliente {self.id}: {self.nombre} (doc. ***{self._documento[-3:]}) <{self.email}>"
    