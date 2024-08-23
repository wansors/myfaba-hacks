# myfaba-hacks
A collection of tools and scripts for customizing and enhancing your MyFaba storytelling box. Unlock new features, personalize your experience, and dive deeper into the world of interactive storytelling with this set of user-friendly hacks and mods.



## Create your own figure
Create a folder with your own songs in faba format
```
./createFigure.sh <figure_ID (3 digits)> <source_folder>
```

Then copy it to your faba box.

Write an NFC TAG with the figure ID and enjoy it!

## Cipher and decipher files
### Decipher file
```
javac MKIDecipher.java
java MKIDecipher ../../K0403_CP01
```

### Decipher file
```
javac MKICipher.java
java MKICipher ../../K0403_CP01.decipher
```