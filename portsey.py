import subprocess

from rich.console import Console
console = Console()
from rich.table import Table
from rich.text import Text
from typing import List, Dict
import json
import os
import platform
import pyfiglet
import re
import requests

# Smart glyph assignment for known apps
SMART_GLYPHS = {
    "Docker": "🐳",
    "Firefox": "🦊",
    "Chrome": "🌐",
    "Brave": "🦁",
    "Safari": "🧭",
    "Edge": "🔵",
    "VMware": "🐧",
    "VirtualBox": "📦",
    "1Password": "🔑",
    "Folx": "📥",
    "Transmission": "📡",
    "BitTorrent": "🌊",
    "Spotify": "🎵",
    "Apple Music": "🍎",
    "VLC": "🎬",
    "OBS": "📹",
    "Zoom": "🎥",
    "Slack": "💬",
    "Discord": "🗨️",
    "Teams": "👥",
    "Skype": "📞",
    "ChatGPT": "🤖",
    "Cursor": "💻",
    "Code": "💻",
    "Windsurf": "💻",
    "Warp": "💻",
    "Python": "🐍",
    "Node": "🟢",
    "Java": "☕",
    "Postman": "📮",
    "Insomnia": "🌙",
    "Redis": "🧠",
    "Mongo": "🍃",
    "MySQL": "🐬",
    "PostgreSQL": "🐘",
    "nginx": "🌀",
    "apache": "🔥",
    "httpd": "🌍",
    "zsh": "💀",
    "bash": "🐚",
    "curl": "🌊",
    "wget": "📡",
    "git": "🌱",
}

DEFAULT_GLYPHS = ["🚀", "🎯", "🔌", "📡", "🎧", "📦", "📁"]
COLORS = ["cyan", "blue", "green", "magenta", "yellow", "red", "white"]

command_styles = {}
color_index = 0
glyph_index = 0

def get_style(command):
    global color_index, glyph_index
    if command not in command_styles:
        color = COLORS[color_index % len(COLORS)]
        glyph = SMART_GLYPHS.get(command, DEFAULT_GLYPHS[glyph_index % len(DEFAULT_GLYPHS)])
        command_styles[command] = {"color": color, "glyph": glyph}
        color_index += 1
        glyph_index += 1
    return command_styles[command]

def run_lsof_command() -> str:
    try:
        return subprocess.check_output(["sudo", "lsof", "-i", "-P", "-n"], text=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: lsof command failed - {e}[/red]")
        return ""
    except FileNotFoundError:
        console.print("[red]Error: lsof command not found. Please install it.[/red]")
        return ""

def load_services_mapping(file_path: str) -> Dict[str, str]:
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        console.print(f"[yellow]Warning: {file_path} not found. Defaulting to empty mapping.[/yellow]")
        return {}

def get_docker_containers() -> Dict[str, Dict[str, str]]:
    containers = {}
    try:
        output = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}} {{.Ports}}"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        if not output.strip():
            return containers
        for line in output.strip().splitlines():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                name, ports = parts
                port_mappings = re.findall(r'(\d+\.\d+\.\d+\.\d+:)?(\d+)->(\d+)/\w+', ports)
                for _, host_port, guest_port in port_mappings:
                    containers[host_port] = {"name": name, "guest_port": guest_port}
    except FileNotFoundError:
        console.print("[yellow]Notice: Docker is not installed or not found in PATH. Docker ports will not be shown.[/yellow]")
    except subprocess.CalledProcessError:
        console.print("[yellow]Notice: Docker is installed but not running. Please start the Docker daemon to view container ports.[/yellow]")
    return containers

def normalize_command(command: str) -> str:
    ide_aliases = {
        "code": "Code",
        "com.microsoft.VSCode": "Code",
        "cursor": "Cursor",
        "warp-terminal": "Warp",
        "warp": "Warp",
        "windsurf": "Windsurf",
    }
    docker_aliases = ["docker", "com.docker", "com.docke"]
    command_lower = command.lower()
    if command_lower in docker_aliases:
        return "Docker"
    return ide_aliases.get(command_lower, command)

