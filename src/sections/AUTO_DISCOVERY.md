# Auto-Discovery

In order to assist potential clients discover a server’s capabilities, SWORD RECOMMENDS the following auto-discovery features to be 
embedded in any web interfaces associated with the service provider.

##  For Services

Embed an html link with a rel value of http://purl.org/net/sword/3.0/discovery/Service

```
<html:link rel="http://purl.org/net/sword/3.0/discovery/Service" href="[Service-URL]"/>
```


##  For Objects

Embed an html link with a rel value of http://purl.org/net/sword/3.0/discovery/Object in any page which represents a deposited resource.

```
<html:link rel="http://purl.org/net/sword/3.0/discovery/Object" href="[Object-URL]"/>
```