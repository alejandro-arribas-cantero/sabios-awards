# Sabios Awards (MVP Vote)

Aplicación web profesional para votaciones mensuales de MVP, construida con Django 5.

## 🚀 Características

*   **Usuarios**: Registro, Login, Historial de votos.
*   **Votación**: Un voto por mes, validación de fechas.
*   **Resultados**: Barras de progreso, revelación automática de ganadores.
*   **Admin Panel**: Gestión completa de votaciones, candidatos y estadísticas.
*   **Automatización**: Cron jobs para apertura/cierre de votaciones.

## 🛠 Requisitos

*   Python 3.10+
*   Pip

## 📦 Instalación

1.  **Clonar el repositorio** (o descargar):
    ```bash
    cd mvp_vote
    ```

2.  **Crear entorno virtual**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar entorno**:
    Copiar `.env.example` a `.env` (opcional en dev, necesario en prod).

5.  **Migraciones y Seed**:
    ```bash
    python manage.py migrate
    python manage.py seed_data
    ```
    *Esto creará un admin (`admin`/`admin`) y un usuario (`usuario`/`usuario`), además de datos de prueba.*

6.  **Ejecutar servidor**:
    ```bash
    python manage.py runserver
    ```

## ⚙️ Automatización (Cron)

Para Windows, se recomienda usar el Programador de Tareas llamando a los comandos de gestión personalizados (si se implementan como comandos) o usar los scripts de cron definidos en `apps/voting/cron.py` mediante `django-crontab` (requiere entorno Unix/WSL).

Para ejecutar manualmente las tareas de cron:
```python
python manage.py crontab add
python manage.py crontab show
```

## 🧪 Tests

Ejecutar tests unitarios:
```bash
python manage.py test apps.voting apps.users
```

## 📂 Estructura

*   `apps/`: Aplicaciones Django (users, voting, dashboard).
*   `mvp_vote/settings/`: Configuraciones separadas (base, dev, prod).
*   `templates/`: Plantillas HTML con Bootstrap 5.

## 🔮 Mejoras Futuras

*   Implementar Celery para tareas asíncronas robustas.
*   Añadir notificaciones por email.
*   Mejorar el diseño con animaciones CSS más complejas.
*   API REST con Django Rest Framework.
