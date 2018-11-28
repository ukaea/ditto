import nmap


def is_port_in_use(address, port):
    scanner = nmap.PortScanner()
    scanner.scan(str(address), str(port))
    state = scanner[str(address)]['tcp'][int(port)]['state']
    return state == 'open'


def print_port_usage(address, port):
    is_in_use = is_port_in_use(address, port)
    print(f'Port {port} is {"" if is_in_use else "not "}in use')
