 
== Software Description

This repository contains a script designed to generate high-quality documentation from Asciidoctor files with templating support. Key features include:

* **Company-Branded Templates**: Use your company's templates to generate documentation with consistent guard pages, headers, footers, and a final page.
* **Automatic Template Transformation**: The script automatically converts the document template into a template file and style file to ensure proper formatting and style consistency.
* **Multi-Format Output**: Starting from an ODT file generated with Pandoc, the script produces DOCX and PDF versions of the document.

=== Additional Features

The script also allows you to:

* Specify a **reviewer** and their **title** for the document.
* Specify an **approver** and their **title**.
* Add a **confidentiality policy** to the document.
* Preserve **revision marks** from the original Asciidoctor file and integrate them into a small table that can be positioned anywhere in your document.

== How to Use

An example of script usage is provided in the `Makefile`. This example demonstrates how to generate documentation using the script.

For details on creating and testing a document template, refer to the `README` file located in the `template` directory.

== Prerequisites

Before using the script, ensure the following dependencies are installed:

=== Required Software

* `python3` with the following tools: `awk`, `sed`
* `pandoc`
* `lua` engine for Pandoc (usually included in most distributions of Pandoc)
* `libreoffice`
* `asciidoctor` with the following extensions/modules:
** `asciidoctor-diagram`
** `asciidoctor-kroki` (if using Kroki for diagrams)
** `asciidoctor-include-ext` (if advanced inclusion features are needed)
** `asciidoctor-epub3` (if generating EPUB3 documents)
** `asciidoctor-reducer` (to flatten Asciidoctor files)
* `asciimath` (for AsciiMath support)
* `ascii` (general support)
* `rqrcode` and `barby` (for generating QR codes for document URLs)

=== Installation of Asciidoctor Modules

All Asciidoctor modules can be installed using the `gem install` command. For example:

[source,bash]
----
gem install asciidoctor-diagram
gem install asciidoctor-kroki
gem install asciidoctor-reducer
----

Ensure you install any additional modules as needed based on the features you plan to use.
