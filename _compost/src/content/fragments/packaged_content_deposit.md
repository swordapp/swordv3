# {{ header("Packaged Content Deposit") }}

SWORD allows you to deposit both Files and Metadata simultaneously through support of Packaged Content.  SWORD does not place any limitations
on the number or type of packaging formats that the client/server support, though see the section {{ section_link("Packaging Formats") }} for the
packages that MUST be supported by the server.


## {{ header("Announcing Support for Packaged Content Deposit", 2) }}

The {{ section_link("Service Document") }} uses the `acceptPackaging` field to indicate that a Service will accept deposits of a particular 
packaging format, and the `acceptArchiveFormat` field to indicate the serialisation/compression formats that it understands.

Clients should refer to the `treatment` description in the Service Document to find out the treatment for a particular packaging type.

Packages formats SHOULD be identified by a IRI, but MAY be identified by an arbitrary string.

If no `acceptPackaging` field is supplied the client MUST assume that the server does not formally support any package formats, and 
should expect everything to be treated as per the server's policies with regard to the mimetype as per the `accept` element.

If no `acceptArchiveFormat` field is supplied the client MUST assume that the server supports `application/zip` only.

```json
{{ json_extract(
    source="content/examples/service-document.json",
    keys=["accept", "acceptArchiveFormat", "acceptPackaging"])
}}
```

## {{ header("Package support during resource creation", 2) }}

When depositing Packaged Content, the client SHOULD indicate the archive file MIME type using the `Content-Type` header, and SHOULD also 
give information about content packaging using the `Packaging` header.

The value of the `Packaging` header SHOULD match one of values the server has advertised as acceptable for the service.

If a server receives a POST with an unacceptable `Packaging` header value, it MUST reject the POST by returning an HTTP response with a 
status code of `415` (Unsupported Media Type) and a SWORD Error document with URI 
http://purl.net/org/sword/3.0/error/PackagingFormatNotAcceptable, or store the content without further processing.


## {{ header("Package description in Status documents", 2) }}

Status documents can speak about packaging in two distinct ways, depending on whether an element in the `links` list refers to a file that 
was deposited, or a file that is available for retrieval by the client (or both).

When a package has been deposited as the Original Deposit, it SHOULD record the packaging format and content type alongside it in the record.

```json
{{ json_extract(
    source="content/examples/packaged-content_status_types.json",
    selector="original_deposit",
    keys=["@id", "rel", "contentType", "packaging"])
}}
```

Similarly, when a package has been created by the server from the Object’s content and made available to the client as a service, the 
packaging format and content type MUST be presented alongside it:

```json
{{ json_extract(
    source="content/examples/packaged-content_status_types.json",
    selector="packaged_content",
    keys=["@id", "rel", "contentType", "packaging"])
}}
```