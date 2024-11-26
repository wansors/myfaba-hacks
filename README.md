# myfaba-hacks
A collection of tools and scripts for customizing and enhancing your MyFaba storytelling box. Unlock new features, personalize your experience, and dive deeper into the world of interactive storytelling with this set of user-friendly hacks and mods.



## Create your own figure
Create a folder with your own songs in faba format
```
./createFigure.sh <figure_ID (3 digits)> <source_folder>
```
For example for figure with ID 742
```
./createFigure.sh 742 /home/user/mysongs
```

Then copy it to your faba box.

Write an NFC TAG with the figure ID and enjoy it!

## Cipher and decipher files
### Decipher file
```
javac MKIDecipher.java
java MKIDecipher ../../K0403_CP01
```

### Cipher file
```
javac MKICipher.java
java MKICipher ../../K0403_CP01.decipher
```

## Known Figure IDs

For a list of known figure IDs and their corresponding characters, please check our [TAGS list](TAGS.md).


## FAQ

For frequently asked questions and troubleshooting tips, please check our [FAQ](FAQ.md).
This addition provides a link to a separate FAQ.md file where you can include frequently asked questions and their answers. Make sure to create the FAQ.md file in the same directory as the README.md file.

## Learn More

To understand how MyFaba works and the process of analyzing and customizing it, read our detailed article:
[Hacking MyFaba: An Educational Journey into Storytelling Box Customization](https://medium.com/@wansors/hacking-myfaba-an-educational-journey-into-storytelling-box-customization-cc6fc5db719d)