# Segmented File Upload

If a client has a very large file that it wishes to transfer to the server by value, then in may be beneficial to do this in several small 
operations, rather than as a single large operation.  Large uploads are at higher risk of failure, depending on a variety of factors, and 
there is no guarantee that a SWORD server will be able to resume a partial upload.

In order to transfer a large file, the client can break it down into a number of equally sized segments of binary data (the final segment 
may be a different size to the rest).  It can then initialise a Segmented File Upload with the server, and then transfer the segments.  The 
server will reconstitute these segments into a single file, and then the client may deposit this file by-reference.

Segments can be uploaded in any order, and can be uploaded one at a time or in parallel.


## Announcing Support for Segmented File Upload

Servers MAY support Segmented File Upload.  To do so, it must provide a staging area where file segments can be uploaded prior to the client
requesting a specific deposit operation.  The server MUST include a `staging` field in the {% link Service Document %} with a URL for where
the client can initialise its Segmented File Upload.  It SHOULD also specify how long it will retain an unfinished Segmented Upload, before 
assuming that the client will not complete it, with the `stagingMaxIdle` field:

```json
{% json_extract
    source=examples/service-document.json,
    keys=staging|stagingMaxIdle
%}
```


## Outline of Process for Segmented File Upload

1. Obtain the {% def urls,Staging-URL %} from the Service from which to request an {% def urls,Temporary-URL %}

    If the client is creating a new Object, the Staging-URL can be found in the `staging` field in the {% link Service Document %}.  If an Object
    already exists, the client should find the Service-URL from the `service` field in the {% link Status Document %}, then GET this URL
    to obtain the appropriate {% link Service Document %}, and subsequently get the Staging-URL from the `staging` field.

2. Request a {% def urls,Temporary-URL %} from the Service, via a **Segmented Upload Initialisation** request.

    Send a POST request to the Staging-URL, as per {% link POST Staging-URL %}, with the appropriate `Content-Disposition` (see below).  The
    server will respond with a Temporary-URL in the `Location` header.

3. Upload all the file segments to the {% def urls,Temporary-URL %}

    Send one or more POST requests to the Temporary-URL as per {% link POST Temporary-URL %}, with the appropriate `Content-Disposition` (see 
    below), until all file segments have been uploaded.

4. Carry out the desired deposit operation as a By-Reference deposit, using the Temporary-URL as the by-reference file.

    Refer to the section [By-Reference Deposit] for more information on this approach.  Deposits of content hosted at Temporary-URLs SHOULD NOT
    contain the `ttl` or `dereference` fields in the By-Reference Document, and if they are included, the server MUST ignore them.


## Segmented Upload Initialisation

Before sending any segments to the server, the client must initialise the process.  This is done by sending a POST request to the
Staging-URL as per {% link POST Staging-URL %}.

The requirements of the protocol for a Segment Upload Initialisation are:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

See the section {% link Content Disposition %} for detailed information on the `Content-Disposition` header.  Based on that section, the
supplied `Content-Disposition` would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

The server MAY choose to reject the Segmented Upload Initialisation request at this stage, for a variety of reasons - for example, it may 
have a limit on the total number of segments it will accept, or the total size may exceed a maximum file size for assembled files.  In 
these cases, the server MUST respond with one of the appropriate {% link Error Types %}.

If the request is successful, the server will respond with a Temporary-URL in the `Location` header, and the segments themselves can be
uploaded to that URL.


## Uploading File Segments

Segments may be uploaded in any order and may also be parallelised.  Segments MUST all be the same size, with the exception of the final 
segment with MUST be the same size or smaller than the other segments.  Segments size MUST be smaller than the `maxUploadSize` specified in 
the {% link Service Document %}.

The requirements of the protocol for File Segment Upload are:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|File Segment|Temporary-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

See the section {% link Content Disposition %} for detailed information on the `Content-Disposition` header.  Based on that section, the
supplied `Content-Disposition` would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=File Segment Upload|File Segment
%}
```


## Retrieving Information about a Segmented File Upload

At any point after creating a Temporary-URL, the client may request information on the state of their Segmented File Upload.  This can
be done via a GET to the Temporary-URL.


## Aborting an Upload

If, part way through a segmented upload (even after completion) the client wishes to abort, it can send an DELETE request to the 
Temporary-URL, with the following requirements:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Delete|Empty Body|Temporary-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Incomplete Upload Retention

Servers MAY delete incomplete Segmented File Uploads after a specified amount of time (in the Service Document), if they are not 
finalised with all segments.


## Errors

Servers MUST respond with Error documents under the following circumstances (in addition to the standard errors that may arise through using
the protocol):

* More bytes have been sent than indicated in the total_size field
* A request is sent after the total_size has been reached
* A request is sent after the segment_count has been reached.
* A segment is recieved which is not the final segment and is not the same as the expected file size
* A segment is received which is the final segment which is larger than the other segment sizes

The server MAY respond with an Error document under the following circumstances:

* The Temporary-URL has timed out, and the server will no longer receive updates to it

If any other errors occur asynchronously, such as in reassembling or unpacking the resulting file, servers MUST provide an error `status` 
field and suitable `log` information in the link record in the Status document.
