# {{ header("One Shot Package Deposit", toc="c") }}

This is the most basic use case for SWORD, which has been supported in some form since the original version.

We want to send a package to a server in a single HTTP operation, and we do not wish to have an ongoing conversation
with the server about the resource once it has been deposited.

The specific requirements for this deposit are laid out in 
[SWORD 3.0 Behaviours - Creating Objects with Packaged Content]({{ url_for("swordv3-behaviours.html", "2.6") }})

We start by defining the `Content-Disposition` required for this kind of package deposit:  

```
{{ content_disposition(
    reqs="tables/content-disposition",
    hierarchy="tables/content-disposition-hierarchy",
    groups=["Upload Type", "Content"],
    match=["Direct Deposit", "Packaged Content"])
}}
```

We can then perform an HTTP POST operation against the Service-URL, with the appropriate headers and body content:

```
{{ http_exchange(
    source="schemas/openapi",
    method="post",
    url="/Service-URL",
    include_headers=["Authorization", "Content-Disposition", "Content-Type", "Digest", "Packaging", "Location"],
    request_body="Packaged Content",
    request_headers={
        "Packaging": "http://purl.org/net/sword/3.0/package/SWORDBagIt", 
        "Content-Type": "application/zip",
        "Content-Disposition" : "attachment; filename=package.zip"
    },
    response_headers={
        "Location": "http://www.myorg.ac.uk/sword3/object/1"
    },
    response=201)
}}
```

Here, the server responds by telling us that the resource has been created (`201`) and provides the `Location` of the
created resource.

The body for the response is the **Status Document**, which in this example looks as follows: 

```
{{ json_extract(
    source="content/examples/status.json",
    exclude=["links", "forwarding", "state", "eTag", "actions"],
    insert={
        "links" : [
            {
                "@id" : "http://www.myorg.ac.uk/sword3/object1/package.zip",
                "rel" : ["http://purl.org/net/sword/3.0/terms/originalDeposit"],
                "contentType" : "application/zip",
                "packaging" : "http://purl.org/net/sword/3.0/package/SWORDBagIt",
                "depositedOn" : "[timestamp]",
                "depositedBy" : "[user identifier]",
                "status" : "http://purl.org/net/sword/3.0/filestate/unpacking",
            }
        ],
        "state" : [
            {
                "@id": "http://purl.org/net/sword/3.0/state/inWorkflow",
                "description": "the item is currently in the ingest workflow"
            }
        ],
        "actions": {
            "appendFiles": false,
            "appendMetadata": false,
            "deleteFiles": false,
            "deleteMetadata": false,
            "deleteObject": false,
            "getFiles": true,
            "getMetadata": true,
            "replaceFiles": false,
            "replaceMetadata": false
          },
        }
    )
}}
```

This contains a single entry in the `links` field, which tells us that our original package was deposited, and that
its current state is that it is `unpacking`.

The server also tells us that the item is in the ingest workflow.  This means that the single shot deposit exchange
has completed, and we are no longer able to make modifications to the item.  This can be seen explicitly in the
`actions` section of the document, which tells us that all modification operations are now unavailable, and we can
only carry out retrieve operations `getFiles` and `getMetadata`.

The deposit is therefore complete, and we do not need to interact any further.

Later, if we wished, we could retrieve the **Status Document** again to see the progress of the item through the workflow
and which files and what metadata were extracted from our deposited package.
