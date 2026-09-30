"""Capa 1 — Conexión. Administra el pool de PostgreSQL."""

from typing import Annotated, AsyncGenerator

import asyncpg
from fastapi import Depends


class Conexion:
    """Abre y cierra el pool de conexiones."""

    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    async def conectar(self, url: str) -> None:
        if self.pool is not None:
            return

        self.pool = await asyncpg.create_pool(
            dsn=url,
            min_size=1,
            max_size=10,
        )

    async def cerrar(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None


conexion = Conexion()


async def get_conexion() -> AsyncGenerator[asyncpg.Connection, None]:
    """Entrega una conexión del pool a cada petición."""

    if conexion.pool is None:
        raise RuntimeError("El pool no está abierto.")

    async with conexion.pool.acquire() as conn:
        yield conn


ConexionDep = Annotated[
    asyncpg.Connection,
    Depends(get_conexion),
]
