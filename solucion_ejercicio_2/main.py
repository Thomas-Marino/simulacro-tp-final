import json, os
from pathlib import Path

class PrecioInvalidoError(Exception):
    """
    Excepción personalizada pensada para lanzarse al momento de intentar asignar
    un precio menor a 0 o no numérico.
    """

class EquipoHidraulico:
    codigo: str
    nombre: str 
    __precio: float

    def __init__(self, codigo: str, nombre: str, precio: float):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    @property
    def precio(self): return self.__precio

    @precio.setter
    def precio(self, valor):
        try:
            self.__precio = float(valor)
            if self.__precio < 0: 
                raise PrecioInvalidoError("El valor a asignar en precio debe ser mayor o igual a 0")
        except ValueError:
            raise PrecioInvalidoError("El tipo de dato a asignar en precio debe ser numérico")
        except TypeError:
            raise PrecioInvalidoError("El valor a asignar en precio no puede ser nulo")

    def ficha_tecnica(self, imprimir: bool = False)-> str:
        ficha = f"codigo: {self.codigo} | nombre: {self.nombre} | precio: {self.precio}"
        
        if imprimir: print(ficha)
        return ficha

    def to_dict(self)-> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio
        }

class TanqueAgua(EquipoHidraulico):
    capacidad_litros: float
    material: str

    def __init__(self, codigo: str, nombre: str, precio: float, capacidad_litros: float, material: str):
        super().__init__(codigo, nombre, precio)
        self.capacidad_litros = capacidad_litros
        self.material = material

    def ficha_tecnica(self, imprimir = False):
        ficha = super().ficha_tecnica()
        ficha += f" | capacidad litros: {self.capacidad_litros} | material: {self.material}"

        if imprimir: print(ficha)
        return ficha

    def to_dict(self):
        dict = super().to_dict()
        dict["capacidad_litros"] = self.capacidad_litros
        dict["material"] = self.material

        return dict

class GestorEquipos:
    @staticmethod
    def guardar_equipos(lista_equipos: list[EquipoHidraulico | TanqueAgua], ruta_directorio_archivo: str = "data")-> bool:
        """
        lista_equipos: Se solicita que el valor de este parametro sea una lista que contenga solamente instancias de EquipoHidraulico ó TanqueAgua
        ruta_directorio_archivo: Se solicita que el valor de este parametro sea una ruta a un directorio para posteriormente 
        concatenarle /equipos_aquaflow.json. Por lo tanto la ruta no debería terminar en / o espacio.
        """
        Path(ruta_directorio_archivo).mkdir(exist_ok=True)

        with open(ruta_directorio_archivo + "/equipos_aquaflow.json", "w") as archivo:
            lista_equipos_serializados = []
            for elemento in lista_equipos:
                lista_equipos_serializados.append(elemento.to_dict())
            json.dump(lista_equipos_serializados, archivo, indent=4)

equipo_1 = EquipoHidraulico("Test-1", "Test-1", 9999)
equipo_2 = EquipoHidraulico("Test-2", "Test-2", 200000)

tanque_1 = TanqueAgua("Test-tanque-1", "Test-tanque-1", 8888888, 5, "Metal")
tanque_2 = TanqueAgua("Test-tanque-2", "Test-tanque-2", 933333, 5, "Plastico")
tanque_3 = TanqueAgua("Test-tanque-3", "Test-tanque-3", 20000000, 5, "Acero")

try:
    equipo_erroneo_1 = EquipoHidraulico("Test-error-1", "Test-error-1", -20000)
except PrecioInvalidoError as e:
    print(f"Excepción capturada al instanciar un equipo hidraulico con precio negativo: {e}")

try:
    tanque_1.precio = None
except PrecioInvalidoError as e: 
    print(f"Excepción capturada al modificar un equipo hidraulico con precio negativo: {e}")

lista_equipos: list[EquipoHidraulico | TanqueAgua] = [
    equipo_1,
    equipo_2,
    tanque_1,
    tanque_2,
    tanque_3
]

for equipo in lista_equipos:
    equipo.ficha_tecnica(True)

GestorEquipos.guardar_equipos(lista_equipos)