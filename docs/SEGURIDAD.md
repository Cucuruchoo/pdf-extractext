# Seguridad del proyecto

El proyecto incorpora medidas básicas de seguridad adecuadas para una API académica.

## Validación de archivos

La API valida:

- Extensión `.pdf`.
- Firma interna `%PDF`.
- Tamaño máximo configurable mediante `MAX_PDF_SIZE_MB`.

Esto evita procesar archivos que no correspondan al formato esperado.

## Procesamiento en memoria

El PDF se procesa en memoria, sin guardarlo temporalmente en disco.

Esto reduce exposición de archivos sensibles y cumple con el requisito de no persistir temporalmente el archivo mientras se procesa.

## Detección de duplicados

Se calcula un checksum SHA-256 del archivo.

Si ya existe un documento con el mismo checksum, la API rechaza la carga duplicada.

## Headers de seguridad HTTP

Se agregan headers de seguridad básicos:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `Permissions-Policy`

## Variables de entorno

La configuración sensible se maneja mediante variables de entorno.

No deben subirse claves privadas ni API keys al repositorio.

## Alcance

El proyecto no implementa autenticación de usuarios porque el alcance de la etapa es una API académica para carga, extracción y administración de documentos PDF.

Para un entorno productivo se recomienda agregar autenticación, autorización, rate limiting y auditoría avanzada.
