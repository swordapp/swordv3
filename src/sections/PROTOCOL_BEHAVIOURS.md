# Protocol Behaviours

This section describes the requirements of every kind of operation that you can do with SWORDv3.

There are 3 key aspects of the specification where requirements can be applied, and these are:

1. The Request: Create, Append, Replace, Retrieve and Delete
2. The Content: Metadata, By-Reference, Metadata+ByReference, Binary File, Packaged Content, Empty Body
3. The Resource: {% def urls,Service-URL %}, {% def urls,Object-URL %}, {% def urls,Metadata-URL %}, {% def urls,FileSet-URL %}, {% def urls,File-URL %}

When combined for a specific request.  For example: Creating (**The Request**) a new Object by request to the Service-URL (**The Resource**) 
with Packaged Content (**The Content**), these aspects tell you the exact requirements.

For the most part, requirements depend on the Request and the Content, then there are additional specific requirements for how some of
the Resources behave on certain requests.  These are defined in the sections below.

The requirements below are presented using a hierarchy; for any given Request, Resource or Content and
all requirements above the relevant node should be imported when considering the actual requirements for an operation.  See the document
[SWORDv3 Behaviours]({% url spec/swordv3-behaviours.html %}) to see each of the behaviours SWORDv3 is capable of with its requirements fully 
expanded.


## The Request

The hierarchy for requests is as follows

```
All Requests
| - Retrieve
\ - Modify
    | - Create
    |   | - Create With Content
    |   \ - Create With Segment Upload Initialisation
    | - Update
    |   | - Append
    |   \ - Replace
    \ - Delete
        
```

Therefore, for example, an Append request imports all the requirements (where defined) from **Update**, **Modify** and **All Requests** in 
addition to its own.

### All Requests

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Modify Requests

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Modify Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Create Requests

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Create Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Create With Content

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Create With Content Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Create With Segment Upload Initialisation

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Create With Segment Upload Initialisation,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


### Update Requests

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Update Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


### Append Requests

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Append Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


### Delete Requests

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Delete Requests,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## The Content

The hierarchy for Content is as follows

```
All Content
| - Empty Body
\ - Has Body Content
    | - JSON
    |   | - Metadata
    |   | - By-Reference
    |   \ - Metadata + By Reference
    \ - Binary
        | - Binary File
        \ - Packaged Content
```

### Empty Body

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Empty Body,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Has Body Content

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Has Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Metadata

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Metadata Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### By-Reference

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=By-Reference Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Metadata + By-Reference

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Metadata + By-Reference Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Binary File

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Binary File Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Packaged Content

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Packaged Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## The Resource

The hierarchy for how rules apply to the resources is as follows:

```
All Resources
| - Service-URL
| - Object-URL
\ - Components
    | - Metadata-URL
    | - FileSet-URL
    \ - File-URL
```

### Service-URL

#### Retrieve

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Retrieve Service-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Object-URL

#### Retrieve

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Retrieve Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Update with Segmented Upload Initialisation

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Update Object-URL with Segmented Upload Initialisation,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

#### Update (except for Segmented Upload Initialisation)

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Update Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

#### Append

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

### Components

#### Retrieve

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Retrieve Components,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

#### Update

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Update Components,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

#### Replace

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Replace Components,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


### Metadata-URL

#### Retrieve

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Retrieve Metadata-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


### FileSet-URL

No additional requirements on working with the FileSet-URL


### File-URL

#### Retrieve

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=Retrieve File-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


