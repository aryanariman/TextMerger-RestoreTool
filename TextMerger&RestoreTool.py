import os
import re
from colorama import Fore, Style, init

init(autoreset=True)

def get_clean_path(prompt):
    path = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
    if (path.startswith('"') and path.endswith('"')) or (path.startswith("'") and path.endswith("'")):
        path = path[1:-1]
    return path

def merge_txt_files(txt_folder, base_folder):
    txt_files = [f for f in os.listdir(txt_folder) if f.lower().endswith('.txt')]
    txt_files.sort(key=lambda x: x.lower())

    merged_lines = []
    map_lines = []
    index = 1

    for file in txt_files:
        file_path = os.path.join(txt_folder, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        for line_num, line in enumerate(lines, start=1):
            merged_lines.append(line)
            map_lines.append(f"{index}::{file}::{line_num}")
            index += 1

    map_folder = os.path.join(base_folder, 'Map_Merger')
    merged_folder = os.path.join(base_folder, 'TXT_Merged')
    os.makedirs(map_folder, exist_ok=True)
    os.makedirs(merged_folder, exist_ok=True)

    merged_path = os.path.join(merged_folder, 'merged.txt')
    map_path = os.path.join(map_folder, 'merged.map')

    with open(merged_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(merged_lines))

    with open(map_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(map_lines))

    print(Fore.GREEN + "\nCreated:"+ Fore.LIGHTGREEN_EX +
          "\n\n- Merged TXT: " + Fore.RESET + f"{merged_path}" +
          Fore.LIGHTGREEN_EX + "\n- Map File: " + Fore.RESET + f"{map_path}")

def resolve_map_path(map_input):
    if os.path.isfile(map_input):
        return map_input
    if os.path.isdir(map_input):
        candidates = [f for f in os.listdir(map_input) if f.lower().endswith('.map')]
        if not candidates:
            print(Fore.RED + "No .map file found in the provided folder.")
            return None
        if 'merged.map' in candidates:
            return os.path.join(map_input, 'merged.map')
        if len(candidates) == 1:
            return os.path.join(map_input, candidates[0])
        print(Fore.RED + "Multiple .map files found. Please provide the exact .map file path.")
        return None
    print(Fore.RED + "Provided map path is neither a file nor a folder.")
    return None

def resolve_merged_path(merged_input, base_folder):
    if os.path.isfile(merged_input):
        return merged_input
    if os.path.isdir(merged_input):
        candidates = [f for f in os.listdir(merged_input) if f.lower().endswith('.txt')]
        if 'merged.txt' in candidates:
            return os.path.join(merged_input, 'merged.txt')
        if len(candidates) == 1:
            return os.path.join(merged_input, candidates[0])
        print(Fore.RED + "Multiple .txt files found. Please provide the exact merged TXT file path.")
        return None
    if not merged_input:
        default_folder = os.path.join(base_folder, 'TXT_Merged')
        default_file = os.path.join(default_folder, 'merged.txt')
        if os.path.isfile(default_file):
            return default_file
        print(Fore.RED + "No merged.txt found in default TXT_Merged folder.")
        return None
    print(Fore.RED + "Provided merged path is neither a file nor a folder.")
    return None

def split_txt_files(map_path, merged_path, base_folder):
    with open(map_path, 'r', encoding='utf-8') as f:
        map_lines = f.read().splitlines()
    with open(merged_path, 'r', encoding='utf-8') as f:
        merged_lines = f.read().splitlines()

    if len(map_lines) != len(merged_lines):
        print(Fore.RED + f"Line count mismatch: map={len(map_lines)} vs merged={len(merged_lines)}")
        return

    output_folder = os.path.join(base_folder, 'Output_TXT_Files')
    os.makedirs(output_folder, exist_ok=True)

    file_contents = {}

    for i, map_line in enumerate(map_lines):
        parts = map_line.split("::")
        if len(parts) != 3:
            print(Fore.RED + f"Malformed map line at {i+1}: {map_line}")
            return
        _, filename, line_num_str = parts
        text = merged_lines[i]
        file_contents.setdefault(filename, []).append(text)

    # چاپ مسیر خروجی یک بار
    print(Fore.LIGHTGREEN_EX + "- Output: " + Fore.RESET + f"{output_folder}\n\n")

    for filename, lines in file_contents.items():
        output_path = os.path.join(output_folder, filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        # فقط اسم فایل
        print(Fore.LIGHTBLACK_EX + f" {filename}")

    print(Fore.GREEN + "\n\nOutput processing completed.")

def main():
    print(Fore.YELLOW + "Welcome to Text Merger & Restore Tool\nAuthor: Nariman\n\n" + Style.RESET_ALL)

    print(Fore.YELLOW + "   1 -" + Style.RESET_ALL + " Merge TXT Files")
    print(Fore.YELLOW + "   2 -" + Style.RESET_ALL + " Restore Original Files\n")

    mode = input(Fore.LIGHTYELLOW_EX + "Enter your Choice (1 or 2): " + Style.RESET_ALL).strip()
    print("")

    if mode == '1':
        txt_folder = get_clean_path("\nEnter the path to the folder containing TXT files: ")
        base_folder = os.path.dirname(txt_folder)
        count = len([f for f in os.listdir(txt_folder) if f.lower().endswith('.txt')])
        print(Fore.CYAN + f"\nFound {count} TXT files in {txt_folder} \n")
        merge_txt_files(txt_folder, base_folder)

    elif mode == '2':
        map_input = get_clean_path("\nEnter the path to the Map File or Folder: ")
        base_folder = os.path.dirname(map_input)
        map_path = resolve_map_path(map_input)
        if not map_path:
            return

        merged_input = get_clean_path("\nEnter the path to the Merged TXT File or Folder: ")
        merged_path = resolve_merged_path(merged_input, base_folder)
        if not merged_path:
            return

        print(Fore.GREEN + f"\n\nProcessing pair:" +
              Fore.LIGHTGREEN_EX + "\n- Map: " + Fore.RESET + f"{map_path}\n" +
              Fore.LIGHTGREEN_EX + "- Merged: " + Fore.RESET + f"{merged_path}")

        split_txt_files(map_path, merged_path, base_folder)

    else:
        print(Fore.RED + "Invalid mode selected.")

    input(Fore.YELLOW + "\n\nPress Enter For Exit..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
