{% toc %}

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
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


# Creating New Objects

## Creating Objects with only Metadata

Create a new Object on the server, sending only Metadata content (i.e. no Binary File content, and no By-Reference Files).

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Metadata Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with only By-Reference Files

Create a new Object on the server, sending on By-Reference Files (i.e. no Binary Files and no Metadata)

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|By-Reference Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with both Metadata and By-Reference Files

Create a new Object on the server, sending both Metadata content and By-Reference Files (i.e. no Binary File content)

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Metadata + By-Reference Body Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with Binary Files

Create a new Object on the server, sending a single Binary File.  The Binary File is an opaque bitstream which the server should not 
attempt to unpack.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Binary File Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects with Packaged Content

Create a new Object on the server, sending a single Binary File.  The Binary File itself is specified as Packaged Content, which the server 
may understand how to unpack.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Content Requests|Has Body Content|Packaged Content,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Creating Objects ready for Segmented Upload

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Create Requests|Create With Segment Upload Initialisation|Empty Body,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


# Retrieving all or part of Objects

## Retrieving an Object's Status

For an Object where you have an Object-URL, you may request information about the current state of that resource, and receive the Status 
document in response.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Retrieve Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
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
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
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
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


##  Retrieving a Packaged Content representation of an Object

To retrieve the full Object packaged according to some Packaging format, the Status document contains all the files that the Object 
contains, and identifies those which allow you to retrieve the entire objects as a package.  Use the Status document to obtain the URL for 
the format you wish to retrieve, and make a GET to that URL.  See the section "Retrieving a Binary File from an Object" for the 
specification of this operation.



# Appending to existing Objects

Metadata and Files may be added to existing Objects through a variety of mechanisms, which are listed in this section.

## Appending/Selectively Updating Metadata on an Object

Append new metadata or selectively overwrite/update existing metadata on an item.  Metadata provided in this way should be considered to 
overlay existing metadata, such that any new metadata fields are added to the item, and any existing metadata fields are overwritten, and 
any other metadata fields held by the server remain untouched.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Append Requests|Has Body Content|Metadata Body Content|Update Object-URL|Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Appending By-Reference Files to an Object

Append new files to an Object by sending one or more By-Reference files.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Append Requests|Has Body Content|By-Reference Body Content|Update Object-URL|Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Appending Metadata and By-Reference Files to an Object

Append new files and append/overlay Metadata at the same time.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Append Requests|Has Body Content|Metadata + By-Reference Body Content|Update Object-URL|Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Appending a single Binary File to an Object

Append new File to the Object, in addition to existing content which it already contains.  This File will be added as-is to the Object, 
without the server unpacking it as it would Packaged Content.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Append Requests|Has Body Content|Binary File Content|Update Object-URL|Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Appending Packaged Content to an Object

Append new Files (via Packaged Content) to the Object, in addition to existing content which it already contains.  The package may be 
unpacked by the server and new file resources added.  Metadata may also be appended/selectively updated, if the package contains 
actionable metadata.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Append Requests|Has Body Content|Packaged Content|Update Object-URL|Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Initialising Append of Binary Files to an Object via Segmented Upload

Initialise the append of a single Binary File to an Object which will be delivered via a Segmented Upload.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Append Requests|Empty Body|Update Object-URL with Segmented Upload Initialisation|Append Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Initialising Append of Packaged Content to an Object via Segmented Upload

As {% link Initialising Append of Binary Files to an Object via Segmented Upload %} - in this case you should be sure to set the `packaging`
format correctly in the `Content-Disposition` header when initialising the Segmented Upload. 


# Replacing all or part of existing Objects

Metadata and Files may be replaced in existing Objects through a variety of mechanisms, which are listed in this section.

## Replacing the Metadata of an Object

Replace in its entirety the Metadata associated with an Object.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Has Body Content|Metadata Body Content|Update Components|Replace Components|Replace Metadata-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Replacing a single File in an Object

Replace an existing file in the Object with a new file.  The server may keep the old version of the file available.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Has Body Content|Binary File Content|Update Components|Replace Components|Replace File-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Replacing a single File in an Object with a By-Reference File

Replace an existing file in the Object with a new file which the server retrieves as a By-Reference File.  The server may keep the old
version of the file available.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Has Body Content|By-Reference Body Content|Single By-Reference File|Update Components|Replace Components|Replace File-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Replacing a single File in an Object with a Segmented Upload

TODO


## Replacing the FileSet of an Object with By-Reference Files

TODO


## Replacing the FileSet of an Object with a single Binary File

Replace in its entirety the FileSet of the Object (i.e. not the Metadata), with a single Binary File.  All previously existing files will 
be removed, and new one will replace them.  The server may or may not keep old versions of the content available at its discretion.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Has Body Content|Binary File Content|Update Components|Replace Components|Replace FileSet-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Replacing the FileSet of an Object with a single Binary File via Segmented Upload

TODO


## Replacing an Object with Metadata only

TODO


## Replacing an Object with By-Reference Files only

TODO


## Replacing an Object with Metadata and By-Reference Files

TODO


## Replacing an Object with a single Binary File

Replace in its entirety the Object, including all Metadata and Files, with the single Binary File.  All previous files and metadata will be 
removed, and new ones will replace them (the updated item will have no Metadata, though).  The server may or may not keep old versions of 
the content available.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Has Body Content|Binary File Content|Update Object-URL|Replace Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


##  Replacing an Object with Packaged Content

Replace in its entirety the Object, including all Metadata and Files, with the Metadata and Files contained in the Packaged Content.  All 
previous files and metadata will be removed, and new ones will replace them.  The server may or may not keep old versions of the content 
available.

{%
overlay_requirements
    source=tables/requirements.csv,
    groups=All Requests|Modify Requests|Update Requests|Has Body Content|Packaged Content|Update Object-URL|Replace Object-URL,
    order=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Replacing an Object with a single Binary File via Segmented Upload

TODO


## Replacing an Object with Packaged Content via Segmented Upload

TODO

