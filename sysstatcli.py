#!/usr/bin/env python3
# 
# SysStatCLI (System Status CLI) Version 2.44.20260315c
# 
# Autor: Axel O'BRIEN (LiGNUxMan) axelobrien@gmail.com y ChatGPT
# 
# axel@hal9001c:~$ python3 ~/Aplicaciones/sysstatcli.py
#
# 
# Nota: En Linux Mint 22.2 (y también en Ubuntu recientes) ya no se instala el comando iw por defecto. Instalar con; sudo apt install iw
# 
# 
# 🐧 OS: Linux Mint 22.2 - ⚙️ Kernel version: 6.14.0-37-generic
# 🏠 Hostname: hal9001c - 👤 User: axel
# ⏱️ Uptime: 1 day, 13:25:28 - 🕒 Time and date: 01:37:33 02/01/2026
# 🤖 CPU used: 22% (CPU0: 20% - CPU1: 22% - CPU2: 24% - CPU3: 21%)
#    ██████░░░░░░░░░░░░░░░░░░░░░░░░░░
# ⚡  CPU frequency: 1.10GHz - 🎚️  Scaling governor: powersave
#    ███████████░░░░░░░░░░░░░░░░░░░░░
# 🌡️ CPU temperature: 39°C
# 🧮 RAM used: 33% (5.10GB / 15.49GB) - 💾 Swap used: 0% (0.00GB / 0.00GB)
#    ██████████▒▒▒▒▒▒▒░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# 🧩 Processes: 265 (run=2, sleep=197, idle=65, stop=0, zombie=0, other=1)
# 📊 Load average: 1.11 1.70 1.83
# 🗄️ Disk used: 48% (225.80GB / 467.91GB) - Read: 0.00MB/s - Write: 0.26MB/s
#    ███████████████░░░░░░░░░░░░░░░░░
# 🌡️ Disk temperature: 33°C
# 📶 WiFi IP: 192.168.0.208 - SSID: OBRIEN 5
# 📡 WiFi signal: 66% - Speed: 195.0Mb/s - Down: 0.04MB/s - Up: 0.00MB/s
#    █████████████████████░░░░░░░░░░░
# 🌡️ WiFi temperature: 41°C
# 🔁 Run: 1 day, 13:24:20 (53ms) | Cycles: 564 | 16.31MB | Next: 10/60s 
# 
#

import argparse
import os
import psutil
import re
import termios
import tty
import select
import socket
import subprocess
import sys
import time
from datetime import timedelta  # Línea agregada para el uptime

# ==========================================================
# CONFIGURACIÓN DE HARDWARE / SISTEMA
# (BUSCAR Y MODIFICAR SOLO ACÁ SI CAMBIA EL HARDWARE)
# ==========================================================

# ─── OS ────────────────────────────────────────────────

# Kernel / sistema

OS_INFO_PATH = "/etc/os-release"
OS_RELEASE_PATH = "/proc/sys/kernel/osrelease"

# ─── CPU ───────────────────────────────────────────────

# Frecuencia CPU (sysfs)

# CPU_FREQ_MIN_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq"
# CPU_FREQ_MAX_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
# CPU_FREQ_CUR_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
# CPU_GOVERNOR_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"

CPU_FREQ_PATH = None
CPU_FREQ_MIN_PATH = None
CPU_FREQ_MAX_PATH = None
CPU_FREQ_CUR_PATH = None
CPU_GOVERNOR_PATH = None

# Interfaces de red
LAN_INTERFACE = "enxc025e92940b8"
WIFI_INTERFACE = "wlp3s0"

# Batería
BATTERY_NAME = None
BATTERY_PATH = None
UPOWER_BATTERY_PATH = None

# Sensores
CPU_TEMP_SENSOR = None
CPU_TEMP_INDEX = 0
NVME_TEMP_SENSOR = None
NVME_TEMP_LABEL = None
WIFI_TEMP_SENSOR = None

