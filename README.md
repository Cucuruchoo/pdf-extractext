# PDF Documents API — Implementación original (monolito)

> **Contexto académico:** este repositorio conserva la implementación original del proyecto de Desarrollo de Software 2026. El sistema evolucionó, dentro de la misma etapa académica, hacia una arquitectura de tres microservicios. **Para consultar y ejecutar la implementación final, utilizá los repositorios de microservicios enlazados más abajo.**

## Evolución del proyecto

La primera implementación concentra en una aplicación FastAPI la recepción de archivos PDF, validación, extracción de texto, cálculo de checksum y operaciones con MongoDB. El código está organizado **por capas** (API, aplicación, dominio e infraestructura), pero se despliega como una aplicación monolítica.

La implementación final separa esas responsabilidades en:

- [pdf-request-service](https://github.com/Cucuruchoo/pdf-request-service): API pública, validación y coordinación.
- [pdf-extraction-service](https://github.com/Cucuruchoo/pdf-extraction-service): extracción de texto.
- [pdf-storage-service](https://github.com/Cucuruchoo/pdf-storage-service): persistencia y CRUD sobre MongoDB.

**Tableros de GitHub Projects:**

- [Implementación original](https://github.com/users/Cucuruchoo/projects/2): tareas del monolito.
- [Implementación final](https://github.com/users/Cucuruchoo/projects/1): tareas de los microservicios.

Ambos tableros reflejan la evolución de **una sola etapa académica**, no entregas independientes.

## Integrantes

- Santiago Viñolo
- Renata Michaux

## Tecnologías

Python 3.12, FastAPI, uv, MongoDB, Motor / PyMongo, pypdf, Docker, Docker Compose, pytest y Ruff.

## Funcionalidades de la implementación original

- Recepción de PDF y validaciones de extensión, firma y tamaño.
- Extracción de texto en memoria, sin guardar temporalmente el archivo original.
- Cálculo de checksum SHA-256 y prevención de documentos duplicados.
- Persistencia de texto y metadatos en MongoDB.
- Operaciones CRUD.
- Obtención de un resumen del texto extraído.
- Registro de eventos y encabezados HTTP de seguridad básicos.

## API de esta versión

Esta implementación utiliza rutas distintas de las de los microservicios:

| Método | Ruta | Función |
| --- | --- | --- |
| `POST` | `/documents` | Subir un PDF |
| `GET` | `/documents` | Listar documentos |
| `GET` | `/documents/{document_id}` | Consultar un documento |
| `GET` | `/documents/{document_id}/summary` | Obtener resumen de texto |
| `PUT` | `/documents/{document_id}` | Actualizar un documento |
| `DELETE` | `/documents/{document_id}` | Eliminar un documento |
| `GET` | `/` | Estado de la aplicación |
| `GET` | `/health/db` | Estado de MongoDB |

La documentación interactiva está disponible en `/docs` al ejecutar la aplicación.

## Organización

- `app/api` y `app/schemas`: presentación y contratos HTTP.
- `app/application` y `app/domain`: casos de uso y reglas de negocio.
- `app/infrastructure`: persistencia, extracción técnica y configuración.
- `tests`: pruebas automatizadas.
- `docker`: archivos de Compose y ejemplo de variables de entorno.
- `docs`: documentación técnica.

Consultá [Arquitectura](docs/ARQUITECTURA.md) y [Seguridad](docs/SEGURIDAD.md) para conocer las decisiones de esta implementación.

## Requisitos y pruebas

Para trabajar con esta versión se requiere Python 3.12 y `uv`; para ejecutarla con contenedores, Docker Desktop.

Desde la raíz del repositorio, las pruebas locales se pueden ejecutar con:

```powershell
uv sync --group dev
uv run pytest -q
uv run ruff check .
```

Los archivos de Docker Compose se encuentran en `docker/`. El archivo `docker/.env.example` muestra la configuración esperada; sus rutas, puertos e imágenes deben ajustarse al entorno en el que se ejecute.

## Estado y propósito del repositorio

Se conserva como **registro histórico y evidencia del desarrollo inicial**. El código, las Issues y el historial Git permiten revisar el trabajo realizado antes de separar las responsabilidades en microservicios. No se deben confundir los comandos ni los endpoints de este monolito con los de la implementación final.

**Versión final:** [pdf-request-service](https://github.com/Cucuruchoo/pdf-request-service) · [pdf-extraction-service](https://github.com/Cucuruchoo/pdf-extraction-service) · [pdf-storage-service](https://github.com/Cucuruchoo/pdf-storage-service).
