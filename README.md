# TXT Merge & Restore Tool

A simple Python tool for merging multiple `.txt` files into a single file while preserving their original structure through a generated map file.

This tool is especially useful for:

* Game translation projects
* Batch text editing
* Subtitle or script localization
* AI-assisted translation workflows

## Features

* Merge all TXT files in a folder into one `merged.txt`
* Automatically generate a `merged.map` file
* Restore the original TXT files after editing or translation
* Preserve original file encodings
* Supports unknown encodings using automatic detection
* Clean CLI interface with colored output

## How It Works

### Merge Mode

The tool:

1. Scans a folder for `.txt` files
2. Combines all lines into a single `merged.txt`
3. Creates a `merged.map` file containing:

   * Original filename
   * Line number
   * Original encoding

### Restore Mode

After editing or translating `merged.txt`, the tool:

1. Reads the map file
2. Splits the merged text back into the original files
3. Restores them with their original encodings

## Requirements

Install dependencies:

```bash
pip install chardet colorama
```

## Usage

Run the script:

```bash
python main.py
```

Then choose:

* `1` → Merge TXT files
* `2` → Restore original files

## Output Structure

### Merge Output

```plaintext
TXT_Merged/
 └── merged.txt

Map_Merger/
 └── merged.map
```

### Restore Output

```plaintext
Output_TXT_Files/
 └── restored txt files...
```

## Author

Nariman
