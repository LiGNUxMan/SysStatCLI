#!/usr/bin/env python3
# 
# SysStatCLI (System Status CLI) Version 2.43.20251108a
# 
# Autor: Axel O'BRIEN (LiGNUxMan) axelobrien@gmail.com y ChatGPT
# 
# axel@hal9001c:~$ python3 ~/Aplicaciones/sysstatcli.py
#
# 
# Nota: En Linux Mint 22.2 (y también en Ubuntu recientes) ya no se instala el comando iw por defecto. Instalar con; sudo apt install iw
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
# Run: 3 days, 4:52:51 (67ms) | Cycles: 1313 | 15.48MB | Next: 10/60s...
# 
#

import datetime
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
# Función para detectar soporte Unicode en la terminal
# =====================================================================
def terminal_supports_unicode() -> bool:
    """
    Devuelve True si la terminal soporta Unicode.
    Si no, fuerza el modo sin íconos (-i).
    """
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
        # Borrar el símbolo impreso
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
        return True
    except Exception:
        return False

# =====================================================================
# Procesar argumentos
# =====================================================================
omit = set(arg[1:].lower() for arg in sys.argv[1:] if arg.startswith("-"))

# Buscar si hay un número entre los argumentos (intervalo en segundos)
interval = 0
for arg in sys.argv[1:]:
    if arg.isdigit():
        interval = int(arg)
        break  # Solo tomamos el primer número encontrado

# Argumentos válidos
valid_args = {
    "sys", "s", "host", "o", "up", "u", "cpu", "c", "ram", "r",
    "proc", "p", "load", "l", "disk", "d", "lan", "a", "wifi", "w",
    "bat", "t", "help", "h",
    "bar", "b", "barc", "bc", "barr", "br", "bard", "bd",
    "barw", "bw", "bart", "bt",
    "i", "icon"
}

# Detectar argumentos inválidos
for arg in sys.argv[1:]:
    if arg.isdigit():
        continue
    if arg.startswith("-") and arg[1:].lower() not in valid_args:
        print(f"\nArgumento no válido: {BOLD}{arg}{RESET}")
        print("Usá -h, -help o --help para ver las opciones disponibles.\n")
        sys.exit(1)
    if not arg.startswith("-") and not arg.isdigit():
        print(f"\nArgumento no válido: {BOLD}{arg}{RESET}")
        print("Usá -h, -help o --help para ver las opciones disponibles.\n")
        sys.exit(1)

# =====================================================================
# Detección automática de soporte Unicode
# =====================================================================
if not terminal_supports_unicode():
    # Si la terminal no soporta Unicode, actuamos como si el usuario hubiera pasado -i
    omit.update({"i", "icon"})

