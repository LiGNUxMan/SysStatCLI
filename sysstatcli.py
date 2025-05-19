#!/usr/bin/env python3
# 
# SysStatCLI (System Status CLI) Version 2.41.20250519g
# 
# Autor: Axel O'BRIEN (LiGNUxMan) axelobrien@gmail.com y ChatGPT
# 
# axel@hal9001c:~$ python3 ~/Aplicaciones/sysstatcli.py
# 
# 
# OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
# Hostname: hal9001c - User: axel
# Uptime: 1 day, 3:37:09 - Time and date: 15:14:25 13/03/2025
# CPU used: 39% (CPU0: 38% - CPU1: 36% - CPU2: 41% - CPU3: 40%)
# ████████████░░░░░░░░░░░░░░░░░░░░
# CPU frequency: 0.8GHz - Scaling governor: powersave
# CPU temperature: 39°C
# RAM used: 39% (6.01GB / 15.49GB) - Swap used: 0% (0.00GB / 0.00GB)
# ████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# Processes: 265 (running=1, sleeping=199, idle=65, stopped=0, zombie=0, other=0)
# Load average: 1.97 1.22 0.98
# Disk used: 43% (202.91GB / 467.91GB) - Read: 8.63MB/s - Write: 0.72MB/s
# █████████████░░░░░░░░░░░░░░░░░░░
# Disk temperature: 32°C
# LAN IP: 192.168.0.123 - Speed: 100Mb/s (Full) - Down: 0.01MB/s - Up: 0.01MB/s
# WIFI lan: OBRIEN 5 - IP: 192.168.0.208
# WIFI signal: 71% - Speed: 325.0Mb/s - Download: 4.57MB/s - Upload: 0.93MB/s
# ██████████████████████░░░░░░░░░░
# WIFI temperature: 42°C
# Battery: 35% - Time: 1h 6m 4s - Mode: Discharging
# ███████████░░░░░░░░░░░░░░░░░░░░░
# Run: 3 days, 4:52:51 (0.067s) / Cycles: 1313 / Next in 10/60 seconds...
# 
#

import datetime
import os
import psutil
import re
import socket
import subprocess
import sys
import time
from datetime import timedelta # Linea agregada para el uptime

# Letra normal, bold, amarilla y roja
BOLD = "\033[1m"
ITALIC = "\033[3m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"
GREEN = "\033[92m"
# ORANGE = "\033[38;5;208m"
ORANGE = "\033[38;5;214m" # naranja intenso.
YELLOW = "\033[33m"
RED = "\033[31m"

# Argumentos para omitir funciones (ej: -cpu -ram -wifi)
omit = set(arg[1:].lower() for arg in sys.argv[1:] if arg.startswith("-"))

# Buscar si hay un número entre los argumentos para guardarlo en la variable "interval" que sera cada cuanto se repite el script
interval = 0
for arg in sys.argv[1:]:
    if arg.isdigit():
        interval = int(arg)
        break  # Solo tomamos el primer número encontrad

# Argumentos válidos para omitir secciones o pedir ayuda
valid_args = {"sys", "s", "host", "o", "up", "u", "cpu", "c", "ram", "r", "proc", "p", "load", "l", "disk", "d", "lan", "a", "wifi", "w", "bat", "t", "help", "h", "bar", "b", "barc", "bc", "barr", "br", "bard", "bd", "barw", "bw", "bart", "bt"}

