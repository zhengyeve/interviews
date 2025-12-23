"""
Challenge: The question will ask you to extract specific insights from a dataset of events
for a business that operates multiple yards that provide parking spaces for trailers.
The event data will be provided at the start of the interview in a JSON file.  


Part Zero: 
Write a date time parse function
https://batonio.notion.site/Trailer-Yard-Invoicing-Part-Zero-cfc5c76cc7864697ad1b2638b054a9aa

Part One: 
Write a function that takes the trailer events, a date, and a facility ID, 
and returns all trailer events for trailers that were at the given facility on the given date.
https://batonio.notion.site/Trailer-Yard-Invoicing-Part-One-5ada0a1106c748fdba9898f997e35ea6

Part Two: 
Write a function that takes a list of all of a customer’s trailer events, a facility ID, and a date,
and returns the peak occupancy for the given facility on the given date.
https://batonio.notion.site/Trailer-Yard-Invoicing-Part-Two-69d70f492b5b4ae68d42435b2878dd56


"""

import json
from datetime import datetime

FILENAME = 'events.json'
# arr = json.load(fh)
# print(arr[0])


def parse_dt(dtstr):
    # "2022-03-25 07:00:00"
    # print(dtstr)
    if dtstr is None:
        return None
    return datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')

def deserializeDatetime(filename):
    fh = open(filename)
    arr = json.load(fh)


    formattedArray = []
    for entry in arr:
        # time handling 
        entry["entrance_time"] = parse_dt(entry["entrance_time"])
        entry["exit_time"] = parse_dt(entry["exit_time"])
        formattedArray.append(entry)

    return formattedArray



def trailerAtFacility(date_str, event):
    """
    Docstring for trailerAtFacility
    
    :param date_str: Description
    :param event: Description
    # date_str e.g. "2022-03-26"
    # e.g. event 
    {
        "id": 57185,
        "trailer_id": 15114,
        "facility_id": 319,
        "entrance_time": datetime obj of "2022-03-26 19:04:54",
        "exit_time": null
    }
    return bool
    """

    date_start = parse_dt('{} 00:00:00'.format(date_str))
    date_end = parse_dt('{} 23:59:59'.format(date_str))

    enter_time = event["entrance_time"]
    exit_time = event["exit_time"]
    
    # exit time is null
    if exit_time is None:
        return enter_time < date_end
    return (enter_time < date_start and exit_time > date_start) or \
        (date_start <= enter_time < date_end)


def allTrailerEvents(date_str, facility_id, events_arr):
    # date_str: %Y-%m-%d
    # facility_id: int
    # events_arr: parsed JSON array [...]

    res = []
    for entry in events_arr:
        if entry["facility_id"] != facility_id:
            continue

        # date time computation
        if trailerAtFacility(date_str, entry):
            res.append(entry)
    return res


def getPeakOccupancy(date_str, facility_id, events_arr):
    """
    Docstring for getPeakOccupancy
    
    :param date_str: Description
    :param facility_id: Description
    :param events_arr: Description
    """
    max_occupancy = 0
    occupancy = 0
    counts = []

    day_events = allTrailerEvents(date_str, facility_id, events_arr)
    for entry in day_events:
        enter_time = entry["entrance_time"]
        exit_time = entry["exit_time"]
        counts.append((enter_time, 1))
        if exit_time:
            counts.append((exit_time, -1))

    counts.sort()
    # print(counts)

    ts_next = parse_dt('{} 23:59:59'.format(date_str))
    for i in range(len(counts)):
        # time = cnt[0]
        if i < len(counts)-1:
            ts_next, _ = counts[i+1]
        ts, increment = counts[i]
        occupancy += increment
        
        if occupancy > max_occupancy:
            max_occupancy = occupancy                
            window = '{} - {}'.format(ts, ts_next)

        
    return max_occupancy, window



from pprint import pprint

arr = deserializeDatetime(FILENAME)
day_events = allTrailerEvents("2022-01-18", 1, arr)
print(getPeakOccupancy("2022-01-18", 1, arr))

# pprint(deserializeDatetime(FILENAME)[:10])