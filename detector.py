from collections import defaultdict
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
INTENTOS_PARA_ALERTA = 3


def cargar_intentos():
    intentos = defaultdict(list)

    with open("eventos.log", "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            try:
                fecha, tipo, usuario = linea.strip().split(" - ", maxsplit=2)
                fecha = datetime.strptime(fecha, FORMATO_FECHA)
            except ValueError:
                print(f"Línea {numero_linea} ignorada: formato inválido.")
                continue

            if tipo == "LOGIN_INCORRECTO":
                intentos[usuario].append(fecha)

    return intentos


def registrar_respuesta(usuario):
    fecha = datetime.now()
    fecha_texto = fecha.strftime(FORMATO_FECHA)

    with open("respuestas.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha_texto}, USUARIO_BLOQUEADO - {usuario}\n")

    return fecha


def main():
    for usuario, registros in cargar_intentos().items():
        if len(registros) < INTENTOS_PARA_ALERTA:
            continue

        inicio = registros[0]
        deteccion = registros[INTENTOS_PARA_ALERTA - 1]
        respuesta = registrar_respuesta(usuario)

        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Número de intentos fallidos:", len(registros))
        print("Primer intento:", inicio.strftime(FORMATO_FECHA))
        print("Detección:", deteccion.strftime(FORMATO_FECHA))
        print("Respuesta anotada en respuestas.log (no bloquea la cuenta).")
        print("Respuesta:", respuesta.strftime(FORMATO_FECHA))
        print("MTTD:", (deteccion - inicio).total_seconds(), "segundos")
        print("MTTR:", (respuesta - deteccion).total_seconds(), "segundos")


if __name__ == "__main__":
    main()
