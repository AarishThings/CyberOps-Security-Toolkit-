import nmap

def port_scan(ip):
    nm = nmap.PortScanner()
    print(f"Scanning ports on: {ip}")

    try:
        port_range = input("Enter the port range to scan (e.g., 20-80): ")
        try:
            start_port, end_port = map(int, port_range.split('-'))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError("Invalid port range. Ports must be in 1-65535 range.")
        except ValueError as ve:
            print(f"Error: {ve}")
            return

        print(f"Scanning ports {start_port}-{end_port} on {ip}...")
        nm.scan(hosts=ip, arguments=f'-p {start_port}-{end_port} -T4 -Pn --open')

        if ip not in nm.all_hosts() or 'tcp' not in nm[ip]:
            print(f"No response or no open TCP ports on {ip}.")
            return

        open_ports = [port for port, data in nm[ip]['tcp'].items() if data['state'] == 'open']

        if open_ports:
            print(f"Open TCP ports on {ip}: {', '.join(map(str, open_ports))}")
        else:
            print(f"No open TCP ports found on {ip}.")
    
    except Exception as e:
        print(f"Error scanning ports on {ip}: {e}")

