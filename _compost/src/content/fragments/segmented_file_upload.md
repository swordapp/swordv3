# {{ header("Segmented File Upload") }}

If a client has a very large file that it wishes to transfer to the server by value, then in may be beneficial to do this in several small 
operations, rather than as a single large operation.  Large uploads are at higher risk of failure, depending on a variety of factors, and 
there is no guarantee that a SWORD server will be able to resume a partial upload.

In order to transfer a large file, the client can break it down into a number of equally sized segments of binary data (the final segment 
may be a different size to the rest).  It can then initialise a Segmented File Upload with the server, and then transfer the segments.  The 
server will reconstitute these segments into a single file, and then the client may deposit this file by-reference.

Segments can be uploaded in any order, and can be uploaded one at a time or in parallel.


## {{ header("Announcing Support for Segmented File Upload", 2) }}

Servers MAY support Segmented File Upload.  To do so, it must provide a staging area where file segments can be uploaded prior to the client
requesting a specific deposit operation.  The server MUST include a `staging` field in the {{  section_link("Service Document") }} with a URL for where
the client can initialise its Segmented File Upload.  It SHOULD also specify how long it will retain an unfinished Segmented File Upload, before 
assuming that the client will not complete it, with the `stagingMaxIdle` field.  In addition, the server SHOULD specify the size
parameters of the segments using `maxSegmentSize`, `minSegmentSize`, `maxAssembledSize` and `maxSegments`:

```json
{{ json_extract("content/examples/service-document.json", 
    ["staging", "stagingMaxIdle", "maxSegmentSize", "minSegmentSize", "maxAssembledSize", "maxSegments"]) }}
```


## {{ header("Outline of Process for Segmented File Upload", 2) }}

1. Obtain the {{ define("tables/urls", "Staging-URL") }} from the Service from which to request an {{ define("tables/urls", "Temporary-URL") }}

    If the client is creating a new Object, the Staging-URL can be found in the `staging` field in the {{  section_link("Service Document") }}.  If an Object
    already exists, the client should find the Service-URL from the `service` field in the {{  section_link("Service Document") }}, then GET this URL
    to obtain the appropriate {{  section_link("Service Document") }}, and subsequently get the Staging-URL from the `staging` field.

2. Request a {{ define("tables/urls", "Temporary-URL") }} from the Service, via a {{  section_link("Segmented Upload Initialisation") }} request.

    Send a POST request to the Staging-URL, as per {{  section_link("POST Staging-URL") }}, with the appropriate `Content-Disposition` (see below).  The
    server will respond with a Temporary-URL in the `Location` header.

3. Upload all the file segments to the {{ define("tables/urls", "Temporary-URL") }}

    Send one or more POST requests to the Temporary-URL as per {{  section_link("POST Temporary-URL") }}, with the appropriate `Content-Disposition` (see 
    below), until all file segments have been uploaded.

4. Carry out the desired deposit operation as a By-Reference deposit, using the Temporary-URL as the by-reference file.

    Refer to the section {{  section_link("By-Reference Deposit") }} for more information on this approach.  Deposits of content hosted at Temporary-URLs SHOULD NOT
    contain the `ttl` or `dereference` fields in the By-Reference Document, and if they are included, the server MUST ignore them.


## {{ header("Segmented Upload Initialisation", 2) }}

Before sending any segments to the server, the client must initialise the process.  This is done by sending a POST request to the
Staging-URL as per {{  section_link("POST Staging-URL") }}.

The requirements of the protocol for a Segment Upload Initialisation are:

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

See the section {{  section_link("Content Disposition") }} for detailed information on the `Content-Disposition` header.  Based on that section, the
supplied `Content-Disposition` would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

The server MAY choose to reject the Segmented Upload Initialisation request at this stage, for a variety of reasons - for example, it may 
have a limit on the total number of segments it will accept, or the total size may exceed a maximum file size for assembled files.  In 
these cases, the server MUST respond with one of the appropriate {{  section_link("Error Types") }}.

If the request is successful, the server will respond with a Temporary-URL in the `Location` header, and the segments themselves can be
uploaded to that URL.


