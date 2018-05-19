{~ html section,clazz=title ~}

{% title_slide 
    title=Usage Patterns and Requirements,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com<br><a href='https://twitter.com/richard_d_jones'>@richard_d_jones</a> <a href='https://twitter.com/cottagelabs'>@cottagelabs</a>"
%}

{~ html /section ~}


{~ html section ~}

{~ html section ~}

## The Documents

{~ html /section ~}


{~ html section ~}

### SWORD: Facilitating Deposit Scenarios

[http://dlib.org/dlib/january12/lewis/01lewis.html](http://dlib.org/dlib/january12/lewis/01lewis.html)

A review of deposit use cases found during work around SWORD and SONEX in 2012.  Each use case is supported by a number of real-world 
examples.

{~ html /section ~}


{~ html section ~}

### Data Deposit Scenarios

[http://swordapp.org/2012/07/data-deposit-scenarios/](http://swordapp.org/2012/07/data-deposit-scenarios/)

A review of research data deposit scenarios, documented during work around SWORD and SONEX in 2012.  We identified data types, sources,
and target repositories and documented them.  The document lists some real-world examples of data deposit.  It then goes on to list 
generalised requirements for data deposit and carries out a gap analysis on SWORDv2.

{~ html /section ~}


{~ html section ~}

### SWORD Community Development Document

[https://docs.google.com/document/d/1Rh80CbH3F7P8pqK4CqyEMpi-efDclETRMNqyqPO71Z0/edit](https://docs.google.com/document/d/1Rh80CbH3F7P8pqK4CqyEMpi-efDclETRMNqyqPO71Z0/edit)

A document circulated by Jisc in 2016 to gather input on case studies, implementations, requirements and sustainability options.  This
 document is written piecemeal by a number of contributors working with SWORD, so is direct input from implementer base in some cases. 

{~ html /section ~}


{~ html section ~}

### SWORD Statement of Requirements

[https://docs.google.com/document/d/1fajFcmFL4jRw4ym_pQTIyec8tqy8NKeLFhemdfqRRts/edit](https://docs.google.com/document/d/1fajFcmFL4jRw4ym_pQTIyec8tqy8NKeLFhemdfqRRts/edit)

A short document pulled together from various notes gathered by Jisc on SWORD, going into 2017.

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### Working Principles

From those documents we devised a short set of working principles that are not requirements or usage patterns, but which would be worth
keeping in mind as the project progressed.

{~ html /section ~}


{~ html section ~}

* The more optional features, the harder true interoperability
* Simpler the better - aim to remove any unusued features from SWORDv2
* Research data support is key, though not at the expense of existing features
* Make it easy for the community to engage and developers to pick up
* Make it easy to maintain and extend
* Be clear about the distinction between protocol and implementation

{~ html /section ~}


{~ html section ~}

* One single simple (as possible) document describing the protocol
* Pay attention to anti-patterns: only one file, only one metadata schema, etc.
* Prioritise current, validated and pressing use cases
* Make it easy to relate implementations to the parts of the protocol
* Minimise the effort to implement against a repository (as few special features as possible)

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### Usage Patterns

A usage pattern is what we called our single units of functionality that we wanted to support.

Smaller than a use case, larger than a user story.

All usage patterns were derived from analysis of the source documents, and from implementation experience with SWORDv2.

Full set [here](https://docs.google.com/spreadsheets/d/14gP6ZjH_QX1VjZrh3CeJdgMsML2w0S95GWdYknV3ziE/edit) (41 in total)

Some examples below.

{~ html /section ~}


{~ html section ~}

{% dl tables/usage-patterns.csv,term=Title,definition=Description,filter_field=ID,filters=UP-001|UP-002|UP-010|UP-012 %} 

{~ html /section ~}


{~ html section ~}

{% dl tables/usage-patterns.csv,term=Title,definition=Description,filter_field=ID,filters=UP-013|UP-020|UP-027|UP-034 %} 

{~ html /section ~}

{~ html /section ~}


{~ html section ~}

{~ html section ~}

### Requirements

The requirements are clean single statements about the capabilities that the specification must have.

Full set [here](https://docs.google.com/spreadsheets/d/14gP6ZjH_QX1VjZrh3CeJdgMsML2w0S95GWdYknV3ziE/edit) (66 in total)

Some examples below.

{~ html /section ~}

{~ html section ~}

{% ul tables/functional-requirements.csv,field=Requirement,filter_field=ID,filters=R-002|R-003|R-008|R-021|R-023 %}

{~ html /section ~}

{~ html section ~}

{% ul tables/functional-requirements.csv,field=Requirement,filter_field=ID,filters=R-026|R-034|R-038|R-044|R-054 %}

{~ html /section ~}

{~ html /section ~}


{~ html section,clazz=title ~}

{% title_slide 
    title=Thanks for Listening,"attribution=Richard Jones, Cottage Labs<br>richard [at] cottagelabs [dot] com<br><a href='https://twitter.com/richard_d_jones'>@richard_d_jones</a> <a href='https://twitter.com/cottagelabs'>@cottagelabs</a>"
%}

{~ html /section ~}