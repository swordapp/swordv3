# Packaging Formats

There are 3 packaging formats the all SWORD implementations MUST support.

## Binary

URI: http://purl.org/net/sword/3.0/package/Binary

This format indicates that the package should be interpreted as an opaque blob, and the server SHOULD NOT attempt to extract any content 
from it.  This is typically for use when depositing single files, which do not need unpacking of any kind.

Servers MAY choose, nonetheless, to extract content from Binary packages, if they have the capabilities, such as metadata from images, 
structural information from text documents, etc.


## SimpleZip

URI: http://purl.org/net/sword/3.0/package/SimpleZip

This format indicates that the package is a compressed set of one or more files in an arbitrary directory structure.  The nature of the 
compression and the structure of the compressed content is not specified.

Servers MAY choose to extract the content from SimpleZip packages, and present the individual file components as `derivedResource`s, if 
desired.


## SWORDBagIt

URI: http://purl.org/net/sword/3.0/package/SWORDBagIt

This format is a profile of the BagIt directory structure, which has in turn been serialised (which may include compression).  The nature 
of the serialisation/compression is not specified, though if the client wishes the server to extract the content, it SHOULD use one of
the formats specified in the {% link Service Document %} field `acceptArchiveFormat`.

```
SwordBagIt
| -- bag-info.txt
| -- bagit.txt
| -- data
| -- | -- bitstreams ...
|    \ -- directories ...
|         \ bitstreams ...
| -- manifest-sha-256.txt
| -- metadata
|     \-- sword.json
\ -- tagmanifest-sha-256.txt
```

This allows us to represent the item as a combination of an arbitrary structure of bitstreams in the data directory (similar to SimpleZip), 
and the metadata in the sword default format in `metadata/sword.json`.  A `manifest` (and `tagmanifest`) of sha-256 checksums is required, as 
well as the `bagit.txt` file and a `bag-info.txt` file.

The content of `sword.json` is exactly as defined in the SWORD default Metadata.  Note that use of `fetch.txt` is not supported here.

The server SHOULD unpack this file, and action at least the Metadata.  The contents of the data directory MAY be unpackaged into 
`derivedResource`s if the server desires.  It is RECOMMENDED that the contents of the data directory be a flat file structure, to aid 
mutual comprehension by servers/clients.