# HELP O AYUDA: sysstatcli.py -help
# if any(arg in help_flags for arg in sys.argv):
if any(arg in ("-h", "--help", "-help") for arg in sys.argv):
    print(f"""{BOLD}SysStatCLI{RESET} (System Status CLI) - Version 2.41.20250519g

{BOLD}Repositorio:{RESET} {UNDERLINE}https://github.com/LiGNUxMan/SysStatCLI{RESET}
    
{BOLD}Autor:{RESET} Axel O'BRIEN ({ITALIC}LiGNUxMan{RESET}) · {UNDERLINE}axelobrien@gmail.com{RESET}
{BOLD}Colaboradora:{RESET} ChatGPT · OpenAI

{BOLD}Uso:{RESET}
  python3 sysstatcli.py [tiempo] [opciones]
  
{BOLD}Tiempo:{RESET} Segundos que se repetira el script en bucle. Si se omite o es 0, se ejecuta una sola vez

{BOLD}Opciones:{RESET} Argumentos disponibles para omitir secciones:
  -sys,  -s → Nombre del sistema operativo y version del kernel
  -host, -o → Nombre de la computadora y el usuario
  -up,   -u → Tiempo de actividad y hora y dia del sistema
  -cpu,  -c → Uso, frecuencia, modo y temperatura del CPU
  -ram,  -r → Uso de memoria RAM y SWAP
  -proc, -p → Procesos y sus estados
  -load, -l → Carga del sistema
  -disk, -d → Uso y temperatura del disco
  -lan,  -a → Red cableada
  -wifi, -w → Red WiFi y temperatura
  -bat,  -t → Batería
  -bar,  -b → Omite todas las barras
    -barc, -bc → Omite la barra de CPU
    -barr, -br → Omite la barra de RAM
    -bard, -bd → Omite la barra de Disk
    -barw, -bw → Omite la barra de WiFi
    -bara, -bt → Omite la barra de Battery

{BOLD}Ejemplos:{RESET}
  python3 sysstatcli.py            → Ejecuta una sola vez
  python3 sysstatcli.py 60         → Ejecuta cada 60 segundos
  python3 sysstatcli.py -ram -wifi → Ejecuta una sola vez, omitiendo RAM y WiFi
  python3 sysstatcli.py -s -b  10  → Ejecuta cada 10s, omitiendo datos del sistema y bateria

{BOLD}Ayuda:{RESET}
  -help, --help, -h → Muestra este mensaje y sale
""")
    sys.exit(0)

# Detectar argumentos inválidos
for arg in sys.argv[1:]:
    # Si es un número, lo aceptamos
    if arg.isdigit():
        continue
    # Si empieza con "-" y no es válido, error
    if arg.startswith("-") and arg[1:].lower() not in valid_args:
        print(f"\nArgumento no válido: {BOLD}{arg}{RESET}")
        print("Usá -h, -help o --help para ver las opciones disponibles.\n")
        sys.exit(1)
    # Si NO empieza con "-" y NO es un número, también es inválido
    if not arg.startswith("-") and not arg.isdigit():
        print(f"\nArgumento no válido: {BOLD}{arg}{RESET}")
        print("Usá -h, -help o --help para ver las opciones disponibles.\n")
        sys.exit(1)

# Variables globales inicializacion
# Se toman estos valores al comienzo de scrpt porque luego seran tomados nuevamente para hacer comparativas
if not ("cpu" in omit or "c" in omit):
    cpu_times_start = psutil.cpu_times(percpu=True)
    cpu_time_start = time.time()
if not ("disk" in omit or "d" in omit):
    disk_io_start = psutil.disk_io_counters()
    disk_time_start = time.time()
if not ("lan" in omit or "n" in omit):
    lan_interface = "enxc025e92940b8" # Nombre de la placa de red
    lan_io_start = psutil.net_io_counters(pernic=True).get(lan_interface)
    lan_time_start = time.time()
if not ("wifi" in omit or "w" in omit):
    wifi_interface = "wlp3s0" # Nombre de la placa WIFI
    wifi_io_start = psutil.net_io_counters(pernic=True).get(wifi_interface)
    wifi_time_start = time.time()
time.sleep(1)  # Pausa de 1 seg. Para mejorar la exactitud de los datos en una sola ejeucuion o la primera del bucle

