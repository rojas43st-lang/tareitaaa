# Ejercicio: edición y borrado de productos

Proyecto educativo con **FastAPI + Jinja2 + HTMX + PostgreSQL (asyncpg)** que
permite consultar, editar y **eliminar** productos de la tabla `productos`.

El enunciado del nuevo ejercicio está en
[`Docs/ejercicio_borrado_productos.md`](Docs/ejercicio_borrado_productos.md).
(El ejercicio anterior, sobre la edición, está en
[`Docs/ejercicio_edicion_productos.md`](Docs/ejercicio_edicion_productos.md); su
implementación ya está incluida en este proyecto y sirve de base.)

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

```bash
cp .env.example .env
```

Edita `.env` y define la cadena de conexión a tu base de datos PostgreSQL.
La variable debe llamarse `DATABASE_URL` y estar exportada antes de arrancar
el servidor:

```bash
export DATABASE_URL="postgresql://usuario:contrasena@host:puerto/basedatos"
```

## Ejecución

```bash
uvicorn main:app --reload
```

Abre el navegador en <http://127.0.0.1:8000/productos>.

## Rutas

| Método y ruta                     | Para qué sirve                                        |
| --------------------------------- | ----------------------------------------------------- |
| `GET /productos`                  | Lista de productos                                     |
| `GET /productos/{id}/editar`      | Formulario de edición con los valores actuales         |
| `POST /productos/{id}`            | Valida y guarda los cambios (`UPDATE`)                 |
| `GET /productos/{id}/cancelar`    | Vuelve a la fila normal sin guardar nada               |
| `DELETE /productos/{id}`          | Elimina el producto indicado (`DELETE`), previa confirmación |

## Estado del proyecto

- `GET /productos` muestra la lista de productos.
- La edición (formulario precargado, validación, `UPDATE` y aviso de éxito)
  está implementada y funcionando.
- El borrado está implementado con `hx-delete` + `hx-confirm` y `DELETE`
  parametrizado. La carpeta `solucion/` (material del docente) contiene la
  misma implementación comentada paso a paso.

## Archivos principales

- `main.py`: crea la aplicación y el pool de conexiones.
- `vistas.py`: rutas de FastAPI y fragmentos HTML que devuelve cada una.
- `repositorio.py`: todas las consultas SQL, siempre parametrizadas.
- `esquemas.py`: reglas de validación de los datos del formulario.
- `templates/`: página completa y fragmentos que HTMX inserta en la tabla.
