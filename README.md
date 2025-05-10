# SysStatCLI (System Status CLI) v2.40.20250509c

## 🇺🇸🇬🇧 English

## Description

**SysStatCLI** is a command-line tool written in Python for real-time system status monitoring in Linux. It provides detailed information on CPU usage, RAM, disk temperature, and Wi-Fi, among other parameters, in a visually organized and color-coded manner for easy interpretation.

## Features

- **System Information**: Displays the operating system name, kernel version, hostname, and current user.
- **Uptime**: Indicates how long the system has been on and the time and day of the power failure.
- **CPU Utilization**: Displays the total percentage of processor utilization and individual core utilization.
- **CPU Frequency**: Reports the CPU speed in GHz and the active scaling mode.
- **CPU Temperature**: It reports the processor temperature and changes color depending on the level.
- **RAM and SWAP Memory**: It shows the percentage of RAM and SWAP usage with colors and progress bars.
- **Processes**: Reports the total number of processes and their status (running, suspended, inactive, etc.).
- **System Load**: Displays the load average over 1, 5, and 15 minutes.
- **Disk**: Indicates the percentage of storage occupied in % and GB and the total capacity in GB, as well as the data read and written in MB/s and the temperature.
- **Wired Connection Status**: Displays the connection speed and IP address.
- **Wi-Fi Connection Status**: It shows the network you are connected to and the IP address, signal quality, connection speed, downloaded and uploaded data in MB/s
- **Wi-Fi Card Temperature**: Reports the temperature of the wireless network adapter and changes color based on the temperature level.
- **Battery Status**: Indicates the charge percentage and whether the device is connected to power or discharging (only if the battery is not at 100%).
- **Autorun**: Can run continuously at a frequency determined by the user.
- **Script information**: Execution time, execution speed, completed loops or cycles, and time to next exercise.

## Installation and Use

### Requirements
- Python 3.x
- Linux with support for `psutil`, `iwconfig`, `sensors`, and `/proc/`

### 🚀 Run

```bash
python3 sysstatcli.py [time] [options]
```

- `time`: Interval in seconds to repeat the script in a loop. If omitted or `0`, it is executed **only once**.
- `options`: Arguments to skip certain sections of the monitoring.

