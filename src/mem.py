#!/usr/bin/python3.12.3

from time import sleep


class MEMORY(object):

    PATHS: dict = {
        "meminfo":"/proc/meminfo",
    }

    MEMORY_INFO: dict = {
        "MemTotal":"",
        "MemFree":"",
        "MemAvailable":"",
        "Cached":"",
    }
    
    def setMemoryInfo(self,) -> None:
        """finding the memory info from."""

        with open("/proc/meminfo", "r") as memInfo:
            while True:
                line = next(memInfo).strip().split()
                key, value = line[0][:len(line[0])-1], line[1]

                if key in self.MEMORY_INFO:
                    self.MEMORY_INFO[key] = value
                    if key == "Cached":
                        break
