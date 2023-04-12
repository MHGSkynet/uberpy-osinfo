#	----------------------------------------------------------------------------------------------------------------------------
#	Ubergen Operating System Information Class Test Harness
#	----------------------------------------------------------------------------------------------------------------------------
#	Description:
#
#		Test harness to check OsInfo class operation.  Dumps all object properties, and debug data.
#
#	Copyrignt: (c) 2023, Kurt Schulte
#
#	History
#	---------- ----- -------------- --------------------------------------------------------------------------------------------
#	2023.04.12 01.00 KSchulte		Original Version
#	---------- ----- -------------- --------------------------------------------------------------------------------------------
#

from osinfo import *

osi = OsInfo()

osi.Dump()
osi.DumpDebugVars()

