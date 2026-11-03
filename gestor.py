"""Gestor central: administra listas internas (sin base de datos) y errores."""

from cliente import Cliente
from excepciones import ClienteInvalidoError, ErrorSoftwareFJ
from registro import obtener_logger
from reserva import Reserva


class GestorSistema:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._log = obtener_logger()
        self.operaciones = 0
        self.exitosas = 0
        self.fallidas = 0

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def _ejecutar(self, descripcion, funcion):
        """Ejecuta una operacion sin que un error detenga el programa.

        Devuelve el resultado, o None si hubo error (registrado en el log).
        """
        try:
            resultado = funcion()
        except ErrorSoftwareFJ as error:
            self.fallidas += 1
            causa = f" | causa original: {error.__cause__}" if error.__cause__ else ""
            self._log.error("%s -> %s: %s%s", descripcion, type(error).__name__, error, causa)
            print(f"  [ERROR] {descripcion}\n          {type(error).__name__}: {error}{causa}")
            return None
        except Exception as error:  # ultimo recurso: errores no previstos
            self.fallidas += 1
            self._log.critical("%s -> error inesperado: %r", descripcion, error, exc_info=True)
            print(f"  [ERROR INESPERADO] {descripcion}: {error!r}")
            return None
        else:
            self.exitosas += 1
            self._log.info("%s -> OK", descripcion)
            print(f"  [OK] {descripcion}")
            return resultado
        finally:
            self.operaciones += 1

    def registrar_cliente(self, nombre, documento, email, telefono):
        def accion():
            if any(c.documento == str(documento).strip() for c in self._clientes):
                raise ClienteInvalidoError(f"Ya existe un cliente con documento {documento}")
            cliente = Cliente(nombre, documento, email, telefono)
            self._clientes.append(cliente)
            return cliente

        return self._ejecutar(f"Registrar cliente {nombre!r}", accion)

    def registrar_servicio(self, clase, **datos):
        def accion():
            servicio = clase(**datos)
            self._servicios.append(servicio)
            return servicio

        return self._ejecutar(f"Crear servicio {clase.__name__} {datos.get('nombre')!r}", accion)

    def crear_reserva(self, cliente, servicio, horas):
        def accion():
            reserva = Reserva(cliente, servicio, horas)
            self._reservas.append(reserva)
            return reserva

        return self._ejecutar("Crear reserva", accion)

    def confirmar_reserva(self, reserva):
        return self._ejecutar(f"Confirmar reserva {reserva.id}", reserva.confirmar)

    def cancelar_reserva(self, reserva):
        return self._ejecutar(f"Cancelar reserva {reserva.id}", reserva.cancelar)

    def procesar_reserva(self, reserva, impuesto=None, descuento=None):
        return self._ejecutar(
            f"Procesar reserva {reserva.id}",
            lambda: reserva.procesar(impuesto, descuento),
        )
    