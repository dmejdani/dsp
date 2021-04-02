"""
Simulation in python of a real-time circular buffer.
Based on the circular buffer there are Delay and FIR buffer simulation.
For fun; not much use of this other than learning.
"""
from typing import Union

import numpy as np


class Buffer:
    """Simple circular buffer"""

    def __init__(self, size: int = 256):
        """
        Initialize the buffer with zeros

        :param size: Size of the buffer as int
        """
        self.size = size
        self.state = np.zeros(size)
        self.ptr = 0

    def insert(self, sample: Union[int, float]) -> None:
        """
        Insert new sample in the circular buffer and increment the pointer accordingly

        :param sample: The new sample to be added
        """
        self.state[self.ptr] = sample
        self.ptr = self.increment(self.ptr)

    def increment(self, pointer: int, amount: int = 1) -> int:
        """Increment a pointer by amount in a circular buffer fashion"""
        return (pointer + amount) & (self.size - 1)
    
    def decrement(self, pointer: int, amount: int = 1) -> int:
        """Decrement a pointer by amount in a circular buffer fashion"""
        return (pointer + self.size - amount) & (self.size - 1)

    def empty(self) -> None:
        """Empty the buffer by filling it with zeros"""
        self.state[:] = 0


class Delay(Buffer):
    """A simple delay"""

    def __init__(self, delay: int = 0, *args, **kwargs):
        """
        Initialize the delay buffer

        :param delay: The amount of delay in samples
        """
        super().__init__(*args, **kwargs)
        
        if self.size <= delay:
            raise RuntimeError(f"Maximum delay possible is {self.size - 1}")

        self.delay = delay
        self.read_ptr = self.decrement(self.ptr, delay)  # set read_ptr delay steps behind

    def read(self) -> Union[int, float]:
        """
        Return the delayed sample of the input and increment `read_ptr` accordingly.
        Throws if `read_ptr` reaches `ptr`.
        """
        if self.read_ptr == self.ptr:
            raise RuntimeError("Read pointer reached write pointer! Add new sample to buffer.")
        
        v = self.state[self.read_ptr]
        self.read_ptr = self.increment(self.read_ptr)
        return v
        

class FIRFilter(Buffer):
    """A simple FIR filter"""

    def __init__(self, taps: np.array, *args, **kwargs):
        """
        Initialize a buffer implementation of a FIR filter
        
        :param taps: Array of filter tap values
        """
        super().__init__(*args, **kwargs)

        if self.size <= len(np):
            raise RuntimeError(f"The maximum size of the filter is {self.size - 1}")

        self.taps = taps
        self.nr_taps = len(taps)

    def compute(self) -> Union[int, float]:
        """Calculate the sum after the current step of the convolution"""
        sum = 0
        for i in range(self.nr_taps):
            sum += self.state[self.decrement(self.ptr, i+1)] * self.taps[i]
        return sum
