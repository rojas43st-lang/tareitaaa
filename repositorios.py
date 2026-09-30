"""Capa 2 — Acceso a datos. Único lugar donde existe SQL."""


async def obtener_productos(conn) -> list[dict]:
    filas = await conn.fetch("""
        SELECT id, nombre, precio, cantidad, descripcion
          FROM productos
         ORDER BY nombre
    """)

    return [dict(fila) for fila in filas]


async def obtener_producto(conn, producto_id: int) -> dict | None:
    fila = await conn.fetchrow("""
        SELECT id, nombre, precio, cantidad, descripcion
          FROM productos
         WHERE id = $1
    """, producto_id)

    return dict(fila) if fila is not None else None


async def actualizar_producto(
    conn,
    producto_id: int,
    nombre: str,
    precio: float,
    cantidad: int,
    descripcion: str | None,
) -> bool:
    resultado = await conn.execute("""
        UPDATE productos
           SET nombre = $2,
               precio = $3,
               cantidad = $4,
               descripcion = $5
         WHERE id = $1
    """, producto_id, nombre, precio, cantidad, descripcion)

    return resultado == "UPDATE 1"


async def eliminar_producto(conn, producto_id: int) -> bool:
    resultado = await conn.execute("""
        DELETE FROM productos
         WHERE id = $1
    """, producto_id)

    return resultado == "DELETE 1"