shacomp(1) -- Compare SHA (or other) checksums between snapshots
================================================================

SYNOPSIS
--------

`shacomp` [-N] [-T] [-h] [-H] [-f] [-F] [-u] [-c ACTIVITY_CHARS] [--help] file file [file ...]

DESCRIPTION
------------

`shacomp` will read multiple files ("snapshots") of SHA (or other) checksums,
and display a summary of what files were changed in between each one.

Snapshots are expected to be in a format smilar to that output by `sha*sum` or
`md5sum`: A checksum, followed by some number of spaces, followed by the
filename, one line per file.

The simplest case is running `shacomp` on two checksum files, which will show
what changes were detected between them. This will produce a report similar to
the following:

```
- /tmp/sortELfgNZ
- /tmp/sortL93Y32
+ /tmp/sortdxUTk2
+ /tmp/sorte9MJK5
# /var/lib/mlocate/mlocate.db
# /var/lib/mysql/ib_logfile0
```

Each file is preceeded by a symbol which shows the nature of the change:

* A `+` indicates an "addition": It was present in the older digest, but not the
  newer.
* A `-` indicates a "deletion": It was present in the newer digest, but not the
  older.
* A `#` indicates a "modification": It was present in both digests, but with a
  differing checksum.

By default, files which are "unchanged" -- they exist in both
digests, with the same checksum -- are not listed.

`shacomp` can also compare multiple digest files. If more than two files are
provided, it will track changes across all of them, giving a more detailed
report:

```
+--telos-digest-1722816420-Aug04-05.07pm-0700.sha
|+--telos-digest-1722830639-Aug04-09.03pm-0700.sha
||+--telos-digest-1722926516-Aug05-11.41pm-0700.sha
|||+--telos-digest-1723064401-Aug07-02.00pm-0700.sha
||||+--telos-digest-1723150801-Aug08-02.00pm-0700.sha
|||||+--telos-digest-1723237201-Aug09-02.00pm-0700.sha
||||||
+|#||| /etc/passwd
+##||| /etc/shadow
|+-||| /tmp/sort4hPmeO
||||+| /var/spool/postfix/maildrop/0418E2C0C1A
```

The first few lines lists the checksum files provided. Following that is a
list of all files that were changed at any point, preceeded by a set of
symbols showing where changes were detected.

Each symbol represents one of the checksum files; it shows what changed in
*that* snapshot. I.E. what changed between that snapshot and the
*previous* snapshot.

The set of symbols are the same as in the first example, with one addition: A
`|` indicates that a file was unchange between snapshots. I.E. Either it
appeared in both files, with the same checksum, or did not appear in either
file.

Note that this report includes a column for the *first* snapshot. Since there
is no "previous" snapshot to compare to (and thus, no meaningful possibility
of "removal" or "modification"), this column will always contain either a `+`
(if the file was present in the first snapshot), or a `|` (if it was not).
This makes it slighly easier to see which snapshot a file first appeared in,
and makes the display overall more consistent.

Similar to the first example, a file will not be listed if it was unchanged
across *all* snapshots.

OPTIONS
--------

* `-N`, `--newest-first`:
  In order to generate a meaningful report, `shacomp` needs to know the
  chronological order of the checksum snapshots; otherwise, the "when" of file
  changes would get mixed up. By default, `shacomp` assumes that the files
  given on the command line are in chronological order, from oldest to newest.
  This option causes `shacomp` to assume they are provided in the reverse
  order.

* `-T`, `--check-timestamps`:
  This option causes `shacomp` to check the timestamps of the snapshot files to
  see what order they should be processed in. In this mode, it does not matter
  what order they are specified on the command line.

* `-h`, `--header`:
  Display a header showing the given snapshot files. The default if more than 2
  files are given.

* `-H`, `--no-header`:
  Do not show the header

* `-f`, `--first-file-changes`:
  Displays a column for the first snapshot. The default if more than 2 files
  are given.

* `-F`, `--no-first-file-changes`:
  Do not dispay a column for the first snapsnot.

* `-u`, `--show-unchanged`:
  Include files that were unchanged across all snapshots

* `-c`, `--activity-chars`:
  Specify the symbols used to indicate each type of file change. This should be
  a 4 character string where the symbol for unchanged, added, deleted, and
  modified files should be specified, in that order. Default is "|+-#".

NOTES
-----

`shacomp` is written in Python. It targets Python 3.9, and thus will run using pypy.

This manual page was created using ronn(1).

COPYRIGHT
----------

`shacomp` is Copyright 2024 Nathan Roberts <nroberts@tardislabs.com>.

This project is licensed under the terms of the MIT license.
