#!/usr/bin/env python2
#
#   Copyright 2013 Science & Technology Facilities Council
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import inspect

import sys

import pygtk, gtk, gobject, urllib2, webkit

VERSION = "1.0"

class WebPresenter(object):

  def __init__(self, list_filename, timer_delay):
    #Load pagelist
    try:
      self.page_list = open(list_filename, "r").readlines()
    except Exception as e:
      sys.exit("ERROR: Unable to open file \"%s\". %s" % (list_filename, e))

    self.page_count = len(self.page_list)
    #Setup Image
    self.page = gtk.Image()
    self.page.show()

    #Setup Window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.connect("delete_event", self.close_application)
    self.window.connect("key_press_event", self.close_application)
    self.window.connect("realize", self.realize)
    self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000"))
    self.view = webkit.WebView()
    self.window.add(self.view)
    self.window.fullscreen()
    self.window.show_all()

    #Display immediately and set up a timer to display every n seconds
    self.page_index = -1
    self.display_next_page()
    self.timer = gobject.timeout_add(int(timer_delay * 1000), self.display_next_page)

    #Start main event loop
    gtk.main()


  def realize(self, widget):
    #Make cursor invisible
    pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
    color = gtk.gdk.Color()
    cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
    widget.window.set_cursor(cursor)


  def close_application(self, widget, event, data=None):
    #Only exit if window is closed or Escape key is pressed
    if event.type == gtk.gdk.KEY_PRESS and gtk.gdk.keyval_name(event.keyval) != "Escape":
      self.display_next_page()
      return True
    else:
      gtk.main_quit()
      return False


  def display_next_page(self):
    #Move to next !mage
    self.page_index += 1

    #If we've displayed all the pages, go back to the start
    if self.page_index == self.page_count:
      self.page_index = 0

    #Get page data
    location = self.page_list[self.page_index]

    try:
      self.view.open(location)

    except Exception as e:
      print("Something's not right about \"%s\", it caused the exception \"%s\"" % (location, e))

    #Continue to generate timer events
    return True


#It's alive!
if __name__ == "__main__":
  from optparse import OptionParser

  p = OptionParser(version=VERSION)

  p.add_option("-f", dest="filename", type="string", help="read page list from FILENAME rather than pages.list", default="pages.list")
  p.add_option("-d", dest="delay",    type="float",  help="delay in seconds between displayed pages",             default=10)

  (o, a) = p.parse_args()

  #Create Presenter
  WebPresenter(o.filename, o.delay)
