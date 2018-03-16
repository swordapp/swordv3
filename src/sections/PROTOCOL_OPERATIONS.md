# Protocol Operations

This section lists the actual on-the-wire protocol operations that are part of SWORDv3.  Actual usage of each of these operations is 
dependent on the action that you wish to take.  See [Protocol Behaviours] for the rules which govern how to use these Protocol Operations.

The full set of protocol operations is available as an OpenAPI definition {% ref OpenAPI %}, available as [JSON]({% url spec/openapi.json%})
and [YAML]({% url spec/openapi.yaml %}).

## Error Responses

The following error responses are possible against some or all of the HTTP Requests.  In each case an Error Document MUST be returned by the 
server with details as to the root cause of the error.

{% 
openapi_list_descriptions
    schemas/openapi.json,
    field=components.responses,
    keys=BadRequest|Unauthorized|Forbidden|NotFound|MethodNotAllowed|Conflict|PreconditionFailed|PayloadTooLarge|UnsupportedMediaType
%}

## Redirects

Some requests may result in redirect codes being sent to the client; the server MAY respond to any request with a suitable redirect.  These 
are the redirect codes that are used, and what they mean:

{%
openapi_list_descriptions
    schemas/openapi.json,
    field=components.responses,
    keys=MovedPermanently|TemporaryRedirect|PermanentRedirect
%}

## HTTP Requests

These are the HTTP requests that are covered by the SWORD protocol.  Each one is listed on the left with the HTTP method, the URL against 
which it can be executed, and any headers that are permitted (requirements for headers are covered in later sections), as well as a list of 
possible Body contents.  On the right is the set of possible successful responses from the server, with the HTTP status code, any headers 
that may be included, and the Body content.

Each request MAY be responded to by the server with a redirect code (see above).  Each request MAY also generate an error; possible errors 
are listed for each section, please refer to the section above for details on the meanings of errors.

{%
openapi_paths
    schemas/openapi.json,
    path_order=Service-URL|Object-URL,
    method_order=get|post|put|delete,
    header_depth=3
%}
