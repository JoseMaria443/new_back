# API de Comunicados Institucionales

Sistema de gestión de comunicados, tareas y evidencias en un entorno universitario.

## Arquitectura

Este proyecto sigue la arquitectura Hexagonal (Puertos y Adaptadores) con los siguientes bounded contexts:

- **catalogos**: Áreas, cargos, tipos de comunicado, medios de recepción, roles, estados de tarea
- **personal**: Empleados, cargos múltiples, historial de estatus
- **comunicados**: Comunicados, destinatarios, archivos adjuntos
- **tareas**: Tareas derivadas de comunicados, responsables
- **evidencias**: Evidencias de tareas y su vinculación

## Instalación


## Ejecución

```bash
# Desde el directorio src/
uvicorn main:app --reload
```

## Estructura del Proyecto

```
proyecto/
├── src/
│   ├── main.py                    # Punto de entrada
│   ├── config/
│   │   ├── settings.py           # Configuración
│   │   └── container.py          # Inyección de dependencias
│   ├── shared/
│   │   ├── domain/
│   │   │   ├── base_entity.py    # Entidad base
│   │   │   └── exceptions.py     # Excepciones
│   │   └── infrastructure/
│   │       ├── database/
│   │       │   ├── connection.py
│   │       │   └── base_repository.py
│   │       ├── storage/
│   │       │   └── file_storage_adapter.py
│   │       └── file_parsers/
│   │           ├── pdf_parser.py
│   │           ├── image_parser.py
│   │           └── parser_factory.py
│   ├── modules/
│   │   ├── catalogos/
│   │   ├── personal/
│   │   ├── comunicados/
│   │   ├── tareas/
│   │   └── evidencias/
│   └── tests/
└── migrations/
    └── 001_init_schema.sql
```

## API Documentation

Una vez ejecutando, la documentación está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc