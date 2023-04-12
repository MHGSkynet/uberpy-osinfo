#	----------------------------------------------------------------------------------------------------------------------------
#	Ubergen Operating System Information class
#	----------------------------------------------------------------------------------------------------------------------------
#	Description:
#
#		Class to get operating system information, IN A STANDARD FORMAT
#
#   Supported OSes:
#       Windows         10, 11?
#       Cygwin          all versions
#       Debian          10, 11
#       Ubuntu          20, 22
#       CentOS          
#       OpenSUSE        Tumbleweed
#
#	Copyrignt: (c) 2023, Kurt Schulte
#
#	History
#	---------- ----- -------------- --------------------------------------------------------------------------------------------
#	2023.04.12 01.00 KSchulte		Original Version
#	---------- ----- -------------- --------------------------------------------------------------------------------------------
#

from datetime import datetime
import os
import platform
import re

class OsInfo(object):
    """
    OsInfo Object

        Operating System Information object.  Contains information about
        the OS, in a consistent manner across platforms for use in compares.

    Returns:
    object: OsInfo          OS Information Object
    """

    # Control data

    _initialized        = False
    _debug              = False                     

    # OS Information Properties
                                                    # Desc                                                      Example
                                                    # --------------------------------------------------------- -------------------------------------
    _type               = 'Unknown'                 # OS type                                                   posix, nt, os2, ce, java, riscos
    _kernel             = 'Unknown'                 # Kernel version
    _machine            = 'Unknown'                 # Machine type                                              x86_64
    _distrobase         = 'Unknown'                 # Disto base                                                Windows, Debian, Redhat
    _codename           = 'Unknown'                 # Internal codename                                         skeletor
    _name               = 'Unknown'                 # Name (as reported by OS)                                  Debian GNU/Linux
    _prettyname         = 'Unknown'                 # Pretty name                                               Ubuntu 20.04.6 LTS
    _flavor             = 'Unknown'                 # Flavor (standardized name)                                Windows, Ubuntu, Debian, SuSE
    _release            = 'Unknown'                 # Major version                                             20
    _version            = 'Unknown'                 # Major/minor version                                       20.04
    _revision           = 'Unknown'                 # Complete version id                                       20.04.6 LTS
    _flavverflav        = 'Unknown'                 # Flavor, Major version, and Minor version, no spaces       Ubuntu20.04
    _desktop            = 'Unknown'                 # Desktop framework                                         Gnome, xfc
    
    _isWindows          = False                     # OS is Windows
    _isWsl              = False                     # OS is Windows Subsystem for Linux of some sort
    _isPosix            = False                     # OS is Posix of some sort
    _isLinux            = False                     # OS is Linux of some sort
    _isCygwin           = False                     # OS is Cygwin
    _isDebian           = False                     # OS is Debiam
    _isUbuntu           = False                     # OS is Ubuntu
    _isOpenSUSE         = False                     # OS is OpenSUSE

    # DEBUG DATA
    # Values returned from os.uname
    _uname_sysname      = 'Unknown'                 # 
    _uname_nodename     = 'Unknown'                 # 
    _uname_release      = 'Unknown'                 # 
    _uname_version      = 'Unknown'                 # 
    _uname_machine      = 'Unknown'                 # 
    _uname_processor    = 'Unknown'                 # 
    
    # Values returned from platform.uname
    _platform_sysname   = 'Unknown'                 #
    _platform_nodename  = 'Unknown'                 #
    _platform_release   = 'Unknown'                 #
    _platform_version   = 'Unknown'                 #
    _platform_machine   = 'Unknown'                 #
    _platform_processor = 'Unknown'                 #

    
    # OsInfo Constructor
    def __init__(self):
        """
        OsInfo Object Constructor

            Creates an OsInfo object.

        Returns:
        none
        """

        self._initialized       = True

        self._type              = os.name

        # Windows
        if self._type == 'nt':

            self._isWindows = True
            self._type      = 'Windows'
            self._release   = platform.release()
            lVersion        = platform.version()
            match           = re.match(r'^([0-9]+[.][0-9]+).[0-9]+.*',lVersion)
            if match:
                self._version   = match.group(1)
            else:
                self._version   = lVersion
 
            l_uname                     = platform.uname()
            self._uname_sysname         = l_uname.system
            self._uname_nodename        = l_uname.node
            self._uname_release         = l_uname.release
            self._uname_version         = l_uname.version
            self._uname_machine         = l_uname.machine
            self._uname_processor       = l_uname.processor

            self._platform_sysname     = l_uname.system
            self._platform_nodename    = l_uname.node
            self._platform_release     = l_uname.release
            self._platform_version     = l_uname.version
            self._platform_machine     = l_uname.machine
            self._platform_processor   = l_uname.processor

            self._flavor                = 'Windows'
            self._name                  = 'Windows'
            self._distrobase            = 'Windows'
            self._machine               = self._uname_machine
            self._revision              = self._uname_version
            self._prettyname            = '{0} {1}'.format(self._name,self._version)
            self._flavverflav           = '{0}{1}'.format(self._name,self._release)

            self._desktop               = 'Windows'

        # Linux
        elif self._type == 'posix':

            self._barfd('Is POSIX')
            self._isPosix               = True

            (self._uname_sysname, self._uname_nodename, self._uname_release, self._uname_version, self._uname_machine) = os.uname()
            l_uname         = platform.uname()
            self._platform_sysname     = l_uname.system
            self._platform_nodename    = l_uname.node
            self._platform_release     = l_uname.release
            self._platform_version     = l_uname.version
            self._platform_machine     = l_uname.machine
            self._platform_processor   = l_uname.processor

            self._uname_sysname     = self._uname_sysname.lower()

            # Cygwin
            if self._uname_sysname.startswith('cygwin'):
                self._barfd('Is CYGWIN')
                self._isCygwin      = True
                self._type          = 'Linux'
                self._flavor        = 'Cygwin'
                self._name          = 'Cygwin'
                self._distrobase    = 'Cygwin'
                self._machine       = self._uname_machine
                match           = re.match(r'^([0-9]+).([0-9]+).([0-9.]+)[^0-9.].*$',self._uname_release)
                if match:
                    self._release   = match.group(1) + '.' + match.group(2)
                    self._version   = match.group(1) + '.' + match.group(2) + '.' + match.group(3)
                    self._revision  = self._version
                    self._prettyname    = "{0} {1}".format(self._name,self._version)
                    self._flavverflav   = "{0}{1}".format(self._name,self._release)
                self._desktop       = '[None]'

            # Linux
            elif self._uname_sysname.startswith('linux'):
                self._barfd('Is LINUX')
                self._isLinux   = True
                self._type      = 'Linux'

                # WSL
                match = re.match(r'.*WSL.*',self._uname_release)
                matched = False
                if match:
                    self._barfd('Is LINUX WSL')
                    self._isWsl         = True
                    self._type          = 'Linux WSL'
                    lOsRelease          = self._readOsRelease()
                    self._machine       = self._uname_machine
                    self._prettyname    = self._qnul(lOsRelease['PRETTY_NAME'])
                    self._name          = self._qnul(lOsRelease['NAME'])
                    self._flavor        = self._qnul(lOsRelease['NAME'])
                    self._release       = self._qnul(lOsRelease['VERSION_ID'])
                    self._version       = self._qnul(lOsRelease['VERSION'])
                    self._revision      = self._qnul(lOsRelease['VERSION'])
                    self._codename      = self._qnul(lOsRelease['VERSION_CODENAME'])
                    self._distrobase    = self._qnul(lOsRelease['ID_LIKE'])
                    match2      = re.match(r'^([^()]+) +[(].*',self._version)
                    if match2:
                        self._version   = match2.group(1)
                    self._flavverflav   = '{0}{1}'.format(self._name,self._release)
                    self._desktop       = 'Windows'
                    matched             = True

                # Debian
                #   > cat /etc/os-release
                #       PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
                #       NAME="Debian GNU/Linux"
                #       VERSION_ID="11"
                #       VERSION="11 (bullseye)"
                #       VERSION_CODENAME=bullseye
                #       ID=debian
                #       HOME_URL="https://www.debian.org/"
                #       SUPPORT_URL="https://www.debian.org/support"
                #       BUG_REPORT_URL="https://bugs.debian.org/"
                if not matched:
                    match = re.match(r'.*Debian.*',self._uname_version)
                    if match:
                        self._isDebian      = True
                        self._barfd('Is LINUX DEBIAN')
                        lOsRelease      = self._readOsRelease()
                        self._machine       = self._uname_machine
                        self._prettyname    = self._qnul(lOsRelease['PRETTY_NAME'])
                        self._name          = self._qnul(lOsRelease['NAME'])
                        self._flavor        = 'Debian'
                        self._release       = self._qnul(lOsRelease['VERSION_ID'])
                        self._version       = self._qnul(self._readDebianRelease())
                        self._revision      = self._version
                        self._codename      = self._qnul(lOsRelease['VERSION_CODENAME'])
                        self._distrobase    = 'Debian'
                        self._flavverflav   = '{0}{1}'.format(self._flavor,self._version)
                        matched             = True

                # Ubuntu
                #   > cat /etc/os-release
                #       NAME="Ubuntu"
                #       VERSION="20.04.6 LTS (Focal Fossa)"
                #       ID=ubuntu
                #       ID_LIKE=debian
                #       PRETTY_NAME="Ubuntu 20.04.6 LTS"
                #       VERSION_ID="20.04"
                #       HOME_URL="https://www.ubuntu.com/"
                #       SUPPORT_URL="https://help.ubuntu.com/"
                #       BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
                #       PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
                #       VERSION_CODENAME=focal
                #       UBUNTU_CODENAME=focal

                if not matched:
                    match = re.match(r'.*Ubuntu.*',self._uname_version)
                    if match:
                        self._barfd('Is LINUX UBUNTU')
                        self._isUbuntu      = True
                        lOsRelease          = self._readOsRelease()
                        self._machine       = self._uname_machine
                        self._prettyname    = self._qnul(lOsRelease['PRETTY_NAME'])
                        self._name          = self._qnul(lOsRelease['NAME'])
                        self._flavor        = 'Ubuntu'
                        self._release       = self._qnul(lOsRelease['VERSION_ID'])
                        self._version       = self._qnul(self._readDebianRelease())
                        self._revision      = self._qnul(lOsRelease['VERSION'])
                        self._codename      = self._qnul(lOsRelease['VERSION_CODENAME'])
                        self._distrobase    = 'Debian'
                        self._flavverflav   = '{0}{1}'.format(self._name,self._release)
                        matched             = True

                # OpenSUSE Tumbleweed 2023.04.11
                #   > cat /etc/os-release
                #       NAME="openSUSE Tumbleweed"
                #       # VERSION="20230411"
                #       ID="opensuse-tumbleweed"
                #       ID_LIKE="opensuse suse"
                #       VERSION_ID="20230411"
                #       PRETTY_NAME="openSUSE Tumbleweed"
                #       ANSI_COLOR="0;32"
                #       CPE_NAME="cpe:/o:opensuse:tumbleweed:20230411"
                #       BUG_REPORT_URL="https://bugzilla.opensuse.org"
                #       SUPPORT_URL="https://bugs.opensuse.org"
                #       HOME_URL="https://www.opensuse.org"
                #       DOCUMENTATION_URL="https://en.opensuse.org/Portal:Tumbleweed"
                #       LOGO="distributor-logo-Tumbleweed"
                if not matched:
                    lOsRelease      = self._readOsRelease()
                    if lOsRelease['NAME'].startswith('openSUSE'):
                        self._barfd('Is LINUX SUSE')
                        self._isOpenSUSE    = True
                        self._machine       = self._platform_machine
                        self._distrobase    = 'OpenSUSE'
                        self._codename      = ''
                        self._name          = self._qnul(lOsRelease['NAME'])
                        self._flavor        = 'OpenSUSE'
                        match = re.match(r'^openSUSE ([A-Za-z]+)$',self._name)
                        if match:
                            self._release       = match.group(1)
                        self._version       = self._qnul(lOsRelease['VERSION_ID'])
                        self._revision      = self._qnul(lOsRelease['VERSION_ID'])                      
                        self._flavverflav   = '{0}{1}'.format(self._flavor,self._release)
                        self._prettyname    = '{0} {1}'.format(self._qnul(lOsRelease['PRETTY_NAME']),self._version)
                        matched             = True               
                        
                # Unknown Linux
                if not matched:
                    print('Unknown flavor of linux! {}'.format(self._uname_sysname))
       

            # Unknown flavor Linux
            else:
                #platform_version      #1 SMP Debian 5.10.92-1 (2022-01-18)

                print('osInfo: Cannot map sysname={}'.format(self._uname_sysname))

    #
    # Private Methods
    #

    def _barfd(self,text):
        """
        Barf Debug

            Print text, if debug is enabled

        Returns:
        none
        """
        if self._debug:
            print("#DEBUG# {}".format(text))

    def _readOsRelease(self) -> dict:
        """
        Read OS Release File

            Reads os-relase file in etc folder to get relase data, as a
            dictionary of key/value pairs.

        Returns:
        dictionary: releaseInfo    key-value pairs
        """
        lDict       = {}
        try:
            releaseFile = '/etc/os-release'
            with open(releaseFile,'r') as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    key, value = line.split('=',1)
                    lDict[key]  = value.replace('"','')
        except FileNotFoundError:
            print("Error: File '{0}' not found.".format(releaseFile))
        except IOError:
            print("Error: Could not open file '{0}'.".format(releaseFile))

        return lDict

    def _readDebianRelease(self) -> str:
        """
        Read Debian Release

            Reads debian_version file in etc folder to determine release number

        Returns:
        str: Debian release number
        """
        retval  = 'Unknown'
        releaseFile = '/etc/debian_version'
        try:
            with open(releaseFile,'r') as fh:
                retval = fh.readline().strip()
        except FileNotFoundError:
            print("Error: File '{0}' not found.".format(releaseFile))
        except IOError:
            print("Error: Could not open file '{0}'.".format(releaseFile))

        return retval

    def _getLinuxDesktop(self) -> str:
        """
        Get Linux Desktop

            Determines what Linux Desktop is being used

        Returns:
        str: Type of Desktop (Gnome,XFCE,KDE,etc), or 'Unknown'
        """
        retval          = 'Unknown'
        xdgDesktop      = os.environ.get('XDG_CURRENT_DESKTOP')
        if (re.match(r'.*GNOME.*',xdgDesktop)):
            retval      = 'Gnome'
        if (re.match(r'.*XFCE.*',xdgDesktop)):
            retval      = 'XFCE'
        if (re.match(r'.*KDE.*',xdgDesktop)):
            retval      = 'KDE'
        return retval

    def _qnul(self,value) -> str:
        retval = value
        if not retval:
            retval  = ''
        return retval

    #
    # Public Properties
    #
    def type(self) -> str:
        """
        OS Type
        
        Returns:
        str:    OS type         (ex:posix, nt, os2, ce, java, riscos,default:Unknown)
        """
        return self._type

    def kernel(self) -> str:
        """
        OS Kernel
        
        Returns:
        str:    OS kernel       (as reported by ???,default:Unknown)
        """
        return self._kernel
        
    def machine(self) -> str:
        """
        Machine Type
        
        Returns:
        str:    Machine type    (ex:_x86_64,default:Unknown)
        """
        return self._machine
        
    def distrobase(self) -> str:
        """
        OS Distro Base
   
        Returns:
        str:    OS distro base  (ex:Debian,Redhat,default:Unknown)
        """
        return self._distrobase
        
    def codename(self) -> str:
        """
        OS Codename
   
        Returns:
        str:    OS codename     (ex:Buster,Sid,Focal,default:Unknown)
        """
        return self._codename

    def name(self) -> str:
        """
        OS Name

           OS name as reported by OS.
        
        Returns:
        str:    OS name         (ex:Debian,Ubuntu,Windows,default:Unknown)
        """
        return self._flavor

    def flavor(self) -> str:
        """
        OS Flavor

           OS name for use in compares, simple and consistent
        
        Returns:
        str:    OS flavor       (Debian,Ubuntu,default:Unknown)
        """
        return self._flavor
        
     
    def release(self) -> str:
        """
        OS Release

           OS major version ID for use in compares, simple and consistent
        
        Returns:
        str:    OS release      (11,default:Unknown)
        """
        return self._release

    def version(self) -> str:
        """
        OS Version

           OS major and minor version ID for use in compares, simple and consistent
        
        Returns:
        str:    OS version      (11.2,default:Unknown)
        """
        return self._version
                
    def revision(self) -> str:
        """
        OS Revision

           OS complete major,minor, and revision ID
        
        Returns:
        str:    OS revision     (20.04 LTS,10.0.32412,default:Unknown)
        """
        return self._revision
        
    def flavverflav(self) -> str:
        """
        OS Flavaflav (Yo!)

           OS name, major, and minor versions, sans spaces, for use in compares,
           simple and consistent
        
        Returns:
        str:    OS flavaflav    (Debian11.0,Ubuntu20.04,Windows10.0,default:Unknown)
        """
        return self._flavverflav

    def desktop(self) -> str:
        """
        OS Desktop

           For systems that are not headless, the kind of desktop environment
           being used.
        
        Returns:
        str:    OS desktop      (ex:Gnome,XFCE,KDE,Windows,default:Unknown)
        """
        return self._desktop
      
    # Logical Properties

    def isWindows(self) -> bool:
        """
        Is Windows

        Returns:
        bool:   isWindows       (true/false)
        """
        return self._isWindows

    def isWsl(self) -> bool:
        """
        Is Windows Subystem for Linux

        Returns:
        bool:   isWsl           (true/false)
        """
        return self._isWsl

    def isPosix(self) -> bool:
        """
        Is Posix (Linux or Unix)

        Returns:
        bool:   isPosix         (true/false)
        """
        return self.isPosix

    def isLinux(self) -> bool:
        """
        Is Linux

        Returns:
        bool:   isLinux         (true/false)
        """
        return self.isLinux

    def isCygwyn(self) -> bool:
        """
        Is Cygwin

        Returns:
        bool:   isCygwin        (true/false)
        """
        return self._isCygwin

    def isDebian(self) -> bool:
        """
        Is Debian

        Returns:
        bool:   isDebian        (true/false)
        """
        return self._isDebian
    
    def isUbuntu(self) -> bool:
        """
        Is Ubuntu

        Returns:
        bool:   isUbuntu        (true/false)
        """
        return self._isUbuntu

    #
    # Public Methods
    #

    def Dump(self):
        """
        Dump

          Print values of all public properties

        Returns:
        none
        """
        outfmt="{0:21} {1:30}"
        dashes=outfmt.format("-"*21,"-"*30)
        print("="*80)
        print("OS INFO")
        print(dashes)
        print(outfmt.format("currdate",datetime.now().strftime("%Y.%m.%d")))
        print(outfmt.format("type",self._type))
        print(outfmt.format("kernel",self._kernel))
        print(outfmt.format("machine",self._machine))
        print(outfmt.format("distrobase",self._distrobase))
        print(outfmt.format("codename",self._codename))
        print(outfmt.format("name",self._name))
        print(outfmt.format("prettyname",self._prettyname))
        print(outfmt.format("flavor",self._flavor))
        print(outfmt.format("release",self._release))
        print(outfmt.format("version",self._version))
        print(outfmt.format("revision",self._revision))
        print(outfmt.format("flaverflav",self._flavverflav))
        print(outfmt.format("desktop",self._desktop))
        outfmt="{0:21} {1}"                                         # :30 causes bools to print as ints, and not T/F ?
        print(outfmt.format("isWindows",self._isWindows))
        print(outfmt.format("isWsl",self._isWsl))
        print(outfmt.format("isPosix",self._isPosix))
        print(outfmt.format("isLinux",self._isLinux))
        print(outfmt.format("isCygwin",self._isCygwin))
        print(outfmt.format("isDebian",self._isDebian))
        print(outfmt.format("isUbuntu",self._isUbuntu))       

    def DumpDebugVars(self):
        """
        Dump Debug Variables

          Print values of all debug data

        Returns:
        none
        """
        outfmt="{0:21} {1:30}"
        print("-- debug data---")
        print(outfmt.format("uname_sysname",self._uname_sysname))
        print(outfmt.format("uname_nodename",self._uname_nodename))
        print(outfmt.format("uname_release",self._uname_release))
        print(outfmt.format("uname_version",self._uname_version))
        print(outfmt.format("uname_machine",self._uname_machine))
        print(outfmt.format("uname_processor",self._uname_processor))
        print(outfmt.format("platform_sysname",self._platform_sysname))
        print(outfmt.format("platform_nodename",self._platform_nodename))
        print(outfmt.format("platform_release",self._platform_release))
        print(outfmt.format("platform_version",self._platform_version))
        print(outfmt.format("platform_machine",self._platform_machine))
        print(outfmt.format("platform_processor",self._platform_processor))

