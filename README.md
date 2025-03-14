# SysStatCLI (System Status CLI)

## English

## Description

**SysStatCLI** is a command-line tool written in Python for real-time system status monitoring in Linux. It provides detailed information on CPU usage, RAM, disk temperature, and Wi-Fi, among other parameters, in a visually organized and color-coded manner for easy interpretation.

## Features

- **System Information**: Displays the operating system name, kernel version, hostname, and current user.
- **Uptime**: Indicates how long the system has been powered on.
- **CPU Utilization**: Displays the total percentage of processor utilization and individual core utilization.
- **CPU Frequency**: Reports the CPU speed in GHz and the active scaling mode.
- **CPU Temperature**: Reports the processor temperature with color-coded heatsinks.
- **RAM and SWAP Memory**: Indicates the percentage of RAM and SWAP usage with progress bars.
- **Processes**: Reports the total number of processes and their status (running, suspended, inactive, etc.).
- **System Load**: Displays the load average over 1, 5, and 15 minutes.
- **Disk Usage**: Indicates the percentage of occupied storage and the temperature of the NVMe drive.
- **Wi-Fi Connection Status**: Displays the signal quality, connection speed, the network you are connected to, and the IP address.
- **Wi-Fi Card Temperature**: Reports the temperature of the wireless network adapter.
- **Battery Status**: Indicates the charge percentage and whether the device is connected to power or discharging (only if the battery is not at 100%).
- **Autorun**: Can run continuously at a frequency determined by the user.

## Installation and Use

### Requirements
- Python 3.x
- Linux with support for `psutil`, `iwconfig`, `sensors`, and `/proc/`

### Execution
To run the script once:
```bash
python3 sysstatcli.py
```

To run it continuously every *X* seconds:
```bash
python3 sysstatcli.py 60 # It will update every 60 seconds
```

### IMPORTANT NOTE:

This script was written and tested on an HP Pavilion x360 Convertible 15-br0xx (103C_5335KV HP Pavilion) notebook. For it to work on your PC, notebook, server, etc., you'll likely need to make some adjustments to some parameters:

**CPU frequency:** The processor frequency colors. In my case, it's set to:

0.4 - 0.8GHz = Normal
0.8 - 2.5GHz = Yellow
2.5 - 3.1GHz = Orange (Turbo)
3.1GHz = Red (Maximum)

**CPU temperature:**

In my case, I get the CPU temperature by reading the file "/sys/class/thermal/thermal_zone0/temp". In your case, you'll need to check if your PC's CPU temperature is located in that file or in another file or device.
You'll also need to adjust the color according to your needs. In my case it's:

<35 = Normal
35 - 40 = Yellow
40 - 60 = Orange
>60 = Red

**Disk temperature:**

In my case, I have an M.2 NVME drive, and I get the temperature by calling the "sensors" command, capturing the output, and searching for the "nvme-pci-0100" / "Composite:" device. The data is then cleared, leaving only the temperature.

<50 = Normal
50 - 70 = Yellow
>70 = Red

On my PC, the Wi-Fi device is called "wlp3s0." From there, I get the data needed to display it on the screen. If it's called something else, you'll have to modify the script. Run the "iwconfig" command and search for the name of the Wi-Fi network card you want to display.

**Battery:**

In my particular case, the battery data is located in "/sys/class/power_supply/BAT0/", but you might need to make minor adjustments because it could be in BAT1 or somewhere else.

### Sample Output

