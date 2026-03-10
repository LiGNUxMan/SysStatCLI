# SysStatCLI (System Status CLI) Version 2.44.20260310a
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square&logo=linux)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-GPLv3-green)

## 🇺🇸🇬🇧 English

<img width="654" height="466" alt="Captura de pantalla de 2025-11-09 10-30-38" src="https://github.com/user-attachments/assets/1feb922f-9da9-4044-ab1c-2f65460edfe0" />

<sub>This screenshot shows all active modules: CPU, RAM, Disk, Network (LAN/WiFi), Temperatures, Battery, and Status Line. All on screen, no scrolling required, and optimized for 80x24 resolution devices.</small>

## Description

**SysStatCLI** is a command-line tool written in Python for real-time system status monitoring in Linux. It provides detailed information on CPU usage, RAM, disk temperature, and Wi-Fi, among other parameters, in a visually organized and color-coded manner for easy interpretation.

Current version 2.44.20260310a: A progress bar for CPU frequency was added. The help function was fixed and improved. Minor details and bugs were corrected elsewhere in the code.

## Features

- **System Information**: Displays the operating system name, kernel version, hostname, and current user.
- **Uptime**: Indicates how long the system has been on and the time and day of the power failure.
- **CPU Utilization**: Displays the total percentage of processor utilization and individual core utilization.
- **CPU Frequency**: Reports the CPU speed in GHz and the active scaling mode.
- **CPU Temperature**: It reports the processor temperature and changes color depending on the level.
- **RAM and Swap Memory**: It shows the percentage of RAM and Swap usage with colors and progress bars.
- **Processes**: Reports the total number of processes and their status (running, suspended, inactive, etc.).
- **System Load**: Displays the load average over 1, 5, and 15 minutes.
- **Disk**: Indicates the percentage of storage occupied in % and GB and the total capacity in GB, as well as the data read and written in MB/s and the temperature.
- **Wired Connection Status**: Displays the connection speed and IP address.
- **Wi-Fi Connection Status**: It shows the network you are connected to and the IP address, signal quality, connection speed, downloaded and uploaded data in MB/s
- **Wi-Fi Card Temperature**: Reports the temperature of the wireless network adapter and changes color based on the temperature level.
- **Battery Status**: Indicates the charge percentage and whether the device is connected to power or discharging (only if the battery is not at 100%).
- **Autorun**: Can run continuously at a frequency determined by the user.
- **Script information**: Execution time, execution speed, completed loops or cycles, and time to next exercise.

## 🗣️ Why use SysStatCLI?

Because it's simple, lightweight, and gives you all the information you need without leaving the console. Ideal for modest rigs, headless servers, or total control freaks.

## Installation and Use

### Requirements
- Python 3.x
- Linux with support for `psutil`, `iwconfig`, `sensors`, and `/proc/`

### 📏 80x24 Support

🖥️ Optimized Layout for Classic 80x24 Terminals

SysStatCLI is carefully designed to fit perfectly on standard terminals (80 columns x 24 rows), without unnecessary scrolling or wasted lines.

### 🚀 Run

```bash
python3 sysstatcli.py [time] [options]
```

- `time`: Interval in seconds to repeat the script in a loop. If omitted or `0`, it is executed **only once**.

  During execution, you can press Q or X to exit.
  
- `options`: Arguments to skip certain sections of the monitoring.

#### 🔧 Available Options
| Section       | Arguments               | Description                              |
|---------------|-------------------------|------------------------------------------|
| System        | `-sys`, `-s`            | Operating system name and kernel version |
| Hostname      | `-host`, `-o`           | Computer and user name                   |
| Uptime        | `-up`, `-u`             | System uptime and time and day           |
| CPU           | `-cpu`, `-c`            | Usage, frequency, and temperature        |
| RAM           | `-ram`, `-r`            | RAM and Swap memory usage                |
| Processes     | `-proc`, `-p`           | Process count and status                 |
| Load          | `-load`, `-l`           | Average System Load                      |
| Disk          | `-disk`, `-d`           | Disk usage, speed, and temperature       |
| LAN           | `-lan`, `-a`            | Wired network status                     |
| WiFi          | `-wifi`, `-w`           | WiFi status and motherboard temperature  |
| Battery       | `-bat`, `-t`            | Power level, time remaining, and mode    |
| Bar           | `-bar`, `-b`            | Omit all bars                            |
|               | `-barc`, `-bc`          | Omit the CPU bar                         |
|               | `-barf`, `-bf`          | Omit the CPU frequency bar               |
|               | `-barr`, `-br`          | Omit the RAM bar                         |
|               | `-bard`, `-bd`          | Omit the Disk bar                        |
|               | `-barw`, `-bw`          | Omit the WIFI bar                        |
|               | `-bara`, `-bt`          | Omit the Battery bar                     |
| Icons         | `-icon`, `-i`           | Omits descriptive icons                  |
| Help          | `-help`, `-h`, `--help` | Show help and exit                       |

