from abc import ABC, abstractmethod
from datetime import datetime


# =========================
# FUNCION PARA LOGS
# =========================

def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")


# =========================
# EXCEPCIONES PERSONALIZADAS
# =========================

class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


# =========================
# CLASE ABSTRACTA
# =========================

class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# =========================
# CLASE CLIENTE
# =========================

class Cliente(Entidad):

    def __init__(self, nombre, correo):

        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if "@" not in correo:
            raise ClienteError("Correo inválido")

        self.__nombre = nombre
        self.__correo = correo

    def mostrar_info(self):
        return f"Cliente: {self.__nombre}"

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo


# =========================
# CLASE ABSTRACTA SERVICIO
# =========================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        if tarifa <= 0:
            raise ServicioError("La tarifa debe ser mayor a 0")

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =========================
# RESERVA DE SALAS
# =========================

class ReservaSala(Servicio):

    def calcular_costo(self, horas):

        if horas <= 0:
            raise ServicioError("Horas inválidas")

        return self.tarifa * horas

    def descripcion(self):
        return f"Reserva de sala: {self.nombre}"


# =========================
# ALQUILER DE EQUIPOS
# =========================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, dias):

        if dias <= 0:
            raise ServicioError("Días inválidos")

        return self.tarifa * dias

    def descripcion(self):
        return f"Alquiler de equipo: {self.nombre}"


# =========================
# ASESORIAS
# =========================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, sesiones):

        if sesiones <= 0:
            raise ServicioError("Sesiones inválidas")

        return self.tarifa * sesiones

    def descripcion(self):
        return f"Asesoría especializada: {self.nombre}"


# =========================
# CLASE RESERVA
# =========================

class Reserva:

    def __init__(self, cliente, servicio, tiempo):

        if tiempo <= 0:
            raise ReservaError("Tiempo inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.tiempo = tiempo
        self.estado = "Pendiente"

    def confirmar(self):

        try:

            costo = self.servicio.calcular_costo(self.tiempo)

        except Exception as e:

            registrar_log(f"ERROR AL CALCULAR COSTO: {e}")

            raise ReservaError("No fue posible procesar la reserva") from e

        else:

            self.estado = "Confirmada"

            registrar_log(
                f"Reserva confirmada para {self.cliente.get_nombre()}"
            )

            print("--------------------------------")
            print("RESERVA EXITOSA")
            print(self.cliente.mostrar_info())
            print(self.servicio.descripcion())
            print(f"Total: ${costo}")
            print("--------------------------------")

        finally:

            registrar_log("Proceso de confirmación finalizado")

    def cancelar(self):

        self.estado = "Cancelada"

        registrar_log(
            f"Reserva cancelada para {self.cliente.get_nombre()}"
        )

        print("Reserva cancelada")


# =========================
# LISTA DE OPERACIONES
# =========================

operaciones = [

    ("Juan", "juan@gmail.com",
     ReservaSala("Sala VIP", 50), 2),

    ("Ana", "correo_malo",
     ReservaSala("Sala Básica", 30), 2),

    ("Pedro", "pedro@gmail.com",
     AlquilerEquipo("Portátil", 40), -1),

    ("Laura", "laura@gmail.com",
     AsesoriaEspecializada("Python", 100), 3),

    ("", "vacio@gmail.com",
     ReservaSala("Sala Ejecutiva", 60), 2),

    ("Carlos", "carlos@gmail.com",
     AlquilerEquipo("VideoBeam", 25), 4),

    ("María", "maria@gmail",
     AsesoriaEspecializada("Redes", 120), 1),

    ("Luis", "luis@gmail.com",
     ReservaSala("Sala Premium", 80), 0),

    ("Camila", "camila@gmail.com",
     AlquilerEquipo("Computador", 35), 5),

    ("Andrés", "andres@gmail.com",
     AsesoriaEspecializada("Bases de Datos", 150), 2)

]


# =========================
# EJECUCION DEL SISTEMA
# =========================

print("======================================")
print("      SOFTWARE FJ - SISTEMA")
print("======================================")

for datos in operaciones:

    try:

        cliente = Cliente(
            datos[0],
            datos[1]
        )

        reserva = Reserva(
            cliente,
            datos[2],
            datos[3]
        )

    except ClienteError as e:

        print("ERROR CLIENTE:", e)

        registrar_log(f"CLIENTE ERROR: {e}")

    except ReservaError as e:

        print("ERROR RESERVA:", e)

        registrar_log(f"RESERVA ERROR: {e}")

    except ServicioError as e:

        print("ERROR SERVICIO:", e)

        registrar_log(f"SERVICIO ERROR: {e}")

    except Exception as e:

        print("ERROR GENERAL:", e)

        registrar_log(f"ERROR GENERAL: {e}")

    else:

        try:

            reserva.confirmar()

        except Exception as e:

            print("ERROR AL CONFIRMAR:", e)

            registrar_log(f"ERROR CONFIRMAR: {e}")

    finally:

        print("Operación finalizada\n")

print("======================================")
print("SISTEMA FINALIZADO")
print("======================================")