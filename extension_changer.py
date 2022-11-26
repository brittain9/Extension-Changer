import os
import sys
import re
from pathlib import Path
import shutil

def change_file_extension() -> bool:
    """
    Usage on command line: python3 <filename>.py <Directory of Files> <current_extension> <new_extension> [<copy=True> default=False]
    copy = True; will create folder inside directory with files with new extension.
    """
    n = len(sys.argv)
    assert n > 3, "Incorrect usage. Three arguments required!"

    path = sys.argv[1]
    
    try:
        Path(path)
        os.chdir(path)
    except:
        print('Directory not found.')
        return False

    # Strip '.' from input so that user can enter .png or png
    current_extension = sys.argv[2].strip('.')
    new_extension = sys.argv[3].strip('.')
    # TODO: Check if valid file extension or if no file extension

    copy = False
    copy_path = None

    if n > 4:
        copy = sys.argv[4].lower() == "true"
        
    if not new_extension in sys.path and copy == True:
        os.mkdir(new_extension)
        print(f'New directory created: {new_extension}')
        
    if copy == True:
        copy_path = os.path.join(path, new_extension)

    files_changed = 0

    for file in os.listdir(path):
        try:
            # Find files ending with .current_extension; $ indicates it must be at the end of the file name
            # BUG: This doesn't work correctly a file named .png.png will turn to .heic.heic;
            if re.search(f"[.{current_extension}]$", file):
                
                if copy == True:
                    shutil.copy(file, copy_path)

                    # Change directory to new folder so we can change extensions
                    os.chdir(copy_path)
                    os.rename(file, file.replace(current_extension, new_extension))

                    # Change directory back so we can keep copying
                    os.chdir(path)

                    print(f'Copied: {file} to {new_extension}')
                else:
                    os.rename(file, file.replace(current_extension, new_extension))
                    print(f'Changed: {file}')

                files_changed += 1

        except WindowsError as w:
            print(w)
            return False

    print(f'{files_changed} extensions were changed/copied from {current_extension} to {new_extension}'
          if files_changed else
          'No extensions were changed/copied.' + '\n')

    return True

if __name__ == '__main__':
    change_file_extension()