# =====================================================================
# HELP / AYUDA
# =====================================================================
if any(arg in ("-h", "--help", "-help") for arg in sys.argv):
    print(f"""{BOLD}SysStatCLI{RESET} (System Status CLI) - Version 2.43.20251108a

{BOLD}Repositorio:{RESET} {UNDERLINE}https://github.com/LiGNUxMan/SysStatCLI{RESET}
    
{BOLD}Autor:{RESET} Axel O'BRIEN ({ITALIC}LiGNUxMan{RESET}) · {UNDERLINE}axelobrien@gmail.com{RESET}
{BOLD}Colaboradora:{RESET} ChatGPT · OpenAI

{BOLD}Uso:{RESET}
  python3 sysstatcli.py [tiempo] [opciones]
  
{BOLD}Tiempo:{RESET} Segundos que se repetirá el script en bucle. Si se omite o es 0, se ejecuta una sola vez.
  Durante la ejecución, puede presionar {BOLD}Q{RESET} o {BOLD}X{RESET} para salir.

{BOLD}Opciones:{RESET} Argumentos disponibles para omitir secciones:
  -{BOLD}s{RESET}ys,  -s → Nombre del sistema operativo y versión del kernel
  -h{BOLD}o{RESET}st, -o → Nombre de la computadora y el usuario
  -{BOLD}u{RESET}p,   -u → Tiempo de actividad, hora y día del sistema
  -{BOLD}c{RESET}pu,  -c → Uso, frecuencia, modo y temperatura del CPU
  -{BOLD}r{RESET}am,  -r → Uso de memoria RAM y SWAP
  -{BOLD}p{RESET}roc, -p → Procesos y sus estados
  -{BOLD}l{RESET}oad, -l → Carga del sistema
  -{BOLD}d{RESET}isk, -d → Uso y temperatura del disco
  -l{BOLD}a{RESET}n,  -a → Red cableada
  -{BOLD}w{RESET}ifi, -w → Red WiFi y temperatura
  -ba{BOLD}t{RESET},  -t → Batería
  -{BOLD}b{RESET}ar,  -b → Omite todas las barras
    -barc, -bc → Omite la barra de CPU
    -barr, -br → Omite la barra de RAM
    -bard, -bd → Omite la barra de Disco
    -barw, -bw → Omite la barra de WiFi
    -bart, -bt → Omite la barra de Batería
  -{BOLD}i{RESET}con, -i → Oculta los íconos decorativos (se muestran por defecto si la terminal los soporta)

{BOLD}Ejemplos:{RESET}
  python3 sysstatcli.py            → Ejecuta una sola vez
  python3 sysstatcli.py 60         → Ejecuta cada 60 segundos
  python3 sysstatcli.py -ram -wifi → Ejecuta una sola vez, omitiendo RAM y WiFi
  python3 sysstatcli.py -s -b 10   → Ejecuta cada 10s, omitiendo datos del sistema y todas las barras

{BOLD}Ayuda:{RESET}
  -help, --help, -h → Muestra este mensaje y sale
""")
    sys.exit(0)


# Variables globales inicializacion
# Se toman estos valores al comienzo de scrpt porque luego seran tomados nuevamente para hacer comparativas
if {"cpu", "c"}.isdisjoint(omit):
    cpu_times_start = psutil.cpu_times(percpu=True)
    cpu_time_start = time.time()
if {"disk", "d"}.isdisjoint(omit):
    disk_io_start = psutil.disk_io_counters()
    disk_time_start = time.time()   
if {"lan", "a"}.isdisjoint(omit):
    lan_interface = "enxc025e92940b8"  # Nombre de la placa de red (MODIFICARLO SI TIENE OTRO NOMBRE)
    lan_stats = psutil.net_io_counters(pernic=True)
    if lan_interface in lan_stats:
        lan_io_start = lan_stats[lan_interface]
    else:
        lan_io_start = None
    lan_time_start = time.time()
if {"wifi", "w"}.isdisjoint(omit):
    wifi_interface = "wlp3s0" # Nombre de la placa WiFi (MODIFICARLO SI TIENE OTRO NOMBRE)
    wifi_io_start = psutil.net_io_counters(pernic=True).get(wifi_interface)
    wifi_time_start = time.time()
time.sleep(1)  # Pausa de 1 seg. Para mejorar la exactitud de los datos en una sola ejeucuion o la primera del bucle

# Función para generar barra de progreso
def barra_progreso(valor, total=100, ancho=32, color=RESET):
    bloques_llenos = int((valor / total) * ancho)
    barra = "█" * bloques_llenos + "░" * (ancho - bloques_llenos) # barra = "█" * bloques_llenos + " " * (ancho - bloques_llenos) ▁▂▃▄▅▆▇█ ░▒▓█
    return f"{color}{barra}{RESET}" # return f"{color}[{barra}]{RESET}" # return f"{color}▕{barra}▏{RESET}" # return f"{color}[{barra}]{RESET}"

# 🐧 OS: Linux Mint 22.1 - ⚙️  Kernel version: 6.11.0-19-generic
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

