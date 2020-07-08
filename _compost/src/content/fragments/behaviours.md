# {{ header("Retrieve the Service Document", toc="b") }}

Request from the server a list of the Service-URLs that the client can deposit to.  A Service-URL allows the server to support multiple
different deposit conditions - each URL may have its own set of rules/workflows behind it; for example, Service-URLs may be
subject-specific, organisational-specific, or process-specific.  It is up to the client to determine which is the suitable URL for its
deposit, based on the information provided by the server.  The list of Service-URLs may vary depending on the authentication credentials
supplied by the client.

This request can be made against a root Service-URL, which will describe the capabilities of the entire server, for information about the
full list of Service-URLs, or can be made against an individual Service-URL for information just about that service.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Retrieve", "Empty Body", "Service-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}


# {{ header("Creating New Objects", toc="b") }}

## {{ header("Creating Objects with only Metadata", 2, toc="b") }}

Create a new Object on the server, sending only Metadata content (i.e. no Binary File content, and no By-Reference Files).

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Metadata", "Service-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Metadata"])
}}
```

## {{ header("Creating Objects with only By-Reference Files", 2, toc="b") }}

Create a new Object on the server, sending on By-Reference Files (i.e. no Binary Files and no Metadata)

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "By-Reference", "Service-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```

## {{ header("Creating Objects with both Metadata and By-Reference Files", 2, toc="b") }}

Create a new Object on the server, sending both Metadata content and By-Reference Files (i.e. no Binary File content)

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "MD+BR", "Service-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "MD+BR"])
}}
```

## {{ header("Creating Objects with Binary Files", 2, toc="b") }}

Create a new Object on the server, sending a single Binary File.  The Binary File is an opaque bitstream which the server should not
attempt to unpack.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Binary File", "Service-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Binary File"])
}}
```

## {{ header("Creating Objects with Packaged Content", 2, toc="b") }}

Create a new Object on the server, sending a single Binary File.  The Binary File itself is specified as Packaged Content, which the server
may understand how to unpack.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Packaged Content", "Service-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Packaged Content"])
}}
```

## {{ header("Creating Objects with Segmented File Upload", 2, toc="b") }}

First create a Temporary-URL to which to upload the file segments:

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

Then upload all the file segments as per {{ section_link("Upload a File Segment", "b") }}.

Then carry out a By-Reference deposit using the Temporary-URL as per {{ section_link("Creating Objects with only By-Reference Files", "b") }}

# {{ header("Retrieving all or part of Objects", toc="b") }}

## {{ header("Retrieving an Object's Status", 2, toc="b") }}

For an Object where you have an Object-URL, you may request information about the current state of that resource, and receive the Status
document in response.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Retrieve", "Empty Body", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}


## {{ header("Retrieving the Metadata from an Object", 2, toc="b") }}

Retrieve the descriptive Metadata document associated with the Object in the standard SWORD format.  This operation is done against the
Metadata-URL, which is the resource URL representing the Object’s metadata.  When retrieved, this resource is serialised only as the
standard SWORD format, content negotiation is not supported.  If you want to retrieve the metadata for the Object in other formats, you can
see a list of the available formats in the Status document, and the individual expressions of the metadata can then be retrieved directly
by the appropriate URL.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Retrieve", "Empty Body", "Metadata-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}


## {{ header("Retrieving a Binary File from an Object", 2, toc="b") }}

Retrieve a single File from the Object; files available for retrieval are listed in the Status document.  These single files could be
actual individual files that make up the object, or:

* Packaged Content that contains a full representation of the Object, including all its files and metadata, packaged according to some standard.
* Metadata in specific formats supported by the server

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Retrieve", "Empty Body", "File-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}


## {{ header("Retrieving a Packaged Content representation of an Object", 2, toc="b") }}

To retrieve the full Object packaged according to some Packaging format, the Status document contains all the files that the Object
contains, and identifies those which allow you to retrieve the entire objects as a package.  Use the Status document to obtain the URL for
the format you wish to retrieve, and make a GET to that URL.  See the section "Retrieving a Binary File from an Object" for the
specification of this operation.



# {{ header("Appending to existing Objects", toc="b") }}

Metadata and Files may be added to existing Objects through a variety of mechanisms, which are listed in this section.

## {{ header("Appending Metadata to an Object", 2, toc="b") }}

Append new metadata to an Object.  Metadata provided in this way should be considered to
extend existing metadata, such that any new metadata fields are added to the Object, and any existing metadata fields are kept as-is.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "Metadata", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Metadata"])
}}
```

