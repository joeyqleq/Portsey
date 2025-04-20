import subprocess
from prettytable import PrettyTable
from typing import List, Dict
import json
import os
import platform


def run_lsof_command() -> str:
    """Run the lsof command and return its output."""
    try:
        return subprocess.check_output(["sudo", "lsof", "-i", "-P", "-n"], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: lsof command failed - {e}")
        return ""
    except FileNotFoundError:
        print("Error: lsof command not found. Please install it.")
        return ""


def load_services_mapping(file_path: str) -> Dict[str, str]:
    """Load port-to-service mappings from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        print(f"Warning: {file_path} not found. Defaulting to empty mapping.")
        return {}


def parse_lsof_output(output: str, services: Dict[str, str]) -> List[List[str]]:
    """Parse the output of the lsof command and return a list of rows."""
    lines = output.splitlines()
    parsed_data = []

    for line in lines[1:]:  # Skip the header line
        if line.strip():
            fields = line.split()
            if len(fields) < 9:  # Skip lines with insufficient fields
                continue

            command, pid, user = fields[:3]
            bind_address = fields[8]

            if ":" in bind_address:
                # Parse IPv4 or IPv6 addresses
                if bind_address.count(":") > 1:  # IPv6
                    *ip, port = bind_address.rsplit(":", 1)
                    ip = ":".join(ip)
                else:  # IPv4
                    ip, port = bind_address.split(":")
                service = services.get(port, "Unknown")
            else:
                ip, port, service = bind_address, "N/A", "N/A"

            parsed_data.append([command, pid, user, ip, port, service])

    return parsed_data


def display_table(data: List[List[str]]) -> None:
    """Display data in a formatted table."""
    table = PrettyTable()
    table.field_names = ["COMMAND", "PID", "USER", "BIND ADDRESS", "PORT", "SERVICE"]

    for row in data:
        table.add_row(row)

    print(table)


def detect_os() -> str:
    """Detect the operating system."""
    system = platform.system().lower()
    if 'darwin' in system:
        return "macOS"
    elif 'linux' in system:
        return "Linux"
    else:
        return "Unknown"


def main():
    """Main function to run the script."""
    services_file = "services.json"
    services = load_services_mapping(services_file)

    os_type = detect_os()
    print(f"Operating System: {os_type}")

    output = run_lsof_command()
    if not output:
        return

    parsed_data = parse_lsof_output(output, services)
    display_table(parsed_data)


if __name__ == "__main__":
    main()