---

## 🧪 Examples

```bash
python3 sysstatcli.py
```
> Runs once, displaying all information.

```bash
python3 sysstatcli.py 30
```
> Runs monitoring every 30 seconds.

```bash
python3 sysstatcli.py -ram -wifi
```
> Runs once, ignoring RAM and WiFi.

```bash
python3 sysstatcli.py -s -b 10
```
> Runs every 10 seconds, ignoring system and battery data.

```bash
python3 sysstatcli.py -i 60
```
> Runs every 60 seconds, omitting descriptive icons.

## 🆘 Help

```bash
python3 sysstatcli.py -h
```
Or also: `--help` or `-help`

---
## ⚠️ IMPORTANT NOTE

This script was written and tested on an notebook **HP Pavilion x360 Convertible 15-br0xx** *(103C_5335KV HP Pavilion)*. Surely, for it to work on your PC, notebook, server, etc., you'll have to make some adjustments to certain parameters:

### 🎨 CPU frequency:

In my case, the processor frequency is set with the following colors:

- **0.4 - 0.8 GHz** → 🟢 Normal
- **0.8 - 2.5 GHz** → 🟡 Yellow
- **2.5 - 3.1 GHz** → 🟠 Orange *(Turbo)*
- **3.1 GHz** → 🔴 Red *(Maximum)*

### 🌡️ CPU temperature:

The CPU temperature can be found using psutil /coretemp, you can also get it by reading the file:
```bash
/sys/class/thermal/thermal_zone0/temp
```
If it's not there in your case, you'll need to check where it's available on your system.
Configured colors:

- **< 35°C** → 🟢 Normal
- **35 - 40°C** → 🟡 Yellow
- **40 - 60°C** → 🟠 Orange
- **> 60°C** → 🔴 Red

### 💾 RAM usage:

- < 75% → 🟢 Normal
- 75–89% → 🟡 Moderate
- ≥ 90% → 🔴 Critical

### 📈 Load average:
Colors based on system load level:

- -3.0 → 🟢 Normal
- 3.0 – 4.0 → 🟡 High load (75%+)
- +4.0 → 🔴 Saturated (more processes than cores)

### 💾 Disk temperature:

In my case, I have an **M.2 NVMe** disk and I get the temperature with the command psutil.sensors_temperatures / nvme (see script), you can also get it from the command:
```bash
sensors
```
Searching for the **"nvme-pci-0100"** → **"Composite:"** devices. Then, the data is wiped, leaving only the temperature.

nvme-pci-0100  
Adapter: PCI adapter  
Composite: +31.9°C  

Configured Colors:

- -50°C → 🟢 Normal
- 50 - 70°C → 🟡 Yellow
- +70°C → 🔴 Red

### 📶 WiFi Card Configuration:

On my PC, the WiFi device is called **"wlp3s0"**. To get its name on your computer, run the command:
```bash
iwconfig
```
If it's named differently, you'll need to modify the script accordingly.

🎯 Wi-Fi Signal:

- 70–100% → 🟢 Excellent
- 40–69% → 🟡 Average
- 0–39% → 🔴 Poor

🌡️ Wi-Fi Temperature:

- 75–100% → 🟢 Excellent
- 50–74% → 🟡 Good
- 50–26% → 🟠 Fair
- 25–0% → 🔴 Poor

### 🔋 Battery:

The battery data in my case is located at:
```bash
/sys/class/power_supply/BAT0/
```
In your case, it could be in **BAT1** or another location. Check and adjust as needed.

