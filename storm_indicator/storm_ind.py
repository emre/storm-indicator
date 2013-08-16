
import gobject
import gtk
import appindicator
import os
import sys

from subprocess import Popen

class StormIndicator(object):

    def __init__(self):

        self.app = appindicator.Indicator(
            "storm-ssh-indicator",
            "gnome-netstatus-tx",
            appindicator.CATEGORY_APPLICATION_STATUS
        )

        self.app.set_status(appindicator.STATUS_ACTIVE)

        self.menu = gtk.Menu()

    def menu_item_callback(self, w, identifier):
        if identifier == 'about':
            self.pop_dialog("storm-indicator is a helper for connecting to your servers easily."
                            "\n\nyou can use the <a href='https://github.com/emre/storm-indicator/issues'>issue"
                            "tracker</a> for bug reports and feature requests")

        elif identifier == 'quit':
            sys.exit(0)
        else:
            self.run_program(["gnome-terminal", "-e", "bash -c \"ssh %s; exec bash;\"" % identifier])

    def add_menu_item(self, text, value=None, sensitive=True):
        menu_item = gtk.MenuItem(text)
        menu_item.set_sensitive(sensitive)
        menu_item.show()

        if sensitive:
            menu_item.connect("activate", self.menu_item_callback, value)

        self.menu.append(menu_item)

    def add_seperator(self):
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

    def run(self):
        self.app.set_menu(self.menu)
        gtk.main()

    def run_program(self, cmd):
        Popen(cmd)

    def pop_dialog(self, message, error=False):
        if error:
            icon = gtk.MESSAGE_ERROR
        else:
            icon = gtk.MESSAGE_INFO
        md = gtk.MessageDialog(None, 0, icon, gtk.BUTTONS_OK)
        try:
            md.set_markup("<b>storm-indicator</b>")
            md.format_secondary_markup(message)
            md.run()
        finally:
            md.destroy()
