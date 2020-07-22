# {{ header("Documents") }}

## {{ header("JSON-LD Context", 2) }}

SWORD defines the semantics of its documents using JSON-LD {{ ref("JSON-LD") }}.  You can see the full JSON-LD Context 
[here]({{ export_url("data/schemas/swordv3.jsonld") }})


## {{ header("Service Document", 2) }}

The Service Document defines the capabilities and operational parameters of the server as a whole, or of a particular Service-URL.

The Service Document consists of a set of properties at the root, and a list of "services".  Each service may define a Service-URL 
and/or additional properties and further nested "services".  For the purposes of normalising the data held in the Service Document (for 
brevity of the serialised document), the Service Document MAY specify at the root properties which MUST be taken to hold true for all 
nested "services" (at any level below) unless that lower service definition overrides the properties.  A service which sits beneath the root of 
the Service Document and above another Service, MAY also redefine properties, and those overrides MUST be considered to cascade down to 
Services beneath that one.

A Service Document can be retrieved either for the root of the service, or from any Service within the hierarchy of Services available. 
If the root Service Document is requested, the full list of Services, including all their children, MUST be provided.  If the URL of a 
Service is requested, it MUST only provide information about itself and its children.

The full JSON Schema {{ ref("JSON-SCHEMA") }} can be downloaded [here]({{ export_url("data/schemas/service-document.schema.json") }}).

An example of the Service Document:

```json
{% include "examples/service-document.json" %}
```

The fields available are defined as follows:

{{ json_schema_definitions("schemas/service-document.schema") }}


## {{ header("Metadata Document", 2) }}

The default SWORD Metadata document allows the deposit of a standard, basic metadata document constructed using the DCMI terms {{ ref("DCMI") }}.  This 
Metadata document can be sent when creating an Object initially, when appending to the metadata, or in replacing the metadata or indeed the 
Object as a whole.

The format of the document is simple and extensible (see the {{ section_link("Metadata Formats") }} section).  The `dc` and `dcterms` vocabularies are supported, 
and servers MUST support this metadata format.

The full JSON Schema {{ ref("JSON-SCHEMA") }} can be downloaded [here]({{ export_url("data/schemas/metadata.schema.json") }}).

An example of the Metadata Document:

```json
{% include "examples/metadata.json" %}
```

The fields available are defined as follows:

{{ json_schema_definitions("schemas/metadata.schema") }}


When sending this document, the client MUST provide a `Content-Disposition` header of the form:

```
Content-Disposition: attachment; metadata=true
```

Additionally, when sending this document the client SHOULD provide the `Metadata-Format` header with the identifier 
for the format: http://purl.org/net/sword/3.0/types/Metadata

```
Metadata-Format: http://purl.org/net/sword/3.0/types/Metadata
```

If the client omits the `Metadata-Format` header, the server MUST assume that it is the above format.


## {{ header("By-Reference Document", 2) }}

The By-Reference document allows the client to send a list of one or more files that the server will fetch asynchronously.  The 
By-Reference document can be sent when creating an Object initially, or when appending to or replacing the FileSet in the Object, or 
replacing the Object as a whole.

The full JSON Schema {{ ref("JSON-SCHEMA") }} can be downloaded [here]({{ export_url("data/schemas/by-reference.schema.json") }}).

An example of the By-Reference Document:

```json
{% include "examples/by-reference.json" %}
```

The fields available are defined as follows:

{{ json_schema_definitions("schemas/by-reference.schema") }}

When sending this document, the client MUST provide a `Content-Disposition` header of the form:

```
Content-Disposition: attachment; by-reference=true
```


## {{ header("Metadata + By-Reference Document", 2) }}

In the event that the client wishes to send both Metadata and By-Reference content to the server, this is possible in
the event that the Metadata format is expressed as JSON, such as the default SWORD metadata format.

If the client wishes to send a metadata format that is not or cannot be expressed as JSON, this operation is not available,
it is provided only as a convenience.  In that case, a separate {{ section_link("Metadata Deposit") }} and {{ section_link("By-Reference Deposit") }}
should be carried out.