⚙️ *If you need to adapt the script, review these parameters and adjust them according to your equipment.*
---

### Sample Output

<img width="654" height="466" alt="Captura de pantalla de 2025-11-09 10-30-38" src="https://github.com/user-attachments/assets/f45005f2-b676-4112-a42b-7e23139c23d2" />

```
🐧 OS: Linux Mint 22.2 - ⚙️ Kernel version: 6.14.0-35-generic
🏠 Hostname: hal9001c - 👤 User: axel
⏱️ Uptime: 2 days, 1:00:40 - 🕒 Time and date: 10:30:27 09/11/2025
🤖 CPU used: 8% (CPU0: 8% - CPU1: 8% - CPU2: 8% - CPU3: 7%)
   ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
⚡  CPU frequency: 1.00GHz - 🎚️ Scaling governor: powersave
   ██████████░░░░░░░░░░░░░░░░░░░░░░
🌡️ CPU temperature: 25°C
🧮 RAM used: 31% (4.80GB / 15.50GB) - 💾 Swap used: 0% (0.00GB / 0.00GB)
   █████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
🧩 Processes: 258 (run=2, sleep=190, idle=66, stop=0, zombie=0, other=0)
📊 Load average: 0.46 0.91 1.58
🗄️ Disk used: 47% (222.05GB / 467.91GB) - Read: 0.36MB/s - Write: 0.08MB/s
   ███████████████░░░░░░░░░░░░░░░░░
🌡️ Disk temperature: 29°C
📶 WiFi IP: 192.168.0.208 - SSID: OBRIEN 5
📡 WiFi signal: 62% - Speed: 292.6Mb/s - Down: 0.00MB/s - Up: 0.00MB/s
   ███████████████████░░░░░░░░░░░░░
🌡️ WiFi temperature: 28°C
🔋 Battery: 24% - Time: 0h 40m - Mode: Discharging
   ███████░░░░░░░░░░░░░░░░░░░░░░░░░
🔁 Run: 1 day, 0:11:43 (39/86/256ms) | Cycles: 531 | 16.34MB | Next: 49/60s
```

## Contributions
Any improvements, corrections, or suggestions are welcome. Add your contribution to this project!

## Author
- **Axel O'BRIEN (LiGNUxMan)** - [GitHub Profile](https://github.com/LiGNUxMan/)
- **ChatGPT** - Development Support

## License
This project is distributed under the **GPLv3** license. Feel free to use, modify, and share it!

> Made with 💚 and a passion for free software.

## 🚀 Future Improvements and Features
We're looking for contributors to continue improving SysStatCLI. Here are some ideas for future versions:

1️⃣ Add audible alerts: Emit a BEEP when a critical parameter is red (e.g., high temperature, excessive CPU usage, or full disk).

3️⃣ Data logging and analysis:
Save the system status to a log file with timestamps.
Implement an option to generate graphs showing the evolution of CPU, memory, temperature, etc. usage.

4️⃣ GUI version:
Create a graphical interface in GTK to display the data in a more user-friendly way.

5️⃣ Standalone execution:
Compile the script into an executable so that it runs without the need for Python.


**If you're interested in contributing, open an issue or make a pull request! 🤝**


---
# SysStatCLI (System Status CLI) Version 2.43.20251108a
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square&logo=linux)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-GPLv3-green)

## 🇪🇸 Español

<img width="654" height="466" alt="Captura de pantalla de 2025-11-09 10-30-38" src="https://github.com/user-attachments/assets/7e1a135d-d06e-483d-a746-1d12fdb1bfe2" />

<sub>Esta captura muestra todos los módulos activos: CPU, RAM, Disco, Red (LAN/WiFi), Temperaturas, Batería y línea de estado. Todo en pantalla, sin necesidad de scroll y optimizado para terminales de 80x24.</small>

## Descripción

**SysStatCLI** es una herramienta de línea de comandos escrita en Python para monitorear en tiempo real el estado del sistema en Linux. Proporciona información detallada sobre el uso del CPU, memoria RAM, temperatura del disco y WiFi, entre otros parámetros, de una forma visualmente organizada y con colores para facilitar la interpretación de los datos.

