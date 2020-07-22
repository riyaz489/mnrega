import time
import socket
from subprocess import call

import hug
from tldextract import extract


@hug.sink('/')
def check_website(request, *args, **kwargs):
    print(f"Getting request for {request.url}")
    print("Add this to allow?")

    if input("[N]|y?").lower() in ("y", "yes"):
        call(["sudo", "allow", request.url])
        print("Giving time for new DNS rules to take affect...")
        time.sleep(5)
        extracted = extract(request.url)
        host = socket.gethostbyname(f"{extracted.domain}.{extracted.suffix}")
        hug.redirect.temporary(f"http://{host}/{request.path}")
