{~ html section,clazz=title ~}

{% title_slide 
    title=Introducing SWORD&nbsp;3,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com<br><a href='https://twitter.com/richard_d_jones'>@richard_d_jones</a> <a href='https://twitter.com/cottagelabs'>@cottagelabs</a>"
%}

{~ html /section ~}


{~ html section ~}

SWORD 3.0 is a protocol enabling clients and servers to communicate around complex digital objects

It defines semantics for creating, appending, replacing, deleting, and retrieving information about these complex resources.  

{~ html /section ~}



{~ html section ~}

{~ html section ~}

### Working Principles

{~ html /section ~}


{~ html section ~}

* The more optional features, the harder true interoperability
* Simpler the better - aim to remove any unusued features from SWORDv2
* Research data support is key, though not at the expense of existing features
* Make it easy for the community to engage and developers to pick up
* Make it easy to maintain and extend
* Be clear about the distinction between protocol and implementation

{~ html /section ~}


{~ html section ~}

* One single simple (as possible) document describing the protocol
* Pay attention to anti-patterns: only one file, only one metadata schema, etc.
* Prioritise current, validated and pressing use cases
* Make it easy to relate implementations to the parts of the protocol
* Minimise the effort to implement against a repository (as few special features as possible)

{~ html /section ~}

{~ html /section ~}



{~ html section ~}

{~ html section ~}

### Usage Patterns

A usage pattern is what we called our single units of functionality that we wanted to support.

