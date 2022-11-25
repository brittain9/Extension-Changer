import os
import sys
import re
from pathlib import Path
import shutil

def changeFileExtension():
    '''
    Usage on command line: python3 <filename>.py <Directory of Files> <current_extension> <new_extension> [<copy> default = False]

    copy = True; will create folder inside directory with files with new extension.
    '''
    n = len(sys.argv)
    assert n > 3, "Incorrect usage. Three arguments required!"

    # NOTE: python3 is ignored as a command line argument. The .py file index 0 of argv.
    path = sys.argv[1]

    # Strip '.' from input so that user can enter .png or png
    current_extension = sys.argv[2].strip('.')
    new_extension = sys.argv[3].strip('.')

    copy = False
    # Check if the user wants to copy the files
    if n > 4:
        copy = sys.argv[4]

    # TODO: Check if valid file extension or if no file extension

    # Check valid directory,
    try:
        Path(path)
        # if an error wasn't raised. Change directory to file location
        os.chdir(path)
    except:
        print('Directory not found.')
        return False

    # Keep track of # of changed files
    changed = 0

    # If we are copying and copy_path already exists, initialize copy path. If not copy_path will be None
    copy_path = Path(path + new_extension) if os.path.exists(Path(path + new_extension))  and copy is not False else None

    # if copy and the path is None, that means we need to create the directory
    if copy is not False and copy_path is None:
        os.mkdir(new_extension)

    # Iterate through files in the path
    for file in os.listdir(path):
        try:

            # Find files ending with .current_extension; $ indicates it must be at the end of the file name
            # BUG: This doesn't work correctly a file named .png.png will turn to .heic.heic;
            if re.search(f"[.{current_extension}]$", file):
                if copy is not False:
                    # Create the new copy
                    shutil.copy(Path(file), Path(copy_path))

                    # Change directory to new folder so we can change extensions
                    os.chdir(copy_path)
                    os.rename(file, file.replace(current_extension, new_extension))

                    # Change directory back so we can keep copying
                    os.chdir(path)

                    print(f'Copied: {file} to \{new_extension}')
                else:
                    os.rename(file, file.replace(current_extension, new_extension))
                    print(f'Changed: {file}')

                changed += 1

        except WindowsError as w:
            print(w)
            return False

    print(f'{changed} extensions were changed/copied from {current_extension} to {new_extension}'
          if changed else
          'No extensions were changed/copied.' + '\n')

    return True

# Program Execution
changeFileExtension()