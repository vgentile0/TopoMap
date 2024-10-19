from scapy.layers.inet import traceroute

def trace_route(target):
    result, unanswered = traceroute(target)
    return result


"""
Alternative: 

from scapy.layers.inet import traceroute

def trace_route(target):
    result, unanswered = traceroute(target)
    return result
"""