def detect_hardware():
    """Detecta dinámicamente las rutas de hardware y sensores de sistema al inicio."""
    global CPU_FREQ_PATH, CPU_FREQ_MIN_PATH, CPU_FREQ_MAX_PATH, CPU_FREQ_CUR_PATH, CPU_GOVERNOR_PATH
    global BATTERY_NAME, BATTERY_PATH, UPOWER_BATTERY_PATH
    global CPU_TEMP_SENSOR, CPU_TEMP_INDEX
    global NVME_TEMP_SENSOR, NVME_TEMP_LABEL
    global WIFI_TEMP_SENSOR

    # --- CPU ---
    CPU_SYS_PATH = "/sys/devices/system/cpu"
    if os.path.isdir(CPU_SYS_PATH):
        for cpu in os.listdir(CPU_SYS_PATH):
            if not cpu.startswith("cpu"):
                continue

            path = os.path.join(CPU_SYS_PATH, cpu, "cpufreq")
            if os.path.isdir(path):
                CPU_FREQ_PATH = path
                break

    if CPU_FREQ_PATH:
        CPU_FREQ_MIN_PATH = os.path.join(CPU_FREQ_PATH, "cpuinfo_min_freq")
        CPU_FREQ_MAX_PATH = os.path.join(CPU_FREQ_PATH, "cpuinfo_max_freq")
        CPU_FREQ_CUR_PATH = os.path.join(CPU_FREQ_PATH, "scaling_cur_freq")
        CPU_GOVERNOR_PATH = os.path.join(CPU_FREQ_PATH, "scaling_governor")

    # --- Batería ---
    POWER_SUPPLY_PATH = "/sys/class/power_supply"
    if os.path.isdir(POWER_SUPPLY_PATH):
        for dev in os.listdir(POWER_SUPPLY_PATH):
            dev_path = os.path.join(POWER_SUPPLY_PATH, dev)

            try:
                with open(os.path.join(dev_path, "type")) as f:
                    if f.read().strip() != "Battery":
                        continue

                with open(os.path.join(dev_path, "scope")) as f:
                    if f.read().strip() != "System":
                        continue

                BATTERY_NAME = dev
                BATTERY_PATH = dev_path
                UPOWER_BATTERY_PATH = f"/org/freedesktop/UPower/devices/battery_{dev}"
                break

            except FileNotFoundError:
                continue

    # --- Sensores Temperatura (psutil) ---
    temps = psutil.sensors_temperatures()

    for name in ("coretemp", "k10temp", "acpitz"):
        if name in temps:
            CPU_TEMP_SENSOR = name
            break

    if "nvme" in temps:
        for entry in temps["nvme"]:
            if entry.current is not None:
                NVME_TEMP_SENSOR = "nvme"
                NVME_TEMP_LABEL = entry.label
                break

    for name in temps:
        if "iwlwifi" in name:
            WIFI_TEMP_SENSOR = name
            break

# =====================================================================
# Colores y estilos ANSI
# =====================================================================
RESET      = "\033[0m"
BOLD       = "\033[1m"
DIM        = "\033[2m"

if os.environ.get("TERM", "") in ("linux", "dumb"):
    ITALIC = "\033[2m"  # En terminales simples, usamos DIM como alternativa
else:
    ITALIC = "\033[3m"

UNDERLINE  = "\033[4m"
# GREEN = "\033[32m"
GREEN      = "\033[92m"
# ORANGE = "\033[38;5;202m" # Naranja rojizo
ORANGE     = "\033[38;5;208m"  # Naranja fuerte
# ORANGE = "\033[38;5;214m" # Naranja más claro
# YELLOW = "\033[33m"
YELLOW     = "\033[93m"
# RED = "\033[31m"
RED        = "\033[91m"
LIGHT_GRAY = "\033[37m"