# Función para generar barra de progreso
def barra_progreso(valor, total=100, ancho=32, color=RESET):
    bloques_llenos = int((valor / total) * ancho)
    barra = "█" * bloques_llenos + "░" * (ancho - bloques_llenos) # barra = "█" * bloques_llenos + " " * (ancho - bloques_llenos) ▁▂▃▄▅▆▇█ ░▒▓█
    return f"{color}{barra}{RESET}" # return f"{color}[{barra}]{RESET}" # return f"{color}▕{barra}▏{RESET}" # return f"{color}[{barra}]{RESET}"

# OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
def get_system_info():
    """Obtiene el nombre del sistema operativo y la versión del kernel y los imprime."""
    try:
        with open("/etc/os-release") as f:
            os_name = None
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    os_name = line.strip().split("=")[1].strip('"')
                    break
    except FileNotFoundError:
        os_name = None

    if os_name is None:
        os_name = f"{RED}Unknown{RESET}"

    with open("/proc/sys/kernel/osrelease") as f:
        kernel_version = f.read().strip()

    print(f"OS: {BOLD}{os_name}{RESET} - Kernel version: {BOLD}{kernel_version}{RESET}")

# Hostname: hal9001c - User: axel
def get_host_user_info():
    hostname = socket.gethostname()
    username = os.getlogin()

    print(f"Hostname: {BOLD}{hostname}{RESET} - User: {BOLD}{username}{RESET}")

# Uptime: 1 day, 3:37:09 - Time and date: 15:14:25 13/03/2025
def get_uptime_and_time():
    """Obtiene el uptime desde /proc/uptime, hora y fecha y los imprime."""
    uptime_seconds = time.time() - psutil.boot_time() # Linea agregada para el uptime de mem_info3_root
    uptime_str = str(timedelta(seconds=int(uptime_seconds))) # Linea agregada para el uptime de mem_info3_root
    current_time = time.strftime("%H:%M:%S %d/%m/%Y")
    print(f"Uptime: {BOLD}{uptime_str}{RESET} - Time and date: {BOLD}{current_time}{RESET}")

# CPU used: 39% (CPU0: 38% - CPU1: 36% - CPU2: 41% - CPU3: 40%)
# ████████████░░░░░░░░░░░░░░░░░░░░
def get_cpu_usage():
    global cpu_times_start, cpu_time_start

    cpu_times_current = psutil.cpu_times(percpu=True)
    cpu_time_current = time.time()

    cpu_time_interval = cpu_time_current - cpu_time_start
#    if cpu_time_interval == 0:
#        return
  
    def get_colored_usage(usage):
        if usage < 33:
            color = RESET
        elif usage < 66:
            color = YELLOW
        elif usage < 99:
            color = ORANGE
        else:
            color = RED
        return f"{color}{BOLD}{usage:.0f}%{RESET}", color

    uso_nucleos = []
    for start, current in zip(cpu_times_start, cpu_times_current):
        total_diff = sum(current) - sum(start)
        idle_diff = current.idle - start.idle
        uso = 100 * (1 - idle_diff / total_diff) if total_diff else 0.0
        uso_nucleos.append(uso)

    promedio_uso = sum(uso_nucleos) / len(uso_nucleos)
    uso_promedio_str, color_barra = get_colored_usage(promedio_uso)

    uso_nucleos_str = " - ".join([f"{ITALIC}CPU{i}{RESET}: {get_colored_usage(uso)[0]}" for i, uso in enumerate(uso_nucleos)])

    print(f"CPU used: {uso_promedio_str} ({uso_nucleos_str})")
    
    if not ("bar" in omit or "b" in omit or "barc" in omit or "bc" in omit):
        print(barra_progreso(promedio_uso, color=color_barra))

    # Actualizar para la siguiente lectura
    cpu_times_start = cpu_times_current
    cpu_time_start = cpu_time_current
 
