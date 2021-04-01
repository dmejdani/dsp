"""
Implementation in python of a circular buffer. 
For fun; not much use of this since there are no pointers in python to do this efficiently.
I will try to do this artificially
"""
from typing import Union

import numpy as np


class Buffer:
    """
    Simple circular buffer
    """
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

    def increment(self, pointer, amount: int = 1) -> int:
        """Increment a pointer by amount taking into account the buffer size"""
        return (pointer + amount) % self.size

    def empty(self) -> None:
        """Empty the buffer by filling it with zeros"""
        self.state[:] = 0


class Delay(Buffer):
    """
    A simple delay 
    """
    def __init__(self, delay: int = 0, *args, **kwargs):
        """
        Initialize the delay buffer

        :param delay: The amount of delay in samples
        """
        super().__init__(*args, **kwargs)
        self.delay = delay
        self.read_ptr = 0
        self.ptr += delay  # push ptr forward 

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

