# Retrieve the Service Document

Request from the server a list of the Service-URLs that the client can deposit to.  A Service-URL allows the server to support multiple 
different deposit conditions - each URL may have its own set of rules/workflows behind it; for example, Service-URLs may be 
subject-specific, organisational-specific, or process-specific.  It is up to the client to determine which is the suitable URL for its 
deposit, based on the information provided by the server.  The list of Service-URLs may vary depending on the authentication credentials 
supplied by the client.

This request can be made against a root Service-URL, which will describe the capabilities of the entire server, for information about the 
full list of Service-URLs, or can be made against an individual Service-URL for information just about that service.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Retrieve Service-URL,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


# Creating New Objects

## Creating Objects with only Metadata

Create a new Object on the server, sending only Metadata content (i.e. no Binary File content, and no By-Reference Files).

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Metadata Body Content,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with only By-Reference Files

Create a new Object on the server, sending on By-Reference Files (i.e. no Binary Files and no Metadata)

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|By-Reference Body Content,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with both Metadata and By-Reference Files

Create a new Object on the server, sending both Metadata content and By-Reference Files (i.e. no Binary File content)

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Metadata + By-Reference Body Content,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with Binary Files

Create a new Object on the server, sending a single Binary File.  The Binary File is an opaque bitstream which the server should not 
attempt to unpack.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Binary File Content,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with Packaged Content

Create a new Object on the server, sending a single Binary File.  The Binary File itself is specified as Packaged Content, which the server 
may understand how to unpack.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Packaged Content,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects ready for Segmented Upload

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Segment Upload Initialisation|Empty Body,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


# Retrieving all or part of Objects

## Retrieving an Object's Status

For an Object where you have an Object-URL, you may request information about the current state of that resource, and receive the Status 
document in response.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Retrieve Object-URL,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


## Retrieving the Metadata from an Object

Retrieve the descriptive Metadata document associated with the Object in the standard SWORD format.  This operation is done against the 
Metadata-URL, which is the resource URL representing the Object’s metadata.  When retrieved, this resource is serialised only as the 
standard SWORD format, content negotiation is not supported.  If you want to retrieve the metadata for the Object in other formats, you can 
see a list of the available formats in the Status document, and the individual expressions of the metadata can then be retrieved directly 
by the appropriate URL.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Retrieve Components|Retrieve Metadata-URL,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}

## Retrieving a Binary File from an Object

Retrieve a single File from the Object; files available for retrieval are listed in the Status document.  These single files could be 
actual individual files that make up the object, or:

* Packaged Content that contains a full representation of the Object, including all its files and metadata, packaged according to some standard.
* Metadata in specific formats supported by the server

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Retrieve Components|Retrieve File-URL,
    order=Protocol Operations|Request Requirements|Server Requirements|Response Requirements
%}


##  Retrieving a Packaged Content representation of an Object

To retrieve the full Object packaged according to some Packaging format, the Status document contains all the files that the Object 
contains, and identifies those which allow you to retrieve the entire objects as a package.  Use the Status document to obtain the URL for 
the format you wish to retrieve, and make a GET to that URL.  See the section “Retrieving a Binary File from an Object” for the 
specification of this operation.