Actual versión 2.44.20260310a: Se agregó una barra de progreso para la frecuencia de la CPU. Se corrigió y mejoró el help. Se corrigieron detalles y errores menores en otras partes del código.

## Características

- **Información del sistema**: Muestra el nombre del sistema operativo, la versión del kernel, el nombre de host y el usuario actual.
- **Tiempo de actividad (Uptime)**: Indica cuánto tiempo ha estado encendido el sistema y la hora y dia del mismo.
- **Uso del CPU**: Muestra el porcentaje total de uso del procesador y el uso individual de cada núcleo.
- **Frecuencia del CPU**: Reporta la velocidad del CPU en GHz y el modo de escalado activo.
- **Temperatura del CPU**: Informa la temperatura del procesador y cambia de color segun el nivel.
- **Memoria RAM y Swap**: Indica el porcentaje de uso de la RAM y la Swap con colores y barras de progreso.
- **Procesos**: Reporta la cantidad total de procesos y su estado (ejecución, suspensión, inactivos, etc.).
- **Carga del sistema**: Muestra el promedio de carga en 1, 5 y 15 minutos.
- **Disco**: Indica el porcentaje de almacenamiento ocupado en % y GB y la capacidad total en GB, ademas de los datos leidos y escritos en MB/s y la temperatura.
- **Estado de la conexión cableada**: Muestra la velocidad de conexión y la dirección IP.
- **Estado de la conexión WiFi**: Muestra la calidad de la señal, la velocidad de conexión, la red a la que está conectado y la dirección IP.
- **Temperatura de la tarjeta WiFi**: Reporta la temperatura del adaptador de red inalámbrico y cambia de color segun el nivel del la misma.
- **Estado de la batería**: Indica el porcentaje de carga y si el equipo está conectado a la corriente o descargándose (solo si la batería no está al 100%).
- **Ejecución automática**: Puede ejecutarse en modo continuo con una frecuencia determinada por el usuario.
- **Información del script**: Tiempo de ejecución, velocidad de ejecución, bucles o ciclos completados y tiempo para la próxima ejercicio.

## 🗣️ ¿Por qué usar SysStatCLI?

Porque es simple, liviano, y te da toda la información que necesitás sin salir de la consola. Ideal para equipos modestos, servidores headless o fanáticos del control total.

## Instalación y Uso

### Requisitos
- Python 3.x
- Linux con soporte para `psutil`, `iwconfig`, `sensors` y `/proc/`

### 📏 Compatibilidad con 80x24

🖥️ Diseño optimizado para terminales clásicas de 80x24

SysStatCLI está cuidadosamente construido para caber perfectamente en terminales estándar (80 columnas x 24 filas), sin scroll innecesario ni líneas desperdiciadas.

### 🚀 Ejecución

```bash
python3 sysstatcli.py [tiempo] [opciones]
```

- `tiempo`: Intervalo en segundos para repetir el script en bucle. Si se omite o es `0`, se ejecuta **una sola vez**.

  Durante la ejecución, puede presionar Q o X para salir.
  
- `opciones`: Argumentos para omitir ciertas secciones del monitoreo.

#### 🔧 Opciones disponibles
| Sección       | Argumentos              | Descripción                                       |
|---------------|-------------------------|---------------------------------------------------|
| Sistema       | `-sys`, `-s`            | Nombre del sistema operativo y version del kernel |
| Hostname      | `-host`, `-o`           | Nombre de la computadora y el usuario             |
| Uptime        | `-up`, `-u`             | Tiempo de actividad y hora y dia del sistema      |
| CPU           | `-cpu`, `-c`            | Uso, frecuencia y temperatura                     |
| RAM           | `-ram`, `-r`            | Uso de memoria RAM y Swap                         |
| Procesos      | `-proc`, `-p`           | Conteo y estados de procesos                      |
| Carga         | `-load`, `-l`           | Carga promedio del sistema                        |
| Disco         | `-disk`, `-d`           | Uso, velocidad y temperatura del disco            |
| Red LAN       | `-lan`, `-n`            | Estado de la red cableada                         |
| Red WiFi      | `-wifi`, `-w`           | Estado de WiFi y temperatura de la placa          |
| Batería       | `-bat`, `-b`            | Nivel, tiempo restante y modo de energía          |
| Barra         | `-bar`, `-b`            | Omite todas las barras                            |
|               | `-barc`, `-bc`          | Omite la barra de CPU                             |
|               | `-barf`, `-bf`          | Omite la barra de frecuencia del CPU              |
|               | `-barr`, `-br`          | Omite la barra de RAM                             |
|               | `-bard`, `-bd`          | Omite la barra de Disco                           |
|               | `-barw`, `-bw`          | Omite la barra de WiFi                            |
|               | `-bara`, `-bt`          | Omite la barra de bateria                         |
| Iconos        | `-icon`, `-i`           | Omite los iconos descrptivos                      |
| Ayuda         | `-help`, `-h`, `--help` | Muestra la ayuda y sale                           |

