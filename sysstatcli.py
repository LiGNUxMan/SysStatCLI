#!/usr/bin/env python3
# 
# SysStatCLI (System Status CLI) Version 1.28.20250321c
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
# RAM used: 32% (4.89GB / 15.49GB) - SWAP used: 0% (0.00GB / 0.00GB)
# ██████████░░░░░░░░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# Processes: 265 (running=1, sleeping=199, idle=65, stopped=0, zombie=0, other=0)
# Load average: 1.97 1.22 0.98
# Disk used: 43% (201.18GB / 467.91GB)
# █████████████░░░░░░░░░░░░░░░░░░░
# Disk temperature: 32°C
# LAN speed: 100Mb/s (Full) - IP: 192.168.0.123
# WIFI signal: 57% - Speed: 97.6Mb/s - Lan: OBRIEN 5 - IP: 192.168.0.208
# ██████████████████░░░░░░░░░░░░░░
# WIFI temperature: 42°C
# Battery: 47% - Mode: Discharging
# ██████████████░░░░░░░░░░░░░░░░░
# Ejecuciones: 4 / Próxima ejecución en 3/60 segundos...
# 
#

import os
import psutil
import re
import socket
import subprocess
import sys
import time
from datetime import timedelta # Linea agregada para el uptime de mem_info3_root

# Letra normal, bold, amarilla y roja
BOLD = "\033[1m" #
ITALIC = "\033[3m"
RESET = "\033[0m" #
GREEN = "\033[92m" #
# ORANGE = "\033[38;5;208m" #
ORANGE = "\033[38;5;214m" # naranja intenso.
YELLOW = "\033[33m" #
RED = "\033[31m" #

# Función para generar barra de progreso
def barra_progreso(valor, total=100, ancho=32, color=RESET):
    bloques_llenos = int((valor / total) * ancho)
    barra = "█" * bloques_llenos + "░" * (ancho - bloques_llenos) # barra = "█" * bloques_llenos + " " * (ancho - bloques_llenos) ▁▂▃▄▅▆▇█ ░▒▓█
    return f"{color}{barra}{RESET}" # return f"{color}[{barra}]{RESET}" # return f"{color}▕{barra}▏{RESET}" # return f"{color}[{barra}]{RESET}"

