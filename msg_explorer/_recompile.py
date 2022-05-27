import os
import pathlib


def compile():
    # Now, the function we need to call will, unfortunately, try to exit python because
    # it was written thinking no one would try to run it in a script (foolish). We are
    # going to briefly override the sys.exit function so that the call to exit does
    # nothing, then restore the function afterwards.
    import sys

    lastCode = [0]
    def __dummyExit(code : int):
        """
        Dummy exit function that will store the code into lastCode.
        """
        lastCode[0] = code

    __tempExitStore = sys.exit
    sys.exit = __dummyExit

    # Now that we have replaced the function, let's call the compile calls.
    from PySide6.scripts.pyside_tool import qt_tool_wrapper

    programPath = pathlib.Path(__file__).resolve().parent / 'ui'
    for uiFile in programPath.glob('*.ui'):
        source = os.fspath(uiFile)
        output = os.fspath(uiFile.with_name(f'ui_{uiFile.stem}').with_suffix('.py'))
        # Check if the file even needs to be compiled in the first place.
        if not os.path.exists(output) or isNewer(source, output):
            qt_tool_wrapper('uic', ['-g', 'python', source, '-o', output], True)
            if lastCode[0] != 0:
                raise Exception(f'Failed to compile "{uiFile.name}".')

    # Finally, restore the exit call.
    sys.exit = __tempExitStore

def isNewer(firstFile, secondFile):
    """
    Checks if the first file is newer than the second file.
    """
    return os.path.getmtime(firstFile) > os.path.getmtime(secondFile)
