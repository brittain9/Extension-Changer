import os
import sys
import re
from pathlib import Path

def changeFileExtension():
    '''
    :return: True if file extensions changed. False otherwise.
    '''
    assert len(sys.argv) >= 4, "Incorrect usage. Three arguments required!"
    # first argument is always the .py file; python3 is ignored in cmd;
    path = sys.argv[1]
    curExt = sys.argv[2].strip('.')
    newExt = sys.argv[3].strip('.')

    # TODO: Check if valid file extension or if no file extension

    try:
        p = Path(path)
    except:
        print('Directory not found.')
        return False

    newPath = os.path.join(os.getcwd(), path)
    os.chdir(newPath)

    extChanged = 0
    for f in os.listdir(newPath):
        # TODO: take in another argument if user wants to create new files and so they can keep old ones.
        try:
            if(re.search(f"[.{curExt}]$", f)):
                print(f'Renaming file: {f}')
                os.rename( f, f.replace(curExt, newExt))
                extChanged += 1
        except WindowsError as w:
            print(w)
            return False

    print(f'{extChanged} extensions were changed from .{sys.argv[2]} to .{sys.argv[3]}')
    return True

def main():
    changed = changeFileExtension()
    print('Success' if changed else 'Failure' + '\n')

# Program execution
main()