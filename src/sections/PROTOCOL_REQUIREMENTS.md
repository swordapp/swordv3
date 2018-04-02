# Protocol Requirements

This section describes the requirements of every kind of operation that you can do with SWORDv3.

There are 3 key aspects of the specification where requirements can be applied, and these are:

1. **Request**: The CRUD operations that you can perform on the resources
2. **Content**: The body content of the request, such as Metadata, By-Reference, Metadata+ByReference, Binary File, Packaged Content, Empty Body
3. **Resource**: {% def urls,Service-URL %}, {% def urls,Object-URL %}, {% def urls,Metadata-URL %}, {% def urls,FileSet-URL %}, {% def urls,File-URL %}

When combined for a specific request.  For example: Creating (**Request**) a new Object by request to the Service-URL (**Resource**) 
with Packaged Content (**Content**), these aspects tell you the exact requirements.

The requirements below are presented using a hierarchy; for any given combination of **Request**, **Content** and **Resource**
all requirements above the relevant node should be imported when considering the actual requirements for an operation.  See the document
[SWORDv3 Behaviours]({% url swordv3-behaviours.html %}) to see each of the behaviours SWORDv3 is capable of with its requirements fully 
expanded.


## Requirement Hierarchies

The hierarchy for the Request is:

{% 
requirements_hierarchy
    source=tables/reqs_hierarchy.csv,
    key=Request
%}

The hierarchy for the Content is:

{% 
requirements_hierarchy
    source=tables/reqs_hierarchy.csv,
    key=Content
%}

The hierarchy for the Resource is:

{% 
requirements_hierarchy
    source=tables/reqs_hierarchy.csv,
    key=Resource
%}

So, for example, when considering an operation such as "Creating Objects with Packaged Content", this would be take requirements as follows:

* For the Request, as a Create, it takes requirements from **Create**, **Modify** and **\***
* For the Content, as Packaged Content, it takes requirements from **Packaged Content**, **Binary**, **Body** and **\***
* For the Resource, as an operation on the Service-URL, it takes requirements from **Service-URL** and **\***

## Requirement Groups

{%
requirements_table
    source=tables/requirements.csv,
    vectors=Request|Content|Resource,
    reqs=Protocol Operation|Request Requirements|Server Requirements|Response Requirements,
    header_level=3
%}

