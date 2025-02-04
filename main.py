from pyfiglet import Figlet
from phish import scan_phishing_url
from network_scan import network_scan
from port_scan import port_scan
from password_strength import check_password_strength
from ransomware_simulation import ransomware_simulation


def display_start_page():
    # Create a Figlet object with your preferred font
    f = Figlet(font='slant')
    title = f.renderText('Cyber Security Toolkit')
    
    # Center each line of the ASCII art
    for line in title.splitlines():
        print(line.center(80))
    
    # Center the developer credit and a separator line
    print("Developed by Aarish".center(80))
    print("=" * 80)
    
    

def main():

    display_start_page()

    while True:
        print("\nChoose an option:")
        print("1. Scan the network for active hosts")
        print("2. Check open ports for a specific IP")
        print("3. Check the strength of a password")
        print("4. Simulate Ransomware")
        print("5. Phishing URL Scan")
        print("6. Exit")

        choice = input("Enter 1, 2, 3, 4, 5, 6 or 7: ")

        if choice == '1':
            try:
            # Automatically detects the local network and scans it
              active_hosts = network_scan()
              
            except Exception as e:
                  print(f"An error occurred during the network scan: {e}")
            
        elif choice == '2':
            ip = input("Enter the IP to check for open ports: ")
            port_scan(ip)
        elif choice == '3':
            password = input("Enter a password to check: ")
            print(check_password_strength(password))
        elif choice == '4':
            
            # You can either use a default directory or allow the user to choose one
            directory = input("Enter the directory for ransomware simulation (default is Desktop/rtf): ")
            if not directory:
                directory = "/home/aarish/Desktop/rtf"  # Default directory will be used
            ransomware_simulation(directory)
            
        elif choice == '5':
            scan_phishing_url()
        elif choice == '6':
            print("Exiting the tool.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")
        
        repeat = input("\nDo you want to start again? (y/n): ").lower()
        if repeat != 'y':
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThanks for using the Cyber Security Toolkit. See you again!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}\nExiting the program. Goodbye!")

