from distutils.core import setup, Extension

import os 
import sysconfig

_DEBUG = True
# Generally I write code so that if DEBUG is defined as 0 then all optimisations
# are off and asserts are enabled. Typically run times of these builds are x2 to x10
# release builds.
# If DEBUG > 0 then extra code paths are introduced such as checking the integrity of
# internal data structures. In this case the performance is by no means comparable
# with release builds.
_DEBUG_LEVEL = 3

# Common flags for both release and debug builds.
extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
# extra_compile_args += ["-std=c++11", "-Wall", "-Wextra"]
if _DEBUG:
    extra_compile_args += ["-g3", "-O0", "-DDEBUG=%s" % _DEBUG_LEVEL, "-UNDEBUG"]
else:
    extra_compile_args += ["-DNDEBUG", "-O3"]
os.system("swig -c++ -python HWsim.i")

pht_module = Extension("_HWsim",
        sources=["HWsim_wrap.cxx",
            "ReadParam.cpp",
            "Technology.cpp",
            "Sum.cpp",
            "FunctionUnit.cpp",
            "formula.cpp",
            "Adder.cpp",
            "RowDecoder.cpp",
            "Mux.cpp",
            "WLDecoderOutput.cpp",
            "DFF.cpp",
            "DeMux.cpp",
            "VoltageSenseAmp.cpp",
            "Precharger.cpp",
            "SenseAmp.cpp",
            "DecoderDriver.cpp",
            "SRAMWriteDriver.cpp",
            "ReadCircuit.cpp",
            "ShiftAdd.cpp",
            "SwitchMatrix.cpp",
            "WLNewDecoderDriver.cpp",
            "NewSwitchMatrix.cpp",
            "CurrentSenseAmp.cpp",
            "Comparator.cpp",
            "MultilevelSAEncoder.cpp",
            "MultilevelSenseAmp.cpp",
            "SubArray.cpp",
            "Core.cpp",
            "HWsim.cpp"
            ],
            extra_compile_args=extra_compile_args
        )
setup(name = "HWsim",
        version = "0.1",
        author = "THU.IME",
        description = "HWsim",
        ext_modules = [pht_module],
        py_modules = ["HWsim"],
        )