# CPU frequency: 0.8GHz - Scaling governor: powersave
def get_cpu_frequency():
    """Obtiene la frecuencia del CPU y el scaling_governor y los imprime con colores según el nivel de uso."""
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq") as f:
            min_freq = int(f.read().strip()) / 1000 / 1000
        with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq") as f:
            max_freq = int(f.read().strip()) / 1000 / 1000
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
            cur_freq = int(f.read().strip()) / 1000 / 1000
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor") as f:
            scaling_governor = f.read().strip()
        
        cur_freq = round(cur_freq, 2)

        color = RESET
        if cur_freq >= max_freq:
            color = RED
        elif cur_freq > 2.5:
            color = ORANGE
        elif cur_freq > 0.8: # elif cur_freq > min_freq:
            color = YELLOW
        
        print(f"CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - Scaling governor: {BOLD}{scaling_governor}{RESET}") # {cur_freq:.2f}
    except FileNotFoundError:
        print(f"CPU frequency: {RED}{BOLD}Unknown{RESET} - Scaling governor: {BOLD}{scaling_governor}{RESET}")

# CPU temperature: 39°C
def get_cpu_temperature():
    """Obtiene la temperatura del CPU usando psutil, con fallback a "/sys/class/thermal/thermal_zone0/temp"."""
    try:
        temps = psutil.sensors_temperatures()
        temp = temps["coretemp"][0].current  # Obtiene la primera lectura de temperatura
           
        color = RESET
        if temp > 60:
            color = RED
        elif temp > 40:
            color = ORANGE
        elif temp > 35:
            color = YELLOW
        
        print(f"CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")
    except Exception:
        print(f"CPU temperature: {RED}{BOLD}Unknown{RESET}")

# RAM used: 39% (6.01GB / 15.49GB) - Swap used: 0% (0.00GB / 0.00GB)
# ████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
def get_memory_usage():
    """Obtiene el uso de RAM y Swap y los imprime con colores según el nivel de uso."""

    def color_usage(value):
        if value >= 90:
            return RED, f"{RED}{value:.0f}%{RESET}"
        elif value >= 75:
            return YELLOW, f"{YELLOW}{value:.0f}%{RESET}"
        else:
            return RESET, f"{value:.0f}%"

    with open("/proc/meminfo") as f:
        meminfo = f.readlines()

    # Parseo de /proc/meminfo
    valores = {}
    for linea in meminfo:
        partes = linea.split(":")
        clave = partes[0]
        valor = int(partes[1].strip().split()[0]) / 1024 / 1024  # de kB a GB
        valores[clave] = valor

    mem_total = valores["MemTotal"]
    mem_available = valores["MemAvailable"]
    mem_free = valores["MemFree"]

    # RAM real usada por apps
    mem_used = mem_total - mem_available
    mem_percent = (mem_used / mem_total) * 100

    # Proporciones
    apps_ratio = mem_used / mem_total
    free_ratio = mem_free / mem_total
    sys_ratio = 1 - apps_ratio - free_ratio
        
    # Swap
    swap_total = valores.get("SwapTotal", 0)
    swap_free = valores.get("SwapFree", 0)
    swap_used = swap_total - swap_free
    swap_percent = (swap_used / swap_total) * 100 if swap_total > 0 else 0

    # Colores según uso
    mem_color, mem_colored = color_usage(mem_percent)
    swap_color, swap_colored = color_usage(swap_percent)

    # Salida principal
    print(f"RAM used: {BOLD}{mem_colored}{RESET} ({BOLD}{mem_used:.2f}GB / {mem_total:.2f}GB{RESET}) - "
          f"Swap used: {BOLD}{swap_colored}{RESET} ({BOLD}{swap_used:.2f}GB / {swap_total:.2f}GB{RESET})")

    # Barra personalizada para RAM
    if not ("bar" in omit or "b" in omit or "barr" in omit or "br" in omit):
        def barra_memoria(apps_ratio, sys_ratio, free_ratio, ancho=32):
            apps_blocks = int(ancho * apps_ratio)
            # sys_blocks = int(ancho * sys_ratio)
            # free_blocks = ancho - apps_blocks - sys_blocks
            free_blocks = int(ancho * free_ratio)
            sys_blocks = ancho - apps_blocks - free_blocks
            
            barra = (
                f"{mem_color}{'█' * apps_blocks}" +
                f"{'▒' * sys_blocks}" +
                f"{'░' * free_blocks}{RESET}"
            )
            return barra

        barra_ram = barra_memoria(apps_ratio, sys_ratio, free_ratio)
        barra_swap = barra_progreso(swap_percent, color=swap_color)
        print(f"{barra_ram} - {barra_swap}")

