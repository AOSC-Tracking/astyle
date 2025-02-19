#! /usr/bin/python3
""" Library files for AStyle test modules.
    All directories and filepaths should be in this module.
    Executed as stand-alone it will run a series of tests.
"""

# to disable the print statement and use the print() function (version 3 format)
from __future__ import print_function

import os
import platform
import subprocess
import sys
import time

if os.name == "nt":
    import msvcrt		# Windows only for get_ch()
else:
    import termios		# Linux only for get_ch()
    import tty

# global variables ------------------------------------------------------------

# test project IDs
CODEBLOCKS   = "CodeBlocks"
LSOF         = "lsof"
JEDIT        = "jEdit"              # Java
LIBSBASE     = "libsBase"           # Objective-C
SCITE        = "SciTE"
SHARPDEVELOP = "SharpDevelop"       # C# - Compile on Windows only
SHARPMAIN    = "SharpDevelopMain"   # C# - 1000 files from SharpDevelop
TESTPROJECT  = "TestProject"
# GWORKSPACE   = "GWorkspace"         # Objective C - Old, doesn't have latest changes
# KDEVELOP     = "KDevelop"           # C++ - To complicated to compile on Windows
# MONODEVELOP  = "MonoDevelop"        # C# - To complicated to compile on Windows


# astyle test options

# OPT0
# no options
OPT0 = ""

# OPT1
# align-pointer=type (k1), add-braces (j), break-blocks=all (F),
#     min-conditional-indent=0 (m0), pad-oper (p), pad-oparen (P)
#     obj-c (xMxQxqxSxP1)
OPT1 = "-CSKNLwxwxWYM50m0FpPHUEk1yexbjOocxMxQxqxSxP1"

# OPT2
# align-pointer=name (k3), align-reference=type (W1),
#     add-one-line-braces (J), break-blocks (f),
#     min-conditional-indent=3 (m3), pad-paren-out(d)
#     pad-oper (p), delete-empty-lines (xe)
#     obj-c (xMxRxrxsxP0)
# WITHOUT: keep-one-line-blocks (O), keep-one-line-statements (o),
OPT2 = "-xGSKNLwxWM60m3fpdHUxeEk3W1eJcxMxRxrxsxP0"

# OPT3
# align-pointer=middle (k2), align-reference=name (W3),
#     min-conditional-indent=1 (m1), pad-paren-in(D)
#     remove-braces (xj),
# WITHOUT: indent-classes (C), indent-switches (S),
#     indent-cases (K), indent-namespaces (N),
#     indent-labels (L), indent-preproc-define (w),
#     add-braces (j,J), break-blocks (f,F),
#     pad-oper (p), delete-empty-lines (xe)
OPT3 = "-xwM80m1DyHUEk2W3xbxjxyxpxkxVxcxlxnxdxgxt2"

# OPT4
# align-pointer=type (k1), add-braces (j), break-blocks=all (F),
#     min-conditional-indent=0 (m0), pad-oper (p), pad-oparen (P)
#     obj-c (xMxQxqxSxP1)
OPT4 = "-CSKNLwxwxWYM50m0FpPHUEyexbjOoc"

# TEST SEPARATELY
# max-code-length (xC), break-after-logical (xL)
# -xC# -xL

# compile configurations
DEBUG     = "debug"
RELEASE   = "release"
STATIC    = "static"
STATIC_XP = "static-xp"

# Visual Studio release
#VS_RELEASE = "vs2015"
VS_RELEASE = "vs2017"
#VS_RELEASE = "vs2019"
# for a new release add a path to compile_windows_executable() below

# test directory name
TEST_DIRECTORY = "TestData"

# multiple extensions in single directory
USE_MULTIPLE_EXTENSIONS = True

# -----------------------------------------------------------------------------

