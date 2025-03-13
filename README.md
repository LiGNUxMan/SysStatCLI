# SysStatCLI (System Status CLI)

## Descripción

**SysStatCLI** es una herramienta de línea de comandos escrita en Python para monitorear en tiempo real el estado del sistema en Linux. Proporciona información detallada sobre el uso del CPU, memoria RAM, temperatura del disco y WiFi, entre otros parámetros, de una forma visualmente organizada y con colores para facilitar la interpretación de los datos.

## Características

- **Información del sistema**: Muestra el nombre del sistema operativo, la versión del kernel, el nombre de host y el usuario actual.
- **Tiempo de actividad (Uptime)**: Indica cuánto tiempo ha estado encendido el sistema.
- **Uso del CPU**: Muestra el porcentaje total de uso del procesador y el uso individual de cada núcleo.
- **Frecuencia del CPU**: Reporta la velocidad del CPU en GHz y el modo de escalado activo.
- **Temperatura del CPU**: Informa la temperatura del procesador con colores según el nivel de calor.
- **Carga del sistema**: Muestra el promedio de carga en 1, 5 y 15 minutos.
- **Memoria RAM y SWAP**: Indica el porcentaje de uso de la RAM y la SWAP con barras de progreso.
- **Procesos**: Reporta la cantidad total de procesos y su estado (ejecución, suspensión, inactivos, etc.).
- **Uso del disco**: Indica el porcentaje de almacenamiento ocupado y la temperatura del disco NVMe.
- **Estado de la conexión WiFi**: Muestra la calidad de la señal, la velocidad de conexión, la red a la que está conectado y la dirección IP.
- **Temperatura de la tarjeta WiFi**: Reporta la temperatura del adaptador de red inalámbrico.
- **Estado de la batería**: Indica el porcentaje de carga y si el equipo está conectado a la corriente o descargándose (solo si la batería no está al 100%).
- **Ejecución automática**: Puede ejecutarse en modo continuo con una frecuencia determinada por el usuario.
- **Alertas auditivas**: Emite un pitido si algún parámetro se encuentra en estado crítico.

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

### Ejemplo de salida
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
Ejecuciones: 118 / Próxima ejecución en 17/60 segundos...
```

## Contribuciones
Cualquier mejora, corrección o sugerencia es bienvenida. ¡Suma tu aporte a este proyecto!

## Autor
- **Axel O'BRIEN (LiGNUxMan)** - [GitHub Profile](https://github.com/tu_usuario)
- **ChatGPT** - Asistencia en desarrollo

## Licencia
Este proyecto se distribuye bajo la licencia **GPLv3**. ¡Úsalo, modifícalo y compártelo libremente!
