import re
from pathlib import Path


def patch_test_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Prevent duplicate execution: check if the file is already patched
        if any("PYTHON = sys.executable" in line for line in lines):
            print(f"[Skip] {filepath.parent.name}/{filepath.name} is already patched.")
            return

        new_lines = []
        
        for line in lines:
            # 1. Insert 'import sys' right after 'import os'
            if line.strip() == 'import os':
                new_lines.append(line)
                new_lines.append('import sys\n')
                continue
            
            # Prevent duplication if 'import sys' is already in the original code
            if line.strip() == 'import sys' and any(l.strip() == 'import sys' for l in new_lines):
                continue
            
            # 2 & 3. Add comments and the PYTHON variable around the 'prg' declaration
            if line.startswith("prg ="):
                new_lines.append("# The script/program under test\n")
                new_lines.append(line)
                new_lines.append("\n")
                new_lines.append("# Path to the Python interpreter in the current virtual environment\n")
                new_lines.append("PYTHON = sys.executable\n")
                continue

            # 4. Replace command execution parts using regular expressions
            modified_line = line
            
            # Case A: When the argument is just 'prg' (e.g., getoutput(prg))
            modified_line = re.sub(r'getoutput\(\s*prg\s*\)', r"getoutput(f'{PYTHON} {prg}')", modified_line)
            modified_line = re.sub(r'getstatusoutput\(\s*prg\s*\)', r"getstatusoutput(f'{PYTHON} {prg}')", modified_line)
            
            # Case B: When it's an f-string (handles both single and double quotes)
            modified_line = re.sub(r'getoutput\(f([\'"]){\s*prg\s*}', r'getoutput(f\g<1>{PYTHON} {prg}', modified_line)
            modified_line = re.sub(r'getstatusoutput\(f([\'"]){\s*prg\s*}', r'getstatusoutput(f\g<1>{PYTHON} {prg}', modified_line)

            new_lines.append(modified_line)

        # Overwrite the original file with the modified content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"[Success] Patched {filepath.parent.name}/{filepath.name}")

    except Exception as e:
        print(f"[Error] Failed to patch {filepath}: {e}")


def delete_makefile(test_filepath):
    """
    Deletes Makefile or makefile if it exists in the same directory as test.py.
    """
    try:
        # Get the parent directory of the current test.py file
        folder_path = test_filepath.parent
        
        # Define possible names to handle cross-platform case-sensitivity
        makefile_names = ["Makefile", "makefile"]
        
        for name in makefile_names:
            makefile_path = folder_path / name
            
            # Check if the file exists and delete it
            if makefile_path.is_file():
                makefile_path.unlink()  # Remove the file from the filesystem
                print(f"[Delete] Removed {name} in {folder_path.name}/")
                
    except Exception as e:
        print(f"[Error] Failed to delete Makefile in {test_filepath.parent}: {e}")

# Entry point
if __name__ == "__main__":
    # Get the absolute path of the directory where this script is located
    base_dir = Path(__file__).resolve().parent.parent
    
    # Recursively find all 'test.py' files in all subdirectories without depth limits
    target_files = list(base_dir.rglob('test.py'))

    if not target_files:
        print(f"Could not find any test.py files under: {base_dir}")
    else:
        for p in target_files:
            patch_test_file(p)
            delete_makefile(p)
        print("Cross-platform compatibility patch and Makefile cleanup completed!")   