def build_astyle_executable(config):
    """Build the astyle executable.
    """
    if config == DEBUG:
        print("Building AStyle Debug")
    elif config == RELEASE:
        print("Building AStyle Release")
    elif config == STATIC and os.name == "nt":
        print("Building AStyle Static")
    elif config == STATIC_XP and os.name == "nt":
        print("Building AStyle Static XP")
    else:
        system_exit("Bad arg in build_astyle_executable(): " + config)
    slnpath = get_astyle_build_directory(config)
    if os.name == "nt":
        if config == STATIC_XP:
            slnpath = slnpath + "/AStyle XP.sln"
        elif VS_RELEASE >= "vs2019":
            # add vs release date
            slnpath = slnpath + "/AStyle " + VS_RELEASE[2:] + ".sln"
        else:
            slnpath = slnpath + "/AStyle.sln"
        compile_windows_executable(slnpath, config)
    else:
        compile_linux_executable(slnpath, config)

# -----------------------------------------------------------------------------

def compile_linux_executable(slnpath, config):
    """Compile the astyle executable for Linux.
    """
    if config == DEBUG:
        build = ["make", "debug"]
    else:
        build = ["make", "release"]
    buildfile = get_temp_directory() + "build." + config + ".tmp"
    if os.path.exists(buildfile):
        remove_build_file(buildfile)
    outfile = open(buildfile, 'w')
    retval = subprocess.call(build, cwd=slnpath, stdout=outfile)
    if retval:
        system_exit("Bad build return: " + str(retval))
    outfile.close()
    remove_build_file(buildfile)

# -----------------------------------------------------------------------------

def compile_windows_executable(slnpath, config):
    """Compile the astyle executable for Windows.
    """
    # remove the cache file as a precaution
    cachepath = slnpath + "/AStyle.sln.cache"
    if os.path.isfile(cachepath):
        os.remove(cachepath)
    # call MSBuild
    if VS_RELEASE == "vs2015":
        buildpath = "C:/Program Files (x86)/MSBuild/14.0/Bin/MSBuild.exe"
    elif VS_RELEASE == "vs2017":
        buildpath = ("C:/Program Files (x86)/Microsoft Visual Studio/"
                     + "2017/Community/MSBuild/15.0/Bin/MSBuild.exe")
    elif VS_RELEASE == "vs2019":
        buildpath = ("C:/Program Files (x86)/Microsoft Visual Studio/"
                     + "2019/Community/MSBuild/Current/Bin/MSBuild.exe")
    else:
        system_exit("Must compile with vs2015 or greater in libastyle: " + VS_RELEASE)
    if platform.architecture()[0] == "32bit":        # if running on a 32-bit system
        buildpath = buildpath.replace("Program Files (x86)", "Program Files")
    if not os.path.isfile(buildpath):
        message = "Cannot find build path: " + buildpath
        system_exit(message)
    if config == DEBUG:
        config_prop = "/property:Configuration=Debug"
    elif config in (STATIC, STATIC_XP):
        config_prop = "/property:Configuration=Static"
    else:
        config_prop = "/property:Configuration=Release"
    platform_prop = "/property:Platform=Win32"
    if VS_RELEASE >= "vs2015":
        platform_prop = "/property:Platform=x86"
    msbuild = ([buildpath, config_prop, platform_prop, slnpath])
    buildfile = get_temp_directory() + "/build." + config + ".tmp"
    if os.path.exists(buildfile):
        remove_build_file(buildfile)
    outfile = open(buildfile, 'w')
    retval = subprocess.call(msbuild, stdout=outfile)
    if retval:
        system_exit("Bad msbuild return: " + str(retval))
    outfile.close()
    remove_build_file(buildfile)

# -----------------------------------------------------------------------------

