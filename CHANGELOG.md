# Changelog - SysStatCLI v2.40.20250513d

## ✨ New Features
Several options have been added to hide progress bars and output either text-only (old-school style) or a specific progress bar from the five available:

Options: Available arguments to omit sections:
-bar, -b → Omit all bars
-barc, -bc → Omit the CPU bar
-barr", -br → Omit the RAM bar
-bard", -bd → Omit the Disk bar
-barw", -bw → Omit the WIFI bar
-bara", -bt → Omit the Battery bar

# Changelog - SysStatCLI v2.40.20250513d

## ✨ Nuevas funciones
Se agregaron varias opción para ocultar las barras de progreso y que la salida sea solo texto (estilo old school) o alguna barra de progreso en particular de las cinco disponibles:

Opciones: Argumentos disponibles para omitir secciones:
-bar, -b → Omite todas las barras
-barc, -bc → Omite la barra de CPU
-barr", -br → Omite la barra de RAM
-bard", -bd → Omite la barra de Disk
-barw", -bw → Omite la barra de WIFI
-bara", -bt → Omite la barra de Battery

# Changelog - SysStatCLI v2.40.20250509c

## ✨ New Features
- Support for single execution or loop execution with interval (`[time]`).
- Added `-help`, `--help`, `-h` arguments to display detailed help.
- Inclusion of short aliases for each section (`-s`, `-c`, `-r`, etc.).
- Automatic validation of invalid arguments with clear messages.
- Link to the repository and author in the help message.
- New, more readable and professional help section.

## 🐞 Fixes
- Correct handling of numeric arguments and non-hyphenated text (`Y`, `Hello`, etc.).
- Improved `sys.argv` logic to avoid errors when passing parameters.

## 🧹 Cleanup and Minor Improvements
- Reordered code for clarity.
- More helpful and consistent error messages.
- Bold invalid arguments for better visibility.

---

# Changelog - SysStatCLI v2.40.20250509c

## ✨ Nuevas funciones
- Soporte para ejecución única o en bucle con intervalo (`[tiempo]`).
- Se agregó argumento `-help`, `--help`, `-h` para mostrar ayuda detallada.
- Inclusión de alias cortos para cada sección (`-s`, `-c`, `-r`, etc.).
- Validación automática de argumentos inválidos con mensajes claros.
- Enlace al repositorio y autor en el mensaje de ayuda.
- Nueva sección de ayuda más legible y profesional.

## 🐞 Correcciones
- Manejo correcto de argumentos numéricos y texto sin guion (`Y`, `Hola`, etc.).
- Mejora en la lógica de `sys.argv` para evitar errores al pasar parámetros.

## 🧹 Limpieza y mejoras menores
- Código reordenado para claridad.
- Mensajes de error más útiles y consistentes.
- Negrita en argumentos inválidos para mayor visibilidad.

---

Autor: Axel O'BRIEN (LiGNUxMan)  
Repositorio: https://github.com/LiGNUxMan/SysStatCLI

