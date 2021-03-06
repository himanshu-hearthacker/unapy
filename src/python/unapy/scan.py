#! /usr/bin/env python
"""\
Scan for serial ports. Linux specific variant that also includes USB/Serial
adapters.

Part of pySerial (http://pyserial.sf.net)
(C) 2009 <cliechti@gmx.net>

Modified 2011 <bewest@gmail.com>
"""

import serial
import logging
import glob
import time
logger = logging.getLogger(__name__)

GLOB_PATTERNS = [ '/dev/tty.usb*', '/dev/ttyUSB*' ]

def scan():
    """scan for available ports. return a list of device names."""
    r = [ ]
    for pat in GLOB_PATTERNS:
      r.extend(glob.glob(pat))
    return r
    #return glob.glob('/dev/tty.usb*') + glob.glob('/dev/ttyUSB*')

def usable_response(lines):
  logger.debug(lines)
  for l in lines:
    if 'OK' == l.strip():
      return True
  return False

def link_usable(candidate):
  usable = False
  try:
    logger.info("attempting to open %s" % candidate)
    port = serial.Serial(candidate, timeout=3)
    for i in xrange(3):
      port.write("AT\r")
      time.sleep(.20)
      if usable_response(port.readlines()):
        usable = True
        logger.debug("%s looks usable." % candidate)
        break
    port.close()
  except serial.SerialException: pass

  return usable

class ScanAttachedDevicesError(Exception): pass
  
def best_guess():
  """Take a guess at finding a usable device.
  """
  try:
    return filter(link_usable, scan( ))[0]
  except IndexError, e:
    raise ScanAttachedDevicesError("""couldn't find a device that works.
    scanned: {globs}""".format(globs=GLOB_PATTERNS))

if __name__=='__main__':
    print "Found ports:"
    for name in scan():
        print name

#####
# EOF
