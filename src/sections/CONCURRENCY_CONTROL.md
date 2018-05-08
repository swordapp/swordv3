#  Concurrency Control

Servers MAY choose to implement concurrency control, in order to ensure that clients do not accidentally overwrite or make changes that 
conflict with other changes which may have happened to the Object since it was first deposited.  Note that this does not prevent clients 
causing damage to Objects, only that it cannot be so easily done by accident.

Objects may change for a number of reasons after their initial creation, such as:

* Additional requests by the original depositing client to modify the Object
* Requests for modify by other clients with authorisation to modify the Object
* Modifications to the Object from agents on the server-side, such as administrators, etc.

In order to provide concurrency control, SWORD follows {% ref RFC7232 %}, and specificially uses the `ETag` and `If-Match` headers.

On each request for a resource, or when the Status document is retrieved, the `ETag` for the resource MUST be returned.  The `ETag` gives 
the client an opaque identifier for the current version of that resource.  When the resource is being updated by the client (for example, 
it is replacing a File), the `ETag` that the client expects to be the current one MUST be sent in the `If-Match` header.  The server MUST 
then compare that with its actual current `ETag` for the resource.  If they match, the request can go ahead, otherwise the Server MUST 
respond with an error (412).

Note that ETags, and Concurrency Control in general, is only applicable from the Object downwards.  There are no requirements for use of 
`ETag` or `If-Match` headers on Service-URLs.


##  Announcing Support for Concurrency Control

The server does not have to announce support for concurrency control in the Service Document.  Clients MUST check response headers for the
presence of an `ETag`.  Presence of the `ETag` indicates that the server requires the client to pay attention to its concurrency control
procedures, and to carry out later requests with an `If-Match` header.

If supporting concurrency control, Servers MUST provide an `ETag` on all responses to requests (GET, POST, PUT) against resources from the 
Object and below.


##  Procedures around Concurrency Control

If a server supports Concurrency Control, it MUST behave in accordance with the following rules.

* An `ETag` MUST be provided for each SWORD resource: the Object, the Metadata, the FileSet and any Files.
* The `ETag` is a resource-level version identifier, it MUST be the same for all expressions of the resource.  For example, all serialised 
Metadata documents (such as in JSON, or in XML) MUST have the same `ETag` as the Metadata resource, and each other.
* The client MUST send the `ETag` that it expects to represent the current version with every request to change the resource (POST, PUT, 
DELETE) by placing it in the `If-Match` header
* If the `ETag` supplied by the client in the `If-Match` header does not match the current `ETag` for the resource, the Server MUST respond with a 412 (Precondition
Failed) error
* If the `ETag` supplied by the client in the `If-Match` header does match the current `ETag` for the resource, the request MUST go ahead as normal.
* The server MUST include the `ETag` in the HTTP headers of every GET request for a resource.
* The server MUST include the `ETag`s for the resources in the appropriate places in the Status document.
* If a resource is modified, its `ETag` MUST change
* If a resource is modified, the `ETag`s of all resources within which it is contained MUST change.
* The server MAY choose between strong and weak `ETag`s, at its discretion
* The server MAY NOT track previous `ETag` values for a resource.


##  Resource Hierarchy for ETag Regeneration

If an `ETag` of a resource changes, the resources above it (up to the level of the Object) MUST also change.  This is to prevent a change 
at a higher level (e.g. an Object replacement) overwriting a change at a lower level (e.g. addition of a single file).

The Object hierarchy is as follows:

* Object
    * Metadata
    * FileSet
        * File

So, for example, if the Metadata is updated, then the Metadata and Object `ETag`s MUST change, but the FileSet and File `ETag`s MAY NOT. 
Similarly, if a File `ETag` changes, then the FileSet and Object `ETag`s must also change, while the Metadata `ETag` MAY NOT.
