import nmap
import os


def is_port_in_use(address, port):
    scanner = nmap.PortScanner()
    scanner.scan(str(address), str(port))
    state = scanner[str(address)]['tcp'][int(port)]['state']
    return state == 'open'


def is_process_running(process_id):
    try:
        os.kill(process_id, 0)
        return True
    except Exception:
        return False


def print_port_state(address, port):
    # See https://nmap.org/book/man-port-scanning-basics.html for an explanation of the various states
    scanner = nmap.PortScanner()
    scanner.scan(str(address), str(port))
    state = scanner[str(address)]['tcp'][int(port)]['state']
    print(f'Port {port} is "{state}"')
