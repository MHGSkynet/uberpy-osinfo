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
#       CentOS          Linux 8, Stream 8+
#       OpenSUSE        Tumbleweed
#
#	Copyrignt: (c) 2023, MHG Squint
#
#	History
#	---------- ----- -------------- --------------------------------------------------------------------------------------------
#	2023.04.12 01.00 Squint  		Original Version
#	---------- ----- -------------- --------------------------------------------------------------------------------------------
#

from datetime import datetime
from doctest import OutputChecker
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
    _flavor             = 'Unknown'                 # Flavor (standardized name)                                Windows, Ubuntu, Debian, OpenSUSE
    _release            = 'Unknown'                 # Major version                                             20
    _version            = 'Unknown'                 # Major/minor version                                       20.04
    _revision           = 'Unknown'                 # Complete version id                                       20.04.6 LTS
    _flavverflav        = 'Unknown'                 # Flavor, Major version, and Minor version, no spaces       Ubuntu20.04
    _desktop            = 'Unknown'                 # Desktop framework                                         Gnome, XFCE, KDE, Windows

    _title              = ''                        # Title for reporting header
    
    _isWindows          = False                     # OS is Windows
    _isWsl              = False                     # OS is Windows Subsystem for Linux of some sort
    _isPosix            = False                     # OS is Posix of some sort
    _isLinux            = False                     # OS is Linux of some sort
    _isCygwin           = False                     # OS is Cygwin
    _isDebian           = False                     # OS is Debian
    _isUbuntu           = False                     # OS is Ubuntu
    _isOpenSuse         = False                     # OS is OpenSuse
    _isRedhat           = False                     # OS is Redhat
    _isCentOS           = False                     # OS is CentOS

    _logEnable          = True                      # Log enable
    _logFile            = None                      # Log file name.  Default={flavverflav}.tct
    _logChan            = None                      # Log file handle

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
            # os.uname does not exist on Windows python
            self._uname_sysname         = 'n/a'
            self._uname_nodename        = 'n/a'
            self._uname_release         = 'n/a'
            self._uname_version         = 'n/a'
            self._uname_machine         = 'n/a'
            self._uname_processor       = 'n/a'

            self._platform_sysname     = l_uname.system
            self._platform_nodename    = l_uname.node
            self._platform_release     = l_uname.release
            self._platform_version     = l_uname.version
            self._platform_machine     = l_uname.machine
            self._platform_processor   = l_uname.processor

            self._machine               = self._platform_machine
            self._name                  = 'Windows'
            self._distrobase            = 'Windows'
            self._flavor                = 'Windows'
            self._revision              = self._platform_version
            self._flavverflav           = '{0}{1}'.format(self._name,self._release)
            self._prettyname            = '{0} {1}'.format(self._name,self._version)

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
                self._desktop       = 'None'

            # Linux
            elif self._uname_sysname.startswith('linux'):
                self._barfd('Is LINUX')
                self._isLinux   = True
                self._type      = 'Linux'

                self._desktop   = self._getLinuxDesktop()

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
                    self._desktop       = 'None'
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
                        self._isOpenSuse    = True
                        self._machine       = self._platform_machine
                        self._distrobase    = 'OpenSUSE'
                        self._codename      = 'n/a'
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
                        
                # Unknown Linux, based on uname.  Try using /etc/os-release only...
                if not matched:
                    lOsRelease          = self._readOsRelease()
                    
                    # CENTOS
                    #
                    # cat /etc/os-release
                    #       NAME="CentOS Stream"
                    #       VERSION="8"
                    #       ID="centos"
                    #       ID_LIKE="rhel fedora"
                    #       VERSION_ID="8"
                    #       PLATFORM_ID="platform:el8"
                    #       PRETTY_NAME="CentOS Stream 8"
                    #       ANSI_COLOR="0;31"
                    #       CPE_NAME="cpe:/o:centos:centos:8"
                    #       HOME_URL="https://centos.org/"
                    #       BUG_REPORT_URL="https://bugzilla.redhat.com/"
                    #       REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 8"
                    #       REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
                    if self._qnul(lOsRelease['ID']) == 'centos':
                        self._isCentOS      = True
                        self._machine       = self._uname_machine
                        self._prettyname    = self._qnul(lOsRelease['PRETTY_NAME'])
                        self._name          = self._qnul(lOsRelease['NAME'])
                        self._flavor        = 'CentOS'
                        self._release       = self._qnul(lOsRelease['VERSION_ID'])
                        self._version       = self._qnul(lOsRelease['VERSION'])
                        self._revision      = self._qnul(lOsRelease['VERSION'])
                        self._codename      = 'n/a'
                        self._distrobase    = 'Redhat'
                        self._flavverflav   = '{0}{1}'.format(self._flavor,self._release)
                        matched             = True

                if not matched:
                    print('Unknown flavor of linux! {}'.format())
       

            # Unknown flavor Linux
            else:
                #platform_version      #1 SMP Debian 5.10.92-1 (2022-01-18)

                print('osInfo: Cannot map sysname={}'.format(self._uname_sysname))

    #
    # Private Methods
    #
   
    def _logInit(self):
        """
        Log Init

            Initialize Log file

        Returns:
        none
        """
        if self._logEnable:
            try:
                self._logChan   = open(self.logFile(),'w')

            except FileNotFoundError:
                print("Error: Log File '{0}' not found.".format(self._logFile))
            except IOError:
                print("Error: Could not open Log file '{0}'.".format(self._logFile))        

    def _logOpen(self):
        """
        Log Open

            Open log file for writing, if it isn't already

        Returns:
        none
        """
        if self._logEnable and self._logChan is None:
            self._logChan     = open(self.logFile(),"a")

    def _logWrite(self,text):
        """
        Log Write 

            Write text to log file

        Returns:
        none
        """ 
        if self._logEnable:
            self._logChan.write(text + "\n")

    def _barf(self,text):
        """
        Barf 

            Print and log text

        Returns:
        none
        """
        print(text)
        self._logWrite(text)

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
        if xdgDesktop:
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
    # Public Properties - Getters
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
      
    def title(self) -> str:
        """
        Title

           Title to be used for output header.  Default={prettyname}
        
        Returns:
        str:    Title           
        """
        if not self._title:
            self._title     = self._prettyname
        return self._title

    def logFile(self) -> str:
        """
        Log File 

            Log File Name

        Returns:
        none
        """
        if self._logFile is None:
            self._logFile   = 'osinfo-data-' + self._flavverflav + '.txt'

        return self._logFile

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

    def isOpenSuse(self) -> bool:
        """
        Is OpenSUSE

        Returns:
        bool:   isOpenSuse      (true/false)
        """
        return self._isOpenSuse

    def isRedhat(self) -> bool:
        """
        Is Redhat

        Returns:
        bool:   isRedhat       (true/false)
        """
        return self._isRedhat

    def isCentOS(self) -> bool:
        """
        Is CentOS

        Returns:
        bool:   isCentOS       (true/false)
        """
        return self._isCentOS

    #
    # Public Properties - Setters
    #
    def setTitle(self,title):
        """
        Set Title
        
        Returns:
        none
        """
        self._title     = title


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
       
        self._logInit()

        outfmt="{0:21} {1:30}"
        dashes=outfmt.format("-"*21,"-"*30)
        print("="*80)
        print('{}'.format(self._qnul(self.title())))
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
        print(outfmt.format("isOpenSuse",self._isOpenSuse))
        print(outfmt.format("isRedhat",self._isRedhat))
        print(outfmt.format("isCentOS",self._isCentOS))

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

        if self._isLinux:
            try:
                print('-- /etc/os-release --')
                releaseFile = '/etc/os-release'
                with open(releaseFile,'r') as fh:
                    for line in fh:
                        print(line.strip())
            except FileNotFoundError:
                print("Error: File '{0}' not found.".format(releaseFile))
            except IOError:
                print("Error: Could not open file '{0}'.".format(releaseFile))