To do this, the client may include the Metadata and By-Reference documents embedded in a single JSON document, structured as shown below. 
The entire Metadata document (including its JSON-LD `@context` when using the default format) is embedded in a field 
entitled `metadata`, and the entire By-Reference document (again, with its JSON-LD `@context`) is embedded in a field entitled `by-reference`.

When a document of this form is sent, the client MUST set the `Content-Disposition` header appropriately, to alert the server of its 
required behaviour.

An example of the Metadata + By-Reference Document:

```json
{% include "examples/metadata+by-reference.json" %}
```

When sending this document, the client MUST provide a `Content-Disposition` header of the form:

```
Content-Disposition: attachment; metadata=true; by-reference=true
```

Additionally, when sending this document the client SHOULD provide the `Metadata-Format` header with the identifier for the format: 

```
Metadata-Format: http://purl.org/net/sword/3.0/types/Metadata
```

If the client omits the `Metadata-Format` header, the server MUST assume that it is the default format: http://purl.org/net/sword/3.0/types/Metadata


## {{ header("Status Document", 2) }}

The status document is provided in response to a deposit operation on a Service-URL, and can be retrieved at any subsequent point by a
GET on the Object-URL, and is returned each time the client takes action on the Object-URL.  It tells the client detailed information about 
the content and current state of the item.

The full JSON Schema {{ ref("JSON-SCHEMA") }} can be downloaded [here]({{ export_url("data/schemas/status.schema.json") }}).

An example of the Status Document:

```json
{% include "examples/status.json" %}
```

The fields available are defined as follows:

{{ json_schema_definitions("schemas/status.schema") }}


### {{ header("Available `rel` types and their meanings", 3) }}

{{ 
sections(
    source="tables/status_rels",
    header_field="rel",
    header_level=4,
    order=["description", "status document link fields"],
    list_fields=["status document link fields"],
    intro=["status document link fields:The relevant properties of the link section for any resource with this rel are"]
    )
}}


### {{ header("Required SWORD State Information", 3) }}

`state/@id` MUST contain one of:

{{ 
dl(
    source="tables/states",
    term="State",
    definition="Description"
    )
}}

The state field is a list, so it may also contain other states that are server-specific in addition to the SWORD values.


### {{ header("Ingest Statuses for Individual Files", 3) }}

Some files, when deposited, may be processed asynchronously to the client’s request.  For example, large files that require unpacking, 
by-reference deposits, etc.  In these cases, the client will not receive feedback on the state or success of their 
deposit in the request/response exchange.  Instead, the client may monitor the file(s) via the Status document, and for each appropriate 
file (Original Deposits), a “status” field will provide information on the current status of processing for that file.  

The following statuses are permitted, servers SHOULD provide one of these by each relevant file:

{{ 
dl(
    source="tables/ingest-statuses",
    term="Status",
    definition="Description"
   )
}}


## {{ header("Segmented File Upload Document", 2) }}

A client may request information on an ongoing Segmented File Upload at any point via a GET to the Temporary-URL.

The full JSON Schema {{ ref("JSON-SCHEMA") }} can be downloaded [here]({{ export_url("data/schemas/segmented-file-upload.schema.json") }}).

An example of the Segmented File Upload Document:

```json
{% include "examples/segmented-file-upload.json" %}
```

The fields available are defined as follows:

{{ json_schema_definitions("schemas/segmented-file-upload.schema") }}


## {{ header("Error Document", 2) }}

An error document is returned at any point that a synchronous operation fails.

The full JSON Schema {{ ref("JSON-SCHEMA") }} can be downloaded [here]({{ export_url("data/schemas/error.schema.json") }}).

An example of the Error Document:

```json
{% include "examples/error.json" %}
```

The fields available are defined as follows:

{{ json_schema_definitions("schemas/error.schema") }}

See {{ section_link("Error Types") }} for details of what errors can be reported in the `@type` field.