# Simulacro de Examen Final - Python

**Empresa ficticia:** AquaFlow Servicios (gestión inteligente de agua potable)
**Puntaje total:** 100 puntos

> Si la consigna no indica una tecnología específica, podés resolverlo como prefieras.
> Si la nombra (como `unittest` o Django), su uso es **obligatorio**.

---

## EJERCICIO 1: Sanitización y Análisis de Lecturas de Medidores (20 Puntos)

Los medidores inteligentes de AquaFlow envían lecturas de caudal con formatos
inconsistentes: identificadores con espacios sobrantes, caudales escritos como texto
con unidades de medida (a veces con coma decimal) y zonas sin informar. Se necesita
un componente que normalice cada lectura y genere un reporte para detectar consumos
excesivos.

* **Punto A: Normalización de lecturas (`limpiar_lectura_medidor`)**
  Diseñá la función `limpiar_lectura_medidor(lectura_raw)`, que recibe un diccionario
  con los datos crudos de un medidor. Por ejemplo:
  `{"medidor_id": "  MED-104 ", "caudal": "12,5 L/min", "zona": None}`.
  La función debe retornar un **nuevo** diccionario estandarizado donde:
  - el identificador quede sin espacios sobrantes;
  - el caudal sea un `float`, sin la unidad y aceptando tanto punto como coma decimal;
  - la zona tenga el valor por defecto `"Zona no asignada"` si falta, es `None` o
    viene vacía.

  Si el caudal no contiene ningún valor numérico, la función debe elevar `ValueError`.

* **Punto B: Reporte de caudal (`generar_reporte_caudal`)**
  Desarrollá la función `generar_reporte_caudal(lista_lecturas_limpias, caudal_maximo)`,
  que recibe lecturas ya normalizadas con la función del Punto A y un caudal límite.
  Debe retornar una tupla `(ids_con_exceso, caudal_promedio)`, con los IDs de los
  medidores que **superan** el límite y el caudal promedio de todas las lecturas.
  Si la lista está vacía, debe retornar `([], 0.0)`.
  Incluí un bloque de ejecución que limpie una lista de lecturas crudas (descartando
  las inválidas sin que el programa se detenga) y que imprima un reporte formateado.

---

## EJERCICIO 2: Modelo de Equipos, Excepciones y Persistencia (40 Puntos)

La división de equipamiento de AquaFlow necesita un módulo que gestione el catálogo de
equipos hidráulicos, que impida precios inconsistentes mediante reglas de negocio y que
guarde el catálogo en disco.

* **Punto A: Dominio del catálogo y reglas de precio**
  Construí la jerarquía orientada a objetos de los equipos. Diseñá una excepción
  personalizada `PrecioInvalidoError` y aplicala en la clase base `EquipoHidraulico`
  (atributos: `codigo`, `nombre`, `precio`) para impedir, mediante encapsulamiento
  explícito, que el precio tome valores negativos, **tanto al crear el objeto como al
  modificarlo después**.
  Desarrollá la clase especializada `TanqueAgua`, que incorpora por herencia sus
  atributos propios (`capacidad_litros` y `material`) y aplica polimorfismo para
  personalizar el método `ficha_tecnica()`.

* **Punto B: Persistencia del catálogo**
  Implementá la clase `GestorEquipos` con el método
  `guardar_equipos_json(lista_equipos, ruta_archivo)`, capaz de serializar los objetos
  del Punto A y guardarlos en `equipos_aquaflow.json`. El JSON debe indicar el tipo de
  cada equipo e incluir los atributos propios de `TanqueAgua`.
  Incluí un bloque de prueba que:
  1. capture `PrecioInvalidoError` al intentar **crear** un equipo con precio negativo;
  2. capture `PrecioInvalidoError` al intentar **modificar** el precio de un equipo
     existente, y muestre que el precio original no cambió;
  3. muestre la ficha técnica de cada equipo válido;
  4. exporte los equipos válidos (al menos un `EquipoHidraulico` y un `TanqueAgua`)
     al archivo JSON.

---

## EJERCICIO 3: Tests Unitarios e Integración Web con Django (40 Puntos)

Antes de lanzar el nuevo sistema de facturación, AquaFlow debe certificar el algoritmo
que calcula el costo del agua. Una vez auditado con pruebas automatizadas, ese
algoritmo debe alimentar el panel web administrativo, desarrollado en **Django**.

* **Punto A: Auditoría del algoritmo de costo (`unittest`)**
  Implementá la función `calcular_costo_agua(consumo_m3, tarifa_m3=850.0)`, que
  retorna `consumo_m3 * tarifa_m3` y eleva `ValueError` si el consumo es negativo.
  Luego implementá la clase `TestCalculoCosto(unittest.TestCase)` con los casos de
  prueba necesarios para validar:
  - la exactitud numérica con la tarifa por defecto y con una tarifa personalizada;
  - el caso límite de consumo cero;
  - un consumo con decimales;
  - la elevación de `ValueError` ante un consumo negativo.

* **Punto B: Resumen de facturación y panel web**
  Desarrollá la función `obtener_resumen_facturacion(registros)`, que reciba un
  historial de consumos con el formato `{"barrio": str, "consumo_m3": float}`.
  **Un mismo barrio puede aparecer varias veces en el historial.** Usando
  `calcular_costo_agua`, la función debe retornar un diccionario con:
  - el total facturado;
  - el consumo acumulado por barrio;
  - el barrio de mayor consumo **acumulado**.

  Por último, dentro de una app de un proyecto Django, diseñá la vista
  `vista_panel_facturacion(request)`, que invoque ese procesamiento y renderice la
  plantilla `facturacion/panel.html` con el diccionario de contexto. La plantilla debe
  mostrar el total facturado, el barrio de mayor consumo y una tabla con el consumo de
  cada barrio. El proyecto debe poder ejecutarse con `python manage.py runserver`.
