from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
cpu = board.get("build.cpu", "")

env.Append(    
    ASFLAGS=[
        "-mthumb",
    ],
    ASPPFLAGS=[
        "-x", "assembler-with-cpp",
    ],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall",
        "-mthumb",
        # "-save-temps=obj" # Generate intermediate files
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU")
    ],

    LINKFLAGS=[
        "-Os",
        "-Wl,--gc-sections,--relax",
        "-mthumb",
        "-Wl,-Map,%s/linkmap.map" % env.get("BUILD_DIR") # Generate map file
    ],

    LIBS=["c", "gcc", "m", "stdc++"]
)

if "BOARD" in env:
    env.Append(
        ASFLAGS=[
            "-mcpu=%s" % cpu
        ],
        CCFLAGS=[
            "-mcpu=%s" % cpu
        ],
        LINKFLAGS=[
            "-mcpu=%s" % cpu
        ]
    )

env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])
