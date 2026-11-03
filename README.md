# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Curso Programación (213023) – UNAD. Sistema orientado a objetos, sin base de datos: todo se maneja con objetos y listas; los archivos se usan solo para el log de eventos y errores.

## Ejecución

    python main.py

Requiere Python 3.8 o superior, sin librerías externas. El log se genera en `logs/software_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| excepciones.py | Excepciones personalizadas (jerarquía desde ErrorSoftwareFJ) |
| registro.py | Configuración del archivo de logs |
| entidad.py | Clase abstracta EntidadBase |
| cliente.py | Cliente con validaciones y encapsulación |
| servicios.py | Servicio (abstracta) + ReservaSala, AlquilerEquipo, AsesoriaEspecializada |
| reserva.py | Reserva y EstadoReserva: confirmar, cancelar, procesar |
| gestor.py | GestorSistema: listas internas y captura central de errores |
| main.py | Simulación de 30 operaciones válidas e inválidas |

## Conceptos aplicados

- Abstracción: EntidadBase y Servicio (métodos abstractos).
- Herencia y polimorfismo: los 3 servicios sobrescriben calcular_costo_base, validar_parametros y describir.
- Encapsulación: atributos privados con @property y setters que validan.
- Sobrecarga: Python no tiene sobrecarga nativa; se simula con parámetros opcionales en calcular_costo(horas, impuesto=None, descuento=None) y las variantes calcular_costo_con_iva y calcular_costo_con_descuento.
- Manejo de excepciones: try/except/else/finally en GestorSistema._ejecutar y Reserva.procesar; encadenamiento con raise ... from en Reserva.
- Logs: cada error y evento relevante se registra en logs/software_fj.log.

## Integrantes

- (nombre 1)
- (nombre 2)
- (nombre 3)
- (nombre 4)
- (nombre 5)