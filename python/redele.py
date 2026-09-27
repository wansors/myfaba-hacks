#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import mutagen
import sys
import re
import utils

from pathlib import Path
from mutagen.id3 import ID3, TIT2
from mutagen.mp3 import MP3


# The MKI cipher: rotate each byte left by 3 bits, then XOR with a repeating 4-byte key.
KEY = [0x30, 0x05, 0x19, 0x20]

def _rotate_left_3(byte):
    return ((byte << 3) | (byte >> 5)) & 0xFF

# The cipher only depends on the byte value and its position mod 4, so precompute
# one 256-entry translation table per position (and its inverse for decryption).
ENCRYPT_TABLES = [bytes(_rotate_left_3(b) ^ key for b in range(256)) for key in KEY]
DECRYPT_TABLES = [bytes.maketrans(table, bytes(range(256))) for table in ENCRYPT_TABLES]


def transform(buf, tables):
    """ Apply per-position translation tables to a bytearray in place """
    for pos in range(4):
        buf[pos::4] = buf[pos::4].translate(tables[pos])
    return buf

def read_bytearray(filename):
    """ Read a whole file straight into a bytearray, without an intermediate bytes copy """
    buf = bytearray(Path(filename).stat().st_size)
    with open(filename, "rb") as f:
        f.readinto(buf)
    return buf

def encrypt_mp3(input_filename, output_filename, new_title):
    """ Strip all tags, set a single title tag and write the ciphered result """
    try:
        buf = io.BytesIO(Path(input_filename).read_bytes())
        tags = MP3(buf, ID3=ID3)
        tags.delete(buf)
        tags["TIT2"] = TIT2(encoding=3, text=new_title)
        tags.save(buf)
        Path(output_filename).write_bytes(transform(bytearray(buf.getbuffer()), ENCRYPT_TABLES))

        print(f"Encryption complete. Output file: {output_filename}")
    except Exception as e:
        print(f"Error processing {input_filename}: {e}")
        sys.exit(1)

def decipher_file(input_filename, output_filename):
    """ Reverse the cipher transformation to restore the original file """
    try:
        buf = read_bytearray(input_filename)
        Path(output_filename).write_bytes(transform(buf, DECRYPT_TABLES))

        print(f"Decryption complete. Output file: {output_filename}")
    except Exception as e:
        print(f"Error processing {input_filename}: {e}")
        sys.exit(1)
        
