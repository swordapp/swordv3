# {{ header("Content Disposition") }}

SWORD uses the `Content-Disposition` header in client requests to indicate to the server information about the payload being delivered. 
Traditionally `Content-Disposition` is an HTTP response header, but it makes sense in the PUSH context of SWORD to use this as a request 
header.  We follow {{ ref("RFC6266") }} for its usage.

Implementers should also note {{ ref("RFC5987") }} if sending filenames which require characters outside the ISO-8859-1 character set.

The general format of a Content-Disposition header is as follows:

```
Content-Disposition: [disposition type]; [disposition param]=[value]; ...
```

The rules below define how to generate the correct Content-Disposition for a given set of Request Conditions. If you are implementing a SWORD client
or server it is **STRONGLY RECOMMENDED** that you work from the **[SWORDv3 Behaviours Document]({{ url_for("swordv3-behaviours.html") }})**,
as this lays out the `Content-Disposition` requirements per-request, rather than in the form of the normalised requirements below.

There are three general deposit operations in SWORD:

1. A direct upload of some content, which may be Metadata, a By-Reference document, or a Binary File (which may itself be Packaged Content)
2. A Segmented Upload Initialisation
3. A File Segment for a Segmented Upload

Each of these has a different `Content-Disposition`, which makes it clear to the server what it should do with that content.

There are two aspects which control what the Content-Disposition should be:

* The Upload Type
* The Content

The requirements below define what *Disposition Type* and *Parameters* are required for each kind of request.  The requirements should be
interpreted according to the following hierarchy for each of the above aspects:

The hierarchy for the Upload Type is:

{{ requirements_hierarchy(
    source="tables/content-disposition-hierarchy",
    key="Upload Type")
}}

The hierarchy for the Content is:

{{ requirements_hierarchy(
    source="tables/content-disposition-hierarchy",
    key="Content")
}}

So, for example, if delivering a Metadata+By-Reference Document (MD+BR) as a Direct Deposit, you would take into account the following
requirements:

* With an Upload Type of Direct Deposit: **Direct Deposit** and **All**
* With a Content type of MD+BR: **MD+BR**, **JSON**, **Body** and **All**


The requirements are:

{{ requirements_table_2(
    source="tables/content-disposition",
    vectors=["Upload Type", "Content"],
    reqs=["Disposition Type", "Param"],
    definitions="tables/content-disposition-definitions")
}}

The following examples show a number of key cases:

**A Metadata Deposit**

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Metadata"])
}}
```

**A By-Reference Deposit**

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "By-Reference"])
}}
```

**A Metadata+By-Reference Deposit**

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "MD+BR"])
}}
```

**A Binary File Deposit**

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Binary File"])
}}
```

**A Segmented Upload Initialisation**

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Segmented Upload Initialisation", "Empty Body"])
}}
```

**A File Segment Upload**

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["File Segment Upload", "File Segment"])
}}
```