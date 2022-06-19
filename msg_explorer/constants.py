import re
import string


# This expression will match any non-ascii character.
RE_SPECIAL_CHAR = re.compile(f'[^{string.printable}]|[\t\n\r\x0B\x0C]')

# This expression will match any standard file name in an MSG file.
# For files that are inside of custom attachment types, this will
# not match.
RE_STANDARD_FILE = re.compile(r'^(__properties_version1\.0)|(__substg1\.0_[0-9a-fA-F]{8}(\-[0-9a-fA-F]{8})?)$')

# This expression will match any standard folder name in an MSG file.
RE_STANDARD_FOLDER = re.compile(r'^(__attach_version1\.0_#[0-9a-fA-F]{8})|(__nameid_version1\.0)|(__recip_version1\.0_#[0-9a-fA-F]{8})$')
