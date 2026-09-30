"""Capa 1 — Configuración de la aplicación."""

import os

from dotenv import load_dotenv

load_dotenv()


class Configuracion:
    """Configuración que llega desde las variables de entorno."""

    base_datos: str = os.environ["DATABASE_URL"]
    nombre_app: str = "TechStore"


CONFIGURACION = Configuracion()