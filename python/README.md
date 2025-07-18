# Red Ele
A python script for customizing and enhancing your MyFaba storytelling box. Unlock new features, personalize your experience, and dive deeper into the world of interactive storytelling with this set of user-friendly hacks and mods.

Faba boxes are essentially MP3 players, but for original Faba boxes they need to have files pre-obfuscated. This script can turn directory of MP3s into directory supported by your FABA box, and can also turn directory of obfuscated MKI files back into MP3s.

## Installation

### On Windows:

You can use your python interpreter if you have it (see linux/macos section), but you can also download pre-built binaries on [Releases page](/../../releases).

### On Linux / MacOS

- Install python3 on your system if you don't have it yet. Make sure to install `pip` as part of your python (usually done by default, but do not deselect it).
- Run `pip install -r requirements.txt` in the script directory to install prerequisites.
- Run `chmod +x redele.py` to enable running the script directly by e.g. double-clicking.
- You can now run the script directly, even double-clicking in GUI should work. Alternatively (or if you skipped previous point), you can run it using `python3 redele.py` in the script directory.

## Create your own figure (Original Faba red cube)

Run the script with no parameters and you can use elementary GUI to do the decryption or encryption.
![GUI Screenshot](img/GUI.png?raw=true "GUI")

Alternatively, you can run the script in command-line.

For example, to encrypt songs in `/home/user/songs` with figure ID `0742` and copy it to FABA box at `/mnt/faba/MKI01`, run:
```
./redele.py encrypt --figure-id 0742 --source-folder /home/user/songs --target-folder /mnt/faba/MKI01
```
Or, to play your Italian red elephant Ele's audio on the computer, you can decrypt it:
```
./redele.py decrypt --source-folder /mnt/faba/MKI01/K0010 --target-folder /home/user/elephant_ele
``` 

Write an NFC TAG with the figure ID and enjoy it!


## Known Figure IDs

For a list of known figure IDs and their corresponding characters, please check our [TAGS list](../TAGS.md).

## FAQ

For frequently asked questions and troubleshooting tips, please check our [FAQ](../FAQ.md).
This addition provides a link to a separate FAQ.md file where you can include frequently asked questions and their answers. Make sure to create the FAQ.md file in the same directory as the README.md file.

## Learn More

To understand how MyFaba works and the process of analyzing and customizing it, read our detailed article:
[Hacking MyFaba: An Educational Journey into Storytelling Box Customization](https://medium.com/@wansors/hacking-myfaba-an-educational-journey-into-storytelling-box-customization-cc6fc5db719d)