# Processes: 265 (running=1, sleeping=199, idle=65, stopped=0, zombie=0, other=0)
def get_process_count():
    """Obtiene la cantidad total de procesos y el desglose por estados y los imprime."""
    try:
        process_states = {"running": 0, "sleeping": 0, "idle": 0, "stopped": 0, "zombie": 0, "other": 0}
        total_processes = 0
        for pid in os.listdir("/proc"):
            if pid.isdigit():
                total_processes += 1
                try:
                    with open(f"/proc/{pid}/stat") as f:
                        stat_info = f.read().split()
                        state = stat_info[2]
                        if state == "R":
                            process_states["running"] += 1
                        elif state == "S":
                            process_states["sleeping"] += 1
                        elif state == "D":
                            process_states["other"] += 1
                        elif state == "T":
                            process_states["stopped"] += 1
                        elif state == "Z":
                            process_states["zombie"] += 1
                        elif state == "I":
                            process_states["idle"] += 1
                        else:
                            process_states["other"] += 1
                except (FileNotFoundError, ProcessLookupError):
                    continue  # El proceso desapareció antes de que lo leyéramos
                except Exception as e:
                    # Podés imprimir esto en modo debug si querés más info
                    # print(f"Error procesando PID {pid}: {e}")
                    continue
        print(f"Processes: {BOLD}{total_processes}{RESET} "
              f"({ITALIC}run{RESET}={BOLD}{process_states['running']}{RESET}, "
              f"{ITALIC}sleep{RESET}={BOLD}{process_states['sleeping']}{RESET}, "
              f"{ITALIC}idle{RESET}={BOLD}{process_states['idle']}{RESET}, "
              f"{ITALIC}stop{RESET}={BOLD}{process_states['stopped']}{RESET}, "
              f"{ITALIC}zombie{RESET}={BOLD}{process_states['zombie']}{RESET}, "
              f"{ITALIC}other{RESET}={BOLD}{process_states['other']}{RESET})")
    except Exception as e:
        print(f"Processes: {RED}{BOLD}Unknown{RESET}")
        # print(f"Error general en get_process_count: {e}")

# Load average: 1.97 1.22 0.98
def get_load_average():
    """Obtiene el Load Average y lo imprime con colores según la cantidad de núcleos."""
    cpu_count = os.cpu_count()
    load1, load5, load15 = os.getloadavg()
    
    def color_load(value):
        if value >= cpu_count:
            return f"{RED}{value:.2f}{RESET}"
        elif value >= cpu_count * 0.75:
            return f"{YELLOW}{value:.2f}{RESET}"
        else:
            return f"{value:.2f}"
    
    load1_str = color_load(load1)
    load5_str = color_load(load5)
    load15_str = color_load(load15)
    
    print(f"Load average: {BOLD}{load1_str}{RESET} {BOLD}{load5_str}{RESET} {BOLD}{load15_str}{RESET}")

# Disk used: 43% (202.91GB / 467.91GB) - Read: 8.63MB/s - Write: 0.72MB/s
# █████████████░░░░░░░░░░░░░░░░░░░
def get_disk_usage():
    """Obtiene el uso del disco y lo imprime con  con colores según el nivel."""
    st = os.statvfs("/")
    total = st.f_blocks * st.f_frsize / (1024 ** 3)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize / (1024 ** 3)
    percent = (used / total) * 100

    color = RESET
    if percent >= 90: # 90
        color = RED
    elif percent >= 80: # 80
        color = YELLOW

    # Obriene la velocidad de lectura y escritura
    global disk_io_start, disk_time_start

    disk_io_current = psutil.disk_io_counters()
    disk_time_current = time.time()

    disk_time_interval = disk_time_current - disk_time_start
