{~ html section,clazz=title ~}

{% title_slide 
    title=Overview of SWORD&nbsp;3,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com"
%}

{~ html /section ~}


{~ html section ~}

SWORD 3.0 is a protocol enabling clients and servers to communicate around complex digital objects

Complex digital objects consist of both Metadata and File content, where the Files may be in a variety of formats, there may be many files, 
and some may be very large.  

It defines semantics for creating, appending, replacing, deleting, and retrieving information about these complex resources.  

It also enables servers to communicate regarding the status of treatment of deposited content, such as exposing ingest workflow information.

{~ html /section ~}


{~ html section ~}

{% fig structure.png,SWORD Object Structure %}

{~ html /section ~}


{~ html section ~}

### Document Types

{% dl tables/documents.csv,term=Name,definition=Description,size=5 %} 

{~ html /section ~}


{~ html section ~}

### Document Types

{% dl tables/documents.csv,term=Name,definition=Description,size=5,offset=5 %} 

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### Basic Workflow

**Retrieve a Service Document**

```
{% http_exchange
    source=schemas/openapi.json,
    method=get,
    url=/Service-URL,
    response=200
%}
```
    
{~ html /section ~}
    
{~ html section ~}

```
{% include examples/service-document.json %} 
```

{~ html /section ~}

{~ html section ~}

**Create a new Object**

```
{% http_exchange
    source=schemas/openapi.json,
    method=post,
    url=/Service-URL,
    response=201,
    include_headers=Authorization|On-Behalf-Of|Content-Disposition|Digest|Packaging
%}
```

{~ html /section ~}

{~ html section ~}

**Retrieve Status Document**

```
{% http_exchange
    source=schemas/openapi.json,
    method=get,
    url=/Object-URL,
    response=200
%}
```

{~ html /section ~}

{~ html section ~}

```
{% include examples/status.json %} 
```

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

## Key Features

{~ html /section ~}


{~ html section ~}

### Concurrency Control

Servers MAY implement Concurrency Control, to prevent clients from unintentionally overwriting data.

The Server provides the `ETag` header on every response, which contains a unique version number for the Object.

The client must then provide the `If-Match` header with every request to change data, which reflects the latest `ETag`

{~ html /section ~}


{~ html section ~}

### Continued Deposit

Clients can indicate to a server that there is more content coming, and the item shouldn't be injected into any post-submission
workflows by providing the `In-Progress` header.

{~ html /section ~}


{~ html section ~}

### Metadata Deposit

SWORD allows the client to deposit arbitrary metadata onto the server through agnostic support for metadata formats.

SWORD has a default format which MUST be supported by the server, which consists of the set of DCMI Terms expressed as JSON

During deposit, the client specifies a `Metadata-Format` header which contains the identifier for the format.

{~ html /section ~}


{~ html section ~}

### Package Deposit

SWORD allows you to deposit both Files and Metadata simultaneously through support of Packaged Content.

When depositing Packaged Content, the client indicates information about the format using the `Packaging` header.

{~ html /section ~}


{~ html section ~}

### Segmented File Upload

If a client has a very large file that it wishes to transfer to the server by value, then in may be beneficial to do this in several small 
operations, rather than as a single large operation.

In order to transfer a large file, the client can break it down into a number of equally sized segments of binary data (the final segment 
may be a different size to the rest).  It can then initialise a Segmented File Upload with the server, and then transfer the segments.  The 
server will reconstitute these segments into a single file, and then the client may deposit this file by-reference.

{~ html /section ~}


{~ html section ~}

### By-Reference Deposit

By-Reference Deposit is when the client provides the server with URLs for Files which it would like the server to retrieve asynchronously 
to the deposit request itself.  

This could be useful in a number of contexts, such as when the files are very large and are stored on 
specialist staging hardware, or where the files are already readily available elsewhere.

{~ html /section ~}


{~ html section,clazz=title ~}

{% title_slide 
    title=Thanks for Listening,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com"
%}

{~ html /section ~}