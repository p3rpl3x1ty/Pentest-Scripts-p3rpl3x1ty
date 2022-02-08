import requests
import threading
import concurrent.futures

appendLock = threading.Lock() #Stops multiple threads from appending to the list at the same time.

workers = 10 #Number of threads. More than 30 may cause problems.

#proxy_list = ['ip:port', 'ip:port', ...etc]
proxy_list = ['51.210.104.79:80', '34.203.142.175:80','34.229.55.246:80','35.175.242.158:3128','68.183.192.29:8080']

results = []
def proxyCheck(proxy):
    try:
        r = requests.get('http://www.httpbin.org/ip', proxies={'https':proxy}, timeout=5)
        with appendLock:
            results.append(proxy)
    except:
        print('boobs')

with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
    for proxy in proxy_list:
        executor.submit(proxyCheck(proxy))

print(results)
