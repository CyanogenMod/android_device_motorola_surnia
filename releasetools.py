# Copyright (C) 2016 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

def FullOTA_Assertions(info):
  AddRadioAssertion(info, info.input_zip)


def IncrementalOTA_Assertions(info):
  AddRadioAssertion(info, info.input_zip)


def AddRadioAssertion(info, input_zip):
  android_info = input_zip.read("OTA/android-info.txt")
  m = re.search(r"require\s+version-radio\s*=\s*(\S+)", android_info)
  if m:
    radios = m.group(1).split("|")
    cmd = ("assert(" +
           " || ".join(['getprop("ro.boot.radio") == "%s"' % (r,)
                         for r in radios]) +
           ' || abort("CDMA devices are not currently supported.");' +
           ");")
    info.script.AppendExtra(info.script.WordWrap(cmd))