## {{ header("Uploading File Segments", 2) }}

Segments may be uploaded in any order and may also be parallelised.  Segments MUST all be the same size, with the exception of the final 
segment with MUST be the same size or smaller than the other segments.  Segments size MUST be smaller than the `maxSegmentSize` if specified
and if not then smaller than `maxUploadSize` specified in the {{ section_link("Service Document") }}. Segments MUST be larger than the `minSegmentSize`
also specified in the {{ section_link("Service Document") }}.

The requirements of the protocol for File Segment Upload are:

{{ 
requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "File Segment", "Temporary-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements", "Error Responses"])
}}

See the section {{  section_link("Content Disposition") }} for detailed information on the `Content-Disposition` header.  Based on that section, the
supplied `Content-Disposition` would be:

```
{{ 
content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["File Segment Upload", "File Segment"])
}}
```

The `Content-Type` header MUST just be `application/octet-stream`.

The `Digest` header MUST contain the Digest for the File Segment itself, so the server can confirm successful transfer of the segment.


## {{ header("Retrieving Information about a Segmented File Upload", 2) }}

At any point after creating a Temporary-URL, the client may request information on the state of their Segmented File Upload.  This can
be done via a GET to the Temporary-URL.

This will return you a document as described in {{  section_link("Segmented File Upload Document") }}.

The requirements for this operation are:

{{ 
requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Retrieve", "Empty Body", "Temporary-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements", "Error Responses"])
}}


**NOTE** that you cannot retrieve an actual copy of the full or partially uploaded Segmented File Upload from the Temporary-URL at any point.


## {{ header("Aborting an Upload", 2) }}

If, part way through a segmented upload (even after completion) the client wishes to abort, it can send an DELETE request to the 
Temporary-URL, with the following requirements:

{{ 
requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Delete", "Empty Body", "Temporary-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements", "Error Responses"])
}}

If a client submits the Temporary-URL as a By-Reference deposit to the server after completing the upload, the client SHOULD NOT delete
the Temporary-URL themselves, the server SHOULD take responsibility for this.  If the client deletes the resource before the By-Reference
deposit has completed, the server SHOULD record an error against the ingest.

## {{ header("Incomplete Upload Retention", 2) }}

Servers SHOULD delete incomplete Segmented File Uploads after a specified amount of time (in the Service Document), if they are not 
finalised with all segments.


## {{ header("Completed Upload Retention", 2) }}

Servers SHOULD delete completed Segmented File Uploads after a specified amount of time (in the Service Document).  Servers MUST be able to
tell when they have been given one of their own Temporary-URLs as a By-Reference deposit, and not delete that resource until after it has
been ingested.


## {{ header("Errors", 2) }}

Servers MUST respond with Error documents under the following circumstances (in addition to the standard errors that may arise through using
the protocol):

* An initialisation request is sent which specifies a total size larger than that allowed by the server (MaxAssembledSizeExceeded)
* An initialisation request is sent which specifies a segment size larger than that allowed by the server (MaxUploadSizeExceeded)
* An initialisation request is sent which specifies a segment size smaller than that allowed by the server (InvalidSegmentSize)
* An initialisation request is sent which specifies a segment count larger than that allowed by the server (SegmentLimitExceeded)
* An upload request is sent after the total_size has been reached (MethodNotAllowed)
* An upload request is sent after the segment_count has been reached (MethodNotAllowed)
* A segment is received which is not the final segment and is not the same as the expected file size (InvalidSegmentSize)
* A segment is received which is the final segment which is larger than the other segment sizes (InvalidSegmentSize)
* A segment is received which is larger than that allowed by the server (InvalidSegmentSize)
* A segment is received which is smaller than that allowed by the server (InvalidSegmentSize)
* A segment number is received which is not in the allowed range (SegmentLimitExceeded)

The server MAY respond with an Error document under the following circumstances:

* The Temporary-URL has timed out, and the server will no longer receive updates to it (SegmentedUploadTimedOut)

If any other errors occur asynchronously, such as in reassembling or unpacking the resulting file, servers MUST provide an error `status` 
field and suitable `log` information in the link record in the Status document.
