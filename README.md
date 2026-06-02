# PDF Documents API

Aplicación web/API desarrollada con Python, FastAPI, uv, MongoDB y Docker para gestionar documentos PDF.

El sistema permite subir archivos PDF, validar su formato y tamaño, extraer el texto, calcular un checksum SHA-256, persistir la información en una base de datos NoSQL y realizar operaciones CRUD sobre los documentos almacenados.

## Integrantes

- Santiago Viñolo
- Renata Michaux
- Gaston Fernandez

## Tecnologías utilizadas

- Python 3.12
- FastAPI
- uv
- MongoDB
- Docker
- Motor / PyMongo
- pypdf
- pytest
- Ruff

## Funcionalidades

- Subida de archivos PDF.
- Validación de extensión `.pdf`.
- Validación de firma PDF.
- Validación de tamaño máximo.
- Extracción de texto desde memoria, sin guardar temporalmente el archivo.
- Cálculo de checksum SHA-256.
- Persistencia en MongoDB.
- Prevención de documentos duplicados por checksum.
- CRUD de documentos:
  - Crear documento.
  - Listar documentos.
  - Buscar documento por ID.
  - Actualizar documento.
  - Eliminar documento.

## Requisitos previos

Tener instalado:

- Python 3.12
- uv
- Git
- Docker Desktop

Verificar instalación:

```powershell
python --version
uv --version
git --version
docker --version```
## Instalación

Clonar el repositorio:

```powershell
git clone https://github.com/Cucuruchoo/pdf-extractext.git
cd pdf-extractext
```

Instalar dependencias:

```powershell
uv sync
```

## Variables de entorno

Si se ejecuta el proyecto localmente con `uv`, crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=pdf_documents
MAX_PDF_SIZE_MB=10
```

El archivo `.env` no debe subirse al repositorio.

## Ejecutar el proyecto con Docker

El proyecto incluye un `docker-compose.yml` que levanta dos servicios:

- `app`: aplicación FastAPI.
- `mongo`: base de datos MongoDB.

Para construir y ejecutar la aplicación completa:

```powershell
docker compose up --build -d
```

Este comando construye la imagen de la API, levanta el contenedor de FastAPI y levanta MongoDB.

Verificar que los contenedores estén corriendo:

```powershell
docker ps
```

Deben aparecer contenedores similares a:

```text
pdf-documents-api
mongo-pdf-api
```

La documentación automática de FastAPI queda disponible en:

```text
http://127.0.0.1:8000/docs
```

Para verificar la conexión con MongoDB:

```text
http://127.0.0.1:8000/health/db
```

Respuesta esperada:

```json
{
  "database": "ok"
}
```

## Logs con Docker

La aplicación registra logs por consola para que puedan verse desde Docker.

Para ver los logs de la API:

```powershell
docker compose logs -f app
```

Para ver los logs de MongoDB:

```powershell
docker compose logs -f mongo
```

Para salir de los logs:

```text
Ctrl + C
```

## Detener los contenedores

Para detener la aplicación y MongoDB:

```powershell
docker compose down
```

Para detener los contenedores y eliminar también el volumen de MongoDB:

```powershell
docker compose down -v
```

## Versión de MongoDB en Docker

El proyecto usa la imagen:

```yaml
mongo:4.4
```

Se utiliza esta versión porque algunas computadoras antiguas no soportan AVX, y MongoDB 5.0 o superior puede fallar en esos equipos.

## Ejecutar tests

Con MongoDB corriendo en Docker, ejecutar:

```powershell
uv run pytest
```

Resultado esperado:

```text
28 passed
```

Para revisar calidad de código:

```powershell
uv run ruff check .
```

## Endpoints principales

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Verifica que la API esté activa |
| GET | `/health/db` | Verifica conexión con MongoDB |
| POST | `/documents` | Sube y guarda un PDF |
| GET | `/documents` | Lista documentos |
| GET | `/documents/{document_id}` | Obtiene un documento por ID |
| PUT | `/documents/{document_id}` | Actualiza datos del documento |
| DELETE | `/documents/{document_id}` | Elimina un documento |

## Estructura del proyecto

```text
pdf-extractext/
├── app/
│   ├── api/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── schemas/
│   └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

## Arquitectura utilizada

El proyecto no utiliza MVC clásico porque no posee vistas HTML ni una interfaz gráfica propia.

Al tratarse de una API REST con FastAPI, se utiliza una arquitectura por capas:

- `api`: capa HTTP de FastAPI, equivalente a controllers.
- `application`: casos de uso y lógica de aplicación.
- `domain`: entidades, reglas de negocio y validaciones.
- `infrastructure`: conexión con MongoDB, logs y extracción de texto desde PDF.
- `schemas`: modelos de entrada y salida de la API.

Esta separación permite reducir acoplamiento, mejorar la mantenibilidad y facilitar las pruebas automáticas.

## Estado del proyecto

- API funcionando.
- MongoDB funcionando con Docker.
- Aplicación FastAPI funcionando con Docker.
- CRUD de documentos implementado.
- Validación de PDFs implementada.
- Extracción de texto implementada.
- Checksum SHA-256 implementado.
- Logs visibles desde Docker.
- Tests automáticos implementados.