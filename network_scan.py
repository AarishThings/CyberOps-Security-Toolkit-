import nmap
import socket
import ipaddress

def get_local_ip():
    """Finds the local IP address of the current machine."""
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))  # Connects to a public DNS server
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as e:
        print(f"Error retrieving local IP: {e}")
        return None

def get_subnet(local_ip):
    """Calculates the subnet range based on the local IP."""
    try:
        network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
        return str(network)
    except Exception as e:
        print(f"Error calculating subnet: {e}")
        return None

def network_scan():
    """Main network scanning function that lets the user choose to scan the current subnet or enter a custom one."""
    print("Choose an option:")
    print("1. Scan the current subnet")
    print("2. Enter a custom subnet")
    
    choice = input("Enter your choice (1/2): ").strip()

    if choice == '1':
        # Automatically detect the current subnet and scan it
        local_ip = get_local_ip()
        if not local_ip:
            print("Could not determine the local IP address. Exiting.")
            return []

        subnet = get_subnet(local_ip)
        if not subnet:
            print("Could not calculate the subnet range. Exiting.")
            return []

        nm = nmap.PortScanner()
        print(f"Scanning subnet: {subnet}")
        try:
            nm.scan(hosts=subnet, arguments='-sP')  # Ping scan to find active hosts
            active_hosts = [host for host in nm.all_hosts() if nm[host].state() == "up"]
            print("Active hosts in the network:")
            for host in active_hosts:
                print(f" - {host}")
            return active_hosts
        except Exception as e:
            print(f"Error during network scan: {e}")
            return []

    elif choice == '2':
        # User can input a custom subnet
        custom_subnet = input("Enter the subnet to scan (e.g., 192.168.1.0/24): ").strip()
        try:
            # Validate the custom subnet
            ipaddress.ip_network(custom_subnet, strict=False)
            nm = nmap.PortScanner()
            print(f"Scanning subnet: {custom_subnet}")
            nm.scan(hosts=custom_subnet, arguments='-sP')  # Ping scan to find active hosts
            active_hosts = [host for host in nm.all_hosts() if nm[host].state() == "up"]
            print("Active hosts in the network:")
            for host in active_hosts:
                print(f" - {host}")
            return active_hosts
        except ValueError:
            print("Invalid subnet entered. Please enter a valid subnet in CIDR notation (e.g., 192.168.1.0/24).")
            return []

    else:
        print("Invalid choice. Exiting.")
        return []


