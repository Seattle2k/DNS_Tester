#python script to send DNS qeueries - written by Cameron Miller, with help from GPT

import dns.resolver
import dns.exception
import time

def send_dns_query(domain, dns_server, print_info=False):
    """
    Send a DNS query to a specific DNS server for the given domain.

    Args:
    - domain (str): The domain to query.
    - dns_server (str): The DNS server to send the query to.
    - print_info (bool): Whether to print DNS request and response.

    Returns:
    - str: The response code (NXDOMAIN, NOERROR, TIMEOUT, SERVFAIL, REFUSED, or other).
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]

    if print_info:
        print(f"Sending DNS query for {domain} to {dns_server}")

    start_time = time.time()

    try:
        answers = resolver.resolve(domain, 'A', lifetime=4)  # Specify the record type as 'A' and set a timeout
        if print_info:
            print("Response:")
            for data in answers:
                print("IP Address:", data.address)
        return "NOERROR"
    except dns.resolver.NXDOMAIN:
        if print_info:
            print("Response: NXDOMAIN")
        return "NXDOMAIN"
    except dns.resolver.NoAnswer:
        if print_info:
            print("Response: NoAnswer")
        return "NOERROR"  # Handle cases where there is no answer but the domain exists
    except dns.exception.Timeout:
        elapsed_time = time.time() - start_time
        if print_info:
            print(f"Response: Timeout ({elapsed_time:.2f} seconds)")
        return "TIMEOUT"
    except dns.resolver.NoNameservers:
        if print_info:
            print("Response: SERVFAIL")
        return "SERVFAIL"
    except dns.resolver.NXDOMAIN:
        if print_info:
            print("Response: REFUSED")
        return "REFUSED"
    except Exception as e:
        if print_info:
            print(f"Response: {str(e)}")
        return "OTHER"

def main():
    domain = input("Enter the domain to query: ")
    dns_server = input("Enter the DNS server: ")
    num_queries = int(input("Enter the number of queries to run: "))
    print_info = True  # Set to True to print DNS request and response

    nxdomain_count = 0
    noerror_count = 0
    timeout_count = 0
    servfail_count = 0
    refused_count = 0
    other_count = 0

    timeouts_without_prompt = 0

    for i in range(num_queries):
        response = send_dns_query(domain, dns_server, print_info)

        if response == "NXDOMAIN":
            nxdomain_count += 1
        elif response == "NOERROR":
            noerror_count += 1
        elif response == "TIMEOUT":
            timeout_count += 1
            timeouts_without_prompt += 1

            if timeouts_without_prompt >= 4:
                continue_checking = input("The last 4 queries timed out. Do you want to continue checking? (y/n): ").lower()
                if continue_checking != 'y':
                    print("Checking aborted.")
                    break  # Exit the loop if the user doesn't want to continue

        elif response == "SERVFAIL":
            servfail_count += 1
        elif response == "REFUSED":
            refused_count += 1
        elif response == "OTHER":
            other_count += 1

    if timeouts_without_prompt > 4:
        print("Continuing checking...")

    print(f"\nNumber of NXDOMAIN responses: {nxdomain_count}")
    print(f"Number of NOERROR responses: {noerror_count}")
    print(f"Number of Timeout responses: {timeout_count}")
    print(f"Number of SERVFAIL responses: {servfail_count}")
    print(f"Number of REFUSED responses: {refused_count}")
    print(f"Number of Other responses: {other_count}")

if __name__ == "__main__":
    main()
