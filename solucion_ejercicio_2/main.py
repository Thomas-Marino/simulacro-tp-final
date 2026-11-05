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
        self.precio = precio # ESTA MAL

    @property
    def precio(self): return self.__precio

    @precio.setter
    def precio(self, valor):
        try:
            self.__precio = float(valor)
            if float(valor) < 0: 
                raise PrecioInvalidoError("El valor a asignar en precio debe ser mayor o igual a 0")
        except ValueError:
            raise PrecioInvalidoError("El tipo de dato a asignar en precio debe ser numérico")
        except TypeError:
            raise PrecioInvalidoError("El valor a asignar en precio no puede ser nulo")

EquipoHidraulico("probando", "probando", 0)