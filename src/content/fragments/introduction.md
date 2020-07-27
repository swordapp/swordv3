See also: [SWORD 3.0 Behaviours]({{ url_for("swordv3-behaviours.html") }}) which provides a denormalised view of the specification's
protocol operations, especially useful for implementers.


# {{ header("Credits") }}

**Technical Lead**: Richard Jones, Cottage Labs

**Community Lead**: Neil Jefferies, University of Oxford

**Funded By**: NII, Jisc, EBSCO

**Funder Liaisons**: Masaharu Hayashi, NII; Dom Fripp, Jisc; Christopher Spalding, EBSCO

**Technical Advisory Group**:
Adam Rehin, Adrian Stevenson, Alan Stiles, Alex Dutton, Catherine Jones, Claire Knowles, David Moles, David Wilcox, Eoghan &Oacute; Carrag&aacute;in, Erick Peirson, 
Gertjan Filarski, Goosyara Kovbasniy, Graham Triggs, Hideaki Takeda, Jan van Mansum, Jauco Noordzij, Jochen Schirrwagen, John Chodacki,
Justin Simpson, Lars Holm Nielsen, Marisa Strong, Martin Wrigley, Masaharu Hayashi, Masud Khokhar, Mike Jackson,
Morane Gruenpeter, Neil Chue Hong, Paul Walk, Peter Sefton, Ralf Claussnitzer, Ricardo Otelo Santos Saraiva Cruz, Richard Rodgers, 
Scott Wilson, Shannon Searle, Stephanie Taylor, Stuart Lewis, Tomasz Parkola, Vitali Peil

# {{ header("Introduction") }}

SWORD 3.0 is a protocol enabling clients and servers to communicate around complex digital objects, especially with regard to supporting the
deposit of these objects into a service like a digital repository.  Complex digital objects consist of both Metadata and File content, 
where the Files may be in a variety of formats, there may be many files, and some may be very large.  The protocol defines semantics for
creating, appending, replacing, deleting, and retrieving information about these complex resources.  It also enables servers to communicate
regarding the status of treatment of deposited content, such as exposing ingest workflow information.

The first major version of SWORD {{ ref("SWORD 1.3") }} built upon the Resouce creation aspects of AtomPub {{ ref("AtomPub") }} to enable 
fire-and-forget package deposit onto a server.

This approach, where the depositor has no further interaction with the server is of significant value in certain use cases, but there are 
others where this is insufficient. Consider, for example, that the depositor wishes to construct a digital artifact file by file over a 
period of time before deciding that it is time to archive it. In these cases, a higher level of interactivity between the participating 
systems is required, and this is the role that SWORD 2.0 {{ ref("SWORD 2.0") }} was subsequently developed to fulfil.

As the use cases for SWORD have developed further, it became clear that the increasing size of files repositories were being asked to deal
with was an issue.  As a result of this, and the fact that the technological approach for SWORD 2.0 was starting to show its age, a new
version, SWORD 3.0, has been developed.  This is a radical departure from SWORD 2.0, eliminating ties with AtomPub, and moving to a much
stricter REST+JSON approach, utilising JSON-LD for alignment with Linked Data.  Its key differences to SWORD 2.0 from a functional
perspective are:

* Support for By-Reference file deposit
* Support for Segmented file deposit
* More advanced native packaging and metadata formats


# {{ header("Notational Conventions") }}

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this 
document are to be interpreted as described in {{ ref("RFC2119") }}.