# Changelog - SysStatCLI v2.44.20260315c

## 🇺🇸🇬🇧 English

- 🛠️ **Complete Help System Overhaul:** The help interface was rewritten from scratch using `argparse`. It now provides professional, standardized, and automatic documentation via `-h`, `--help`, or `-help`.
- 🚀 **Migration to Argparse:** Manual `sys.argv` logic was removed. The new engine allows for robust input validation, type handling, and the use of direct boolean flags (`args.sys`, `args.cpu`), eliminating the old set-based validation.
- 🏗️ **Modular Architecture & Cleanup:** Total code refactor into specialized functions:
  - `detect_hardware()`: Centralizes interface and sensor detection at startup.
  - `init_metrics()`: Calibrates network and disk counters to prevent erroneous measurements.
  - `print_all_stats()`: Decouples data visualization from the main loop logic.
- 🛡️ **Metric Robustness:** Added `try-except` blocks in hardware data capture to prevent the script from crashing due to permission issues or unavailable sensors.
- ⌨️ **Terminal Control (Raw Mode):** Implemented `termios` and `tty` to capture exit keys (`q`/`x`) silently, with guaranteed terminal restoration via `try...finally` blocks.

---

## 🇪🇸 Español

- 🛠️ **Reescritura Total del Sistema de Ayuda:** Se rediseñó la ayuda desde cero utilizando `argparse`. Ahora genera documentación profesional, estandarizada y automática mediante `-h`, `--help` o `-help`.
- 🚀 **Migración a Argparse:** Se eliminó la lógica manual de `sys.argv`. El nuevo motor permite validación robusta de entradas, manejo de tipos y el uso de flags booleanos directos (`args.sys`, `args.cpu`), eliminando la vieja validación por conjuntos.
- 🏗️ **Arquitectura Modular y Limpieza:** Refactorización total del código en funciones especializadas:
  - `detect_hardware()`: Centraliza la detección de interfaces y sensores al inicio.
  - `init_metrics()`: Calibra contadores de red y disco para evitar mediciones erróneas.
  - `print_all_stats()`: Separa la visualización de los datos de la lógica del bucle principal.
- 🛡️ **Robustez en Métricas:** Se añadieron bloques `try-except` en la captura de datos de hardware para evitar que el script falle ante problemas de permisos o sensores no disponibles.
- ⌨️ **Control de Terminal (Raw Mode):** Implementación de `termios` y `tty` para capturar teclas de salida (`q`/`x`) de forma silenciosa, con restauración garantizada de la terminal mediante `try...finally`.

---

# Changelog - SysStatCLI v2.44.20260310a

## 🇺🇸🇬🇧 English

- ✨ **New Feature:** Added a progress bar for CPU frequency to visually represent processor scaling.
- 🐞 **Fixes:** Initial improvements to documentation and basic help logic.

---

## 🇪🇸 Español

- ✨ **Nueva función:** Se agregó una barra de progreso para la frecuencia del CPU para representar visualmente el escalado del procesador.
- 🐞 **Correcciones:** Mejoras iniciales en la documentación y la lógica básica de ayuda.

---

# Changelog - SysStatCLI v2.41.20250525l

## 🇺🇸🇬🇧 English

- Fixed an issue in get_lan_info (Lan).

Fixed a bug that caused the script to stop when hot-plugging the USB network card.

---

## 🇪🇸 Español

- Se soluciono problema en get_lan_info (Lan).

Se arreglo un error que hacia que el script se detuviera cuando conectaba la placa de red USB en caliente.

---

# Changelog - SysStatCLI v2.41.20250523k

## 🇺🇸🇬🇧 English

- Much of the get_lan_info (Lan) code has been rewritten.

- The argument conditions have been optimized, with simpler and cleaner code.

Ex: before:

```python
if not ("bar" in omit or "b" in omit or "barc" in omit or "bc" in omit):
```

Now:

```python
if {"bar", "b", "barc", "bc"}.isdisjoint(omit):
```
Much clearer and easier to maintain.

- The colors have been changed to brighter and purer colors.

- The status line has been given a "DIM" style, making it more subdued and separating the data displayed by the program from the program's data.

---

## 🇪🇸 Español

- Se reescribió gran parte del código de get_lan_info (Lan).

- Se optimizo los condicionantes de los argumentos, con un código mas sencillo y limpio.

Ej: antes:

```python
if not ("bar" in omit or "b" in omit or "barc" in omit or "bc" in omit):
```

Ahora: 

```python
if {"bar", "b", "barc", "bc"}.isdisjoint(omit):
```
Mucho mas claro y facil de mantener.

- Se cambiaron los colores por unos mas vividos y puros.

- Se puso el estilo "DIM" al statusline. Para que sea mas tenue y que quede separado de los datos que muestra el programa con los datos del programa.

---

# Changelog - SysStatCLI v2.41.20250520h

## 🇺🇸🇬🇧 English

- The algorithm for calculating memory used by programs "█", the system "▒", and free memory "░" has been improved and optimized.

- The option to exit by pressing the Q or X key has been added (for now, Esc has been disabled because the system is not responding correctly).

- The last line of execution information has been modified:

Old:

```
Run: 21:19:10 (0.061s) / Cycles: 77 / Next in 66/600 seconds...
```

New, simpler and more compact:

```
Run: 21:19:10 (61ms) | Cycles: 77 | Next: 66/600s... 
```

#### 🐞 Fixes and 🧹 Minor Cleanups and Improvements

