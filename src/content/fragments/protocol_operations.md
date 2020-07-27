# {{ header("Protocol Operations") }}

This section lists the actual on-the-wire protocol operations that are part of SWORDv3.  Actual usage of each of these operations is 
dependent on the action that you wish to take.  See {{ section_link("Protocol Requirements") }} for the rules which govern how to use these Protocol 
Operations.

The full set of protocol operations is available as an OpenAPI definition {{ ref("OpenAPI") }}, available as [JSON]({{ export_url("data/schemas/openapi.json") }})
and [YAML]({{ export_url("data/schemas/openapi_.yaml") }}).

## {{ header("Error Responses", 2) }}

The following error responses are possible against some or all of the HTTP Requests.  In each case an Error Document MUST be returned by the 
server with details as to the root cause of the error.

{{ 
openapi_list_descriptions(
    "schemas/openapi",
    field="components.responses",
    keys=["BadRequest", "Unauthorized", "Forbidden", "NotFound", "MethodNotAllowed", "Gone", "PreconditionFailed", "PayloadTooLarge", "UnsupportedMediaType"],
    expand_source="tables/error-types",
    expand_on="HTTP Name",
    expand_field="Error Type",
    expand_prefix=" (see Error Types: ",
    expand_suffix=")",
    expand_anchor=True,
    expand_anchor_prefix="error_"
    )
}}

## {{ header("Redirects", 2) }}

Some requests may result in redirect codes being sent to the client; the server MAY respond to any request with a suitable redirect.  These 
are the redirect codes that are used, and what they mean:

{{ 
openapi_list_descriptions(
    "schemas/openapi",
    field="components.responses",
    keys=["MovedPermanently", "TemporaryRedirect", "PermanentRedirect"]
    )
}}

## {{ header("HTTP Requests", 2) }}

These are the HTTP requests that are covered by the SWORD protocol.

Each request MAY be responded to by the server with a redirect code (see above).  Each request MAY also generate an error; possible errors 
are listed for each section, please refer to the section above for details on the meanings of errors.

{{ 
openapi_paths(
    "schemas/openapi",
    path_order=["Service-URL", "Object-URL", "Metadata-URL", "FileSet-URL", "File-URL", "Staging-URL", "Temporary-URL"],
    method_order=["get", "post", "put", "delete"],
    header_depth=3,
    omit=["301", "307", "308"],
    in_brief=["400", "401", "403", "404", "405", "410", "412", "413", "415"]
    )
}}
