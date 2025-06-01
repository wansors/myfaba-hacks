#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import mutagen
import os
import sys
import re
import shutil
import utils

from pathlib import Path
from gooey import GooeyParser
from mutagen.id3 import ID3, TIT2
from mutagen.mp3 import MP3



# Cipher transformation tables
byte_high_nibble = [
    [0x30, 0x30, 0x20, 0x20, 0x10, 0x10, 0x00, 0x00, 0x70, 0x70, 0x60, 0x60, 0x50, 0x50, 0x40, 0x40,
     0xB0, 0xB0, 0xA0, 0xA0, 0x90, 0x90, 0x80, 0x80, 0xF0, 0xF0, 0xE0, 0xE0, 0xD0, 0xD0, 0xC0, 0xC0],
    [0x00, 0x00, 0x10, 0x10, 0x20, 0x20, 0x30, 0x30, 0x40, 0x40, 0x50, 0x50, 0x60, 0x60, 0x70, 0x70,
     0x80, 0x80, 0x90, 0x90, 0xA0, 0xA0, 0xB0, 0xB0, 0xC0, 0xC0, 0xD0, 0xD0, 0xE0, 0xE0, 0xF0, 0xF0],
    [0x10, 0x10, 0x00, 0x00, 0x30, 0x30, 0x20, 0x20, 0x50, 0x50, 0x40, 0x40, 0x70, 0x70, 0x60, 0x60,
     0x90, 0x90, 0x80, 0x80, 0xB0, 0xB0, 0xA0, 0xA0, 0xD0, 0xD0, 0xC0, 0xC0, 0xF0, 0xF0, 0xE0, 0xE0],
    [0x20, 0x20, 0x30, 0x30, 0x00, 0x00, 0x10, 0x10, 0x60, 0x60, 0x70, 0x70, 0x40, 0x40, 0x50, 0x50,
     0xA0, 0xA0, 0xB0, 0xB0, 0x80, 0x80, 0x90, 0x90, 0xE0, 0xE0, 0xF0, 0xF0, 0xC0, 0xC0, 0xD0, 0xD0]
]

byte_low_nibble_even = [[0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7],
                        [0x5, 0x4, 0x7, 0x6, 0x1, 0x0, 0x3, 0x2],
                        [0x9, 0x8, 0xB, 0xA, 0xD, 0xC, 0xF, 0xE],
                        [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7]]

byte_low_nibble_odd = [[0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF],
                       [0xD, 0xC, 0xF, 0xE, 0x9, 0x8, 0xB, 0xA],
                       [0x1, 0x0, 0x3, 0x2, 0x5, 0x4, 0x7, 0x6],
                       [0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF]]


def clear_and_set_title(mp3_file, new_title):
    """ Remove all MP3 tags and set a single title tag """
    try:
        tags = MP3(mp3_file, ID3=ID3)
        tags.delete()
        tags["TIT2"] = TIT2(encoding=3, text=new_title)
        tags.save()
    except Exception as e:
        print(f"Error processing {mp3_file}: {e}")
        sys.exit(1)

