# Red Ele
A python script for customizing and enhancing your MyFaba storytelling box. Unlock new features, personalize your experience, and dive deeper into the world of interactive storytelling with this set of user-friendly hacks and mods.

Faba boxes are essentially MP3 players, but for original Faba boxes they need to have files pre-obfuscated. This script can turn directory of MP3s into directory supported by your FABA box, and can also turn directory of obfuscated MKI files back into MP3s.


## Create your own figure (Original Faba red cube)
Run the script with no parameters and you can use elementary GUI to do the decryption or encryption.
![GUI Screenshot](img/GUI.png?raw=true "GUI")

Alternatively, you can run the script in command-line.

For example, to encrypt songs in `/home/user/songs` with figure ID `0742` and copy it to FABA box at `/mnt/faba/MKI01`, run:
```
./redele.py --encrypt --source-folder /home/user/songs --figure-id 0742 --target-folder /mnt/faba/MKI01
```
Or, to play your Italian red elephant Ele's audio on the computer, you can decrypt it:
```
./redele.py --decrypt --source-folder /mnt/faba/MKI01/K0010 --target-folder /home/user/elephant_ele
``` 

Write an NFC TAG with the figure ID and enjoy it!

#### On Windows:

You can use your python interpreter if you have it, but you can also download pre-built binaries on Releases page.


## Known Figure IDs

For a list of known figure IDs and their corresponding characters, please check our [TAGS list](../TAGS.md).

## FAQ

For frequently asked questions and troubleshooting tips, please check our [FAQ](../FAQ.md).
This addition provides a link to a separate FAQ.md file where you can include frequently asked questions and their answers. Make sure to create the FAQ.md file in the same directory as the README.md file.

## Learn More

To understand how MyFaba works and the process of analyzing and customizing it, read our detailed article:
[Hacking MyFaba: An Educational Journey into Storytelling Box Customization](https://medium.com/@wansors/hacking-myfaba-an-educational-journey-into-storytelling-box-customization-cc6fc5db719d)