{~ html section,clazz=title ~}

{% title_slide 
    title=New Features,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com<br><a href='https://twitter.com/richard_d_jones'>@richard_d_jones</a> <a href='https://twitter.com/cottagelabs'>@cottagelabs</a>"
%}

{~ html /section ~}


{~ html section ~}

* Concurrency Control
* Metadata Formats
* Segmented File Upload
* By-Reference Deposit

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### Concurrency Control

Servers MAY implement Concurrency Control, to prevent clients from unintentionally overwriting data.

The Server provides the `ETag` header on every response, which contains a unique version number for the Object.

The client must then provide the `If-Match` header with every request to change data, which reflects the latest `ETag`

{~ html /section ~}

{~ html section ~}

Objects may change for a number of reasons after their initial creation, such as:

* Additional requests by the original depositing client to modify the Object
* Requests for modify by other clients with authorisation to modify the Object
* Modifications to the Object from agents on the server-side, such as administrators, etc.

{~ html /section ~}


{~ html section ~}

### Announcing Support for Concurrency Control.

Servers are not required to support Concurrency Control.

Clients MUST check response headers for the presence of an `ETag`. Presence of the `ETag` indicates that the server requires the client to 
pay attention to its concurrency control procedures, and to carry out later requests with an `If-Match` header.

{~ html /section ~}


{~ html section ~}

### Key Requirements

* An `ETag` MUST be provided for each SWORD resource: the Object, the Metadata, the FileSet and any Files.
* The client MUST send the `ETag` that it expects to represent the current version with every request to change the resource (POST, PUT, 
DELETE) by placing it in the `If-Match` header
* If the `ETag` supplied by the client in the `If-Match` header does not match the current `ETag` for the resource, the deposit will fail
* If a resource is modified, its `ETag` MUST change
* If a resource is modified, the `ETags` of all resources within which it is contained MUST change.

{~ html /section ~}

{~ html /section ~}



{~ html section ~}

{~ html section ~}

### Metadata Formats

SWORD allows the client to deposit arbitrary metadata onto the server through agnostic support for metadata formats

{~ html /section ~}


{~ html section ~}

### Announcing Support for Metadata Formats

The server can list Metadata formats that it will accept in the `acceptMetadata` field of the Service Document.

