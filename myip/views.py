from django.shortcuts import render
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


def index(request):
    remote_ip = get_client_ip(request)
    hostname = get_hostname(remote_ip)
    return render(request, 'myip/index.html', {'remote_ip': remote_ip, 'hostname': hostname})

