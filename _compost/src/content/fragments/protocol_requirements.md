# {{ header("Protocol Requirements") }}

This section describes the requirements of every kind of operation that you can do with SWORDv3.  Each section in 
{{ section_link("Requirement Groups") }} identifies which Request Conditions have what requirements.  To determine
the requirements for a specific request, identify each block below which is relevant to your request, and this will
provide the overall protocol requirements for that operation.

Converting the below into a set of requirements for a specific request is time consuming, so this has been done for
you in the **[SWORDv3 Behaviours Document]({{ url_for("swordv3-behaviours.html") }})**. If you are implementing a SWORD client
or server it is **STRONGLY RECOMMENDED** that you work from that document rather than the normalised requirements below.

There are 3 key aspects of the Request Conditions where requirements can be applied, and these are:

1. **Request**: The operation that you are performing on the resources
2. **Content**: The body content of the request, such as Metadata, By-Reference, Metadata+ByReference, Binary File, Packaged Content, Empty Body
3. **Resource**: {{ define("tables/urls", "Service-URL") }}, {{ define("tables/urls", "Object-URL") }}, {{ define("tables/urls", "Metadata-URL") }}, {{ define("tables/urls", "FileSet-URL") }}, {{ define("tables/urls", "File-URL") }}, {{ define("tables/urls", "Staging-URL") }}, {{ define("tables/urls", "Temporary-URL") }}

When combined for a specific request, these aspects tell you the exact requirements.  For example: Creating (**Request**) a new Object by request to the Service-URL (**Resource**) 
with Packaged Content (**Content**)

Each of these aspects of the Request Conditions are presented below according to a hierarchy. For a specific aspect,
you must import the requirements for it and all its parents in the hierarchy, to obtain all the requierements for the
request.

For each Request Condition, up to 4 kinds of requirement are present:

1. **Protocol Operation**: which of the protocol operations MUST be used for this request
2. **Request Requirements**: constraints applied to the client request
3. **Server Requirements**: constraints applied to how the server handles the request
4. **Response Requirements**: constraints applied to how the server responds to the request

See the document [SWORDv3 Behaviours]({{ url_for("swordv3-behaviours.html") }}) to see each of the behaviours SWORDv3 is 
capable of with its requirements fully expanded.


## {{ header("Requirement Hierarchies", 2) }}

The hierarchy for the Request is:

{{ 
requirements_hierarchy(
    source="tables/reqs_hierarchy",
    key="Request")
}}

The hierarchy for the Content is:

{{  
requirements_hierarchy(
    source="tables/reqs_hierarchy",
    key="Content")
}}

The hierarchy for the Resource is:

{{  
requirements_hierarchy(
    source="tables/reqs_hierarchy",
    key="Resource")
}}

So, for example, when considering an Request Condition such as "Creating Objects with Packaged Content", this would be take requirements as follows:

* For the Request, as a Create, it takes requirements from **Create**, **Modify** and **All**
* For the Content, as Packaged Content, it takes requirements from **Packaged Content**, **Binary**, **Body** and **All**
* For the Resource, as an operation on the Service-URL, it takes requirements from **Service-URL**, **Deposit** and **All**

## {{ header("Requirement Groups", 2) }}

<div class="requirement-groups">

{{ 
requirements_table_2(
    source="tables/requirements",
    vectors=["Request", "Content", "Resource"],
    reqs=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

</div>