# OS: Linux Mint 22.1 - Kernel version: 6.11.0-19-generic
# Hostname: hal9001c - User: axel
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

    hostname = socket.gethostname()
    username = os.getlogin()

    print(f"OS: {BOLD}{os_name}{RESET} - Kernel version: {BOLD}{kernel_version}{RESET}")
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

    def get_colored_usage(usage):
        """Devuelve el porcentaje con color según el nivel de uso."""
        if usage < 33:
            color = RESET  # Normal
        elif usage < 66:
            color = YELLOW  # Amarillo
        elif usage < 99:
            color = ORANGE  # Amarillo
        else:
            color = RED  # Rojo
        return f"{color}{BOLD}{usage:.0f}%{RESET}", color  # Retorna el texto formateado y el color

    uso_nucleos = psutil.cpu_percent(interval=1,percpu=True) # Hace una pausa de 1seg para obtener el uso de CPU
    promedio_uso = sum(uso_nucleos) / len(uso_nucleos)

    uso_promedio_str, color_barra = get_colored_usage(promedio_uso)

    # Formatear el uso de cada núcleo con colores
    uso_nucleos_str = " - ".join([f"{ITALIC}CPU{i}{RESET}: {get_colored_usage(uso)[0]}" for i, uso in enumerate(uso_nucleos)])

    # Mostrar la salida formateada con el promedio en color y barra de progreso
    print(f"CPU used: {uso_promedio_str} ({uso_nucleos_str})")
    print(barra_progreso(promedio_uso, color=color_barra))
 
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
    """Obtiene la temperatura del CPU desde "/sys/class/thermal/thermal_zone0/temp" y la imprime con colores según el nivel."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read().strip()) / 1000
        color = RESET
        if temp > 60:
            color = RED
        elif temp > 40:
            color = ORANGE
        elif temp > 35:
            color = YELLOW

        print(f"CPU temperature: {color}{BOLD}{temp:.0f}°C{RESET}")
    except FileNotFoundError:
        print(f"CPU temperature: {RED}{BOLD}Unknown{RESET}")

# RAM used: 32% (4.89GB / 15.49GB) - SWAP used: 0% (0.00GB / 0.00GB)
# ██████████░░░░░░░░░░░░░░░░░░░░░░ - ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
def get_memory_usage():
    """Obtiene el uso de RAM y SWAP y los imprime con colores según el nivel de uso."""

    def color_usage(value):
        if value >= 90: # 90
            return RED, f"{RED}{value:.0f}%{RESET}"
        elif value >= 75: # 75
            return YELLOW, f"{YELLOW}{value:.0f}%{RESET}"
        else:
            return RESET, f"{value:.0f}%"

    with open("/proc/meminfo") as f:
        meminfo = f.readlines()
    
    mem_total = int(meminfo[0].split()[1]) / 1024 / 1024
    mem_available = int(meminfo[2].split()[1]) / 1024 / 1024
    mem_used = mem_total - mem_available
    mem_percent = (mem_used / mem_total) * 100
    
    swap_total = int(meminfo[14].split()[1]) / 1024 / 1024 if len(meminfo) > 14 else 0
    swap_free = int(meminfo[15].split()[1]) / 1024 / 1024 if len(meminfo) > 15 else 0
    swap_used = swap_total - swap_free
    swap_percent = (swap_used / swap_total) * 100 if swap_total > 0 else 0
    
    mem_color, mem_colored = color_usage(mem_percent)
    swap_color, swap_colored = color_usage(swap_percent)
    
    print(f"RAM used: {BOLD}{mem_colored}{RESET} ({BOLD}{mem_used:.2f}GB / {mem_total:.2f}GB{RESET}) - "
          f"SWAP used: {BOLD}{swap_colored}{RESET} ({BOLD}{swap_used:.2f}GB / {swap_total:.2f}GB{RESET})")
    
    barra_mem = barra_progreso(mem_percent, color=mem_color)
    barra_swap = barra_progreso(swap_percent, color=swap_color)
    print(f"{barra_mem} - {barra_swap}")

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
                            process_states["other"] += 1  # D (espera ininterrumpible) no es "idle"
                        elif state == "T":
                            process_states["stopped"] += 1
                        elif state == "Z":
                            process_states["zombie"] += 1
                        elif state == "I":
                            process_states["idle"] += 1  # Procesos en "I" son realmente idle
                        else:
                            process_states["other"] += 1
                except FileNotFoundError:
                    continue
        print(f"Processes: {BOLD}{total_processes}{RESET} "
              f"({ITALIC}running{RESET}={BOLD}{process_states['running']}{RESET}, "
              f"{ITALIC}sleeping{RESET}={BOLD}{process_states['sleeping']}{RESET}, "
              f"{ITALIC}idle{RESET}={BOLD}{process_states['idle']}{RESET}, "
              f"{ITALIC}stopped{RESET}={BOLD}{process_states['stopped']}{RESET}, "
              f"{ITALIC}zombie{RESET}={BOLD}{process_states['zombie']}{RESET}, "
              f"{ITALIC}other{RESET}={BOLD}{process_states['other']}{RESET})")
    except FileNotFoundError:
        print(f"Processes: {RED}{BOLD}Unknown{RESET}")

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

# Disk used: 43% (201.18GB / 467.91GB)
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

    barra_disk = barra_progreso(percent, color=color)

    print(f"Disk used: {color}{BOLD}{percent:.0f}%{RESET} ({BOLD}{used:.2f}GB / {total:.2f}GB{RESET})")
    print(barra_disk)

# Disk temperature: 32°C
def get_nvme_temperature():
    """Obtiene la temperatura del NVMe desde el comando 'sensors' y la imprime con colores según el nivel."""
    try:
        # Ejecutar el comando 'sensors' y obtener la salida
        output = subprocess.run(["sensors"], capture_output=True, text=True).stdout
        
        # Buscar la sección nvme-pci-0100
        nvme_section = re.search(r"(nvme-pci-0100.*?)(\n\n|\Z)", output, re.S)
        if not nvme_section:
            print(f"Disk temperature: {RED}{BOLD}Unknown{RESET}")
            return
        
        # Buscar la línea de temperatura 'Composite'
        temp_match = re.search(r"Composite:\s+\+([\d.]+)°C", nvme_section.group(1))
        if not temp_match:
            print(f"Disk temperature: {RED}{BOLD}Unknown{RESET}")
            return
        
        # Obtener el valor numérico de la temperatura
        temp = float(temp_match.group(1))
        
        # Aplicar colores según la temperatura
        if temp >= 70: #70
            color = RED  # Alerta roja
        elif temp >= 50: # 50
            color = YELLOW  # Advertencia amarilla
        else:
            color = RESET  # Normal, sin color

        # Imprimir la temperatura
        print(f"Disk temperature: {color}{BOLD}{temp:.0f}°C{RESET}") # print(f"NVMe Temp: {color}{BOLD}{temp:.1f}°C{RESET}")

    except Exception as e:
        print(f"Disk temperature: {RED}{BOLD}Error: {str(e)}{RESET}") # print(f"NVMe Temp: {RED}{BOLD}Error: {str(e)}{RESET}")

# LAN speed: 100Mb/s (Full) - IP: 192.168.0.123
def get_lan_info():
    iface = "enxc025e92940b8"  # Nombre de tu interfaz de red cableada
    stats = psutil.net_if_stats().get(iface)
    addrs = psutil.net_if_addrs().get(iface)
    
    # Si la interfaz no existe o no está activa, no mostrar nada
    if not stats or not stats.isup:
        return ""
    
    # Buscar una dirección IPv4 en la interfaz
    ip_address = None
    if addrs:
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
                break
    if not ip_address:
        return ""
    
    # Obtener velocidad (en Mb/s) y modo dúplex
    speed = stats.speed  # En Mb/s
    duplex = stats.duplex
    if duplex == psutil.NIC_DUPLEX_FULL:
        duplex_str = "Full"
    elif duplex == psutil.NIC_DUPLEX_HALF:
        duplex_str = "Half"
    else:
        duplex_str = "Unknown"
    
    # Devolver la salida formateada
    print(f"LAN speed: {BOLD}{speed}Mb/s{RESET} ({BOLD}{duplex_str}{RESET}) - IP: {BOLD}{ip_address}{RESET}")

# WIFI signal: 57% - Speed: 97.6Mb/s - Lan: OBRIEN 5 - IP: 192.168.0.208
# ██████████████████░░░░░░░░░░░░░░
# WIFI temperature: 42°C
def get_wifi_info():
    """Obtiene la información de la red WiFi."""
    try:
        # Obtener información de la red WiFi
        output = subprocess.run(["iwconfig", "wlp3s0"], capture_output=True, text=True).stdout
        if "no wireless extensions" in output or "Not-Associated" in output:
            return  # No mostrar nada si no hay WiFi conectado
        
        # Extraer información relevante
        ssid_match = re.search(r'ESSID:"(.*?)"', output)
        quality_match = re.search(r'Link Quality=(\d+)/(\d+)', output)
        signal_match = re.search(r'Signal level=(-?\d+) dBm', output)
        speed_match = re.search(r'Bit Rate=(\d+\.?\d*) Mb/s', output)
        ip_output = subprocess.run(["ip", "-4", "addr", "show", "wlp3s0"], capture_output=True, text=True).stdout
        ip_match = re.search(r'inet\s(\d+\.\d+\.\d+\.\d+)', ip_output)
        
        # Procesar valores
        ssid = ssid_match.group(1) if ssid_match else "Unknown"
        quality = int(quality_match.group(1)) if quality_match else 0
        max_quality = int(quality_match.group(2)) if quality_match else 70
        signal_percent = (quality / max_quality) * 100 if quality_match else 0
        speed = float(speed_match.group(1)) if speed_match else 0.0
        ip = ip_match.group(1) if ip_match else "Unknown"
        
        # Definir color de la señal WiFi
        if signal_percent < 40:
            color = RED
        elif signal_percent < 70:
            color = YELLOW
        else:
            color = RESET
        
        # Construir salida de WiFi
        wifi_info = (f"WIFI signal: {color}{BOLD}{signal_percent:.0f}%{RESET} - "
            f"Speed: {BOLD}{speed:.1f}Mb/s{RESET} - "
            f"Lan: {BOLD}{ssid}{RESET} - "
            f"IP: {BOLD}{ip}{RESET}\n"
            f"{barra_progreso(signal_percent, color=color)}")
        
        # Obtener temperatura de la placa WiFi
        temp_output = subprocess.run(["sensors"], capture_output=True, text=True).stdout
        temp_match = re.search(r'iwlwifi_1-virtual-0.*?temp1:\s*\+(\d+\.\d+)°C', temp_output, re.DOTALL)
        temperature = float(temp_match.group(1)) if temp_match else None
        
        if temperature is not None:
            if temperature > 70:
                temp_color = RED
            elif temperature > 50:
                temp_color = YELLOW
            else:
                temp_color = RESET
            wifi_info += f"\nWIFI temperature: {temp_color}{BOLD}{temperature:.0f}°C{RESET}"
        
        print(wifi_info)
    except Exception as e:
        pass  # No mostrar nada en caso de error

# Battery: 47% - Mode: Discharging
# ███████████████░░░░░░░░░░░░░░░░░
def get_battery_info():
    try:        
        base_path = "/sys/class/power_supply/BAT0/"

        # Leer el estado de la batería
        with open(os.path.join(base_path, "status"), "r") as f:
            battery_mode = f.read().strip()

        if battery_mode == "Full":
            return ""  # No hacer nada
        else:
            # Leer el porcentaje de batería
            with open(os.path.join(base_path, "capacity"), "r") as f:
                battery_percent = int(f.read().strip())

            # Aplicar color al porcentaje
            if battery_percent > 25:
                color = RESET  # Blanco
            elif battery_percent > 10:
                color = YELLOW  # Amarillo
            else:
                color = RED  # Rojo

            barra_battery = barra_progreso(battery_percent, color=color)

            print(f"Battery: {color}{BOLD}{battery_percent}%{RESET} - Mode: {BOLD}{battery_mode}{RESET}")
            print(barra_battery)

    except Exception as e:
        print(f"Battery: Error: {e}")

# Repetición automática
def main():
    get_system_info()
    get_uptime_and_time()
    get_cpu_usage()
    get_cpu_frequency()
    get_cpu_temperature()
    get_memory_usage()
    get_process_count()
    get_load_average()
    get_disk_usage()
    get_nvme_temperature()
    get_lan_info()
    get_wifi_info()
    get_battery_info()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            count = 1  # Inicializa el contador
            while True:
                os.system('clear')
                main()
                
                # Cuenta regresiva
                for i in range(interval, 0, -1):
                    # sys.stdout.write("\r" + " " * 40 + "\r") # Borra la línea
                    sys.stdout.write(f"\rRuns: {count} / Next run in {i}/{interval} seconds... ")
                    sys.stdout.flush()
                    time.sleep(1)

                count += 1  # Aumenta el contador en cada iteración
                
        except ValueError:
            print("Uso incorrecto: Debes proporcionar un número natural paralos segundos.")
            sys.exit(1)
    else:
        main()


