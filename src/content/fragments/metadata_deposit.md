# {{ header("Metadata Deposit") }}

SWORD allows the client to deposit arbitrary metadata onto the server through agnostic support for metadata formats.  A metadata format is
any document which expresses metadata in a given serialisation.  SWORD has a default format
which MUST be supported by the server, which consists of the set of DCMI Terms {{ ref("DCMI") }} expressed as JSON (see {{ section_link("Metadata Document") }}).

In general, the form of metadata consists of several aspects:

1. The serialisation, such as to JSON or XML

2. The vocabulary of the metadata, such as Dublin Core, or MODS (sometimes the vocabulary and the serialisation will be conflated here)

3. The profile of the metadata, such as the RIOXX profile for DC (+extensions)

Any format (combining the 3 aspects above) may be represented by an IRI in the protocol, or an opaque string if no IRI exists or can be minted.

SWORD does not require that the server be able to disseminate any metadata in a format other than the default format.  Metadata in the 
default format can be obtained from {{ section_link("GET Metadata-URL") }}.  If the server chooses to make other metadata formats
available, this SHOULD be listed in the `links` section of the {{ section_link("Status Document") }}.  See 
{{ section_link("Representing Other Formats in the Service Document") }} for details.


## {{ header("Announcing Support for Metadata Formats", 2) }}

The server can list Metadata formats that it will accept in the `acceptMetadata` field of the {{ section_link("Service Document") }}.

If no `acceptMetadata` field is present, the client MUST assume the server only supports the default SWORD metadata format 
(http://purl.org/net/sword/3.0/types/Metadata).

```json
{{ json_extract(
    source="content/examples/service-document.json",
    keys=["acceptMetadata"])
}}
```


## {{ header("Indicating Metadata Format to the Server", 2) }}

During deposit, the client SHOULD specify a `Metadata-Format` header which contains the identifier for the format.  For example, if 
supplying the default SWORD metadata format:

```
Metadata-Format: http://purl.org/net/sword/3.0/types/Metadata
```

If this header is not present the server MUST assume it has the above value.
