# 💰 Dinerless API

Dinerless es una solución de Backend diseñada para la gestión de finanzas personales. El objetivo principal de este proyecto es centralizar el control de ingresos, gastos y planificación presupuestaria a través de una interfaz de programación (API) segura, escalable y fácil de integrar.

## 🎯 Objetivo del Proyecto
El proyecto busca resolver la fragmentación de la información financiera, permitiendo a los usuarios monitorizar su salud económica en tiempo real mediante el seguimiento de presupuestos por categorías y la generación de reportes mensuales automatizados.

## 🛠️ Stack Tecnológico
Para garantizar la eficiencia y seguridad del sistema, se seleccionaron las siguientes herramientas:
* **Lenguaje:** Python 3.x
* **Framework Principal:** Django & Django REST Framework (DRF)
* **Autenticación:** JSON Web Token (JWT) para sesiones seguras y sin estado.
* **Documentación:** OpenAPI 3.0 con Swagger UI a través de `drf-spectacular`.
* **Base de Datos:** PostgreSQL / SQLite.

## 🌟 Buenas Prácticas Aplicadas
En este desarrollo se priorizó la calidad del código y la mantenibilidad siguiendo estándares de la industria:

* **Arquitectura de Software:** Uso de una estructura de carpetas modular y versionada (`API v1`), facilitando el crecimiento del proyecto sin romper compatibilidad.
* **Seguridad y Privacidad:** * Implementación de **Permissions** a nivel de objeto: cada usuario solo puede acceder, editar o eliminar sus propios datos.
    * Manejo de credenciales mediante variables de entorno.
* **Optimización de Consultas:** Uso de filtros eficientes en `get_queryset` para asegurar que el motor de base de datos responda con rapidez.
* **Validación de Datos:** Lógica de negocio robusta integrada en Serializers para garantizar que la información entrante sea íntegra y coherente.
* **Documentación Automatizada:** Configuración de esquemas para que la API sea "autodescriptiva", facilitando la integración con cualquier Frontend (React, Mobile, etc.).
* **Principio DRY (Don't Repeat Yourself):** Reutilización de lógica mediante clases base y mixins de Django.

 portafolio profesional como desarrollador Backend.*