## {{ header("Appending By-Reference Files to an Object", 2, toc="b") }}

Append new files to an Object by sending one or more By-Reference files.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "By-Reference", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```

## {{ header("Appending Metadata and By-Reference Files to an Object", 2, toc="b") }}

Append new files and append/overlay Metadata at the same time.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "MD+BR", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "MD+BR"])
}}
```

## {{ header("Appending a single Binary File to an Object", 2, toc="b") }}

Append new File to the Object, in addition to existing content which it already contains.  This File will be added as-is to the Object,
without the server unpacking it as it would Packaged Content.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "Binary File", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Binary File"])
}}
```

## {{ header("Appending Packaged Content to an Object", 2, toc="b") }}

Append new Files (via Packaged Content) to the Object, in addition to existing content which it already contains.  The package may be
unpacked by the server and new file resources added.  Metadata may also be appended/selectively updated, if the package contains
actionable metadata.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "Packaged Content", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Packaged Content"])
}}
```

## {{ header("Append of Binary Files to an Object via Segmented File Upload", 2, toc="b") }}

Append a single Binary File to an Object which will be delivered via a Segmented File Upload.

First create a Temporary-URL to which to upload the file segments:

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

Then upload all the file segments as per {{ section_link("Upload a File Segment", "b") }}.

Then carry out a By-Reference deposit using the Temporary-URL as per {{ section_link("Appending By-Reference Files to an Object", "b") }}


## {{ header("Append of Packaged Content to an Object via Segmented File Upload", 2, toc="b") }}

As {{ section_link("Append of Binary Files to an Object via Segmented File Upload", "b") }}.


# {{ header("Replacing all or part of existing Objects", toc="b") }}

Metadata and Files may be replaced in existing Objects through a variety of mechanisms, which are listed in this section.

## {{ header("Replacing the Metadata of an Object", 2, toc="b") }}

Replace in its entirety the Metadata associated with an Object.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "Metadata", "Metadata-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Metadata"])
}}
```

## {{ header("Replacing a single File in an Object", 2, toc="b") }}

Replace an existing file in the Object with a new file.  The server may keep the old version of the file available.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "Binary File", "File-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Binary File"])
}}
```


## {{ header("Replacing a single File in an Object with a By-Reference File", 2, toc="b") }}

Replace an existing file in the Object with a new file which the server retrieves as a By-Reference File.  The server may keep the old
version of the file available.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "By-Reference", "File-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```


## {{ header("Replacing a single File in an Object with a Segmented Upload", 2, toc="b") }}

Replace an existing file in the Object with a new file, which the client will send in segments.

First create a Temporary-URL to which to upload the file segments:

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

Then upload all the file segments as per {{ section_link("Upload a File Segment", "b") }}.

Then carry out a By-Reference deposit using the Temporary-URL as per {{ section_link("Replacing a single File in an Object with a By-Reference File", "b") }}


## {{ header("Replacing the FileSet of an Object with By-Reference Files", 2, toc="b") }}

Replace all the files in the FileSet of an Object with one or more By-Reference Files.  All previously existing files will be removed, and
new ones will replace them.  The server may or may not keep old versions of the content available, at its discretion.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "By-Reference", "FileSet-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```


## {{ header("Replacing the FileSet of an Object with a single Binary File", 2, toc="b") }}

Replace in its entirety the FileSet of the Object (i.e. not the Metadata), with a single Binary File.  All previously existing files will
be removed, and the new one will replace them.  The server may or may not keep old versions of the content available, at its discretion.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "Binary File", "FileSet-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Binary File"])
}}
```


## {{ header("Replacing the FileSet of an Object with a single Binary File via Segmented File Upload", 2, toc="b") }}

Replace in its entirity the FileSet of the Object (i.e. not the Metadata), with a single Binary File, that is provided via Segmented File Upload.
All previously existing files will be removed, and the new one will replace them.  The server may or may not keep old versions of the
content available, at its discretion.

First create a Temporary-URL to which to upload the file segments:

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

Then upload all the file segments as per {{ section_link("Upload a File Segment", "b") }}.

Then carry out a By-Reference deposit using the Temporary-URL as per {{ section_link("Replacing the FileSet of an Object with By-Reference Files", "b") }}


## {{ header("Replacing an Object with Metadata only", 2, toc="b") }}

Replace the entire Object, removing all previous files and metadata, and replace it with just the supplied Metadata.  The server may or may
not keep old versions of the content available, at its discretion.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "Metadata", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Metadata"])
}}
```

