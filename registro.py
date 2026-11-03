"""Configuracion del archivo de logs (unico uso de archivos del sistema)."""

import logging
from pathlib import Path

RUTA_LOG = Path(__file__).parent / "logs" / "software_fj.log"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, configurado una sola vez."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:
        RUTA_LOG.parent.mkdir(exist_ok=True)
        logger.setLevel(logging.INFO)
        formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger
