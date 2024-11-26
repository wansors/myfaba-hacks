# Faba Box Hacking FAQ

## General Questions

### Q: What are the correct NFC tags to use?
A: The recommended NFC tags are NTAG213 compatible. You can find suitable tags on platforms like Temu. Here's an example link: [Temu NFC Tags](https://www.temu.com/goods.html?_bg_fs=1&goods_id=601099537125301&sku_id=17592302840204)

### Q: Can I 3D print my own Faba-compatible disks?
A: Yes, it's possible to 3D print disks similar to the original Faba ones. These custom-printed disks can work with the Faba Box.

### Q: What size should the custom disks be?
A: Custom disks should be 5cm in diameter to fit with the Faba Box (Mine are make of wood).

## Faba Box and App

### Q: What happens if I connect my Faba Box to the official app?
A: Connecting your Faba Box to the official app may result in an update that erases all folders currently stored in the Box's memory. It's recommended to avoid updating if you want to keep your existing content.

### Q: How much storage does the Faba Box have?
A: The Faba Box initially comes with about 4.5GB of storage data. After connecting to the app, this may be reduced to around 100MB for a small number of official tags.

### Q: Can I add my own audio files to the Faba Box?
A: Yes, you can add your own audio files to the Faba Box. However, you'll need to follow specific procedures to ensure they're recognized by the system.

## Hacking and Customization

### Q: How do I write a custom code to an NFC tag?
A: You'll need to use an NFC writing tool to copy the code of a character onto a blank NTAG213 tag. Specific instructions may vary depending on the tool you're using.

### Q: What should I do if the Faba Box doesn't recognize my custom tag?
A: If the box's light stays steady and doesn't make any noise when you place your custom tag, double-check that you've written the correct code to the tag and that you're using a compatible NFC tag type.

### Q: How can I decrypt the files from the Faba Box?
A: To decrypt the files:
1. Compile the Java file: `javac MKICipher.java`
2. Run the program with the path to the file you want to decrypt: `java MKICipher ../../K0403_CP01`

### Q: Is it possible to create custom characters for the Faba Box?
A: Yes, it's possible to create custom characters for the Faba Box by programming custom NFC tags. This requires knowledge of the Faba Box's tag recognition system.

## Troubleshooting

### Q: What should I do if my custom tags aren't working?
A: If your custom tags aren't working:
1. Verify that you're using NTAG213 compatible tags.
2. Double-check that you've correctly written the character code to the tag.
3. Ensure you're placing the tag correctly on the Faba Box.
4. Try using the tag with the official Faba app to see if it's recognized.

If problems persist, you may need to try a different brand or type of NFC tag.

### Q: How can I reset my Faba Box to factory settings?
A: The process for resetting a Faba Box to factory settings may vary. Generally, it involves a specific button sequence or connecting to the official app. Consult the user manual or contact Faba support for precise instructions.

### Q: What software dependencies do I need to install?
A: To work with the Faba Box and perform various hacking operations, you'll need to install:

1. Java SDK (Software Development Kit): This is required to compile and run the decryption tool.
2. id3v2: This is a command line ID3v2 tag editor. You can install it on Debian-based systems (like Ubuntu) using: sudo apt-get install id3v2