## {{ header("Replacing an Object with By-Reference Files only", 2, toc="b") }}

Replace the entire Object, removing all previous files and metadata, and replace it with one or more files supplied via By-Reference upload.
The server may or may not keep old versions of the content available, at its discretion.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "By-Reference", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```

## {{ header("Replacing an Object with Metadata and By-Reference Files", 2, toc="b") }}

Replace the entire Object, removing all previous files and metadata, and replace it with new Metadata and one or more files supplied via
By-Reference upload.  The server may or may not keep old versions of the content available, at its discretion.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "MD+BR", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "MD+BR"])
}}
```

## {{ header("Replacing an Object with a single Binary File", 2, toc="b") }}

Replace in its entirety the Object, including all Metadata and Files, with the single Binary File.  All previous files and metadata will be
removed, and new ones will replace them (the updated item will have no Metadata, though).  The server may or may not keep old versions of
the content available.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "Binary File", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Binary File"])
}}
```

## {{ header("Replacing an Object with Packaged Content", 2, toc="b") }}

Replace in its entirety the Object, including all Metadata and Files, with the Metadata and Files contained in the Packaged Content.  All
previous files and metadata will be removed, and new ones will replace them.  The server may or may not keep old versions of the content
available.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Replace", "Packaged Content", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Packaged Content"])
}}
```


## {{ header("Replacing an Object with a single Binary File via Segmented File Upload", 2, toc="b") }}

Replace in its entirety the Object, including all Metadata and Files, with a single Binary File, which will be delivered via Segmented
File Upload.  All previous files and metadata will be removed, and new ones will replace them.  The server may or may not keep old versions of
the content available.

First create a Temporary-URL to which to upload the file segments:

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

Then upload all the file segments as per {{ section_link("Upload a File Segment", "b") }}.

Then carry out a By-Reference deposit using the Temporary-URL as per {{ section_link("Replacing an Object with By-Reference Files only", "b") }}


## {{ header("Replacing an Object with Packaged Content via Segmented File Upload", 2, toc="b") }}

This operation is carried out exactly as per {{ section_link("Replacing an Object with a single Binary File via Segmented File Upload", "b") }}.


# {{ header("Deleting all or part of Objects", toc="b") }}

## {{ header("Deleting an Object's Metadata", 2, toc="b") }}

Delete all the metadata fields from the Object.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Delete", "Empty Body", "Metadata-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

## {{ header("Deleting a single Binary File from an Object", 2, toc="b") }}

Delete a single File from the Object.  The server may keep old versions of the file.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Delete", "Empty Body", "File-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

## {{ header("Deleting all the Files from an Object", 2, toc="b") }}

Remove all the Files from an object.  This will leave the Object and its Metadata intact.  The server may keep old versions of the files
available.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Delete", "Empty Body", "FileSet-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

## {{ header("Deleting the entire Object", 2, toc="b") }}

Delete the Object in its entirety from the server, along with all Metadata and Files.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Delete", "Empty Body", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}


# {{ header("File Segments", toc="b") }}

## {{ header("Initialise a Segmented File Upload", 2, toc="b") }}

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Create", "Empty Body", "Staging-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

## {{ header("Upload a File Segment", 2, toc="b") }}

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Append", "File Segment", "Temporary-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

The `Content-Disposition` in this case would be:

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["File Segment Upload", "File Segment"])
}}
```


## {{ header("Abort a Segmented File Upload", 2, toc="b") }}

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Delete", "Empty Body", "Temporary-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

## {{ header("Retrieve information about a Segmented File Upload", 2, toc="b") }}

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Retrieve", "Empty Body", "Temporary-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

# {{ header("Completing Previously In-Progress Deposits", toc="b") }}

Where you have previously carried out deposits and sent the object the `In-Progress: true` header, you will eventually need to tell the
server that you have completed your additions or modifications to the Object, so that it can finalise your deposit.

{{ requirements(
    reqs="tables/requirements",
    hierarchy="tables/reqs_hierarchy",
    groups=["Request", "Content", "Resource"],
    match=["Complete", "Empty Body", "Object-URL"],
    output=["Protocol Operation", "Request Requirements", "Server Requirements", "Response Requirements"])
}}

No `Content-Disposition` header is required in this request.