def cipher_file(input_filename):
    """ Apply custom byte transformation to an input file """
    output_filename = input_filename + ".MKI"
    try:
        with open(input_filename, "rb") as infile, open(output_filename, "wb") as outfile:
            pos = 0
            while byte_read := infile.read(1):
                byte_read = byte_read[0]
                byte_pos = pos % 4
                modified_byte = byte_high_nibble[byte_pos][byte_read % 32]
                
                if byte_read % 2 == 0:
                    modified_byte += byte_low_nibble_even[byte_pos][byte_read // 32]
                else:
                    modified_byte += byte_low_nibble_odd[byte_pos][byte_read // 32]
                
                outfile.write(bytes([modified_byte]))
                pos += 1

        return output_filename
    except IOError as e:
        print(f"Error processing {input_filename}: {e}")
        sys.exit(1)

def decipher_file(input_filename, output_filename):
    """ Reverse the cipher transformation to restore the original file """
    try:
        with open(input_filename, "rb") as infile, open(output_filename, "wb") as outfile:
            pos = 0
            while byte_read := infile.read(1):
                byte_read = byte_read[0]
                byte_pos = pos % 4

                high_byte = byte_read & 0xF0
                low_byte = byte_read & 0x0F

                index_high = byte_high_nibble[byte_pos].index(high_byte)
                if low_byte in byte_low_nibble_even[byte_pos]:
                    index_low = byte_low_nibble_even[byte_pos].index(low_byte)
                else:
                    index_low = byte_low_nibble_odd[byte_pos].index(low_byte)
                    index_high += 1
                
                original_byte = index_low * 32 + index_high
                outfile.write(bytes([original_byte]))

                pos += 1

        print(f"Deciphering complete. Output file: {output_filename}")
        return output_filename
    except IOError as e:
        print(f"Error processing {input_filename}: {e}")
        sys.exit(1)
        
def main():
    
    parser = GooeyParser(
        prog="Red Ele",
        description="Encrypt/Decrypt myfaba box MP3s",
    )
    
    encdecgroup = parser.add_mutually_exclusive_group(
        gooey_options={'initial_selection': 0}
    )
    encdecgroup.add_argument(
        "-e", 
        "--encrypt", 
        metavar="Encrypt", 
        action="store_true"
    )
    encdecgroup.add_argument(
        "-d", 
        "--decrypt", 
        metavar="Decrypt", 
        action="store_true"
    )

    main_group = parser.add_argument_group(
        "Directory to process",
        gooey_options={'columns':2}
    )
    main_group.add_argument(
        "-s", 
        "--source-folder",
        metavar="Source Folder",
        help="Source of files to process",
        widget='DirChooser',
        gooey_options={'full_width':True}
    )
    main_group.add_argument(
        "-t", 
        "--target-folder",
        metavar="Target Folder",
        help="Target of conversion. For encryption, subfolder for the figure will be created.",
        widget='DirChooser',
        gooey_options={'full_width':True}
    )
    main_group.add_argument(
        "-f", 
        "--figure-id",
        metavar="Figure ID",
        help="Four digit ID of the figure to be created (for encryption)."
    )

    args = parser.parse_args()
    
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = utils.Unbuffered(codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict'))
    if sys.stderr.encoding != 'UTF-8':
        sys.stderr = utils.Unbuffered(codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict'))    

    if not os.path.isdir(args.source_folder):
        print(f"Error: Source folder '{args.source_folder}' does not exist or is not a directory.")
        sys.exit(1)

    if args.encrypt:
        
        # monkeypatch out exceptions on invalid ID3 headers - we're only trying to delete
        # every ID3 tag after all...
        mutagen.id3._tags.ID3Header.__init__ = utils.id3header_constructor_monkeypatch
        
        if not re.match(r"^\d{4}$", args.figure_id):
            print("Error: Figure ID must be exactly 4 digits.")
            sys.exit(1)

        output_dir = os.path.join(args.target_folder, f"K{args.figure_id}")
        os.makedirs(output_dir, exist_ok=True)

        mp3_files = []
        for root, _, filenames in os.walk(args.source_folder):
            for filename in filenames:
                full_path = Path(root) / filename
                if filename.lower().endswith(".mp3"):
                    mp3_files.append(str(full_path))
        if not mp3_files:
            print("No MP3 files found in the source folder.")
            sys.exit(1)

        iterator = 1
        for file in mp3_files:
            print(f"=========================[{iterator}/{len(mp3_files)}]")
            print(f"Processing {file}...")
            
            iterator_str = f"{iterator:02d}"
            new_title = f"K{args.figure_id}CP{iterator_str}"
            source_file = os.path.join(args.source_folder, file)
            target_file = os.path.join(output_dir, f"CP{iterator_str}")

            shutil.copy(source_file, target_file)
            clear_and_set_title(target_file, new_title)

            encrypted_file = cipher_file(target_file)
            os.remove(target_file)

            iterator += 1

        print(f"Processing complete. Copy the files from '{output_dir}' directory to your Faba box.")
    
    if args.decrypt:
        
        count = 0
        mki_files = {}
        for root, _, filenames in os.walk(args.source_folder):
            for filename in filenames:
                rel_path = Path(root).relative_to(args.source_folder)
                if filename.lower().endswith(".mki"):
                    mki_files.setdefault(str(rel_path), []).append(filename)
                    count += 1

        if not mki_files:
            print("No MKI files found in the source folder.")
            sys.exit(1)

        iterator = 1
        for subdir in mki_files:
            os.makedirs(Path(args.target_folder) / subdir, exist_ok=True)
            for file in mki_files[subdir]:
                print(f"=========================[{iterator}/{count}]")
                print(f"Processing {Path(subdir) / file}...")
                source_file = str(Path(args.source_folder) / subdir / file)
                target_file = str(Path(args.target_folder) / subdir / file)
                mki_re = re.compile(re.escape('.mki'), re.IGNORECASE)
                target_file = mki_re.sub('.mp3', target_file)

                decrypted_file = decipher_file(source_file, target_file)

                iterator += 1

        print(f"Processing complete.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        from gooey import Gooey
        main = Gooey(program_name='Red Ele',
                     default_size=(1100, 820),
                     progress_regex=r"^=+\[(\d+)/(\d+)]$",
                     progress_expr="x[0] / x[1] * 100",
                     encoding='UTF-8'
                    )(main)
    # Gooey reruns the script with this parameter for the actual execution.
    # Since we don't use decorator to enable commandline use, remove this parameter
    # and just run the main when in commandline mode.
    if '--ignore-gooey' in sys.argv:
        sys.argv.remove('--ignore-gooey')
    main()
