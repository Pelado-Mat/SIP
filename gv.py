# !/usr/bin/python
# -*- coding: utf-8 -*-

import time
from calendar import timegm
from helpers import password_salt

#####################
#### Global vars ####
#####################

##############################
#### Revision information ####

major_ver = 3
minor_ver = 2
old_count = 0
ver_str = ''
ver_date = ''
revision = ''



# Settings Dictionary. A set of vars kept in memory and persisted in a file.
# Edit this default dictionary definition to add or remove "key": "value" pairs or change defaults.
# note old passwords stored in the "pwd" option will be lost - reverts to default password.

sd = {
    u"en": 1,
    u"seq": 1,
    u"ir": [0],
    u"iw": [0],
    u"rsn": 0,
    u"htp": 8080,
    u"rdst": 0,
    u"loc": u"",
    u"tz": 48,
    u"tf": 1,
    u"rs": 0,
    u"rd": 0,
    u"mton": 0,
    u"lr": 100,
    u"sdt": 0,
    u"mas": 0,
    u"wl": 100,
    u"bsy": 0,
    u"lg": u"",
    u"urs": 0,
    u"nopts": 13,
    u"pwd": u"b3BlbmRvb3I=",
    u"password": u"",
    u"ipas": 0,
    u"rst": 1,
    u"mm": 0,
    u"mo": [0],
    u"rbt": 0,
    u"mtoff": 0,
    u"nprogs": 1,
    u"tu": u"C",
    u"snlen": 32,
    u"name": u"SIP",
    u"theme": u"basic",
    u"show": [255],
    u"salt": password_salt(),
    u"lang": u"default",
    u"controlName": u"relayBoard",
    u"nbrd" : 1, # FIXME! must be replaced with the proper call to ControlPlugin
    u'nst' : 8
}


platform = '' # 'pi' | 'bo'

use_pigpio = False # Boolean

scontrol = None #Place holder for the Station Control Module

nowt = time.localtime()
now = timegm(nowt)
tz_offset = int(time.time() - timegm(time.localtime())) # compatible with Javascript (negative tz shown as positive value)
plugin_menu = []  # Empty list of lists for plugin links (e.g. ['name', 'URL'])

srvals = [0]   # Shift Register values

rovals = [0]   # Run Once durations
snames = [0]  # Load station names from file
pd = [0]  # Load program data from file
plugin_data = {}  # Empty dictionary to hold plugin based global data
ps = []  # Program schedule (used for UI display)
pon = None  # Program on (Holds program number of a running program)
sbits = [0]   # Used to display stations that are on in UI

rs = []  # run schedule
lrun = [0, 0, 0, 0]  # station index, program number, duration, end time (Used in UI)
scount = 0  # Station count, used in set station to track on stations with master association.


options = [
    [_("System name"), "string", "name", _("Unique name of this SIP system."), _("System")],
    [_("Location"), "string", "loc", _("City name or zip code. Use comma or + in place of space."), _("System")],
    [_("Language"),"list","lang", _("Select language."),_("System")],
#    [_("Time zone"), "int", "tz", _("Example: GMT-4:00, GMT+5:30 (effective after reboot.)"), _("System")],
    [_("24-hour clock"), "boolean", "tf", _("Display times in 24 hour format (as opposed to AM/PM style.)"), _("System")],
    [_("HTTP port"), "int", "htp", _("HTTP port."), _("System")],
    [_("Water Scaling"), "int", "wl", _("Water scaling (as %), between 0 and 100."), _("System")],
    [_("Disable security"), "boolean", "ipas", _("Allow anonymous users to access the system without a password."), _("Change Password")],
    [_("Current password"), "password", "opw", _("Re-enter the current password."), _("Change Password")],
    [_("New password"), "password", "npw", _("Enter a new password."), _("Change Password")],
    [_("Confirm password"), "password", "cpw", _("Confirm the new password."), _("Change Password")],
    [_("Sequential"), "boolean", "seq", _("Sequential or concurrent running mode."), _("Station Handling")],
    [_("Extension boards"), "int", "nbrd", _("Number of extension boards."), _("Station Handling")],
    [_("Station delay"), "int", "sdt", _("Station delay time (in seconds), between 0 and 240."), _("Station Handling")],
    [_("Master station"), "int", "mas",_( "Select master station."), _("Configure Master")],
    [_("Master on adjust"), "int", "mton", _("Master on delay (in seconds), between +0 and +60."), _("Configure Master")],
    [_("Master off adjust"), "int", "mtoff", _("Master off delay (in seconds), between -60 and +60."), _("Configure Master")],
    [_("Use rain sensor"), "boolean", "urs", _("Use rain sensor."), _("Rain Sensor")],
    [_("Normally open"), "boolean", "rst", _("Rain sensor type."), _("Rain Sensor")],
    [_("Enable logging"), "boolean", "lg", _("Log all events - note that repetitive writing to an SD card can shorten its lifespan."), _("Logging")],
    [_("Max log entries"), "int", "lr", _("Length of log to keep, 0=no limits."), _("Logging")]
]

