"""
Problem Description

Scale Down

Imagine you are given a stream of data points consisting of <timestamp, commodityPrice> you are supposed to return the maxCommodityPrice at any point in time.
The timestamps in the stream can be out of order, or there can be duplicate timestamps, we need to update the commodityPrice at that particular timestamp if an entry for the timestamp already exists.
Create an in-memory solution tailored to prioritize frequent reads and writes for the given problem statement.
RunningCommodityPrice r = new RunningCommodityPrice();
r.upsertCommodityPrice(4, 27);
r.upsertCommodityPrice(6, 26);
r.upsertCommodityPrice(9, 25);
r.getMaxCommodityPrice();         // output should be 27 which is at timestamp 4
r.upsertCommodityPrice(4, 28);    // timestamps can come out of order and there can be duplicates
// the commodity price at timestamp 4 got updated to 28, so the max commodity price is 28
r.getMaxCommodityPrice();

Restriction:
+ timestamp and price are positive integers.
+ when prices are tied, data entry with bigger timestamp should return for the Max method


Extra:
+ Implement Deletion

"""

# from heapq import heappush_max, heappop_max
import heapq

class CommodityPrice:
    def __init__(self, timestamp: int, price: int):
        self.timestamp = timestamp
        self.price = price

    def __repr__(self):
        return "timesamp, price: ({}, {})".format(self.timestamp, self.price)
    
    def __lt__(self, other):
        if not isinstance(other, CommodityPrice):
            return NotImplemented
        if other.price != self.price:
            return self.price < other.price
        # when price are the same, compare timestamp instead
        return self.timestamp < other.timestamp

    def __neg__(self):
        # for heap operations (only minheap operations before Python 3.14)
        return CommodityPrice(-self.timestamp, -self.price)


class RunningCommodityPrice:

    DELETED = "DELETED"

    def __init__(self):
        self.ts_to_prices = {}
        self.current_max_cp = CommodityPrice(-1, -1)
        
        # max heap
        self.maxheap_prices = []
        self.total = 0
        self.to_delete = 0

        
    def upsertCommodityPrice(self, ts: int, price: int):
        
        cp = CommodityPrice(ts, price)

        # upsert
        if ts not in self.ts_to_prices:
            self.total += 1
        self.ts_to_prices[ts] = cp
        heapq.heappush(self.maxheap_prices, -cp)
        
        # single max tracking, when no deletion
        if not len(self.ts_to_prices) or cp > self.current_max_cp:
            self.current_max_cp = cp

        
    def getMaxCommodityPrice(self):
        # Inefficient - sorting all values
        # sortedPrice = sorted(self.ts_to_prices.values())
        # maxCP = sortedPrice[-1]

        # retrieved the current max, tracked during upsert, O(1), when no deletion
        # maxCP = self.current_max_cp

        # empty queue
        if self.total == 0 or len(self.ts_to_prices) == 0:
            print('No values recorded!')
            return
        
        # when heap is instroduced, take the value from heap (no deletion)
        if self.to_delete == 0:
            negMaxCP = self.maxheap_prices[0]
            return -negMaxCP

        # when deletion in introduced, first handle deletion
        # heep could contain duplicated entries, we will delete them when encountered
        for i in range(len(self.maxheap_prices)):
            negMaxCP = self.maxheap_prices[0]
            ts = -negMaxCP.timestamp

            if ts not in self.ts_to_prices:
                # item in priority queue but already deleted, delete in priority queue
                heapq.heappop(self.maxheap_prices)
                continue

            if self.ts_to_prices[ts] == self.DELETED:
                self.ts_to_prices.pop(ts)
                self.to_delete -= 1
                heapq.heappop(self.maxheap_prices)

        maxCP = -self.maxheap_prices[0]
        
        return maxCP

    def deleteCommodityPrice(self, ts: int):

        # track deletions
        if ts not in self.ts_to_prices:
            # alert
            print('ts {} does not exist!'.format(ts))
            return
        if self.total == 0: 
            print('No more entries to delete!')
            return
        
        self.ts_to_prices[ts] = self.DELETED
        self.total -= 1
        self.to_delete += 1


r = RunningCommodityPrice()
r.upsertCommodityPrice(4, 27)
r.upsertCommodityPrice(6, 26)
r.upsertCommodityPrice(9, 25)
print(r.getMaxCommodityPrice())        # (4, 27)
r.upsertCommodityPrice(4, 28)
print(r.getMaxCommodityPrice())        # (4, 28)


r.upsertCommodityPrice(2, 28)
r.upsertCommodityPrice(5, 28)
r.upsertCommodityPrice(3, 28)
print(r.getMaxCommodityPrice())        # (5, 28)


r.upsertCommodityPrice(5, 29)   
print(r.getMaxCommodityPrice())         # (5, 29)

r.deleteCommodityPrice(5)
r.deleteCommodityPrice(4)
r.deleteCommodityPrice(2)
r.deleteCommodityPrice(3)
print(r.getMaxCommodityPrice())        # (6, 26)
r.deleteCommodityPrice(6)
print(r.getMaxCommodityPrice())        # (9, 25)
r.upsertCommodityPrice(5, 28)
print(r.getMaxCommodityPrice())        # (5, 28)
r.deleteCommodityPrice(5)
r.deleteCommodityPrice(9)
print(r.getMaxCommodityPrice())        # No avalues




