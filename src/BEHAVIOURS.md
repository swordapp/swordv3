{~ html div,clazz=nav ~}
{% toc %}
{~ html /div ~}

{~ html div,clazz=spec ~}
Last modified: {% date now,%Y-%m-%d %}

# Retrieve the Service Document

Request from the server a list of the Service-URLs that the client can deposit to.  A Service-URL allows the server to support multiple 
different deposit conditions - each URL may have its own set of rules/workflows behind it; for example, Service-URLs may be 
subject-specific, organisational-specific, or process-specific.  It is up to the client to determine which is the suitable URL for its 
deposit, based on the information provided by the server.  The list of Service-URLs may vary depending on the authentication credentials 
supplied by the client.

This request can be made against a root Service-URL, which will describe the capabilities of the entire server, for information about the 
full list of Service-URLs, or can be made against an individual Service-URL for information just about that service.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Retrieve|Empty Body|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


# Creating New Objects

## Creating Objects with only Metadata

Create a new Object on the server, sending only Metadata content (i.e. no Binary File content, and no By-Reference Files).

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Metadata|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Metadata
%}
```

## Creating Objects with only By-Reference Files

Create a new Object on the server, sending on By-Reference Files (i.e. no Binary Files and no Metadata)

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|By-Reference|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|By-Reference
%}
```

## Creating Objects with both Metadata and By-Reference Files

Create a new Object on the server, sending both Metadata content and By-Reference Files (i.e. no Binary File content)

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|MD+BR|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|MD+BR
%}
```

## Creating Objects with Binary Files

Create a new Object on the server, sending a single Binary File.  The Binary File is an opaque bitstream which the server should not 
attempt to unpack.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Binary File|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Binary File
%}
```

## Creating Objects with Packaged Content

Create a new Object on the server, sending a single Binary File.  The Binary File itself is specified as Packaged Content, which the server 
may understand how to unpack.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Packaged Content|Service-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Packaged Content
%}
```

## Creating Objects with Segmented File Upload

First create a Temporary-URL to which to upload the file segments:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

Then upload all the file segments as per {% link Upload a File Segment %}.

Then carry out a By-Reference deposit using the Temporary-URL as per {% link Creating Objects with only By-Reference Files %}

# Retrieving all or part of Objects

## Retrieving an Object's Status

For an Object where you have an Object-URL, you may request information about the current state of that resource, and receive the Status 
document in response.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Retrieve|Empty Body|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Retrieving the Metadata from an Object

Retrieve the descriptive Metadata document associated with the Object in the standard SWORD format.  This operation is done against the 
Metadata-URL, which is the resource URL representing the Object’s metadata.  When retrieved, this resource is serialised only as the 
standard SWORD format, content negotiation is not supported.  If you want to retrieve the metadata for the Object in other formats, you can 
see a list of the available formats in the Status document, and the individual expressions of the metadata can then be retrieved directly 
by the appropriate URL.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Retrieve|Empty Body|Metadata-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


## Retrieving a Binary File from an Object

Retrieve a single File from the Object; files available for retrieval are listed in the Status document.  These single files could be 
actual individual files that make up the object, or:

* Packaged Content that contains a full representation of the Object, including all its files and metadata, packaged according to some standard.
* Metadata in specific formats supported by the server

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Retrieve|Empty Body|File-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
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
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|Metadata|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Metadata
%}
```

## Appending By-Reference Files to an Object

Append new files to an Object by sending one or more By-Reference files.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|By-Reference|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|By-Reference
%}
```

## Appending Metadata and By-Reference Files to an Object

Append new files and append/overlay Metadata at the same time.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|MD+BR|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|MD+BR
%}
```

## Appending a single Binary File to an Object

Append new File to the Object, in addition to existing content which it already contains.  This File will be added as-is to the Object, 
without the server unpacking it as it would Packaged Content.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|Binary File|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Binary File
%}
```

## Appending Packaged Content to an Object

Append new Files (via Packaged Content) to the Object, in addition to existing content which it already contains.  The package may be 
unpacked by the server and new file resources added.  Metadata may also be appended/selectively updated, if the package contains 
actionable metadata.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|Packaged Content|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Packaged Content
%}
```

## Append of Binary Files to an Object via Segmented File Upload

Append a single Binary File to an Object which will be delivered via a Segmented File Upload.

First create a Temporary-URL to which to upload the file segments:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

Then upload all the file segments as per {% link Upload a File Segment %}.

Then carry out a By-Reference deposit using the Temporary-URL as per {% link Appending By-Reference Files to an Object %}


## Append of Packaged Content to an Object via Segmented File Upload

As {% link Append of Binary Files to an Object via Segmented File Upload %}. 


# Replacing all or part of existing Objects

Metadata and Files may be replaced in existing Objects through a variety of mechanisms, which are listed in this section.

## Replacing the Metadata of an Object

Replace in its entirety the Metadata associated with an Object.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|Metadata|Metadata-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Metadata
%}
```

## Replacing a single File in an Object

Replace an existing file in the Object with a new file.  The server may keep the old version of the file available.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|Binary File|File-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Binary File
%}
```


## Replacing a single File in an Object with a By-Reference File

