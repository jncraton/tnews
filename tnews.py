import requests
import re

from time import perf_counter
start = perf_counter()

DEBUG = False

def log(msg):
    if DEBUG:
        print(f"{perf_counter() - start} {msg}")

def get_npr_articles():
    res = requests.get("https://text.npr.org/")
    log("Loaded NPR article list")

    html = res.text
    
    lis = re.findall(r'<li>.*?href="(.*?)".*?>(.*?)</a></li>', html)
    
    return [li for li in lis if li[0].startswith("/nx")]

def get_npr_text(url):
    """
    >>> get_npr_text("/nx-s1-5218580")
    
    """
    html = requests.get("https://text.npr.org" + url).text
    log(f"Loaded NPR article content {url}")
    
    # Remove segments of HTML we aren't interested in    
    for t in ["style", "script", "nav", "header", "footer"]:
        html = re.sub(f"<{t}>.*?</{t}>", "", html, flags=re.DOTALL|re.M)
    
    # Prepend headers with `#` for markdown
    html = re.sub("<h1.*?>", r"<h1># ", html)
    html = re.sub("<h2.*?>", r"<h2>## ", html)
    
    # Grab all paras (and headers)
    paras = re.findall(r"(<p>|<h\d.*?>)(.*?)(</p>|</h\d>)", html)
    
    text = '\n\n'.join(re.sub("<.*?>", "", p[1]) for p in paras)
    log(f"Extracted article text")
    
    return text

articles = get_npr_articles()

for url, title in articles:
    print(get_npr_text(url))
    print("\n\n" + "-" * 80 + "\n\n")
    