#================================================================================
# 
#    DUMP FROM VARIOUS OPERATING SYSTEMS
# 
#================================================================================


#================================================================================
# Windows 10 
#================================================================================
#OS INFO
#--------------------- ------------------------------
#currdate              2023.04.12
#type                  Windows
#kernel                Unknown
#machine               AMD64
#distrobase            Windows
#codename              Unknown
#name                  Windows
#prettyname            Windows 10.0
#flavor                Windows
#release               10
#version               10.0
#revision              10.0.19044
#flaverflav            Windows10
#desktop               Windows
#isWindows             True
#isWsl                 False
#isPosix               False
#isLinux               False
#isCygwin              False
#isDebian              False
#isUbuntu              False
#-- debug variables---
#uname_sysname         Windows
#uname_nodename        ANIMAL-W10
#uname_release         10
#uname_version         10.0.19044
#uname_machine         AMD64
#uname_processor       AMD64 Family 23 Model 49 Stepping 0, AuthenticAMD
#platform_sysname      Windows
#platform_nodename     ANIMAL-W10
#platform_release      10
#platform_version      10.0.19044
#platform_machine      AMD64
#platform_processor    AMD64 Family 23 Model 49 Stepping 0, AuthenticAMD

#================================================================================
# Cygwin
#================================================================================
#OS INFO
#--------------------- ------------------------------
#currdate              2023.04.12
#type                  Linux
#kernel                Unknown
#machine               x86_64
#distrobase            Cygwin
#codename              Unknown
#name                  Cygwin
#prettyname            Cygwin 3.4.3
#flavor                Cygwin
#release               3.4
#version               3.4.3
#revision              3.4.3
#flaverflav            Cygwin3.4
#desktop               None
#isWindows             False
#isWsl                 False
#isPosix               True
#isLinux               False
#isCygwin              True
#isDebian              False
#isUbuntu              False
#-- debug data---
#uname_sysname         cygwin_nt-10.0-19044
#uname_nodename        ANIMAL-W10
#uname_release         3.4.3-1.x86_64
#uname_version         2022-12-16 12:38 UTC
#uname_machine         x86_64
#uname_processor       Unknown
#platform_sysname      CYGWIN_NT-10.0-19044
#platform_nodename     ANIMAL-W10
#platform_release      3.4.3-1.x86_64
#platform_version      2022-12-16 12:38 UTC
#platform_machine      x86_64
#platform_processor

