#!/usr/bin/env python

try:
    from storm import ssh_config
except ImportError:
    raise ImportError("stormssh is not installed. you need to install it in order to use storm-indicator."
                      " try 'sudo pip install stormssh'.")

import gobject
import gtk
import appindicator
import getpass
import os
import sys


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
            self.run_program("gnome-terminal -e 'bash -c \"ssh %s; exec bash;\"'" % identifier)

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
        os.system(cmd)

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


if __name__ == '__main__':

    indicator = StormIndicator()
    indicator.add_menu_item('SSH Connections', sensitive=False)
    indicator.add_seperator()

    ssh_config = ssh_config.ConfigParser()

    for host_entry in ssh_config.load():

        if not host_entry.get("type") == 'entry' or host_entry.get("host") == '*':
            continue

        identifier = " {host} \n    {user}@{hostname}".format(
            user=host_entry.get("options", {}).get("user", getpass.getuser()),
            hostname=host_entry.get("options", {}).get("hostname"),
            host=host_entry.get("host"),
        )

        indicator.add_seperator()

        indicator.add_menu_item(
            identifier,
            host_entry.get("host"),
            sensitive=True
        )

    indicator.add_seperator()
    indicator.add_menu_item(
        'About',
        value='about',
        sensitive=True
    )

    indicator.add_seperator()
    indicator.add_menu_item(
        'Quit',
        value='quit',
        sensitive=True
    )

    indicator.run()