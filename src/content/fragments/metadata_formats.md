# {{ header("Metadata Formats") }}

## {{ header("Default Format", 2) }}

In order to provide a baseline of interoperability, SWORD provides a default metadata format which MUST be supported by the server.  This 
document has the following aspects (as per {{ section_link("Metadata Deposit") }}):

1. It is serialised as JSON and with a JSON-LD `@context`

2. It contains `dc` and `dcterms` vocabulary elements, and any other arbitrary elements added by the client

3. It does not pre-suppose any particular profile of usage of these vocabulary elements.

Clients MAY choose to extend this document with their own metadata fields, though the server MAY NOT understand them, and MAY ignore them.

When using this Metadata Format, the client should identify it in the Metadata-Format header with the following IRI:

```
http://purl.org/net/sword/3.0/types/Metadata
```


## {{ header("Depositing Other Formats", 2) }}

In addition to the standard SWORD metadata format described above, SWORD can support the deposit of arbitrary metadata schemas and 
serialisations.  

Clients who wish to ensure that their servers support all the metadata they send them should consider minting a new identifier for their 
format, and looking for servers to declare explicit support for it.

Clients should not expect that servers will keep their metadata in the format it is provided.  Servers can and will store the metadata
in their internal formats as needed.

The following is a minimal example of the deposit of a MODS XML metadata file while creating a new Object:


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

If the server supports the MODS Metadata-Format, identified with the IRI `http://www.loc.gov/mods/v3` then it will be able to create a new 
Object from this XML document, and populate the Metadata from the data therein.


## {{ header("Representing Other Formats in the Service Document", 2) }}

A server is not required to retain or be able to disseminate the metadata delivered to it by the client in the format it is provided.  Alternative
metadata formats to the default format MAY be accepted (as defined by the `acceptMetadata` field in the {{ section_link("Status Document") }}),
but the server is not required to be able to serve that metadata format as well.

If the server chooses to expose metadata in alternative formats to the default, it may do so by providing them
as links in the `links` section of the {{ section_link("Status Document") }}.  To do this:

* Provide a link to the serialised metadata
* Specify a `rel` type of `http://purl.org/net/sword/3.0/terms/formattedMetadata`
* Specify the `contentType` as needed
* Specify the `metadataFormat` as the format identifier for the metadata schema.

For example, to reflect the metadata from the previous section back to the client:

```json
{{ json_extract("content/examples/status.json", 
                selector="links", 
                listobj_match={"@id" : "http://www.swordserver.ac.uk/col1/mydeposit/metadata.mods.xml"},
                unwrap_single_entry_list=True)
}}
```