#    if disk_time_interval == 0:
#        return

    disk_read_diff = disk_io_current.read_bytes - disk_io_start.read_bytes
    disk_write_diff = disk_io_current.write_bytes - disk_io_start.write_bytes

    disk_read_speed = disk_read_diff / (1024 * 1024 * disk_time_interval) # MB/s
    disk_write_speed = disk_write_diff / (1024 * 1024 * disk_time_interval) # MB/s

    # Se toman estos valores nuevamente porque luego seran tomados nuevamente para hacer comparativas
    disk_io_start = disk_io_current
    disk_time_start = disk_time_current

    print(f"Disk used: {color}{BOLD}{percent:.0f}%{RESET} ({BOLD}{used:.2f}GB / {total:.2f}GB{RESET}) - Read: {BOLD}{disk_read_speed:.2f}MB/s{RESET} - Write: {BOLD}{disk_write_speed:.2f}MB/s{RESET}")
    
    if not ("bar" in omit or "b" in omit or "bard" in omit or "bd" in omit):
        barra_disk = barra_progreso(percent, color=color)
        print(barra_disk)

# Disk temperature: 32°C
def get_nvme_temperature():
    """Obtiene la temperatura del disco NVMe usando psutil y la imprime con colores según el nivel."""
    try:
        temps = psutil.sensors_temperatures()
        nvme_temps = temps.get("nvme")

        if not nvme_temps:
            print(f"Disk temperature: {RED}{BOLD}Unknown{RESET}")
            return

        # Buscar la entrada con etiqueta 'Composite' (por convención)
        composite_temp = next((t.current for t in nvme_temps if t.label == "Composite"), None)
        if composite_temp is None:
            print(f"Disk temperature: {RED}{BOLD}Unknown{RESET}")
            return

        # Aplicar colores según la temperatura
        if composite_temp >= 70:
            color = RED
        elif composite_temp >= 50:
            color = YELLOW
        else:
            color = RESET

        print(f"Disk temperature: {color}{BOLD}{composite_temp:.0f}°C{RESET}")

    except Exception as e:
        print(f"Disk temperature: {RED}{BOLD}Error: {str(e)}{RESET}")

# LAN IP: 192.168.0.123 - Speed: 100Mb/s (Full) - Down: 0.01MB/s - Up: 0.01MB/s
def get_lan_info():
    iface = lan_interface  # Interfaz de red cableada
    stats = psutil.net_if_stats().get(iface)
    addrs = psutil.net_if_addrs().get(iface)

#    # Verificar si la interfaz está activa
#    if not stats or not stats.isup:
#        return

    # Obtener IP
    ip_address = None
    if addrs:
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
                break
    if not ip_address:
        return

    # Obtener velocidad y modo dúplex
    speed = stats.speed
    duplex = stats.duplex
    duplex_str = "Full" if duplex == psutil.NIC_DUPLEX_FULL else "Half" if duplex == psutil.NIC_DUPLEX_HALF else "Unknown"

    # Medir tráfico de red usando variables globales
    global lan_io_start, lan_time_start
    lan_io_end = psutil.net_io_counters(pernic=True).get(iface)
    lan_time_end = time.time()

#    if not lan_io_start or not lan_io_end:
#        return

    lan_time_interval = lan_time_end - lan_time_start
#    if lan_time_interval == 0:
#        return

    lan_download = (lan_io_end.bytes_recv - lan_io_start.bytes_recv) / (1024 * 1024) / lan_time_interval
    lan_upload = (lan_io_end.bytes_sent - lan_io_start.bytes_sent) / (1024 * 1024) / lan_time_interval

    # Mostrar la salida formateada
    print(f"LAN IP: {BOLD}{ip_address}{RESET} - Speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET}) - Down: {BOLD}{lan_download:.2f}MB/s{RESET} - Up: {BOLD}{lan_upload:.2f}MB/s{RESET}")

    # Actualizar los valores para la próxima iteración
    lan_io_start = lan_io_end
    lan_time_start = lan_time_end

