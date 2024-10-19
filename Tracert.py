from scapy.layers.inet import traceroute

def trace_route(target):
    result, unanswered = traceroute(target)
    return result


"""
Alternativa: 

from scapy.layers.inet import traceroute

def trace_route(target):
    result, unanswered = traceroute(target)
    return result
"""