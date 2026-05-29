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
docker --version