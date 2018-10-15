import socket

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_hostname(remote_ip):
    try:
        hostname = socket.gethostbyaddr(remote_ip)[0]
    except:
        hostname = ''
    
    return hostname