#================================================================================
# WSL Linux - Ubuntu 22.04 LTS
#================================================================================
#OS INFO
#--------------------- ------------------------------
#currdate              2023.04.12
#type                  Linux WSL
#kernel                Unknown
#machine               x86_64
#distrobase            debian
#codename              jammy
#name                  Ubuntu
#prettyname            Ubuntu 22.04.2 LTS
#flavor                Ubuntu
#release               22.04
#version               22.04.2 LTS
#revision              22.04.2 LTS (Jammy Jellyfish)
#flaverflav            Ubuntu22.04
#desktop               Windows
#isWindows             False
#isWsl                 True
#isPosix               True
#isLinux               True
#isCygwin              False
#isDebian              False
#isUbuntu              False
#-- debug data---
#uname_sysname         linux
#uname_nodename        ANIMAL-W10
#uname_release         5.15.90.1-microsoft-standard-WSL2
#uname_version         #1 SMP Fri Jan 27 02:56:13 UTC 2023
#uname_machine         x86_64
#uname_processor       Unknown
#platform_sysname      Linux
#platform_nodename     ANIMAL-W10
#platform_release      5.15.90.1-microsoft-standard-WSL2
#platform_version      #1 SMP Fri Jan 27 02:56:13 UTC 2023
#platform_machine      x86_64
#platform_processor    x86_64

