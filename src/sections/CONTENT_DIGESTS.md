# Content Digests

In order to ensure that the content transmitted via SWORD is correct when it arrives at its destination, clients MUST provide Digests that 
servers MUST check against incoming content.

## Announcing Support For Digests

Servers can announce support for the Digest formats that they support in the Service Document as follows:

```json
{% json_extract
    source=examples/service-document.json,
    keys=digest
%}
```

The Server SHOULD list all the digest formats that it supports.  Servers MUST support at least SHA-256 and MAY support any other digest 
formats.

The Digest formats MUST be identified as per the IANA HTTP Digest Algorithm values: {% ref IANA Digest %}


## Transmitting Digests

SWORD uses the recommendations of {%ref RFC3230 %} for transmitting base64 encoded Digests of request bodies.

For every request where there is a request body, the client MUST attach the `Digest` header with the appropriate content:

````
Digest: SHA-256=MzA1ZmIzMDJiZjA4MzUzYTg5ZGY4NDIxMjcyY2JmZTEwNzM5ODdmMjJhY2Y1ZDc5NzFhOTY3MmM1MGNkN2ZlMA==
````

Note that the client MAY send multiple digests from different algorithms, separated by commas in the header:

````
Digest: SHA-256=MzA1ZmIzMDJiZjA4MzUzYTg5ZGY4NDIxMjcyY2JmZTEwNzM5ODdmMjJhY2Y1ZDc5NzFhOTY3MmM1MGNkN2ZlMA==, MD5=ZjQxNjA3N2M3MDdhODJkZGJlMGE0YTk2NGRjZWEyNWE=
````

The server MUST validate at least one digest, SHOULD validate all digests, though MAY choose its preferred format to validate against.
