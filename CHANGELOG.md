**v1.2.1**
* Expanded range of compatible extract-msg versions.
* Fixed bugs that prevented properly properties.

**v1.2.0**
* Updated to new version set of extract-msg (>=0.33.0, <0.34.0). Version 0.32.0 was skipped intentionally due to some issues in the code as well as to prioritize the release of version 0.33.0.
* Fixed issue where double clicking attachments no longer worked (forgot to update the type checks to use the enum).
* Fixed bug that caused streams in embedded MSG files to not be found if you loaded it to be the current MSG file.
* Fixed typo that caused string viewer to not clear (forgot to add `.ui` before a ui element name).

**v1.1.0**
* Updated to new version set of extract-msg (>=0.31.0, <0.32.0).
* Added sorting to many of the displays. Updated internal way data is handled to help this.
* Added link to readme for supporting development.

**v1.0.1**
* Fix `README` to actually be correct. A lot was copied from msg-extractor and I missed a few sections.

**v1.0.0**
* Initial release.
