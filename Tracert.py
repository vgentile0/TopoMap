from scapy.layers.inet import traceroute


def trace_route(target):
    # Perform traceroute and get the result and unanswered packets
    result, unanswered = traceroute(target)

    # Initialize a set to track unique IPs
    seen_ips = set()

    # Create an empty list to store the filtered result
    filtered_result = []

    # Iterate over the traceroute result
    for snd, rcv in result:
        # Check if the received IP address is already in the set of seen IPs
        if rcv.src not in seen_ips:
            # If it's a new IP, add it to the filtered result and the set
            filtered_result.append((snd, rcv))
            seen_ips.add(rcv.src)

    # Display traceroute hops in a format similar to original output
    for idx, (snd, rcv) in enumerate(filtered_result, start=1):
        print(f"{idx:<2} {rcv.src:<15} {rcv.sport}")

    return filtered_result

 # ADD DNS Resolver to allow input url instead of IP address to trace route