def create_ramdrive():
    """Create a ram drive as drive R: using OSFMount.
       The ramdrive is NOT deleted by the python scripts.
       Uses the defaults except for the drive letter (R:).
           -a            Mount a virtual disk.
           -t vm         Indicates RAM disk.
           -m R:         Specifies a drive letter
           -o format...  Volume label, format with ntsf (fastest) or fat32.
           -s 512M       Size in (M)egabytes or (G)igabytes.
       shell=True on subprocess.call for elevated privileges.
       There is a Help.exe file in the "Program Files/OSFMount" folder.
    """
    if os.name != "nt":
        return
    if os.path.exists("R:"):
        return
    exepath = "C:/Program Files/OSFMount/OSFMount.com"
    if not os.path.exists(exepath):
        system_exit("OSFMount not installed: " + exepath)

    # create version 2 ramdrive
    #ramdrive = ([exepath, "-a", "-t", "vm", "-m", "R:", "-o", "format:\"RAMDRIVE\"", "-s", "512M"])

    # create V3 BETA 2 ramdrive from 2019/01/25
    # had problems with "format:ntfs:\"RAMDRIVE\"" command
    # the ntfs option is not documented in osfmount_Help.exe
    # return code 8, but seems to run ok
    ramdrive = ([exepath, "-a", "-t", "vm", "-m", "R:", "-o", "format:ntfs:\"RAMDRIVE\"", "-s", "512M"])

    # must use a shell to get elevated (administrative) privileges
    # the output cannot be redirected from a shell
    retval = subprocess.call(ramdrive, shell=True)
    if retval:
        system_exit("Bad ramdrive return: " + str(retval))
    os.mkdir("R:/" + TEST_DIRECTORY)

# -----------------------------------------------------------------------------

def get_7zip_path():
    """Get the 7zip executable path for the os environment.
    """
    if os.name == "nt":
        exepath = "C:/Program Files/7-Zip/7z.exe"
    else:
        exepath = "7zz"
    return exepath

# -----------------------------------------------------------------------------

def get_archive_directory(endsep=False):
    """Get the archives directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_archive_directory(): " + str(endsep))
    arcdir = get_project_directory() + "/TestArchives"
    if not os.path.isdir(arcdir):
        message = "Cannot find archive directory: " + arcdir
        system_exit(message)
    if endsep:
        arcdir += '/'
    return arcdir

# -----------------------------------------------------------------------------

def get_astyle_build_directory(config):
    """Get the AStyle build path for the os environment.
    """
    if config not in (DEBUG, RELEASE, STATIC, STATIC_XP):
        system_exit("Bad arg in get_astyle_build_directory(): " + config)
    astyledir = get_astyle_directory()
    if os.name == "nt":
        if config == STATIC_XP:
            subpath = "/build/" + VS_RELEASE + "-xp"
        else:
            subpath = "/build/" + VS_RELEASE
    else:
        subpath = "/build/gcc"
    astylepath = astyledir + subpath
    if not os.path.isdir(astylepath):
        message = "Cannot find astyle build directory: " + astylepath
        system_exit(message)
    return astylepath

# -----------------------------------------------------------------------------

def get_astyle_directory(endsep=False):
    """Get the AStyle directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_astyle_directory(): " + str(endsep))
    if os.name == "nt":
        astyledir = get_project_directory() + "/AStyle"
    else:
        astyledir = get_project_directory() + "/AStyle"
        if not os.path.isdir(astyledir):
            astyledir = get_project_directory() + "/astyle"
    if not os.path.isdir(astyledir):
        message = "Cannot find astyle directory: " + astyledir
        system_exit(message)
    if endsep:
        astyledir += '/'
    return astyledir

# -----------------------------------------------------------------------------

def get_astyleexe_directory(config, endsep=False):
    """Get the AStyle executable directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_astyleexe_directory(): " + str(endsep))
    if config not in (DEBUG, RELEASE, STATIC, STATIC_XP):
        system_exit("Bad arg in get_astyleexe_directory(): " + config)
    astyledir = get_astyle_directory()
    if os.name == "nt":
        subpath = "/build/" + VS_RELEASE + "/bin"
        if config == DEBUG:
            subpath = subpath.replace("bin", "debug")
        elif config == STATIC:
            subpath = subpath.replace("bin", "binstatic")
        elif config == STATIC_XP:
            subpath = subpath.replace("bin", "binstatic_xp")
    else:
        subpath = "/build/gcc/bin"
    astylepath = astyledir + subpath
    if not os.path.isdir(astylepath):
        message = "Cannot find astyleexe directory: " + astylepath
        system_exit(message)
    if endsep:
        astylepath += '/'
    return astylepath

# -----------------------------------------------------------------------------

def get_astyleexe_path(config):
    """Get the AStyle executable path for the os environment.
    """
    if config not in (DEBUG, RELEASE, STATIC, STATIC_XP):
        system_exit("Bad arg in get_astyle_path(): " + config)
    astyledir = get_astyleexe_directory(config, True)
    if os.name == "nt":
        if config == DEBUG:
            progname = "AStyled.exe"
        else:
            progname = "AStyle.exe"
        astylepath = astyledir + progname
        if not os.path.isfile(astylepath):
            message = "Cannot find astyleexe path: " + astylepath
            system_exit(message)
    else:
        if config == DEBUG:
            progname = "astyled"
        else:
            progname = "astyle"
        astylepath = astyledir + progname
    return astylepath

# -----------------------------------------------------------------------------

def get_astyletest_directory(endsep=False):
    """Get the AStyleTest directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_astyletest_directory(): " + str(endsep))
    if os.name == "nt":
        astyletestdir = get_project_directory() + "/AStyleTest"
    else:
        astyletestdir = get_project_directory() + "/AStyleTest"
        if not os.path.isdir(astyletestdir):
            astyletestdir = get_project_directory() + "/astyletest"
    if not os.path.isdir(astyletestdir):
        message = "Cannot find astyletest directory: " + astyletestdir
        system_exit(message)
    if endsep:
        astyletestdir += '/'
    return astyletestdir