#     print(f"🐧 OS: {BOLD}{os_name}{RESET} - ⚙️  Kernel version: {BOLD}{kernel_version}{RESET}")

    if {"icon", "i"}.isdisjoint(omit):
        print(f"🐧 OS: {BOLD}{os_name}{RESET} - ⚙️  Kernel version: {BOLD}{kernel_version}{RESET}")
    else:
        print(f"OS: {BOLD}{os_name}{RESET} - Kernel version: {BOLD}{kernel_version}{RESET}")


# 🏠 Hostname: hal9001c - User: axel
def get_host_user_info():
    hostname = socket.gethostname()
    username = os.getlogin()

    if {"icon", "i"}.isdisjoint(omit):
        print(f"🏠 Hostname: {BOLD}{hostname}{RESET} - 👤 User: {BOLD}{username}{RESET}")
    else:
       print(f"Hostname: {BOLD}{hostname}{RESET} - User: {BOLD}{username}{RESET}") 

# ⏱️ Uptime: 1 day, 3:37:09 - 🕒 Time and date: 15:14:25 13/03/2025
def get_uptime_and_time():
    """Obtiene el uptime desde /proc/uptime, hora y fecha y los imprime."""
    uptime_seconds = time.time() - psutil.boot_time() # Linea agregada para el uptime de mem_info3_root
    uptime_str = str(timedelta(seconds=int(uptime_seconds))) # Linea agregada para el uptime de mem_info3_root
    current_time = time.strftime("%H:%M:%S %d/%m/%Y")

    if {"icon", "i"}.isdisjoint(omit):
        print(f"⏱️  Uptime: {BOLD}{uptime_str}{RESET} - 🕒 Time and date: {BOLD}{current_time}{RESET}")
    else:
        print(f"Uptime: {BOLD}{uptime_str}{RESET} - Time and date: {BOLD}{current_time}{RESET}")

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

    if {"icon", "i"}.isdisjoint(omit):
        print(f"🤖 CPU used: {uso_promedio_str} ({uso_nucleos_str})")
    else:
        print(f"CPU used: {uso_promedio_str} ({uso_nucleos_str})")
    
    if {"bar", "b", "barc", "bc"}.isdisjoint(omit):
        if {"icon", "i"}.isdisjoint(omit):
            print("   " + barra_progreso(promedio_uso, color=color_barra))
        else:
            print(barra_progreso(promedio_uso, color=color_barra))

    # Actualizar para la siguiente lectura
    cpu_times_start = cpu_times_current
    cpu_time_start = cpu_time_current
 
# ⚡ CPU frequency: 0.8GHz - 🎚️ Scaling governor: powersave
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
        
        if {"icon", "i"}.isdisjoint(omit):
             print(f"⚡ CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - 🎚️  Scaling governor: {BOLD}{scaling_governor}{RESET}") # {cur_freq:.2f}
        else:
             print(f"CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - Scaling governor: {BOLD}{scaling_governor}{RESET}") # {cur_freq:.2f}

    except FileNotFoundError:
        if {"icon", "i"}.isdisjoint(omit):
             print(f"⚡ CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - 🎚️  Scaling governor: {BOLD}{scaling_governor}{RESET}") # {cur_freq:.2f}
        else:
             print(f"CPU frequency: {color}{BOLD}{cur_freq:.2f}GHz{RESET} - Scaling governor: {BOLD}{scaling_governor}{RESET}") # {cur_freq:.2f}

