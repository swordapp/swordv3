# Content Disposition

SWORD uses the `Content-Disposition` header in client requests to indicate to the server information about the payload being delivered. 
Traditionally `Content-Disposition` is an HTTP response header, but it makes sense in the PUSH context of SWORD to use this as a request 
header.  We follow {% ref RFC6266 %} for its usage.

Implementers should also note {% ref RFC5987 %} if sending filenames which require characters outside the ISO-8859-1 character set.

The general format of a Content-Disposition header is as follows:

```
Content-Disposition: [disposition type]; [disposition param]=[value]; ...
```

There are three general deposit operations in SWORD:

1. A direct upload of some content, which may be Metadata, a By-Reference document, or a Binary File (which may itself be Packaged Content)
2. A Segment Upload Initialisation
3. A segment for a Segment Upload

Each of these has a different Content-Disposition, which makes it clear to the server what it should do with that content:

## Direct Uploads:

* MUST have the disposition type `attachment`
* A Direct Upload containing Metadata MUST contain the disposition param `metadata=true`.
* A Direct Upload containing ByReference Files, MUST contain the disposition param `by-reference=true`
* A Direct Upload containing a Binary File or Packaged Content MAY contain the disposition param `filename` (or `filename*` if using a 
character set outside of ISO-8859-1).

##  Segment Upload Initialisation:

* MUST have the disposition type `segment-init`
* MUST follow the documentation in the [File Segment Upload] section of this specification on constructing the `Content-Disposition` for a 
Segment Upload Initialisation

##  Segment Upload:

* MUST have the disposition type `segment`
* MUST follow the documentation in the [File Segment Upload] section of this specification on constructing the `Content-Disposition` for 
Uploading Segments
