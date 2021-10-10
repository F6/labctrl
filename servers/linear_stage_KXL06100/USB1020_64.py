# -*- coding: utf-8 -*-

"""USB1020_64.py:
Wrapper for USB1020_64.h
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

# Begin preamble for Python v(3, 2)

import ctypes, os, sys
from ctypes import *

def cmp(a, b):
    return (a > b) - (a < b)

_int_types = (c_int16, c_int32)
if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types


class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, Union):

    _fields_ = [("raw", POINTER(c_char)), ("data", c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from bytes
        elif isinstance(obj, bytes):
            return cls(obj)

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj.encode())

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from c_char array
        elif isinstance(obj, c_char * len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    """
    Simple helper used for casts to simple builtin types:  if the argument is a
    string type, it will be converted to it's ordinal value.

    This function will raise an exception if the argument is string with more
    than one characters.
    """
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import platform
import ctypes
import ctypes.util


def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []


class LibraryLoader(object):
    # library names formatted specifically for platforms
    name_formats = ["%s"]

    class Lookup(object):
        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

        def get(self, name, calling_convention="cdecl"):
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            try:
                return self.Lookup(path)
            except:
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # search through a prioritized series of locations for the library

            # we first search any specific directories identified by user
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    # dir_i should be absolute already
                    yield os.path.join(dir_i, fmt % libname)

            # then we search the directory where the generated python interface is stored
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            # now, use the ctypes tools to try to find the library
            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            # then we search all paths identified as platform-specific lib paths
            for path in self.getplatformpaths(libname):
                yield path

            # Finally, we'll try the users current working directory
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, libname):
        return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
        # of the default RTLD_LOCAL.  Without this, you end up with
        # libraries not being loadable, resulting in "Symbol not found"
        # errors
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir, name)

    def getdirs(self, libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser("~/lib"), "/usr/local/lib", "/usr/lib"]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        if hasattr(sys, "frozen") and sys.frozen == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    class _Directories(dict):
        def __init__(self):
            self.order = 0

        def add(self, directory):
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            # only adds and updates order if exists and not already in set
            if not os.path.exists(directory):
                return
            o = self.setdefault(directory, self.order)
            if o == self.order:
                self.order += 1

        def extend(self, directories):
            for d in directories:
                self.add(d)

        def ordered(self):
            return (i[0] for i in sorted(self.items(), key=lambda D: D[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive funtion to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """

        try:
            with open(conf) as f:
                for D in f:
                    D = D.strip()
                    if not D:
                        continue

                    m = self._include.match(D)
                    if not m:
                        dirs.add(D)
                    else:
                        for D2 in glob.glob(m.group("pattern")):
                            self._get_ld_so_conf_dirs(D2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",  # HPUX
            "LIBPATH",  # OS/2, AIX
            "LIBRARY_PATH",  # BE/OS
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            # prefer 64 bit if that is our arch
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        # must include standard libs, since those paths are also used by 64 bit
        # installs
        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            if bitage.startswith("32"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/x86_64-linux-gnu", "/usr/lib/x86_64-linux-gnu"]
            else:
                # guess...
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        ext_re = re.compile(r"\.s[ol]$")
        for dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            # we iterate through all found paths for library, since we may have
            # actually found multiple architectures or other library types that
            # may not load
            yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for F in other_dirs:
        if not os.path.isabs(F):
            F = os.path.abspath(F)
        load_library.other_dirs.append(F)


del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries
_libs["./USB1020_64"] = load_library("./USB1020_64")

# 1 libraries
# End libraries

# No modules

USHORT = c_ushort# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\minwindef.h: 26

PUSHORT = POINTER(USHORT)# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\minwindef.h: 27

WINBOOL = c_int# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\minwindef.h: 127

BOOL = c_int# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\minwindef.h: 131

PBOOL = POINTER(WINBOOL)# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\minwindef.h: 134

UINT = c_uint# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\minwindef.h: 159

SHORT = c_short# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\winnt.h: 286

LONG = c_long# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\winnt.h: 287

PSHORT = POINTER(SHORT)# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\winnt.h: 392

PLONG = POINTER(LONG)# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\winnt.h: 393

HANDLE = POINTER(None)# .\llvm-mingw-20211002-msvcrt-x86_64\\include\\winnt.h: 405

# ./USB1020_64.h: 19
class struct__USB1020_PARA_DataList(Structure):
    pass

struct__USB1020_PARA_DataList.__slots__ = [
    'Multiple',
    'StartSpeed',
    'DriveSpeed',
    'Acceleration',
    'Deceleration',
    'AccIncRate',
    'DecIncRate',
]
struct__USB1020_PARA_DataList._fields_ = [
    ('Multiple', LONG),
    ('StartSpeed', LONG),
    ('DriveSpeed', LONG),
    ('Acceleration', LONG),
    ('Deceleration', LONG),
    ('AccIncRate', LONG),
    ('DecIncRate', LONG),
]

USB1020_PARA_DataList = struct__USB1020_PARA_DataList# ./USB1020_64.h: 19

PUSB1020_PARA_DataList = POINTER(struct__USB1020_PARA_DataList)# ./USB1020_64.h: 19

# ./USB1020_64.h: 35
class struct__USB1020_PARA_LCData(Structure):
    pass

struct__USB1020_PARA_LCData.__slots__ = [
    'AxisNum',
    'LV_DV',
    'DecMode',
    'PulseMode',
    'PLSLogLever',
    'DIRLogLever',
    'Line_Curve',
    'Direction',
    'nPulseNum',
]
struct__USB1020_PARA_LCData._fields_ = [
    ('AxisNum', LONG),
    ('LV_DV', LONG),
    ('DecMode', LONG),
    ('PulseMode', LONG),
    ('PLSLogLever', LONG),
    ('DIRLogLever', LONG),
    ('Line_Curve', LONG),
    ('Direction', LONG),
    ('nPulseNum', LONG),
]

USB1020_PARA_LCData = struct__USB1020_PARA_LCData# ./USB1020_64.h: 35

PUSB1020_PARA_LCData = POINTER(struct__USB1020_PARA_LCData)# ./USB1020_64.h: 35

# ./USB1020_64.h: 45
class struct__USB1020_PARA_InterpolationAxis(Structure):
    pass

struct__USB1020_PARA_InterpolationAxis.__slots__ = [
    'Axis1',
    'Axis2',
    'Axis3',
]
struct__USB1020_PARA_InterpolationAxis._fields_ = [
    ('Axis1', LONG),
    ('Axis2', LONG),
    ('Axis3', LONG),
]

USB1020_PARA_InterpolationAxis = struct__USB1020_PARA_InterpolationAxis# ./USB1020_64.h: 45

PUSB1020_PARA_InterpolationAxis = POINTER(struct__USB1020_PARA_InterpolationAxis)# ./USB1020_64.h: 45

# ./USB1020_64.h: 57
class struct__USB1020_PARA_LineData(Structure):
    pass

struct__USB1020_PARA_LineData.__slots__ = [
    'Line_Curve',
    'ConstantSpeed',
    'n1AxisPulseNum',
    'n2AxisPulseNum',
    'n3AxisPulseNum',
]
struct__USB1020_PARA_LineData._fields_ = [
    ('Line_Curve', LONG),
    ('ConstantSpeed', LONG),
    ('n1AxisPulseNum', LONG),
    ('n2AxisPulseNum', LONG),
    ('n3AxisPulseNum', LONG),
]

USB1020_PARA_LineData = struct__USB1020_PARA_LineData# ./USB1020_64.h: 57

PUSB1020_PARA_LineData = POINTER(struct__USB1020_PARA_LineData)# ./USB1020_64.h: 57

# ./USB1020_64.h: 70
class struct__USB1020_PARA_CircleData(Structure):
    pass

struct__USB1020_PARA_CircleData.__slots__ = [
    'ConstantSpeed',
    'Direction',
    'Center1',
    'Center2',
    'Pulse1',
    'Pulse2',
]
struct__USB1020_PARA_CircleData._fields_ = [
    ('ConstantSpeed', LONG),
    ('Direction', LONG),
    ('Center1', LONG),
    ('Center2', LONG),
    ('Pulse1', LONG),
    ('Pulse2', LONG),
]

USB1020_PARA_CircleData = struct__USB1020_PARA_CircleData# ./USB1020_64.h: 70

PUSB1020_PARA_CircleData = POINTER(struct__USB1020_PARA_CircleData)# ./USB1020_64.h: 70

# ./USB1020_64.h: 165
class struct__USB1020_PARA_Interrupt(Structure):
    pass

struct__USB1020_PARA_Interrupt.__slots__ = [
    'PULSE',
    'PBCM',
    'PSCM',
    'PSCP',
    'PBCP',
    'CDEC',
    'CSTA',
    'DEND',
    'CIINT',
    'BPINT',
]
struct__USB1020_PARA_Interrupt._fields_ = [
    ('PULSE', UINT),
    ('PBCM', UINT),
    ('PSCM', UINT),
    ('PSCP', UINT),
    ('PBCP', UINT),
    ('CDEC', UINT),
    ('CSTA', UINT),
    ('DEND', UINT),
    ('CIINT', UINT),
    ('BPINT', UINT),
]

USB1020_PARA_Interrupt = struct__USB1020_PARA_Interrupt# ./USB1020_64.h: 165

PUSB1020_PARA_Interrupt = POINTER(struct__USB1020_PARA_Interrupt)# ./USB1020_64.h: 165

# ./USB1020_64.h: 190
class struct__USB1020_PARA_SynchronActionOwnAxis(Structure):
    pass

struct__USB1020_PARA_SynchronActionOwnAxis.__slots__ = [
    'PBCP',
    'PSCP',
    'PSCM',
    'PBCM',
    'DSTA',
    'DEND',
    'IN3LH',
    'IN3HL',
    'LPRD',
    'CMD',
    'AXIS1',
    'AXIS2',
    'AXIS3',
]
struct__USB1020_PARA_SynchronActionOwnAxis._fields_ = [
    ('PBCP', UINT),
    ('PSCP', UINT),
    ('PSCM', UINT),
    ('PBCM', UINT),
    ('DSTA', UINT),
    ('DEND', UINT),
    ('IN3LH', UINT),
    ('IN3HL', UINT),
    ('LPRD', UINT),
    ('CMD', UINT),
    ('AXIS1', UINT),
    ('AXIS2', UINT),
    ('AXIS3', UINT),
]

USB1020_PARA_SynchronActionOwnAxis = struct__USB1020_PARA_SynchronActionOwnAxis# ./USB1020_64.h: 190

PUSB1020_PARA_SynchronActionOwnAxis = POINTER(struct__USB1020_PARA_SynchronActionOwnAxis)# ./USB1020_64.h: 190

# ./USB1020_64.h: 211
class struct__USB1020_PARA_SynchronActionOtherAxis(Structure):
    pass

struct__USB1020_PARA_SynchronActionOtherAxis.__slots__ = [
    'FDRVP',
    'FDRVM',
    'CDRVP',
    'CDRVM',
    'SSTOP',
    'ISTOP',
    'LPSAV',
    'EPSAV',
    'LPSET',
    'EPSET',
    'OPSET',
    'VLSET',
    'OUTN',
    'INTN',
]
struct__USB1020_PARA_SynchronActionOtherAxis._fields_ = [
    ('FDRVP', UINT),
    ('FDRVM', UINT),
    ('CDRVP', UINT),
    ('CDRVM', UINT),
    ('SSTOP', UINT),
    ('ISTOP', UINT),
    ('LPSAV', UINT),
    ('EPSAV', UINT),
    ('LPSET', UINT),
    ('EPSET', UINT),
    ('OPSET', UINT),
    ('VLSET', UINT),
    ('OUTN', UINT),
    ('INTN', UINT),
]

USB1020_PARA_SynchronActionOtherAxis = struct__USB1020_PARA_SynchronActionOtherAxis# ./USB1020_64.h: 211

PUSB1020_PARA_SynchronActionOtherAxis = POINTER(struct__USB1020_PARA_SynchronActionOtherAxis)# ./USB1020_64.h: 211

# ./USB1020_64.h: 234
class struct__USB1020_PARA_ExpMode(Structure):
    pass

struct__USB1020_PARA_ExpMode.__slots__ = [
    'EPCLR',
    'FE0',
    'FE1',
    'FE2',
    'FE3',
    'FE4',
    'FL0',
    'FL1',
    'FL2',
]
struct__USB1020_PARA_ExpMode._fields_ = [
    ('EPCLR', UINT),
    ('FE0', UINT),
    ('FE1', UINT),
    ('FE2', UINT),
    ('FE3', UINT),
    ('FE4', UINT),
    ('FL0', UINT),
    ('FL1', UINT),
    ('FL2', UINT),
]

USB1020_PARA_ExpMode = struct__USB1020_PARA_ExpMode# ./USB1020_64.h: 234

PUSB1020_PARA_ExpMode = POINTER(struct__USB1020_PARA_ExpMode)# ./USB1020_64.h: 234

# ./USB1020_64.h: 250
class struct__USB1020_PARA_DCC(Structure):
    pass

struct__USB1020_PARA_DCC.__slots__ = [
    'DCCE',
    'DCCL',
    'DCCW0',
    'DCCW1',
    'DCCW2',
]
struct__USB1020_PARA_DCC._fields_ = [
    ('DCCE', UINT),
    ('DCCL', UINT),
    ('DCCW0', UINT),
    ('DCCW1', UINT),
    ('DCCW2', UINT),
]

USB1020_PARA_DCC = struct__USB1020_PARA_DCC# ./USB1020_64.h: 250

PUSB1020_PARA_DCC = POINTER(struct__USB1020_PARA_DCC)# ./USB1020_64.h: 250

# ./USB1020_64.h: 269
class struct__USB1020_PARA_AutoHomeSearch(Structure):
    pass

struct__USB1020_PARA_AutoHomeSearch.__slots__ = [
    'ST1E',
    'ST1D',
    'ST2E',
    'ST2D',
    'ST3E',
    'ST3D',
    'ST4E',
    'ST4D',
    'PCLR',
    'SAND',
    'LIMIT',
    'HMINT',
]
struct__USB1020_PARA_AutoHomeSearch._fields_ = [
    ('ST1E', UINT),
    ('ST1D', UINT),
    ('ST2E', UINT),
    ('ST2D', UINT),
    ('ST3E', UINT),
    ('ST3D', UINT),
    ('ST4E', UINT),
    ('ST4D', UINT),
    ('PCLR', UINT),
    ('SAND', UINT),
    ('LIMIT', UINT),
    ('HMINT', UINT),
]

USB1020_PARA_AutoHomeSearch = struct__USB1020_PARA_AutoHomeSearch# ./USB1020_64.h: 269

PUSB1020_PARA_AutoHomeSearch = POINTER(struct__USB1020_PARA_AutoHomeSearch)# ./USB1020_64.h: 269

# ./USB1020_64.h: 284
class struct__USB1020_PARA_DO(Structure):
    pass

struct__USB1020_PARA_DO.__slots__ = [
    'OUT0',
    'OUT1',
    'OUT2',
    'OUT3',
    'OUT4',
    'OUT5',
    'OUT6',
    'OUT7',
]
struct__USB1020_PARA_DO._fields_ = [
    ('OUT0', UINT),
    ('OUT1', UINT),
    ('OUT2', UINT),
    ('OUT3', UINT),
    ('OUT4', UINT),
    ('OUT5', UINT),
    ('OUT6', UINT),
    ('OUT7', UINT),
]

USB1020_PARA_DO = struct__USB1020_PARA_DO# ./USB1020_64.h: 284

PUSB1020_PARA_DO = POINTER(struct__USB1020_PARA_DO)# ./USB1020_64.h: 284

# ./USB1020_64.h: 309
class struct__USB1020_PARA_RR0(Structure):
    pass

struct__USB1020_PARA_RR0.__slots__ = [
    'XDRV',
    'YDRV',
    'ZDRV',
    'UDRV',
    'XERROR',
    'YERROR',
    'ZERROR',
    'UERROR',
    'IDRV',
    'CNEXT',
    'ZONE0',
    'ZONE1',
    'ZONE2',
    'BPSC0',
    'BPSC1',
]
struct__USB1020_PARA_RR0._fields_ = [
    ('XDRV', UINT),
    ('YDRV', UINT),
    ('ZDRV', UINT),
    ('UDRV', UINT),
    ('XERROR', UINT),
    ('YERROR', UINT),
    ('ZERROR', UINT),
    ('UERROR', UINT),
    ('IDRV', UINT),
    ('CNEXT', UINT),
    ('ZONE0', UINT),
    ('ZONE1', UINT),
    ('ZONE2', UINT),
    ('BPSC0', UINT),
    ('BPSC1', UINT),
]

USB1020_PARA_RR0 = struct__USB1020_PARA_RR0# ./USB1020_64.h: 309

PUSB1020_PARA_RR0 = POINTER(struct__USB1020_PARA_RR0)# ./USB1020_64.h: 309

# ./USB1020_64.h: 332
class struct__USB1020_PARA_RR1(Structure):
    pass

struct__USB1020_PARA_RR1.__slots__ = [
    'CMPP',
    'CMPM',
    'ASND',
    'CNST',
    'DSND',
    'AASND',
    'ACNST',
    'ADSND',
    'IN0',
    'IN1',
    'IN2',
    'IN3',
    'LMTP',
    'LMTM',
    'ALARM',
    'EMG',
]
struct__USB1020_PARA_RR1._fields_ = [
    ('CMPP', UINT),
    ('CMPM', UINT),
    ('ASND', UINT),
    ('CNST', UINT),
    ('DSND', UINT),
    ('AASND', UINT),
    ('ACNST', UINT),
    ('ADSND', UINT),
    ('IN0', UINT),
    ('IN1', UINT),
    ('IN2', UINT),
    ('IN3', UINT),
    ('LMTP', UINT),
    ('LMTM', UINT),
    ('ALARM', UINT),
    ('EMG', UINT),
]

USB1020_PARA_RR1 = struct__USB1020_PARA_RR1# ./USB1020_64.h: 332

PUSB1020_PARA_RR1 = POINTER(struct__USB1020_PARA_RR1)# ./USB1020_64.h: 332

# ./USB1020_64.h: 352
class struct__USB1020_PARA_RR2(Structure):
    pass

struct__USB1020_PARA_RR2.__slots__ = [
    'SLMTP',
    'SLMTM',
    'HLMTP',
    'HLMTM',
    'ALARM',
    'EMG',
    'HOME',
    'HMST0',
    'HMST1',
    'HMST2',
    'HMST3',
    'HMST4',
]
struct__USB1020_PARA_RR2._fields_ = [
    ('SLMTP', UINT),
    ('SLMTM', UINT),
    ('HLMTP', UINT),
    ('HLMTM', UINT),
    ('ALARM', UINT),
    ('EMG', UINT),
    ('HOME', UINT),
    ('HMST0', UINT),
    ('HMST1', UINT),
    ('HMST2', UINT),
    ('HMST3', UINT),
    ('HMST4', UINT),
]

USB1020_PARA_RR2 = struct__USB1020_PARA_RR2# ./USB1020_64.h: 352

PUSB1020_PARA_RR2 = POINTER(struct__USB1020_PARA_RR2)# ./USB1020_64.h: 352

# ./USB1020_64.h: 375
class struct__USB1020_PARA_RR3(Structure):
    pass

struct__USB1020_PARA_RR3.__slots__ = [
    'XIN0',
    'XIN1',
    'XIN2',
    'XIN3',
    'XEXPP',
    'XEXPM',
    'XINPOS',
    'XALARM',
    'YIN0',
    'YIN1',
    'YIN2',
    'YIN3',
    'YEXPP',
    'YEXPM',
    'YINPOS',
    'YALARM',
]
struct__USB1020_PARA_RR3._fields_ = [
    ('XIN0', UINT),
    ('XIN1', UINT),
    ('XIN2', UINT),
    ('XIN3', UINT),
    ('XEXPP', UINT),
    ('XEXPM', UINT),
    ('XINPOS', UINT),
    ('XALARM', UINT),
    ('YIN0', UINT),
    ('YIN1', UINT),
    ('YIN2', UINT),
    ('YIN3', UINT),
    ('YEXPP', UINT),
    ('YEXPM', UINT),
    ('YINPOS', UINT),
    ('YALARM', UINT),
]

USB1020_PARA_RR3 = struct__USB1020_PARA_RR3# ./USB1020_64.h: 375

PUSB1020_PARA_RR3 = POINTER(struct__USB1020_PARA_RR3)# ./USB1020_64.h: 375

# ./USB1020_64.h: 398
class struct__USB1020_PARA_RR4(Structure):
    pass

struct__USB1020_PARA_RR4.__slots__ = [
    'ZIN0',
    'ZIN1',
    'ZIN2',
    'ZIN3',
    'ZEXPP',
    'ZEXPM',
    'ZINPOS',
    'ZALARM',
    'UIN0',
    'UIN1',
    'UIN2',
    'UIN3',
    'UEXPP',
    'UEXPM',
    'UINPOS',
    'UALARM',
]
struct__USB1020_PARA_RR4._fields_ = [
    ('ZIN0', UINT),
    ('ZIN1', UINT),
    ('ZIN2', UINT),
    ('ZIN3', UINT),
    ('ZEXPP', UINT),
    ('ZEXPM', UINT),
    ('ZINPOS', UINT),
    ('ZALARM', UINT),
    ('UIN0', UINT),
    ('UIN1', UINT),
    ('UIN2', UINT),
    ('UIN3', UINT),
    ('UEXPP', UINT),
    ('UEXPM', UINT),
    ('UINPOS', UINT),
    ('UALARM', UINT),
]

USB1020_PARA_RR4 = struct__USB1020_PARA_RR4# ./USB1020_64.h: 398

PUSB1020_PARA_RR4 = POINTER(struct__USB1020_PARA_RR4)# ./USB1020_64.h: 398

# ./USB1020_64.h: 416
class struct__USB1020_PARA_RR5(Structure):
    pass

struct__USB1020_PARA_RR5.__slots__ = [
    'PULSE',
    'PBCM',
    'PSCM',
    'PSCP',
    'PBCP',
    'CDEC',
    'CSTA',
    'DEND',
    'HMEND',
    'SYNC',
]
struct__USB1020_PARA_RR5._fields_ = [
    ('PULSE', UINT),
    ('PBCM', UINT),
    ('PSCM', UINT),
    ('PSCP', UINT),
    ('PBCP', UINT),
    ('CDEC', UINT),
    ('CSTA', UINT),
    ('DEND', UINT),
    ('HMEND', UINT),
    ('SYNC', UINT),
]

USB1020_PARA_RR5 = struct__USB1020_PARA_RR5# ./USB1020_64.h: 416

PUSB1020_PARA_RR5 = POINTER(struct__USB1020_PARA_RR5)# ./USB1020_64.h: 416

# ./USB1020_64.h: 431
if _libs["./USB1020_64"].has("USB1020_CreateDevice", "cdecl"):
    USB1020_CreateDevice = _libs["./USB1020_64"].get("USB1020_CreateDevice", "cdecl")
    USB1020_CreateDevice.argtypes = [c_int]
    USB1020_CreateDevice.restype = HANDLE

# ./USB1020_64.h: 434
if _libs["./USB1020_64"].has("USB1020_CreateDeviceEx", "cdecl"):
    USB1020_CreateDeviceEx = _libs["./USB1020_64"].get("USB1020_CreateDeviceEx", "cdecl")
    USB1020_CreateDeviceEx.argtypes = [c_int]
    USB1020_CreateDeviceEx.restype = HANDLE

# ./USB1020_64.h: 437
if _libs["./USB1020_64"].has("USB1020_GetDeviceCount", "cdecl"):
    USB1020_GetDeviceCount = _libs["./USB1020_64"].get("USB1020_GetDeviceCount", "cdecl")
    USB1020_GetDeviceCount.argtypes = [HANDLE]
    USB1020_GetDeviceCount.restype = c_int

# ./USB1020_64.h: 440
if _libs["./USB1020_64"].has("USB1020_GetDeviceCurrentID", "cdecl"):
    USB1020_GetDeviceCurrentID = _libs["./USB1020_64"].get("USB1020_GetDeviceCurrentID", "cdecl")
    USB1020_GetDeviceCurrentID.argtypes = [HANDLE, PLONG, PLONG]
    USB1020_GetDeviceCurrentID.restype = c_int

# ./USB1020_64.h: 445
if _libs["./USB1020_64"].has("USB1020_ReleaseDevice", "cdecl"):
    USB1020_ReleaseDevice = _libs["./USB1020_64"].get("USB1020_ReleaseDevice", "cdecl")
    USB1020_ReleaseDevice.argtypes = [HANDLE]
    USB1020_ReleaseDevice.restype = BOOL

# ./USB1020_64.h: 448
if _libs["./USB1020_64"].has("USB1020_Reset", "cdecl"):
    USB1020_Reset = _libs["./USB1020_64"].get("USB1020_Reset", "cdecl")
    USB1020_Reset.argtypes = [HANDLE]
    USB1020_Reset.restype = BOOL

# ./USB1020_64.h: 453
if _libs["./USB1020_64"].has("USB1020_PulseOutMode", "cdecl"):
    USB1020_PulseOutMode = _libs["./USB1020_64"].get("USB1020_PulseOutMode", "cdecl")
    USB1020_PulseOutMode.argtypes = [HANDLE, LONG, LONG, LONG, LONG]
    USB1020_PulseOutMode.restype = BOOL

# ./USB1020_64.h: 460
if _libs["./USB1020_64"].has("USB1020_PulseInputMode", "cdecl"):
    USB1020_PulseInputMode = _libs["./USB1020_64"].get("USB1020_PulseInputMode", "cdecl")
    USB1020_PulseInputMode.argtypes = [HANDLE, LONG, LONG]
    USB1020_PulseInputMode.restype = BOOL

# ./USB1020_64.h: 465
if _libs["./USB1020_64"].has("USB1020_SetR", "cdecl"):
    USB1020_SetR = _libs["./USB1020_64"].get("USB1020_SetR", "cdecl")
    USB1020_SetR.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetR.restype = BOOL

# ./USB1020_64.h: 470
if _libs["./USB1020_64"].has("USB1020_SetA", "cdecl"):
    USB1020_SetA = _libs["./USB1020_64"].get("USB1020_SetA", "cdecl")
    USB1020_SetA.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetA.restype = BOOL

# ./USB1020_64.h: 475
if _libs["./USB1020_64"].has("USB1020_SetDec", "cdecl"):
    USB1020_SetDec = _libs["./USB1020_64"].get("USB1020_SetDec", "cdecl")
    USB1020_SetDec.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetDec.restype = BOOL

# ./USB1020_64.h: 480
if _libs["./USB1020_64"].has("USB1020_SetAccIncRate", "cdecl"):
    USB1020_SetAccIncRate = _libs["./USB1020_64"].get("USB1020_SetAccIncRate", "cdecl")
    USB1020_SetAccIncRate.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetAccIncRate.restype = BOOL

# ./USB1020_64.h: 485
if _libs["./USB1020_64"].has("USB1020_SetDecIncRate", "cdecl"):
    USB1020_SetDecIncRate = _libs["./USB1020_64"].get("USB1020_SetDecIncRate", "cdecl")
    USB1020_SetDecIncRate.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetDecIncRate.restype = BOOL

# ./USB1020_64.h: 490
if _libs["./USB1020_64"].has("USB1020_SetSV", "cdecl"):
    USB1020_SetSV = _libs["./USB1020_64"].get("USB1020_SetSV", "cdecl")
    USB1020_SetSV.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetSV.restype = BOOL

# ./USB1020_64.h: 495
if _libs["./USB1020_64"].has("USB1020_SetV", "cdecl"):
    USB1020_SetV = _libs["./USB1020_64"].get("USB1020_SetV", "cdecl")
    USB1020_SetV.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetV.restype = BOOL

# ./USB1020_64.h: 500
if _libs["./USB1020_64"].has("USB1020_SetHV", "cdecl"):
    USB1020_SetHV = _libs["./USB1020_64"].get("USB1020_SetHV", "cdecl")
    USB1020_SetHV.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetHV.restype = BOOL

# ./USB1020_64.h: 505
if _libs["./USB1020_64"].has("USB1020_SetP", "cdecl"):
    USB1020_SetP = _libs["./USB1020_64"].get("USB1020_SetP", "cdecl")
    USB1020_SetP.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetP.restype = BOOL

# ./USB1020_64.h: 510
if _libs["./USB1020_64"].has("USB1020_SetIP", "cdecl"):
    USB1020_SetIP = _libs["./USB1020_64"].get("USB1020_SetIP", "cdecl")
    USB1020_SetIP.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetIP.restype = BOOL

# ./USB1020_64.h: 515
if _libs["./USB1020_64"].has("USB1020_SetC", "cdecl"):
    USB1020_SetC = _libs["./USB1020_64"].get("USB1020_SetC", "cdecl")
    USB1020_SetC.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetC.restype = BOOL

# ./USB1020_64.h: 520
if _libs["./USB1020_64"].has("USB1020_SetLP", "cdecl"):
    USB1020_SetLP = _libs["./USB1020_64"].get("USB1020_SetLP", "cdecl")
    USB1020_SetLP.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetLP.restype = BOOL

# ./USB1020_64.h: 525
if _libs["./USB1020_64"].has("USB1020_SetEP", "cdecl"):
    USB1020_SetEP = _libs["./USB1020_64"].get("USB1020_SetEP", "cdecl")
    USB1020_SetEP.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetEP.restype = BOOL

# ./USB1020_64.h: 530
if _libs["./USB1020_64"].has("USB1020_SetAccofst", "cdecl"):
    USB1020_SetAccofst = _libs["./USB1020_64"].get("USB1020_SetAccofst", "cdecl")
    USB1020_SetAccofst.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetAccofst.restype = BOOL

# ./USB1020_64.h: 535
if _libs["./USB1020_64"].has("USB1020_SelectLPEP", "cdecl"):
    USB1020_SelectLPEP = _libs["./USB1020_64"].get("USB1020_SelectLPEP", "cdecl")
    USB1020_SelectLPEP.argtypes = [HANDLE, LONG, LONG]
    USB1020_SelectLPEP.restype = BOOL

# ./USB1020_64.h: 540
if _libs["./USB1020_64"].has("USB1020_SetCOMPP", "cdecl"):
    USB1020_SetCOMPP = _libs["./USB1020_64"].get("USB1020_SetCOMPP", "cdecl")
    USB1020_SetCOMPP.argtypes = [HANDLE, LONG, USHORT, LONG]
    USB1020_SetCOMPP.restype = BOOL

# ./USB1020_64.h: 546
if _libs["./USB1020_64"].has("USB1020_SetCOMPM", "cdecl"):
    USB1020_SetCOMPM = _libs["./USB1020_64"].get("USB1020_SetCOMPM", "cdecl")
    USB1020_SetCOMPM.argtypes = [HANDLE, LONG, USHORT, LONG]
    USB1020_SetCOMPM.restype = BOOL

# ./USB1020_64.h: 553
if _libs["./USB1020_64"].has("USB1020_SetSynchronAction", "cdecl"):
    USB1020_SetSynchronAction = _libs["./USB1020_64"].get("USB1020_SetSynchronAction", "cdecl")
    USB1020_SetSynchronAction.argtypes = [HANDLE, LONG, PUSB1020_PARA_SynchronActionOwnAxis, PUSB1020_PARA_SynchronActionOtherAxis]
    USB1020_SetSynchronAction.restype = BOOL

# ./USB1020_64.h: 559
if _libs["./USB1020_64"].has("USB1020_SynchronActionDisable", "cdecl"):
    USB1020_SynchronActionDisable = _libs["./USB1020_64"].get("USB1020_SynchronActionDisable", "cdecl")
    USB1020_SynchronActionDisable.argtypes = [HANDLE, LONG, PUSB1020_PARA_SynchronActionOwnAxis, PUSB1020_PARA_SynchronActionOtherAxis]
    USB1020_SynchronActionDisable.restype = BOOL

# ./USB1020_64.h: 565
if _libs["./USB1020_64"].has("USB1020_WriteSynchronActionCom", "cdecl"):
    USB1020_WriteSynchronActionCom = _libs["./USB1020_64"].get("USB1020_WriteSynchronActionCom", "cdecl")
    USB1020_WriteSynchronActionCom.argtypes = [HANDLE, LONG]
    USB1020_WriteSynchronActionCom.restype = BOOL

# ./USB1020_64.h: 571
if _libs["./USB1020_64"].has("USB1020_SetDCC", "cdecl"):
    USB1020_SetDCC = _libs["./USB1020_64"].get("USB1020_SetDCC", "cdecl")
    USB1020_SetDCC.argtypes = [HANDLE, LONG, PUSB1020_PARA_DCC]
    USB1020_SetDCC.restype = BOOL

# ./USB1020_64.h: 576
if _libs["./USB1020_64"].has("USB1020_StartDCC", "cdecl"):
    USB1020_StartDCC = _libs["./USB1020_64"].get("USB1020_StartDCC", "cdecl")
    USB1020_StartDCC.argtypes = [HANDLE, LONG]
    USB1020_StartDCC.restype = BOOL

# ./USB1020_64.h: 580
if _libs["./USB1020_64"].has("USB1020_ExtMode", "cdecl"):
    USB1020_ExtMode = _libs["./USB1020_64"].get("USB1020_ExtMode", "cdecl")
    USB1020_ExtMode.argtypes = [HANDLE, LONG, PUSB1020_PARA_ExpMode]
    USB1020_ExtMode.restype = BOOL

# ./USB1020_64.h: 586
if _libs["./USB1020_64"].has("USB1020_SetInEnable", "cdecl"):
    USB1020_SetInEnable = _libs["./USB1020_64"].get("USB1020_SetInEnable", "cdecl")
    USB1020_SetInEnable.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetInEnable.restype = BOOL

# ./USB1020_64.h: 592
if _libs["./USB1020_64"].has("USB1020_SetAutoHomeSearch", "cdecl"):
    USB1020_SetAutoHomeSearch = _libs["./USB1020_64"].get("USB1020_SetAutoHomeSearch", "cdecl")
    USB1020_SetAutoHomeSearch.argtypes = [HANDLE, LONG, PUSB1020_PARA_AutoHomeSearch]
    USB1020_SetAutoHomeSearch.restype = BOOL

# ./USB1020_64.h: 597
if _libs["./USB1020_64"].has("USB1020_StartAutoHomeSearch", "cdecl"):
    USB1020_StartAutoHomeSearch = _libs["./USB1020_64"].get("USB1020_StartAutoHomeSearch", "cdecl")
    USB1020_StartAutoHomeSearch.argtypes = [HANDLE, LONG]
    USB1020_StartAutoHomeSearch.restype = BOOL

# ./USB1020_64.h: 603
if _libs["./USB1020_64"].has("USB1020_SetEncoderSignalType", "cdecl"):
    USB1020_SetEncoderSignalType = _libs["./USB1020_64"].get("USB1020_SetEncoderSignalType", "cdecl")
    USB1020_SetEncoderSignalType.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetEncoderSignalType.restype = BOOL

# ./USB1020_64.h: 610
if _libs["./USB1020_64"].has("USB1020_InitLVDV", "cdecl"):
    USB1020_InitLVDV = _libs["./USB1020_64"].get("USB1020_InitLVDV", "cdecl")
    USB1020_InitLVDV.argtypes = [HANDLE, PUSB1020_PARA_DataList, PUSB1020_PARA_LCData]
    USB1020_InitLVDV.restype = BOOL

# ./USB1020_64.h: 615
if _libs["./USB1020_64"].has("USB1020_StartLVDV", "cdecl"):
    USB1020_StartLVDV = _libs["./USB1020_64"].get("USB1020_StartLVDV", "cdecl")
    USB1020_StartLVDV.argtypes = [HANDLE, LONG]
    USB1020_StartLVDV.restype = BOOL

# ./USB1020_64.h: 619
if _libs["./USB1020_64"].has("USB1020_Start4D", "cdecl"):
    USB1020_Start4D = _libs["./USB1020_64"].get("USB1020_Start4D", "cdecl")
    USB1020_Start4D.argtypes = [HANDLE]
    USB1020_Start4D.restype = BOOL

# ./USB1020_64.h: 622
if _libs["./USB1020_64"].has("USB1020_InitLineInterpolation_2D", "cdecl"):
    USB1020_InitLineInterpolation_2D = _libs["./USB1020_64"].get("USB1020_InitLineInterpolation_2D", "cdecl")
    USB1020_InitLineInterpolation_2D.argtypes = [HANDLE, PUSB1020_PARA_DataList, PUSB1020_PARA_InterpolationAxis, PUSB1020_PARA_LineData]
    USB1020_InitLineInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 628
if _libs["./USB1020_64"].has("USB1020_StartLineInterpolation_2D", "cdecl"):
    USB1020_StartLineInterpolation_2D = _libs["./USB1020_64"].get("USB1020_StartLineInterpolation_2D", "cdecl")
    USB1020_StartLineInterpolation_2D.argtypes = [HANDLE]
    USB1020_StartLineInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 633
if _libs["./USB1020_64"].has("USB1020_InitLineInterpolation_3D", "cdecl"):
    USB1020_InitLineInterpolation_3D = _libs["./USB1020_64"].get("USB1020_InitLineInterpolation_3D", "cdecl")
    USB1020_InitLineInterpolation_3D.argtypes = [HANDLE, PUSB1020_PARA_DataList, PUSB1020_PARA_InterpolationAxis, PUSB1020_PARA_LineData]
    USB1020_InitLineInterpolation_3D.restype = BOOL

# ./USB1020_64.h: 639
if _libs["./USB1020_64"].has("USB1020_StartLineInterpolation_3D", "cdecl"):
    USB1020_StartLineInterpolation_3D = _libs["./USB1020_64"].get("USB1020_StartLineInterpolation_3D", "cdecl")
    USB1020_StartLineInterpolation_3D.argtypes = [HANDLE]
    USB1020_StartLineInterpolation_3D.restype = BOOL

# ./USB1020_64.h: 644
if _libs["./USB1020_64"].has("USB1020_InitCWInterpolation_2D", "cdecl"):
    USB1020_InitCWInterpolation_2D = _libs["./USB1020_64"].get("USB1020_InitCWInterpolation_2D", "cdecl")
    USB1020_InitCWInterpolation_2D.argtypes = [HANDLE, PUSB1020_PARA_DataList, PUSB1020_PARA_InterpolationAxis, PUSB1020_PARA_CircleData]
    USB1020_InitCWInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 650
if _libs["./USB1020_64"].has("USB1020_StartCWInterpolation_2D", "cdecl"):
    USB1020_StartCWInterpolation_2D = _libs["./USB1020_64"].get("USB1020_StartCWInterpolation_2D", "cdecl")
    USB1020_StartCWInterpolation_2D.argtypes = [HANDLE, LONG]
    USB1020_StartCWInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 654
if _libs["./USB1020_64"].has("USB1020_SetCWRadius", "cdecl"):
    USB1020_SetCWRadius = _libs["./USB1020_64"].get("USB1020_SetCWRadius", "cdecl")
    USB1020_SetCWRadius.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetCWRadius.restype = BOOL

# ./USB1020_64.h: 660
if _libs["./USB1020_64"].has("USB1020_InitBitInterpolation_2D", "cdecl"):
    USB1020_InitBitInterpolation_2D = _libs["./USB1020_64"].get("USB1020_InitBitInterpolation_2D", "cdecl")
    USB1020_InitBitInterpolation_2D.argtypes = [HANDLE, PUSB1020_PARA_InterpolationAxis, PUSB1020_PARA_DataList]
    USB1020_InitBitInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 665
if _libs["./USB1020_64"].has("USB1020_InitBitInterpolation_3D", "cdecl"):
    USB1020_InitBitInterpolation_3D = _libs["./USB1020_64"].get("USB1020_InitBitInterpolation_3D", "cdecl")
    USB1020_InitBitInterpolation_3D.argtypes = [HANDLE, PUSB1020_PARA_InterpolationAxis, PUSB1020_PARA_DataList]
    USB1020_InitBitInterpolation_3D.restype = BOOL

# ./USB1020_64.h: 670
if _libs["./USB1020_64"].has("USB1020_AutoBitInterpolation_2D", "cdecl"):
    USB1020_AutoBitInterpolation_2D = _libs["./USB1020_64"].get("USB1020_AutoBitInterpolation_2D", "cdecl")
    USB1020_AutoBitInterpolation_2D.argtypes = [HANDLE, PUSHORT, UINT]
    USB1020_AutoBitInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 675
if _libs["./USB1020_64"].has("USB1020_AutoBitInterpolation_3D", "cdecl"):
    USB1020_AutoBitInterpolation_3D = _libs["./USB1020_64"].get("USB1020_AutoBitInterpolation_3D", "cdecl")
    USB1020_AutoBitInterpolation_3D.argtypes = [HANDLE, PSHORT, UINT]
    USB1020_AutoBitInterpolation_3D.restype = BOOL

# ./USB1020_64.h: 680
if _libs["./USB1020_64"].has("USB1020_ReleaseBitInterpolation", "cdecl"):
    USB1020_ReleaseBitInterpolation = _libs["./USB1020_64"].get("USB1020_ReleaseBitInterpolation", "cdecl")
    USB1020_ReleaseBitInterpolation.argtypes = [HANDLE]
    USB1020_ReleaseBitInterpolation.restype = BOOL

# ./USB1020_64.h: 683
if _libs["./USB1020_64"].has("USB1020_SetBP_2D", "cdecl"):
    USB1020_SetBP_2D = _libs["./USB1020_64"].get("USB1020_SetBP_2D", "cdecl")
    USB1020_SetBP_2D.argtypes = [HANDLE, LONG, LONG, LONG, LONG]
    USB1020_SetBP_2D.restype = BOOL

# ./USB1020_64.h: 690
if _libs["./USB1020_64"].has("USB1020_SetBP_3D", "cdecl"):
    USB1020_SetBP_3D = _libs["./USB1020_64"].get("USB1020_SetBP_3D", "cdecl")
    USB1020_SetBP_3D.argtypes = [HANDLE, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT]
    USB1020_SetBP_3D.restype = BOOL

# ./USB1020_64.h: 699
if _libs["./USB1020_64"].has("USB1020_BPRegisterStack", "cdecl"):
    USB1020_BPRegisterStack = _libs["./USB1020_64"].get("USB1020_BPRegisterStack", "cdecl")
    USB1020_BPRegisterStack.argtypes = [HANDLE]
    USB1020_BPRegisterStack.restype = LONG

# ./USB1020_64.h: 702
if _libs["./USB1020_64"].has("USB1020_StartBitInterpolation_2D", "cdecl"):
    USB1020_StartBitInterpolation_2D = _libs["./USB1020_64"].get("USB1020_StartBitInterpolation_2D", "cdecl")
    USB1020_StartBitInterpolation_2D.argtypes = [HANDLE]
    USB1020_StartBitInterpolation_2D.restype = BOOL

# ./USB1020_64.h: 705
if _libs["./USB1020_64"].has("USB1020_StartBitInterpolation_3D", "cdecl"):
    USB1020_StartBitInterpolation_3D = _libs["./USB1020_64"].get("USB1020_StartBitInterpolation_3D", "cdecl")
    USB1020_StartBitInterpolation_3D.argtypes = [HANDLE]
    USB1020_StartBitInterpolation_3D.restype = BOOL

# ./USB1020_64.h: 708
if _libs["./USB1020_64"].has("USB1020_BPWait", "cdecl"):
    USB1020_BPWait = _libs["./USB1020_64"].get("USB1020_BPWait", "cdecl")
    USB1020_BPWait.argtypes = [HANDLE, PBOOL]
    USB1020_BPWait.restype = BOOL

# ./USB1020_64.h: 712
if _libs["./USB1020_64"].has("USB1020_ClearBPData", "cdecl"):
    USB1020_ClearBPData = _libs["./USB1020_64"].get("USB1020_ClearBPData", "cdecl")
    USB1020_ClearBPData.argtypes = [HANDLE]
    USB1020_ClearBPData.restype = BOOL

# ./USB1020_64.h: 716
if _libs["./USB1020_64"].has("USB1020_NextWait", "cdecl"):
    USB1020_NextWait = _libs["./USB1020_64"].get("USB1020_NextWait", "cdecl")
    USB1020_NextWait.argtypes = [HANDLE]
    USB1020_NextWait.restype = BOOL

# ./USB1020_64.h: 721
if _libs["./USB1020_64"].has("USB1020_SingleStepInterpolationCom", "cdecl"):
    USB1020_SingleStepInterpolationCom = _libs["./USB1020_64"].get("USB1020_SingleStepInterpolationCom", "cdecl")
    USB1020_SingleStepInterpolationCom.argtypes = [HANDLE]
    USB1020_SingleStepInterpolationCom.restype = BOOL

# ./USB1020_64.h: 724
if _libs["./USB1020_64"].has("USB1020_StartSingleStepInterpolation", "cdecl"):
    USB1020_StartSingleStepInterpolation = _libs["./USB1020_64"].get("USB1020_StartSingleStepInterpolation", "cdecl")
    USB1020_StartSingleStepInterpolation.argtypes = [HANDLE]
    USB1020_StartSingleStepInterpolation.restype = BOOL

# ./USB1020_64.h: 727
if _libs["./USB1020_64"].has("USB1020_SingleStepInterpolationExt", "cdecl"):
    USB1020_SingleStepInterpolationExt = _libs["./USB1020_64"].get("USB1020_SingleStepInterpolationExt", "cdecl")
    USB1020_SingleStepInterpolationExt.argtypes = [HANDLE]
    USB1020_SingleStepInterpolationExt.restype = BOOL

# ./USB1020_64.h: 730
if _libs["./USB1020_64"].has("USB1020_ClearSingleStepInterpolation", "cdecl"):
    USB1020_ClearSingleStepInterpolation = _libs["./USB1020_64"].get("USB1020_ClearSingleStepInterpolation", "cdecl")
    USB1020_ClearSingleStepInterpolation.argtypes = [HANDLE]
    USB1020_ClearSingleStepInterpolation.restype = BOOL

# ./USB1020_64.h: 734
if _libs["./USB1020_64"].has("USB1020_SetInterruptBit", "cdecl"):
    USB1020_SetInterruptBit = _libs["./USB1020_64"].get("USB1020_SetInterruptBit", "cdecl")
    USB1020_SetInterruptBit.argtypes = [HANDLE, LONG, PUSB1020_PARA_Interrupt]
    USB1020_SetInterruptBit.restype = BOOL

# ./USB1020_64.h: 739
if _libs["./USB1020_64"].has("USB1020_ClearInterruptStatus", "cdecl"):
    USB1020_ClearInterruptStatus = _libs["./USB1020_64"].get("USB1020_ClearInterruptStatus", "cdecl")
    USB1020_ClearInterruptStatus.argtypes = [HANDLE]
    USB1020_ClearInterruptStatus.restype = BOOL

# ./USB1020_64.h: 745
if _libs["./USB1020_64"].has("USB1020_SetOutEnableDV", "cdecl"):
    USB1020_SetOutEnableDV = _libs["./USB1020_64"].get("USB1020_SetOutEnableDV", "cdecl")
    USB1020_SetOutEnableDV.argtypes = [HANDLE, LONG]
    USB1020_SetOutEnableDV.restype = BOOL

# ./USB1020_64.h: 749
if _libs["./USB1020_64"].has("USB1020_SetOutEnableLV", "cdecl"):
    USB1020_SetOutEnableLV = _libs["./USB1020_64"].get("USB1020_SetOutEnableLV", "cdecl")
    USB1020_SetOutEnableLV.argtypes = [HANDLE, LONG]
    USB1020_SetOutEnableLV.restype = BOOL

# ./USB1020_64.h: 755
if _libs["./USB1020_64"].has("USB1020_SetPDirSoftwareLimit", "cdecl"):
    USB1020_SetPDirSoftwareLimit = _libs["./USB1020_64"].get("USB1020_SetPDirSoftwareLimit", "cdecl")
    USB1020_SetPDirSoftwareLimit.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetPDirSoftwareLimit.restype = BOOL

# ./USB1020_64.h: 761
if _libs["./USB1020_64"].has("USB1020_SetMDirSoftwareLimit", "cdecl"):
    USB1020_SetMDirSoftwareLimit = _libs["./USB1020_64"].get("USB1020_SetMDirSoftwareLimit", "cdecl")
    USB1020_SetMDirSoftwareLimit.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetMDirSoftwareLimit.restype = BOOL

# ./USB1020_64.h: 767
if _libs["./USB1020_64"].has("USB1020_ClearSoftwareLimit", "cdecl"):
    USB1020_ClearSoftwareLimit = _libs["./USB1020_64"].get("USB1020_ClearSoftwareLimit", "cdecl")
    USB1020_ClearSoftwareLimit.argtypes = [HANDLE, LONG]
    USB1020_ClearSoftwareLimit.restype = BOOL

# ./USB1020_64.h: 773
if _libs["./USB1020_64"].has("USB1020_SetPDirLMTEnable", "cdecl"):
    USB1020_SetPDirLMTEnable = _libs["./USB1020_64"].get("USB1020_SetPDirLMTEnable", "cdecl")
    USB1020_SetPDirLMTEnable.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetPDirLMTEnable.restype = BOOL

# ./USB1020_64.h: 779
if _libs["./USB1020_64"].has("USB1020_SetMDirLMTEnable", "cdecl"):
    USB1020_SetMDirLMTEnable = _libs["./USB1020_64"].get("USB1020_SetMDirLMTEnable", "cdecl")
    USB1020_SetMDirLMTEnable.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetMDirLMTEnable.restype = BOOL

# ./USB1020_64.h: 785
if _libs["./USB1020_64"].has("USB1020_SetStopEnable", "cdecl"):
    USB1020_SetStopEnable = _libs["./USB1020_64"].get("USB1020_SetStopEnable", "cdecl")
    USB1020_SetStopEnable.argtypes = [HANDLE, LONG, LONG, LONG]
    USB1020_SetStopEnable.restype = BOOL

# ./USB1020_64.h: 791
if _libs["./USB1020_64"].has("USB1020_SetStopDisable", "cdecl"):
    USB1020_SetStopDisable = _libs["./USB1020_64"].get("USB1020_SetStopDisable", "cdecl")
    USB1020_SetStopDisable.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetStopDisable.restype = BOOL

# ./USB1020_64.h: 796
if _libs["./USB1020_64"].has("USB1020_SetALARMEnable", "cdecl"):
    USB1020_SetALARMEnable = _libs["./USB1020_64"].get("USB1020_SetALARMEnable", "cdecl")
    USB1020_SetALARMEnable.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetALARMEnable.restype = BOOL

# ./USB1020_64.h: 801
if _libs["./USB1020_64"].has("USB1020_SetALARMDisable", "cdecl"):
    USB1020_SetALARMDisable = _libs["./USB1020_64"].get("USB1020_SetALARMDisable", "cdecl")
    USB1020_SetALARMDisable.argtypes = [HANDLE, LONG]
    USB1020_SetALARMDisable.restype = BOOL

# ./USB1020_64.h: 805
if _libs["./USB1020_64"].has("USB1020_SetINPOSEnable", "cdecl"):
    USB1020_SetINPOSEnable = _libs["./USB1020_64"].get("USB1020_SetINPOSEnable", "cdecl")
    USB1020_SetINPOSEnable.argtypes = [HANDLE, LONG, LONG]
    USB1020_SetINPOSEnable.restype = BOOL

# ./USB1020_64.h: 810
if _libs["./USB1020_64"].has("USB1020_SetINPOSDisable", "cdecl"):
    USB1020_SetINPOSDisable = _libs["./USB1020_64"].get("USB1020_SetINPOSDisable", "cdecl")
    USB1020_SetINPOSDisable.argtypes = [HANDLE, LONG]
    USB1020_SetINPOSDisable.restype = BOOL

# ./USB1020_64.h: 817
if _libs["./USB1020_64"].has("USB1020_DecValid", "cdecl"):
    USB1020_DecValid = _libs["./USB1020_64"].get("USB1020_DecValid", "cdecl")
    USB1020_DecValid.argtypes = [HANDLE]
    USB1020_DecValid.restype = BOOL

# ./USB1020_64.h: 820
if _libs["./USB1020_64"].has("USB1020_DecInvalid", "cdecl"):
    USB1020_DecInvalid = _libs["./USB1020_64"].get("USB1020_DecInvalid", "cdecl")
    USB1020_DecInvalid.argtypes = [HANDLE]
    USB1020_DecInvalid.restype = BOOL

# ./USB1020_64.h: 823
if _libs["./USB1020_64"].has("USB1020_DecStop", "cdecl"):
    USB1020_DecStop = _libs["./USB1020_64"].get("USB1020_DecStop", "cdecl")
    USB1020_DecStop.argtypes = [HANDLE, LONG]
    USB1020_DecStop.restype = BOOL

# ./USB1020_64.h: 827
if _libs["./USB1020_64"].has("USB1020_InstStop", "cdecl"):
    USB1020_InstStop = _libs["./USB1020_64"].get("USB1020_InstStop", "cdecl")
    USB1020_InstStop.argtypes = [HANDLE, LONG]
    USB1020_InstStop.restype = BOOL

# ./USB1020_64.h: 831
if _libs["./USB1020_64"].has("USB1020_AutoDec", "cdecl"):
    USB1020_AutoDec = _libs["./USB1020_64"].get("USB1020_AutoDec", "cdecl")
    USB1020_AutoDec.argtypes = [HANDLE, LONG]
    USB1020_AutoDec.restype = BOOL

# ./USB1020_64.h: 835
if _libs["./USB1020_64"].has("USB1020_HanDec", "cdecl"):
    USB1020_HanDec = _libs["./USB1020_64"].get("USB1020_HanDec", "cdecl")
    USB1020_HanDec.argtypes = [HANDLE, LONG, LONG]
    USB1020_HanDec.restype = BOOL

# ./USB1020_64.h: 842
if _libs["./USB1020_64"].has("USB1020_ReadLP", "cdecl"):
    USB1020_ReadLP = _libs["./USB1020_64"].get("USB1020_ReadLP", "cdecl")
    USB1020_ReadLP.argtypes = [HANDLE, LONG]
    USB1020_ReadLP.restype = LONG

# ./USB1020_64.h: 846
if _libs["./USB1020_64"].has("USB1020_ReadEP", "cdecl"):
    USB1020_ReadEP = _libs["./USB1020_64"].get("USB1020_ReadEP", "cdecl")
    USB1020_ReadEP.argtypes = [HANDLE, LONG]
    USB1020_ReadEP.restype = LONG

# ./USB1020_64.h: 850
if _libs["./USB1020_64"].has("USB1020_ReadBR", "cdecl"):
    USB1020_ReadBR = _libs["./USB1020_64"].get("USB1020_ReadBR", "cdecl")
    USB1020_ReadBR.argtypes = [HANDLE, LONG]
    USB1020_ReadBR.restype = LONG

# ./USB1020_64.h: 854
if _libs["./USB1020_64"].has("USB1020_ReadCV", "cdecl"):
    USB1020_ReadCV = _libs["./USB1020_64"].get("USB1020_ReadCV", "cdecl")
    USB1020_ReadCV.argtypes = [HANDLE, LONG]
    USB1020_ReadCV.restype = LONG

# ./USB1020_64.h: 858
if _libs["./USB1020_64"].has("USB1020_ReadCA", "cdecl"):
    USB1020_ReadCA = _libs["./USB1020_64"].get("USB1020_ReadCA", "cdecl")
    USB1020_ReadCA.argtypes = [HANDLE, LONG]
    USB1020_ReadCA.restype = LONG

# ./USB1020_64.h: 864
if _libs["./USB1020_64"].has("USB1020_OutSwitch", "cdecl"):
    USB1020_OutSwitch = _libs["./USB1020_64"].get("USB1020_OutSwitch", "cdecl")
    USB1020_OutSwitch.argtypes = [HANDLE, LONG, LONG]
    USB1020_OutSwitch.restype = BOOL

# ./USB1020_64.h: 869
if _libs["./USB1020_64"].has("USB1020_SetDeviceDO", "cdecl"):
    USB1020_SetDeviceDO = _libs["./USB1020_64"].get("USB1020_SetDeviceDO", "cdecl")
    USB1020_SetDeviceDO.argtypes = [HANDLE, LONG, PUSB1020_PARA_DO]
    USB1020_SetDeviceDO.restype = BOOL

# ./USB1020_64.h: 875
if _libs["./USB1020_64"].has("USB1020_ReadRR", "cdecl"):
    USB1020_ReadRR = _libs["./USB1020_64"].get("USB1020_ReadRR", "cdecl")
    USB1020_ReadRR.argtypes = [HANDLE, LONG, LONG]
    USB1020_ReadRR.restype = LONG

# ./USB1020_64.h: 880
if _libs["./USB1020_64"].has("USB1020_GetRR0Status", "cdecl"):
    USB1020_GetRR0Status = _libs["./USB1020_64"].get("USB1020_GetRR0Status", "cdecl")
    USB1020_GetRR0Status.argtypes = [HANDLE, PUSB1020_PARA_RR0]
    USB1020_GetRR0Status.restype = BOOL

# ./USB1020_64.h: 884
if _libs["./USB1020_64"].has("USB1020_GetRR1Status", "cdecl"):
    USB1020_GetRR1Status = _libs["./USB1020_64"].get("USB1020_GetRR1Status", "cdecl")
    USB1020_GetRR1Status.argtypes = [HANDLE, LONG, PUSB1020_PARA_RR1]
    USB1020_GetRR1Status.restype = BOOL

# ./USB1020_64.h: 889
if _libs["./USB1020_64"].has("USB1020_GetRR2Status", "cdecl"):
    USB1020_GetRR2Status = _libs["./USB1020_64"].get("USB1020_GetRR2Status", "cdecl")
    USB1020_GetRR2Status.argtypes = [HANDLE, LONG, PUSB1020_PARA_RR2]
    USB1020_GetRR2Status.restype = BOOL

# ./USB1020_64.h: 894
if _libs["./USB1020_64"].has("USB1020_GetRR3Status", "cdecl"):
    USB1020_GetRR3Status = _libs["./USB1020_64"].get("USB1020_GetRR3Status", "cdecl")
    USB1020_GetRR3Status.argtypes = [HANDLE, PUSB1020_PARA_RR3]
    USB1020_GetRR3Status.restype = BOOL

# ./USB1020_64.h: 898
if _libs["./USB1020_64"].has("USB1020_GetRR4Status", "cdecl"):
    USB1020_GetRR4Status = _libs["./USB1020_64"].get("USB1020_GetRR4Status", "cdecl")
    USB1020_GetRR4Status.argtypes = [HANDLE, PUSB1020_PARA_RR4]
    USB1020_GetRR4Status.restype = BOOL

# ./USB1020_64.h: 902
if _libs["./USB1020_64"].has("USB1020_GetRR5Status", "cdecl"):
    USB1020_GetRR5Status = _libs["./USB1020_64"].get("USB1020_GetRR5Status", "cdecl")
    USB1020_GetRR5Status.argtypes = [HANDLE, LONG, PUSB1020_PARA_RR5]
    USB1020_GetRR5Status.restype = BOOL

# ./USB1020_64.h: 75
try:
    USB1020_XAXIS = 0
except:
    pass

# ./USB1020_64.h: 76
try:
    USB1020_YAXIS = 1
except:
    pass

# ./USB1020_64.h: 77
try:
    USB1020_ZAXIS = 2
except:
    pass

# ./USB1020_64.h: 78
try:
    USB1020_UAXIS = 3
except:
    pass

# ./USB1020_64.h: 79
try:
    USB1020_ALLAXIS = 15
except:
    pass

# ./USB1020_64.h: 83
try:
    USB1020_DV = 0
except:
    pass

# ./USB1020_64.h: 84
try:
    USB1020_LV = 1
except:
    pass

# ./USB1020_64.h: 88
try:
    USB1020_AUTO = 0
except:
    pass

# ./USB1020_64.h: 89
try:
    USB1020_HAND = 1
except:
    pass

# ./USB1020_64.h: 93
try:
    USB1020_CWCCW = 0
except:
    pass

# ./USB1020_64.h: 94
try:
    USB1020_CPDIR = 1
except:
    pass

# ./USB1020_64.h: 109
try:
    USB1020_LINE = 0
except:
    pass

# ./USB1020_64.h: 110
try:
    USB1020_CURVE = 1
except:
    pass

# ./USB1020_64.h: 114
try:
    USB1020_MDIRECTION = 0
except:
    pass

# ./USB1020_64.h: 115
try:
    USB1020_PDIRECTION = 1
except:
    pass

# ./USB1020_64.h: 126
try:
    USB1020_LOGIC = 0
except:
    pass

# ./USB1020_64.h: 127
try:
    USB1020_FACT = 1
except:
    pass

# ./USB1020_64.h: 138
try:
    USB1020_SUDDENSTOP = 0
except:
    pass

# ./USB1020_64.h: 143
try:
    USB1020_GENERALOUT = 0
except:
    pass

_USB1020_PARA_DataList = struct__USB1020_PARA_DataList# ./USB1020_64.h: 19

_USB1020_PARA_LCData = struct__USB1020_PARA_LCData# ./USB1020_64.h: 35

_USB1020_PARA_InterpolationAxis = struct__USB1020_PARA_InterpolationAxis# ./USB1020_64.h: 45

_USB1020_PARA_LineData = struct__USB1020_PARA_LineData# ./USB1020_64.h: 57

_USB1020_PARA_CircleData = struct__USB1020_PARA_CircleData# ./USB1020_64.h: 70

_USB1020_PARA_Interrupt = struct__USB1020_PARA_Interrupt# ./USB1020_64.h: 165

_USB1020_PARA_SynchronActionOwnAxis = struct__USB1020_PARA_SynchronActionOwnAxis# ./USB1020_64.h: 190

_USB1020_PARA_SynchronActionOtherAxis = struct__USB1020_PARA_SynchronActionOtherAxis# ./USB1020_64.h: 211

_USB1020_PARA_ExpMode = struct__USB1020_PARA_ExpMode# ./USB1020_64.h: 234

_USB1020_PARA_DCC = struct__USB1020_PARA_DCC# ./USB1020_64.h: 250

_USB1020_PARA_AutoHomeSearch = struct__USB1020_PARA_AutoHomeSearch# ./USB1020_64.h: 269

_USB1020_PARA_DO = struct__USB1020_PARA_DO# ./USB1020_64.h: 284

_USB1020_PARA_RR0 = struct__USB1020_PARA_RR0# ./USB1020_64.h: 309

_USB1020_PARA_RR1 = struct__USB1020_PARA_RR1# ./USB1020_64.h: 332

_USB1020_PARA_RR2 = struct__USB1020_PARA_RR2# ./USB1020_64.h: 352

_USB1020_PARA_RR3 = struct__USB1020_PARA_RR3# ./USB1020_64.h: 375

_USB1020_PARA_RR4 = struct__USB1020_PARA_RR4# ./USB1020_64.h: 398

_USB1020_PARA_RR5 = struct__USB1020_PARA_RR5# ./USB1020_64.h: 416

# No inserted files

# No prefix-stripping

