from django.shortcuts import render
from .utils import get_client_ip, get_hostname


def index(request):
    remote_ip = get_client_ip(request)
    hostname = get_hostname(remote_ip)
    return render(request, 'myip/index.html', {'remote_ip': remote_ip, 'hostname': hostname})

