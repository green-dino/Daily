#!python3
# Prints network Addresses, Hosts, NETMASK, global and private 

import ipaddress

def get_valid_input(prompt):
    while True:
        try:
            network = input(prompt).strip()
            netobj = ipaddress.ip_network(network, strict=False)
            return netobj
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid network address.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def print_hosts(network):
    host_list = list(network.hosts())
    for i in host_list in enumerate(host_list, start=1):
        print(host_list)
        if i % 10 == 0: # hosts per page 
            cont = input("Press enter for more hosts or type 'exit' to stop:")
            if cont == 'exit':
                break

def print_network_details(network):
    """Print network details and hosts."""
    print(f"\nNetwork Address: {network.network_address}")
    print(f"Number of valid hosts: {network.num_addresses - 2}")
    print(f"Network Size: {network.num_addresses}")
    print(f"Netmask: {network.netmask}")
    print(f"Network Slash Notation: {network.exploded}")
    print(f"Is global: {network.is_global}")
    print(f"Is private: {network.is_private}")
    print(f"Is link local: {network.is_link_local}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(f"Network Version: {'IPv6' if network.version == 6 else 'IPv4'}")
    
    for ip in network.hosts():
        print(ip)

def usage_guide():
    print("Usage: Enter a network address in CIDR notation, e.g., 192.168.1.0/24")
    print("The script will display network address details and valid host addresses.")
    print("Type 'exit' to quit the program at any prompt.\n")

def main():
    while True:
        try:
            network = get_valid_input("Enter a network address in the following format xxx.xxx.xxx.0/xx: ")
            print_network_details(network)

            for ip in network.hosts():
                print(ip)
            
            cont = input("\nPress enter to continue or type 'exit' to quit: ").strip().lower()
            if cont == 'exit':
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn unexpected error has occurred: {e}")
            break

if __name__ == "__main__":
    main()