#================================================================================
# Linux - Debian 11.6
#================================================================================
#OS INFO
#--------------------- ------------------------------
#currdate              2023.04.12                    
#type                  Linux                         
#kernel                Unknown                       
#machine               x86_64                        
#distrobase            Debian                        
#codename              bullseye                      
#name                  Debian GNU/Linux              
#prettyname            Debian GNU/Linux 11 (bullseye)
#flavor                Debian                        
#release               11                            
#version               11.6                          
#revision              11.6                          
#flaverflav            Debian11.6                    
#desktop               Unknown                       
#isWindows             False
#isWsl                 False
#isPosix               True
#isLinux               True
#isCygwin              False
#isDebian              True
#isUbuntu              False
#-- debug data---
#uname_sysname         linux                         
#uname_nodename        maude-d11-01                  
#uname_release         5.10.0-11-amd64               
#uname_version         #1 SMP Debian 5.10.92-1 (2022-01-18)
#uname_machine         x86_64                        
#uname_processor       Unknown                       
#platform_sysname      Linux                         
#platform_nodename     maude-d11-01                  
#platform_release      5.10.0-11-amd64               
#platform_version      #1 SMP Debian 5.10.92-1 (2022-01-18)
#platform_machine      x86_64                        
#platform_processor               

#================================================================================
# Linux - Ubuntu 20.04 LTS
#================================================================================
#OS INFO
#--------------------- ------------------------------
#currdate              2023.04.12                    
#type                  Linux                         
#kernel                Unknown                       
#machine               x86_64                        
#distrobase            Debian                        
#codename              focal                         
#name                  Ubuntu                        
#prettyname            Ubuntu 20.04.6 LTS            
#flavor                Ubuntu                        
#release               20.04                         
#version               bullseye/sid                  
#revision              20.04.6 LTS (Focal Fossa)     
#flaverflav            Ubuntu20.04                   
#desktop               Unknown                       
#isWindows             False
#isWsl                 False
#isPosix               True
#isLinux               True
#isCygwin              False
#isDebian              False
#isUbuntu              True
#-- debug data---
#uname_sysname         linux                         
#uname_nodename        ubuntu                        
#uname_release         5.15.0-69-generic             
#uname_version         #76~20.04.1-Ubuntu SMP Mon Mar 20 15:54:19 UTC 2023
#uname_machine         x86_64                        
#uname_processor       Unknown                       
#platform_sysname      Linux                         
#platform_nodename     ubuntu                        
#platform_release      5.15.0-69-generic             
#platform_version      #76~20.04.1-Ubuntu SMP Mon Mar 20 15:54:19 UTC 2023
#platform_machine      x86_64                        
#platform_processor    x86_64                        
#root@ubuntu:/mnt/kode/UberGen/pyth                    