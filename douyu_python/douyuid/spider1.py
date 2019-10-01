import urllib.request

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
request = urllib.request.Request("https://www.douyu.com/gapi/rkc/directory/0_0/2", headers=headers)
response = urllib.request.urlopen(request)
doc = response.read().decode('utf-8')
print(doc)