Replace an existing file in the Object with a new file which the server retrieves as a By-Reference File.  The server may keep the old
version of the file available.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|By-Reference|File-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|By-Reference
%}
```


## Replacing a single File in an Object with a Segmented Upload

Replace an existing file in the Object with a new file, which the client will send in segments.  

First create a Temporary-URL to which to upload the file segments:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

Then upload all the file segments as per {% link Upload a File Segment %}.

Then carry out a By-Reference deposit using the Temporary-URL as per {% link Replacing a single File in an Object with a By-Reference File %}


## Replacing the FileSet of an Object with By-Reference Files

Replace all the files in the FileSet of an Object with one or more By-Reference Files.  All previously existing files will be removed, and
new ones will replace them.  The server may or may not keep old versions of the content availabl, at its discretion.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|By-Reference|FileSet-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|By-Reference
%}
```


## Replacing the FileSet of an Object with a single Binary File

Replace in its entirety the FileSet of the Object (i.e. not the Metadata), with a single Binary File.  All previously existing files will 
be removed, and the new one will replace them.  The server may or may not keep old versions of the content available, at its discretion.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|Binary File|FileSet-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Binary File
%}
```


## Replacing the FileSet of an Object with a single Binary File via Segmented File Upload

Replace in its entirity the FileSet of the Object (i.e. not the Metadata), with a single Binary File, that is provided via Segmented File Upload.
All previously existing files will be removed, and the new one will replace them.  The server may or may not keep old versions of the 
content available, at its discretion.

First create a Temporary-URL to which to upload the file segments:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

Then upload all the file segments as per {% link Upload a File Segment %}.

Then carry out a By-Reference deposit using the Temporary-URL as per {% link Replacing the FileSet of an Object with By-Reference Files %}


## Replacing an Object with Metadata only

Replace the entire Object, removing all previous files and metadata, and replace it with just the supplied Metadata.  The server may or may 
not keep old versions of the content available, at its discretion.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|Metadata|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Metadata
%}
```

## Replacing an Object with By-Reference Files only

Replace the entire Object, removing all previous files and metadata, and replace it with one or more files supplied via By-Reference upload.
The server may or may not keep old versions of the content available, at its discretion.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|By-Reference|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|By-Reference
%}
```

## Replacing an Object with Metadata and By-Reference Files

Replace the entire Object, removing all previous files and metadata, and replace it with new Metadata and one or more files supplied via
By-Reference upload.  The server may or may not keep old versions of the content available, at its discretion.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|MD+BR|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|MD+BR
%}
```

## Replacing an Object with a single Binary File

Replace in its entirety the Object, including all Metadata and Files, with the single Binary File.  All previous files and metadata will be 
removed, and new ones will replace them (the updated item will have no Metadata, though).  The server may or may not keep old versions of 
the content available.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|Binary File|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Binary File
%}
```

##  Replacing an Object with Packaged Content

Replace in its entirety the Object, including all Metadata and Files, with the Metadata and Files contained in the Packaged Content.  All 
previous files and metadata will be removed, and new ones will replace them.  The server may or may not keep old versions of the content 
available.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Replace|Packaged Content|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Direct Deposit|Packaged Content
%}
```


## Replacing an Object with a single Binary File via Segmented File Upload

Replace in its entirety the Object, including all Metadata and Files, with a single Binary File, which will be delivered via Segmented
File Upload.  All previous files and metadata will be removed, and new ones will replace them.  The server may or may not keep old versions of 
the content available.

First create a Temporary-URL to which to upload the file segments:

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

Then upload all the file segments as per {% link Upload a File Segment %}.

Then carry out a By-Reference deposit using the Temporary-URL as per {% link Replacing an Object with By-Reference Files only %}


## Replacing an Object with Packaged Content via Segmented File Upload

This operation is carried out exactly as per {% link Replacing an Object with a single Binary File via Segmented File Upload %}.


# Deleting all or part of Objects

## Deleting an Object's Metadata

Delete all the metadata fields from the Object.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Delete|Empty Body|Metadata-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Deleting a single Binary File from an Object

Delete a single File from the Object.  The server may keep old versions of the file.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Delete|Empty Body|File-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Deleting all the Files from an Object

Remove all the Files from an object.  This will leave the Object and its Metadata intact.  The server may keep old versions of the files 
available.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Delete|Empty Body|FileSet-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Deleting the entire Object

Delete the Object in its entirety from the server, along with all Metadata and Files.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Delete|Empty Body|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}


# File Segments

## Initialise a Segmented File Upload

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Create|Empty Body|Staging-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=Segmented Upload Initialisation|Empty Body
%}
```

## Upload a File Segment

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Append|File Segment|Temporary-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

The `Content-Disposition` in this case would be:

```
{%
content_disposition
    reqs=tables/content-disposition.csv,
    hierarchy=tables/content-disposition-hierarchy.csv,
    groups=Upload Type|Content,
    match=File Segment Upload|File Segment
%}
```


## Abort a Segmented File Upload

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Delete|Empty Body|Temporary-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

## Retrieve information about a Segmented File Upload

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Retrieve|Empty Body|Temporary-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

# Completing Previously In-Progress Deposits

Where you have previously carried out deposits and sent the object the `In-Progress: true` header, you will eventually need to tell the
server that you have completed your additions or modifications to the Object, so that it can finalise your deposit.

{%
requirements
    reqs=tables/requirements.csv,
    hierarchy=tables/reqs_hierarchy.csv,
    groups=Request|Content|Resource,
    match=Complete|Empty Body|Object-URL,
    output=Protocol Operation|Request Requirements|Server Requirements|Response Requirements
%}

No `Content-Disposition` header is required in this request.


{~ html /div ~}