Full set [here](https://docs.google.com/spreadsheets/d/14gP6ZjH_QX1VjZrh3CeJdgMsML2w0S95GWdYknV3ziE/edit) (41 in total)

Some examples below.

{~ html /section ~}


{~ html section ~}

{% dl tables/usage-patterns.csv,term=Title,definition=Description,filter_field=ID,filters=UP-001|UP-002|UP-010|UP-012 %} 

{~ html /section ~}


{~ html section ~}

{% dl tables/usage-patterns.csv,term=Title,definition=Description,filter_field=ID,filters=UP-013|UP-020|UP-027|UP-034 %} 

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

### Differences to SWORDv2 and New Features

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### JSON instead of XML

No more AtomPub.  Was:

```
<?xml version="1.0" ?>
<service xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:sword="http://purl.org/net/sword/terms/"
    xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns="http://www.w3.org/2007/app">

    <sword:version>2.0</sword:version>
    <sword:maxUploadSize>16777216</sword:maxUploadSize>

    <workspace>
        <atom:title>Main Site</atom:title>

        <collection href="http://swordapp.org/col-iri/43">
            <atom:title>Collection 43</atom:title>
            <accept>*/*</accept>
            <accept alternate="multipart-related">*/*</accept>
            <sword:collectionPolicy>Collection Policy</sword:collectionPolicy>
            <dcterms:abstract>Collection Description</dcterms:abstract>
            <sword:mediation>false</sword:mediation>
            <sword:treatment>Treatment description</sword:treatment>
            <sword:acceptPackaging>http://purl.org/net/sword/package/SimpleZip</sword:acceptPackaging>
            <sword:acceptPackaging>http://purl.org/net/sword/package/METSDSpaceSIP</sword:acceptPackaging>
            <sword:service>http://swordapp.org/sd-iri/e4</sword:service>
        </collection>
    </workspace>
</service>
```

{~ html /section ~}

{~ html section ~}

Now

```
{% include examples/service-document.json %}
```

{~ html /section ~}

{~ html /section ~}



{~ html section ~}

{~ html section ~}

### Support for Arbitrary Metadata

SWORDv2 provided *implicit* support for arbitrary metadata formats, with no standard way to indicate to the server what you were sending it.

SWORD v3 provides *explicit* support for arbitrary metadata formats, via the `Metadata-Format` header.

{~ html /section ~}

{~ html section ~}

**SWORDv2: Create a resource with metadata only**

```
POST Col-IRI HTTP/1.1
Host: example.org
Authorization: Basic ZGFmZnk6c2VjZXJldA==
Content-Length: [content length]
Content-Type: application/atom+xml;type=entry
In-Progress: true
On-Behalf-Of: jbloggs
Slug: [suggested identifier]

<?xml version="1.0"?>
<entry xmlns="http://www.w3.org/2005/Atom"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <title>Title</title>
    <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
    <updated>2005-10-07T17:17:08Z</updated>
    <author><name>Contributor</name></author>
    <summary type="text">The abstract</summary>

    <!-- some embedded metadata -->
    <dcterms:abstract>The abstract</dcterms:abstract>
    <dcterms:accessRights>Access Rights</dcterms:accessRights>
    <dcterms:alternative>Alternative Title</dcterms:alternative>
    <dcterms:available>Date Available</dcterms:available>
    <dcterms:bibliographicCitation>Bibliographic Citation</dcterms:bibliographicCitation>
    <dcterms:contributor>Contributor</dcterms:contributor>
    <dcterms:description>Description</dcterms:description>
    <dcterms:hasPart>Has Part</dcterms:hasPart>
    <dcterms:hasVersion>Has Version</dcterms:hasVersion>
    <dcterms:identifier>Identifier</dcterms:identifier>
    <dcterms:isPartOf>Is Part Of</dcterms:isPartOf>
    <dcterms:publisher>Publisher</dcterms:publisher>
    <dcterms:references>References</dcterms:references>
    <dcterms:rightsHolder>Rights Holder</dcterms:rightsHolder>
    <dcterms:source>Source</dcterms:source>
    <dcterms:title>Title</dcterms:title>
    <dcterms:type>Type</dcterms:type>

</entry>
```

{~ html /section ~}

{~ html section ~}

**SWORDv3: Create a resource with metadata-only**

(using a metadata format that is not the default)

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

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

### Concurrency Control

SWORDv2 did not have the concept of concurrency control.

SWORDv3 provides Optimistic Concurrency Control via the use of `ETag` and `If-Match` headers.

{~ html /section ~}


{~ html section ~}

### Segmented File Upload

SWORDv2 dealt only in full by-value deposits of files, which could be problematic if the files are very large.

In SWORDv3, to transfer a large file, the client can break it down into a number of equally sized segments of binary data (the final segment 
may be a different size to the rest).  It can then initialise a Segmented File Upload with the server, and then transfer the segments.  The 
server will reconstitute these segments into a single file, and then the client may deposit this file by-reference.

{~ html /section ~}


{~ html section ~}

### By-Reference Deposit

SWORDv2 did not have any formal mechanism for depositing files by-reference (although some workarounds existed)

SWORDv3 provides explicit support for By-Reference deposit, where the client provides the server with URLs for Files which it would like 
the server to retrieve asynchronously.  

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### More Advanced Packaging

There has been a lot of pressure on the SWORD team to provide more detail about actual packaging formats.  We have resisted for a long time,
but for SWORDv3 we have introduced a BagIt profile which is slightly more advanced than the package formats required by SWORDv2

{~ html /section ~}

{~ html section ~}

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
and the metadata in the sword default format in `metadata/sword.json`. A `manifest` (and `tagmanifest`) of sha-256 checksums is required, as well 
as the `bagit.txt` file and a `bag-info.txt` file.

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### Implementation Plans

We are currently waiting to hear on the outcome of a proposal for onward funding for implementation.

Below is what we're hoping to get funding to cover:

{~ html /section ~}

{~ html section ~}

We want to implement all the aspects of the specification which are identified as MUST in the
documentation. This means we would be doing the smallest complete implementation
possible, which will provide significant insight into the implementability of the full specification.

{~ html /section ~}

{~ html section ~}

**Client**

Implement a full client which can carry out all of the operations available to
it in the specification.

This would be a fully re-usable code-library for anyone else wanting to work with SWORDv3

{~ html /section ~}

{~ html section ~}

**Test Suite**

Provide a test suite which can drive the client to carry out all the actions
defined in the specification, in each case with a selection of data, including
error cases.

This would also be fully re-usable so anyone else implementing a SWORDv3 server
would be able to run our test suite to validate their work.

{~ html /section ~}

{~ html section ~}

**Invenio Back-End**

Implement Invenio support for all of the features of the specification which
are identified as MUST in the documentation, and any optional features
which are required to support those features in this environment.

This would make Invenio3 a SWORDv3 compliant repository and also provide a reference
implementation for SWORDv3 servers.  Some components will be re-usable outside
Invenio.

{~ html /section ~}

{~ html /section ~}

{~ html section ~}

### Last But Not Least

Thanks to all of the following who were involved in the Technical Advisory Board:

Adam Rehin, Adrian Stevenson, Alan Stiles, Catherine Jones, Claire Knowles, David Moles, David Wilcox, Eoghan &Oacute; Carrag&aacute;in, Erick Peirson, 
Gertjan Filarski, Goosyara Kovbasniy, Graham Triggs, Hideaki Takeda, Jan van Mansum, Jauco Noordzij, Jochen Schirrwagen, John Chodacki,
Justin Simpson, Lars Holm Nielsen, Marisa Strong, Martin Wrigley, Masaharu Hayashi, Masud Khokhar, Mike Jackson,
Morane Gruenpeter, Neil Chue Hong, Paul Walk, Peter Sefton, Ralf Claussnitzer, Ricardo Otelo Santos Saraiva Cruz, Richard Rodgers, 
Scott Wilson, Shannon Searle, Stephanie Taylor, Stuart Lewis, Tomasz Parkola, Vitali Peil

{~ html /section ~}

{~ html section,clazz=title ~}

{% title_slide 
    title=Thanks for Listening,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com<br><a href='https://twitter.com/richard_d_jones'>@richard_d_jones</a> <a href='https://twitter.com/cottagelabs'>@cottagelabs</a>"
%}

{~ html /section ~}