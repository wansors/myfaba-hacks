# Changes in this fork

Fork: [`samuil4/myfaba-hacks`](https://github.com/samuil4/myfaba-hacks) — based on the
original project [`wansors/myfaba-hacks`](https://github.com/wansors/myfaba-hacks).
Everything described below is local to this fork and is not (yet) proposed upstream.

## 2026-09-15 — Docker build fixed and verified end-to-end

### 1. `Dockerfile` — base image updated from `bullseye` to `bookworm`

`docker build -t createfigure-image .` could not finish anymore: `debian:bullseye` is
end-of-life and its packages are no longer served from `deb.debian.org`, so every
security/update archive returned `404 Not Found` and `apt-get install` aborted with
`exit code: 100`:

```
E: Failed to fetch http://deb.debian.org/debian-security/pool/updates/main/o/openjdk-17/openjdk-17-jdk_17.0.20.1+1-1~deb11u1_amd64.deb  404  Not Found
E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
ERROR: process "/bin/sh -c apt-get update && apt-get install -y bash id3v2 openjdk-17-jre openjdk-17-jdk curl ..." did not complete successfully: exit code: 100
```

Change:

```diff
-# Use the lightweight debian:bullseye-slim image
-FROM debian:bullseye-slim
+# Use the lightweight debian:bookworm-slim image
+# (bullseye is end-of-life, its apt repositories now return 404)
+FROM debian:bookworm-slim
```

Nothing else in the `Dockerfile` was touched — Debian 12 ships the same JDK 17 and
`id3v2` that the scripts need:

| Package | Version verified inside the container |
|---|---|
| `openjdk-17-jdk` / `openjdk-17-jre` | `17.0.20.1+1-1~deb12u1` |
| `id3v2` | `0.1.12+dfsg-7` |
| `bash`, `curl` | present |

### 2. `README.md` — Windows `docker run` example used a 3-digit figure ID

`createFigure.sh` validates the figure ID with `^[0-9]{4}$`, therefore the documented
Windows example (`... createfigure-image 999 /source-folder`) fails immediately with
`Error: Figure ID must be exactly 4 digits.` The example now matches the Linux one and
uses the zero-padded ID:

```diff
-docker run --rm -v C:\path\to\my-songs:/source-folder createfigure-image 999 /source-folder
+docker run --rm -v C:\path\to\my-songs:/source-folder createfigure-image 0999 /source-folder
```

### 3. Git remotes — `origin` now points to this fork

| Before | After |
|---|---|
| `origin` → `https://github.com/wansors/myfaba-hacks.git` | `origin` → `https://github.com/samuil4/myfaba-hacks.git` (this fork — used for `pull`/`push`) |
| — | `upstream` → `https://github.com/wansors/myfaba-hacks.git` (original project, kept as read-only reference) |

Commands used, from the repository root:

```bash
git remote rename origin upstream
git remote add origin https://github.com/samuil4/myfaba-hacks.git
git fetch origin
git branch --set-upstream-to=origin/main main
```

`main` now tracks `origin/main` (the fork). To sync with the original project:

```bash
git fetch upstream
git merge upstream/main      # or: git rebase upstream/main
git push origin main
```

### 4. Verification (build + run)

```bash
docker build -t createfigure-image .
# => naming to docker.io/library/createfigure-image:latest  (image id c594b43d2162, 1.02 GB on disk / 289 MB content)

docker run --rm -v E:/projects/myfaba-hacks/src:/source-folder createfigure-image 0999 /source-folder
# => File processed successfully. Output file: /source-folder/K0999/CP01.MKI
# => Processing complete. Copy the files from '/source-folder/K0999' directory to your Faba box.
```

Result on the host: `src/K0999/CP01.MKI` (6,588,544 bytes) generated from `src/1.mp3`
(6,624,269 bytes).

Round-trip check — the generated file was deciphered again inside the container and its
ID3 tags inspected:

```bash
docker run --rm --entrypoint bash -v E:/projects/myfaba-hacks/src:/source-folder createfigure-image \
  -c "cd /app && cp /source-folder/K0999/CP01.MKI /tmp/CP01.MKI && java MKIDecipher /tmp/CP01.MKI && id3v2 -l /tmp/CP01.MKI.mp3"
```

```
Title  : K0999CP01        Artist : Artist Artist
Album  : Album Album      Track  : 1/1
Comment: Converted for Faba Box
```

=> the cipher → decipher round trip produces a valid MP3 with exactly the tags a Faba box
expects (`TALB`, `TPE1`, `TRCK`, `COMM`, `TIT2`).

Also checked: `git push --dry-run origin main` against the new remote finishes without
asking for credentials (`Everything up-to-date`).

### 5. Notes / pitfalls

- **The figure ID must be exactly 4 digits** — for figure `999` pass `0999`.
- **`-v` needs both paths**: `-v <host-folder>:/source-folder`, and the container path must
  match the second script argument (`/source-folder`). Omitting `:<container-path>` makes
  Docker create an anonymous volume instead of a bind mount, so the generated files never
  reach the host.
- **Windows usage** (exactly as verified on this machine):

  ```powershell
  docker build -t createfigure-image .
  docker run --rm -v E:/projects/myfaba-hacks/src:/source-folder createfigure-image 0999 /source-folder
  ```
- The local `src/` folder (`1.mp3` + the generated `K0999/`) is **not** part of the
  repository: `.gitignore` covers `**.mp3` and `/K0*/` (the latter only for root-level
  folders, which is why `src/` shows up as untracked locally — do not commit it).
- The container runs as `root`, so files created on a bind mount are owned by root on
  Linux/macOS (irrelevant on Windows / Docker Desktop).
