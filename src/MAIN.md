{~ html div,clazz=nav ~}
{% toc %}
{~ html /div ~}

{~ html div,clazz=spec ~}
Last modified: {% date now,%Y-%m-%d %}
{% include sections/INTRODUCTION.md %}
{% include sections/TERMINOLOGY.md %}
{% include sections/HTTP_HEADERS.md %}
{% include sections/PROTOCOL_OPERATIONS.md %}
{% include sections/PROTOCOL_REQUIREMENTS.md %}
{% include sections/DOCUMENTS.md %}
{% include sections/CONTENT_DISPOSITION.md %}
{% include sections/CONTENT_DIGESTS.md %}
{% include sections/REFERENCES.md %}
{~ html /div ~}