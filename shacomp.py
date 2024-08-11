#!/usr/bin/env python3

import argparse
from argparse import ArgumentParser
from pathlib import Path
from pprint import pp
from sys import stderr

def main():
    parser = ArgumentParser(
            add_help=False,
            description='Compare SHA digests'
            )

    parser.add_argument( '-N', '--newest-first', dest='forder',
                        action='store_const', const='newest',
                        default='oldest',
                        help='Assume given digests provided in order from '
                        'newest to oldest. (Default is oldest-to-newest)' )
    parser.add_argument( '-T', '--check-timestamps', dest='forder',
                        action='store_const', const='timestamp',
                        help='Check digest file timestamps to determine order' )
    parser.add_argument( '-h', '--header', action='store_true', default=None,
                        help='Display header (default if more than 2 files)' )
    parser.add_argument( '-H', '--no-header', action='store_false',
                        dest='header',
                        help='Do not display header' )
    parser.add_argument( '-f', '--first-file-changes', action='store_true',
                        dest='first', default=None,
                        help='Display change column for first digest file ' +
                        '(default if more than 2 files)' )
    parser.add_argument( '-F', '--no-first-file-changes', action='store_false',
                        dest='first',
                        help="Don't display change column for first "
                        "digest file" )
    parser.add_argument( '-u', '--show-unchanged', action='store_true',
                        help="Include files that were unchanged across "
                        "all digests" )
    parser.add_argument( '-c', '--activity-chars', default='|+-#',
                        help='Characters to display for files that are '
                        'unchanged, added, removed, or modified. '
                        '(Default "|+-#")' )
    parser.add_argument( '--help', action='help',
                        help='Show this help message' )

    parser.add_argument( 'ffile', type=Path, metavar='file',
                        help=argparse.SUPPRESS )
    parser.add_argument( 'files', nargs='+', type=Path, metavar='file',
                        help='Digest file to compare' )

    args = parser.parse_args()

    if len( args.files ) > 1:
        if args.first == None: args.first = True
        if args.header == None: args.header = True

    if len( args.activity_chars ) != 4:
        print( "ACTIVITY_CHARS must be exactly 4 characteres.", file=stderr )
        exit( 1 )

    if 0:
        print( args )
        exit()

    # List of digest files, in chronological order
    digestFiles = []
    digestFiles.append( args.ffile )
    digestFiles.extend( args.files )

    # Reverse files if they were given in reverse order
    if args.forder == 'newest':
        digestFiles.reverse()
    elif args.forder == 'timestamp':
        for f in digestFiles:
            digestFiles.sort( key=lambda f: f.stat().st_mtime )

    if 0:
        for f in digestFiles:
            print( str( f ))
        exit()

    # Set of files in all digests
    allFiles = set()
    # Data in each digest file (in same order as digestFiles)
    digests = []

    # Read all the digest files
    for digestFile in digestFiles:
        # Digest data: Key=filename, value=hash
        data = {}
        with open( digestFile ) as f:
            data = readDigests( f )
        digests.append( data )
        allFiles |= set( data.keys() )

    # Sort file list
    files = list( allFiles )
    files.sort()

    # Print header
    if args.header:
        # Extra number of pipes to print per line
        offs = 0
        # What to print before first file
        ff = ". "
        if args.first:
            offs = 1
            ff = "+--"

        print( f"{ff}{str( digestFiles[0] )}" )
        for i in range( 1, len( digestFiles )):
            print( f"{'|' * (i + offs - 1)}+--{str( digestFiles[i] )}" )
        print( "|" * (len( digestFiles ) + offs - 1) )

    # Go through each file and find changes between digests
    for file in files:
        # Were changes found in any revision?
        anyChange = False
        # Status of each file for each rev
        stat = ""

        if args.first:
            if file in digests[0]:
                stat = args.activity_chars[1]
            else:
                stat = args.activity_chars[0]

        # Go through each digest and compare to the next one
        for i in range( len( digests ) - 1 ):
            old = digests[i]
            new = digests[i + 1]
            
            if file in old and file not in new:
                # File removed from later dataset
                stat += args.activity_chars[2]
                anyChange = True
            elif file in new and file not in old:
                # File added to later dataset
                stat += args.activity_chars[1]
                anyChange = True
            elif file in old and file in new and old[file] != new[file]:
                # File changed between digests
                stat += args.activity_chars[3]
                anyChange = True
            else:
                # No change between digests
                stat += args.activity_chars[0]

        if anyChange or args.show_unchanged:
            print( f"{stat} {file}" )

def readDigests( fd ):
    """Read a snapshot file from the given file object.

    Returns a dict with filenames as keys and checksums as values.
    """
    data = {}
    for line in fd.readlines():
        (sha, filename) = line.split( ' ', maxsplit=1 )
        filename = filename.lstrip( ' ' ).rstrip( "\n" )
        data[filename] = sha
    return data

if __name__ == "__main__":
    main()