# =====================================================================
# Procesar argumentos (argparse)
# =====================================================================
def parse_arguments():
    """Configura y devuelve los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        usage=argparse.SUPPRESS,
        description=f"{BOLD}SysStatCLI{RESET} (System Status CLI) - Version 2.44.20260315b\n\n"
                    f"{BOLD}Repositorio:{RESET} {UNDERLINE}https://github.com/LiGNUxMan/SysStatCLI{RESET}\n\n"
                    f"{BOLD}Autor:{RESET} Axel O'BRIEN ({ITALIC}LiGNUxMan{RESET}) · {UNDERLINE}axelobrien@gmail.com{RESET}\n"
                    f"{BOLD}Colaboradores:{RESET} ChatGPT · OpenAI / Google Antigravity\n\n"
                    f"{BOLD}Uso:{RESET} python3 sysstatcli_2.44.0b.py [tiempo] [opciones]\n"
                    f"     Durante la ejecución, puede presionar {BOLD}Q{RESET} o {BOLD}X{RESET} para salir.\n\n"
                    f"{BOLD}Tiempo:{RESET} Intervalo en segundos para repetir el script",
        epilog=f"{BOLD}Consejo:{RESET} Use -b -i para ocultar las barras de progreso e iconos\n"
               f"         (útil en terminales antiguas o sin soporte Unicode).\n\n"
               f"{BOLD}Ejemplos:{RESET}\n"
               f"python3 sysstatcli_2.44.0b.py            → Ejecuta una sola vez\n"
               f"python3 sysstatcli_2.44.0b.py 60         → Ejecuta cada 60 segundos\n"
               f"python3 sysstatcli_2.44.0b.py -r -w      → Ejecuta una sola vez, omitiendo RAM y WiFi\n"
               f"python3 sysstatcli_2.44.0b.py -s -b 10   → Ejecuta cada 10s, omit. datos del sist. y barras\n\n"
               f"python3 sysstatcli_2.44.0b.py -s -o -u -p -l -a -t 60\n"
               f"🤖 CPU used: 2% (CPU0: 1% - CPU1: 4% - CPU2: 1% - CPU3: 2%)\n"
               f"   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n"
               f"⚡ CPU frequency: {YELLOW}0.90GHz{RESET} - 🎚️  Scaling governor: powersave\n"
               f"   {YELLOW}█████████░░░░░░░░░░░░░░░░░░░░░░░{RESET}\n"
               f"🌡️  CPU temperature: 35°C\n"
               f"🧮 RAM used: 53% (8.16GB / 15.49GB) - 💾 Swap used: 0% (0.00GB / 0.00GB)\n"
               f"   ████████████████▒▒▒▒▒▒▒▒▒▒░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n"
               f"🗄️  Disk used: 49% (229.43GB / 467.91GB) - Read: 0.00MB/s - Write: 0.00MB/s\n"
               f"   ███████████████░░░░░░░░░░░░░░░░░\n"
               f"🌡️  Disk temperature: 32°C\n"
               f"📶 WiFi IP: 192.168.0.208 - SSID: OBRIEN 5\n"
               f"📡 WiFi signal: {YELLOW}58%{RESET} - Speed: 234.0Mb/s - Down: 0.00MB/s - Up: 0.00MB/s\n"
               f"   {YELLOW}██████████████████░░░░░░░░░░░░░░{RESET}\n"
               f"🌡️  WiFi temperature: 40°C\n"
               f"🔁 {DIM}Run: 1 day, 13:24:20 (53ms) | Cycles: 564 | 16.31MB | Next: 10/60s {RESET}",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )

    parser._optionals.title = f"{BOLD}Opciones:{RESET} (Argumentos disponibles para omitir secciones)"

    parser.add_argument("-h", "--help", "-help", action="help", default=argparse.SUPPRESS, help="Muestra este mensaje de ayuda y sale")
    parser.add_argument("interval", nargs="?", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("-s", "-sys", action="store_true", dest="sys",  help="Omitir nombre del sistema operativo y versión del kernel")
    parser.add_argument("-o", "-host", action="store_true", dest="host", help="Omitir nombre de la computadora y usuario")
    parser.add_argument("-u", "-up", action="store_true", dest="up",   help="Omitir tiempo de actividad, hora y fecha")
    parser.add_argument("-c", "-cpu", action="store_true", dest="cpu",  help="Omitir uso, frecuencia, modo y temperatura del CPU")
    parser.add_argument("-r", "-ram", action="store_true", dest="ram",  help="Omitir uso de memoria RAM y SWAP")
    parser.add_argument("-p", "-proc", action="store_true", dest="proc", help="Omitir procesos y sus estados")
    parser.add_argument("-l", "-load", action="store_true", dest="load", help="Omitir carga del sistema (Load average)")
    parser.add_argument("-d", "-disk", action="store_true", dest="disk", help="Omitir uso y temperatura del disco")
    parser.add_argument("-a", "-lan", action="store_true", dest="lan",  help="Omitir red cableada (LAN)")
    parser.add_argument("-w", "-wifi", action="store_true", dest="wifi", help="Omitir red WiFi y temperatura")
    parser.add_argument("-t", "-bat", action="store_true", dest="bat",  help="Omitir batería")
    parser.add_argument("-b", "-bar", action="store_true", dest="bar",  help="Omitir todas las barras de progreso")
    parser.add_argument("-bc", "-barc", action="store_true", dest="barc", help="Omitir la barra de uso de CPU")
    parser.add_argument("-bf", "-barf", action="store_true", dest="barf", help="Omitir la barra de frecuencia del CPU")
    parser.add_argument("-br", "-barr", action="store_true", dest="barr", help="Omitir la barra de uso de RAM")
    parser.add_argument("-bd", "-bard", action="store_true", dest="bard", help="Omitir la barra de uso de Disco")
    parser.add_argument("-bw", "-barw", action="store_true", dest="barw", help="Omitir la barra de señal WiFi")
    parser.add_argument("-bt", "-bart", action="store_true", dest="bart", help="Omitir la barra de Batería")
    parser.add_argument("-i", "-icon", action="store_true", dest="icon", help="Oculta los íconos decorativos")

    return parser.parse_args()

# Parsea los argumentos al instante al cargar el módulo para tener las globals disponibles.
args = parse_arguments()
interval = args.interval

# Variables para guardar estado previo de métricas (se inician en init_metrics)
cpu_times_start = None
cpu_time_start = None
disk_io_start = None
disk_time_start = None
lan_io_start = None
lan_time_start = None
wifi_io_start = None
wifi_time_start = None

def init_metrics():
    """Inicializa contadores globales basados en args."""
    global cpu_times_start, cpu_time_start
    global disk_io_start, disk_time_start
    global lan_io_start, lan_time_start
    global wifi_io_start, wifi_time_start

    if not args.cpu:
        cpu_times_start = psutil.cpu_times(percpu=True)
        cpu_time_start = time.time()

    if not args.disk:
        disk_io_start = psutil.disk_io_counters()
        disk_time_start = time.time()

    if not args.lan:
        lan_stats = psutil.net_io_counters(pernic=True)
        if LAN_INTERFACE in lan_stats:
            lan_io_start = lan_stats[LAN_INTERFACE]
        else:
            lan_io_start = None
        lan_time_start = time.time()

    if not args.wifi:
        wifi_io_start = psutil.net_io_counters(pernic=True).get(WIFI_INTERFACE)
        wifi_time_start = time.time()

# -------------------------------------------------------------
# Funciones Terminal y GUI
# -------------------------------------------------------------

# =====================================================================
# Función para detectar soporte Unicode en la terminal
# =====================================================================
def terminal_supports_unicode() -> bool:
    """
    Devuelve True si la terminal soporta Unicode.
    Si el usuario pasó -i / -icon, se salta completamente.
    """

    # --- RESPETAR EXPLICITAMENTE -i / -icon ---
    if args.icon:
        return False

    term = os.environ.get("TERM", "").lower()
    encoding = (sys.stdout.encoding or "").lower()

    # Terminales que casi nunca soportan Unicode
    if any(x in term for x in ["linux", "vt100", "xterm-color", "dumb", "ansi"]):
        return False

    # Codificaciones que no son UTF
    if not encoding.startswith("utf"):
        return False

    # Intentar una prueba real de escritura
    try:
        sys.stdout.write("🔁")
        sys.stdout.flush()
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
        return True
    except Exception:
        return False

# =====================================================================
# Detección automática de soporte Unicode
# =====================================================================
if not args.icon and not terminal_supports_unicode():
    # Si la terminal no soporta Unicode, actuamos como si el usuario hubiera pasado -i
    args.icon = True

# Función centralizada para imprimir con o sin iconos
def print_info(icono, texto_con_icono, texto_sin_icono=None):
    """
    Imprime un texto con o sin icono dependiendo de los argumentos del usuario.
    Si no se proporciona texto_sin_icono, se usa el texto_con_icono sin el prefijo del icono.
    """
    if texto_sin_icono is None:
        texto_sin_icono = texto_con_icono
        
    if not args.icon:
        print(f"{icono} {texto_con_icono}")
    else:
        print(f"{texto_sin_icono}")

def print_barra(texto_barra):
    """
    Imprime una barra de progreso. Si los íconos están activados, agrega 
    un margen izquierdo para alinearla con el texto superior.
    """
    if not args.icon:
        print("   " + texto_barra)
    else:
        print(texto_barra)

# Función para generar barra de progreso
def barra_progreso(valor, total=100, ancho=32, color=RESET):
    bloques_llenos = int((valor / total) * ancho)
    barra = "█" * bloques_llenos + "░" * (ancho - bloques_llenos) # barra = "█" * bloques_llenos + " " * (ancho - bloques_llenos) ▁▂▃▄▅▆▇█ ░▒▓█
    return f"{color}{barra}{RESET}" # return f"{color}[{barra}]{RESET}" # return f"{color}▕{barra}▏{RESET}" # return f"{color}[{barra}]{RESET}"

# 🐧 OS: Linux Mint 22.1 - ⚙️  Kernel version: 6.11.0-19-generic
def get_system_info():
    """Obtiene el nombre del sistema operativo y la versión del kernel."""
    try:
        with open(OS_INFO_PATH) as f:
            os_name = None
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    os_name = line.strip().split("=")[1].strip('"')
                    break
    except FileNotFoundError:
        os_name = f"{RED}Unknown{RESET}"

    try:
        with open(OS_RELEASE_PATH) as f:
            kernel_version = f.read().strip()
    except FileNotFoundError:
        kernel_version = f"{RED}Unknown{RESET}"

    if not args.icon:
        print(f"🐧 OS: {BOLD}{os_name}{RESET} - ⚙️  Kernel version: {BOLD}{kernel_version}{RESET}")
    else:
        print(f"OS: {BOLD}{os_name}{RESET} - Kernel version: {BOLD}{kernel_version}{RESET}")

# 🏠 Hostname: hal9001c - User: axel
def get_host_user_info():
    hostname = socket.gethostname()
    username = os.getlogin()

    print_info("🏠", f"Hostname: {BOLD}{hostname}{RESET} - 👤 User: {BOLD}{username}{RESET}",
                     f"Hostname: {BOLD}{hostname}{RESET} - User: {BOLD}{username}{RESET}")

# ⏱️ Uptime: 1 day, 3:37:09 - 🕒 Time and date: 15:14:25 13/03/2025
def get_uptime_and_time():
    """Obtiene el uptime desde /proc/uptime, hora y fecha y los imprime."""
    uptime_seconds = time.time() - psutil.boot_time() # Linea agregada para el uptime de mem_info3_root
    uptime_str = str(timedelta(seconds=int(uptime_seconds))) # Linea agregada para el uptime de mem_info3_root
    current_time = time.strftime("%H:%M:%S %d/%m/%Y")

    print_info("⏱️ ", f"Uptime: {BOLD}{uptime_str}{RESET} - 🕒 Time and date: {BOLD}{current_time}{RESET}",
                      f"Uptime: {BOLD}{uptime_str}{RESET} - Time and date: {BOLD}{current_time}{RESET}")

# 🤖 CPU used: 39% (CPU0: 38% - CPU1: 36% - CPU2: 41% - CPU3: 40%)
#    ████████████░░░░░░░░░░░░░░░░░░░░
def get_cpu_usage():
    global cpu_times_start, cpu_time_start

    cpu_times_current = psutil.cpu_times(percpu=True)
    cpu_time_current = time.time()

    cpu_time_interval = cpu_time_current - cpu_time_start
#    if cpu_time_interval == 0:
#        return
  
    def get_colored_usage(usage):
        if usage <= 33:  # cambiamos de <33 a <=33
            color = RESET
        elif usage <= 66:
            color = YELLOW
        elif usage <= 99:
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

    print_info("🤖", f"CPU used: {uso_promedio_str} ({uso_nucleos_str})",
                     f"CPU used: {uso_promedio_str} ({uso_nucleos_str})")
    
    if not args.bar and not args.barc:
        print_barra(barra_progreso(promedio_uso, color=color_barra))

    # Actualizar para la siguiente lectura
    cpu_times_start = cpu_times_current
    cpu_time_start = cpu_time_current
 
# ⚡ CPU frequency: 1.10GHz - 🎚️  Scaling governor: powersave
#   ███████████░░░░░░░░░░░░░░░░░░░░░
def get_cpu_frequency():
    """Obtiene la frecuencia del CPU y el scaling_governor y los imprime con colores."""
    try:
        with open(CPU_FREQ_MIN_PATH) as f:
            min_freq = int(f.read().strip()) / 1_000_000
        with open(CPU_FREQ_MAX_PATH) as f:
            max_freq = int(f.read().strip()) / 1_000_000
        with open(CPU_FREQ_CUR_PATH) as f:
            cur_freq = int(f.read().strip()) / 1_000_000
        with open(CPU_GOVERNOR_PATH) as f:
            scaling_governor = f.read().strip()

        cur_freq = round(cur_freq, 2)

        color = RESET
        if cur_freq >= max_freq:
            color = RED
        elif cur_freq > 2.5:
            color = ORANGE
        elif cur_freq > 0.8:
            color = YELLOW

        print_info("⚡", f"CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - 🎚️  Scaling governor: {BOLD}{scaling_governor}{RESET}",
                         f"CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - Scaling governor: {BOLD}{scaling_governor}{RESET}")

        percent = (cur_freq / max_freq) * 100

        if not args.bar and not args.barf:
            print_barra(barra_progreso(percent, color=color))

    except FileNotFoundError:
        print_info("⚡", f"CPU frequency: {RED}{BOLD}Unknown{RESET} - 🎚️  Scaling governor: {RED}{BOLD}Unknown{RESET}",
                         f"CPU frequency: {RED}{BOLD}Unknown{RESET} - Scaling governor: {RED}{BOLD}Unknown{RESET}")

# 🌡️ CPU temperature: 39°C
def get_cpu_temperature():
    """Obtiene la temperatura del CPU usando psutil"""
    try:
        temps = psutil.sensors_temperatures()
        temp = temps[CPU_TEMP_SENSOR][CPU_TEMP_INDEX].current
    
        color = RESET
        if temp > 60:
            color = RED
        elif temp > 40:
            color = ORANGE
        elif temp > 35:
            color = YELLOW

        print_info("🌡️ ", f"CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}",
                          f"CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")

    except Exception:
        print_info("🌡️ ", f"CPU temperature: {RED}{BOLD}Unknown{RESET}",
                          f"CPU temperature: {RED}{BOLD}Unknown{RESET}")

# 🧮 RAM used: 39% (6.01GB / 15.49GB) - 💾 Swap used: 0% (0.00GB / 0.00GB)
#    ████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
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

    print_info("🧮", f"RAM used: {BOLD}{mem_colored}{RESET} ({BOLD}{mem_used:.2f}GB / {mem_total:.2f}GB{RESET}) - 💾 Swap used: {BOLD}{swap_colored}{RESET} ({BOLD}{swap_used:.2f}GB / {swap_total:.2f}GB{RESET})",
                     f"RAM used: {BOLD}{mem_colored}{RESET} ({BOLD}{mem_used:.2f}GB / {mem_total:.2f}GB{RESET}) - Swap used: {BOLD}{swap_colored}{RESET} ({BOLD}{swap_used:.2f}GB / {swap_total:.2f}GB{RESET})")

    # Barra personalizada para RAM
    if not args.bar and not args.barr:
        def barra_memoria(apps_ratio, sys_ratio, free_ratio, ancho=32):
            apps_blocks = int(ancho * apps_ratio)
            free_blocks = int(ancho * free_ratio)
            sys_blocks = ancho - apps_blocks - free_blocks
            
            # ▁▂▃▄▅▆▇█ ░▒▓█
            barra = (
                f"{mem_color}{'█' * apps_blocks}" +
                f"{'▒' * sys_blocks}" +
                f"{'░' * free_blocks}{RESET}"
            )
            return barra

        barra_ram = barra_memoria(apps_ratio, sys_ratio, free_ratio)
        barra_swap = barra_progreso(swap_percent, color=swap_color)
        print_barra(f"{barra_ram} - {barra_swap}")

# 🧩 Processes: 265 (running=1, sleeping=199, idle=65, stopped=0, zombie=0, other=0)
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

        info_str = f"Processes: {BOLD}{total_processes}{RESET} ({ITALIC}run{RESET}={BOLD}{process_states['running']}{RESET}, {ITALIC}sleep{RESET}={BOLD}{process_states['sleeping']}{RESET}, {ITALIC}idle{RESET}={BOLD}{process_states['idle']}{RESET}, {ITALIC}stop{RESET}={BOLD}{process_states['stopped']}{RESET}, {ITALIC}zombie{RESET}={BOLD}{process_states['zombie']}{RESET}, {ITALIC}other{RESET}={BOLD}{process_states['other']}{RESET})"
        print_info("🧩", info_str, info_str)
        
    except Exception as e:
        print_info("🧩", f"Processes: {RED}{BOLD}Unknown{RESET}",
                         f"Processes: {RED}{BOLD}Unknown{RESET}")

# 📊 Load average: 1.97 1.22 0.98
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
    
    print_info("📊", f"Load average: {BOLD}{load1_str}{RESET} {BOLD}{load5_str}{RESET} {BOLD}{load15_str}{RESET}",
                     f"Load average: {BOLD}{load1_str}{RESET} {BOLD}{load5_str}{RESET} {BOLD}{load15_str}{RESET}")

# 🗄️ Disk used: 43% (202.91GB / 467.91GB) - Read: 8.63MB/s - Write: 0.72MB/s
#    █████████████░░░░░░░░░░░░░░░░░░░
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

    print_info("🗄️ ", f"Disk used: {color}{BOLD}{percent:.0f}%{RESET} ({BOLD}{used:.2f}GB / {total:.2f}GB{RESET}) - Read: {BOLD}{disk_read_speed:.2f}MB/s{RESET} - Write: {BOLD}{disk_write_speed:.2f}MB/s{RESET}",
                      f"Disk used: {color}{BOLD}{percent:.0f}%{RESET} ({BOLD}{used:.2f}GB / {total:.2f}GB{RESET}) - Read: {BOLD}{disk_read_speed:.2f}MB/s{RESET} - Write: {BOLD}{disk_write_speed:.2f}MB/s{RESET}")
    
    if not args.bar and not args.bard:
        print_barra(barra_progreso(percent, color=color))

# 🌡️ Disk temperature: 32°C
def get_nvme_temperature():
    """Obtiene la temperatura del disco NVMe usando psutil y la imprime con colores según el nivel."""
    try:
        temps = psutil.sensors_temperatures()
        nvme_temps = temps.get(NVME_TEMP_SENSOR)

        if not nvme_temps:
            print(f"Disk temperature: {RED}{BOLD}Unknown{RESET}")
            return

        # Buscar la entrada con etiqueta 'Composite' (por convención)
        composite_temp = next((t.current for t in nvme_temps if t.label == NVME_TEMP_LABEL),None)


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

        print_info("🌡️ ", f"Disk temperature: {color}{BOLD}{composite_temp:.0f}°C{RESET}",
                          f"Disk temperature: {color}{BOLD}{composite_temp:.0f}°C{RESET}")

    except Exception as e:
        print_info("🌡️ ", f"Disk temperature: {RED}{BOLD}Unknown{RESET}",
                          f"Disk temperature: {RED}{BOLD}Unknown{RESET}")

# 🌐 LAN IP: 192.168.0.123 - Speed: 100Mb/s (Full) - Down: 0.01MB/s - Up: 0.01MB/s
def get_lan_info():
    global lan_io_start, lan_time_start

    iface = LAN_INTERFACE

    addrs = psutil.net_if_addrs().get(iface)
    if not addrs:
        return

    # Verificar que tenga IP asignada
    ip_address = next((addr.address for addr in addrs if addr.family == socket.AF_INET), None)
    if not ip_address:
        return

    stats = psutil.net_if_stats().get(iface)
    if not stats or not stats.isup:
        return

    # Obtener velocidad y modo dúplex
    speed = stats.speed
    duplex = stats.duplex
    duplex_str = "Full" if duplex == psutil.NIC_DUPLEX_FULL else "Half" if duplex == psutil.NIC_DUPLEX_HALF else "Unknown"

    # Obtener datos actuales de red
    lan_io_end = psutil.net_io_counters(pernic=True).get(iface)
    lan_time_end = time.time()

    # Si no hay datos previos, solo mostrar IP y velocidad
    if lan_io_end is None or lan_io_start is None or lan_time_start is None:
        print(f"LAN IP: {BOLD}{ip_address}{RESET} - Speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET})")
        lan_io_start = lan_io_end
        lan_time_start = lan_time_end
        return

    # Calcular tráfico
    lan_time_interval = lan_time_end - lan_time_start
    if lan_time_interval == 0:
        return

    lan_download = (lan_io_end.bytes_recv - lan_io_start.bytes_recv) / (1024 * 1024) / lan_time_interval
    lan_upload = (lan_io_end.bytes_sent - lan_io_start.bytes_sent) / (1024 * 1024) / lan_time_interval

    print_info("🌐", f"LAN IP: {BOLD}{ip_address}{RESET} - Speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET}) - Down: {BOLD}{lan_download:.2f}MB/s{RESET} - Up: {BOLD}{lan_upload:.2f}MB/s{RESET}",
                     f"LAN IP: {BOLD}{ip_address}{RESET} - Speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET}) - Down: {BOLD}{lan_download:.2f}MB/s{RESET} - Up: {BOLD}{lan_upload:.2f}MB/s{RESET}")

    # Guardar valores para próxima llamada
    lan_io_start = lan_io_end
    lan_time_start = lan_time_end

# 📶 WIFI lan: OBRIEN 5 - IP: 192.168.0.208
# 📡 WIFI signal: 71% - Speed: 325.0Mb/s - Down: 4.57MB/s - Up: 0.93MB/s
# ██████████████████████░░░░░░░░░░
# 🌡️ WIFI temperature: 42°C
def get_wifi_info():
    """Obtiene la información de la red WiFi y tráfico."""
    global wifi_io_start, wifi_time_start

    iface = WIFI_INTERFACE

    try:
        # Obtener información de la red WiFi usando "iw dev (wifi_interfac) link"
        output = subprocess.run(["iw", "dev", iface, "link"], capture_output=True, text=True).stdout
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
        ip_addrs = psutil.net_if_addrs().get(iface, [])
        ip = next((addr.address for addr in ip_addrs if addr.family == socket.AF_INET), "N/A")

        # Convertir dBm a porcentaje aproximado
        signal_percent = max(0, min(100, 2 * (signal_dbm + 100)))

        # Calcular tráfico de red
        io_current = psutil.net_io_counters(pernic=True).get(iface)
        time_current = time.time()
        interval = time_current - wifi_time_start

        bytes_recv_diff = io_current.bytes_recv - wifi_io_start.bytes_recv
        bytes_sent_diff = io_current.bytes_sent - wifi_io_start.bytes_sent
        download_speed = bytes_recv_diff / (1024 * 1024 * interval)
        upload_speed = bytes_sent_diff / (1024 * 1024 * interval)

        wifi_io_start = io_current
        wifi_time_start = time_current

        # Definir color de la señal WiFi
        if signal_percent < 25:
            color = RED
        elif signal_percent < 50:
            color = ORANGE
        elif signal_percent < 75:
            color = YELLOW
        else:
            color = RESET

        print_info("📶", f"WiFi IP: {BOLD}{ip}{RESET} - SSID: {BOLD}{ssid}{RESET}",
                         f"WiFi IP: {BOLD}{ip}{RESET} - SSID: {BOLD}{ssid}{RESET}")
        print_info("📡", f"WiFi signal: {color}{BOLD}{signal_percent:.0f}%{RESET} - Speed: {BOLD}{speed:.1f}Mb/s{RESET} - Down: {BOLD}{download_speed:.2f}MB/s{RESET} - Up: {BOLD}{upload_speed:.2f}MB/s{RESET}",
                         f"WiFi signal: {color}{BOLD}{signal_percent:.0f}%{RESET} - Speed: {BOLD}{speed:.1f}Mb/s{RESET} - Down: {BOLD}{download_speed:.2f}MB/s{RESET} - Up: {BOLD}{upload_speed:.2f}MB/s{RESET}")
        
        if not args.bar and not args.barw:
            print_barra(barra_progreso(signal_percent, color=color))

        # Obtener temperatura de la placa WiFi desde psutil
        temps = psutil.sensors_temperatures()
        wifi_temp = None

        if WIFI_TEMP_SENSOR in temps:
            sensor = temps[WIFI_TEMP_SENSOR][0]
            wifi_temp = sensor.current

        if wifi_temp is not None:
            if wifi_temp > 70:
                temp_color = RED
            elif wifi_temp > 50:
                temp_color = YELLOW
            else:
                temp_color = RESET

            print_info("🌡️ ", f"WiFi temperature: {temp_color}{BOLD}{wifi_temp:.0f}°C{RESET}",
                              f"WiFi temperature: {temp_color}{BOLD}{wifi_temp:.0f}°C{RESET}")

    except Exception as e:
        print(f"{RED}Error inesperado: {e}{RESET}")

# 🔋 Battery: 37% - Time: 0h 58m 52s - Mode: Discharging
# ███████████░░░░░░░░░░░░░░░░░░░░░
def get_battery_info():

    # print("DEBUG BATTERY_PATH =", BATTERY_PATH)

    # No hay batería física
    if not BATTERY_PATH or not os.path.isdir(BATTERY_PATH):
        # print("DEBUG: saliendo porque no hay batería")
        return

    try:
        base_path = BATTERY_PATH
        
        # Leer el estado de la batería
        with open(os.path.join(base_path, "status"), "r") as f:
            battery_mode = f.read().strip()

        # if battery_mode == "Full":
        #     return  # No mostrar nada si está al 100%
        if battery_mode not in ("Charging", "Discharging"):
            return  # No mostrar nada si no está cargando o descargando

        # Leer el porcentaje de batería
        with open(os.path.join(base_path, "capacity"), "r") as f:
            battery_percent = int(f.read().strip())

        # Definir color según el nivel
        if battery_percent > 50:
            color = RESET
        elif battery_percent > 25:
            color = YELLOW
        elif battery_percent > 10:
            color = ORANGE
        else:
            color = RED

        # Obtener tiempo restante con psutil o fallback con upower
        battery = psutil.sensors_battery()
        time_part = ""
        if battery and battery.secsleft not in (
            psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN, -2, -1
        ):
            h, m = divmod(battery.secsleft // 60, 60)
            #s = battery.secsleft % 60
            #time_part = f" - Time: {BOLD}{h}h {m}m {s}s{RESET}"
            #s = battery.secsleft % 60
            time_part = f" - Time: {BOLD}{h}h {m}m{RESET}"
        else:
            try:
                output = subprocess.check_output(
                    ["upower", "-i", UPOWER_BATTERY_PATH],
                    text=True
                )
                for line in output.splitlines():
                    if "time to full" in line or "time to empty" in line:
                        tiempo = line.split(":")[1].strip()
                        if "hour" in tiempo or "minute" in tiempo:
                            # Unificar formato "17,3 minutes" a algo más natural
                            tiempo = tiempo.replace(",", ".")
                            if "minute" in tiempo:
                                mins = float(tiempo.split()[0])
                                h = int(mins // 60)
                                m = int(mins % 60)
                                time_part = f" - Time: {BOLD}{h}h {m}m{RESET}"
                            elif "hour" in tiempo:
                                h = float(tiempo.split()[0])
                                h_int = int(h)
                                m = int((h - h_int) * 60)
                                time_part = f" - Time: {BOLD}{h_int}h {m}m{RESET}"
                        else:
                            time_part = f" - Time: {BOLD}{tiempo}{RESET}"
                        break
            except Exception:
                pass

        # Mostrar datos de batería
        print_info("🔋", f"Battery: {color}{BOLD}{battery_percent}%{RESET}{time_part} - Mode: {BOLD}{battery_mode}{RESET}",
                         f"Battery: {color}{BOLD}{battery_percent}%{RESET}{time_part} - Mode: {BOLD}{battery_mode}{RESET}")

        if not args.bar and not args.bart:
            print_barra(barra_progreso(battery_percent, color=color))

    except FileNotFoundError:
        # Batería no presente / removida
        return
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

### Funciones para detectar las teclas Q y X para salir
def get_keypress(timeout=1):
    dr, _, _ = select.select([sys.stdin], [], [], timeout)
    if dr:
        # Leer hasta 3 bytes (suficiente para teclas especiales como F1–F4)
        raw = os.read(sys.stdin.fileno(), 3).decode(errors='ignore')
        # Si es una sola letra simple, devolverla
        return raw if len(raw) == 1 else None
    return None

def enable_raw_mode():
    """Activa modo sin buffer para leer teclas sin Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old_settings