# 🌡️ CPU temperature: 39°C
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

        if {"icon", "i"}.isdisjoint(omit):
             print(f"🌡️  CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")
        else:
             print(f"CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")

    except Exception:
        if {"icon", "i"}.isdisjoint(omit):
             print(f"🌡️  CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")
        else:
             print(f"CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")

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

    if {"icon", "i"}.isdisjoint(omit):
        print(f"🧮 RAM used: {BOLD}{mem_colored}{RESET} ({BOLD}{mem_used:.2f}GB / {mem_total:.2f}GB{RESET}) - "
            f"💾 Swap used: {BOLD}{swap_colored}{RESET} ({BOLD}{swap_used:.2f}GB / {swap_total:.2f}GB{RESET})")
    else:
        print(f"RAM used: {BOLD}{mem_colored}{RESET} ({BOLD}{mem_used:.2f}GB / {mem_total:.2f}GB{RESET}) - "
            f"Swap used: {BOLD}{swap_colored}{RESET} ({BOLD}{swap_used:.2f}GB / {swap_total:.2f}GB{RESET})")

    # Barra personalizada para RAM
    if {"bar", "b", "barr", "br"}.isdisjoint(omit):
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

        if {"icon", "i"}.isdisjoint(omit):
             print(f"   {barra_ram} - {barra_swap}")
        else:
            print(f"{barra_ram} - {barra_swap}")

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

        if {"icon", "i"}.isdisjoint(omit):
            print(f"🧩 Processes: {BOLD}{total_processes}{RESET} "
              f"({ITALIC}run{RESET}={BOLD}{process_states['running']}{RESET}, "
              f"{ITALIC}sleep{RESET}={BOLD}{process_states['sleeping']}{RESET}, "
              f"{ITALIC}idle{RESET}={BOLD}{process_states['idle']}{RESET}, "
              f"{ITALIC}stop{RESET}={BOLD}{process_states['stopped']}{RESET}, "
              f"{ITALIC}zombie{RESET}={BOLD}{process_states['zombie']}{RESET}, "
              f"{ITALIC}other{RESET}={BOLD}{process_states['other']}{RESET})")
        else:
            print(f"Processes: {BOLD}{total_processes}{RESET} "
              f"({ITALIC}run{RESET}={BOLD}{process_states['running']}{RESET}, "
              f"{ITALIC}sleep{RESET}={BOLD}{process_states['sleeping']}{RESET}, "
              f"{ITALIC}idle{RESET}={BOLD}{process_states['idle']}{RESET}, "
              f"{ITALIC}stop{RESET}={BOLD}{process_states['stopped']}{RESET}, "
              f"{ITALIC}zombie{RESET}={BOLD}{process_states['zombie']}{RESET}, "
              f"{ITALIC}other{RESET}={BOLD}{process_states['other']}{RESET})")
        
    except Exception as e:
        if {"icon", "i"}.isdisjoint(omit):
            print(f"🧩 Processes: {RED}{BOLD}Unknown{RESET}")
            # print(f"Error general en get_process_count: {e}")
        else:
            print(f"Processes: {RED}{BOLD}Unknown{RESET}")
            # print(f"Error general en get_process_count: {e}")

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
    
    if {"icon", "i"}.isdisjoint(omit):
        print(f"📊 Load average: {BOLD}{load1_str}{RESET} {BOLD}{load5_str}{RESET} {BOLD}{load15_str}{RESET}")
    else:        
        print(f"Load average: {BOLD}{load1_str}{RESET} {BOLD}{load5_str}{RESET} {BOLD}{load15_str}{RESET}")

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

    if {"icon", "i"}.isdisjoint(omit):
        print(f"🗄️  Disk used: {color}{BOLD}{percent:.0f}%{RESET} ({BOLD}{used:.2f}GB / {total:.2f}GB{RESET}) - Read: {BOLD}{disk_read_speed:.2f}MB/s{RESET} - Write: {BOLD}{disk_write_speed:.2f}MB/s{RESET}")
    else:
        print(f"Disk used: {color}{BOLD}{percent:.0f}%{RESET} ({BOLD}{used:.2f}GB / {total:.2f}GB{RESET}) - Read: {BOLD}{disk_read_speed:.2f}MB/s{RESET} - Write: {BOLD}{disk_write_speed:.2f}MB/s{RESET}")
    
    if {"bar", "b", "bard", "bd"}.isdisjoint(omit):
        barra_disk = barra_progreso(percent, color=color)
        if {"icon", "i"}.isdisjoint(omit):            
            print("   " + barra_disk)        
        else:
            print(barra_disk)

