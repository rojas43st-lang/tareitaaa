"""Capa 2 — Reglas de negocio de los productos."""

from dominio import repositorios


class ProductoInvalido(Exception):
    """El producto incumple una regla de negocio."""


async def actualizar_producto(
    conn,
    producto_id: int,
    nombre: str,
    precio: float,
    cantidad: int,
    descripcion: str | None,
) -> bool:

    if precio < 0:
        raise ProductoInvalido("El precio no puede ser negativo.")

    if cantidad < 0:
        raise ProductoInvalido("La cantidad no puede ser negativa.")

    return await repositorios.actualizar_producto(
        conn,
        producto_id,
        nombre,
        precio,
        cantidad,
        descripcion,
    )


async def eliminar_producto(conn, producto_id: int) -> bool:
    """Elimina un producto mediante el repositorio."""

    return await repositorios.eliminar_producto(conn, producto_id)
