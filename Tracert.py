from scapy.layers.inet import traceroute

def trace_route(target):
    result, unanswered = traceroute(target)
    return result

#trace = trace_route("8.8.8.8")
#print(trace)