# WIFI lan: OBRIEN 5 - IP: 192.168.0.208
# WIFI signal: 71% - Speed: 325.0Mb/s - Down: 4.57MB/s - Up: 0.93MB/s
# ██████████████████████░░░░░░░░░░
# WIFI temperature: 42°C
def get_wifi_info():
    """Obtiene la información de la red WiFi y tráfico."""
    global wifi_interface, wifi_io_start, wifi_time_start
    try:
        # Obtener información de la red WiFi usando "iw dev (wifi_interfac) link"
        output = subprocess.run(["iw", "dev", wifi_interface, "link"], capture_output=True, text=True).stdout
        if "Not connected" in output or not re.search(r'SSID: (.+)', output):
            return  # No mostrar nada si el WIFI no está conectado

        # Extraer información relevante
        ssid_match = re.search(r'SSID: (.+)', output)
        signal_match = re.search(r'signal: (-?\d+) dBm', output)
        speed_match = re.search(r'(?:rx )?bitrate: ([\d\.]+) MBit/s', output)

        ssid = ssid_match.group(1).strip() if ssid_match else "Unknown"
        signal_dbm = int(signal_match.group(1)) if signal_match else -100
        speed = float(speed_match.group(1)) if speed_match else 0.0

        # Verificar si hay IP asignada
        ip_addrs = psutil.net_if_addrs().get(wifi_interface, [])
        ip = next((addr.address for addr in ip_addrs if addr.family == socket.AF_INET), "N/A")

        # Convertir dBm a porcentaje aproximado
        signal_percent = max(0, min(100, 2 * (signal_dbm + 100)))

        # Calcular tráfico de red
        io_current = psutil.net_io_counters(pernic=True).get(wifi_interface)
        time_current = time.time()
        interval = time_current - wifi_time_start

        bytes_recv_diff = io_current.bytes_recv - wifi_io_start.bytes_recv
        bytes_sent_diff = io_current.bytes_sent - wifi_io_start.bytes_sent
        download_speed = bytes_recv_diff / (1024 * 1024 * interval)
        upload_speed = bytes_sent_diff / (1024 * 1024 * interval)

        wifi_io_start = io_current
        wifi_time_start = time_current

        # Definir color de la señal WiFi
        if signal_percent < 40:
            color = RED
        elif signal_percent < 70:
            color = YELLOW
        else:
            color = RESET

        print(f"WiFi IP: {BOLD}{ip}{RESET} - SSID: {BOLD}{ssid}{RESET}")
        print(f"WiFi signal: {color}{BOLD}{signal_percent:.0f}%{RESET} - Speed: {BOLD}{speed:.1f}Mb/s{RESET} - Down: {BOLD}{download_speed:.2f}MB/s{RESET} - Up: {BOLD}{upload_speed:.2f}MB/s{RESET}")
        
        if not ("bar" in omit or "b" in omit or "barw" in omit or "bw" in omit):
            print(f"{barra_progreso(signal_percent, color=color)}")

        # Obtener temperatura de la placa WiFi desde psutil
        temps = psutil.sensors_temperatures()
        wifi_temp = None
        if 'iwlwifi_1' in temps:
            sensor = temps['iwlwifi_1'][0]
            wifi_temp = sensor.current

        if wifi_temp is not None:
            if wifi_temp > 70:
                temp_color = RED
            elif wifi_temp > 50:
                temp_color = YELLOW
            else:
                temp_color = RESET

            print(f"WiFi temperature: {temp_color}{BOLD}{wifi_temp:.0f}°C{RESET}")

    except Exception as e:
        print(f"{RED}Error inesperado: {e}{RESET}")

