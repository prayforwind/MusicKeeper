# MusicKeeper
Music file management via audio metadata.

# Prerequisite
https://pypi.org/project/audio-metadata/

# Tips
If you meet with messy code filenames, try to modify the code of pylib audio-metadata.
Because the bug is caused by audio metadata string encoding.
Search the pylib with keyword "iso-8859-1".
In my case, I add or modify "iso-8859-1" -> "gbk".
It works.
