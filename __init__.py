"""
mycroft-hue : A Mycroft skill for controlling Phillips Hue

Copyright (C) 2016  Christopher Rogers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from os.path import dirname

import dbus
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'BugHunterPhilosopher'

LOGGER = getLogger(__name__)


class ClementinePlayerSkill(MycroftSkill):

    def __init__(self):
        super(ClementinePlayerSkill, self).__init__(name="ClementinePlayerSkill")

        self.player = dbus.SessionBus().get_object('org.mpris.MediaPlayer2.clementine', '/org/mpris/MediaPlayer2')

    def initialize(self):
        self.load_data_files(dirname(__file__))

        play_intent = IntentBuilder("ClementinePlayerPlayIntent").require("Play").build()
        self.register_intent(play_intent, self.handle_play_intent)

        pause_intent = IntentBuilder("ClementinePlayerPauseIntent").require("Pause").build()
        self.register_intent(pause_intent, self.handle_pause_intent)

        stop_intent = IntentBuilder("ClementinePlayerStopIntent").require("Stop").build()
        self.register_intent(stop_intent, self.handle_stop_intent)

        previous_intent = IntentBuilder("ClementinePlayerPreviousIntent").require("Previous").build()
        self.register_intent(previous_intent, self.handle_previous_intent)

        next_intent = IntentBuilder("ClementinePlayerNextIntent").require("Next").build()
        self.register_intent(next_intent, self.handle_next_intent)

        vol_plus_intent = IntentBuilder("ClementinePlayerVolPlusIntent").require("VolPlus").build()
        self.register_intent(vol_plus_intent, self.handle_vol_plus_intent)

        vol_minus_intent = IntentBuilder("ClementinePlayerVolMinusIntent").require("VolMinus").build()
        self.register_intent(vol_minus_intent, self.handle_vol_minus_intent)

    def handle_play_intent(self):
        self.player.Play()

    def handle_pause_intent(self):
        self.player.Pause()

    def handle_stop_intent(self):
        self.player.Stop()

    def handle_previous_intent(self):
        self.player.Prev()

    def handle_next_intent(self):
        self.player.Next()

    def handle_vol_plus_intent(self):
        volume = self.player.Get('org.mpris.MediaPlayer2.Player', 'Volume',
                           dbus_interface='org.freedesktop.DBus.Properties')
        property_interface = dbus.Interface(self.player, dbus_interface='org.freedesktop.DBus.Properties')
        property_interface.Set('org.mpris.MediaPlayer2.Player', 'Volume', volume + 0.2)

    def handle_vol_minus_intent(self):
        volume = self.player.Get('org.mpris.MediaPlayer2.Player', 'Volume',
                           dbus_interface='org.freedesktop.DBus.Properties')
        property_interface = dbus.Interface(self.player, dbus_interface='org.freedesktop.DBus.Properties')
        property_interface.Set('org.mpris.MediaPlayer2.Player', 'Volume', volume - 0.2)

    def stop(self):
        pass


def create_skill():
    return ClementinePlayerSkill()
