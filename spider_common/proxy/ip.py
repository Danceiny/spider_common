from parser_engine.patch import get_redis
from parser_engine.singleton import Singleton
import requests


@Singleton
class IP:
    def __init__(self, proxy_api_host, redis_params, **kwargs):
        self.host = proxy_api_host
        self.r = get_redis(**redis_params)

    def change(self, pname):
        get_ip_url = self.host + '/api/proxy/ip/' + pname
        complete_ip_url = self.host + '/api/complete/ip'
        register_ip_url = self.host + '/api/register/ip/' + pname
        response = requests.get(get_ip_url, headers={'Connection': 'close'})
        ip = ''
        if response.status_code == requests.codes.ok:
            ip = str(response.content, encoding="utf-8")

        current_ip = self.get(pname)
        if current_ip:
            current_ip = str(current_ip, encoding="utf-8")
        if not ip:
            if current_ip:
                ip = current_ip
            else:
                # 兜底 ip
                ip = '211.159.171.58:80'
            # 重新申请一批
            requests.get(register_ip_url, headers={'Connection': 'close'})
        else:
            if current_ip:
                requests.post(complete_ip_url, data={'pname': pname, 'ip': current_ip}, headers={'Connection': 'close'})
            self.r.set(pname + ':current_ip', ip)
        return ip

    def get(self, pname):
        return self.r.get(pname + ':current_ip')
