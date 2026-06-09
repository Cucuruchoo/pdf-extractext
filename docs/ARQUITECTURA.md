# Arquitectura del proyecto

El proyecto utiliza una arquitectura por capas para separar responsabilidades y facilitar mantenimiento, pruebas y evolución.

## 1. Capa de presentación

Carpetas:

- `app/api`
- `app/schemas`

Responsabilidades:

- Exponer endpoints HTTP con FastAPI.
- Recibir solicitudes del cliente.
- Validar datos de entrada y salida.
- Transformar entidades del dominio en respuestas HTTP.

Ejemplos:

- `POST /documents`
- `GET /documents`
- `GET /documents/{document_id}`
- `PUT /documents/{document_id}`
- `DELETE /documents/{document_id}`

## 2. Capa de aplicación y dominio

Carpetas:

- `app/application`
- `app/domain`

Responsabilidades:

- Implementar los casos de uso del sistema.
- Aplicar reglas de negocio.
- Validar archivos PDF.
- Calcular checksum.
- Extraer texto.
- Coordinar la persistencia de documentos.

## 3. Capa de infraestructura y datos

Carpetas:

- `app/infrastructure`

Responsabilidades:

- Conexión con MongoDB.
- Implementación del repositorio.
- Configuración de logs.
- Extracción técnica de texto desde PDF.
- Seguridad básica mediante headers HTTP.

## Justificación

No se utiliza MVC clásico porque el sistema es una API REST y no tiene vistas HTML propias.

La separación por capas permite cumplir principios como bajo acoplamiento, alta cohesión, mantenibilidad, testeabilidad y separación de responsabilidades.
