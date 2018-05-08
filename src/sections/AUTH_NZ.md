#  Authentication and Authorisation

It is strongly RECOMMENDED that SWORD servers support authentication and authorisation for requests.

SWORD servers are not restricted in the forms of authentication that they employ, and there is no minimum requirement or default supported 
approach.


##  Announcing Support for Authentication Schemes

Servers SHOULD enumerate the authentication schemes that they support in the Service Document, in the field `authentication`, and MUST draw 
from the IANA registry of HTTP auth scheme names {% ref IANA Auth %} where one is available.

Where an authentication scheme is in use by the server which is not covered by the IANA registry - such as a custom API-token-based 
approach, the server MAY indicate this in whatever way seems most appropriate.

For example, a Server which supports Basic, Digest and OAuth authentication, as well as a custom API-Key approach could indicate as follows:

```json
{% json_extract
    source=examples/service-document.json,
    keys=authentication
%}
```

Servers MAY also choose to support On-Behalf-Of deposit, which means that the authenticating user is providing content to the server, as 
if another user were actually carrying out this request.  A use case for this would be when a known third-party deposit tool is sending 
content to a server and has been authorised by another user to add content on their behalf.

If a server supports On-Behalf-Of deposit, it SHOULD indicate this in the Service Document with the field `onBehalfOf` set to `true`. 
If this field is not present clients MUST assume that the server does not support On-Behalf-Of deposit.

```json
{% json_extract
    source=examples/service-document.json,
    keys=onBehalfOf
%}
```


##  Authentication and Authorisation in requests

When carrying out authenticated requests, Authorization headers MUST be sent with every request to the server - the server is not 
responsible for maintaining state for the client.  The server is responsible for authenticating and authorising every request individually. 
Clients may choose also to send `Cookie` headers, and servers may support these, but support for Cookies is explicitly outside this 
specification.

When an On-Behalf-Of deposit is received, the server MUST ensure that the user identified in that header is valid with respect to the 
associated Authorization header.  For example, when using OAuth2, the On-Behalf-Of user MUST match the user for which the token in the 
Authorization header was granted.


##  Recording Depositing Users

In all cases (On-Behalf-Of or not) where a user has authenticated to make a deposit, servers SHOULD preserve the user's identity in the 
`depositedBy` property of the Original Deposit in the Status document. In On-Behalf-Of deposit, the value given in the `On-Behalf-Of` 
header SHOULD be used for the value of the `depositedOnBehalfOf` property of the Original Deposit in the Status document.

Note that recording a user's identity in this way does not have to contain enough information for the client to directly identify the
user, and implementers should take note of privacy legislation when choosing what information to expose in these fields.
