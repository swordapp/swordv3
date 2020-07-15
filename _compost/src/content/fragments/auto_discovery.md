# {{ header("Auto-Discovery") }}

In order to assist potential clients discover a server’s capabilities, SWORD RECOMMENDS the following auto-discovery features to be 
embedded in any web interfaces associated with the service provider.


## {{ header("For Services", 2) }}

Embed an html link with a rel value of `http://purl.org/net/sword/3.0/discovery/Service` in any page which represents
a deposit Service.

```
<html:link rel="http://purl.org/net/sword/3.0/discovery/Service" href="[Service-URL]"/>
```


## {{ header("For Objects", 2) }}

Embed an html link with a rel value of `http://purl.org/net/sword/3.0/discovery/Object` in any page which represents a deposited resource.

```
<html:link rel="http://purl.org/net/sword/3.0/discovery/Object" href="[Object-URL]"/>
```


## {{ header("Well-Known URI", 2) }}

For any server which wishes to expose its main or root Service-URL via Well-Known URIs {{ ref("RFC8615") }}, provide a
redirect (307) from `./well-known/swordv3` (PROVISIONAL) to your root Service-URL.