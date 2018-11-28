import nmap


def is_port_in_use(address, port):
    scanner = nmap.PortScanner()
    scanner.scan(str(address), str(port))
    state = scanner[str(address)]['tcp'][int(port)]['state']
    return state == 'open'
