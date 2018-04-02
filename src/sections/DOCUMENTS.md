# Documents

## JSON-LD Context

SWORD defines the semantics of its documents using JSON-LD {% ref JSON-LD %}.  You can see the full JSON-LD Context 
[here]({% url spec/swordv3.jsonld%})


## Service Document

The Service Document defines the capabilities and operational parameters of the server as a whole, or of a particular Service-URL.

The Service Document consists of a set of properties at the root, and a list of "services".  Each service may define a Service-URL 
and/or additional properties and further nested "services".  For the purposes of normalising the data held in the Service Document (for 
brevity of the serialised document), the Service Document MAY specify at the root properties which MUST be taken to hold true for all 
nested "services" (at any level below) unless that service definition overrides the properties.  A service which sits beneath the root of 
the Service Document and above another Service, MAY also redefine properties, and those overrides MUST be considered to cascade down to 
Services beneath that one.

A Service Document can be retrieved either for the root of the service, or from any Service within the hierarchy of Services available. 
If the root Service Document is requested, the full list of Services, including all their children, MUST be provided.  If the URL of a 
Service is requested, it MUST only provide information about itself and its children.

The full JSON Schema {% ref JSON-SCHEMA %} can be downloaded [here]({% url spec/service-document.schema.json %}).

An example of the Service Document:

```json
{% include examples/service-document.json %}
```

The fields available are defined as follows:

{% json_schema_definitions schemas/service-document.schema.json %}


## Metadata

The default SWORD Metadata document allows the deposit of a standard, basic metadata document constructed using the DCMI terms.  This 
Metadata document can be sent when creating an Object initially, when appending to the metadata, or in replacing the metadata or indeed the 
Object as a whole.

The format of the document is simple and extensible (see the Metadata Formats section).  The “dc” and “dcterms” vocabularies are supported, 
and servers MUST support this metadata format.

The full JSON Schema {% ref JSON-SCHEMA %} can be downloaded [here]({% url spec/metadata.schema.json %}).

An example of the Service Document:

```json
{% include examples/metadata.json %}
```

The fields available are defined as follows:

{% json_schema_definitions schemas/metadata.schema.json %}


When sending this document, the client MUST provide a `Content-Disposition` header of the form:

```
Content-Disposition: attachment; metadata=true
```

Additionally, when sending this document the client SHOULD provide the `Metadata-Format` header with the identifier for the format: http://purl.org/net/sword/3.0/types/Metadata

```
Metadata-Format: http://purl.org/net/sword/3.0/types/Metadata
```

If the client omits the `Metadata-Format` header, the server MUST assume that it is the above format.
