# -*- coding: utf-8 -*-

"""MultiCard.py:
Wrapper for MultiCard.h
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220106"

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
_libs["MultiCard"] = load_library("MultiCard")

# 1 libraries
# End libraries

# No modules

GAS_IOCallBackFun = CFUNCTYPE(UNCHECKED(None), c_ulong, c_ulong)# MultiCard.h: 14

# MultiCard.h: 111
class struct_TrapPrm(Structure):
    pass

struct_TrapPrm._pack_ = 2
struct_TrapPrm.__slots__ = [
    'acc',
    'dec',
    'velStart',
    'smoothTime',
]
struct_TrapPrm._fields_ = [
    ('acc', c_double),
    ('dec', c_double),
    ('velStart', c_double),
    ('smoothTime', c_short),
]

TTrapPrm = struct_TrapPrm# MultiCard.h: 111

# MultiCard.h: 119
class struct_JogPrm(Structure):
    pass

struct_JogPrm._pack_ = 2
struct_JogPrm.__slots__ = [
    'dAcc',
    'dDec',
    'dSmooth',
]
struct_JogPrm._fields_ = [
    ('dAcc', c_double),
    ('dDec', c_double),
    ('dSmooth', c_double),
]

TJogPrm = struct_JogPrm# MultiCard.h: 119

# MultiCard.h: 126
class struct__CrdDataState(Structure):
    pass

struct__CrdDataState._pack_ = 2
struct__CrdDataState.__slots__ = [
    'dLength',
    'dSynLength',
    'dEndSpeed',
]
struct__CrdDataState._fields_ = [
    ('dLength', c_double * int(8)),
    ('dSynLength', c_double),
    ('dEndSpeed', c_double),
]

TCrdDataState = struct__CrdDataState# MultiCard.h: 126

# MultiCard.h: 138
class struct__CrdPrm(Structure):
    pass

struct__CrdPrm._pack_ = 2
struct__CrdPrm.__slots__ = [
    'dimension',
    'profile',
    'synVelMax',
    'synAccMax',
    'evenTime',
    'setOriginFlag',
    'originPos',
]
struct__CrdPrm._fields_ = [
    ('dimension', c_short),
    ('profile', c_short * int(8)),
    ('synVelMax', c_double),
    ('synAccMax', c_double),
    ('evenTime', c_short),
    ('setOriginFlag', c_short),
    ('originPos', c_long * int(8)),
]

TCrdPrm = struct__CrdPrm# MultiCard.h: 138

enum__CMD_TYPE = c_int# MultiCard.h: 141

CMD_G00 = 1# MultiCard.h: 141

CMD_G01 = (CMD_G00 + 1)# MultiCard.h: 141

CMD_G02 = (CMD_G01 + 1)# MultiCard.h: 141

CMD_G03 = (CMD_G02 + 1)# MultiCard.h: 141

CMD_G04 = (CMD_G03 + 1)# MultiCard.h: 141

CMD_G05 = (CMD_G04 + 1)# MultiCard.h: 141

CMD_G54 = (CMD_G05 + 1)# MultiCard.h: 141

CMD_M00 = 11# MultiCard.h: 141

CMD_M30 = (CMD_M00 + 1)# MultiCard.h: 141

CMD_M31 = (CMD_M30 + 1)# MultiCard.h: 141

CMD_M32 = (CMD_M31 + 1)# MultiCard.h: 141

CMD_M99 = (CMD_M32 + 1)# MultiCard.h: 141

CMD_SET_IO = 101# MultiCard.h: 141

CMD_WAIT_IO = (CMD_SET_IO + 1)# MultiCard.h: 141

CMD_BUFFER_MOVE_SET_POS = (CMD_WAIT_IO + 1)# MultiCard.h: 141

CMD_BUFFER_MOVE_SET_VEL = (CMD_BUFFER_MOVE_SET_POS + 1)# MultiCard.h: 141

CMD_BUFFER_MOVE_SET_ACC = (CMD_BUFFER_MOVE_SET_VEL + 1)# MultiCard.h: 141

CMD_BUFFER_GEAR = (CMD_BUFFER_MOVE_SET_ACC + 1)# MultiCard.h: 141

# MultiCard.h: 168
class struct__G00PARA(Structure):
    pass

struct__G00PARA._pack_ = 2
struct__G00PARA.__slots__ = [
    'synVel',
    'synAcc',
    'lX',
    'lY',
    'lZ',
    'lA',
    'iDimension',
    'segNum',
]
struct__G00PARA._fields_ = [
    ('synVel', c_float),
    ('synAcc', c_float),
    ('lX', c_long),
    ('lY', c_long),
    ('lZ', c_long),
    ('lA', c_long),
    ('iDimension', c_ubyte),
    ('segNum', c_long),
]

# MultiCard.h: 180
class struct__G01PARA(Structure):
    pass

struct__G01PARA._pack_ = 2
struct__G01PARA.__slots__ = [
    'synVel',
    'synAcc',
    'velEnd',
    'lX',
    'lY',
    'lZ',
    'lA',
    'segNum',
    'iDimension',
    'iPreciseStopFlag',
]
struct__G01PARA._fields_ = [
    ('synVel', c_float),
    ('synAcc', c_float),
    ('velEnd', c_float),
    ('lX', c_long),
    ('lY', c_long),
    ('lZ', c_long),
    ('lA', c_long),
    ('segNum', c_long),
    ('iDimension', c_ubyte),
    ('iPreciseStopFlag', c_ubyte),
]

# MultiCard.h: 197
class struct__G02_3PARA(Structure):
    pass

struct__G02_3PARA._pack_ = 2
struct__G02_3PARA.__slots__ = [
    'synVel',
    'synAcc',
    'velEnd',
    'iPlaneSelect',
    'iEnd1',
    'iEnd2',
    'iI',
    'iJ',
    'segNum',
    'iPreciseStopFlag',
]
struct__G02_3PARA._fields_ = [
    ('synVel', c_float),
    ('synAcc', c_float),
    ('velEnd', c_float),
    ('iPlaneSelect', c_int),
    ('iEnd1', c_int),
    ('iEnd2', c_int),
    ('iI', c_int),
    ('iJ', c_int),
    ('segNum', c_long),
    ('iPreciseStopFlag', c_ubyte),
]

# MultiCard.h: 211
class struct__G04PARA(Structure):
    pass

struct__G04PARA._pack_ = 2
struct__G04PARA.__slots__ = [
    'ulDelayTime',
    'segNum',
]
struct__G04PARA._fields_ = [
    ('ulDelayTime', c_ulong),
    ('segNum', c_long),
]

# MultiCard.h: 217
class struct__G05PARA(Structure):
    pass

struct__G05PARA._pack_ = 2
struct__G05PARA.__slots__ = [
    'lUserSegNum',
]
struct__G05PARA._fields_ = [
    ('lUserSegNum', c_long),
]

# MultiCard.h: 222
class struct__BufferMoveGearPARA(Structure):
    pass

struct__BufferMoveGearPARA._pack_ = 2
struct__BufferMoveGearPARA.__slots__ = [
    'lAxis1Pos',
    'lUserSegNum',
    'cAxisMask',
    'cModalMask',
]
struct__BufferMoveGearPARA._fields_ = [
    ('lAxis1Pos', c_long * int(8)),
    ('lUserSegNum', c_long),
    ('cAxisMask', c_ubyte),
    ('cModalMask', c_ubyte),
]

# MultiCard.h: 230
class struct__BufferMoveVelAccPARA(Structure):
    pass

struct__BufferMoveVelAccPARA._pack_ = 2
struct__BufferMoveVelAccPARA.__slots__ = [
    'dVelAcc',
    'lUserSegNum',
    'cAxisMask',
]
struct__BufferMoveVelAccPARA._fields_ = [
    ('dVelAcc', c_float * int(8)),
    ('lUserSegNum', c_long),
    ('cAxisMask', c_ubyte),
]

# MultiCard.h: 237
class struct__SetIOPara(Structure):
    pass

struct__SetIOPara._pack_ = 2
struct__SetIOPara.__slots__ = [
    'nCarkIndex',
    'nDoMask',
    'nDoValue',
    'lUserSegNum',
]
struct__SetIOPara._fields_ = [
    ('nCarkIndex', c_ushort),
    ('nDoMask', c_ushort),
    ('nDoValue', c_ushort),
    ('lUserSegNum', c_long),
]

# MultiCard.h: 245
class union__CMDPara(Union):
    pass

union__CMDPara._pack_ = 2
union__CMDPara.__slots__ = [
    'G00PARA',
    'G01PARA',
    'G02_3PARA',
    'G04PARA',
    'G05PARA',
    'BufferMoveGearPARA',
    'BufferMoveVelAccPARA',
    'SetIOPara',
]
union__CMDPara._fields_ = [
    ('G00PARA', struct__G00PARA),
    ('G01PARA', struct__G01PARA),
    ('G02_3PARA', struct__G02_3PARA),
    ('G04PARA', struct__G04PARA),
    ('G05PARA', struct__G05PARA),
    ('BufferMoveGearPARA', struct__BufferMoveGearPARA),
    ('BufferMoveVelAccPARA', struct__BufferMoveVelAccPARA),
    ('SetIOPara', struct__SetIOPara),
]

# MultiCard.h: 260
class struct__CrdData(Structure):
    pass

struct__CrdData._pack_ = 2
struct__CrdData.__slots__ = [
    'CMDType',
    'CMDPara',
]
struct__CrdData._fields_ = [
    ('CMDType', c_ubyte),
    ('CMDPara', union__CMDPara),
]

TCrdData = struct__CrdData# MultiCard.h: 260

# MultiCard.h: 274
class struct__LookAheadPrm(Structure):
    pass

struct__LookAheadPrm._pack_ = 2
struct__LookAheadPrm.__slots__ = [
    'lookAheadNum',
    'dSpeedMax',
    'dAccMax',
    'dMaxStepSpeed',
    'dScale',
    'pLookAheadBuf',
]
struct__LookAheadPrm._fields_ = [
    ('lookAheadNum', c_int),
    ('dSpeedMax', c_double * int(6)),
    ('dAccMax', c_double * int(6)),
    ('dMaxStepSpeed', c_double * int(6)),
    ('dScale', c_double * int(6)),
    ('pLookAheadBuf', POINTER(TCrdData)),
]

TLookAheadPrm = struct__LookAheadPrm# MultiCard.h: 274

# MultiCard.h: 287
class struct__AxisHomeParm(Structure):
    pass

struct__AxisHomeParm._pack_ = 2
struct__AxisHomeParm.__slots__ = [
    'nHomeMode',
    'nHomeDir',
    'lOffset',
    'dHomeRapidVel',
    'dHomeLocatVel',
    'dHomeIndexVel',
    'dHomeAcc',
]
struct__AxisHomeParm._fields_ = [
    ('nHomeMode', c_short),
    ('nHomeDir', c_short),
    ('lOffset', c_long),
    ('dHomeRapidVel', c_double),
    ('dHomeLocatVel', c_double),
    ('dHomeIndexVel', c_double),
    ('dHomeAcc', c_double),
]

TAxisHomePrm = struct__AxisHomeParm# MultiCard.h: 287

# MultiCard.h: 308
class struct__AllSysStatusData(Structure):
    pass

struct__AllSysStatusData._pack_ = 2
struct__AllSysStatusData.__slots__ = [
    'dAxisEncPos',
    'dAxisPrfPos',
    'lAxisStatus',
    'nADCValue',
    'lUserSegNum',
    'lRemainderSegNum',
    'nCrdRunStatus',
    'lCrdSpace',
    'dCrdVel',
    'dCrdPos',
    'lLimitPosRaw',
    'lLimitNegRaw',
    'lAlarmRaw',
    'lHomeRaw',
    'lMPG',
    'lGpiRaw',
]
struct__AllSysStatusData._fields_ = [
    ('dAxisEncPos', c_double * int(9)),
    ('dAxisPrfPos', c_double * int(8)),
    ('lAxisStatus', c_ulong * int(8)),
    ('nADCValue', c_short * int(2)),
    ('lUserSegNum', c_long * int(2)),
    ('lRemainderSegNum', c_long * int(2)),
    ('nCrdRunStatus', c_short * int(2)),
    ('lCrdSpace', c_long * int(2)),
    ('dCrdVel', c_double * int(2)),
    ('dCrdPos', (c_double * int(5)) * int(2)),
    ('lLimitPosRaw', c_long),
    ('lLimitNegRaw', c_long),
    ('lAlarmRaw', c_long),
    ('lHomeRaw', c_long),
    ('lMPG', c_long),
    ('lGpiRaw', c_long * int(4)),
]

TAllSysStatusData = struct__AllSysStatusData# MultiCard.h: 308

# MultiCard.h: 323
class struct__ComDataFrameHead(Structure):
    pass

struct__ComDataFrameHead._pack_ = 2
struct__ComDataFrameHead.__slots__ = [
    'nCardNum',
    'nType',
    'nSubType',
    'nResult',
    'ulAxisMask',
    'nCrdMask',
    'nFrameCount',
    'nDataBufLen',
    'ulCRC',
]
struct__ComDataFrameHead._fields_ = [
    ('nCardNum', c_char),
    ('nType', c_char),
    ('nSubType', c_char),
    ('nResult', c_char),
    ('ulAxisMask', c_ulong),
    ('nCrdMask', c_ubyte),
    ('nFrameCount', c_ubyte),
    ('nDataBufLen', c_ushort),
    ('ulCRC', c_ulong),
]

TComDataFrameHead = struct__ComDataFrameHead# MultiCard.h: 323

# MultiCard.h: 340
class struct__LookAheadState(Structure):
    pass

struct__LookAheadState._pack_ = 2
struct__LookAheadState.__slots__ = [
    'iFirstTime',
    'iWriteIndex',
    'iNeedLookAhead',
    'iNeedAutoSendAllDataInBuf',
    'dTotalLength',
    'dStartSpeed',
    'dStartPos',
    'dModalPos',
    'dEndPos',
    'pCrdDataState',
    'iReserve1',
]
struct__LookAheadState._fields_ = [
    ('iFirstTime', c_int),
    ('iWriteIndex', c_int),
    ('iNeedLookAhead', c_int),
    ('iNeedAutoSendAllDataInBuf', c_int),
    ('dTotalLength', c_double),
    ('dStartSpeed', c_double),
    ('dStartPos', c_double * int(8)),
    ('dModalPos', c_double * int(8)),
    ('dEndPos', c_double * int(8)),
    ('pCrdDataState', POINTER(TCrdDataState)),
    ('iReserve1', c_int),
]

TLookAheadState = struct__LookAheadState# MultiCard.h: 340

# MultiCard.h: 347
class struct__ComDataFrame(Structure):
    pass

struct__ComDataFrame._pack_ = 2
struct__ComDataFrame.__slots__ = [
    'Head',
    'nDataBuf',
]
struct__ComDataFrame._fields_ = [
    ('Head', TComDataFrameHead),
    ('nDataBuf', c_ubyte * int(1100)),
]

TComDataFrame = struct__ComDataFrame# MultiCard.h: 347

# MultiCard.h: 361
for _lib in _libs.values():
    try:
        m_nCardNum = (c_short).in_dll(_lib, "m_nCardNum")
        break
    except:
        pass

# MultiCard.h: 363
for _lib in _libs.values():
    try:
        m_LookAheadCrdPrm = (TCrdPrm * int(2)).in_dll(_lib, "m_LookAheadCrdPrm")
        break
    except:
        pass

# MultiCard.h: 367
for _lib in _libs.values():
    try:
        m_LookAheadPrm = ((TLookAheadPrm * int(2)) * int(2)).in_dll(_lib, "m_LookAheadPrm")
        break
    except:
        pass

# MultiCard.h: 369
for _lib in _libs.values():
    try:
        mLookAheadState = ((TLookAheadState * int(2)) * int(2)).in_dll(_lib, "mLookAheadState")
        break
    except:
        pass

# MultiCard.h: 371
for _lib in _libs.values():
    if not _lib.has("ComWaitForResponseData", "cdecl"):
        continue
    ComWaitForResponseData = _lib.get("ComWaitForResponseData", "cdecl")
    ComWaitForResponseData.argtypes = [POINTER(TComDataFrame), POINTER(TComDataFrame)]
    ComWaitForResponseData.restype = c_int
    break

# MultiCard.h: 372
for _lib in _libs.values():
    if not _lib.has("ComSendData", "cdecl"):
        continue
    ComSendData = _lib.get("ComSendData", "cdecl")
    ComSendData.argtypes = [POINTER(TComDataFrame), POINTER(TComDataFrame)]
    ComSendData.restype = c_int
    break

# MultiCard.h: 373
for _lib in _libs.values():
    if not _lib.has("ComSendDataOpen", "cdecl"):
        continue
    ComSendDataOpen = _lib.get("ComSendDataOpen", "cdecl")
    ComSendDataOpen.argtypes = [String, c_int]
    ComSendDataOpen.restype = c_int
    break

# MultiCard.h: 374
for _lib in _libs.values():
    if not _lib.has("WriteFrameToLookAheadBuf", "cdecl"):
        continue
    WriteFrameToLookAheadBuf = _lib.get("WriteFrameToLookAheadBuf", "cdecl")
    WriteFrameToLookAheadBuf.argtypes = [c_short, c_short, POINTER(TCrdData)]
    WriteFrameToLookAheadBuf.restype = c_int
    break

# MultiCard.h: 375
for _lib in _libs.values():
    if not _lib.has("InitLookAheadBufCtrlData", "cdecl"):
        continue
    InitLookAheadBufCtrlData = _lib.get("InitLookAheadBufCtrlData", "cdecl")
    InitLookAheadBufCtrlData.argtypes = [c_short, c_short]
    InitLookAheadBufCtrlData.restype = c_int
    break

# MultiCard.h: 376
for _lib in _libs.values():
    if not _lib.has("LookAhead", "cdecl"):
        continue
    LookAhead = _lib.get("LookAhead", "cdecl")
    LookAhead.argtypes = [c_short, c_short]
    LookAhead.restype = c_int
    break

# MultiCard.h: 377
for _lib in _libs.values():
    if not _lib.has("ReadFrameFromLookAheadBuf", "cdecl"):
        continue
    ReadFrameFromLookAheadBuf = _lib.get("ReadFrameFromLookAheadBuf", "cdecl")
    ReadFrameFromLookAheadBuf.argtypes = [c_short, c_short, POINTER(TCrdData)]
    ReadFrameFromLookAheadBuf.restype = c_int
    break

# MultiCard.h: 378
for _lib in _libs.values():
    if not _lib.has("ClearLookAheadBuf", "cdecl"):
        continue
    ClearLookAheadBuf = _lib.get("ClearLookAheadBuf", "cdecl")
    ClearLookAheadBuf.argtypes = [c_short, c_short]
    ClearLookAheadBuf.restype = c_int
    break

# MultiCard.h: 379
for _lib in _libs.values():
    if not _lib.has("CalConSpeed", "cdecl"):
        continue
    CalConSpeed = _lib.get("CalConSpeed", "cdecl")
    CalConSpeed.argtypes = [c_short, c_short, POINTER(TCrdDataState), POINTER(TCrdDataState), POINTER(TCrdData), POINTER(TCrdData)]
    CalConSpeed.restype = c_double
    break

# MultiCard.h: 380
for _lib in _libs.values():
    if not _lib.has("IsLookAheadBufEmpty", "cdecl"):
        continue
    IsLookAheadBufEmpty = _lib.get("IsLookAheadBufEmpty", "cdecl")
    IsLookAheadBufEmpty.argtypes = [c_short, c_short]
    IsLookAheadBufEmpty.restype = c_int
    break

# MultiCard.h: 381
for _lib in _libs.values():
    if not _lib.has("IsLookAheadBufFull", "cdecl"):
        continue
    IsLookAheadBufFull = _lib.get("IsLookAheadBufFull", "cdecl")
    IsLookAheadBufFull.argtypes = [c_short, c_short]
    IsLookAheadBufFull.restype = c_int
    break

# MultiCard.h: 382
for _lib in _libs.values():
    if not _lib.has("CalculateAngleByRelativePos", "cdecl"):
        continue
    CalculateAngleByRelativePos = _lib.get("CalculateAngleByRelativePos", "cdecl")
    CalculateAngleByRelativePos.argtypes = [c_double, c_double]
    CalculateAngleByRelativePos.restype = c_float
    break

# MultiCard.h: 383
for _lib in _libs.values():
    if not _lib.has("CalEndSpeed", "cdecl"):
        continue
    CalEndSpeed = _lib.get("CalEndSpeed", "cdecl")
    CalEndSpeed.argtypes = [c_double, c_double, c_double]
    CalEndSpeed.restype = c_double
    break

# MultiCard.h: 385
for _lib in _libs.values():
    if not _lib.has("GetLookAheadBufRemainDataNum", "cdecl"):
        continue
    GetLookAheadBufRemainDataNum = _lib.get("GetLookAheadBufRemainDataNum", "cdecl")
    GetLookAheadBufRemainDataNum.argtypes = [c_short, c_short]
    GetLookAheadBufRemainDataNum.restype = c_int
    break

# MultiCard.h: 387
for _lib in _libs.values():
    if not _lib.has("MC_GetClockHighPrecision", "cdecl"):
        continue
    MC_GetClockHighPrecision = _lib.get("MC_GetClockHighPrecision", "cdecl")
    MC_GetClockHighPrecision.argtypes = [POINTER(c_ulong)]
    MC_GetClockHighPrecision.restype = c_int
    break

# MultiCard.h: 388
for _lib in _libs.values():
    if not _lib.has("MC_GetClock", "cdecl"):
        continue
    MC_GetClock = _lib.get("MC_GetClock", "cdecl")
    MC_GetClock.argtypes = [POINTER(c_ulong)]
    MC_GetClock.restype = c_int
    break

# MultiCard.h: 389
for _lib in _libs.values():
    if not _lib.has("MC_LoadConfig", "cdecl"):
        continue
    MC_LoadConfig = _lib.get("MC_LoadConfig", "cdecl")
    MC_LoadConfig.argtypes = [String]
    MC_LoadConfig.restype = c_int
    break

# MultiCard.h: 390
for _lib in _libs.values():
    if not _lib.has("MC_GetConfig", "cdecl"):
        continue
    MC_GetConfig = _lib.get("MC_GetConfig", "cdecl")
    MC_GetConfig.argtypes = []
    MC_GetConfig.restype = c_int
    break

# MultiCard.h: 391
for _lib in _libs.values():
    if not _lib.has("MC_GpiSns", "cdecl"):
        continue
    MC_GpiSns = _lib.get("MC_GpiSns", "cdecl")
    MC_GpiSns.argtypes = [c_ulong]
    MC_GpiSns.restype = c_int
    break

# MultiCard.h: 392
for _lib in _libs.values():
    if not _lib.has("MC_GetGpiSns", "cdecl"):
        continue
    MC_GetGpiSns = _lib.get("MC_GetGpiSns", "cdecl")
    MC_GetGpiSns.argtypes = [POINTER(c_ulong)]
    MC_GetGpiSns.restype = c_int
    break

# MultiCard.h: 393
for _lib in _libs.values():
    if not _lib.has("MC_GetProfileScale", "cdecl"):
        continue
    MC_GetProfileScale = _lib.get("MC_GetProfileScale", "cdecl")
    MC_GetProfileScale.argtypes = [c_short, POINTER(c_short), POINTER(c_short)]
    MC_GetProfileScale.restype = c_int
    break

# MultiCard.h: 394
for _lib in _libs.values():
    if not _lib.has("MC_SetMtrBias", "cdecl"):
        continue
    MC_SetMtrBias = _lib.get("MC_SetMtrBias", "cdecl")
    MC_SetMtrBias.argtypes = [c_short, c_short]
    MC_SetMtrBias.restype = c_int
    break

# MultiCard.h: 395
for _lib in _libs.values():
    if not _lib.has("MC_GetMtrBias", "cdecl"):
        continue
    MC_GetMtrBias = _lib.get("MC_GetMtrBias", "cdecl")
    MC_GetMtrBias.argtypes = [c_short, POINTER(c_short)]
    MC_GetMtrBias.restype = c_int
    break

# MultiCard.h: 396
for _lib in _libs.values():
    if not _lib.has("MC_SetMtrLmt", "cdecl"):
        continue
    MC_SetMtrLmt = _lib.get("MC_SetMtrLmt", "cdecl")
    MC_SetMtrLmt.argtypes = [c_short, c_short]
    MC_SetMtrLmt.restype = c_int
    break

# MultiCard.h: 397
for _lib in _libs.values():
    if not _lib.has("MC_GetMtrLmt", "cdecl"):
        continue
    MC_GetMtrLmt = _lib.get("MC_GetMtrLmt", "cdecl")
    MC_GetMtrLmt.argtypes = [c_short, POINTER(c_short)]
    MC_GetMtrLmt.restype = c_int
    break

# MultiCard.h: 399
for _lib in _libs.values():
    if not _lib.has("MC_SetFollowMaster", "cdecl"):
        continue
    MC_SetFollowMaster = _lib.get("MC_SetFollowMaster", "cdecl")
    MC_SetFollowMaster.argtypes = [c_short, c_short, c_short, c_short]
    MC_SetFollowMaster.restype = c_int
    break

# MultiCard.h: 400
for _lib in _libs.values():
    if not _lib.has("MC_GetFollowMaster", "cdecl"):
        continue
    MC_GetFollowMaster = _lib.get("MC_GetFollowMaster", "cdecl")
    MC_GetFollowMaster.argtypes = [c_short, POINTER(c_short), POINTER(c_short), POINTER(c_short)]
    MC_GetFollowMaster.restype = c_int
    break

# MultiCard.h: 401
for _lib in _libs.values():
    if not _lib.has("MC_SetFollowLoop", "cdecl"):
        continue
    MC_SetFollowLoop = _lib.get("MC_SetFollowLoop", "cdecl")
    MC_SetFollowLoop.argtypes = [c_short, c_short]
    MC_SetFollowLoop.restype = c_int
    break

# MultiCard.h: 402
for _lib in _libs.values():
    if not _lib.has("MC_GetFollowLoop", "cdecl"):
        continue
    MC_GetFollowLoop = _lib.get("MC_GetFollowLoop", "cdecl")
    MC_GetFollowLoop.argtypes = [c_short, POINTER(c_long)]
    MC_GetFollowLoop.restype = c_int
    break

# MultiCard.h: 403
for _lib in _libs.values():
    if not _lib.has("MC_SetFollowEvent", "cdecl"):
        continue
    MC_SetFollowEvent = _lib.get("MC_SetFollowEvent", "cdecl")
    MC_SetFollowEvent.argtypes = [c_short, c_short, c_short, c_long]
    MC_SetFollowEvent.restype = c_int
    break

# MultiCard.h: 404
for _lib in _libs.values():
    if not _lib.has("MC_GetFollowEvent", "cdecl"):
        continue
    MC_GetFollowEvent = _lib.get("MC_GetFollowEvent", "cdecl")
    MC_GetFollowEvent.argtypes = [c_short, POINTER(c_short), POINTER(c_short), POINTER(c_long)]
    MC_GetFollowEvent.restype = c_int
    break

# MultiCard.h: 405
for _lib in _libs.values():
    if not _lib.has("MC_FollowSpace", "cdecl"):
        continue
    MC_FollowSpace = _lib.get("MC_FollowSpace", "cdecl")
    MC_FollowSpace.argtypes = [c_short, POINTER(c_short), c_short]
    MC_FollowSpace.restype = c_int
    break

# MultiCard.h: 406
for _lib in _libs.values():
    if not _lib.has("MC_FollowData", "cdecl"):
        continue
    MC_FollowData = _lib.get("MC_FollowData", "cdecl")
    MC_FollowData.argtypes = [c_short, c_long, c_double, c_short, c_short]
    MC_FollowData.restype = c_int
    break

# MultiCard.h: 407
for _lib in _libs.values():
    if not _lib.has("MC_FollowClear", "cdecl"):
        continue
    MC_FollowClear = _lib.get("MC_FollowClear", "cdecl")
    MC_FollowClear.argtypes = [c_short, c_short]
    MC_FollowClear.restype = c_int
    break

# MultiCard.h: 408
for _lib in _libs.values():
    if not _lib.has("MC_FollowStart", "cdecl"):
        continue
    MC_FollowStart = _lib.get("MC_FollowStart", "cdecl")
    MC_FollowStart.argtypes = [c_long, c_long]
    MC_FollowStart.restype = c_int
    break

# MultiCard.h: 409
for _lib in _libs.values():
    if not _lib.has("MC_FollowSwitch", "cdecl"):
        continue
    MC_FollowSwitch = _lib.get("MC_FollowSwitch", "cdecl")
    MC_FollowSwitch.argtypes = [c_long]
    MC_FollowSwitch.restype = c_int
    break

# MultiCard.h: 410
for _lib in _libs.values():
    if not _lib.has("MC_SetFollowMemory", "cdecl"):
        continue
    MC_SetFollowMemory = _lib.get("MC_SetFollowMemory", "cdecl")
    MC_SetFollowMemory.argtypes = [c_short, c_short]
    MC_SetFollowMemory.restype = c_int
    break

# MultiCard.h: 411
for _lib in _libs.values():
    if not _lib.has("MC_GetFollowMemory", "cdecl"):
        continue
    MC_GetFollowMemory = _lib.get("MC_GetFollowMemory", "cdecl")
    MC_GetFollowMemory.argtypes = [c_short, POINTER(c_short)]
    MC_GetFollowMemory.restype = c_int
    break

# MultiCard.h: 412
for _lib in _libs.values():
    if not _lib.has("MC_SetPtLoop", "cdecl"):
        continue
    MC_SetPtLoop = _lib.get("MC_SetPtLoop", "cdecl")
    MC_SetPtLoop.argtypes = [c_short]
    MC_SetPtLoop.restype = c_int
    break

# MultiCard.h: 413
for _lib in _libs.values():
    if not _lib.has("MC_GetPtLoop", "cdecl"):
        continue
    MC_GetPtLoop = _lib.get("MC_GetPtLoop", "cdecl")
    MC_GetPtLoop.argtypes = [c_short]
    MC_GetPtLoop.restype = c_int
    break

# MultiCard.h: 414
for _lib in _libs.values():
    if not _lib.has("MC_PrfPvt", "cdecl"):
        continue
    MC_PrfPvt = _lib.get("MC_PrfPvt", "cdecl")
    MC_PrfPvt.argtypes = [c_short]
    MC_PrfPvt.restype = c_int
    break

# MultiCard.h: 415
for _lib in _libs.values():
    if not _lib.has("MC_SetPvtLoop", "cdecl"):
        continue
    MC_SetPvtLoop = _lib.get("MC_SetPvtLoop", "cdecl")
    MC_SetPvtLoop.argtypes = [c_short, c_long]
    MC_SetPvtLoop.restype = c_int
    break

# MultiCard.h: 416
for _lib in _libs.values():
    if not _lib.has("MC_GetPvtLoop", "cdecl"):
        continue
    MC_GetPvtLoop = _lib.get("MC_GetPvtLoop", "cdecl")
    MC_GetPvtLoop.argtypes = [c_short, POINTER(c_long), POINTER(c_long)]
    MC_GetPvtLoop.restype = c_int
    break

# MultiCard.h: 417
for _lib in _libs.values():
    if not _lib.has("MC_PvtTable", "cdecl"):
        continue
    MC_PvtTable = _lib.get("MC_PvtTable", "cdecl")
    MC_PvtTable.argtypes = [c_short, c_long, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    MC_PvtTable.restype = c_int
    break

# MultiCard.h: 418
for _lib in _libs.values():
    if not _lib.has("MC_PvtTableComplete", "cdecl"):
        continue
    MC_PvtTableComplete = _lib.get("MC_PvtTableComplete", "cdecl")
    MC_PvtTableComplete.argtypes = [c_short, c_long, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, c_double]
    MC_PvtTableComplete.restype = c_int
    break

# MultiCard.h: 419
for _lib in _libs.values():
    if not _lib.has("MC_PvtTablePercent", "cdecl"):
        continue
    MC_PvtTablePercent = _lib.get("MC_PvtTablePercent", "cdecl")
    MC_PvtTablePercent.argtypes = [c_short, c_long, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double]
    MC_PvtTablePercent.restype = c_int
    break

# MultiCard.h: 420
for _lib in _libs.values():
    if not _lib.has("MC_PvtPercentCalculate", "cdecl"):
        continue
    MC_PvtPercentCalculate = _lib.get("MC_PvtPercentCalculate", "cdecl")
    MC_PvtPercentCalculate.argtypes = [c_long, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, POINTER(c_double)]
    MC_PvtPercentCalculate.restype = c_int
    break

# MultiCard.h: 421
for _lib in _libs.values():
    if not _lib.has("MC_PvtTableContinuous", "cdecl"):
        continue
    MC_PvtTableContinuous = _lib.get("MC_PvtTableContinuous", "cdecl")
    MC_PvtTableContinuous.argtypes = [c_short, c_long, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double]
    MC_PvtTableContinuous.restype = c_int
    break

# MultiCard.h: 422
for _lib in _libs.values():
    if not _lib.has("MC_PvtContinuousCalculate", "cdecl"):
        continue
    MC_PvtContinuousCalculate = _lib.get("MC_PvtContinuousCalculate", "cdecl")
    MC_PvtContinuousCalculate.argtypes = [c_long, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    MC_PvtContinuousCalculate.restype = c_int
    break

# MultiCard.h: 423
for _lib in _libs.values():
    if not _lib.has("MC_PvtTableSelect", "cdecl"):
        continue
    MC_PvtTableSelect = _lib.get("MC_PvtTableSelect", "cdecl")
    MC_PvtTableSelect.argtypes = [c_short, c_short]
    MC_PvtTableSelect.restype = c_int
    break

# MultiCard.h: 424
for _lib in _libs.values():
    if not _lib.has("MC_PvtStart", "cdecl"):
        continue
    MC_PvtStart = _lib.get("MC_PvtStart", "cdecl")
    MC_PvtStart.argtypes = [c_long]
    MC_PvtStart.restype = c_int
    break

# MultiCard.h: 425
for _lib in _libs.values():
    if not _lib.has("MC_PvtStatus", "cdecl"):
        continue
    MC_PvtStatus = _lib.get("MC_PvtStatus", "cdecl")
    MC_PvtStatus.argtypes = [c_short, POINTER(c_short), POINTER(c_double), c_short]
    MC_PvtStatus.restype = c_int
    break

# MultiCard.h: 426
for _lib in _libs.values():
    if not _lib.has("MC_IntConfig", "cdecl"):
        continue
    MC_IntConfig = _lib.get("MC_IntConfig", "cdecl")
    MC_IntConfig.argtypes = [c_short, c_short, c_short]
    MC_IntConfig.restype = c_int
    break

# MultiCard.h: 427
for _lib in _libs.values():
    if not _lib.has("MC_GetIntConfig", "cdecl"):
        continue
    MC_GetIntConfig = _lib.get("MC_GetIntConfig", "cdecl")
    MC_GetIntConfig.argtypes = [c_short, c_short, POINTER(c_short)]
    MC_GetIntConfig.restype = c_int
    break

# MultiCard.h: 428
for _lib in _libs.values():
    if not _lib.has("MC_IntEnable", "cdecl"):
        continue
    MC_IntEnable = _lib.get("MC_IntEnable", "cdecl")
    MC_IntEnable.argtypes = [c_short, GAS_IOCallBackFun]
    MC_IntEnable.restype = c_int
    break

# MultiCard.h: 429
for _lib in _libs.values():
    if not _lib.has("MC_GetControlInfo", "cdecl"):
        continue
    MC_GetControlInfo = _lib.get("MC_GetControlInfo", "cdecl")
    MC_GetControlInfo.argtypes = [c_short]
    MC_GetControlInfo.restype = c_int
    break

# MultiCard.h: 430
for _lib in _libs.values():
    if not _lib.has("MC_StartWatch", "cdecl"):
        continue
    MC_StartWatch = _lib.get("MC_StartWatch", "cdecl")
    MC_StartWatch.argtypes = []
    MC_StartWatch.restype = c_int
    break

# MultiCard.h: 431
for _lib in _libs.values():
    if not _lib.has("MC_StopWatch", "cdecl"):
        continue
    MC_StopWatch = _lib.get("MC_StopWatch", "cdecl")
    MC_StopWatch.argtypes = []
    MC_StopWatch.restype = c_int
    break

# MultiCard.h: 432
for _lib in _libs.values():
    if not _lib.has("MC_FwUpdate", "cdecl"):
        continue
    MC_FwUpdate = _lib.get("MC_FwUpdate", "cdecl")
    MC_FwUpdate.argtypes = [String, c_ulong]
    MC_FwUpdate.restype = c_int
    break

# MultiCard.h: 455
for _lib in _libs.values():
    if not _lib.has("MC_CrdStartStep", "cdecl"):
        continue
    MC_CrdStartStep = _lib.get("MC_CrdStartStep", "cdecl")
    MC_CrdStartStep.argtypes = [c_short, c_short]
    MC_CrdStartStep.restype = c_int
    break

# MultiCard.h: 456
for _lib in _libs.values():
    if not _lib.has("MC_CrdStepMode", "cdecl"):
        continue
    MC_CrdStepMode = _lib.get("MC_CrdStepMode", "cdecl")
    MC_CrdStepMode.argtypes = [c_short, c_short]
    MC_CrdStepMode.restype = c_int
    break

# MultiCard.h: 457
for _lib in _libs.values():
    if not _lib.has("MC_SetCrdStopDec", "cdecl"):
        continue
    MC_SetCrdStopDec = _lib.get("MC_SetCrdStopDec", "cdecl")
    MC_SetCrdStopDec.argtypes = [c_short, c_double, c_double]
    MC_SetCrdStopDec.restype = c_int
    break

# MultiCard.h: 458
for _lib in _libs.values():
    if not _lib.has("MC_GetCrdStopDec", "cdecl"):
        continue
    MC_GetCrdStopDec = _lib.get("MC_GetCrdStopDec", "cdecl")
    MC_GetCrdStopDec.argtypes = [c_short, POINTER(c_double), POINTER(c_double)]
    MC_GetCrdStopDec.restype = c_int
    break

# MultiCard.h: 459
for _lib in _libs.values():
    if not _lib.has("MC_GetUserTargetVel", "cdecl"):
        continue
    MC_GetUserTargetVel = _lib.get("MC_GetUserTargetVel", "cdecl")
    MC_GetUserTargetVel.argtypes = [c_short, POINTER(c_double)]
    MC_GetUserTargetVel.restype = c_int
    break

# MultiCard.h: 460
for _lib in _libs.values():
    if not _lib.has("MC_GetSegTargetPos", "cdecl"):
        continue
    MC_GetSegTargetPos = _lib.get("MC_GetSegTargetPos", "cdecl")
    MC_GetSegTargetPos.argtypes = [c_short, POINTER(c_long)]
    MC_GetSegTargetPos.restype = c_int
    break

# MultiCard.h: 469
for _lib in _libs.values():
    if not _lib.has("MC_HomeInit", "cdecl"):
        continue
    MC_HomeInit = _lib.get("MC_HomeInit", "cdecl")
    MC_HomeInit.argtypes = []
    MC_HomeInit.restype = c_int
    break

# MultiCard.h: 470
for _lib in _libs.values():
    if not _lib.has("MC_Home", "cdecl"):
        continue
    MC_Home = _lib.get("MC_Home", "cdecl")
    MC_Home.argtypes = [c_short, c_long, c_double, c_double, c_long]
    MC_Home.restype = c_int
    break

# MultiCard.h: 471
for _lib in _libs.values():
    if not _lib.has("MC_Index", "cdecl"):
        continue
    MC_Index = _lib.get("MC_Index", "cdecl")
    MC_Index.argtypes = [c_short, c_long, c_long]
    MC_Index.restype = c_int
    break

# MultiCard.h: 472
for _lib in _libs.values():
    if not _lib.has("MC_HomeSts", "cdecl"):
        continue
    MC_HomeSts = _lib.get("MC_HomeSts", "cdecl")
    MC_HomeSts.argtypes = [c_short, POINTER(c_ushort)]
    MC_HomeSts.restype = c_int
    break

# MultiCard.h: 474
for _lib in _libs.values():
    if not _lib.has("MC_HandwheelInit", "cdecl"):
        continue
    MC_HandwheelInit = _lib.get("MC_HandwheelInit", "cdecl")
    MC_HandwheelInit.argtypes = []
    MC_HandwheelInit.restype = c_int
    break

# MultiCard.h: 475
for _lib in _libs.values():
    if not _lib.has("MC_SetHandwheelStopDec", "cdecl"):
        continue
    MC_SetHandwheelStopDec = _lib.get("MC_SetHandwheelStopDec", "cdecl")
    MC_SetHandwheelStopDec.argtypes = [c_short, c_double, c_double]
    MC_SetHandwheelStopDec.restype = c_int
    break

# MultiCard.h: 477
for _lib in _libs.values():
    if not _lib.has("MC_CmpRpt", "cdecl"):
        continue
    MC_CmpRpt = _lib.get("MC_CmpRpt", "cdecl")
    MC_CmpRpt.argtypes = [c_short, c_short, c_short, c_long, c_long, c_long, c_short]
    MC_CmpRpt.restype = c_int
    break

# MultiCard.h: 478
for _lib in _libs.values():
    if not _lib.has("MC_CmpRpt", "cdecl"):
        continue
    MC_CmpRpt = _lib.get("MC_CmpRpt", "cdecl")
    MC_CmpRpt.argtypes = [c_short, c_short, c_long, c_long, c_long, c_short, c_short, c_short]
    MC_CmpRpt.restype = c_int
    break

# MultiCard.h: 483
for _lib in _libs.values():
    if not _lib.has("MC_Open", "cdecl"):
        continue
    MC_Open = _lib.get("MC_Open", "cdecl")
    MC_Open.argtypes = [c_short, String, c_ushort, String, c_ushort]
    MC_Open.restype = c_int
    break

# MultiCard.h: 484
for _lib in _libs.values():
    if not _lib.has("MC_Close", "cdecl"):
        continue
    MC_Close = _lib.get("MC_Close", "cdecl")
    MC_Close.argtypes = []
    MC_Close.restype = c_int
    break

# MultiCard.h: 485
for _lib in _libs.values():
    if not _lib.has("MC_Reset", "cdecl"):
        continue
    MC_Reset = _lib.get("MC_Reset", "cdecl")
    MC_Reset.argtypes = []
    MC_Reset.restype = c_int
    break

# MultiCard.h: 486
for _lib in _libs.values():
    if not _lib.has("MC_GetVersion", "cdecl"):
        continue
    MC_GetVersion = _lib.get("MC_GetVersion", "cdecl")
    MC_GetVersion.argtypes = [String]
    MC_GetVersion.restype = c_int
    break

# MultiCard.h: 487
for _lib in _libs.values():
    if not _lib.has("MC_SetPrfPos", "cdecl"):
        continue
    MC_SetPrfPos = _lib.get("MC_SetPrfPos", "cdecl")
    MC_SetPrfPos.argtypes = [c_short, c_long]
    MC_SetPrfPos.restype = c_int
    break

# MultiCard.h: 488
for _lib in _libs.values():
    if not _lib.has("MC_SynchAxisPos", "cdecl"):
        continue
    MC_SynchAxisPos = _lib.get("MC_SynchAxisPos", "cdecl")
    MC_SynchAxisPos.argtypes = [c_long]
    MC_SynchAxisPos.restype = c_int
    break

# MultiCard.h: 490
for _lib in _libs.values():
    if not _lib.has("MC_SetAxisBand", "cdecl"):
        continue
    MC_SetAxisBand = _lib.get("MC_SetAxisBand", "cdecl")
    MC_SetAxisBand.argtypes = [c_short, c_long, c_long]
    MC_SetAxisBand.restype = c_int
    break

# MultiCard.h: 491
for _lib in _libs.values():
    if not _lib.has("MC_GetAxisBand", "cdecl"):
        continue
    MC_GetAxisBand = _lib.get("MC_GetAxisBand", "cdecl")
    MC_GetAxisBand.argtypes = [c_short, POINTER(c_long), POINTER(c_long)]
    MC_GetAxisBand.restype = c_int
    break

# MultiCard.h: 492
for _lib in _libs.values():
    if not _lib.has("MC_SetBacklash", "cdecl"):
        continue
    MC_SetBacklash = _lib.get("MC_SetBacklash", "cdecl")
    MC_SetBacklash.argtypes = [c_short, c_long, c_double, c_long]
    MC_SetBacklash.restype = c_int
    break

# MultiCard.h: 493
for _lib in _libs.values():
    if not _lib.has("MC_GetBacklash", "cdecl"):
        continue
    MC_GetBacklash = _lib.get("MC_GetBacklash", "cdecl")
    MC_GetBacklash.argtypes = [c_short, POINTER(c_long), POINTER(c_double), POINTER(c_long)]
    MC_GetBacklash.restype = c_int
    break

# MultiCard.h: 497
for _lib in _libs.values():
    if not _lib.has("MC_AlarmOn", "cdecl"):
        continue
    MC_AlarmOn = _lib.get("MC_AlarmOn", "cdecl")
    MC_AlarmOn.argtypes = [c_short]
    MC_AlarmOn.restype = c_int
    break

# MultiCard.h: 498
for _lib in _libs.values():
    if not _lib.has("MC_AlarmOff", "cdecl"):
        continue
    MC_AlarmOff = _lib.get("MC_AlarmOff", "cdecl")
    MC_AlarmOff.argtypes = [c_short]
    MC_AlarmOff.restype = c_int
    break

# MultiCard.h: 499
for _lib in _libs.values():
    if not _lib.has("MC_GetAlarmOnOff", "cdecl"):
        continue
    MC_GetAlarmOnOff = _lib.get("MC_GetAlarmOnOff", "cdecl")
    MC_GetAlarmOnOff.argtypes = [c_short, POINTER(c_short)]
    MC_GetAlarmOnOff.restype = c_int
    break

# MultiCard.h: 500
for _lib in _libs.values():
    if not _lib.has("MC_AlarmSns", "cdecl"):
        continue
    MC_AlarmSns = _lib.get("MC_AlarmSns", "cdecl")
    MC_AlarmSns.argtypes = [c_ushort]
    MC_AlarmSns.restype = c_int
    break

# MultiCard.h: 501
for _lib in _libs.values():
    if not _lib.has("MC_GetAlarmSns", "cdecl"):
        continue
    MC_GetAlarmSns = _lib.get("MC_GetAlarmSns", "cdecl")
    MC_GetAlarmSns.argtypes = [POINTER(c_ushort)]
    MC_GetAlarmSns.restype = c_int
    break

# MultiCard.h: 502
for _lib in _libs.values():
    if not _lib.has("MC_HomeSns", "cdecl"):
        continue
    MC_HomeSns = _lib.get("MC_HomeSns", "cdecl")
    MC_HomeSns.argtypes = [c_ushort]
    MC_HomeSns.restype = c_int
    break

# MultiCard.h: 503
for _lib in _libs.values():
    if not _lib.has("MC_GetHomeSns", "cdecl"):
        continue
    MC_GetHomeSns = _lib.get("MC_GetHomeSns", "cdecl")
    MC_GetHomeSns.argtypes = [POINTER(c_ushort)]
    MC_GetHomeSns.restype = c_int
    break

# MultiCard.h: 506
for _lib in _libs.values():
    if not _lib.has("MC_GetLmtsOnOff", "cdecl"):
        continue
    MC_GetLmtsOnOff = _lib.get("MC_GetLmtsOnOff", "cdecl")
    MC_GetLmtsOnOff.argtypes = [c_short, POINTER(c_short), POINTER(c_short)]
    MC_GetLmtsOnOff.restype = c_int
    break

# MultiCard.h: 507
for _lib in _libs.values():
    if not _lib.has("MC_LmtSns", "cdecl"):
        continue
    MC_LmtSns = _lib.get("MC_LmtSns", "cdecl")
    MC_LmtSns.argtypes = [c_ushort]
    MC_LmtSns.restype = c_int
    break

# MultiCard.h: 508
for _lib in _libs.values():
    if not _lib.has("MC_LmtSnsEX", "cdecl"):
        continue
    MC_LmtSnsEX = _lib.get("MC_LmtSnsEX", "cdecl")
    MC_LmtSnsEX.argtypes = [c_ulong]
    MC_LmtSnsEX.restype = c_int
    break

# MultiCard.h: 509
for _lib in _libs.values():
    if not _lib.has("MC_GetLmtSns", "cdecl"):
        continue
    MC_GetLmtSns = _lib.get("MC_GetLmtSns", "cdecl")
    MC_GetLmtSns.argtypes = [POINTER(c_ushort)]
    MC_GetLmtSns.restype = c_int
    break

# MultiCard.h: 510
for _lib in _libs.values():
    if not _lib.has("MC_ProfileScale", "cdecl"):
        continue
    MC_ProfileScale = _lib.get("MC_ProfileScale", "cdecl")
    MC_ProfileScale.argtypes = [c_short, c_short, c_short]
    MC_ProfileScale.restype = c_int
    break

# MultiCard.h: 511
for _lib in _libs.values():
    if not _lib.has("MC_EncScale", "cdecl"):
        continue
    MC_EncScale = _lib.get("MC_EncScale", "cdecl")
    MC_EncScale.argtypes = [c_short, c_short, c_short]
    MC_EncScale.restype = c_int
    break

# MultiCard.h: 512
for _lib in _libs.values():
    if not _lib.has("MC_GetEncScale", "cdecl"):
        continue
    MC_GetEncScale = _lib.get("MC_GetEncScale", "cdecl")
    MC_GetEncScale.argtypes = [c_short, POINTER(c_short), POINTER(c_short)]
    MC_GetEncScale.restype = c_int
    break

# MultiCard.h: 513
for _lib in _libs.values():
    if not _lib.has("MC_StepDir", "cdecl"):
        continue
    MC_StepDir = _lib.get("MC_StepDir", "cdecl")
    MC_StepDir.argtypes = [c_short]
    MC_StepDir.restype = c_int
    break

# MultiCard.h: 514
for _lib in _libs.values():
    if not _lib.has("MC_StepPulse", "cdecl"):
        continue
    MC_StepPulse = _lib.get("MC_StepPulse", "cdecl")
    MC_StepPulse.argtypes = [c_short]
    MC_StepPulse.restype = c_int
    break

# MultiCard.h: 515
for _lib in _libs.values():
    if not _lib.has("MC_GetStep", "cdecl"):
        continue
    MC_GetStep = _lib.get("MC_GetStep", "cdecl")
    MC_GetStep.argtypes = [c_short, POINTER(c_short)]
    MC_GetStep.restype = c_int
    break

# MultiCard.h: 516
for _lib in _libs.values():
    if not _lib.has("MC_StepSns", "cdecl"):
        continue
    MC_StepSns = _lib.get("MC_StepSns", "cdecl")
    MC_StepSns.argtypes = [c_ushort]
    MC_StepSns.restype = c_int
    break

# MultiCard.h: 517
for _lib in _libs.values():
    if not _lib.has("MC_GetStepSns", "cdecl"):
        continue
    MC_GetStepSns = _lib.get("MC_GetStepSns", "cdecl")
    MC_GetStepSns.argtypes = [POINTER(c_short)]
    MC_GetStepSns.restype = c_int
    break

# MultiCard.h: 518
for _lib in _libs.values():
    if not _lib.has("MC_EncSns", "cdecl"):
        continue
    MC_EncSns = _lib.get("MC_EncSns", "cdecl")
    MC_EncSns.argtypes = [c_ushort]
    MC_EncSns.restype = c_int
    break

# MultiCard.h: 519
for _lib in _libs.values():
    if not _lib.has("MC_GetEncSns", "cdecl"):
        continue
    MC_GetEncSns = _lib.get("MC_GetEncSns", "cdecl")
    MC_GetEncSns.argtypes = [POINTER(c_short)]
    MC_GetEncSns.restype = c_int
    break

# MultiCard.h: 520
for _lib in _libs.values():
    if not _lib.has("MC_EncOn", "cdecl"):
        continue
    MC_EncOn = _lib.get("MC_EncOn", "cdecl")
    MC_EncOn.argtypes = [c_short]
    MC_EncOn.restype = c_int
    break

# MultiCard.h: 521
for _lib in _libs.values():
    if not _lib.has("MC_EncOff", "cdecl"):
        continue
    MC_EncOff = _lib.get("MC_EncOff", "cdecl")
    MC_EncOff.argtypes = [c_short]
    MC_EncOff.restype = c_int
    break

# MultiCard.h: 522
for _lib in _libs.values():
    if not _lib.has("MC_GetEncOnOff", "cdecl"):
        continue
    MC_GetEncOnOff = _lib.get("MC_GetEncOnOff", "cdecl")
    MC_GetEncOnOff.argtypes = [c_short, POINTER(c_short)]
    MC_GetEncOnOff.restype = c_int
    break

# MultiCard.h: 523
for _lib in _libs.values():
    if not _lib.has("MC_SetPosErr", "cdecl"):
        continue
    MC_SetPosErr = _lib.get("MC_SetPosErr", "cdecl")
    MC_SetPosErr.argtypes = [c_short, c_long]
    MC_SetPosErr.restype = c_int
    break

# MultiCard.h: 524
for _lib in _libs.values():
    if not _lib.has("MC_GetPosErr", "cdecl"):
        continue
    MC_GetPosErr = _lib.get("MC_GetPosErr", "cdecl")
    MC_GetPosErr.argtypes = [c_short, POINTER(c_long)]
    MC_GetPosErr.restype = c_int
    break

# MultiCard.h: 525
for _lib in _libs.values():
    if not _lib.has("MC_SetStopDec", "cdecl"):
        continue
    MC_SetStopDec = _lib.get("MC_SetStopDec", "cdecl")
    MC_SetStopDec.argtypes = [c_short, c_double, c_double]
    MC_SetStopDec.restype = c_int
    break

# MultiCard.h: 526
for _lib in _libs.values():
    if not _lib.has("MC_GetStopDec", "cdecl"):
        continue
    MC_GetStopDec = _lib.get("MC_GetStopDec", "cdecl")
    MC_GetStopDec.argtypes = [c_short, POINTER(c_double), POINTER(c_double)]
    MC_GetStopDec.restype = c_int
    break

# MultiCard.h: 527
for _lib in _libs.values():
    if not _lib.has("MC_CtrlMode", "cdecl"):
        continue
    MC_CtrlMode = _lib.get("MC_CtrlMode", "cdecl")
    MC_CtrlMode.argtypes = [c_short, c_short]
    MC_CtrlMode.restype = c_int
    break

# MultiCard.h: 528
for _lib in _libs.values():
    if not _lib.has("MC_GetCtrlMode", "cdecl"):
        continue
    MC_GetCtrlMode = _lib.get("MC_GetCtrlMode", "cdecl")
    MC_GetCtrlMode.argtypes = [c_short, POINTER(c_short)]
    MC_GetCtrlMode.restype = c_int
    break

# MultiCard.h: 529
for _lib in _libs.values():
    if not _lib.has("MC_SetStopIo", "cdecl"):
        continue
    MC_SetStopIo = _lib.get("MC_SetStopIo", "cdecl")
    MC_SetStopIo.argtypes = [c_short, c_short, c_short, c_short]
    MC_SetStopIo.restype = c_int
    break

# MultiCard.h: 545
for _lib in _libs.values():
    if not _lib.has("MC_Stop", "cdecl"):
        continue
    MC_Stop = _lib.get("MC_Stop", "cdecl")
    MC_Stop.argtypes = [c_long, c_long]
    MC_Stop.restype = c_int
    break

# MultiCard.h: 546
for _lib in _libs.values():
    if not _lib.has("MC_AxisOn", "cdecl"):
        continue
    MC_AxisOn = _lib.get("MC_AxisOn", "cdecl")
    MC_AxisOn.argtypes = [c_short]
    MC_AxisOn.restype = c_int
    break

# MultiCard.h: 547
for _lib in _libs.values():
    if not _lib.has("MC_AxisOff", "cdecl"):
        continue
    MC_AxisOff = _lib.get("MC_AxisOff", "cdecl")
    MC_AxisOff.argtypes = [c_short]
    MC_AxisOff.restype = c_int
    break

# MultiCard.h: 548
for _lib in _libs.values():
    if not _lib.has("MC_GetAllSysStatus", "cdecl"):
        continue
    MC_GetAllSysStatus = _lib.get("MC_GetAllSysStatus", "cdecl")
    MC_GetAllSysStatus.argtypes = [POINTER(TAllSysStatusData)]
    MC_GetAllSysStatus.restype = c_int
    break

# MultiCard.h: 551
for _lib in _libs.values():
    if not _lib.has("MC_PrfTrap", "cdecl"):
        continue
    MC_PrfTrap = _lib.get("MC_PrfTrap", "cdecl")
    MC_PrfTrap.argtypes = [c_short]
    MC_PrfTrap.restype = c_int
    break

# MultiCard.h: 552
for _lib in _libs.values():
    if not _lib.has("MC_SetTrapPrm", "cdecl"):
        continue
    MC_SetTrapPrm = _lib.get("MC_SetTrapPrm", "cdecl")
    MC_SetTrapPrm.argtypes = [c_short, POINTER(TTrapPrm)]
    MC_SetTrapPrm.restype = c_int
    break

# MultiCard.h: 553
for _lib in _libs.values():
    if not _lib.has("MC_SetTrapPrmSingle", "cdecl"):
        continue
    MC_SetTrapPrmSingle = _lib.get("MC_SetTrapPrmSingle", "cdecl")
    MC_SetTrapPrmSingle.argtypes = [c_short, c_double, c_double, c_double, c_short]
    MC_SetTrapPrmSingle.restype = c_int
    break

# MultiCard.h: 554
for _lib in _libs.values():
    if not _lib.has("MC_GetTrapPrm", "cdecl"):
        continue
    MC_GetTrapPrm = _lib.get("MC_GetTrapPrm", "cdecl")
    MC_GetTrapPrm.argtypes = [c_short, POINTER(TTrapPrm)]
    MC_GetTrapPrm.restype = c_int
    break

# MultiCard.h: 555
for _lib in _libs.values():
    if not _lib.has("MC_GetTrapPrmSingle", "cdecl"):
        continue
    MC_GetTrapPrmSingle = _lib.get("MC_GetTrapPrmSingle", "cdecl")
    MC_GetTrapPrmSingle.argtypes = [c_short, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_short)]
    MC_GetTrapPrmSingle.restype = c_int
    break

# MultiCard.h: 556
for _lib in _libs.values():
    if not _lib.has("MC_PrfJog", "cdecl"):
        continue
    MC_PrfJog = _lib.get("MC_PrfJog", "cdecl")
    MC_PrfJog.argtypes = [c_short]
    MC_PrfJog.restype = c_int
    break

# MultiCard.h: 557
for _lib in _libs.values():
    if not _lib.has("MC_SetJogPrm", "cdecl"):
        continue
    MC_SetJogPrm = _lib.get("MC_SetJogPrm", "cdecl")
    MC_SetJogPrm.argtypes = [c_short, POINTER(TJogPrm)]
    MC_SetJogPrm.restype = c_int
    break

# MultiCard.h: 558
for _lib in _libs.values():
    if not _lib.has("MC_SetJogPrmSingle", "cdecl"):
        continue
    MC_SetJogPrmSingle = _lib.get("MC_SetJogPrmSingle", "cdecl")
    MC_SetJogPrmSingle.argtypes = [c_short, c_double, c_double, c_double]
    MC_SetJogPrmSingle.restype = c_int
    break

# MultiCard.h: 559
for _lib in _libs.values():
    if not _lib.has("MC_GetJogPrm", "cdecl"):
        continue
    MC_GetJogPrm = _lib.get("MC_GetJogPrm", "cdecl")
    MC_GetJogPrm.argtypes = [c_short, POINTER(TJogPrm)]
    MC_GetJogPrm.restype = c_int
    break

# MultiCard.h: 560
for _lib in _libs.values():
    if not _lib.has("MC_GetJogPrmSingle", "cdecl"):
        continue
    MC_GetJogPrmSingle = _lib.get("MC_GetJogPrmSingle", "cdecl")
    MC_GetJogPrmSingle.argtypes = [c_short, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    MC_GetJogPrmSingle.restype = c_int
    break

# MultiCard.h: 561
for _lib in _libs.values():
    if not _lib.has("MC_SetPos", "cdecl"):
        continue
    MC_SetPos = _lib.get("MC_SetPos", "cdecl")
    MC_SetPos.argtypes = [c_short, c_long]
    MC_SetPos.restype = c_int
    break

# MultiCard.h: 562
for _lib in _libs.values():
    if not _lib.has("MC_GetPos", "cdecl"):
        continue
    MC_GetPos = _lib.get("MC_GetPos", "cdecl")
    MC_GetPos.argtypes = [c_short, POINTER(c_long)]
    MC_GetPos.restype = c_int
    break

# MultiCard.h: 563
for _lib in _libs.values():
    if not _lib.has("MC_SetVel", "cdecl"):
        continue
    MC_SetVel = _lib.get("MC_SetVel", "cdecl")
    MC_SetVel.argtypes = [c_short, c_double]
    MC_SetVel.restype = c_int
    break

# MultiCard.h: 564
for _lib in _libs.values():
    if not _lib.has("MC_GetVel", "cdecl"):
        continue
    MC_GetVel = _lib.get("MC_GetVel", "cdecl")
    MC_GetVel.argtypes = [c_short, POINTER(c_double)]
    MC_GetVel.restype = c_int
    break

# MultiCard.h: 567
for _lib in _libs.values():
    if not _lib.has("MC_Update", "cdecl"):
        continue
    MC_Update = _lib.get("MC_Update", "cdecl")
    MC_Update.argtypes = [c_long]
    MC_Update.restype = c_int
    break

# MultiCard.h: 575
for _lib in _libs.values():
    if not _lib.has("MC_GearStart", "cdecl"):
        continue
    MC_GearStart = _lib.get("MC_GearStart", "cdecl")
    MC_GearStart.argtypes = [c_long]
    MC_GearStart.restype = c_int
    break

# MultiCard.h: 576
for _lib in _libs.values():
    if not _lib.has("MC_GearStop", "cdecl"):
        continue
    MC_GearStop = _lib.get("MC_GearStop", "cdecl")
    MC_GearStop.argtypes = [c_long, c_long]
    MC_GearStop.restype = c_int
    break

# MultiCard.h: 577
for _lib in _libs.values():
    if not _lib.has("MC_SetGearEvent", "cdecl"):
        continue
    MC_SetGearEvent = _lib.get("MC_SetGearEvent", "cdecl")
    MC_SetGearEvent.argtypes = [c_short, c_short, c_double, c_double]
    MC_SetGearEvent.restype = c_int
    break

# MultiCard.h: 578
for _lib in _libs.values():
    if not _lib.has("MC_GetGearEvent", "cdecl"):
        continue
    MC_GetGearEvent = _lib.get("MC_GetGearEvent", "cdecl")
    MC_GetGearEvent.argtypes = [c_short, POINTER(c_short), POINTER(c_double), POINTER(c_double)]
    MC_GetGearEvent.restype = c_int
    break

# MultiCard.h: 582
for _lib in _libs.values():
    if not _lib.has("MC_PtSpace", "cdecl"):
        continue
    MC_PtSpace = _lib.get("MC_PtSpace", "cdecl")
    MC_PtSpace.argtypes = [c_short, POINTER(c_long), c_short]
    MC_PtSpace.restype = c_int
    break

# MultiCard.h: 583
for _lib in _libs.values():
    if not _lib.has("MC_PtRemain", "cdecl"):
        continue
    MC_PtRemain = _lib.get("MC_PtRemain", "cdecl")
    MC_PtRemain.argtypes = [c_short, POINTER(c_long), c_short]
    MC_PtRemain.restype = c_int
    break

# MultiCard.h: 584
for _lib in _libs.values():
    if not _lib.has("MC_PtData", "cdecl"):
        continue
    MC_PtData = _lib.get("MC_PtData", "cdecl")
    MC_PtData.argtypes = [c_short, POINTER(c_short), c_long, c_double]
    MC_PtData.restype = c_int
    break

# MultiCard.h: 585
for _lib in _libs.values():
    if not _lib.has("MC_PtClear", "cdecl"):
        continue
    MC_PtClear = _lib.get("MC_PtClear", "cdecl")
    MC_PtClear.argtypes = [c_long]
    MC_PtClear.restype = c_int
    break

# MultiCard.h: 586
for _lib in _libs.values():
    if not _lib.has("MC_PtStart", "cdecl"):
        continue
    MC_PtStart = _lib.get("MC_PtStart", "cdecl")
    MC_PtStart.argtypes = [c_long]
    MC_PtStart.restype = c_int
    break

# MultiCard.h: 589
for _lib in _libs.values():
    if not _lib.has("MC_StartDebugLog", "cdecl"):
        continue
    MC_StartDebugLog = _lib.get("MC_StartDebugLog", "cdecl")
    MC_StartDebugLog.argtypes = []
    MC_StartDebugLog.restype = c_int
    break

# MultiCard.h: 590
for _lib in _libs.values():
    if not _lib.has("MC_StopDebugLog", "cdecl"):
        continue
    MC_StopDebugLog = _lib.get("MC_StopDebugLog", "cdecl")
    MC_StopDebugLog.argtypes = []
    MC_StopDebugLog.restype = c_int
    break

# MultiCard.h: 591
for _lib in _libs.values():
    if not _lib.has("MC_SetCrdPrm", "cdecl"):
        continue
    MC_SetCrdPrm = _lib.get("MC_SetCrdPrm", "cdecl")
    MC_SetCrdPrm.argtypes = [c_short, POINTER(TCrdPrm)]
    MC_SetCrdPrm.restype = c_int
    break

# MultiCard.h: 592
for _lib in _libs.values():
    if not _lib.has("MC_GetCrdPrm", "cdecl"):
        continue
    MC_GetCrdPrm = _lib.get("MC_GetCrdPrm", "cdecl")
    MC_GetCrdPrm.argtypes = [c_short, POINTER(TCrdPrm)]
    MC_GetCrdPrm.restype = c_int
    break

# MultiCard.h: 593
for _lib in _libs.values():
    if not _lib.has("MC_SetCrdPrmSingle", "cdecl"):
        continue
    MC_SetCrdPrmSingle = _lib.get("MC_SetCrdPrmSingle", "cdecl")
    MC_SetCrdPrmSingle.argtypes = [c_short, c_short, POINTER(c_short), c_double, c_double, c_short, c_short, POINTER(c_long)]
    MC_SetCrdPrmSingle.restype = c_int
    break

# MultiCard.h: 594
for _lib in _libs.values():
    if not _lib.has("MC_InitLookAhead", "cdecl"):
        continue
    MC_InitLookAhead = _lib.get("MC_InitLookAhead", "cdecl")
    MC_InitLookAhead.argtypes = [c_short, c_short, POINTER(TLookAheadPrm)]
    MC_InitLookAhead.restype = c_int
    break

# MultiCard.h: 595
for _lib in _libs.values():
    if not _lib.has("MC_InitLookAheadSingle", "cdecl"):
        continue
    MC_InitLookAheadSingle = _lib.get("MC_InitLookAheadSingle", "cdecl")
    MC_InitLookAheadSingle.argtypes = [c_short, c_short, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    MC_InitLookAheadSingle.restype = c_int
    break

# MultiCard.h: 596
for _lib in _libs.values():
    if not _lib.has("MC_CrdClear", "cdecl"):
        continue
    MC_CrdClear = _lib.get("MC_CrdClear", "cdecl")
    MC_CrdClear.argtypes = [c_short, c_short]
    MC_CrdClear.restype = c_int
    break

# MultiCard.h: 605
for _lib in _libs.values():
    if not _lib.has("MC_CrdStart", "cdecl"):
        continue
    MC_CrdStart = _lib.get("MC_CrdStart", "cdecl")
    MC_CrdStart.argtypes = [c_short, c_short]
    MC_CrdStart.restype = c_int
    break

# MultiCard.h: 606
for _lib in _libs.values():
    if not _lib.has("MC_SetOverride", "cdecl"):
        continue
    MC_SetOverride = _lib.get("MC_SetOverride", "cdecl")
    MC_SetOverride.argtypes = [c_short, c_double]
    MC_SetOverride.restype = c_int
    break

# MultiCard.h: 607
for _lib in _libs.values():
    if not _lib.has("MC_GetCrdPos", "cdecl"):
        continue
    MC_GetCrdPos = _lib.get("MC_GetCrdPos", "cdecl")
    MC_GetCrdPos.argtypes = [c_short, POINTER(c_double)]
    MC_GetCrdPos.restype = c_int
    break

# MultiCard.h: 608
for _lib in _libs.values():
    if not _lib.has("MC_GetCrdVel", "cdecl"):
        continue
    MC_GetCrdVel = _lib.get("MC_GetCrdVel", "cdecl")
    MC_GetCrdVel.argtypes = [c_short, POINTER(c_double)]
    MC_GetCrdVel.restype = c_int
    break

# MultiCard.h: 617
for _lib in _libs.values():
    if not _lib.has("MC_BufMove", "cdecl"):
        continue
    MC_BufMove = _lib.get("MC_BufMove", "cdecl")
    MC_BufMove.argtypes = [c_short, c_short, POINTER(c_long), c_short, c_short, c_long]
    MC_BufMove.restype = c_int
    break

# MultiCard.h: 618
for _lib in _libs.values():
    if not _lib.has("MC_BufGear", "cdecl"):
        continue
    MC_BufGear = _lib.get("MC_BufGear", "cdecl")
    MC_BufGear.argtypes = [c_short, c_short, POINTER(c_long), c_short, c_long]
    MC_BufGear.restype = c_int
    break

# MultiCard.h: 621
for _lib in _libs.values():
    if not _lib.has("MC_GetDi", "cdecl"):
        continue
    MC_GetDi = _lib.get("MC_GetDi", "cdecl")
    MC_GetDi.argtypes = [c_short, POINTER(c_long)]
    MC_GetDi.restype = c_int
    break

# MultiCard.h: 622
for _lib in _libs.values():
    if not _lib.has("MC_GetDiRaw", "cdecl"):
        continue
    MC_GetDiRaw = _lib.get("MC_GetDiRaw", "cdecl")
    MC_GetDiRaw.argtypes = [c_short, POINTER(c_long)]
    MC_GetDiRaw.restype = c_int
    break

# MultiCard.h: 625
for _lib in _libs.values():
    if not _lib.has("MC_SetDo", "cdecl"):
        continue
    MC_SetDo = _lib.get("MC_SetDo", "cdecl")
    MC_SetDo.argtypes = [c_short, c_long]
    MC_SetDo.restype = c_int
    break

# MultiCard.h: 626
for _lib in _libs.values():
    if not _lib.has("MC_SetDoBit", "cdecl"):
        continue
    MC_SetDoBit = _lib.get("MC_SetDoBit", "cdecl")
    MC_SetDoBit.argtypes = [c_short, c_short, c_short]
    MC_SetDoBit.restype = c_int
    break

# MultiCard.h: 627
for _lib in _libs.values():
    if not _lib.has("MC_SetDoBitReverse", "cdecl"):
        continue
    MC_SetDoBitReverse = _lib.get("MC_SetDoBitReverse", "cdecl")
    MC_SetDoBitReverse.argtypes = [c_short, c_short, c_long, c_short]
    MC_SetDoBitReverse.restype = c_int
    break

# MultiCard.h: 628
for _lib in _libs.values():
    if not _lib.has("MC_GetDo", "cdecl"):
        continue
    MC_GetDo = _lib.get("MC_GetDo", "cdecl")
    MC_GetDo.argtypes = [c_short, POINTER(c_long)]
    MC_GetDo.restype = c_int
    break

# MultiCard.h: 631
for _lib in _libs.values():
    if not _lib.has("MC_SetEncPos", "cdecl"):
        continue
    MC_SetEncPos = _lib.get("MC_SetEncPos", "cdecl")
    MC_SetEncPos.argtypes = [c_short, c_long]
    MC_SetEncPos.restype = c_int
    break

# MultiCard.h: 634
for _lib in _libs.values():
    if not _lib.has("MC_SetPwm", "cdecl"):
        continue
    MC_SetPwm = _lib.get("MC_SetPwm", "cdecl")
    MC_SetPwm.argtypes = [c_short, c_double, c_double]
    MC_SetPwm.restype = c_int
    break

# MultiCard.h: 635
for _lib in _libs.values():
    if not _lib.has("MC_GetPwm", "cdecl"):
        continue
    MC_GetPwm = _lib.get("MC_GetPwm", "cdecl")
    MC_GetPwm.argtypes = [c_short, POINTER(c_double), POINTER(c_double)]
    MC_GetPwm.restype = c_int
    break

# MultiCard.h: 639
for _lib in _libs.values():
    if not _lib.has("MC_SetExtDoBit", "cdecl"):
        continue
    MC_SetExtDoBit = _lib.get("MC_SetExtDoBit", "cdecl")
    MC_SetExtDoBit.argtypes = [c_short, c_short, c_ushort]
    MC_SetExtDoBit.restype = c_int
    break

# MultiCard.h: 640
for _lib in _libs.values():
    if not _lib.has("MC_GetExtDiBit", "cdecl"):
        continue
    MC_GetExtDiBit = _lib.get("MC_GetExtDiBit", "cdecl")
    MC_GetExtDiBit.argtypes = [c_short, c_short, POINTER(c_ushort)]
    MC_GetExtDiBit.restype = c_int
    break

# MultiCard.h: 641
for _lib in _libs.values():
    if not _lib.has("MC_GetExtDoBit", "cdecl"):
        continue
    MC_GetExtDoBit = _lib.get("MC_GetExtDoBit", "cdecl")
    MC_GetExtDoBit.argtypes = [c_short, c_short, POINTER(c_ushort)]
    MC_GetExtDoBit.restype = c_int
    break

# MultiCard.h: 642
for _lib in _libs.values():
    if not _lib.has("MC_SendEthToUartString", "cdecl"):
        continue
    MC_SendEthToUartString = _lib.get("MC_SendEthToUartString", "cdecl")
    MC_SendEthToUartString.argtypes = [c_short, POINTER(c_ubyte), c_short]
    MC_SendEthToUartString.restype = c_int
    break

# MultiCard.h: 643
for _lib in _libs.values():
    if not _lib.has("MC_ReadUartToEthString", "cdecl"):
        continue
    MC_ReadUartToEthString = _lib.get("MC_ReadUartToEthString", "cdecl")
    MC_ReadUartToEthString.argtypes = [c_short, POINTER(c_ubyte), POINTER(c_short)]
    MC_ReadUartToEthString.restype = c_int
    break

# MultiCard.h: 646
for _lib in _libs.values():
    if not _lib.has("MC_SetIOEventTrigger", "cdecl"):
        continue
    MC_SetIOEventTrigger = _lib.get("MC_SetIOEventTrigger", "cdecl")
    MC_SetIOEventTrigger.argtypes = [c_short, c_short, c_short, c_long, c_short, c_double, c_double]
    MC_SetIOEventTrigger.restype = c_int
    break

# MultiCard.h: 647
for _lib in _libs.values():
    if not _lib.has("MC_GetIOEventTrigger", "cdecl"):
        continue
    MC_GetIOEventTrigger = _lib.get("MC_GetIOEventTrigger", "cdecl")
    MC_GetIOEventTrigger.argtypes = [c_short, POINTER(c_short), c_short]
    MC_GetIOEventTrigger.restype = c_int
    break

# MultiCard.h: 650
for _lib in _libs.values():
    if not _lib.has("MC_CmpPluse", "cdecl"):
        continue
    MC_CmpPluse = _lib.get("MC_CmpPluse", "cdecl")
    MC_CmpPluse.argtypes = [c_short, c_short, c_short, c_short, c_short, c_short, c_short]
    MC_CmpPluse.restype = c_int
    break

# MultiCard.h: 651
for _lib in _libs.values():
    if not _lib.has("MC_CmpBufSetChannel", "cdecl"):
        continue
    MC_CmpBufSetChannel = _lib.get("MC_CmpBufSetChannel", "cdecl")
    MC_CmpBufSetChannel.argtypes = [c_short, c_short]
    MC_CmpBufSetChannel.restype = c_int
    break

# MultiCard.h: 653
for _lib in _libs.values():
    if not _lib.has("MC_CmpBufSts", "cdecl"):
        continue
    MC_CmpBufSts = _lib.get("MC_CmpBufSts", "cdecl")
    MC_CmpBufSts.argtypes = [POINTER(c_short), POINTER(c_ushort), POINTER(c_ushort)]
    MC_CmpBufSts.restype = c_int
    break

# MultiCard.h: 654
for _lib in _libs.values():
    if not _lib.has("MC_CmpBufStop", "cdecl"):
        continue
    MC_CmpBufStop = _lib.get("MC_CmpBufStop", "cdecl")
    MC_CmpBufStop.argtypes = [c_short]
    MC_CmpBufStop.restype = c_int
    break

# MultiCard.h: 658
for _lib in _libs.values():
    if not _lib.has("MC_SetCaptureMode", "cdecl"):
        continue
    MC_SetCaptureMode = _lib.get("MC_SetCaptureMode", "cdecl")
    MC_SetCaptureMode.argtypes = [c_short, c_short]
    MC_SetCaptureMode.restype = c_int
    break

# MultiCard.h: 661
for _lib in _libs.values():
    if not _lib.has("MC_SetCaptureSense", "cdecl"):
        continue
    MC_SetCaptureSense = _lib.get("MC_SetCaptureSense", "cdecl")
    MC_SetCaptureSense.argtypes = [c_short, c_short, c_short]
    MC_SetCaptureSense.restype = c_int
    break

# MultiCard.h: 662
for _lib in _libs.values():
    if not _lib.has("MC_GetCaptureSense", "cdecl"):
        continue
    MC_GetCaptureSense = _lib.get("MC_GetCaptureSense", "cdecl")
    MC_GetCaptureSense.argtypes = [c_short, c_short, POINTER(c_short)]
    MC_GetCaptureSense.restype = c_int
    break

# MultiCard.h: 663
for _lib in _libs.values():
    if not _lib.has("MC_ClearCaptureStatus", "cdecl"):
        continue
    MC_ClearCaptureStatus = _lib.get("MC_ClearCaptureStatus", "cdecl")
    MC_ClearCaptureStatus.argtypes = [c_short]
    MC_ClearCaptureStatus.restype = c_int
    break

# MultiCard.h: 664
for _lib in _libs.values():
    if not _lib.has("MC_SetContinueCaptureMode", "cdecl"):
        continue
    MC_SetContinueCaptureMode = _lib.get("MC_SetContinueCaptureMode", "cdecl")
    MC_SetContinueCaptureMode.argtypes = [c_short, c_short, c_short, c_short]
    MC_SetContinueCaptureMode.restype = c_int
    break

# MultiCard.h: 665
for _lib in _libs.values():
    if not _lib.has("MC_GetContinueCaptureData", "cdecl"):
        continue
    MC_GetContinueCaptureData = _lib.get("MC_GetContinueCaptureData", "cdecl")
    MC_GetContinueCaptureData.argtypes = [c_short, POINTER(c_long), POINTER(c_short)]
    MC_GetContinueCaptureData.restype = c_int
    break

# MultiCard.h: 668
for _lib in _libs.values():
    if not _lib.has("MC_SetSoftLimit", "cdecl"):
        continue
    MC_SetSoftLimit = _lib.get("MC_SetSoftLimit", "cdecl")
    MC_SetSoftLimit.argtypes = [c_short, c_long, c_long]
    MC_SetSoftLimit.restype = c_int
    break

# MultiCard.h: 669
for _lib in _libs.values():
    if not _lib.has("MC_GetSoftLimit", "cdecl"):
        continue
    MC_GetSoftLimit = _lib.get("MC_GetSoftLimit", "cdecl")
    MC_GetSoftLimit.argtypes = [c_short, POINTER(c_long), POINTER(c_long)]
    MC_GetSoftLimit.restype = c_int
    break

# MultiCard.h: 670
for _lib in _libs.values():
    if not _lib.has("MC_SetHardLimP", "cdecl"):
        continue
    MC_SetHardLimP = _lib.get("MC_SetHardLimP", "cdecl")
    MC_SetHardLimP.argtypes = [c_short, c_short, c_short, c_short]
    MC_SetHardLimP.restype = c_int
    break

# MultiCard.h: 671
for _lib in _libs.values():
    if not _lib.has("MC_SetHardLimN", "cdecl"):
        continue
    MC_SetHardLimN = _lib.get("MC_SetHardLimN", "cdecl")
    MC_SetHardLimN.argtypes = [c_short, c_short, c_short, c_short]
    MC_SetHardLimN.restype = c_int
    break

# MultiCard.h: 672
for _lib in _libs.values():
    if not _lib.has("MC_EStopSetIO", "cdecl"):
        continue
    MC_EStopSetIO = _lib.get("MC_EStopSetIO", "cdecl")
    MC_EStopSetIO.argtypes = [c_short, c_short, c_short, c_ulong]
    MC_EStopSetIO.restype = c_int
    break

# MultiCard.h: 673
for _lib in _libs.values():
    if not _lib.has("MC_EStopOnOff", "cdecl"):
        continue
    MC_EStopOnOff = _lib.get("MC_EStopOnOff", "cdecl")
    MC_EStopOnOff.argtypes = [c_short]
    MC_EStopOnOff.restype = c_int
    break

# MultiCard.h: 674
for _lib in _libs.values():
    if not _lib.has("MC_EStopGetSts", "cdecl"):
        continue
    MC_EStopGetSts = _lib.get("MC_EStopGetSts", "cdecl")
    MC_EStopGetSts.argtypes = [POINTER(c_short)]
    MC_EStopGetSts.restype = c_int
    break

# MultiCard.h: 675
for _lib in _libs.values():
    if not _lib.has("MC_EStopClrSts", "cdecl"):
        continue
    MC_EStopClrSts = _lib.get("MC_EStopClrSts", "cdecl")
    MC_EStopClrSts.argtypes = []
    MC_EStopClrSts.restype = c_int
    break

# MultiCard.h: 678
for _lib in _libs.values():
    if not _lib.has("MC_HomeStart", "cdecl"):
        continue
    MC_HomeStart = _lib.get("MC_HomeStart", "cdecl")
    MC_HomeStart.argtypes = [c_short]
    MC_HomeStart.restype = c_int
    break

# MultiCard.h: 679
for _lib in _libs.values():
    if not _lib.has("MC_HomeStop", "cdecl"):
        continue
    MC_HomeStop = _lib.get("MC_HomeStop", "cdecl")
    MC_HomeStop.argtypes = [c_short]
    MC_HomeStop.restype = c_int
    break

# MultiCard.h: 680
for _lib in _libs.values():
    if not _lib.has("MC_HomeSetPrm", "cdecl"):
        continue
    MC_HomeSetPrm = _lib.get("MC_HomeSetPrm", "cdecl")
    MC_HomeSetPrm.argtypes = [c_short, POINTER(TAxisHomePrm)]
    MC_HomeSetPrm.restype = c_int
    break

# MultiCard.h: 681
for _lib in _libs.values():
    if not _lib.has("MC_HomeSetPrmSingle", "cdecl"):
        continue
    MC_HomeSetPrmSingle = _lib.get("MC_HomeSetPrmSingle", "cdecl")
    MC_HomeSetPrmSingle.argtypes = [c_short, c_short, c_short, c_long, c_double, c_double, c_double, c_double]
    MC_HomeSetPrmSingle.restype = c_int
    break

# MultiCard.h: 682
for _lib in _libs.values():
    if not _lib.has("MC_HomeGetPrm", "cdecl"):
        continue
    MC_HomeGetPrm = _lib.get("MC_HomeGetPrm", "cdecl")
    MC_HomeGetPrm.argtypes = [c_short, POINTER(TAxisHomePrm)]
    MC_HomeGetPrm.restype = c_int
    break

# MultiCard.h: 683
for _lib in _libs.values():
    if not _lib.has("MC_HomeGetPrmSingle", "cdecl"):
        continue
    MC_HomeGetPrmSingle = _lib.get("MC_HomeGetPrmSingle", "cdecl")
    MC_HomeGetPrmSingle.argtypes = [c_short, POINTER(c_short), POINTER(c_short), POINTER(c_long), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    MC_HomeGetPrmSingle.restype = c_int
    break

# MultiCard.h: 684
for _lib in _libs.values():
    if not _lib.has("MC_HomeGetSts", "cdecl"):
        continue
    MC_HomeGetSts = _lib.get("MC_HomeGetSts", "cdecl")
    MC_HomeGetSts.argtypes = [c_short, POINTER(c_ushort)]
    MC_HomeGetSts.restype = c_int
    break

# MultiCard.h: 688
for _lib in _libs.values():
    if not _lib.has("MC_EndHandwheel", "cdecl"):
        continue
    MC_EndHandwheel = _lib.get("MC_EndHandwheel", "cdecl")
    MC_EndHandwheel.argtypes = [c_short]
    MC_EndHandwheel.restype = c_int
    break

# MultiCard.h: 691
for _lib in _libs.values():
    if not _lib.has("MC_GetIP", "cdecl"):
        continue
    MC_GetIP = _lib.get("MC_GetIP", "cdecl")
    MC_GetIP.argtypes = [POINTER(c_ulong)]
    MC_GetIP.restype = c_int
    break

# MultiCard.h: 692
for _lib in _libs.values():
    if not _lib.has("MC_SetIP", "cdecl"):
        continue
    MC_SetIP = _lib.get("MC_SetIP", "cdecl")
    MC_SetIP.argtypes = [c_ulong]
    MC_SetIP.restype = c_int
    break

# MultiCard.h: 693
for _lib in _libs.values():
    if not _lib.has("MC_GetID", "cdecl"):
        continue
    MC_GetID = _lib.get("MC_GetID", "cdecl")
    MC_GetID.argtypes = [POINTER(c_ulong)]
    MC_GetID.restype = c_int
    break

# MultiCard.h: 12
try:
    MAX_MACRO_CHAR_LENGTH = 128
except:
    pass

# MultiCard.h: 17
try:
    MC_COM_SUCCESS = 0
except:
    pass

# MultiCard.h: 18
try:
    MC_COM_ERR_EXEC_FAIL = 1
except:
    pass

# MultiCard.h: 19
try:
    MC_COM_ERR_LICENSE_WRONG = 2
except:
    pass

# MultiCard.h: 20
try:
    MC_COM_ERR_DATA_WORRY = 7
except:
    pass

# MultiCard.h: 21
try:
    MC_COM_ERR_SEND = (-1)
except:
    pass

# MultiCard.h: 22
try:
    MC_COM_ERR_CARD_OPEN_FAIL = (-6)
except:
    pass

# MultiCard.h: 23
try:
    MC_COM_ERR_TIME_OUT = (-7)
except:
    pass

# MultiCard.h: 24
try:
    MC_COM_ERR_COM_OPEN_FAIL = (-8)
except:
    pass

# MultiCard.h: 27
try:
    AXIS_STATUS_ESTOP = 1
except:
    pass

# MultiCard.h: 28
try:
    AXIS_STATUS_SV_ALARM = 2
except:
    pass

# MultiCard.h: 29
try:
    AXIS_STATUS_POS_SOFT_LIMIT = 4
except:
    pass

# MultiCard.h: 30
try:
    AXIS_STATUS_NEG_SOFT_LIMIT = 8
except:
    pass

# MultiCard.h: 31
try:
    AXIS_STATUS_FOLLOW_ERR = 16
except:
    pass

# MultiCard.h: 32
try:
    AXIS_STATUS_POS_HARD_LIMIT = 32
except:
    pass

# MultiCard.h: 33
try:
    AXIS_STATUS_NEG_HARD_LIMIT = 64
except:
    pass

# MultiCard.h: 34
try:
    AXIS_STATUS_IO_SMS_STOP = 128
except:
    pass

# MultiCard.h: 35
try:
    AXIS_STATUS_IO_EMG_STOP = 256
except:
    pass

# MultiCard.h: 36
try:
    AXIS_STATUS_ENABLE = 512
except:
    pass

# MultiCard.h: 37
try:
    AXIS_STATUS_RUNNING = 1024
except:
    pass

# MultiCard.h: 38
try:
    AXIS_STATUS_ARRIVE = 2048
except:
    pass

# MultiCard.h: 39
try:
    AXIS_STATUS_HOME_RUNNING = 4096
except:
    pass

# MultiCard.h: 40
try:
    AXIS_STATUS_HOME_SUCESS = 8192
except:
    pass

# MultiCard.h: 41
try:
    AXIS_STATUS_HOME_SWITCH = 16384
except:
    pass

# MultiCard.h: 42
try:
    AXIS_STATUS_INDEX = 32768
except:
    pass

# MultiCard.h: 43
try:
    AXIS_STATUS_GEAR_START = 65536
except:
    pass

# MultiCard.h: 44
try:
    AXIS_STATUS_GEAR_FINISH = 131072
except:
    pass

# MultiCard.h: 47
try:
    CRDSYS_STATUS_PROG_RUN = 1
except:
    pass

# MultiCard.h: 48
try:
    CRDSYS_STATUS_PROG_STOP = 2
except:
    pass

# MultiCard.h: 49
try:
    CRDSYS_STATUS_PROG_ESTOP = 4
except:
    pass

# MultiCard.h: 51
try:
    CRDSYS_STATUS_FIFO_FINISH_0 = 16
except:
    pass

# MultiCard.h: 52
try:
    CRDSYS_STATUS_FIFO_FINISH_1 = 32
except:
    pass

# MultiCard.h: 55
try:
    MC_LIMIT_POSITIVE = 0
except:
    pass

# MultiCard.h: 56
try:
    MC_LIMIT_NEGATIVE = 1
except:
    pass

# MultiCard.h: 57
try:
    MC_ALARM = 2
except:
    pass

# MultiCard.h: 58
try:
    MC_HOME = 3
except:
    pass

# MultiCard.h: 59
try:
    MC_GPI = 4
except:
    pass

# MultiCard.h: 60
try:
    MC_ARRIVE = 5
except:
    pass

# MultiCard.h: 61
try:
    MC_IP_SWITCH = 6
except:
    pass

# MultiCard.h: 62
try:
    MC_MPG = 7
except:
    pass

# MultiCard.h: 65
try:
    MC_ENABLE = 10
except:
    pass

# MultiCard.h: 66
try:
    MC_CLEAR = 11
except:
    pass

# MultiCard.h: 67
try:
    MC_GPO = 12
except:
    pass

# MultiCard.h: 71
try:
    CAPTURE_HOME = 1
except:
    pass

# MultiCard.h: 72
try:
    CAPTURE_INDEX = 2
except:
    pass

# MultiCard.h: 73
try:
    CAPTURE_PROBE1 = 3
except:
    pass

# MultiCard.h: 74
try:
    CAPTURE_PROBE2 = 4
except:
    pass

# MultiCard.h: 77
try:
    PT_MODE_STATIC = 0
except:
    pass

# MultiCard.h: 78
try:
    PT_MODE_DYNAMIC = 1
except:
    pass

# MultiCard.h: 80
try:
    PT_SEGMENT_NORMAL = 0
except:
    pass

# MultiCard.h: 81
try:
    PT_SEGMENT_EVEN = 1
except:
    pass

# MultiCard.h: 82
try:
    PT_SEGMENT_STOP = 2
except:
    pass

# MultiCard.h: 84
try:
    GEAR_MASTER_ENCODER = 1
except:
    pass

# MultiCard.h: 85
try:
    GEAR_MASTER_PROFILE = 2
except:
    pass

# MultiCard.h: 86
try:
    GEAR_MASTER_AXIS = 3
except:
    pass

# MultiCard.h: 90
try:
    GEAR_EVENT_IMMED = 1
except:
    pass

# MultiCard.h: 91
try:
    GEAR_EVENT_BIG_EQU = 2
except:
    pass

# MultiCard.h: 92
try:
    GEAR_EVENT_SMALL_EQU = 3
except:
    pass

# MultiCard.h: 93
try:
    GEAR_EVENT_IO_ON = 4
except:
    pass

# MultiCard.h: 94
try:
    GEAR_EVENT_IO_OFF = 5
except:
    pass

# MultiCard.h: 97
try:
    FROCAST_LEN = 200
except:
    pass

# MultiCard.h: 99
try:
    INTERPOLATION_AXIS_MAX = 6
except:
    pass

# MultiCard.h: 100
try:
    CRD_FIFO_MAX = 4096
except:
    pass

# MultiCard.h: 101
try:
    CRD_MAX = 2
except:
    pass

# MultiCard.h: 349
try:
    CRDSYS_MAX_COUNT = 2
except:
    pass

# MultiCard.h: 350
try:
    AXIS_MAX = 8
except:
    pass

TrapPrm = struct_TrapPrm# MultiCard.h: 111

JogPrm = struct_JogPrm# MultiCard.h: 119

_CrdDataState = struct__CrdDataState# MultiCard.h: 126

_CrdPrm = struct__CrdPrm# MultiCard.h: 138

_G00PARA = struct__G00PARA# MultiCard.h: 168

_G01PARA = struct__G01PARA# MultiCard.h: 180

_G02_3PARA = struct__G02_3PARA# MultiCard.h: 197

_G04PARA = struct__G04PARA# MultiCard.h: 211

_G05PARA = struct__G05PARA# MultiCard.h: 217

_BufferMoveGearPARA = struct__BufferMoveGearPARA# MultiCard.h: 222

_BufferMoveVelAccPARA = struct__BufferMoveVelAccPARA# MultiCard.h: 230

_SetIOPara = struct__SetIOPara# MultiCard.h: 237

_CMDPara = union__CMDPara# MultiCard.h: 245

_CrdData = struct__CrdData# MultiCard.h: 260

_LookAheadPrm = struct__LookAheadPrm# MultiCard.h: 274

_AxisHomeParm = struct__AxisHomeParm# MultiCard.h: 287

_AllSysStatusData = struct__AllSysStatusData# MultiCard.h: 308

_ComDataFrameHead = struct__ComDataFrameHead# MultiCard.h: 323

_LookAheadState = struct__LookAheadState# MultiCard.h: 340

_ComDataFrame = struct__ComDataFrame# MultiCard.h: 347

# No inserted files

# No prefix-stripping

