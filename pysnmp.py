import sys
print sys.version
from pysnmp.entity.rfc3413.oneliner import cmdgen
cg = cmdgen.CommandGenerator()