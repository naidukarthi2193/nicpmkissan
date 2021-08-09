# nicpmkissan

Download the Code from the Repository 

Open CMD

with IPCONIG note the Host IP Address

open the Repository Folder on CMD

execute the following command on CMD

```
python main.py --port 0.0.0.0
```

Open Apache Server Config  httpd.conf and add the following 

```
LoadModule proxy_module modules/mod_proxy.so  
LoadModule proxy_http_module modules/mod_proxy_http.so 
<VirtualHost *:80> 
ProxyRequests Off 
ProxyPass / http://IPADDRESS:8000/    
ProxyPassReverse / http://IPADDRESS:8000/   
</VirtualHost> 
```
Add the IPADDRESS to the Android App in Android Code
