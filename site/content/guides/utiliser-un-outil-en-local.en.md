---
draft: true
title: "Using a tool locally"
description: "Install Python, download a jerlash.labs tool, check its SHA-256 hash and run it on Windows."
niveau: "debutant"
derniere_verification: 2026-10-31
slug: "using-a-tool-locally"
traduction:
  source: "d3a39f9456e01060407f0aaac1a056f5d283da21"
---

By the end of this guide, you will have installed a jerlash.labs tool on your Windows computer, checked that the downloaded file is indeed the one that was published, and run the tool.

## What “locally” means

A local tool runs on your computer. The documents you give it are read on your machine and do not leave it, unless the tool page states that it calls on an AI provider. In that case, the tool page describes precisely what is sent and to whom.

The jerlash.labs tools are written in Python, a free and very widely used language. You need to install it once; after that, each tool is launched with a double-click.

## Prerequisites

- A computer running Windows 10 or 11, with the right to install a program (otherwise, contact your IT provider and pass this guide on to them).
- About ten minutes the first time.

## Steps

### Installing Python

1. Open [python.org/downloads](https://www.python.org/downloads/) and download the version offered for Windows. Any version 3.10 or later will do.
2. Run the installer and follow its screens. If it offers an option to add Python to the PATH, tick it. [À VÉRIFIER sur un poste Windows vierge : libellés exacts de l'installateur actuel]
3. Check the installation: open the Start menu, type `PowerShell`, open it, type `python --version` and press Enter. A line such as `Python 3.12.10` should appear.

### Downloading the tool and checking its hash

4. On the tool page, click “Download”. The file lands in your `Downloads` folder.
5. In PowerShell, type the following command, adjusting the file name:

   ```
   Get-FileHash "$HOME\Downloads\controle-avant-envoi-0.1.0.zip" -Algorithm SHA256
   ```

6. Compare the string of characters shown under `Hash` with the SHA-256 hash given on the tool page. Upper and lower case do not matter. If the two differ, do not use the file: delete it and report it.

The hash is a kind of digital signature of the file: the slightest change to the file produces a completely different hash. This check guarantees that you have exactly the published file, and not a version altered along the way.

### Unzipping and running

7. Right-click the `.zip` file, choose “Extract All…”, then choose a permanent folder, for example `Documents\Tools`.
8. Open the extracted folder and double-click the file ending in `.pyw` (for example `Controle avant envoi.pyw`). The tool's window opens.
9. If Windows asks you which program to open the file with, choose “Python”. If the file opens in a text editor, right-click it, choose “Open with”, then “Python”.

### Updating

10. When a new version is published (see [Updates](/nouveautes/)), download it, check its hash and replace the old folder with the new one.

## Points to watch

- Only download a tool from its tool page on jerlash.labs, and always check the hash.
- Keep the tool outside your client case files and outside folders synchronised with third parties.
- A local tool that calls on an AI requires your API key: the tool page and the dedicated guide explain how to protect it. The Pre-send check tool does not need one.
- The tools also work on Mac or Linux: install Python 3.10 or later, then run `python3 "Controle avant envoi.pyw"` from the tool's folder.

## Sources

- Python Software Foundation, download page: [python.org/downloads](https://www.python.org/downloads/), consulted on 31 October 2026.
- Microsoft, documentation for the `Get-FileHash` command: [learn.microsoft.com](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/get-filehash), consulted on 31 October 2026.