# 🌡️ Disk temperature: 32°C
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

        if {"icon", "i"}.isdisjoint(omit):
            print(f"🌡️  Disk temperature: {color}{BOLD}{composite_temp:.0f}°C{RESET}")
        else:        
            print(f"Disk temperature: {color}{BOLD}{composite_temp:.0f}°C{RESET}")

    except Exception as e:

        if {"icon", "i"}.isdisjoint(omit):
            print(f"🌡️  Disk temperature: {RED}{BOLD}Error: {str(e)}{RESET}")
        else:        
            print(f"Disk temperature: {RED}{BOLD}Error: {str(e)}{RESET}")

# 🌐 LAN IP: 192.168.0.123 - Speed: 100Mb/s (Full) - Down: 0.01MB/s - Up: 0.01MB/s
def get_lan_info():
    global lan_io_start, lan_time_start

    iface = lan_interface
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

    if {"icon", "i"}.isdisjoint(omit):
       print(f"🌐 LAN IP: {BOLD}{ip_address}{RESET} - Speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET}) - Down: {BOLD}{lan_download:.2f}MB/s{RESET} - Up: {BOLD}{lan_upload:.2f}MB/s{RESET}") 
    else:
        print(f"LAN IP: {BOLD}{ip_address}{RESET} - Speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET}) - Down: {BOLD}{lan_download:.2f}MB/s{RESET} - Up: {BOLD}{lan_upload:.2f}MB/s{RESET}")

    # Guardar valores para próxima llamada
    lan_io_start = lan_io_end
    lan_time_start = lan_time_end

# 📶 WIFI lan: OBRIEN 5 - IP: 192.168.0.208
# 📡 WIFI signal: 71% - Speed: 325.0Mb/s - Down: 4.57MB/s - Up: 0.93MB/s
# ██████████████████████░░░░░░░░░░
# 🌡️ WIFI temperature: 42°C
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
        if signal_percent < 25:
            color = RED
        elif signal_percent < 50:
            color = ORANGE
        elif signal_percent < 75:
            color = YELLOW
        else:
            color = RESET

        if {"icon", "i"}.isdisjoint(omit):
            print(f"📶 WiFi IP: {BOLD}{ip}{RESET} - SSID: {BOLD}{ssid}{RESET}")
            print(f"📡 WiFi signal: {color}{BOLD}{signal_percent:.0f}%{RESET} - Speed: {BOLD}{speed:.1f}Mb/s{RESET} - Down: {BOLD}{download_speed:.2f}MB/s{RESET} - Up: {BOLD}{upload_speed:.2f}MB/s{RESET}")       
        else:
            print(f"WiFi IP: {BOLD}{ip}{RESET} - SSID: {BOLD}{ssid}{RESET}")
            print(f"WiFi signal: {color}{BOLD}{signal_percent:.0f}%{RESET} - Speed: {BOLD}{speed:.1f}Mb/s{RESET} - Down: {BOLD}{download_speed:.2f}MB/s{RESET} - Up: {BOLD}{upload_speed:.2f}MB/s{RESET}")
        
        if {"bar", "b", "barw", "bw"}.isdisjoint(omit):
            if {"icon", "i"}.isdisjoint(omit):
                print(f"   {barra_progreso(signal_percent, color=color)}")
            else:
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

            if {"icon", "i"}.isdisjoint(omit):
                print(f"🌡️  WiFi temperature: {temp_color}{BOLD}{wifi_temp:.0f}°C{RESET}")
            else:
                print(f"WiFi temperature: {temp_color}{BOLD}{wifi_temp:.0f}°C{RESET}")

    except Exception as e:
        print(f"{RED}Error inesperado: {e}{RESET}")

