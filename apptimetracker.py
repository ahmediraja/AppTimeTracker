from __future__ import print_function
import time
from os import system
from activity import *
import json
import datetime
from subprocess import call
import sys

if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    # macOS specific
    from AppKit import NSWorkspace
    from Foundation import *

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = ActivityList([])
first_time = True

# function to convert a long url into just the domain name (i.e. youtube.com)
def url_to_domain_name(url):
    string_list = url.split('/')
    return string_list[2]

# function to get the window that is currently active
def get_active_window():
    _active_window_name = None
    if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        _active_window_name = (NSWorkspace.sharedWorkspace()
                               .activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name

# function to get the current chrome tab that is active
def get_chrome_url():
    if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        textOfMyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
        s = NSAppleScript.initWithSource_(
            NSAppleScript.alloc(), textOfMyScript)
        results, err = s.executeAndReturnError_(None)
        return results.stringValue()
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name

try:
    activeList.initialize_me()
except Exception:
    print('No json')


try:
    while True:
        #tracking tab
        previous_site = ""
        if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            new_window_name = get_active_window()
            if 'Google Chrome' in new_window_name:
                new_window_name = url_to_domain_name(get_chrome_url()) #only show domain of a chrome tab
        
        if active_window_name != new_window_name:
            print(active_window_name)
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)

                if not exists:
                    activity = Activity(activity_name, [time_entry])
                    activeList.activities.append(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name
        
        # DOES NOT WORK -- JUST TESTING SOMETHING -- IGNORE THIS
        # #update firebase daily
        # yesterday = datetime.date.today() - datetime.timedelta(days = 1)
        # if datetime.date.today() != yesterday:
        #     yesterday = datetime.date.today
        #     call(['node', 'import.js'])

        time.sleep(1)
    
except KeyboardInterrupt:
    with open('activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
