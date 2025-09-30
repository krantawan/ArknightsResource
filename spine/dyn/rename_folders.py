#!/usr/bin/env python3
import os
import sys

def process_atlas_files(folder_path):
    """Process .atlas files in the folder and replace # with _ in line 2"""
    atlas_count = 0
    for file in os.listdir(folder_path):
        if file.endswith('.atlas'):
            atlas_path = os.path.join(folder_path, file)
            try:
                with open(atlas_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if len(lines) >= 2 and '#' in lines[1]:
                    # Replace # with _ in line 2 (index 1)
                    lines[1] = lines[1].replace('#', '_')

                    with open(atlas_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    print(f"  ✓ Updated .atlas file: {file}")
                    atlas_count += 1
            except Exception as e:
                print(f"  ✗ Error processing {file}: {e}", file=sys.stderr)

    return atlas_count

def rename_files_in_folder(folder_path):
    """Rename files with # to _ inside the folder"""
    file_count = 0
    for file in os.listdir(folder_path):
        if '#' in file:
            new_file = file.replace('#', '_')
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_file)

            try:
                os.rename(old_path, new_path)
                print(f"  ✓ Renamed file: {file} -> {new_file}")
                file_count += 1
            except Exception as e:
                print(f"  ✗ Error renaming file {file}: {e}", file=sys.stderr)

    return file_count

def rename_folders():
    """Rename folders from 'dyn_illust_' to 'dyn_illust_char_' and process contents"""
    current_dir = os.getcwd()
    renamed_folder_count = 0
    total_files_renamed = 0
    total_atlas_updated = 0

    # Get all items in current directory
    items = os.listdir(current_dir)

    for item in items:
        # Check if it's a directory and starts with 'dyn_illust_'
        if os.path.isdir(item) and item.startswith('dyn_illust_'):
            folder_to_process = item

            # Check if it doesn't already have 'char_' in the name
            if not item.startswith('dyn_illust_char_'):
                # Create new name by inserting 'char_' after 'dyn_illust_'
                new_name = item.replace('dyn_illust_', 'dyn_illust_char_', 1)
                # Replace # with _
                new_name = new_name.replace('#', '_')

                try:
                    os.rename(item, new_name)
                    print(f"✓ Renamed folder: {item} -> {new_name}")
                    renamed_folder_count += 1
                    folder_to_process = new_name
                except Exception as e:
                    print(f"✗ Error renaming {item}: {e}", file=sys.stderr)
                    continue

            # Process files inside the folder (whether renamed or not)
            print(f"  Processing contents of {folder_to_process}...")
            files_renamed = rename_files_in_folder(folder_to_process)
            atlas_updated = process_atlas_files(folder_to_process)

            total_files_renamed += files_renamed
            total_atlas_updated += atlas_updated

    print(f"\n=== Summary ===")
    print(f"Folders renamed: {renamed_folder_count}")
    print(f"Files renamed: {total_files_renamed}")
    print(f"Atlas files updated: {total_atlas_updated}")

if __name__ == "__main__":
    print("Starting folder rename process...")
    print("This will rename folders from 'dyn_illust_*' to 'dyn_illust_char_*'")
    print("and replace '#' with '_' in folder names\n")

    rename_folders()
