# Metadata Formats

## Default Format

In order to provide a baseline of interoperability, SWORD provides a default metadata format which MUST be supported by the server.  This 
document has the following aspects:

1. It is serialised as JSON and with a JSON-LD `@context`

2. It contains `dc` and `dcterms` vocabulary elements, and any other arbitrary elements added by the client

3. It does not pre-suppose any particular profile of usage of these vocabulary elements.

Clients MAY choose to extend this document with their own metadata fields, though the server MAY NOT understand them, and MAY ignore them.

When using this Metadata Format, the client should identify it in the Metadata-Format header with the following IRI:

```
http://purl.org/net/sword/3.0/types/Metadata
```


## Depositing Other Formats

In addition to the standard SWORD metadata format described above, SWORD can support the deposit of arbitrary metadata schemas and 
serialisations.  

Clients who wish to ensure that their servers support all the metadata they send them should consider minting a new identifier for their 
format, and looking for servers to declare explicit support for it.

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
