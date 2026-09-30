"""Capa 3 — Rutas del módulo productos."""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from dominio import repositorios
from dominio.servicios import (
    actualizar_producto,
    eliminar_producto,
)
from nucleo.conexion import ConexionDep


templates = Jinja2Templates(
    directory="presentacion/templates"
)

router = APIRouter()


def producto_no_encontrado(
    request: Request,
    producto_id: int,
):
    return templates.TemplateResponse(
        request=request,
        name="componentes/producto_no_encontrado.html",
        context={
            "producto_id": producto_id,
        },
        status_code=404,
    )


@router.get("/productos")
async def mostrar_productos(
    request: Request,
    conn: ConexionDep,
):
    productos = await repositorios.obtener_productos(conn)

    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context={
            "productos": productos,
        },
    )


@router.get("/productos/{producto_id}/editar")
async def editar_producto(
    request: Request,
    conn: ConexionDep,
    producto_id: int,
):
    producto = await repositorios.obtener_producto(
        conn,
        producto_id,
    )

    if producto is None:
        return producto_no_encontrado(
            request,
            producto_id,
        )

    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_editar.html",
        context={
            "producto": producto,
            "errores": {},
        },
    )


@router.get("/productos/{producto_id}/cancelar")
async def cancelar_edicion(
    request: Request,
    conn: ConexionDep,
    producto_id: int,
):
    producto = await repositorios.obtener_producto(
        conn,
        producto_id,
    )

    if producto is None:
        return producto_no_encontrado(
            request,
            producto_id,
        )

    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_producto.html",
        context={
            "producto": producto,
        },
    )


@router.post("/productos/{producto_id}")
async def actualizar_producto_vista(
    request: Request,
    conn: ConexionDep,
    producto_id: int,
):
    formulario = await request.form()

    nombre = str(
        formulario.get("nombre", "")
    ).strip()

    precio = float(
        formulario.get("precio", 0)
    )

    cantidad = int(
        formulario.get("cantidad", 0)
    )

    descripcion = str(
        formulario.get("descripcion", "")
    ).strip() or None

    producto = await repositorios.obtener_producto(
        conn,
        producto_id,
    )

    if producto is None:
        return producto_no_encontrado(
            request,
            producto_id,
        )

    try:
        actualizado = await actualizar_producto(
            conn,
            producto_id,
            nombre,
            precio,
            cantidad,
            descripcion,
        )

    except Exception as error:
        return templates.TemplateResponse(
            request=request,
            name="componentes/fila_editar.html",
            context={
                "producto": producto,
                "errores": {
                    "general": str(error),
                },
            },
            status_code=422,
        )

    if not actualizado:
        return producto_no_encontrado(
            request,
            producto_id,
        )

    producto = await repositorios.obtener_producto(
        conn,
        producto_id,
    )

    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_actualizada.html",
        context={
            "producto": producto,
        },
    )


@router.delete("/productos/{producto_id}")
async def eliminar_producto_vista(
    request: Request,
    conn: ConexionDep,
    producto_id: int,
):
    eliminado = await eliminar_producto(
        conn,
        producto_id,
    )

    if not eliminado:
        return producto_no_encontrado(
            request,
            producto_id,
        )

    return templates.TemplateResponse(
        request=request,
        name="componentes/fila_eliminada.html",
        context={
            "producto_id": producto_id,
        },
    )
