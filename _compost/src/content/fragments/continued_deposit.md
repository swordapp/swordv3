# {{ header("Continued Deposit") }}

Some systems may wish to give the client more control over the ingest process, and SWORD uses the `In-Progress` HTTP header to allow the 
client to indicate that a deposit should not yet be injected into any post-submission or pre-ingest workflow. The `In-Progress` header MUST 
take the value `true` or `false`, and if it is not present the server MUST assume that it is `false` and behave as described below.

An example use case for this is that the client may be embedded into a system which uses the SWORD server as a storage layer, but which 
cannot acquire all of the content for a "finished" item in one deposit operation. Consider a user-facing system which encourages users to 
upload files one at a time through some web interface, which causes each file to be directly deposited onto the SWORD server. At the start 
of the deposit the client asserts that deposit is `In-Progress: true`, and then proceeds to upload files. If uploading them to the 
Object-URL the client continues to assert `In-Progress: true` on each request (if depositing to other URLs this is not necessary). This 
goes on until the user confirms that they have uploaded all the relevant files, or navigates away from the page. At that stage, the client 
can issue a blank HTTP POST request to the SWORD server, with `In-Progress: false` to complete the deposit.

Note that the `In-Progress` header is intended to indicate to the server that further content will be coming in which is associated with 
the existing content, before it can be considered "complete". It is not intended to provide workflow control, and clients MUST NOT assume 
that asserting `In-Progress: true` will have any specific effect on the state of the item.

## {{ header("Deposit Complete", 2) }}

If `In-Progress` is `false`, the server MAY assume that it can carry on processing the deposit as it sees fit.

## {{ header("Deposit Incomplete", 2) }}

If `In-Progress` is `true`, the server SHOULD expect the client to provide further updates to the item some undetermined time in the future. 
Details of how this is implemented is dependent on the server's purpose. For example, a repository system may hold items which are marked 
`In-Progress` in a workspace until such time as a client request indicates that the deposit is complete.

## {{ header("Completing a Previously Incomplete Deposit", 2) }}

The client can assert that a deposit process has completed by issuing an HTTP POST to the Object-URL with a blank request body and with the 
`In-Progress` header set to `false` (it may simply omit the header altogether too, as this is treated as `In-Progress: false` by the 
server). The client MAY specify a `Content-Length: 0` HTTP header, and MUST NOT include any body content.

* The client MAY provide an In-Progress header with a value of false
* The client MAY provide an On-Behalf-Of header

Once the server has processed the request it MUST respond with status code 204 (No Content), or a suitable error.
