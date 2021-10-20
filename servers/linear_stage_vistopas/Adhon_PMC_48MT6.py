# -*- coding: utf-8 -*-

"""Adhon_PMC_48MT6.py:
Wrapper for Adhon_PMC_48MT6.h
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211020"


__docformat__ = "restructuredtext"

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

# No libraries

# No modules

enum_tagProgramWorkMod = c_int# Adhon_PMC_48MT6.h: 42

WORK_MODE_PROGRAM = 1# Adhon_PMC_48MT6.h: 42

WORK_MODE_COMMAND = 2# Adhon_PMC_48MT6.h: 42

WORK_MODE_DOWN = 3# Adhon_PMC_48MT6.h: 42

WORK_MODE_STEP = 4# Adhon_PMC_48MT6.h: 42

PROGRAM_WORK_MODE_E = enum_tagProgramWorkMod# Adhon_PMC_48MT6.h: 42

enum_tagAxisType = c_int# Adhon_PMC_48MT6.h: 53

AXIS_X = 1# Adhon_PMC_48MT6.h: 53

AXIS_Y = 2# Adhon_PMC_48MT6.h: 53

AXIS_Z = 4# Adhon_PMC_48MT6.h: 53

AXIS_U = 8# Adhon_PMC_48MT6.h: 53

AXIS_V = 16# Adhon_PMC_48MT6.h: 53

AXIS_W = 32# Adhon_PMC_48MT6.h: 53

AXIS_TYPE_E = enum_tagAxisType# Adhon_PMC_48MT6.h: 53

enum_tagControlForType = c_int# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_NONE = 0# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_SPEED_SYNC_X = 1# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_POS_SYNC_X = 2# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_CLOSED_CTRL_X = 3# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_SPEED_X = 4# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_POS_X = 5# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_SPEED_SYNC_Y = 6# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_POS_SYNC_Y = 7# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_CLOSED_CTRL_Y = 8# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_SPEED_Y = 9# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_POS_Y = 10# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_SPEED_SYNC_Z = 11# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_POS_SYNC_Z = 12# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_CLOSED_CTRL_Z = 13# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_SPEED_Z = 14# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_POS_Z = 15# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_SPEED_SYNC_A = 16# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_POS_SYNC_A = 17# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_CLOSED_CTRL_A = 18# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_SPEED_A = 19# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_POS_A = 20# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_SPEED_SYNC_B = 21# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_POS_SYNC_B = 22# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_CLOSED_CTRL_B = 23# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_SPEED_B = 24# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_POS_B = 25# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_SPEED_SYNC_C = 26# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_POS_SYNC_C = 27# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_CLOSED_CTRL_C = 28# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_SPEED_C = 29# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_READ_POS_C = 30# Adhon_PMC_48MT6.h: 89

CONTROL_FOR_TYPE_E = enum_tagControlForType# Adhon_PMC_48MT6.h: 89

# Adhon_PMC_48MT6.h: 420
for _lib in _libs.values():
    if not _lib.has("PMC_GlobalInit", "stdcall"):
        continue
    PMC_GlobalInit = _lib.get("PMC_GlobalInit", "stdcall")
    PMC_GlobalInit.argtypes = []
    PMC_GlobalInit.restype = c_int
    break

# Adhon_PMC_48MT6.h: 427
for _lib in _libs.values():
    if not _lib.has("PMC_GlobalRelease", "stdcall"):
        continue
    PMC_GlobalRelease = _lib.get("PMC_GlobalRelease", "stdcall")
    PMC_GlobalRelease.argtypes = []
    PMC_GlobalRelease.restype = c_int
    break

# Adhon_PMC_48MT6.h: 434
for _lib in _libs.values():
    if not _lib.has("PMC_OpenSericalPort", "stdcall"):
        continue
    PMC_OpenSericalPort = _lib.get("PMC_OpenSericalPort", "stdcall")
    PMC_OpenSericalPort.argtypes = [c_int]
    PMC_OpenSericalPort.restype = c_int
    break

# Adhon_PMC_48MT6.h: 441
for _lib in _libs.values():
    if not _lib.has("PMC_CloseSericalPort", "stdcall"):
        continue
    PMC_CloseSericalPort = _lib.get("PMC_CloseSericalPort", "stdcall")
    PMC_CloseSericalPort.argtypes = []
    PMC_CloseSericalPort.restype = None
    break

# Adhon_PMC_48MT6.h: 449
for _lib in _libs.values():
    if not _lib.has("PMC_SetUserProgram", "stdcall"):
        continue
    PMC_SetUserProgram = _lib.get("PMC_SetUserProgram", "stdcall")
    PMC_SetUserProgram.argtypes = [POINTER(c_ubyte), c_ushort]
    PMC_SetUserProgram.restype = c_int
    break

# Adhon_PMC_48MT6.h: 456
for _lib in _libs.values():
    if not _lib.has("PMC_DownLoadProgram", "stdcall"):
        continue
    PMC_DownLoadProgram = _lib.get("PMC_DownLoadProgram", "stdcall")
    PMC_DownLoadProgram.argtypes = [c_ubyte]
    PMC_DownLoadProgram.restype = c_int
    break

# Adhon_PMC_48MT6.h: 465
for _lib in _libs.values():
    if not _lib.has("PMC_GetControllerVersion", "stdcall"):
        continue
    PMC_GetControllerVersion = _lib.get("PMC_GetControllerVersion", "stdcall")
    PMC_GetControllerVersion.argtypes = [c_ubyte, POINTER(c_ulong)]
    PMC_GetControllerVersion.restype = c_int
    break

# Adhon_PMC_48MT6.h: 474
for _lib in _libs.values():
    if not _lib.has("PMC_SetWorkMode", "stdcall"):
        continue
    PMC_SetWorkMode = _lib.get("PMC_SetWorkMode", "stdcall")
    PMC_SetWorkMode.argtypes = [c_ubyte, PROGRAM_WORK_MODE_E, c_ubyte]
    PMC_SetWorkMode.restype = c_int
    break

# Adhon_PMC_48MT6.h: 482
for _lib in _libs.values():
    if not _lib.has("PMC_GetWorkMode", "stdcall"):
        continue
    PMC_GetWorkMode = _lib.get("PMC_GetWorkMode", "stdcall")
    PMC_GetWorkMode.argtypes = [c_ubyte, POINTER(PROGRAM_WORK_MODE_E)]
    PMC_GetWorkMode.restype = c_int
    break

# Adhon_PMC_48MT6.h: 490
for _lib in _libs.values():
    if not _lib.has("PMC_SetControllerAddr", "stdcall"):
        continue
    PMC_SetControllerAddr = _lib.get("PMC_SetControllerAddr", "stdcall")
    PMC_SetControllerAddr.argtypes = [c_ubyte, c_ubyte]
    PMC_SetControllerAddr.restype = c_int
    break

# Adhon_PMC_48MT6.h: 497
for _lib in _libs.values():
    if not _lib.has("PMC_GetControllerAddr", "stdcall"):
        continue
    PMC_GetControllerAddr = _lib.get("PMC_GetControllerAddr", "stdcall")
    PMC_GetControllerAddr.argtypes = [POINTER(c_ubyte)]
    PMC_GetControllerAddr.restype = c_int
    break

# Adhon_PMC_48MT6.h: 504
for _lib in _libs.values():
    if not _lib.has("PMC_PauseController", "stdcall"):
        continue
    PMC_PauseController = _lib.get("PMC_PauseController", "stdcall")
    PMC_PauseController.argtypes = [c_ubyte]
    PMC_PauseController.restype = c_int
    break

# Adhon_PMC_48MT6.h: 511
for _lib in _libs.values():
    if not _lib.has("PMC_ContinueController", "stdcall"):
        continue
    PMC_ContinueController = _lib.get("PMC_ContinueController", "stdcall")
    PMC_ContinueController.argtypes = [c_ubyte]
    PMC_ContinueController.restype = c_int
    break

# Adhon_PMC_48MT6.h: 519
for _lib in _libs.values():
    if not _lib.has("PMC_Beeper", "stdcall"):
        continue
    PMC_Beeper = _lib.get("PMC_Beeper", "stdcall")
    PMC_Beeper.argtypes = [c_ubyte, c_ulong]
    PMC_Beeper.restype = c_int
    break

# Adhon_PMC_48MT6.h: 546
for _lib in _libs.values():
    if not _lib.has("PMC_GetAllIOPinLevel", "stdcall"):
        continue
    PMC_GetAllIOPinLevel = _lib.get("PMC_GetAllIOPinLevel", "stdcall")
    PMC_GetAllIOPinLevel.argtypes = [c_ubyte, c_ushort, POINTER(c_ulong)]
    PMC_GetAllIOPinLevel.restype = c_int
    break

# Adhon_PMC_48MT6.h: 555
for _lib in _libs.values():
    if not _lib.has("PMC_SetMotorDriveDiv", "stdcall"):
        continue
    PMC_SetMotorDriveDiv = _lib.get("PMC_SetMotorDriveDiv", "stdcall")
    PMC_SetMotorDriveDiv.argtypes = [c_ubyte, AXIS_TYPE_E, c_ulong]
    PMC_SetMotorDriveDiv.restype = c_int
    break

# Adhon_PMC_48MT6.h: 564
for _lib in _libs.values():
    if not _lib.has("PMC_GetMotorDriveDiv", "stdcall"):
        continue
    PMC_GetMotorDriveDiv = _lib.get("PMC_GetMotorDriveDiv", "stdcall")
    PMC_GetMotorDriveDiv.argtypes = [c_ubyte, AXIS_TYPE_E, POINTER(c_ulong)]
    PMC_GetMotorDriveDiv.restype = c_int
    break

# Adhon_PMC_48MT6.h: 573
for _lib in _libs.values():
    if not _lib.has("PMC_SetMotorPitch", "stdcall"):
        continue
    PMC_SetMotorPitch = _lib.get("PMC_SetMotorPitch", "stdcall")
    PMC_SetMotorPitch.argtypes = [c_ubyte, AXIS_TYPE_E, c_float]
    PMC_SetMotorPitch.restype = c_int
    break

# Adhon_PMC_48MT6.h: 582
for _lib in _libs.values():
    if not _lib.has("PMC_GetMotorPitch", "stdcall"):
        continue
    PMC_GetMotorPitch = _lib.get("PMC_GetMotorPitch", "stdcall")
    PMC_GetMotorPitch.argtypes = [c_ubyte, AXIS_TYPE_E, POINTER(c_float)]
    PMC_GetMotorPitch.restype = c_int
    break

# Adhon_PMC_48MT6.h: 591
for _lib in _libs.values():
    if not _lib.has("PMC_SetMotorAcc", "stdcall"):
        continue
    PMC_SetMotorAcc = _lib.get("PMC_SetMotorAcc", "stdcall")
    PMC_SetMotorAcc.argtypes = [c_ubyte, AXIS_TYPE_E, c_ulong]
    PMC_SetMotorAcc.restype = c_int
    break

# Adhon_PMC_48MT6.h: 600
for _lib in _libs.values():
    if not _lib.has("PMC_GetMotorAcc", "stdcall"):
        continue
    PMC_GetMotorAcc = _lib.get("PMC_GetMotorAcc", "stdcall")
    PMC_GetMotorAcc.argtypes = [c_ubyte, AXIS_TYPE_E, POINTER(c_ulong)]
    PMC_GetMotorAcc.restype = c_int
    break

# Adhon_PMC_48MT6.h: 609
for _lib in _libs.values():
    if not _lib.has("PMC_SetMotorDec", "stdcall"):
        continue
    PMC_SetMotorDec = _lib.get("PMC_SetMotorDec", "stdcall")
    PMC_SetMotorDec.argtypes = [c_ubyte, AXIS_TYPE_E, c_ulong]
    PMC_SetMotorDec.restype = c_int
    break

# Adhon_PMC_48MT6.h: 618
for _lib in _libs.values():
    if not _lib.has("PMC_GetMotorDec", "stdcall"):
        continue
    PMC_GetMotorDec = _lib.get("PMC_GetMotorDec", "stdcall")
    PMC_GetMotorDec.argtypes = [c_ubyte, AXIS_TYPE_E, POINTER(c_ulong)]
    PMC_GetMotorDec.restype = c_int
    break

# Adhon_PMC_48MT6.h: 627
for _lib in _libs.values():
    if not _lib.has("PMC_SetMotorMaxSpeed", "stdcall"):
        continue
    PMC_SetMotorMaxSpeed = _lib.get("PMC_SetMotorMaxSpeed", "stdcall")
    PMC_SetMotorMaxSpeed.argtypes = [c_ubyte, AXIS_TYPE_E, c_float]
    PMC_SetMotorMaxSpeed.restype = c_int
    break

# Adhon_PMC_48MT6.h: 636
for _lib in _libs.values():
    if not _lib.has("PMC_SetMotorMinSpeed", "stdcall"):
        continue
    PMC_SetMotorMinSpeed = _lib.get("PMC_SetMotorMinSpeed", "stdcall")
    PMC_SetMotorMinSpeed.argtypes = [c_ubyte, AXIS_TYPE_E, c_float]
    PMC_SetMotorMinSpeed.restype = c_int
    break

# Adhon_PMC_48MT6.h: 645
for _lib in _libs.values():
    if not _lib.has("PMC_GetMotorCurSpeed", "stdcall"):
        continue
    PMC_GetMotorCurSpeed = _lib.get("PMC_GetMotorCurSpeed", "stdcall")
    PMC_GetMotorCurSpeed.argtypes = [c_ubyte, AXIS_TYPE_E, POINTER(c_float)]
    PMC_GetMotorCurSpeed.restype = c_int
    break

# Adhon_PMC_48MT6.h: 654
for _lib in _libs.values():
    if not _lib.has("PMC_MotorMove", "stdcall"):
        continue
    PMC_MotorMove = _lib.get("PMC_MotorMove", "stdcall")
    PMC_MotorMove.argtypes = [c_ubyte, AXIS_TYPE_E, c_float]
    PMC_MotorMove.restype = c_int
    break

# Adhon_PMC_48MT6.h: 662
for _lib in _libs.values():
    if not _lib.has("PMC_ManualLeftMove", "stdcall"):
        continue
    PMC_ManualLeftMove = _lib.get("PMC_ManualLeftMove", "stdcall")
    PMC_ManualLeftMove.argtypes = [c_ubyte, AXIS_TYPE_E]
    PMC_ManualLeftMove.restype = c_int
    break

# Adhon_PMC_48MT6.h: 670
for _lib in _libs.values():
    if not _lib.has("PMC_ManualRightMove", "stdcall"):
        continue
    PMC_ManualRightMove = _lib.get("PMC_ManualRightMove", "stdcall")
    PMC_ManualRightMove.argtypes = [c_ubyte, AXIS_TYPE_E]
    PMC_ManualRightMove.restype = c_int
    break

# Adhon_PMC_48MT6.h: 680
for _lib in _libs.values():
    if not _lib.has("PMC_MotorGoPos", "stdcall"):
        continue
    PMC_MotorGoPos = _lib.get("PMC_MotorGoPos", "stdcall")
    PMC_MotorGoPos.argtypes = [c_ubyte, AXIS_TYPE_E, c_float]
    PMC_MotorGoPos.restype = c_int
    break

# Adhon_PMC_48MT6.h: 690
for _lib in _libs.values():
    if not _lib.has("SetMotorLimitSignal", "stdcall"):
        continue
    SetMotorLimitSignal = _lib.get("SetMotorLimitSignal", "stdcall")
    SetMotorLimitSignal.argtypes = [c_ubyte, AXIS_TYPE_E, c_ubyte, c_ubyte]
    SetMotorLimitSignal.restype = c_int
    break

# Adhon_PMC_48MT6.h: 699
for _lib in _libs.values():
    if not _lib.has("PMC_QuickStopMotor", "stdcall"):
        continue
    PMC_QuickStopMotor = _lib.get("PMC_QuickStopMotor", "stdcall")
    PMC_QuickStopMotor.argtypes = [c_ubyte, AXIS_TYPE_E]
    PMC_QuickStopMotor.restype = c_int
    break

# Adhon_PMC_48MT6.h: 707
for _lib in _libs.values():
    if not _lib.has("PMC_SlowStopMotor", "stdcall"):
        continue
    PMC_SlowStopMotor = _lib.get("PMC_SlowStopMotor", "stdcall")
    PMC_SlowStopMotor.argtypes = [c_ubyte, AXIS_TYPE_E]
    PMC_SlowStopMotor.restype = c_int
    break

# Adhon_PMC_48MT6.h: 723
for _lib in _libs.values():
    if not _lib.has("PMC_ClearMotorPosition", "stdcall"):
        continue
    PMC_ClearMotorPosition = _lib.get("PMC_ClearMotorPosition", "stdcall")
    PMC_ClearMotorPosition.argtypes = [c_ubyte, AXIS_TYPE_E]
    PMC_ClearMotorPosition.restype = c_int
    break

# Adhon_PMC_48MT6.h: 732
for _lib in _libs.values():
    if not _lib.has("PMC_GetMotorPosition", "stdcall"):
        continue
    PMC_GetMotorPosition = _lib.get("PMC_GetMotorPosition", "stdcall")
    PMC_GetMotorPosition.argtypes = [c_ubyte, AXIS_TYPE_E, POINTER(c_float)]
    PMC_GetMotorPosition.restype = c_int
    break

# Adhon_PMC_48MT6.h: 741
for _lib in _libs.values():
    if not _lib.has("PMC_Line2Move", "stdcall"):
        continue
    PMC_Line2Move = _lib.get("PMC_Line2Move", "stdcall")
    PMC_Line2Move.argtypes = [c_ubyte, c_float, c_float]
    PMC_Line2Move.restype = c_int
    break

# Adhon_PMC_48MT6.h: 750
for _lib in _libs.values():
    if not _lib.has("PMC_Line2Goto", "stdcall"):
        continue
    PMC_Line2Goto = _lib.get("PMC_Line2Goto", "stdcall")
    PMC_Line2Goto.argtypes = [c_ubyte, c_float, c_float]
    PMC_Line2Goto.restype = c_int
    break

# Adhon_PMC_48MT6.h: 759
for _lib in _libs.values():
    if not _lib.has("PMC_Line2MoveDM", "stdcall"):
        continue
    PMC_Line2MoveDM = _lib.get("PMC_Line2MoveDM", "stdcall")
    PMC_Line2MoveDM.argtypes = [c_ubyte, c_ushort, c_ushort]
    PMC_Line2MoveDM.restype = c_int
    break

# Adhon_PMC_48MT6.h: 768
for _lib in _libs.values():
    if not _lib.has("PMC_Line2GotoDM", "stdcall"):
        continue
    PMC_Line2GotoDM = _lib.get("PMC_Line2GotoDM", "stdcall")
    PMC_Line2GotoDM.argtypes = [c_ubyte, c_ushort, c_ushort]
    PMC_Line2GotoDM.restype = c_int
    break

# Adhon_PMC_48MT6.h: 778
for _lib in _libs.values():
    if not _lib.has("PMC_Line3Move", "stdcall"):
        continue
    PMC_Line3Move = _lib.get("PMC_Line3Move", "stdcall")
    PMC_Line3Move.argtypes = [c_ubyte, c_float, c_float, c_float]
    PMC_Line3Move.restype = c_int
    break

# Adhon_PMC_48MT6.h: 788
for _lib in _libs.values():
    if not _lib.has("PMC_Line3Goto", "stdcall"):
        continue
    PMC_Line3Goto = _lib.get("PMC_Line3Goto", "stdcall")
    PMC_Line3Goto.argtypes = [c_ubyte, c_float, c_float, c_float]
    PMC_Line3Goto.restype = c_int
    break

# Adhon_PMC_48MT6.h: 798
for _lib in _libs.values():
    if not _lib.has("PMC_Line3MoveDM", "stdcall"):
        continue
    PMC_Line3MoveDM = _lib.get("PMC_Line3MoveDM", "stdcall")
    PMC_Line3MoveDM.argtypes = [c_ubyte, c_ushort, c_ushort, c_ushort]
    PMC_Line3MoveDM.restype = c_int
    break

# Adhon_PMC_48MT6.h: 807
for _lib in _libs.values():
    if not _lib.has("PMC_Line3GotoDM", "stdcall"):
        continue
    PMC_Line3GotoDM = _lib.get("PMC_Line3GotoDM", "stdcall")
    PMC_Line3GotoDM.argtypes = [c_ubyte, c_ushort, c_ushort, c_ushort]
    PMC_Line3GotoDM.restype = c_int
    break

# Adhon_PMC_48MT6.h: 817
for _lib in _libs.values():
    if not _lib.has("PMC_CircleMoveG2_Pos", "stdcall"):
        continue
    PMC_CircleMoveG2_Pos = _lib.get("PMC_CircleMoveG2_Pos", "stdcall")
    PMC_CircleMoveG2_Pos.argtypes = [c_ubyte, c_float, c_float, c_float]
    PMC_CircleMoveG2_Pos.restype = c_int
    break

# Adhon_PMC_48MT6.h: 827
for _lib in _libs.values():
    if not _lib.has("PMC_CircleMoveG3_Pos", "stdcall"):
        continue
    PMC_CircleMoveG3_Pos = _lib.get("PMC_CircleMoveG3_Pos", "stdcall")
    PMC_CircleMoveG3_Pos.argtypes = [c_ubyte, c_float, c_float, c_float]
    PMC_CircleMoveG3_Pos.restype = c_int
    break

# Adhon_PMC_48MT6.h: 838
for _lib in _libs.values():
    if not _lib.has("PMC_CircleMoveG2_Angle", "stdcall"):
        continue
    PMC_CircleMoveG2_Angle = _lib.get("PMC_CircleMoveG2_Angle", "stdcall")
    PMC_CircleMoveG2_Angle.argtypes = [c_ubyte, c_ushort, c_ushort, c_ushort]
    PMC_CircleMoveG2_Angle.restype = c_int
    break

# Adhon_PMC_48MT6.h: 848
for _lib in _libs.values():
    if not _lib.has("PMC_CircleMoveG3_Angle", "stdcall"):
        continue
    PMC_CircleMoveG3_Angle = _lib.get("PMC_CircleMoveG3_Angle", "stdcall")
    PMC_CircleMoveG3_Angle.argtypes = [c_ubyte, c_ushort, c_ushort, c_ushort]
    PMC_CircleMoveG3_Angle.restype = c_int
    break

# Adhon_PMC_48MT6.h: 902
for _lib in _libs.values():
    if not _lib.has("Modbus_OpenSerical", "stdcall"):
        continue
    Modbus_OpenSerical = _lib.get("Modbus_OpenSerical", "stdcall")
    Modbus_OpenSerical.argtypes = [c_ubyte, POINTER(c_ubyte)]
    Modbus_OpenSerical.restype = c_int
    break

# Adhon_PMC_48MT6.h: 908
for _lib in _libs.values():
    if not _lib.has("Modbus_CloseSerical", "stdcall"):
        continue
    Modbus_CloseSerical = _lib.get("Modbus_CloseSerical", "stdcall")
    Modbus_CloseSerical.argtypes = [c_ubyte]
    Modbus_CloseSerical.restype = c_int
    break

# Adhon_PMC_48MT6.h: 933
for _lib in _libs.values():
    if not _lib.has("Modbus_WriteFloat", "stdcall"):
        continue
    Modbus_WriteFloat = _lib.get("Modbus_WriteFloat", "stdcall")
    Modbus_WriteFloat.argtypes = [c_ubyte, c_ushort, c_float]
    Modbus_WriteFloat.restype = c_int
    break

# Adhon_PMC_48MT6.h: 941
for _lib in _libs.values():
    if not _lib.has("Modbus_ReadFloat", "stdcall"):
        continue
    Modbus_ReadFloat = _lib.get("Modbus_ReadFloat", "stdcall")
    Modbus_ReadFloat.argtypes = [c_ubyte, c_ushort]
    Modbus_ReadFloat.restype = c_float
    break

# Adhon_PMC_48MT6.h: 949
for _lib in _libs.values():
    if not _lib.has("Modbus_WriteLong", "stdcall"):
        continue
    Modbus_WriteLong = _lib.get("Modbus_WriteLong", "stdcall")
    Modbus_WriteLong.argtypes = [c_ubyte, c_ushort, c_ulong]
    Modbus_WriteLong.restype = c_int
    break

# Adhon_PMC_48MT6.h: 957
for _lib in _libs.values():
    if not _lib.has("Modbus_ReadLong", "stdcall"):
        continue
    Modbus_ReadLong = _lib.get("Modbus_ReadLong", "stdcall")
    Modbus_ReadLong.argtypes = [c_ubyte, c_ushort]
    Modbus_ReadLong.restype = c_ulong
    break

# Adhon_PMC_48MT6.h: 965
for _lib in _libs.values():
    if not _lib.has("Modbus_WriteShort", "stdcall"):
        continue
    Modbus_WriteShort = _lib.get("Modbus_WriteShort", "stdcall")
    Modbus_WriteShort.argtypes = [c_ubyte, c_ushort, c_ushort]
    Modbus_WriteShort.restype = c_int
    break

# Adhon_PMC_48MT6.h: 973
for _lib in _libs.values():
    if not _lib.has("Modbus_ReadShort", "stdcall"):
        continue
    Modbus_ReadShort = _lib.get("Modbus_ReadShort", "stdcall")
    Modbus_ReadShort.argtypes = [c_ubyte, c_ushort]
    Modbus_ReadShort.restype = c_ushort
    break

# Adhon_PMC_48MT6.h: 981
for _lib in _libs.values():
    if not _lib.has("PMC_CommandRawData", "stdcall"):
        continue
    PMC_CommandRawData = _lib.get("PMC_CommandRawData", "stdcall")
    PMC_CommandRawData.argtypes = [c_ubyte, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]
    PMC_CommandRawData.restype = c_int
    break

# Adhon_PMC_48MT6.h: 23
try:
    SUCCEED = 0
except:
    pass

# Adhon_PMC_48MT6.h: 24
try:
    FAILED = 1
except:
    pass

# Adhon_PMC_48MT6.h: 25
try:
    OPEN_SERICAL_FAIL = 2
except:
    pass

# Adhon_PMC_48MT6.h: 26
try:
    RECEIVE_FAILED = 3
except:
    pass

# Adhon_PMC_48MT6.h: 27
try:
    SEND_FAILED = 4
except:
    pass

# Adhon_PMC_48MT6.h: 28
try:
    INVALID_PAR = 5
except:
    pass

# Adhon_PMC_48MT6.h: 29
try:
    ERR_CANNOT_EXCUTE_COMMAND = 6
except:
    pass

# Adhon_PMC_48MT6.h: 32
try:
    ERR_DOWNLOAD_ONE_FAILED = 2
except:
    pass

# Adhon_PMC_48MT6.h: 107
try:
    MODBUS_MAX_LEN = 256
except:
    pass

# Adhon_PMC_48MT6.h: 108
try:
    MODBUS_MIN_LEN = 8
except:
    pass

# Adhon_PMC_48MT6.h: 109
try:
    MODBUS_TIME_OVER = 4
except:
    pass

# Adhon_PMC_48MT6.h: 110
try:
    MAX_USER_POINT = 200
except:
    pass

# Adhon_PMC_48MT6.h: 111
try:
    MOTOR_HISTORY_POS_X = 6000
except:
    pass

# Adhon_PMC_48MT6.h: 112
try:
    MOTOR_HISTORY_POS_Y = 6100
except:
    pass

# Adhon_PMC_48MT6.h: 113
try:
    MOTOR_HISTORY_POS_Z = 6200
except:
    pass

# Adhon_PMC_48MT6.h: 128
try:
    MODBUS_MAX_LEN = 256
except:
    pass

# Adhon_PMC_48MT6.h: 129
try:
    MODBUS_MIN_LEN = 8
except:
    pass

# Adhon_PMC_48MT6.h: 130
try:
    MODBUS_TIME_OVER = 4
except:
    pass

# Adhon_PMC_48MT6.h: 131
try:
    MAX_USER_POINT = 200
except:
    pass

# Adhon_PMC_48MT6.h: 136
try:
    MOTOR_HIGH_FRE_IN1 = 6300
except:
    pass

# Adhon_PMC_48MT6.h: 137
try:
    MOTOR_HIGH_FRE_IN2 = 6302
except:
    pass

# Adhon_PMC_48MT6.h: 138
try:
    MOTOR_HIGH_FRE_IN3 = 6304
except:
    pass

# Adhon_PMC_48MT6.h: 139
try:
    MOTOR_HIGH_FRE_IN4 = 6306
except:
    pass

# Adhon_PMC_48MT6.h: 140
try:
    MOTOR_HIGH_FRE_IN5 = 6308
except:
    pass

# Adhon_PMC_48MT6.h: 141
try:
    MOTOR_HIGH_FRE_IN6 = 6310
except:
    pass

# Adhon_PMC_48MT6.h: 142
try:
    MOTOR_PLUS_CNT_IN1 = 6312
except:
    pass

# Adhon_PMC_48MT6.h: 143
try:
    MOTOR_PLUS_CNT_IN2 = 6314
except:
    pass

# Adhon_PMC_48MT6.h: 144
try:
    MOTOR_PLUS_CNT_IN3 = 6316
except:
    pass

# Adhon_PMC_48MT6.h: 145
try:
    MOTOR_PLUS_CNT_IN4 = 6318
except:
    pass

# Adhon_PMC_48MT6.h: 146
try:
    MOTOR_PLUS_CNT_IN5 = 6320
except:
    pass

# Adhon_PMC_48MT6.h: 147
try:
    MOTOR_PLUS_CNT_IN6 = 6322
except:
    pass

# Adhon_PMC_48MT6.h: 152
try:
    DM_REMAIN_TIMER_0 = 6400
except:
    pass

# Adhon_PMC_48MT6.h: 153
try:
    DM_REMAIN_TIMER_1 = 6402
except:
    pass

# Adhon_PMC_48MT6.h: 154
try:
    DM_REMAIN_TIMER_2 = 6404
except:
    pass

# Adhon_PMC_48MT6.h: 155
try:
    DM_REMAIN_TIMER_3 = 6406
except:
    pass

# Adhon_PMC_48MT6.h: 156
try:
    DM_REMAIN_TIMER_4 = 6408
except:
    pass

# Adhon_PMC_48MT6.h: 157
try:
    DM_REMAIN_TIMER_5 = 6410
except:
    pass

# Adhon_PMC_48MT6.h: 158
try:
    DM_REMAIN_TIMER_6 = 6412
except:
    pass

# Adhon_PMC_48MT6.h: 159
try:
    DM_REMAIN_TIMER_7 = 6414
except:
    pass

# Adhon_PMC_48MT6.h: 164
try:
    DM_ENCODER_READ_SPEED_X = 6450
except:
    pass

# Adhon_PMC_48MT6.h: 165
try:
    DM_ENCODER_READ_SPEED_Y = 6452
except:
    pass

# Adhon_PMC_48MT6.h: 166
try:
    DM_ENCODER_READ_SPEED_Z = 6454
except:
    pass

# Adhon_PMC_48MT6.h: 167
try:
    DM_ENCODER_READ_SPEED_A = 6456
except:
    pass

# Adhon_PMC_48MT6.h: 168
try:
    DM_ENCODER_READ_SPEED_B = 6458
except:
    pass

# Adhon_PMC_48MT6.h: 169
try:
    DM_ENCODER_READ_SPEED_C = 6460
except:
    pass

# Adhon_PMC_48MT6.h: 170
try:
    DM_ENCODER_READ_POSITION_X = 6462
except:
    pass

# Adhon_PMC_48MT6.h: 171
try:
    DM_ENCODER_READ_POSITION_Y = 6464
except:
    pass

# Adhon_PMC_48MT6.h: 172
try:
    DM_ENCODER_READ_POSITION_Z = 6466
except:
    pass

# Adhon_PMC_48MT6.h: 173
try:
    DM_ENCODER_READ_POSITION_A = 6468
except:
    pass

# Adhon_PMC_48MT6.h: 174
try:
    DM_ENCODER_READ_POSITION_B = 6470
except:
    pass

# Adhon_PMC_48MT6.h: 175
try:
    DM_ENCODER_READ_POSITION_C = 6472
except:
    pass

# Adhon_PMC_48MT6.h: 180
try:
    DM_AD_VALUE_1 = 6500
except:
    pass

# Adhon_PMC_48MT6.h: 181
try:
    DM_AD_VALUE_2 = 6502
except:
    pass

# Adhon_PMC_48MT6.h: 184
try:
    COIL_COMMON_IO_IN = 0
except:
    pass

# Adhon_PMC_48MT6.h: 185
try:
    COIL_IN1_ADDR = (COIL_COMMON_IO_IN + 1)
except:
    pass

# Adhon_PMC_48MT6.h: 186
try:
    COIL_IN2_ADDR = (COIL_COMMON_IO_IN + 2)
except:
    pass

# Adhon_PMC_48MT6.h: 187
try:
    COIL_IN3_ADDR = (COIL_COMMON_IO_IN + 3)
except:
    pass

# Adhon_PMC_48MT6.h: 188
try:
    COIL_IN4_ADDR = (COIL_COMMON_IO_IN + 4)
except:
    pass

# Adhon_PMC_48MT6.h: 189
try:
    COIL_IN5_ADDR = (COIL_COMMON_IO_IN + 5)
except:
    pass

# Adhon_PMC_48MT6.h: 190
try:
    COIL_IN6_ADDR = (COIL_COMMON_IO_IN + 6)
except:
    pass

# Adhon_PMC_48MT6.h: 191
try:
    COIL_IN7_ADDR = (COIL_COMMON_IO_IN + 7)
except:
    pass

# Adhon_PMC_48MT6.h: 192
try:
    COIL_IN8_ADDR = (COIL_COMMON_IO_IN + 8)
except:
    pass

# Adhon_PMC_48MT6.h: 193
try:
    COIL_IN9_ADDR = (COIL_COMMON_IO_IN + 9)
except:
    pass

# Adhon_PMC_48MT6.h: 194
try:
    COIL_IN10_ADDR = (COIL_COMMON_IO_IN + 10)
except:
    pass

# Adhon_PMC_48MT6.h: 195
try:
    COIL_IN11_ADDR = (COIL_COMMON_IO_IN + 11)
except:
    pass

# Adhon_PMC_48MT6.h: 196
try:
    COIL_IN12_ADDR = (COIL_COMMON_IO_IN + 12)
except:
    pass

# Adhon_PMC_48MT6.h: 197
try:
    COIL_IN13_ADDR = (COIL_COMMON_IO_IN + 13)
except:
    pass

# Adhon_PMC_48MT6.h: 198
try:
    COIL_IN14_ADDR = (COIL_COMMON_IO_IN + 14)
except:
    pass

# Adhon_PMC_48MT6.h: 199
try:
    COIL_IN15_ADDR = (COIL_COMMON_IO_IN + 15)
except:
    pass

# Adhon_PMC_48MT6.h: 200
try:
    COIL_IN16_ADDR = (COIL_COMMON_IO_IN + 16)
except:
    pass

# Adhon_PMC_48MT6.h: 201
try:
    COIL_IN17_ADDR = (COIL_COMMON_IO_IN + 17)
except:
    pass

# Adhon_PMC_48MT6.h: 202
try:
    COIL_IN18_ADDR = (COIL_COMMON_IO_IN + 18)
except:
    pass

# Adhon_PMC_48MT6.h: 203
try:
    COIL_IN19_ADDR = (COIL_COMMON_IO_IN + 19)
except:
    pass

# Adhon_PMC_48MT6.h: 204
try:
    COIL_IN20_ADDR = (COIL_COMMON_IO_IN + 20)
except:
    pass

# Adhon_PMC_48MT6.h: 205
try:
    COIL_IN21_ADDR = (COIL_COMMON_IO_IN + 21)
except:
    pass

# Adhon_PMC_48MT6.h: 206
try:
    COIL_IN22_ADDR = (COIL_COMMON_IO_IN + 22)
except:
    pass

# Adhon_PMC_48MT6.h: 207
try:
    COIL_IN23_ADDR = (COIL_COMMON_IO_IN + 23)
except:
    pass

# Adhon_PMC_48MT6.h: 208
try:
    COIL_IN24_ADDR = (COIL_COMMON_IO_IN + 24)
except:
    pass

# Adhon_PMC_48MT6.h: 209
try:
    COIL_IN25_ADDR = (COIL_COMMON_IO_IN + 25)
except:
    pass

# Adhon_PMC_48MT6.h: 210
try:
    COIL_IN26_ADDR = (COIL_COMMON_IO_IN + 26)
except:
    pass

# Adhon_PMC_48MT6.h: 211
try:
    COIL_IN27_ADDR = (COIL_COMMON_IO_IN + 27)
except:
    pass

# Adhon_PMC_48MT6.h: 212
try:
    COIL_IN28_ADDR = (COIL_COMMON_IO_IN + 28)
except:
    pass

# Adhon_PMC_48MT6.h: 213
try:
    COIL_IN29_ADDR = (COIL_COMMON_IO_IN + 29)
except:
    pass

# Adhon_PMC_48MT6.h: 214
try:
    COIL_IN30_ADDR = (COIL_COMMON_IO_IN + 30)
except:
    pass

# Adhon_PMC_48MT6.h: 215
try:
    COIL_IN31_ADDR = (COIL_COMMON_IO_IN + 31)
except:
    pass

# Adhon_PMC_48MT6.h: 216
try:
    COIL_IN32_ADDR = (COIL_COMMON_IO_IN + 32)
except:
    pass

# Adhon_PMC_48MT6.h: 218
try:
    COIL_COMMON_IO_OUT = 32
except:
    pass

# Adhon_PMC_48MT6.h: 219
try:
    COIL_OUT1_ADDR = (COIL_COMMON_IO_OUT + 1)
except:
    pass

# Adhon_PMC_48MT6.h: 220
try:
    COIL_OUT2_ADDR = (COIL_COMMON_IO_OUT + 2)
except:
    pass

# Adhon_PMC_48MT6.h: 221
try:
    COIL_OUT3_ADDR = (COIL_COMMON_IO_OUT + 3)
except:
    pass

# Adhon_PMC_48MT6.h: 222
try:
    COIL_OUT4_ADDR = (COIL_COMMON_IO_OUT + 4)
except:
    pass

# Adhon_PMC_48MT6.h: 223
try:
    COIL_OUT5_ADDR = (COIL_COMMON_IO_OUT + 5)
except:
    pass

# Adhon_PMC_48MT6.h: 224
try:
    COIL_OUT6_ADDR = (COIL_COMMON_IO_OUT + 6)
except:
    pass

# Adhon_PMC_48MT6.h: 225
try:
    COIL_OUT7_ADDR = (COIL_COMMON_IO_OUT + 7)
except:
    pass

# Adhon_PMC_48MT6.h: 226
try:
    COIL_OUT8_ADDR = (COIL_COMMON_IO_OUT + 8)
except:
    pass

# Adhon_PMC_48MT6.h: 227
try:
    COIL_OUT9_ADDR = (COIL_COMMON_IO_OUT + 9)
except:
    pass

# Adhon_PMC_48MT6.h: 228
try:
    COIL_OUT10_ADDR = (COIL_COMMON_IO_OUT + 10)
except:
    pass

# Adhon_PMC_48MT6.h: 229
try:
    COIL_OUT11_ADDR = (COIL_COMMON_IO_OUT + 11)
except:
    pass

# Adhon_PMC_48MT6.h: 230
try:
    COIL_OUT12_ADDR = (COIL_COMMON_IO_OUT + 12)
except:
    pass

# Adhon_PMC_48MT6.h: 231
try:
    COIL_OUT13_ADDR = (COIL_COMMON_IO_OUT + 13)
except:
    pass

# Adhon_PMC_48MT6.h: 232
try:
    COIL_OUT14_ADDR = (COIL_COMMON_IO_OUT + 14)
except:
    pass

# Adhon_PMC_48MT6.h: 233
try:
    COIL_OUT15_ADDR = (COIL_COMMON_IO_OUT + 15)
except:
    pass

# Adhon_PMC_48MT6.h: 234
try:
    COIL_OUT16_ADDR = (COIL_COMMON_IO_OUT + 16)
except:
    pass

# Adhon_PMC_48MT6.h: 235
try:
    COIL_OUT17_ADDR = (COIL_COMMON_IO_OUT + 17)
except:
    pass

# Adhon_PMC_48MT6.h: 236
try:
    COIL_OUT18_ADDR = (COIL_COMMON_IO_OUT + 18)
except:
    pass

# Adhon_PMC_48MT6.h: 237
try:
    COIL_OUT19_ADDR = (COIL_COMMON_IO_OUT + 19)
except:
    pass

# Adhon_PMC_48MT6.h: 238
try:
    COIL_OUT20_ADDR = (COIL_COMMON_IO_OUT + 20)
except:
    pass

# Adhon_PMC_48MT6.h: 239
try:
    COIL_OUT21_ADDR = (COIL_COMMON_IO_OUT + 21)
except:
    pass

# Adhon_PMC_48MT6.h: 240
try:
    COIL_OUT22_ADDR = (COIL_COMMON_IO_OUT + 22)
except:
    pass

# Adhon_PMC_48MT6.h: 241
try:
    COIL_OUT23_ADDR = (COIL_COMMON_IO_OUT + 23)
except:
    pass

# Adhon_PMC_48MT6.h: 242
try:
    COIL_OUT24_ADDR = (COIL_COMMON_IO_OUT + 24)
except:
    pass

# Adhon_PMC_48MT6.h: 244
try:
    COIL_MOTOR_COIL = 60
except:
    pass

# Adhon_PMC_48MT6.h: 246
try:
    COIL_MOTOR_X_DIR = (COIL_MOTOR_COIL + 1)
except:
    pass

# Adhon_PMC_48MT6.h: 247
try:
    COIL_MOTOR_Y_DIR = (COIL_MOTOR_COIL + 2)
except:
    pass

# Adhon_PMC_48MT6.h: 248
try:
    COIL_MOTOR_Z_DIR = (COIL_MOTOR_COIL + 3)
except:
    pass

# Adhon_PMC_48MT6.h: 249
try:
    COIL_MOTOR_A_DIR = (COIL_MOTOR_COIL + 4)
except:
    pass

# Adhon_PMC_48MT6.h: 250
try:
    COIL_MOTOR_B_DIR = (COIL_MOTOR_COIL + 5)
except:
    pass

# Adhon_PMC_48MT6.h: 251
try:
    COIL_MOTOR_C_DIR = (COIL_MOTOR_COIL + 6)
except:
    pass

# Adhon_PMC_48MT6.h: 252
try:
    COIL_MOTOR_X_S = (COIL_MOTOR_COIL + 7)
except:
    pass

# Adhon_PMC_48MT6.h: 253
try:
    COIL_MOTOR_Y_S = (COIL_MOTOR_COIL + 8)
except:
    pass

# Adhon_PMC_48MT6.h: 254
try:
    COIL_MOTOR_Z_S = (COIL_MOTOR_COIL + 9)
except:
    pass

# Adhon_PMC_48MT6.h: 255
try:
    COIL_MOTOR_A_S = (COIL_MOTOR_COIL + 10)
except:
    pass

# Adhon_PMC_48MT6.h: 256
try:
    COIL_MOTOR_B_S = (COIL_MOTOR_COIL + 11)
except:
    pass

# Adhon_PMC_48MT6.h: 257
try:
    COIL_MOTOR_C_S = (COIL_MOTOR_COIL + 12)
except:
    pass

# Adhon_PMC_48MT6.h: 258
try:
    COIL_MOTOR_LEFT_X = (COIL_MOTOR_COIL + 13)
except:
    pass

# Adhon_PMC_48MT6.h: 259
try:
    COIL_MOTOR_RIGHT_X = (COIL_MOTOR_COIL + 14)
except:
    pass

# Adhon_PMC_48MT6.h: 260
try:
    COIL_MOTOR_LEFT_Y = (COIL_MOTOR_COIL + 15)
except:
    pass

# Adhon_PMC_48MT6.h: 261
try:
    COIL_MOTOR_RIGHT_Y = (COIL_MOTOR_COIL + 16)
except:
    pass

# Adhon_PMC_48MT6.h: 262
try:
    COIL_MOTOR_LEFT_Z = (COIL_MOTOR_COIL + 17)
except:
    pass

# Adhon_PMC_48MT6.h: 263
try:
    COIL_MOTOR_RIGHT_Z = (COIL_MOTOR_COIL + 18)
except:
    pass

# Adhon_PMC_48MT6.h: 264
try:
    COIL_MOTOR_LEFT_A = (COIL_MOTOR_COIL + 19)
except:
    pass

# Adhon_PMC_48MT6.h: 265
try:
    COIL_MOTOR_RIGHT_A = (COIL_MOTOR_COIL + 20)
except:
    pass

# Adhon_PMC_48MT6.h: 266
try:
    COIL_MOTOR_LEFT_B = (COIL_MOTOR_COIL + 21)
except:
    pass

# Adhon_PMC_48MT6.h: 267
try:
    COIL_MOTOR_RIGHT_B = (COIL_MOTOR_COIL + 22)
except:
    pass

# Adhon_PMC_48MT6.h: 268
try:
    COIL_MOTOR_LEFT_C = (COIL_MOTOR_COIL + 23)
except:
    pass

# Adhon_PMC_48MT6.h: 269
try:
    COIL_MOTOR_RIGHT_C = (COIL_MOTOR_COIL + 24)
except:
    pass

# Adhon_PMC_48MT6.h: 270
try:
    COIL_MOTOR_CLEAR_X = (COIL_MOTOR_COIL + 25)
except:
    pass

# Adhon_PMC_48MT6.h: 271
try:
    COIL_MOTOR_CLEAR_Y = (COIL_MOTOR_COIL + 26)
except:
    pass

# Adhon_PMC_48MT6.h: 272
try:
    COIL_MOTOR_CLEAR_Z = (COIL_MOTOR_COIL + 27)
except:
    pass

# Adhon_PMC_48MT6.h: 273
try:
    COIL_MOTOR_CLEAR_A = (COIL_MOTOR_COIL + 28)
except:
    pass

# Adhon_PMC_48MT6.h: 274
try:
    COIL_MOTOR_CLEAR_B = (COIL_MOTOR_COIL + 29)
except:
    pass

# Adhon_PMC_48MT6.h: 275
try:
    COIL_MOTOR_CLEAR_C = (COIL_MOTOR_COIL + 30)
except:
    pass

# Adhon_PMC_48MT6.h: 277
try:
    COIL_PERICAL_STATUS = 100
except:
    pass

# Adhon_PMC_48MT6.h: 278
try:
    COIL_PWM_1_STATUS = (COIL_PERICAL_STATUS + 1)
except:
    pass

# Adhon_PMC_48MT6.h: 279
try:
    COIL_PWM_2_STATUS = (COIL_PERICAL_STATUS + 2)
except:
    pass

# Adhon_PMC_48MT6.h: 280
try:
    COIL_LIMIT_TRIGER_LEVEL = (COIL_PERICAL_STATUS + 10)
except:
    pass

# Adhon_PMC_48MT6.h: 282
try:
    SYSTEM_OTHER_COIL = 150
except:
    pass

# Adhon_PMC_48MT6.h: 284
try:
    COIL_SYS_PAUSE = (SYSTEM_OTHER_COIL + 1)
except:
    pass

# Adhon_PMC_48MT6.h: 285
try:
    COIL_SYS_CONTINUE = (SYSTEM_OTHER_COIL + 2)
except:
    pass

# Adhon_PMC_48MT6.h: 286
try:
    COIL_SYS_RESET = (SYSTEM_OTHER_COIL + 3)
except:
    pass

# Adhon_PMC_48MT6.h: 287
try:
    COIL_SET_STEP_MODE = (SYSTEM_OTHER_COIL + 4)
except:
    pass

# Adhon_PMC_48MT6.h: 288
try:
    COIL_RUN_STEP_CODE = (SYSTEM_OTHER_COIL + 5)
except:
    pass

# Adhon_PMC_48MT6.h: 289
try:
    COIL_EARSE_DM_DATA = (SYSTEM_OTHER_COIL + 6)
except:
    pass

# Adhon_PMC_48MT6.h: 292
try:
    COIL_VIDEO_TEACH_BEGIN = (SYSTEM_OTHER_COIL + 7)
except:
    pass

# Adhon_PMC_48MT6.h: 293
try:
    COIL_VIDEO_TEACH_END = (SYSTEM_OTHER_COIL + 8)
except:
    pass

# Adhon_PMC_48MT6.h: 294
try:
    COIL_VIDEO_SAVE_POINT = (SYSTEM_OTHER_COIL + 9)
except:
    pass

# Adhon_PMC_48MT6.h: 297
try:
    COIL_SIMULATE_INPUT_1 = (SYSTEM_OTHER_COIL + 10)
except:
    pass

# Adhon_PMC_48MT6.h: 298
try:
    COIL_SIMULATE_INPUT_32 = (SYSTEM_OTHER_COIL + 41)
except:
    pass

# Adhon_PMC_48MT6.h: 300
try:
    COIL_CUSTOM_DEFINE = 200
except:
    pass

# Adhon_PMC_48MT6.h: 303
try:
    DM_MOTOR_ACC_X = 1
except:
    pass

# Adhon_PMC_48MT6.h: 304
try:
    DM_MOTOR_ACC_Y = 2
except:
    pass

# Adhon_PMC_48MT6.h: 305
try:
    DM_MOTOR_ACC_Z = 3
except:
    pass

# Adhon_PMC_48MT6.h: 306
try:
    DM_MOTOR_ACC_A = 4
except:
    pass

# Adhon_PMC_48MT6.h: 307
try:
    DM_MOTOR_ACC_B = 5
except:
    pass

# Adhon_PMC_48MT6.h: 308
try:
    DM_MOTOR_ACC_C = 6
except:
    pass

# Adhon_PMC_48MT6.h: 309
try:
    DM_MOTOR_DEC_X = 7
except:
    pass

# Adhon_PMC_48MT6.h: 310
try:
    DM_MOTOR_DEC_Y = 8
except:
    pass

# Adhon_PMC_48MT6.h: 311
try:
    DM_MOTOR_DEC_Z = 9
except:
    pass

# Adhon_PMC_48MT6.h: 312
try:
    DM_MOTOR_DEC_A = 10
except:
    pass

# Adhon_PMC_48MT6.h: 313
try:
    DM_MOTOR_DEC_B = 11
except:
    pass

# Adhon_PMC_48MT6.h: 314
try:
    DM_MOTOR_DEC_C = 12
except:
    pass

# Adhon_PMC_48MT6.h: 315
try:
    DM_MOTOR_PITH_X = 13
except:
    pass

# Adhon_PMC_48MT6.h: 316
try:
    DM_MOTOR_PITH_Y = 15
except:
    pass

# Adhon_PMC_48MT6.h: 317
try:
    DM_MOTOR_PITH_Z = 17
except:
    pass

# Adhon_PMC_48MT6.h: 318
try:
    DM_MOTOR_PITH_A = 19
except:
    pass

# Adhon_PMC_48MT6.h: 319
try:
    DM_MOTOR_PITH_B = 21
except:
    pass

# Adhon_PMC_48MT6.h: 320
try:
    DM_MOTOR_PITH_C = 23
except:
    pass

# Adhon_PMC_48MT6.h: 321
try:
    DM_MOTOR_DIV_X = 25
except:
    pass

# Adhon_PMC_48MT6.h: 322
try:
    DM_MOTOR_DIV_Y = 27
except:
    pass

# Adhon_PMC_48MT6.h: 323
try:
    DM_MOTOR_DIV_Z = 29
except:
    pass

# Adhon_PMC_48MT6.h: 324
try:
    DM_MOTOR_DIV_A = 31
except:
    pass

# Adhon_PMC_48MT6.h: 325
try:
    DM_MOTOR_DIV_B = 33
except:
    pass

# Adhon_PMC_48MT6.h: 326
try:
    DM_MOTOR_DIV_C = 35
except:
    pass

# Adhon_PMC_48MT6.h: 327
try:
    DM_MOTOR_MAX_SPD_X = 37
except:
    pass

# Adhon_PMC_48MT6.h: 328
try:
    DM_MOTOR_MAX_SPD_Y = 39
except:
    pass

# Adhon_PMC_48MT6.h: 329
try:
    DM_MOTOR_MAX_SPD_Z = 41
except:
    pass

# Adhon_PMC_48MT6.h: 330
try:
    DM_MOTOR_MAX_SPD_A = 43
except:
    pass

# Adhon_PMC_48MT6.h: 331
try:
    DM_MOTOR_MAX_SPD_B = 45
except:
    pass

# Adhon_PMC_48MT6.h: 332
try:
    DM_MOTOR_MAX_SPD_C = 47
except:
    pass

# Adhon_PMC_48MT6.h: 333
try:
    DM_MOTOR_MIN_SPD_X = 49
except:
    pass

# Adhon_PMC_48MT6.h: 334
try:
    DM_MOTOR_MIN_SPD_Y = 51
except:
    pass

# Adhon_PMC_48MT6.h: 335
try:
    DM_MOTOR_MIN_SPD_Z = 53
except:
    pass

# Adhon_PMC_48MT6.h: 336
try:
    DM_MOTOR_MIN_SPD_A = 55
except:
    pass

# Adhon_PMC_48MT6.h: 337
try:
    DM_MOTOR_MIN_SPD_B = 57
except:
    pass

# Adhon_PMC_48MT6.h: 338
try:
    DM_MOTOR_MIN_SPD_C = 59
except:
    pass

# Adhon_PMC_48MT6.h: 339
try:
    DM_MOTOR_POS_X = 61
except:
    pass

# Adhon_PMC_48MT6.h: 340
try:
    DM_MOTOR_POS_Y = 63
except:
    pass

# Adhon_PMC_48MT6.h: 341
try:
    DM_MOTOR_POS_Z = 65
except:
    pass

# Adhon_PMC_48MT6.h: 342
try:
    DM_MOTOR_POS_A = 67
except:
    pass

# Adhon_PMC_48MT6.h: 343
try:
    DM_MOTOR_POS_B = 69
except:
    pass

# Adhon_PMC_48MT6.h: 344
try:
    DM_MOTOR_POS_C = 71
except:
    pass

# Adhon_PMC_48MT6.h: 345
try:
    DM_MOTOR_MOVE_X = 73
except:
    pass

# Adhon_PMC_48MT6.h: 346
try:
    DM_MOTOR_MOVE_Y = 75
except:
    pass

# Adhon_PMC_48MT6.h: 347
try:
    DM_MOTOR_MOVE_Z = 77
except:
    pass

# Adhon_PMC_48MT6.h: 348
try:
    DM_MOTOR_MOVE_A = 79
except:
    pass

# Adhon_PMC_48MT6.h: 349
try:
    DM_MOTOR_MOVE_B = 81
except:
    pass

# Adhon_PMC_48MT6.h: 350
try:
    DM_MOTOR_MOVE_C = 83
except:
    pass

# Adhon_PMC_48MT6.h: 353
try:
    DM_MOTOR_LIMIT_LEFT_X = 85
except:
    pass

# Adhon_PMC_48MT6.h: 354
try:
    DM_MOTOR_LIMIT_RIGHT_X = 86
except:
    pass

# Adhon_PMC_48MT6.h: 355
try:
    DM_MOTOR_LIMIT_LEFT_Y = 87
except:
    pass

# Adhon_PMC_48MT6.h: 356
try:
    DM_MOTOR_LIMIT_RIGHT_Y = 88
except:
    pass

# Adhon_PMC_48MT6.h: 357
try:
    DM_MOTOR_LIMIT_LEFT_Z = 89
except:
    pass

# Adhon_PMC_48MT6.h: 358
try:
    DM_MOTOR_LIMIT_RIGHT_Z = 90
except:
    pass

# Adhon_PMC_48MT6.h: 359
try:
    DM_MOTOR_LIMIT_LEFT_A = 91
except:
    pass

# Adhon_PMC_48MT6.h: 360
try:
    DM_MOTOR_LIMIT_RIGHT_A = 92
except:
    pass

# Adhon_PMC_48MT6.h: 361
try:
    DM_MOTOR_LIMIT_LEFT_B = 93
except:
    pass

# Adhon_PMC_48MT6.h: 362
try:
    DM_MOTOR_LIMIT_RIGHT_B = 94
except:
    pass

# Adhon_PMC_48MT6.h: 363
try:
    DM_MOTOR_LIMIT_LEFT_C = 95
except:
    pass

# Adhon_PMC_48MT6.h: 364
try:
    DM_MOTOR_LIMIT_RIGHT_C = 96
except:
    pass

# Adhon_PMC_48MT6.h: 367
try:
    DM_AD_MIN_1 = 120
except:
    pass

# Adhon_PMC_48MT6.h: 368
try:
    DM_AD_MAX_1 = 122
except:
    pass

# Adhon_PMC_48MT6.h: 369
try:
    DM_AD_MIN_2 = 124
except:
    pass

# Adhon_PMC_48MT6.h: 370
try:
    DM_AD_MAX_2 = 126
except:
    pass

# Adhon_PMC_48MT6.h: 371
try:
    DM_AD_MODE_1 = 128
except:
    pass

# Adhon_PMC_48MT6.h: 372
try:
    DM_AD_MODE_2 = 130
except:
    pass

# Adhon_PMC_48MT6.h: 373
try:
    DM_ENCODER_LINE_1 = 132
except:
    pass

# Adhon_PMC_48MT6.h: 374
try:
    DM_ENCODER_LINE_2 = 134
except:
    pass

# Adhon_PMC_48MT6.h: 375
try:
    DM_ENCODER_LINE_3 = 136
except:
    pass

# Adhon_PMC_48MT6.h: 376
try:
    DM_ENCODER_SCALE_1 = 138
except:
    pass

# Adhon_PMC_48MT6.h: 377
try:
    DM_ENCODER_SCALE_2 = 140
except:
    pass

# Adhon_PMC_48MT6.h: 378
try:
    DM_ENCODER_SCALE_3 = 142
except:
    pass

# Adhon_PMC_48MT6.h: 379
try:
    DM_ENCODER_MODE_1 = 144
except:
    pass

# Adhon_PMC_48MT6.h: 380
try:
    DM_ENCODER_MODE_2 = 146
except:
    pass

# Adhon_PMC_48MT6.h: 381
try:
    DM_ENCODER_MODE_3 = 148
except:
    pass

# Adhon_PMC_48MT6.h: 384
try:
    DM_CONTROL_ADDR = 200
except:
    pass

# Adhon_PMC_48MT6.h: 385
try:
    DM_PROGRAM_NO = 201
except:
    pass

# Adhon_PMC_48MT6.h: 386
try:
    DM_WORK_MODE = 202
except:
    pass

# Adhon_PMC_48MT6.h: 387
try:
    DM_PROGRAM_CODE_LINE = 203
except:
    pass

# Adhon_PMC_48MT6.h: 388
try:
    DM_USE_TRY_TOTAL_TIMES = 204
except:
    pass

# Adhon_PMC_48MT6.h: 389
try:
    DM_USE_HAVE_RUN_TIME = 206
except:
    pass

# Adhon_PMC_48MT6.h: 390
try:
    DM_USE_PASSWD = 208
except:
    pass

# Adhon_PMC_48MT6.h: 393
try:
    DM_VIDEO_TEACHSTART_POINT_X = 350
except:
    pass

# Adhon_PMC_48MT6.h: 394
try:
    DM_VIDEO_TEACHSTART_POINT_Y = 352
except:
    pass

# Adhon_PMC_48MT6.h: 395
try:
    DM_VIDEO_TEACHVER_NUM = 354
except:
    pass

# Adhon_PMC_48MT6.h: 396
try:
    DM_VIDEO_TEACHHER_NUM = 355
except:
    pass

# Adhon_PMC_48MT6.h: 397
try:
    DM_VIDEO_TEACHVER_DIST = 356
except:
    pass

# Adhon_PMC_48MT6.h: 398
try:
    DM_VIDEO_TEACHHER_DIST = 358
except:
    pass

# Adhon_PMC_48MT6.h: 399
try:
    DM_VIDEO_TEACH_TOTAL_POINT = 360
except:
    pass

# Adhon_PMC_48MT6.h: 400
try:
    DM_VIDEO_TEACH_CUR_POINT = 361
except:
    pass

# Adhon_PMC_48MT6.h: 401
try:
    DM_VIDEO_TEACH_MASK_INPUT = 362
except:
    pass

# Adhon_PMC_48MT6.h: 402
try:
    DM_VIDEO_TEACH_MASK_OUTPUT = 364
except:
    pass

# Adhon_PMC_48MT6.h: 403
try:
    DM_VIDEO_TEACH_DELAY_TIME = 366
except:
    pass

# Adhon_PMC_48MT6.h: 406
try:
    DM_MAX_USER_CNT = 5
except:
    pass

# Adhon_PMC_48MT6.h: 407
try:
    DM_USER_PROGRAM_INDEX = 378
except:
    pass

# Adhon_PMC_48MT6.h: 408
try:
    DM_USER_PROGRAM_SIZE_0 = 380
except:
    pass

# Adhon_PMC_48MT6.h: 409
try:
    DM_USER_PROGRAM_SIZE_1 = 382
except:
    pass

# Adhon_PMC_48MT6.h: 410
try:
    DM_USER_PROGRAM_SIZE_2 = 384
except:
    pass

# Adhon_PMC_48MT6.h: 411
try:
    DM_USER_PROGRAM_SIZE_3 = 386
except:
    pass

# Adhon_PMC_48MT6.h: 412
try:
    DM_USER_PROGRAM_SIZE_4 = 387
except:
    pass

# Adhon_PMC_48MT6.h: 414
try:
    DM_CUSTOM_DEFINE = 400
except:
    pass

# No inserted files

# No prefix-stripping

