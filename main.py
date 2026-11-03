"""Software FJ - Sistema integral de gestion de clientes, servicios y reservas.

Ejecutar:  python main.py
Simula mas de 10 operaciones (validas e invalidas) sin base de datos.
Los errores y eventos quedan en logs/software_fj.log
"""

from gestor import GestorSistema
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def titulo(texto):
    print(f"\n=== {texto} ===")


def main():
    g = GestorSistema()

    titulo("1. Registro de clientes (validos e invalidos)")
    ana = g.registrar_cliente("Ana Gomez", "1052345678", "ana@correo.com", "3101234567")
    carlos = g.registrar_cliente("Carlos Perez", "79456123", "carlos@correo.com", "3209876543")
    g.registrar_cliente("Luis Mora", "1000111222", "correo-malo", "3001112233")       # email invalido
    g.registrar_cliente("Ana Duplicada", "1052345678", "otra@correo.com", "3101234567")  # documento repetido
    g.registrar_cliente(None, "12345678", "x@correo.com", "3001112233")               # parametro faltante
    g.registrar_cliente("Marta Ruiz", "12ab", "marta@correo.com", "3001112233")       # documento invalido

    titulo("2. Creacion de servicios (correcta e incorrecta)")
    sala = g.registrar_servicio(ReservaSala, nombre="Sala Ejecutiva", tarifa_hora=50000, capacidad=30)
    equipo = g.registrar_servicio(AlquilerEquipo, nombre="Videobeam HD", tarifa_hora=15000,
                                  tipo_equipo="Proyector", cargo_manejo=10000)
    asesoria = g.registrar_servicio(AsesoriaEspecializada, nombre="Asesoria Python",
                                    tarifa_hora=80000, especialidad="Backend", nivel="senior")
    g.registrar_servicio(ReservaSala, nombre="Sala Fantasma", tarifa_hora=-100, capacidad=10)  # tarifa negativa
    g.registrar_servicio(AsesoriaEspecializada, nombre="Asesoria X", tarifa_hora=70000,
                         especialidad="Datos", nivel="dios")                                  # nivel inexistente
    g.registrar_servicio(AlquilerEquipo, nombre="Equipo sin tipo", tarifa_hora=5000, tipo_equipo="")

    titulo("3. Polimorfismo: describir() y costo de cada servicio por 2 horas")
    for s in g.servicios:
        print(f"  {s.describir()}")
        print(f"     base ${s.calcular_costo(2):,.0f} | con IVA ${s.calcular_costo_con_iva(2):,.0f} "
              f"| con 10% desc. e IVA ${s.calcular_costo_con_descuento(2, 0.10, 0.19):,.0f}")

    titulo("4. Reservas exitosas")
    r1 = g.crear_reserva(ana, sala, 3)
    g.confirmar_reserva(r1)
    g.procesar_reserva(r1, impuesto=0.19)

    r2 = g.crear_reserva(carlos, equipo, 24)
    g.confirmar_reserva(r2)
    g.procesar_reserva(r2, impuesto=0.19, descuento=0.10)

    titulo("5. Reservas fallidas")
    g.crear_reserva(ana, sala, 20)            # excede 12 horas
    g.crear_reserva(None, sala, 2)            # cliente faltante
    g.crear_reserva(carlos, asesoria, "dos")  # duracion no numerica

    r3 = g.crear_reserva(carlos, asesoria, 2)
    g.procesar_reserva(r3)                    # sin confirmar -> operacion no permitida
    g.confirmar_reserva(r3)
    g.procesar_reserva(r3, descuento=1.5)     # descuento inconsistente -> queda FALLIDA (excepcion encadenada)
    g.confirmar_reserva(r3)                   # ya no es PENDIENTE

    r4 = g.crear_reserva(ana, equipo, 5)
    g.cancelar_reserva(r4)
    g.confirmar_reserva(r4)                   # cancelada: no se puede confirmar

    equipo.disponible = False
    g.crear_reserva(ana, equipo, 2)           # servicio no disponible
    equipo.disponible = True

    titulo("6. Resumen final")
    for r in g.reservas:
        print(f"  {r}")
    print(f"\n  Operaciones: {g.operaciones} | Exitosas: {g.exitosas} | Con error controlado: {g.fallidas}")
    print("  El programa termino sin interrupciones. Revisa logs/software_fj.log")


if __name__ == "__main__":
    main()