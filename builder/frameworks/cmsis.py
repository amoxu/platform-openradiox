import sys
import os
from os.path import exists,isdir, isfile, join
from string import Template

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
product_line = board.get("build.product_line", "")

env.SConscript("_bare.py")

CMSIS_DIR = platform.get_package_dir("framework-cmsis")

def get_linker_script():
    ldscript = join(platform.get_dir(),"linkscript", product_line + ".ld")

    if isfile(ldscript):
        return ldscript

    sys.stderr.write("Warning! Cannot find a linker script for the required board! desired path: %s\n" % ldscript)


env.Append(
    CPPPATH=[
        join(CMSIS_DIR, "CMSIS", "Include"),
    ],

    LINKFLAGS=[
        "--specs=nano.specs",
        "--specs=nosys.specs"
    ]
)

env.Append(
    CPPDEFINES=[
        env["BUILD_TYPE"].upper()
    ]
)

# Information about obsolete method of specifying linker scripts
if any("-Wl,-T" in f for f in env.get("LINKFLAGS", [])):
    print("Warning! '-Wl,-T' option for specifying linker scripts is deprecated. "
          "Please use 'board_build.ldscript' option in your 'platformio.ini' file.")

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=get_linker_script())