---

## 🧪 Ejemplos

```bash
python3 sysstatcli.py
```
> Ejecuta una sola vez mostrando toda la información.

```bash
python3 sysstatcli.py 30
```
> Ejecuta el monitoreo cada 30 segundos.

```bash
python3 sysstatcli.py -ram -wifi
```
> Ejecuta una sola vez, omitiendo RAM y WiFi.

```bash
python3 sysstatcli.py -s -b 10
```
> Ejecuta cada 10 segundos, omitiendo datos del sistema y batería.

```bash
python3 sysstatcli.py -i 60
```
> Ejecuta cada 60 segundos, omitiendo iconos descriptivos.

## 🆘 Ayuda

```bash
python3 sysstatcli.py -h
```

O también: `--help` o `-help`

---
## ⚠️ NOTA IMPORTANTE

Este script está hecho y probado en una notebook **HP Pavilion x360 Convertible 15-br0xx** *(103C_5335KV HP Pavilion)*. Seguramente, para que funcione en tu PC, notebook, servidor, etc., tendrás que hacer algunos ajustes en ciertos parámetros:

### 🎨 CPU frequency:

En mi caso, la frecuencia del procesador está ajustada con los siguientes colores:

- **0,4 - 0,8 GHz** → 🟢 Normal
- **0,8 - 2,5 GHz** → 🟡 Amarillo
- **2,5 - 3,1 GHz** → 🟠 Naranja *(Turbo)*
- **3,1 GHz** → 🔴 Rojo *(Máximo)*

### 🌡️ CPU temperature:

La temperatura del CPU usando psutil / coretemp, tambien la puedes obteener leyendo el archivo:
```bash
/sys/class/thermal/thermal_zone0/temp
```
Si en tu caso no se encuentra allí, deberás revisar dónde está disponible en tu sistema.

Colores configurados:

- **< 35°C** → 🟢 Normal
- **35 - 40°C** → 🟡 Amarillo
- **40 - 60°C** → 🟠 Naranja
- **> 60°C** → 🔴 Rojo

### 💾 RAM usage:

- < 75% → 🟢 Normal
- 75–89% → 🟡 Moderado
- ≥ 90% → 🔴 Crítico

### 📈 Load average:
Colores según el nivel de saturación del sistema:

- -3.0 → 🟢 Normal
- 3.0 – 4.0 → 🟡 Carga alta (75%+)
- +4.0 → 🔴 Saturado (más procesos que núcleos)

### 💾 Disk temperature:

En mi caso, tengo un disco **M.2 NVMe** y obtengo la temperatura con el comando psutil.sensors_temperatures / nvme (ver script), tambien la puedes obtener del comando:
```bash
sensors
```
Buscando los dispositivos **"nvme-pci-0100"** → **"Composite:"**. Luego, se limpian los datos dejando solo la temperatura.

nvme-pci-0100  
Adapter: PCI adapter  
Composite: +31.9°C  

Colores configurados:

- **< 50°C** → 🟢 Normal
- **50 - 70°C** → 🟡 Amarillo
- **> 70°C** → 🔴 Rojo

### 📶 Configuración de la Placa WiFi:

En mi PC, el dispositivo WiFi se llama **"wlp3s0"**. Para obtener su nombre en tu equipo, ejecuta el comando:
```bash
iwconfig
```
Si se llama diferente, tendrás que modificar el script en consecuencia.

