# {{ header("By-Reference Deposit") }}

By-Reference Deposit is when the client provides the server with URLs for Files which it would like the server to retrieve asynchronously 
to the deposit request itself.  This could be useful in a number of contexts, such as when the files are very large, and are stored on 
specialist staging hardware, or where the files are already readily available elsewhere, and there is no need to push them through a 
by-value deposit.

## {{ header("Announcing Support for By Reference Deposit", 2) }}

Servers MAY support By-Reference deposit.  If a server supports By-Reference it SHOULD indicate this in the {{ section_link("Service Document") }} 
using the field `byReferenceDeposit`:

```json
{{ json_extract(
    source="content/examples/service-document.json",
    keys="byReferenceDeposit")
}}
```


## {{ header("Options for By-Reference Deposit", 2) }}

Clients may use a By-Reference Deposit anywhere a by-value deposit could be carried out.  Instead of sending any Binary content, the 
client sends the {{ section_link("By-Reference Document") }} containing one or more (depending on context) URLs to files which the server can
retrieve.

See the document [SWORDv3 Behaviours]({{ url_for("swordv3-behaviours.html") }}) for an expansion of the {{ section_link("Protocol Requirements") }} for 
requests to deposit By-Reference.

The {{ section_link("Content Disposition") }} for a By-Reference deposit is:

```
{{ 
content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```

### {{ header("Usage with Segmented File Upload", 3) }}

If carrying out a {{ section_link("Segmented File Upload") }}, the final deposit stage is to send the {{ define("tables/urls","Temporary-URL") }} to the server 
as part of a By-Reference deposit.  In this case the client SHOULD omit the `ttl` and `dereference` fields from the
{{ section_link("By-Reference Document") }}, thus:

```json
{% include "examples/segmented-file-upload_by-reference.json" %}
```

The server MUST recognise one of its own Temporary-URLs, and should implement ingest in the most efficient way possible, remembering that
you cannot retrieve a copy of the actual Segmented File Upload from the Temporary-URL via GET, so the server MUST have a way to retrieve the content
from those uploads in another way.  The server MUST NOT delete the resource
until after it has been successfully ingested (i.e. the `stagingMaxIdle` time should be ignored when the server has received the resource
as a By-Reference deposit).

## {{ header("Server-Side Processing of By Reference Deposits", 2) }}

The following is the procedure that MUST be followed by servers implementing By-Reference deposit.

1. The server receives a {{ section_link("By-Reference Document") }} with one or more files listed

2. The server creates records for each of these files that it plans to dereference, which then become visible in the 
{{ section_link("Status Document") }}.  Files marked by the client not to be dereferenced are considered metadata, and MAY NOT appear in the Status 
Document.  All other supplied Files MUST have the status `pending` in the Status Document.

3. The server responds to the client with the appropriate response for the action (See {{ section_link("Protocol Operations") }} and {{ section_link("Protocol Requirements") }})

4. At its own pace, taking into account the `ttl` of the Files, the server obtains all the files that are marked for dereference and 
validates them against their Digest and any other supporting information such as `contentType`, `contentLength`, and `packaging`.  During 
the download the server SHOULD set the status to `downloading`.  The server SHOULD be able to resume an interrupted download.

5. Once the Files are downloaded and processed, the server MUST set the status to `ingested`.  If the Files need unpacking first, the 
server SHOULD first set the status to `unpacking` and then `ingested` when this operation is complete.  The server MUST also remove the 
`byReferenceDeposit` rel.

6. If there is an error in downloading or otherwise processing the file, the server MUST set the status to `error` and SHOULD provide a 
meaningful `log` message.

7. The server MAY continue to record the original URL of the file if desired.


### {{ header("Representation in the Status Document", 3) }}

While a By-Reference File is being processed, it MUST be represented in the {{ section_link("Status Document") }} under the `link` field.  The
following sections show how it is represented.

**On Initial Deposit**

```json
{{ json_extract(
    source="content/examples/by-reference_status_stages.json",
    selector="init")
}}
```

**During Download**

```json
{{ json_extract(
    source="content/examples/by-reference_status_stages.json",
    selector="downloading")
}}
```

**During Unpacking**

```json
{{ json_extract(
    source="content/examples/by-reference_status_stages.json",
    selector="unpacking")
}}
```

**After Completion**

```json
{{ json_extract(
    source="content/examples/by-reference_status_stages.json",
    selector="ingested")
}}
```

**In Case of Error**

```json
{{ json_extract(
    source="content/examples/by-reference_status_stages.json",
    selector="error")
}}
```

## {{ header("Responsibilities of the client/reference server", 2) }}

To provide deposit By-Reference, the reference server, where the file is initially hosted, SHOULD:

* Support resumable downloads
* Hold the file for sufficient time for the repository to retrieve it

To use By-Reference deposit, the client SHOULD:

* Follow up on the deposit to determine if the dereference of the file has been successful
* Be able to take suitable onward action if there is an error
