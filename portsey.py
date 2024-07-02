from prettytable import PrettyTable
import subprocess

# lsof command output
output = subprocess.check_output("sudo lsof -i -P -n", shell=True).decode()

# Split the output into lines
lines = output.split("\n")

# define the table
table = PrettyTable()
table.field_names = ["COMMAND", "PID", "USER", "BIND ADDRESS", "PORT", "STATUS", "SERVICE"]

# Map known ports to their services
services = {
    "22": "Standard SSH",
    "53": "Standard DNS",
    "54": "Adguard DNS",
    "80": "HTTP",
    "443": "HTTPS",
    "1080": "V2ray HTTPS Proxy",
    "3000": "Adguard Admin",
    "3306": "MySQL",
    "5900": "VNC:1",
    "5901": "VNC:1",
    "6722": "Custom SSH",
    "6733": "Phishing Page",
    "10000": "Standard Webmin",
    "12000": "Custom Webmin",
    "20000": "Standard Usermin",
    "22000": "Custom Usermin",
    "31337": "Shadowsocks",
    "31338": "Wireguard VPN",
    "31339": "Wireguard Manager",
    "33060": "MySQL",
    "37173": "Netbird Admin",
    "37337": "LiberTea Admin",
}

# this is where all the data is shown in a pretty tsable
for line in lines[1:]:  # Skip the header line
    if line:
        fields = line.split()
        fields = fields[:3] + fields[8:]  # Adjust fields as before
        if ':' in fields[3]:
            if fields[3].count(':') > 1:  # Likely an IPv6 address
                *ip, port = fields[3].rsplit(':', 1)
                ip = ':'.join(ip)
            else:  # IPv4
                ip, port = fields[3].split(':')
            service = services.get(port, 'Unknown')
            fields[3] = ip
            fields.insert(4, port)
            fields.append(service)
        else:
            fields.insert(4, 'N/A')
            fields.append('N/A')
        if len(fields) == 7:  # Ensure the row has the correct number of fields
            table.add_row(fields)

print(table)