🎯 Señal WiFi:

- 75–100% → 🟢 Excelente
- 50-74% → 🟡 Buena
- 50–26% → 🟠 Regular
- 25–0% → 🔴 Mala

🌡️ Temperatura del WiFi:

- -50°C → 🟢 Normal
- 50–70°C → 🟡 Moderada
- +70°C → 🔴 Alta

### 🔋 Battery:

Los datos de la batería en mi caso se encuentran en:
```bash
/sys/class/power_supply/BAT0/
```
En tu caso, podría estar en **BAT1** u otra ubicación. Verifica y ajusta según sea necesario.

⚙️ *Si necesitas adaptar el script, revisa estos parámetros y ajústalos según tu equipo.*
---

### Ejemplo de salida

<img width="654" height="466" alt="Captura de pantalla de 2025-11-09 10-30-38" src="https://github.com/user-attachments/assets/4fa5ac41-d3fc-4770-a353-c62697cca6ad" />

```
🐧 OS: Linux Mint 22.2 - ⚙️ Kernel version: 6.14.0-35-generic
🏠 Hostname: hal9001c - 👤 User: axel
⏱️ Uptime: 2 days, 1:00:40 - 🕒 Time and date: 10:30:27 09/11/2025
🤖 CPU used: 8% (CPU0: 8% - CPU1: 8% - CPU2: 8% - CPU3: 7%)
   ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
⚡  CPU frequency: 1.00GHz - 🎚️ Scaling governor: powersave
   ██████████░░░░░░░░░░░░░░░░░░░░░░
🌡️ CPU temperature: 25°C
🧮 RAM used: 31% (4.80GB / 15.50GB) - 💾 Swap used: 0% (0.00GB / 0.00GB)
   █████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
🧩 Processes: 258 (run=2, sleep=190, idle=66, stop=0, zombie=0, other=0)
📊 Load average: 0.46 0.91 1.58
🗄️ Disk used: 47% (222.05GB / 467.91GB) - Read: 0.36MB/s - Write: 0.08MB/s
   ███████████████░░░░░░░░░░░░░░░░░
🌡️ Disk temperature: 29°C
📶 WiFi IP: 192.168.0.208 - SSID: OBRIEN 5
📡 WiFi signal: 62% - Speed: 292.6Mb/s - Down: 0.00MB/s - Up: 0.00MB/s
   ███████████████████░░░░░░░░░░░░░
🌡️ WiFi temperature: 28°C
🔋 Battery: 24% - Time: 0h 40m - Mode: Discharging
   ███████░░░░░░░░░░░░░░░░░░░░░░░░░
🔁 Run: 1 day, 0:11:43 (39/86/256ms) | Cycles: 531 | 16.34MB | Next: 49/60s
```

## Contribuciones
Cualquier mejora, corrección o sugerencia es bienvenida. ¡Suma tu aporte a este proyecto!

## Autor
- **Axel O'BRIEN (LiGNUxMan)** - [GitHub Profile](https://github.com/LiGNUxMan/)
- **ChatGPT** - Asistencia en desarrollo

## Licencia
Este proyecto se distribuye bajo la licencia **GPLv3**. ¡Úsalo, modifícalo y compártelo libremente!

> Hecho con 💚 y pasión por el software libre.

## 🚀 Mejoras y funcionalidades futuras
Estamos buscando colaboradores para seguir mejorando SysStatCLI. Estas son algunas ideas para futuras versiones:

1️⃣ Agregar alertas sonoras: Emitir un BEEP cuando algún parámetro crítico esté en rojo (por ejemplo, alta temperatura, uso excesivo de CPU o disco lleno).

3️⃣ Registro y análisis de datos:
Guardar el estado del sistema en un archivo de registro (log) con marcas de tiempo.
Implementar una opción para generar gráficos con la evolución del uso de CPU, memoria, temperatura, etc.

4️⃣ Versión con GUI:
Crear una interfaz gráfica en GTK para visualizar los datos de manera más amigable.

5️⃣ Ejecución independiente:
Compilar el script en un ejecutable para que funcione sin necesidad de Python instalado.


**Si te interesa contribuir, ¡abre un issue o haz un pull request! 🤝**

