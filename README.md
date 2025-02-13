# myfaba-hacks
A collection of tools and scripts for customizing and enhancing your MyFaba and Faba+ storytelling box. Unlock new features, personalize your experience, and dive deeper into the world of interactive storytelling with this set of user-friendly hacks and mods.



## Create your own figure (Original Faba)
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

## Create your own figure (Faba+)
Create a folder with your own songs in faba format
```
./createFigureFabaPlus.sh <figure_ID (3 digits)> <source_folder>
```
For example for figure with ID 742
```
./createFigureFabaPlus.sh 742 /home/user/mysongs
```

Then copy it to your faba box (See FAQ).

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

---

## Using the Docker Image

If you're using Windows or prefer not to set up the scripts and dependencies manually, you can use a Docker-based alternative to run the scripts in a containerized environment. This method eliminates the need to install Java or other tools on your system and provides a clean, portable setup.

>Note: This Docker-based solution is completely optional. It is an alternative to running the scripts directly on your system. If you already have the environment set up or prefer manual execution, you can skip this section.

To use Docker, follow these instructions. Please note that **Docker must be installed** on your system for these steps to work. You can download Docker from [here](https://www.docker.com/get-started).

### Step 1: Build the Docker Image

First, build the Docker image from the provided Dockerfile. This step only needs to be done once.

Open a terminal (Linux/macOS) or Command Prompt/PowerShell (Windows) and run:

#### On Linux/macOS:

```bash
docker build -t createfigure-image .
```

#### On Windows:

Open **Command Prompt** or **PowerShell**, then run the same command:
```bash
docker build -t createfigure-image .
```

This will create a Docker image named `createfigure-image` with all the necessary dependencies to run the script.

### Step 2: Run the Docker Container

Once the image is built, use the following command to run the `createFigure.sh` script inside the container.

For example, to create a figure with ID `999` using your song files from a folder named `my-songs`, use this command:

#### On Linux/macOS:

```bash
docker run --rm -v /path/to/my-songs:/source-folder createfigure-image 999 /source-folder
```

#### On Windows:

Open **Command Prompt** or **PowerShell** and run this command:
```bash
docker run --rm -v C:\path\to\my-songs:/source-folder createfigure-image 999 /source-folder
```

Make sure to replace `C:\path\to\my-songs` with the actual path to the folder containing your songs in `.mp3` format. This folder will be mounted to the `/source-folder` directory inside the Docker container. You can use this exact name.

#### Explanation of the Command:

- `docker run`: Runs a Docker container.
- `--rm`: Automatically removes the container once it finishes running.
- `-v /path/to/my-songs:/source-folder`: Maps your local `my-songs` folder to the `/source-folder` directory inside the container. Ensure this path is correct based on your operating system.
- `createfigure-image`: The name of the Docker image you created in Step 1.
- `999 /source-folder`: These are the arguments passed to the `createFigure.sh` script, where `999` is the figure ID and `/source-folder` is the path to the source folder inside the container.

This will run the script inside the Docker container and output the files into the `/source-folder` directory, which is mapped to your local `my-songs` folder.

### What Happens After Running the Command

The script processes your `.mp3` files and creates a `K0999` folder inside your `my-songs` directory. This folder contains the modified files (e.g., `CP01`, `CP02`, etc.) and can be copied to your Faba box.

### Step 3: Follow the Remaining Instructions

After running the Docker container, follow the rest of the instructions in the [Create your own figure](#create-your-own-figure) section of this README to copy the generated files to your Faba box and write the NFC tag.

---

## Known Figure IDs

For a list of known figure IDs and their corresponding characters, please check our [TAGS list](TAGS.md).

## FAQ

For frequently asked questions and troubleshooting tips, please check our [FAQ](FAQ.md).
This addition provides a link to a separate FAQ.md file where you can include frequently asked questions and their answers. Make sure to create the FAQ.md file in the same directory as the README.md file.

## Learn More

To understand how MyFaba works and the process of analyzing and customizing it, read our detailed article:
[Hacking MyFaba: An Educational Journey into Storytelling Box Customization](https://medium.com/@wansors/hacking-myfaba-an-educational-journey-into-storytelling-box-customization-cc6fc5db719d)