from __future__ import annotations

from django.db.models import Count, Q

from .models import Autor, Libro


def libros_por_categoria(nombre_categoria: str):
    """
    Devuelve un QuerySet de Libros que pertenecen a la categoría indicada.

    Args:
        nombre_categoria: nombre exacto de la categoría (ej: "fantasía")

    Returns:
        QuerySet[Libro]

    Ejemplo de uso:
        libros = libros_por_categoria("fantasía")
        for libro in libros:
            print(libro.titulo)
    """
    # Filtramos los libros buscando en el campo 'nombre' del modelo 'Categoria' relacionado
    return Libro.objects.filter(categorias__nombre=nombre_categoria)
   


def autores_con_mas_de_n_libros(n: int):
    """
    Devuelve un QuerySet de Autores que tienen más de n libros en el catálogo.
    """
    return Autor.objects.annotate(cantidad_libros=Count("libro")).filter(cantidad_libros__gt=n)


def libros_sin_disponibilidad():
    """
    Devuelve un QuerySet de Libros donde no hay copias disponibles.
    (prestamos_activos == cantidad_total)

    Returns:
        QuerySet[Libro]

    Restricción: resolver con ORM, SIN iterar libros en Python
    (no usar disponibles() en un loop).

    Pista: podés contar los préstamos activos por libro con annotate:
        Libro.objects.annotate(
            activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
        ).filter(activos=models.F("cantidad_total"))
    """

    # 1. Contamos los préstamos que no tienen fecha de devolución (están activos).
    # 2. F() para comparar ese conteo contra la columna 'cantidad_total'.
    return Libro.objects.annotate(
        activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
    ).filter(activos=F("cantidad_total"))



def top_n_libros_mas_prestados(n: int):
    """
    Devuelve los N libros con más préstamos (en total, sin importar si están activos).

    Args:
        n: cantidad de libros a retornar

    Returns:
        QuerySet[Libro] con hasta n elementos, ordenados de más a menos prestados.

    Pista:
        Libro.objects.annotate(total_prestamos=Count("prestamo"))
                     .order_by("-total_prestamos")[:n]
    """
    # TODO: implementar con annotate + order_by + slicing
    raise NotImplementedError