def disable_raw_mode(old_settings):
    """Restaura la configuración del terminal."""
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if not args.bat:
        get_battery_info()

def print_all_stats():
    """Imprime todas las estadísticas requeridas (reemplaza al viejo main)."""
    if not args.sys:
        get_system_info()
    
    if not args.host:
        get_host_user_info()
    
    if not args.up:
        get_uptime_and_time()

    if not args.cpu:
        get_cpu_usage()
        get_cpu_frequency()
        get_cpu_temperature()
    
    if not args.ram:
        get_memory_usage()

    if not args.proc:
        get_process_count()

    if not args.load:
        get_load_average()

    if not args.disk:
        get_disk_usage()
        get_nvme_temperature()

    if not args.lan:
        get_lan_info()

    if not args.wifi:
        get_wifi_info()

    if not args.bat:
        get_battery_info()

def main():
    global args, interval
    detect_hardware()

    # Chequeo dinámico para forzar variables o ajustes visuales dependientes de arg
    if not args.icon and not terminal_supports_unicode():
        args.icon = True

    init_metrics()
    time.sleep(1)  # Pausa de 1 seg para mejorar exactitud en la primera ejecución o única

    if interval > 0:
        start_time = time.time()
        count = 1
        old_settings = enable_raw_mode()

        try:
            while True:
                exec_start = time.time()
                os.system('clear')

                print_all_stats()

                elapsed = int(time.time() - start_time)
                uptime = format_uptime(elapsed)
                exec_duration = (time.time() - exec_start) * 1000

                proceso = psutil.Process(os.getpid())
                mem_proc_mb = proceso.memory_info().rss / 1024 / 1024

                for i in range(interval, 0, -1):
                    icono = "🔁 " if not args.icon else ""
                    texto_base = f"{DIM}Run: {uptime} ({exec_duration:.0f}ms) | Cycles: {count} | {mem_proc_mb:.2f}MB | Next: {i}/{interval}s {RESET}"
                    
                    sys.stdout.write(f"\r{icono}{texto_base}")
                    sys.stdout.flush()

                    tick_start = time.time()
                    while True:
                        key = get_keypress(timeout=0.1)
                        if key and key.lower() in ['q', 'x']:
                            print("")
                            raise SystemExit
                        if time.time() - tick_start >= 1:
                            break

                count += 1
        finally:
            disable_raw_mode(old_settings)
    else:
        print_all_stats()

if __name__ == "__main__":
    main()

