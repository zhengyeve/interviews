""" F1 lap hero

Atlassian is the name partner of Atlassian Williams Racing.

Design and implement a program that accepts lap times for Formula 1 race drivers. 
Return the "Last Lap Hero" - the driver who had the biggest improvement on their last lap compared to their average lap time. 

Driver, Lap Time
"Driver1", 100
"Driver2", 90
"Driver3", 70
"Driver1", 110
"Driver2", 95
"Driver3", 50
// Driver 1 Last Lap Gain = 110 - (100+110)/2 = 5
// Driver 2 Last Lap Gain = 95 - (90+95)/2 = 2.5
// Driver 3 Last Lap Gain = 50 - (70+50)/2 = -10
// Driver 3 is last lap hero

Restrictions
+ Lap time is going to be a positive integer
+ Data entry can be very big
+ expect each entry to be added once by a method, and the lap hero call can be called anytime during data entry insert


Extra Questions:
+ Space complexity, Time complexity, Optimization
+ How to implement a telemetry system from here
"""

class LapHeroCalculator:

    def __init__(self):
        pass

    def upsertLapTime(self, driver: str, laptime: int):
        pass

    def getLastLapHero(self):
        pass