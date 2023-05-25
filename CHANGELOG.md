**v1.7.0**
* Updated to `extract-msg` version `>=0.41.1, <0.42`.
* Fixed a few bugs.

**v1.6.0**
* Fixed missing import in `__main__.py`.
* Updated to `extract-msg` version `>=0.39.1, <0.40`.
* Updated requirements to require Python 3.8 or greater. `extract-msg` will soon be updated to this, this update is preempting that.

**v1.5.0**
* Attempting to switch to strict semantic versioning. This version contains no breaking changes to API (possible exception is a bump to requirements), only additions.
* Bump to `extract-msg` version 0.38.4.
* Added button to export the current MSG file to a file. This works on non-embedded MSG files too.
* Filtered more of the strings through the `tr` function so that text can be translated in more places.

**v1.4.1**
* Didn't properly edit the version number for extract-msg last time.

**v1.4.0**
* Upgraded to `extract-msg` version 0.36.0.
* Fixed bug in `HexViewer` that caused the offset to be wrong.

**v1.3.0**
* Upgraded to `extract-msg` version 0.35.0. Named properties viewer has been updated to reflect the new form.

**v1.2.7**
* Fixed typo that prevented named properties on attachments from being viewed if they were a stream.
* Removed debug prints that accidentally made it into the release.
* Changed UI elements to use `ScrollPerPixel` instead of `ScrollPerItem`.

**v1.2.6**
* Fixed bugs in named property viewer.
* Fixed a bug where sorting caused various tables to display incorrectly (forgot to turn off sorting while editing them and turn it back on afterwards).

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
