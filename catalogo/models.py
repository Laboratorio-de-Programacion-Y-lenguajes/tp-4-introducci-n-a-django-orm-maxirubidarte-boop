from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    """
    Representa a un autor/a.
    Requerido: nombre, email único, biografía opcional.
    """
    #definimos nombre,biografia y email (unico)
    nombre = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.nombre



class Categoria(models.Model):
    """
    Categoría temática de libros.
    Ejemplos: 'fantasía', 'ciencia ficción', 'historia'.
    """
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre
    

class Libro(models.Model):
    """
    Libro del catálogo de la biblioteca.
    Tiene relación N:1 con Autor y N:M con Categoria.
    """

    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    fecha_publicacion = models.DateField()
    cantidad_total = models.PositiveIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)

    
    # Preguntas guía:

    # ¿Qué pasa si eliminás un autor que tiene libros? (PROTECT vs CASCADE)
    # PROTECT evita que se elimine un autor si tiene libros asociados, mientras que CASCADE eliminaría todos los libros relacionados automáticamente.
    #  En este caso, PROTECT es más adecuado para preservar la integridad de los datos y evitar la pérdida accidental de información sobre los libros.

    # ¿Por qué isbn debe ser único?
    # El ISBN es un identificador único para cada libro, lo que permite distinguir entre diferentes ediciones y versiones. Si no fuera único,
    # podría haber confusión al identificar y catalogar los libros en la biblioteca.

    

    def prestamos_activos(self) -> int:
        """
        Retorna la cantidad de préstamos activos (fecha_devolucion IS NULL).

        Un préstamo es "activo" cuando no se ha registrado devolución.
        """
        # TODO: implementar con ORM usando filter sobre los préstamos relacionados
        # Pista: self.prestamo_set.filter(fecha_devolucion__isnull=True).count()
        #        (o el related_name que hayas definido en Prestamo.libro)
        raise NotImplementedError

    def disponibles(self) -> int:
        """
        Retorna cuántas copias están disponibles:
        cantidad_total - prestamos_activos()
        """
        # TODO: implementar
        raise NotImplementedError

    def tiene_disponibles(self) -> bool:
        """Retorna True si hay al menos una copia disponible."""
        # TODO: implementar
        raise NotImplementedError


class Prestamo(models.Model):
    """
    Registro de un préstamo de libro a un usuario.
    Si fecha_devolucion es NULL → el préstamo está activo.
    """

    # TODO: implementar los campos:
    # libro              → ForeignKey(Libro, on_delete=models.CASCADE)
    # nombre_prestatario → CharField
    # fecha_prestamo     → DateField
    # fecha_devolucion   → DateField (null=True, blank=True)
    #
    # Preguntas guía:
    # ¿Por qué usamos CASCADE aquí y PROTECT en Libro→Autor?
    # ¿Qué valor por defecto tendría sentido para fecha_prestamo?
    # Tip: podés usar default=timezone.now si querés fecha automática,
    #      o dejarlo sin default para que el test lo defina explícitamente.

    pass
