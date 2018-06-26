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

    # Clementine lives on the Session bus
    session_bus = dbus.SessionBus()

    # Get Clementine's player object, and then get an interface from that object,
    # otherwise we'd have to type out the full interface name on every method call.
    player = session_bus.get_object('org.mpris.clementine', '/Player')
    self.iface = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')

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
    self.iface.Play()

  def handle_pause_intent(self):
    self.iface.Pause()

  def handle_stop_intent(self):
    self.iface.Stop()

  def handle_previous_intent(self):
    self.iface.Prev()

  def handle_next_intent(self):
    self.iface.Next()

  def handle_vol_plus_intent(self):
    volume = self.iface.Get('org.freedesktop.MediaPlayer', 'Volume')
    print(volume)
    self.iface.Set('org.freedesktop.MediaPlayer', 'Volume', volume + 0.2)

  def handle_vol_minus_intent(self):
    volume = self.iface.Get('org.freedesktop.MediaPlayer', 'Volume')
    print(volume)
    self.iface.Set('org.freedesktop.MediaPlayer', 'Volume', volume - 0.2)

  def stop(self):
    pass


def create_skill():
  return ClementinePlayerSkill()