# -----------------------------------------------------------------------------

def get_ch():
    """get_ch() for Windows and Linux.
       This won't work unless run from a terminal.
    """
    # this must be executed from a terminal
    if not is_executed_from_console():
        system_exit("libastyle.get_ch() must be run from the console")
    # WINDOWS uses msvcrt
    if os.name == "nt":
        # clear buffer
        while msvcrt.kbhit():
            msvcrt.getch()
        # read char
        ch_in = msvcrt.getch()
    # LINUX uses termios and tty
    else:
        # clear buffer
        sys.stdin.flush()
        # read char
        fd_in = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd_in)
        try:
            tty.setraw(sys.stdin.fileno())
            ch_in = sys.stdin.read(1)
            if ch_in == '\x1b':			# alt key (27)
                ch_in = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd_in, termios.TCSADRAIN, old_settings)
    return ch_in

# -----------------------------------------------------------------------------

def get_diff_path():
    """Get the diff executable path for the os environment.
    """
    if os.name == "nt":
        exepath = "C:/Program Files" + "/WinMerge/WinMergeU.exe"
        if not os.path.isfile(exepath):
            message = "Cannot find diff path: " + exepath
            system_exit(message)
    else:
        exepath = "diff"
    return exepath

# -----------------------------------------------------------------------------

def get_file_py_directory(endsep=False):
    """Get the file-py directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_file_py_directory(): " + str(endsep))
    # get the path where this file is located
    pydir = sys.path[0]
    if endsep:
        pydir += '/'
    # verify it is executed from fixed disk and not a USB
    if os.name == "nt":
        if pydir[0:2].upper() != "C:":
            system_exit("File executed from drive " + pydir[0:2])
    #else:
        #--if pydir[0:6] != "/home/":
          #  system_exit("File executed from " + pydir)
    return pydir

# -----------------------------------------------------------------------------

def get_formatted_time():
    """Get the current time for printing.
    """
    tm = time.strftime("%I:%M")
    if tm[0] == '0':
        tm = tm.replace('0', ' ', 1)
    return tm

# -----------------------------------------------------------------------------

def get_home_directory(endsep=False):
    """Get the home directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_home_directory(): " + str(endsep))
    if os.name == "nt":
        homedir = os.getenv("USERPROFILE")
        homedir = homedir.replace('\\', '/')
    else:
        homedir = os.getenv("HOME")
    if endsep:
        homedir += '/'
    return homedir

# -----------------------------------------------------------------------------

