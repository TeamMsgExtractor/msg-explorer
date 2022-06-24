**v1.2.5**
* Fixed issue that cause the multiple viewer to not clear it's data.

**v1.2.4**
* Fixed issue with files with non-standard streams from custom attachment types. There were issues with viewing the streams in the tree as well as with opening them in the stream viewer.
* Switched `HexViewer` from `QPlainTextEdit` to `QTextEdit` to allow for coloring to easily differentiate the headers from the actual data.
* Added the ability to drag and drop an MSG file onto the window to open it.

**v1.2.3**
* Added `python_requires` to setup.py.

**v1.2.2**
* Added app icon.

**v1.2.1**
* Expanded range of compatible extract-msg versions.
* Fixed bugs that prevented properly viewing properties.

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
