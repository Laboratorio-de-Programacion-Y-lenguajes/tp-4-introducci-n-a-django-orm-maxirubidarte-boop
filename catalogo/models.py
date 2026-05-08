from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    """
    Representa a un autor/a.
    Requerido: nombre, email único, biografía opcional.
    """
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

    def __str__(self):
        return self.titulo

    # --- MÉTODOS DE LÓGICA DE NEGOCIO ---

    def prestamos_activos(self) -> int:
        """
        Retorna la cantidad de préstamos activos (fecha_devolucion IS NULL).
        """
        return self.prestamo_set.filter(fecha_devolucion__isnull=True).count()

    def disponibles(self) -> int:
        """
        Retorna cuántas copias están disponibles:
        cantidad_total - prestamos_activos()
        """
        return self.cantidad_total - self.prestamos_activos()

    def tiene_disponibles(self) -> bool:
        """Retorna True si hay al menos una copia disponible."""
        return self.disponibles() > 0


class Prestamo(models.Model):
    """
    Registro de un préstamo de libro a un usuario.
    Si fecha_devolucion es NULL → el préstamo está activo.
    """
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_prestatario = models.CharField(max_length=120)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.libro.titulo} prestado a {self.nombre_prestatario}"

    # Preguntas guía respondidas:
    # ¿Por qué usamos CASCADE aquí y PROTECT en Libro→Autor?
    # Usamos CASCADE en Prestamo porque si el libro se elimina, el registro del préstamo pierde su razón de ser. 
    # En cambio, usamos PROTECT en Libro→Autor para no perder los libros si se borra accidentalmente al autor.