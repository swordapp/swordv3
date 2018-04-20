# Structure of SWORD Objects

Objects, as represented by SWORD, have the following structure:

{% fig structure.png,Structure of a SWORD Object %}

* All Metadata and all types of Files are contained within the Object
* Some Files are expressions of the Object's metadata.
* There is a single Metadata Resource which is the abstract representation of the Metadata through which SWORD operations are carried out
* Some Files are expressions of the Object as Packaged Content
* Some Files are considered part of the "FileSet", which means they are available for SWORD operations to be carried out on them (replaced, removed)
* The Object may contain arbitrary other Files which do not fit into the above categories

The SWORD Object is expressed as JSON via the {% link Status Document %}, along with all its supporting metadata and workflow information.

Each of the three primary File categories can be identified by their `rel` values, as they appear in the {% link Status Document %}:

* Metadata Expressions: http://purl.org/net/sword/3.0/terms/formattedMetadata
* FileSet Files: http://purl.org/net/sword/3.0/terms/fileSetFile
* Packaged Content Expressions: http://purl.org/net/sword/terms/packagedContent