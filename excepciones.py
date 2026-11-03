"""Excepciones personalizadas de Software FJ.

Todas heredan de ErrorSoftwareFJ para poder capturarlas de forma general
o especifica segun la necesidad.
"""


class ErrorSoftwareFJ(Exception):
    """Excepcion base del sistema."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se omitio un parametro obligatorio."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente invalidos o duplicados."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Parametros de servicio invalidos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado no esta disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Intento de reserva incorrecto o procesamiento fallido."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La operacion no es valida para el estado actual."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Calculo de costos con valores inconsistentes."""