def main():
    
    # No CLI arguments means GUI mode: only then is gooey needed, for its folder pickers.
    # Gooey then reruns this script with the arguments, which a plain ArgumentParser handles.
    if len(sys.argv) == 1:
        from gooey import GooeyParser as ArgumentParser
        dir_chooser = {"widget": "DirChooser", "gooey_options": {"full_width": True}}
    else:
        from argparse import ArgumentParser
        dir_chooser = {}

    parser = ArgumentParser(
        prog="Red Ele",
        description="Encrypt/Decrypt myfaba box MP3s",
    )
    
    subs = parser.add_subparsers(help="commands", dest="command")
    
    encrypt_group = subs.add_parser(
        "encrypt", prog="Encrypt",
    ).add_argument_group("")
    encrypt_group.add_argument(
        "-f",
        "--figure-id",
        metavar="Figure ID",
        help="Faba NFC chip identifier (4 digit number 0001-9999)",
        default="0000"
    )
    encrypt_group.add_argument(
        "-x",
        "--extract-figure",
        action="store_true",
        help="Get figure ID from directory name (MP3 files have to be located in folder named K0001-K9999)",
    ).metavar = "Extract Figure ID"  # GUI label; plain argparse rejects metavar on store_true
    encrypt_group.add_argument(
        "-s", 
        "--source-folder",
        metavar="Source Folder",
        help="Folder with MP3 files to process.",
        **dir_chooser,
    )
    encrypt_group.add_argument(
        "-t", 
        "--target-folder",
        metavar="Target Folder",
        help="Folder where generated FABA .MKI files will be stored. Subfolder for the figure will be created.",
        **dir_chooser,
    )
    
    decrypt_group = subs.add_parser(
        "decrypt", prog="Decrypt",
    ).add_argument_group("")
    decrypt_group.add_argument(
        "-s", 
        "--source-folder",
        metavar="Source Folder",
        help="Folder with MKI files to process. Supports recursion.",
        **dir_chooser,
    )
    decrypt_group.add_argument(
        "-t", 
        "--target-folder",
        metavar="Target Folder",
        help="Folder for decrypted MP3 files.",
        **dir_chooser,
    )
    

    args = parser.parse_args()
    
    # Gooey reads our output through a pipe, as UTF-8, and drives its progress bar from it.
    # It normally runs us with "python -u" and PYTHONIOENCODING set, but not in frozen builds.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", line_buffering=True)

    if not Path(args.source_folder).is_dir():
        print(f"Error: Source folder '{args.source_folder}' does not exist or is not a directory.")
        sys.exit(1)

    if args.command=="encrypt":
        
        # monkeypatch out exceptions on invalid ID3 headers - we're only trying to delete
        # every ID3 tag after all...
        mutagen.id3._tags.ID3Header.__init__ = utils.id3header_constructor_monkeypatch
        
        if not args.extract_figure and not re.match(r"^\d{4}$", args.figure_id):
            print("Error: Figure ID must be exactly 4 digits.")
            sys.exit(1)

        mp3_files = {}
        for file in Path(args.source_folder).rglob("*"):
            if file.suffix.lower() != ".mp3" or not file.is_file():
                continue
            if args.extract_figure:
                match = re.fullmatch(r"K(\d{4})", file.parent.name)
                if not match:
                    continue
                figure = match.group(1)
            else:
                figure = args.figure_id
            mp3_files.setdefault(figure, []).append(file)

        count = sum(map(len, mp3_files.values()))
        if count == 0:
            print("No MP3 files found in the source folder.")
            sys.exit(1)

        iterator = 1
        for figure, files in mp3_files.items():
            figure_folder = Path(args.target_folder) / f"K{figure}"
            figure_folder.mkdir(parents=True, exist_ok=True)
            for filenum, file in enumerate(sorted(files), start=1):
                print(f"=========================[{iterator}/{count}]")
                print(f"Processing {file}...")
                encrypt_mp3(file, figure_folder / f"CP{filenum:02d}.MKI", f"K{figure}CP{filenum:02d}")
                iterator += 1

        print(f"Processing complete. Copy the files from '{args.target_folder}' directory to your Faba box.")
    
    if args.command=="decrypt":
        
        mki_files = [f for f in Path(args.source_folder).rglob("*") if f.suffix.lower() == ".mki" and f.is_file()]
        count = len(mki_files)
        if count == 0:
            print("No MKI files found in the source folder.")
            sys.exit(1)

        for iterator, source_file in enumerate(mki_files, start=1):
            rel_path = source_file.relative_to(args.source_folder)
            target_file = (Path(args.target_folder) / rel_path).with_suffix(".mp3")
            target_file.parent.mkdir(parents=True, exist_ok=True)
            print(f"=========================[{iterator}/{count}]")
            print(f"Processing {rel_path}...")
            decipher_file(source_file, target_file)

        print(f"Processing complete.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        try:
            from gooey import Gooey
        except ImportError:
            sys.exit("Gooey is not installed: install it for the GUI, or pass command-line arguments (see --help).")
        main = Gooey(program_name='Red Ele',
                     default_size=(600, 600),
                     progress_regex=r"^=+\[(\d+)/(\d+)]$",
                     progress_expr="x[0] / x[1] * 100",
                     encoding='UTF-8',
                     navigation="TABBED",
                    )(main)
    # Gooey reruns the script with this parameter for the actual execution.
    # Since we don't use decorator to enable commandline use, remove this parameter
    # and just run the main when in commandline mode.
    if '--ignore-gooey' in sys.argv:
        sys.argv.remove('--ignore-gooey')
    main()