def identify_service(port):
    try:
        response = requests.get(f"https://portapi.io/port/{port}")
        service_display = "Unknown"
        if response.status_code == 200:
            data = response.json()
            return data.get("service", "Unknown")
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to query service for port {port} - {e}[/yellow]")
    return "Unknown"

def parse_lsof_output(output: str, services: Dict[str, str], docker_containers: Dict[str, Dict[str, str]]) -> List[List[str]]:
    lines = output.splitlines()
    parsed_data = []
    seen_entries = set()

    ipv4_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)->(\d+\.\d+\.\d+\.\d+):(\d+)')

    for line in lines[1:]:
        if line.strip():
            fields = line.split()
            if len(fields) < 9:
                continue

            command, pid, user = fields[:3]
            bind_address = fields[8]

            if '[' in bind_address or bind_address.count(':') > 2:
                continue

            match = ipv4_pattern.match(bind_address)
            if match:
                local_ip, local_port, remote_ip, remote_port = match.groups()
                ip_display = remote_ip
                port_display = remote_port
            else:
                if ':' in bind_address:
                    ip_display, local_port = bind_address.split(':')
                    port_display = local_port
                else:
                    ip_display, port_display = bind_address, "N/A"

            command_display = normalize_command(command)

            if local_port in docker_containers:
                container_info = docker_containers[local_port]
                service_display = f"{container_info['name']} ({services.get(local_port, 'Unknown')})"
                command_display = "Docker"
                port_display = f"{local_port}:{container_info['guest_port']}"
            else:
                service_display = services.get(local_port, "Unknown")

            entry_key = (command_display, port_display)
            if entry_key in seen_entries:
                continue
            seen_entries.add(entry_key)

            parsed_data.append([command_display, pid, user, ip_display, port_display, service_display])

    parsed_data.sort(key=lambda x: (0 if x[0] == "Docker" else 1, x[0]))
    return parsed_data

def display_table(data: List[List[str]]) -> None:
    ascii_banner = pyfiglet.figlet_format("Portsey", font="slant")
    console.print(Text(ascii_banner, style="bold cyan"))

    table = Table(show_header=True, header_style="bold white on blue", border_style="bright_black")
    headers = ["COMMAND", "PID", "USER", "REMOTE IP", "PORT", "SERVICE"]
    for header in headers:
        table.add_column(header)

    for row in data:
        command, pid, user, ip, port, service = row
        style = get_style(command)
        color, glyph = style["color"], style["glyph"]

        table.add_row(
            f"[{color}]{glyph} {command}[/{color}]",
            f"[yellow]{pid}[/yellow]",
            f"[green]{user}[/green]",
            f"[cyan]{ip}[/cyan]",
            f"[magenta]{port}[/magenta]",
            f"[{color}]{service}[/{color}]"
        )

    console.print(table)

def detect_os() -> str:
    system = platform.system().lower()
    return "macOS 🍎" if 'darwin' in system else "Linux 🐧" if 'linux' in system else "Unknown ❓"

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    services_file = os.path.join(script_dir, "services.json")
    services = load_services_mapping(services_file)

    os_type = detect_os()
    console.print(f"[bold green]Operating System: {os_type}[/bold green]")

    output = run_lsof_command()
    if not output:
        return

    docker_containers = get_docker_containers()
    parsed_data = parse_lsof_output(output, services, docker_containers)
    display_table(parsed_data)

    alias_file = os.path.expanduser("~/.zshrc") if os.path.exists(os.path.expanduser("~/.zshrc")) else os.path.expanduser("~/.bashrc")
    alias_command = f"alias ports='python3 {os.path.abspath(__file__)}'"
    with open(alias_file, "r+") as file:
        content = file.read()
        if "alias ports=" not in content:
            file.write(f"\n# Alias for Portsey script\n{alias_command}\n")
            console.print("[bold cyan]Alias 'ports' added to your shell config. Restart your terminal or run 'source ~/.zshrc' or 'source ~/.bashrc' to use it.[/bold cyan]")

if __name__ == "__main__":
    main()