### 🔧 Available Options
| Section       | Arguments          | Description                               |
|---------------|--------------------|-------------------------------------------|
| System        | `-sys`, `-s`       | System information and uptime             |
| CPU           | `-cpu`, `-c`       | Usage, frequency, and temperature         |
| RAM           | `-ram`, `-r`       | RAM and swap memory usage                 |
| Processes     | `-proc`, `-p`      | Process count and status                  |
| Load          | `-load`, `-l`      | Average System Load                       |
| Disk          | `-disk`, `-d`      | Disk usage, speed, and temperature        |
| LAN           | `-lan`, `-n`       | Wired network status                      |
| WiFi          | `-wifi`, `-w`      | WiFi status and motherboard temperature   |
| Battery       | `-bat`, `-b`       | Power level, time remaining, and mode     |

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
```

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

The CPU temperature is obtained by reading the file:
```bash
/sys/class/thermal/thermal_zone0/temp
```
If it's not there in your case, you'll need to check where it's available on your system.

Configured colors:

- **< 35°C** → 🟢 Normal
- **35 - 40°C** → 🟡 Yellow
- **40 - 60°C** → 🟠 Orange
- **> 60°C** → 🔴 Red

### 💾 Disk temperature:

In my case, I have an drive **M.2 NVMe** and I get the temperature with the command:
```bash
sensors
```
Searching for the **"nvme-pci-0100"** → **"Composite:"** devices. Then, the data is wiped, leaving only the temperature.

nvme-pci-0100  
Adapter: PCI adapter  
Composite: +31.9°C  

Configured Colors:

- **< 50°C** → 🟢 Normal
- **50 - 70°C** → 🟡 Yellow
- **> 70°C** → 🔴 Red

### 📶 WiFi Card Configuration:

On my PC, the WiFi device is called **"wlp3s0"**. To get its name on your computer, run the command:
```bash
iwconfig
```
If it's named differently, you'll need to modify the script accordingly.

### 🔋 Battery:

The battery data in my case is located at:
```bash
/sys/class/power_supply/BAT0/
```
In your case, it could be in **BAT1** or another location. Check and adjust as needed.

⚙️ *If you need to adapt the script, review these parameters and adjust them according to your equipment.*
---

### Sample Output

![Captura de pantalla de 2025-04-09 22-10-53](https://github.com/user-attachments/assets/45ef972c-49c5-4a3a-a7e0-6666315bb865)

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-21-generic
Hostname: hal9001c - User: axel
Uptime: 14 days, 10:24:21 - Time and date: 22:10:35 09/04/2025
CPU used: 39% (CPU0: 88% - CPU1: 19% - CPU2: 30% - CPU3: 18%)
████████████░░░░░░░░░░░░░░░░░░░░
CPU frequency: 3.10GHz - Scaling governor: powersave
CPU temperature: 62°C
RAM used: 37% (5.72GB / 15.49GB) - SWAP used: 0% (0.00GB / 0.00GB)
███████████░░░░░░░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Processes: 258 (running=2, sleeping=192, idle=63, stopped=0, zombie=0, other=1)
Load average: 2.37 2.28 1.74
Disk used: 43% (202.94GB / 467.91GB) - Read: 0.00MB/s - Write: 0.00MB/s
█████████████░░░░░░░░░░░░░░░░░░░
Disk temperature: 32°C
WIFI lan: OBRIEN 5 - IP: 192.168.0.208
WIFI signal: 54% - Speed: 117.0Mb/s - Download: 0.00MB/s - Upload: 0.00MB/s
█████████████████░░░░░░░░░░░░░░░
WIFI temperature: 40°C
Runs: 1 / Next run inin 42/60 seconds...
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
# SysStatCLI (System Status CLI) v2.40.20250509c

## 🇪🇸 Español

## Descripción

**SysStatCLI** es una herramienta de línea de comandos escrita en Python para monitorear en tiempo real el estado del sistema en Linux. Proporciona información detallada sobre el uso del CPU, memoria RAM, temperatura del disco y WiFi, entre otros parámetros, de una forma visualmente organizada y con colores para facilitar la interpretación de los datos.

## Características

- **Información del sistema**: Muestra el nombre del sistema operativo, la versión del kernel, el nombre de host y el usuario actual.
- **Tiempo de actividad (Uptime)**: Indica cuánto tiempo ha estado encendido el sistema y la hora y dia del mismo.
- **Uso del CPU**: Muestra el porcentaje total de uso del procesador y el uso individual de cada núcleo.
- **Frecuencia del CPU**: Reporta la velocidad del CPU en GHz y el modo de escalado activo.
- **Temperatura del CPU**: Informa la temperatura del procesador y cambia de color segun el nivel.
- **Memoria RAM y SWAP**: Indica el porcentaje de uso de la RAM y la SWAP con colores y barras de progreso.
- **Procesos**: Reporta la cantidad total de procesos y su estado (ejecución, suspensión, inactivos, etc.).
- **Carga del sistema**: Muestra el promedio de carga en 1, 5 y 15 minutos.
- **Disco**: Indica el porcentaje de almacenamiento ocupado en % y GB y la capacidad total en GB, ademas de los datos leidos y escritos en MB/s y la temperatura.
- **Estado de la conexión cableada**: Muestra la velocidad de conexión y la dirección IP.
- **Estado de la conexión WiFi**: Muestra la calidad de la señal, la velocidad de conexión, la red a la que está conectado y la dirección IP.
- **Temperatura de la tarjeta WiFi**: Reporta la temperatura del adaptador de red inalámbrico y cambia de color segun el nivel del la misma.
- **Estado de la batería**: Indica el porcentaje de carga y si el equipo está conectado a la corriente o descargándose (solo si la batería no está al 100%).
- **Ejecución automática**: Puede ejecutarse en modo continuo con una frecuencia determinada por el usuario.
- **Información del script**: Tiempo de ejecución, velocidad de ejecución, bucles o ciclos completados y tiempo para la próxima ejercicio.

## Instalación y Uso

### Requisitos
- Python 3.x
- Linux con soporte para `psutil`, `iwconfig`, `sensors` y `/proc/`

### 🚀 Ejecución

```bash
python3 sysstatcli.py [tiempo] [opciones]
```

- `tiempo`: Intervalo en segundos para repetir el script en bucle. Si se omite o es `0`, se ejecuta **una sola vez**.
- `opciones`: Argumentos para omitir ciertas secciones del monitoreo.

### 🔧 Opciones disponibles
| Sección       | Argumentos         | Descripción                               |
|---------------|--------------------|-------------------------------------------|
| Sistema       | `-sys`, `-s`       | Información del sistema y uptime          |
| CPU           | `-cpu`, `-c`       | Uso, frecuencia y temperatura             |
| RAM           | `-ram`, `-r`       | Uso de memoria RAM y SWAP                 |
| Procesos      | `-proc`, `-p`      | Conteo y estados de procesos              |
| Carga         | `-load`, `-l`      | Carga promedio del sistema                |
| Disco         | `-disk`, `-d`      | Uso, velocidad y temperatura del disco    |
| Red LAN       | `-lan`, `-n`       | Estado de la red cableada                 |
| Red WiFi      | `-wifi`, `-w`      | Estado de WiFi y temperatura de la placa  |
| Batería       | `-bat`, `-b`       | Nivel, tiempo restante y modo de energía  |

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
```
```
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

La temperatura del CPU se obtiene leyendo el archivo:
```bash
/sys/class/thermal/thermal_zone0/temp
```
Si en tu caso no se encuentra allí, deberás revisar dónde está disponible en tu sistema.

Colores configurados:

- **< 35°C** → 🟢 Normal
- **35 - 40°C** → 🟡 Amarillo
- **40 - 60°C** → 🟠 Naranja
- **> 60°C** → 🔴 Rojo

### 💾 Disk temperature:

En mi caso, tengo un disco **M.2 NVMe** y obtengo la temperatura con el comando:
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

### 🔋 Battery:

Los datos de la batería en mi caso se encuentran en:
```bash
/sys/class/power_supply/BAT0/
```
En tu caso, podría estar en **BAT1** u otra ubicación. Verifica y ajusta según sea necesario.

⚙️ *Si necesitas adaptar el script, revisa estos parámetros y ajústalos según tu equipo.*
---

### Ejemplo de salida

![Captura de pantalla de 2025-04-09 22-10-53](https://github.com/user-attachments/assets/42b90bc9-e4cc-4c90-bcad-1ba8ef2024d3)

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-21-generic
Hostname: hal9001c - User: axel
Uptime: 14 days, 10:24:21 - Time and date: 22:10:35 09/04/2025
CPU used: 39% (CPU0: 88% - CPU1: 19% - CPU2: 30% - CPU3: 18%)
████████████░░░░░░░░░░░░░░░░░░░░
CPU frequency: 3.10GHz - Scaling governor: powersave
CPU temperature: 62°C
RAM used: 37% (5.72GB / 15.49GB) - SWAP used: 0% (0.00GB / 0.00GB)
███████████░░░░░░░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Processes: 258 (running=2, sleeping=192, idle=63, stopped=0, zombie=0, other=1)
Load average: 2.37 2.28 1.74
Disk used: 43% (202.94GB / 467.91GB) - Read: 0.00MB/s - Write: 0.00MB/s
█████████████░░░░░░░░░░░░░░░░░░░
Disk temperature: 32°C
WIFI lan: OBRIEN 5 - IP: 192.168.0.208
WIFI signal: 54% - Speed: 117.0Mb/s - Download: 0.00MB/s - Upload: 0.00MB/s
█████████████████░░░░░░░░░░░░░░░
WIFI temperature: 40°C
Runs: 1 / Next run in 42/60 seconds...
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

