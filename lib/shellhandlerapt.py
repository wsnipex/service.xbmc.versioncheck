# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import xbmc
try:
    from subprocess import check_output
    from subprocess import call
    print "shellhandler initialised"
except:
    log('python apt import error')
    


def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % ("XBMC Version Check", txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

class ShellHandlerApt:

    _pwd = ""

    def __init__(self, usesudo=False):
        self.sudo = usesudo
        

    def check_version(self, package):
        _cmd = "apt-cache policy " + package

        if not self._update_cache():
            return False, False

        try:
            if self.sudo:
                result = check_output('echo \'%s\' | sudo -S %s' %(self._getpassword(), _cmd), shell=True).split("\n")
            else:
                result = check_output([_cmd], shell=True).split("\n")
        except Exception as error:
            log("ShellHandlerApt: exception while executing shell command %s: %s" %(_cmd, error))
            return False, False

        if result[0].replace(":", "") == package:
            installed = result[1].split()[1]
            candidate = result[2].split()[1]
            return installed, candidate
        else:
            log("ShellHandlerApt: error during version check")
            return False, False

    def _update_cache(self):
        _cmd = 'apt-get update'
        try:
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' %(self._getpassword(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error))
            return False

        return True

    def upgrade_package(self, package):
        _cmd = "apt-get install -y " + package
        try:
            if self.sudo:
                x = check_output('echo \'%s\' | sudo -S %s' %(self._getpassword(), _cmd), shell=True)
            else:
                x = check_output(_cmd.split())
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error))
            return False

        return True

    def update_system(self):
        _cmd = "apt-get upgrade -y"
        try:
            if self.sudo:
                return check_output('echo \'%s\' | sudo -S %s' %(pwd, cmd), shell=True)
            else:
                return check_output(cmd.split())
        except Exception as error:
            log("Exception while executing shell command %s: %s" %(_cmd, error))
            return False
        return result

    def _getpassword(self):
        if len(self._pwd) == 0:
            #keyboard = xbmc.Keyboard(__localize__(32022), "", True)
            keyboard = xbmc.Keyboard("", "XBMC Version Check, please enter your password", True)
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                self._pwd = keyboard.getText()
        return self._pwd