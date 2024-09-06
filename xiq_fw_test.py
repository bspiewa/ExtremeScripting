#! /usr/bin/python
import concurrent.futures
import importlib.util
import socket

requests_spec = importlib.util.find_spec("requests")
is_requests = requests_spec is not None

# Tested with Python 3.6
# Fork of "ExtremeCloudIQ-APIs -> XIQ API Python demo scripts -> XIQ-FW port test.py"

SSL_VERIFY = True


class Style:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"


try:
    import requests
    import urllib3
except ImportError:
    print(f"{Style.YELLOW}***WARNING: No 'requests' module installed***{Style.RESET}")


def main():

    with open("results.txt", "w", encoding="utf-8") as output:
        print("\nExtremeCloud IQ reachability test")

        print("\nTesting the ability to reach the ExtremeCloud IQ Global Data Center")
        xiq_default_servers = [
            ["extremecloudiq.com", tcp, 80],
            ["redirector.aerohive.com", tcp, 22],
            ["redirector.aerohive.com", tcp, 443],
            ["hmupdates-ng.aerohive.com", tcp, 443],
            ["extremecloudiq.com", tcp, 443],
            ["cloud-rd.aerohive.com", tcp, 443],
            ["redirector.aerohive.com", udp, 12222],
        ]
        test_servers(xiq_default_servers, output)

        print("\nTesting the ability to reach the ExtremeCloud IQ Regional Data Center")
        update_servers = [
            ["nl-gcp.extremecloudiq.com", tcp, 443],
            ["nl-gcp.extremecloudiq.com", tcp, 2083],
        ]
        test_servers(update_servers, output)

        print("\nTesting license Server Communication")
        test_servers(
            [
                ["hmupdates-ng.aerohive.com", tcp, 443],
            ],
            output,
        )
        if is_requests:
            print("\nTesting response time")
            urls = [
                "https://extremecloudiq.com",
                "https://nl-gcp.extremecloudiq.com",
                "https://va2.extremecloudiq.com",
                "https://redirector.aerohive.com",
                "https://hmupdates-ng.aerohive.com",
            ]
            test_response_time(urls)
            print("\n\nTest complete. Check details in 'results.txt'")


def test_servers(servers, log):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(server[1], server[0], server[2]) for server in servers
        ]
        for future in concurrent.futures.as_completed(futures):
            result, logged = future.result()
            print(result)
            log.write(logged)
            log.flush()


def tcp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(10)
        s.connect((host, port))
        result = f"{host + ':' + str(port):<40}{Style.GREEN}pass{Style.RESET}"
        log = f"{host}:{port} pass\n"
    except socket.error as e:
        result = f"{host + ':' + str(port):<40}{Style.RED}fail{Style.RESET}"
        log = f"{host}:{port} fail with exception {e}\n"
    finally:
        s.close()
    return result, log


def udp(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = "70408000000000000000012c040045000009f61900001f400038".rjust(164, "0")
        hex_message = bytes.fromhex(message)
        s.sendto(hex_message, (host, port))
        # receive data from the client
        s.setblocking(0)  # Set to non-blocking.
        s.settimeout(10)  # give the server 10 seconds to respond.
        # data = s.recvfrom(1024)
        # reply = data[0]
        # address = data[1]
        result = f"{host + ':' + str(port):<40}{Style.GREEN}pass{Style.RESET}"
        log = f"{host}:{port} pass\n"
    except socket.error as e:
        result = f"{host + ':' + str(port):<40}" f"{Style.RED}fail{Style.RESET}"
        log = f"{host}:{port} fail with exception {e}\n"
    finally:
        s.close()
    return result, log


def test_response_time(urls):
    if not SSL_VERIFY:
        urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
        print(f"{Style.YELLOW}***WARNING: SSL_VERIFY disabled***{Style.RESET}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(make_request, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)


def make_request(url):
    try:
        r = requests.get(url, timeout=10, verify=SSL_VERIFY)
        return f"{url:<40}{Style.GREEN}{r.elapsed.total_seconds():.6f} seconds{Style.RESET}"
    except requests.exceptions.Timeout:
        return f"{url:<40}{Style.RED}timeout{Style.RESET}"
    except requests.exceptions.RequestException as e:
        return f"{url:<40}{Style.RED}fail with exception {e}{Style.RESET}"


if __name__ == "__main__":
    main()