If no `acceptMetadata` field is present, the client MUST assume the server only supports the default SWORD metadata format 
(http://purl.org/net/sword/3.0/types/Metadata).

```json
{% json_extract
    source=examples/service-document.json,
    keys=acceptMetadata
%}
```

{~ html /section ~}


{~ html section ~}

### Indicating Metadata Format

During deposit, the client SHOULD specify a Metadata-Format header which contains the identifier for the format. For example, if supplying 
the default SWORD metadata format:

```
Metadata-Format: http://purl.org/net/sword/3.0/types/Metadata
```

If this header is not present the server MUST assume it has the above value.

{~ html /section ~}


{~ html section ~}

**Request/Response**

```
{% http_exchange
    source=schemas/openapi.json,
    method=post,
    url=/Service-URL,
    include_headers=Authorization|Content-Disposition|Content-Type|Digest|Metadata-Format,
    request_body=Metadata Document,
    header_values=Metadata-Format|http://purl.org/net/sword/3.0/types/Metadata|Content-Type|application/json,
    response=201
%}
```

{~ html /section ~}


{~ html section ~}

### Default Format

SWORD provides a default metadata format which MUST be supported by the server.

* It is serialised as JSON and with a JSON-LD `@context`

* It contains `dc` and `dcterms` vocabulary elements, and any other arbitrary elements added by the client

* It does not pre-suppose any particular profile of usage of these vocabulary elements.

{~ html /section ~}


{~ html section ~}

**Default Metadata Example**

```
{% include examples/metadata.json %}
```

{~ html /section ~}


{~ html section ~}

**Alternative Format Example**

```
POST Service-URL
Content-Type: application/xml
Content-Disposition: attachment; metadata=true
Digest: SHA-256=74b2851bd2760785b0987ba219debea69c228353f7ccc67a2bdcd9819f97fc71
Metadata-Format: http://www.loc.gov/mods/v3

<mods xmlns:mods="http://www.loc.gov/mods/v3">
  <originInfo>
    <place>
      <placeTerm type="code" authority="marccountry">nyu</placeTerm>
      <placeTerm type="text">Ithaca, NY</placeTerm>
    </place>
    <publisher>Cornell University Press</publisher>
    <copyrightDate>1999</copyrightDate>
  </originInfo>
</mods>
```

{~ html /section ~}

{~ html /section ~}



{~ html section ~}

{~ html section ~}

### Segmented File Upload

If a client has a very large file that it wishes to transfer to the server by value, then in may be beneficial to do this in several small 
operations, rather than as a single large operation.

In order to transfer a large file, the client can break it down into a number of equally sized segments of binary data (the final segment 
may be a different size to the rest). It can then initialise a Segmented File Upload with the server, and then transfer the segments. The 
server will reconstitute these segments into a single file, and then the client may deposit this file by-reference.

{~ html /section ~}


{~ html section ~}

### Announcing Support for Segmented File Upload

Servers MAY support Segmented File Upload.  To do so, it must provide a staging area where file segments can be uploaded prior to the client
requesting a specific deposit operation.  In the Service Document:

```json
{% json_extract
    source=examples/service-document.json,
    keys=staging|stagingMaxIdle
%}
```

{~ html /section ~}


{~ html section ~}

### Process for Segmented File Upload

1. Obtain the Staging-URL from the Service from which to request an Temporary-URL

2. Request a Temporary-URL from the Service, via a Segmented Upload Initialisation request.

3. Upload all the file segments to the Temporary-URL

4. Carry out the desired deposit operation as a By-Reference deposit, using the Temporary-URL as the by-reference file.


{~ html /section ~}


{~ html section ~}

### Segmented Upload Initialisation

```
{% http_exchange
    source=schemas/openapi.json,
    method=post,
    url=/Staging-URL,
    response=201
%}
```

{~ html /section ~}


{~ html section ~}

### Uploading File Segments

```
{% http_exchange
    source=schemas/openapi.json,
    method=post,
    url=/Temporary-URL,
    include_headers=Authorization|Content-Disposition|Content-Length|Content-Type|Digest,
    response=204
%}
```

{~ html /section ~}


{~ html section ~}

### Retrieving Information

At any point after creating a Temporary-URL, the client may request information on the state of their Segmented File Upload. This can be 
done via a GET to the Temporary-URL.

```
{% include examples/segmented-file-upload.json %}
```

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### By-Reference Deposit

By-Reference Deposit is when the client provides the server with URLs for Files which it would like the server to retrieve asynchronously.

This could be useful in a number of contexts, such as when the files are very large, and are stored on specialist staging hardware, or 
where the files are already readily available elsewhere.


{~ html /section ~}


{~ html section ~}

### Announcing Support

Servers MAY support By-Reference deposit.  If a server supports By-Reference it SHOULD indicate this in the Service Document 
using the field `byReferenceDeposit`:

```json
{% json_extract
    source=examples/service-document.json,
    keys=byReferenceDeposit
%}
```


{~ html /section ~}


{~ html section ~}

Clients may use a By-Reference Deposit anywhere a by-value deposit could be carried out. Instead of sending any Binary content, the client 
sends the By-Reference Document containing one or more (depending on context) URLs to files which the server can retrieve.

```
{% include examples/by-reference.json %}
```

{~ html /section ~}


{~ html section ~}

### Usage with Segemented File Upload

If carrying out a Segmented File Upload, the final deposit stage is to send the Temporary-URL to the server as part of a By-Reference 
deposit.

```json
{% include examples/segmented-file-upload_by-reference.json %}
```

{~ html /section ~}


{~ html section ~}

### Server-Side processing

1. The server receives a By-Reference Document with one or more files listed and creates records for each of these files that it plans to 
dereference. 

2. The server responds to the client with the appropriate response for the action

3. At its own pace the server obtains all the files that are marked for dereference. 

4. Once the Files are downloaded and processed, the server sets the file status appropriately in the Status Document

5. If there is an error in downloading or otherwise processing the file, the server sets the status to error and provides a 
meaningful log message.


{~ html /section ~}

{~ html /section ~}


{~ html section,clazz=title ~}

{% title_slide 
    title=Thanks for Listening,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com<br><a href='https://twitter.com/richard_d_jones'>@richard_d_jones</a> <a href='https://twitter.com/cottagelabs'>@cottagelabs</a>"
%}

{~ html /section ~}