# Credits

Technical Lead: Richard Jones, Cottage Labs

Community Lead: Neil Jefferies, University of Oxford

Funder Liaison: Dom Fripp, Jisc


# Introduction

The first major version of SWORD {% ref SWORD 1.3 %} built upon the Resouce creation aspects of AtomPub {% ref AtomPub %} to enable fire-and-forget package 
deposit onto a server.

This approach, where the depositor has no further interaction with the server is of significant value in certain use cases, but there are 
others where this is insufficient. Consider, for example, that the depositor wishes to construct a digital artifact file by file over a 
period of time before deciding that it is time to archive it. In these cases, a higher level of interactivity between the participating 
systems is required, and this is the role that SWORD 2.0 {% ref SWORD 2.0 %} was subsequently developed to fulfil.

As the use cases for SWORD have developed further, it became clear that the increasing size of files repositories were being asked to deal
with was an issue.  As a result of this, and the fact that the technological approach for SWORD 2.0 was starting to show its age, a new
version, SWORD 3.0, has been developed.  This is a radical departure from SWORD 2.0, eliminating ties with AtomPub, and moving to a much
stricter REST+JSON approach, utilising JSON-LD for alignment with Linked Data.  Its key differences to SWORD 2.0 from a functional
perspective are:

* Support for By-Reference file deposit
* Support for Segmented file deposit
* More advanced native packaging and metadata formats

...TODO...

# Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this 
document are to be interpreted as described in {% ref RFC2119 %}.