![sysstatcli2](https://github.com/user-attachments/assets/4c7bc675-1e46-42c8-aa8f-619f6f7ea39e)

```
OS: Linux Mint 22.1 - Kernel version: 6.11. 0-19-generic
Hostname: hal9001c - User: axel
Uptime: 1 day, 3:05:17 - Time and date: 14:42:33 03/13/2025
CPU used: 2% (CPU0: 3% - CPU1: 1% - CPU2: 1% - CPU3: 3%)
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
CPU frequency: 1.0GHz - Scaling governor: powersave
CPU temperature: 37°C
RAM used: 34% (5.28GB / 15.49GB) - SWAP used: 0% (0.00GB / 0.00GB)
██████████░░░░░░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Processes: 269 (running=1, sleeping=201, idle=67, stopped=0, zombie=0, other=0)
Load average: 1.24 1.47 1.14
Disk used: 43% (201.20GB / 467.91GB)
█████████████░░░░░░░░░░░░░░░░░░░
Disk temperature: 32°C
WIFI signal: 57% - Speed: 0.0Mb/s - Lan: OBRIEN 5 - IP: 192.168.0.208
██████████████████░░░░░░░░░░░░░░
WIFI temperature: 41°C
Battery: 47% - Mode: Discharging
███████████████░░░░░░░░░░░░░░░░░
Runs: 118 / Next run in 17/60 seconds...
```

## Contributions
Any improvements, corrections, or suggestions are welcome. Add your contribution to this project!

## Author
- **Axel O'BRIEN (LiGNUxMan)** - [GitHub Profile](https://github.com/LiGNUxMan/)
- **ChatGPT** - Development Support

## License
This project is distributed under the **GPLv3** license. Feel free to use, modify, and share it!

## 🚀 Future Improvements and Features
We're looking for contributors to continue improving SysStatCLI. Here are some ideas for future versions:

1️⃣ Display the wired network card parameters.

2️⃣ Add audible alerts: Emit a BEEP when a critical parameter is red (e.g., high temperature, excessive CPU usage, or full disk).

3️⃣ Data logging and analysis:
Save the system status to a log file with timestamps.
Implement an option to generate graphs showing the evolution of CPU, memory, temperature, etc. usage.

4️⃣ GUI version:
Create a graphical interface in GTK to display the data in a more user-friendly way.

5️⃣ Standalone execution:
Compile the script into an executable so that it runs without the need for Python.


**If you're interested in contributing, open an issue or make a pull request! 🤝**


# SysStatCLI (System Status CLI)

## Castellano

## Descripción

**SysStatCLI** es una herramienta de línea de comandos escrita en Python para monitorear en tiempo real el estado del sistema en Linux. Proporciona información detallada sobre el uso del CPU, memoria RAM, temperatura del disco y WiFi, entre otros parámetros, de una forma visualmente organizada y con colores para facilitar la interpretación de los datos.

## Características

- **Información del sistema**: Muestra el nombre del sistema operativo, la versión del kernel, el nombre de host y el usuario actual.
- **Tiempo de actividad (Uptime)**: Indica cuánto tiempo ha estado encendido el sistema.
- **Uso del CPU**: Muestra el porcentaje total de uso del procesador y el uso individual de cada núcleo.
- **Frecuencia del CPU**: Reporta la velocidad del CPU en GHz y el modo de escalado activo.
- **Temperatura del CPU**: Informa la temperatura del procesador con colores según el nivel de calor.
- **Memoria RAM y SWAP**: Indica el porcentaje de uso de la RAM y la SWAP con barras de progreso.
- **Procesos**: Reporta la cantidad total de procesos y su estado (ejecución, suspensión, inactivos, etc.).
- **Carga del sistema**: Muestra el promedio de carga en 1, 5 y 15 minutos.
- **Uso del disco**: Indica el porcentaje de almacenamiento ocupado y la temperatura del disco NVMe.
- **Estado de la conexión WiFi**: Muestra la calidad de la señal, la velocidad de conexión, la red a la que está conectado y la dirección IP.
- **Temperatura de la tarjeta WiFi**: Reporta la temperatura del adaptador de red inalámbrico.
- **Estado de la batería**: Indica el porcentaje de carga y si el equipo está conectado a la corriente o descargándose (solo si la batería no está al 100%).
- **Ejecución automática**: Puede ejecutarse en modo continuo con una frecuencia determinada por el usuario.

## Instalación y Uso

### Requisitos
- Python 3.x
- Linux con soporte para `psutil`, `iwconfig`, `sensors` y `/proc/`

### Ejecución
Para ejecutar el script una sola vez:
```bash
python3 sysstatcli.py
```

Para ejecutarlo de forma continua cada *X* segundos:
```bash
python3 sysstatcli.py 60  # Se actualizará cada 60 segundos
```

### NOTA IMPORTANTE:

Este script esta hecho y probado en una notebook HP Pavilion x360 Convertible 15-br0xx (103C_5335KV HP Pavilion). Seguramente para que funcione en tu PC, notebook, server. etc. tendrás que hacer algunos ajustes en algunos parámetros que son:

**CPU frequency:** Los colores de la frecuencia del procesador. En mi caso esta ajustado para:

0,4 - 0,8GHz = Normal
0,8 - 2,5GHz = Amarillo
2,5 - 3,1GHz = Naranja (Turbo)
3,1GHz = Rojo (maximo)

**CPU temperature:**

En mi caso la temperatura del CPU la obtengo leyendo el archivo "/sys/class/thermal/thermal_zone0/temp". En tu caso tendrás que ver si en tu PC la temperatura del CPU se encuentra en ese archivo o en otro archivo o dispositivo.
Ademas tendrás que ajustar el color de acuerdo a tu conveniencia. En mi caso es:

<35 = Normal
35 - 40 = Amarillo
40 - 60 = Naranja
>60 = Rojo

**Disk temperature:**

En mi caso tengo un disco M.2 NVME y obtengo la temperatura llamando al comando "sensors" y capturando la salida y buscando el dispositivo "nvme-pci-0100" / "Composite:" Luego se limpian los datos dejando solo la temperatura.

<50 = Normal
50 - 70 = Amarillo
>70 = Rojo

En mi PC el dispositivo Wifi se llama "wlp3s0" Y de ahí obtengo los datos necesarios para mostrar en pantalla, si en tu caso se llama diferente tendrás que modificar el script, ejecuta el comando "iwconfig" y busca como se llama la placa de red Wifi que deseas mostrar.

**Battery:**

En mi caso particular los datos de la batería se encuentran en "/sys/class/power_supply/BAT0/", pero tu a lo mejor tendrías que hacer pequeños ajustes porque puede estar en BAT1 o algún otro lugar.

### Ejemplo de salida

![sysstatcli2](https://github.com/user-attachments/assets/4c7bc675-1e46-42c8-aa8f-619f6f7ea39e)

```
OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
Hostname: hal9001c - User: axel
Uptime: 1 day, 3:05:17 - Time and date: 14:42:33 13/03/2025
CPU used: 2% (CPU0: 3% - CPU1: 1% - CPU2: 1% - CPU3: 3%)
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
CPU frequency: 1.0GHz - Scaling governor: powersave
CPU temperature: 37°C
RAM used: 34% (5.28GB / 15.49GB) - SWAP used: 0% (0.00GB / 0.00GB)
██████████░░░░░░░░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Processes: 269 (running=1, sleeping=201, idle=67, stopped=0, zombie=0, other=0)
Load average: 1.24 1.47 1.14
Disk used: 43% (201.20GB / 467.91GB)
█████████████░░░░░░░░░░░░░░░░░░░
Disk temperature: 32°C
WIFI signal: 57% - Speed: 0.0Mb/s - Lan: OBRIEN 5 - IP: 192.168.0.208
██████████████████░░░░░░░░░░░░░░
WIFI temperature: 41°C
Battery: 47% - Mode: Discharging
███████████████░░░░░░░░░░░░░░░░░
Runs: 118 / Next run in 17/60 seconds...
```

## Contribuciones
Cualquier mejora, corrección o sugerencia es bienvenida. ¡Suma tu aporte a este proyecto!

## Autor
- **Axel O'BRIEN (LiGNUxMan)** - [GitHub Profile](https://github.com/LiGNUxMan/)
- **ChatGPT** - Asistencia en desarrollo

## Licencia
Este proyecto se distribuye bajo la licencia **GPLv3**. ¡Úsalo, modifícalo y compártelo libremente!

## 🚀 Mejoras y funcionalidades futuras
Estamos buscando colaboradores para seguir mejorando SysStatCLI. Estas son algunas ideas para futuras versiones:

1️⃣ Mostrar los parametros de la placa de red cableada.

2️⃣ Agregar alertas sonoras: Emitir un BEEP cuando algún parámetro crítico esté en rojo (por ejemplo, alta temperatura, uso excesivo de CPU o disco lleno).

3️⃣ Registro y análisis de datos:
Guardar el estado del sistema en un archivo de registro (log) con marcas de tiempo.
Implementar una opción para generar gráficos con la evolución del uso de CPU, memoria, temperatura, etc.

4️⃣ Versión con GUI:
Crear una interfaz gráfica en GTK para visualizar los datos de manera más amigable.

5️⃣ Ejecución independiente:
Compilar el script en un ejecutable para que funcione sin necesidad de Python instalado.


**Si te interesa contribuir, ¡abre un issue o haz un pull request! 🤝**

