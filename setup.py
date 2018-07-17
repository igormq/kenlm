import glob
import os
import platform

from Cython.Build import cythonize
from setuptools import Extension, setup

extra_compile_args = []
libraries = []

CC = os.environ.get('CC', 'gcc')


# Does gcc compile with this header and library?
def compile_test(header, library):
    dummy_path = os.path.join(os.path.dirname(__file__), "dummy")
    command = "bash -c \"" + CC + " -include " + header + " -l"
    command += library + " -x c++ - <<<'int main() {}' -o " + dummy_path + " >/dev/null 2>/dev/null && rm "
    command += dummy_path + " 2>/dev/null\""
    return os.system(command) == 0


files = glob.glob('util/*.cc') + glob.glob('lm/*.cc') + glob.glob('util/double-conversion/*.cc')
files = [fn for fn in files if not (fn.endswith('main.cc') or fn.endswith('test.cc'))]

if platform.system() == 'Linux':
    libraries += ['stdc++', 'rt']
elif platform.system() == 'Darwin':
    libraries += ['stdc++']

# We don't need -std=c++11 but python seems to be compiled with it now.  https://github.com/kpu/kenlm/issues/86
extra_compile_args += ['-O3', '-DNDEBUG', '-DKENLM_MAX_ORDER=6', '-std=c++11']

if compile_test('zlib.h', 'z'):
    extra_compile_args += ['-DHAVE_ZLIB']
    libraries += ['z']

if compile_test('bzlib.h', 'bz2'):
    extra_compile_args += ['-DHAVE_BZLIB']
    libraries += ['bz2']

if compile_test('lzma.h', 'lzma'):
    extra_compile_args += ['-DHAVE_XZLIB']
    libraries += ['lzma']

ext_modules = cythonize(
    Extension(
        name='kenlm',
        sources=files + ['python/kenlm.pyx'],
        language='c++',
        include_dirs=['.'],
        libraries=libraries,
        extra_compile_args=extra_compile_args))

setup(name='kenlm', ext_modules=ext_modules, include_package_data=True, setup_requires=["cython"])
