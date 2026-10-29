from abc import ABC, abstractmethod
from dataclasses import dataclass

# Datos de usuario
@dataclass
class Usuario:
    nombre: str
    correo: str
    telefono: str

# Guardar usuarios
class Repositorio(ABC):
    @abstractmethod
    def guardar(self, usuario): ...

class RepositorioUsuario(Repositorio):
    def __init__(self):
        self.usuarios = []
    def guardar(self, usuario):
        self.usuarios.append(usuario)

# Notificadores (en el Observer, cada Notificador es un oyente)
class Notificador(ABC):
    @abstractmethod
    def enviar(self, usuario, mensaje): ...

class NotificadorCorreo(Notificador):
    def enviar(self, usuario, mensaje):
        print(f"Hola {usuario.nombre}, te escribimos a {usuario.correo}: {mensaje}")

class NotificadorSMS(Notificador):
    def enviar(self, usuario, mensaje):
        print(f"SMS a {usuario.telefono}: {mensaje}")

class NotificadorAdmin(Notificador):
    def enviar(self, usuario, mensaje):
        print(f"[ADMIN] Nuevo usuario registrado: {usuario.nombre}")

# CREACIONAL: Factory Method
# Cada fabrica decide que Notificador crear y el main no usa clases concretas.
class FabricaNotificador(ABC):
    @abstractmethod
    def crear(self): ...

class FabricaCorreo(FabricaNotificador):
    def crear(self): return NotificadorCorreo()

class FabricaSMS(FabricaNotificador):
    def crear(self): return NotificadorSMS()

# ESTRUCTURAL: Decorator
# Envuelve cualquier Notificador y le suma auditoria sin modificarlo.
class NotificadorAuditado(Notificador):
    def __init__(self, base):
        self.base = base
    def enviar(self, usuario, mensaje):
        print(f"[AUDITORIA] notificando a {usuario.nombre}")
        self.base.enviar(usuario, mensaje)

# COMPORTAMIENTO: Observer
# ServicioRegistro (sujeto) avisa a todos los oyentes suscritos al registrar un usuario y
# sin conocer que hace cada uno.
class ServicioRegistro:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.oyentes = []
    def suscribir(self, oyente):
        self.oyentes.append(oyente)
    def registrar(self, usuario):
        self.repositorio.guardar(usuario)
        for oyente in self.oyentes:
            oyente.enviar(usuario, "Bienvenido")

# Principal
if __name__ == "__main__":
    usuario = Usuario(input("Nombre: "), input("Correo: "), input("Telf: "))
    canal = input("Notificar: 1 Correo o 2 SMS: ")

    fabrica = FabricaSMS() if canal == "2" else FabricaCorreo()

    servicio = ServicioRegistro(RepositorioUsuario())
    servicio.suscribir(NotificadorAuditado(fabrica.crear()))      
    servicio.suscribir(NotificadorAdmin())                        
    servicio.registrar(usuario)