# Battery: 37% - Time: 0h 58m 52s - Mode: Discharging
# ███████████░░░░░░░░░░░░░░░░░░░░░
def get_battery_info():
    try:
        base_path = "/sys/class/power_supply/BAT0/"

        # Leer el estado de la batería
        with open(os.path.join(base_path, "status"), "r") as f:
            battery_mode = f.read().strip()

        if battery_mode == "Full":
            return  # No mostrar nada si está al 100%

        # Leer el porcentaje de batería
        with open(os.path.join(base_path, "capacity"), "r") as f:
            battery_percent = int(f.read().strip())

        # Definir color según el nivel
        if battery_percent > 25:
            color = RESET
        elif battery_percent > 10:
            color = YELLOW
        else:
            color = RED

        # Obtener tiempo restante (si está disponible)
        battery = psutil.sensors_battery()
        time_part = ""
        if battery and battery.secsleft not in (psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN):
            h, m = divmod(battery.secsleft // 60, 60)
            s = battery.secsleft % 60
            time_part = f" - Time: {BOLD}{h}h {m}m {s}s{RESET}"

        # Barra y salida
        print(f"Battery: {color}{BOLD}{battery_percent}%{RESET}{time_part} - Mode: {BOLD}{battery_mode}{RESET}")
        
        if not ("bar" in omit or "b" in omit or "bart" in omit or "bt" in omit):
            barra_battery = barra_progreso(battery_percent, color=color)
            print(barra_battery)

    except Exception as e:
        print(f"{RED}Battery error: {e}{RESET}")
        
# Run: 3 days, 4:52:51 (Esta funcion calcula el tiempo de ejecucion del script)
def format_uptime(seconds):
    """Convierte segundos en un formato legible estilo uptime."""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)

    if days > 0:
        return f"{days} day{'s' if days != 1 else ''}, {hours}:{minutes:02}:{secs:02}"
    else:
        return f"{hours:02}:{minutes:02}:{secs:02}"

def main():
    if not ("sys" in omit or "s" in omit):
        get_system_info()
    
    if not ("host" in omit or "o" in omit):
        get_host_user_info()
    
    if not ("up" in omit or "u" in omit):
        get_uptime_and_time()

    if not ("cpu" in omit or "c" in omit):
        get_cpu_usage()
        get_cpu_frequency()
        get_cpu_temperature()

    if not ("ram" in omit or "r" in omit):
        get_memory_usage()

    if not ("proc" in omit or "p" in omit):
        get_process_count()

    if not ("load" in omit or "l" in omit):
        get_load_average()

    if not ("disk" in omit or "d" in omit):
        get_disk_usage()
        get_nvme_temperature()

    if not ("lan" in omit or "n" in omit):
        get_lan_info()

    if not ("wifi" in omit or "w" in omit):
        get_wifi_info()

    if not ("bat" in omit or "a" in omit):
        get_battery_info()

#    print("\a")
#    subprocess.run(["beep"])

# Repetición automática
if __name__ == "__main__":
    if interval > 0:
        start_time = time.time()
        
        count = 1

        while True:
            # Medir tiempo de ejecución de main(), borra la pantalla y le da tormato al uptime
            exec_start = time.time()
            
            os.system('clear')
            
            main()
            
            # Tiempo total desde que arrancó el script
            elapsed = int(time.time() - start_time)
            uptime = format_uptime(elapsed)
            
            # Calcula el tiempo de ejecución de main()
            exec_duration = time.time() - exec_start

            for i in range(interval, 0, -1):
                # Run: 3 days, 4:52:51 (0.067s) / Cycles: 1313 / Next in 10/60 seconds...
                sys.stdout.write(f"\rRun: {uptime} ({exec_duration:.3f}s) / Cycles: {count} / Next in {i}/{interval} seconds... ")
                sys.stdout.flush()
                time.sleep(1)

            count += 1
    else:
        main()

