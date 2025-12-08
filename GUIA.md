# 📖 Guía de Uso - Sabios Awards

Bienvenido a **Sabios Awards**, la plataforma oficial para las votaciones mensuales del MVP (Most Valuable Player). Esta aplicación permite a los usuarios participar en elecciones democráticas para reconocer a los miembros más destacados de nuestra comunidad cada mes.

---

## 🔐 Acceso y Autenticación

Para utilizar la aplicación, es necesario tener una cuenta de usuario registrada por un administrador.

*   **Iniciar Sesión**: Accede con tus credenciales (usuario y contraseña) a través de la página de Login.
*   **Registro**: Actualmente, el registro de nuevos usuarios está restringido a administradores para garantizar la integridad de las votaciones. Si necesitas acceso, contacta con un administrador.
*   **Cerrar Sesión**: Puedes salir de tu cuenta en cualquier momento desde el menú de navegación.

---

## 🗳️ Zona de Votación

Esta es la funcionalidad principal de la aplicación.

### ¿Cómo votar?
1.  Navega a la sección de **Votar** (`/vote/cast/`).
2.  Verás la votación **Abierta** correspondiente al mes actual.
3.  Se mostrarán los candidatos nominados con sus respectivas fotos y motivos de nominación.
4.  Selecciona a tu candidato favorito y confirma tu voto.

**Importante**:
*   Solo puedes emitir **un voto por periodo** (mes).
*   Una vez emitido, el voto **no se puede cambiar**.
*   Si la votación está cerrada, no podrás votar.

---

## 📊 Resultados y Hall of Fame

### Resultados en Tiempo Real
*   En la sección de **Resultados** (`/vote/results/`), puedes ver cómo va la votación actual.
*   Si la votación sigue abierta, verás los porcentajes y barras de progreso.
*   También puedes consultar los resultados de meses anteriores seleccionando el periodo deseado.

### Hall of Fame (Salón de la Fama)
*   Visita el **Hall of Fame** (`/vote/hall-of-fame/`) para ver a los ganadores históricos.
*   Aquí se muestran las fotos de los ganadores de todos los periodos pasados que ya han sido revelados.

---

## 🛠️ Panel de Administración

*(Esta sección es visible solo para usuarios con permisos de administrador)*

El panel de administración personalizado permite gestionar todo el ciclo de vida de los premios.

### 1. Gestión de Votaciones (Periodos)
*   **Crear Periodo**: Define un nuevo mes y año para votación.
*   **Estados**:
    *   **Abierta**: Los usuarios pueden votar.
    *   **Cerrada**: Ya no se admiten votos, pero los resultados finales aún no son públicos en el Hall of Fame.
    *   **Resultados Públicos**: Se muestra el ganador en el Hall of Fame.
*   **Ganador Manual**: Permite forzar un ganador si es necesario, o subir una foto específica del ganador.

### 2. Gestión de Candidatos
*   Añade candidatos a un periodo de votación específico.
*   Sube la **Foto de Perfil** del candidato.
*   Opcionalmente, puedes subir una **Foto de Ganador** especial que se mostrará si ese candidato gana.
*   Define el **Motivo de Nominación** que verán los votantes.

### 3. Gestión de Usuarios
*   **Crear Usuarios**: Da de alta a nuevos votantes manualmente.
*   **Activar/Desactivar**: Puedes inhabilitar un usuario temporalmente sin borrarlo (útil para suspender permisos de voto).
*   **Eliminar**: Borra usuarios permanentemente.

### 4. Estadísticas
*   Consulta métricas globales sobre la participación y distribución de votos.

---

## 🚀 Soporte

Si encuentras algún error o tienes dudas sobre el funcionamiento, por favor contacta con el equipo de soporte o desarrollo.
