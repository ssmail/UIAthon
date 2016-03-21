#coding=utf-8
__author__ = 'Chris'

import os
import re
import ADB
import sys
reload(sys)
from time import sleep
import xml.etree.cElementTree as ET
sys.setdefaultencoding('utf-8')


class UIAthon:

    def __init__(self):
        self.adb = ADB.ADB()
        pass

    def findElement(self, target):

        uidump_file = os.path.join(os.getcwd(), 'uidump.xml')

        self.dump_uixml()
        if not os.path.exists(uidump_file):
            print 'uidump xml file not found'
            exit()

        root = ET.parse(uidump_file)
        node = root.getiterator('node')

        for element in node:
            for control in element:
                class_name = control.attrib['class']
                index = control.attrib['index']
                resource = control.attrib['resource-id']
                package = control.attrib['package']
                content = control.attrib['content-desc']
                checkable = control.attrib['checkable']
                checked = control.attrib['checked']
                clickable = control.attrib['clickable']
                enabled = control.attrib['enabled']
                focusable = control.attrib['focusable']
                focused = control.attrib['focused']
                scrollable = control.attrib['scrollable']
                long = control.attrib['long-clickable']
                password = control.attrib['password']
                selected = control.attrib['selected']
                bounds = control.attrib['bounds']
                text = control.attrib['text']

                tmpLocation = re.findall('\[(\d+),(\d+)\]', bounds)

                xPoint = (int(tmpLocation[1][0]) - int(tmpLocation[0][0]))/2 + int(tmpLocation[0][0])
                yPoint = (int(tmpLocation[1][1]) - int(tmpLocation[0][1]))/2 + int(tmpLocation[0][1])

                bounds = [xPoint, yPoint]

                property = ""

                print "resource: ", resource

                if text.strip() == target:
                    property = text.strip()
                elif content.strip() == target:
                    property = content.strip()
                elif resource == target:
                    property = resource

                # if type == 'text':
                #     property = text.strip()
                # elif type == 'desc':
                #     property = content.strip()
                # else:
                #     print 'error control type'
                #     return None

                try:
                    if property == target:
                        element = Element(text, index, resource, class_name, package, content,checked,bounds)
                        return element
                except Exception,e:
                    print e
                    return None

    def findElementinHorizontal(self, target, times):
        for i in range(0, 1):
            self.adb.swipeToDown()

        for i in range(0, times):
            result = self.findElement(target)
            if result:
                return result
            self.adb.swipeToUp()


    def findElementinVertical(self, target, times):
        for i in range(0, 1):
            self.adb.swipeToRight()

        for i in range(0, times):
            result = self.findElement(target)
            if result:
                return result
            self.adb.swipeToLeft()


    def enumAllElement(self):

        uidump_file = os.path.join(os.getcwd(), 'uidump.xml')

        self.dump_uixml()
        if not os.path.exists(uidump_file):
            print 'uidump xml file not found'
            exit()

        root = ET.parse(uidump_file)
        node = root.getiterator('node')

        tree_list = []

        for element in node:
            for control in element:
                class_name = control.attrib['class']
                index = control.attrib['index']
                resource = control.attrib['resource-id']
                package = control.attrib['package']
                content = control.attrib['content-desc']
                checkable = control.attrib['checkable']
                checked = control.attrib['checked']
                clickable = control.attrib['clickable']
                enabled = control.attrib['enabled']
                focusable = control.attrib['focusable']
                focused = control.attrib['focused']
                scrollable = control.attrib['scrollable']
                long = control.attrib['long-clickable']
                password = control.attrib['password']
                selected = control.attrib['selected']
                bounds = control.attrib['bounds']
                text = control.attrib['text']

                tmpLocation = re.findall('\[(\d+),(\d+)\]', bounds)

                xPoint = (int(tmpLocation[1][0]) - int(tmpLocation[0][0]))/2 + int(tmpLocation[0][0])
                yPoint = (int(tmpLocation[1][1]) - int(tmpLocation[0][1]))/2 + int(tmpLocation[0][1])

                bounds = [xPoint, yPoint]

                if text or content or resource:
                    element = Element(text, index, resource, class_name, package, content,checked,bounds)
                    tree_list.append(element)

        return tree_list

    def dump_uixml(self):
        pattern = re.compile(r"\d+")
        os.system('adb shell rm /data/local/tmp/uidump.xml')
        os.system('adb shell uiautomator dump /data/local/tmp/uidump.xml')
        os.system('adb pull /data/local/tmp/uidump.xml')


class Element:

    def __init__(self, text, index, resource, classname, package, desc, checked, bound):
        self.text = text
        self.index = index
        self.resource = resource
        self.classname = classname
        self.package = package
        self.desc = desc
        self.checked = checked
        self.bound = bound

    def click(self):
        os.system('adb shell input tap ' + str(self.bound[0]) + " " + str(str(self.bound[1])))



# initialization the UIA Object
myUIA = UIAthon()

# find the object in vertical space
app = myUIA.findElementinVertical("口袋购物", 3)

# find it, click it
if app:
    app.click()
else:
    print 'can not find the  object'