As with all previous versions, minor corrections and improvements were also made to other parts of the code.

---

## 🇪🇸 Español

- Se mejoro y optimizo el algoritmo para calcular la memoria utilizada por los programas "█", el sistema "▒" y la libre "░".

- Se agrego la opción de salir presionando las tecla Q o X (por ahora Esc se anulo, porque no responde el sistema correctamente).

- Se modifico la ultima linea de información de ejecución:

Vieja:

```
 Run: 21:19:10 (0.061s) / Cycles: 77 / Next in 66/600 seconds... 
```

Nueva, mas simple y compacta:

```
Run: 21:19:10 (61ms) | Cycles: 77 | Next: 66/600s... 
```

- 🐞 Correcciones y 🧹 limpieza y mejoras menores

Como todas las versión enteriores también se hicieron correcciones y mejoras menores en otras partes del código.

---

# Changelog - SysStatCLI v2.41.20250519g

## 🇺🇸🇬🇧 English

- The RAM progress bar has been modified.
It now displays memory used by applications "█" and memory used by the system (buffers + cache + slab) "▒" and free memory "░"

- General optimizations to other, less significant parts of the code... A little here, a little there, and a little here :)
Registro de cambios - SysStatCLI v2.41.20250519g

---

## 🇪🇸 Español

- Se modifico la barra de progreso de la memoria RAM.
Ahora muestra la memoria usada por las aplicaciones "█" y la usada por el sistema (buffers + cache + slab) "▒" y la memoria libre "░"

- Optimización de otras partes del código en general sin mayor relevancia... Un poco por allí, un poco por allá y otro poco por acá :)

---

# Changelog - SysStatCLI v2.40.20250514e

## 🇺🇸🇬🇧 English

- New -host, -o option:

The -sys, -s option, which was previously hidden, has been separated:

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
Hostname: hal9001c - User: axel
```

Into two separate options:

-sys, -s

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
```

-host, -o

```
Hostname: hal9001c - User: axel
```

- I also updated, modified, and fixed (minor issues) the help: -help, -h, --help

---

## 🇪🇸 Español

- Nueva opción -host, -o:

Se separo la opción -sys, -s, que antes ocultaba:

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
Hostname: hal9001c - User: axel
```

En dos opciones distintas:

-sys, -s

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
```

-host, -o

```
Hostname: hal9001c - User: axel
```

- Ademas me actualizo, modifico y arreglo (problemas menores) del help: -help, -h, --help

---

# Changelog - SysStatCLI v2.40.20250513d

## 🇺🇸🇬🇧 English

- ✨ New Features
Several options have been added to hide progress bars and output either text-only (old-school style) or a specific progress bar from the five available:

Options: Available arguments to omit sections:
- -bar, -b → Omit all bars
- -barc, -bc → Omit the CPU bar
- -barr", -br → Omit the RAM bar
- -bard", -bd → Omit the Disk bar
- -barw", -bw → Omit the WIFI bar
- -bara", -bt → Omit the Battery bar

---

## 🇪🇸 Español

- ✨ Nuevas funciones
Se agregaron varias opción para ocultar las barras de progreso y que la salida sea solo texto (estilo old school) o alguna barra de progreso en particular de las cinco disponibles:

Opciones: Argumentos disponibles para omitir secciones:
- -bar, -b → Omite todas las barras
- -barc, -bc → Omite la barra de CPU
- -barr", -br → Omite la barra de RAM
- -bard", -bd → Omite la barra de Disk
- -barw", -bw → Omite la barra de WIFI
- -bara", -bt → Omite la barra de Battery

---

# Changelog - SysStatCLI v2.40.20250509c

## 🇺🇸🇬🇧 English

- ✨ New Features:

Support for single execution or loop execution with interval (`[time]`).

Added `-help`, `--help`, `-h` arguments to display detailed help.

Inclusion of short aliases for each section (`-s`, `-c`, `-r`, etc.).

Automatic validation of invalid arguments with clear messages.

Link to the repository and author in the help message.

New, more readable and professional help section.


- 🐞 Fixes:

Correct handling of numeric arguments and non-hyphenated text (`Y`, `Hello`, etc.).

Improved `sys.argv` logic to avoid errors when passing parameters.


- 🧹 Cleanup and Minor Improvements:

Reordered code for clarity.

More helpful and consistent error messages.

Bold invalid arguments for better visibility.

---

## 🇪🇸 Español

- ✨ Nuevas funciones:

 Soporte para ejecución única o en bucle con intervalo (`[tiempo]`).
 
 Se agregó argumento `-help`, `--help`, `-h` para mostrar ayuda detallada.
 
 Inclusión de alias cortos para cada sección (`-s`, `-c`, `-r`, etc.).
 
 Validación automática de argumentos inválidos con mensajes claros.
 
 Enlace al repositorio y autor en el mensaje de ayuda.
 
 Nueva sección de ayuda más legible y profesional.
 

- 🐞 Correcciones:

Manejo correcto de argumentos numéricos y texto sin guion (`Y`, `Hola`, etc.).

Mejora en la lógica de `sys.argv` para evitar errores al pasar parámetros.


- 🧹 Limpieza y mejoras menores:

Código reordenado para claridad.

Mensajes de error más útiles y consistentes.

Negrita en argumentos inválidos para mayor visibilidad.

---

Autor: Axel O'BRIEN (LiGNUxMan)  
Repositorio: https://github.com/LiGNUxMan/SysStatCLI

