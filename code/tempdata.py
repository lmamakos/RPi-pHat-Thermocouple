# -*- coding: UTF-8 -*-
# Keeps a moving average of Temperature Sensor data
#
# Copyright (c) 2019 Mike Lawrence
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import logging
# logging.basicConfig(format='Fridge Monitor: %(message)s', level=logging.DEBUG)

# logger for this module
#logger = logging.getLogger(__name__)

class TempData:
    def __init__(self, maxlength = 10, name = ""):
        """Keep track of temperature sensor data over time and average."""
        # save maximum number of data points to store
        if maxlength == None:
            # default length is 10
            self._maxlength = 10
        else:
            self._maxlength = maxlength
        # local copy of sensor name
        self._name = name
        # create empty list for incoming data
        self._data = []
        self._count = 0

    def append(self, temp):
        """Add temperature sample to data store."""
        if temp:
            if temp != float("NaN"):
                # add data to the left side of the list (newest side)
                self._data.insert(0, temp)
                self._count += 1
                # prevent list from exceed maxlength
                # if maxlength is 0 then number fo samples stored will 
                #   never be truncated
                if self._maxlength > 0 and len(self._data) > self._maxlength:
                    # pop the data from the right side of list (oldest side)
                    self._data.pop()
                    self._count -= 1
            else:
                logging.debug(f"Debug, {self._name} add NaN thrown out.")    
        else:
            logging.debug(f"Debug, {self._name} add None thrown out.")    
    def average(self):
        """Get the average of all stored temperature samples."""
        sum = 0
        # loop through all temperature samples
        for temp in self._data:
            sum += temp
        logging.debug(f"Debug, {self._name} average {sum / self._count:0.2F}.")
        return sum / self._count
    
    def clear(self):
        """Clear all stored temperature samples."""
        logging.debug(f"Debug, {self._name} clear {self._count} samples.")
        self._count = 0
        self._data = [] 

    def len(self):
        """Returns the number of stored temperature samples."""
        return self._count

