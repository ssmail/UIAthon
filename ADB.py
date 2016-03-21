__author__ = 'Chris'

import os
import re
import subprocess
import platform
from time import sleep

DEBUG = False



class ADB:

    def __init__(self, device_id = ""):
        if device_id:
            self.device_id = "-s {device_id}".format(device_id= device_id)
        else:
            self.device_id = " "

    def adb(self, cmd):
        cmd = 'adb {device_id} {cmd}'.format(device_id = self.device_id, cmd=cmd)
        if DEBUG:
            print cmd
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def shell(self, cmd):
        cmd = 'adb {device_id} shell {cmd}'.format(device_id = self.device_id, cmd=cmd)
        if DEBUG:
            print cmd
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def press(self, key_code):
        pass


    def get_device_status(self):
        return self.adb("get-state").stdout.read().strip()


    def swipeByRatio(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, duration=" "):
        self.shell("input swipe %s %s %s %s %s" % (str(start_ratioWidth * self.getScreenResolution()[0]), str(start_ratioHigh * self.getScreenResolution()[1]), \
                                             str(end_ratioWidth * self.getScreenResolution()[0]), str(end_ratioHigh * self.getScreenResolution()[1]), str(duration)))
        sleep(0.5)


    def getScreenResolution(self):
        pattern = re.compile(r"\d+")
        out = self.shell("dumpsys display | grep PhysicalDisplayInfo").stdout.read()
        display = pattern.findall(out)
        print display
        return (int(display[0]), int(display[1]))


    def swipeToDown(self):
        #swipe to down
        self.swipeByRatio(0.5, 0.2, 0.5, 0.8)


    def swipeToUp(self):
        #swipe to up
        self.swipeByRatio(0.5, 0.8, 0.5, 0.2)


    def swipeToRight(self):
        # swipe to right
        self.swipeByRatio(0.2, 0.5, 0.8, 0.5)


    def swipeToLeft(self):
        # swipe to left
        self.swipeByRatio(0.8, 0.5, 0.2, 0.5)


    def longPressKey(self, keycode):
        self.shell("input keyevent --longpress %s" % str(keycode))
        sleep(0.5)


    def sendKeyEvent(self, keycode):
        self.shell("input keyevent %s" % str(keycode))
        sleep(0.5)


    def startActivity(self, component):
        self.shell("am start -n %s" % component)


    def clearAppData(self, packageName):
        if "Success" in self.shell("pm clear %s" % packageName).stdout.read().splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"


    def removeApp(self, packageName):
        self.adb("uninstall %s" % packageName)


    def isInstall(self, packageName):

        if self.getMatchingAppList(packageName):
            return True
        else:
            return False


    def installApp(self, appFile):
        self.adb("install %s" % appFile)


    def getAppStartTotalTime(self, component):
        time = self.shell("am start -W %s | grep TotalTime" % (component)) \
            .stdout.read().split(": ")[-1]
        return int(time)


    def getMatchingAppList(self, keyword):
        matApp = []
        for packages in self.shell("pm list packages %s" % keyword).stdout.readlines():
            matApp.append(packages.split(":")[-1].splitlines()[0])

        return matApp


    def getThirdAppList(self):
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.split(":")[-1].splitlines()[0])

        return thirdApp


    def getSystemAppList(self):
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.split(":")[-1].splitlines()[0])

        return sysApp


    def reboot(self):
        self.adb("reboot")


    def getBatteryTemp(self):
        temp = self.shell("dumpsys battery | grep temperature").stdout.read().split(": ")[-1]
        return int(temp) / 10.0


    def getBatteryLevel(self):
        level = self.shell("dumpsys battery | grep level").stdout.read().split(": ")[-1]
        return int(level)


    def getCurrentActivity(self):
        return self.getFocusedPackageAndActivity().split("/")[-1]


    def getCurrentPackageName(self):
        return self.getFocusedPackageAndActivity().split("/")[0]


    def getFocusedPackageAndActivity(self):
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.shell("dumpsys window w | grep \/ | grep name=").stdout.read()

        return pattern.findall(out)[0]

    def quitApp(self, packageName):
        self.shell("am force-stop %s" % packageName)

    def killProcess(self, pid):
        if self.shell("kill %s" % str(pid)).stdout.read().split(": ")[-1] == "":
            return "kill success"
        else:
            return self.shell("kill %s" % str(pid)).stdout.read().split(": ")[-1]

    def getPid(self, packageName):
        system = platform.system()

        if system is "Windows":
            pidinfo = self.shell("ps | findstr %s$" % packageName).stdout.read()
        else:
            pidinfo = self.shell("ps | grep -w %s" % packageName).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return  pattern.findall(" ".join(result))[0]


    def getDeviceModel(self):
        return self.shell("getprop ro.product.model").stdout.read().strip()


    def getDeviceState(self):
        return self.adb("get-state").stdout.read().strip()


    def getDeviceID(self):
        return self.adb("get-serialno").stdout.read().strip()


    def getAndroidVersion(self):
        return self.shell("getprop ro.build.version.release").stdout.read().strip()


    def getSdkVersion(self):
        return self.shell("getprop ro.build.version.sdk").stdout.read().strip()

    def sendText(self, string):

        text = str(string).split(" ")
        out = []
        for i in text:
            if i != "":
                out.append(i)
        length = len(out)

        for i in xrange(length):
            self.shell("input text %s" % out[i])
            if i != length - 1:
                self.sendKeyEvent(KeyCode.SPACE)
        sleep(0.5)


class KeyCode:

    POWER = 26
    BACK = 4
    HOME = 3
    MENU = 82
    VOLUME_UP= 24
    VOLUME_DOWN = 25
    SPACE = 62
    BACKSPACE = 67
    ENTER = 66
    MOVE_HOME = 122
    MOVE_END = 123
