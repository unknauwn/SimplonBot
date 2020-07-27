#Discord Simplon Bot
#Author: RAPHAEL.L
#Fabrique: Cannes 06
#Formation: Dev Data#1
#Language: Python
#GoogleQuery with Unique domain URL

try:
    from urllib.parse import urlparse
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def googleQuery(query, maxResults=5):
    uniqueDomainCheck = []
    results = ''
    for url in search(query, tld="com", lang="fr", stop=15):
        while len(uniqueDomainCheck) < maxResults and not any(urlparse(url).netloc in s for s in uniqueDomainCheck):
            results += (url+'\n')
            uniqueDomainCheck.append(url)
    return results