def get_project_directory(endsep=False):
    """Get the Project directory for the os environment.
       Extract the Project directory from sys.path[0]
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_project_directory(): " + str(endsep))
    # get project directory
    pydir = get_file_py_directory()

    projdir = os.path.realpath(pydir + "../../../")
    #~ print("project directory = " + projdir)
    if endsep:
        projdir += '/'

    return projdir

# -----------------------------------------------------------------------------

def get_project_excludes(project):
    """Get the project excludes list for AStyle processing.
       Argument must be one of the global variables.
       Returns a list of excludes.
    """
    excludes = []
    if project == SCITE:
        excludes.append("--exclude=lua")
    elif project == SHARPDEVELOP:
        excludes.append("--exclude=Debugger.Tests")    # xml data
    return excludes

# -----------------------------------------------------------------------------

def get_project_filepaths(project):
    """Get filepath list for AStyle processing.
       Argument must be one of the global variables.
       Returns a list of filepaths to process.
    """
    filepaths = []
    test_directory = get_test_directory()
    if project == CODEBLOCKS:
        if USE_MULTIPLE_EXTENSIONS:
            filepaths.append(test_directory + "/CodeBlocks/src/src/*.cpp,*.cxx,*.h")
        else:
            filepaths.append(test_directory + "/CodeBlocks/src/*.cpp")
            filepaths.append(test_directory + "/CodeBlocks/src/*.h")
    elif project == LSOF:
        filepaths.append(test_directory + "/lsof/*.c,*.h")
        filepaths.append(test_directory + "/lsof/lib/*.c,*.h")
    elif project == JEDIT:
        filepaths.append(test_directory + "/jEdit/*.java")
#	elif project == KDEVELOP:
#		filepaths.append(test_directory + "/KDevelop/*.cpp")
#		filepaths.append(test_directory + "/KDevelop/*.h")
#	elif project == MONODEVELOP:
#		filepaths.append(test_directory + "/MonoDevelop/src/*.cs")
    elif project == LIBSBASE:
        if USE_MULTIPLE_EXTENSIONS:
            filepaths.append(test_directory + "/libsBase/Source/*.m,*.h")
        else:
            filepaths.append(test_directory + "/libsBase/Source/*.m")
            filepaths.append(test_directory + "/libsBase/Source/*.h")
    elif project == SCITE:
        if USE_MULTIPLE_EXTENSIONS:
            filepaths.append(test_directory + "/SciTE/*.cxx,*.h")
        else:
            filepaths.append(test_directory + "/SciTE/*.cxx")
            filepaths.append(test_directory + "/SciTE/*.h")
    elif project == SHARPDEVELOP:
        filepaths.append(test_directory + "/SharpDevelop/src/*.cs")
    elif project == SHARPMAIN:
        # number of files: Main 1000, Libraries 1200, AddIns 5000, Tools 50, Setup 0
        # also change libextract.py, extract_sharpmain()
        filepaths.append(test_directory + "/SharpDevelopMain/src/Main/*.cs")
        #~ filepaths.append(test_directory + "/SharpDevelopMain/src/Libraries/*.cs")
    elif project == TESTPROJECT:
        # the test file paths can be changed depending n the circumstances
        # if the test is not CodeBlocks change extract_testproject() in libextract.py
        if USE_MULTIPLE_EXTENSIONS:
            filepaths.append(test_directory + "/TestProject/scite/gtk/*.cxx,*.h")
        else:
            filepaths.append(test_directory + "/TestProject/scite/gtk/*.cxx")
            filepaths.append(test_directory + "/TestProject/scite/gtk/*.h")
    else:
        system_exit("Bad get_project_filepaths() project id: " + project)
    return filepaths

# -----------------------------------------------------------------------------

def get_python_version():
    """Return the Python version number as a string."""
    version = ""
    if platform.python_implementation() == "CPython":
        version = "Python"
    else:
        version = platform.python_implementation()
    version += " {0}.{1}.{2}  ".format(sys.version_info[0],
                                       sys.version_info[1],
                                       sys.version_info[2])
    version += "({0})".format(platform.architecture()[0])
    return version

# -----------------------------------------------------------------------------

def get_python_version_number():
    """Return the Python version number as a number."""
    return sys.version_info[0]

# -----------------------------------------------------------------------------

def get_temp_directory():
    """Get the temporary directory for the os environment.
       endsep = True will add an ending separator.
    """
    if os.name == "nt":
        tempdir = os.getenv("TEMP")
        tempdir = tempdir.replace('\\', '/')
    else:
        tempdir = "./"
    return tempdir

# -----------------------------------------------------------------------------

def get_test_directory(endsep=False):
    """Get the test directory for the os environment.
       endsep = True will add an ending separator.
    """
    if endsep is not True and endsep is not False:
        system_exit("Bad arg in get_test_directory(): " + str(endsep))
    if os.name == "nt" and os.path.exists("R:"):
        testdir = "R:/" + TEST_DIRECTORY
    else:
        testdir = get_project_directory(True) + TEST_DIRECTORY
    if not os.path.isdir(testdir):
        message = "Cannot find test directory: " + testdir
        system_exit(message)
    if endsep:
        testdir += '/'
    return testdir

# -----------------------------------------------------------------------------

def is_executed_from_console():
    """Check if this script is run is from the console or from an editor.
       If run from a console the sys.stdin will be a TTY.
    """
    return sys.stdin.isatty()

# -----------------------------------------------------------------------------

def remove_build_file(buildfile):
    """Remove the build.CONFIG.tmp file from the astyle compile.
       If the file cannot be removed it is probably in use by another script.
       Wait until the other script finishes the compile to fix the problem.
    """
    try:
        os.remove(buildfile)
    except WindowsError as err:
        print()
        print(err)
        message = ("The file '{0}' must be removed "
                   "before continuing").format(buildfile)
        system_exit(message)

# -----------------------------------------------------------------------------

def set_test_directory(test_directory):
    """Change the name of the global test directory.
    """
    global TEST_DIRECTORY
    TEST_DIRECTORY = test_directory
    testdir = get_project_directory(True) + TEST_DIRECTORY
    testdir = testdir.replace('\\', '/')
    if not os.path.isdir(testdir):
        print("Creating: " + testdir)
        os.mkdir(testdir)

# -----------------------------------------------------------------------------

def set_text_color(color):
    """Change text color if script is run from the console.
    """
    if is_executed_from_console():
        if os.name == "nt":
            color_values = {"blue"    : "color 09",
                            "cyan"    : "color 0B",
                            "green"   : "color 0A",
                            "magenta" : "color 0D",
                            "red"     : "color 0C",
                            "white"   : "color 0F",
                            "yellow"  : "color 0E"}

            system_code = color_values.get(color, "invalid")
            if system_code == "invalid":
                system_exit("Invalid color param " + color)
            os.system(system_code)
        else:
            color_values = {"blue"    : "echo -n '[1;34m'",
                            "cyan"    : "echo -n '[1;36m'",
                            "green"   : "echo -n '[1;32m'",
                            "magenta" : "echo -n '[1;35m'",
                            "red"     : "echo -n '[1;31m'",
                            "white"   : "echo -n '[1;37m'",
                            "yellow"  : "echo -n '[1;33m'"}

            system_code = color_values.get(color, "invalid")
            if system_code == "invalid":
                system_exit("Invalid color param " + color)
            os.system(system_code)

# -----------------------------------------------------------------------------

def system_exit(message=''):
    """Accept keyboard input to assure a message is noticed.
    """
    if len(message.strip()) > 0:
        set_text_color("red")
        print(message)
    # pause if script is run from the console
    if os.name == "nt" and is_executed_from_console():
        print("\nPress any key to end . . .")
        get_ch()

    # this does NOT raise a SystemExit exception like sys.exit()
    os._exit(0)

# -----------------------------------------------------------------------------

def test_all_functions():
    """Test all functions for syntax.
    """
    build_astyle_executable(DEBUG)		# calls compile_astyle_linux() or ..._windows()
    #create_ramdrive()
    get_7zip_path()
    get_archive_directory()
    get_astyle_build_directory(DEBUG)
    get_astyle_directory()
    get_astyleexe_path(DEBUG)
    get_astyletest_directory()
    get_diff_path()
    get_file_py_directory()
    get_home_directory()
    get_project_directory()
    get_project_excludes(TESTPROJECT)
    get_project_filepaths(TESTPROJECT)
    get_python_version()
    get_python_version_number()
    get_temp_directory()
    get_test_directory()
    is_executed_from_console()
    set_text_color("white")

# -----------------------------------------------------------------------------

# make the module executable
# run tests if executed as stand-alone
if __name__ == "__main__":

    set_text_color("yellow")
    print(get_python_version())
    test_all_functions()
    system_exit()