# 🔋 Battery: 37% - Time: 0h 58m 52s - Mode: Discharging
# ███████████░░░░░░░░░░░░░░░░░░░░░
def get_battery_info():
    try:
        base_path = "/sys/class/power_supply/BAT0/"

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
                    ["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"],
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
        if {"icon", "i"}.isdisjoint(omit):
            print(f"🔋 Battery: {color}{BOLD}{battery_percent}%{RESET}{time_part} - Mode: {BOLD}{battery_mode}{RESET}")
        else:        
            print(f"Battery: {color}{BOLD}{battery_percent}%{RESET}{time_part} - Mode: {BOLD}{battery_mode}{RESET}")

        if {"bar", "b", "bart", "bt"}.isdisjoint(omit):
            barra_battery = barra_progreso(battery_percent, color=color)
            if {"icon", "i"}.isdisjoint(omit):
                print("   " + barra_battery)
            else:
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

###

def main():
    if {"sys", "s"}.isdisjoint(omit):
        get_system_info()
    
    if {"host", "o"}.isdisjoint(omit):
        get_host_user_info()
    
    if {"up", "u"}.isdisjoint(omit):
        get_uptime_and_time()

    if {"cpu", "c"}.isdisjoint(omit):
        get_cpu_usage()
        get_cpu_frequency()
        get_cpu_temperature()
    
    if {"ram", "r"}.isdisjoint(omit):
        get_memory_usage()

    if {"proc", "p"}.isdisjoint(omit):
        get_process_count()

    if {"load", "l"}.isdisjoint(omit):
        get_load_average()

    if {"disk", "d"}.isdisjoint(omit):
        get_disk_usage()
        get_nvme_temperature()

    if {"lan", "a"}.isdisjoint(omit):
        get_lan_info()

    if {"wifi", "w"}.isdisjoint(omit):
        get_wifi_info()

    if {"bat", "t"}.isdisjoint(omit):
        get_battery_info()

#    print("\a")
#    subprocess.run(["beep"])

# Repetición automática
if __name__ == "__main__":
    if interval > 0:
        start_time = time.time()

        count = 1

        # Inicia varialbes de minimo y maximo (borrar si ya no se quiere mostar)
        min_exec_duration = float('inf')
        max_exec_duration = float('-inf')

        old_settings = enable_raw_mode()

        try:
            while True:
                exec_start = time.time()

                os.system('clear')

                main()

                elapsed = int(time.time() - start_time)
                uptime = format_uptime(elapsed)

                exec_duration = (time.time() - exec_start) * 1000  # en milisegundos

                # Actualizar valores mínimos y máximos (borrar si ya no se quiere mostar)
                min_exec_duration = min(min_exec_duration, exec_duration)
                max_exec_duration = max(max_exec_duration, exec_duration)

                # actualiza la cantidad de RAM que consume este proceso                 
                proceso = psutil.Process(os.getpid())
                mem_proc_mb = proceso.memory_info().rss / 1024 / 1024

                for i in range(interval, 0, -1):

                    # Mostrar primero la línea de estado
                    # Mostrar primero la línea de estado
                    if {"icon", "i"}.isdisjoint(omit):
                        sys.stdout.write(
                            f"\r🔁 {DIM}Run: {uptime} ({min_exec_duration:.0f}/{exec_duration:.0f}/{max_exec_duration:.0f}ms)"
                            f" | Cycles: {count} | {mem_proc_mb:.2f}MB | Next: {i}/{interval}s {RESET}"
                        )
                    else:
                        sys.stdout.write(
                            f"\r{DIM}Run: {uptime} ({min_exec_duration:.0f}/{exec_duration:.0f}/{max_exec_duration:.0f}ms)"
                            f" | Cycles: {count} | {mem_proc_mb:.2f}MB | Next: {i}/{interval}s {RESET}"
                        )

                    sys.stdout.flush()

                    tick_start = time.time()

                    # Bucle interno que espera 1 segundo real, verificando teclas cada 0.1s
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
        main()


