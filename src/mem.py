#!/usr/bin/python3.12.3

from time import sleep
from ast import literal_eval

class MEMORY(object):

    MB: int = 2 ** 20
    GB: int = 2 ** 30
    
    PATHS: dict = {
        "meminfo":"/proc/meminfo",
    }

    MEMORY_INFO: dict = {
        "Cached": "",
        "MemFree": "",
        "MemUsed": "",
        "MemTotal": "",
        "MemAvailable": "",
    }

    def convertSize(self, value: str) -> str:
        """comverting the memory size to Gigabyte and Megabyte."""
        
        return f"{int(value) / self.GB: .1f}G" if int(value) > self.MB else f"{int(value) / self.MB: .0f}M"
    
    def calcUsedMemory(self,) -> str:
        """calculating used memory from memoryInfo."""

        match [self.MEMORY_INFO["MemTotal"][-1], self.MEMORY_INFO["MemAvailable"][-1]]:
            case ["G", "G"]:
                self.MEMORY_INFO["MemUsed"] = self.convertSize(
                    (literal_eval(self.MEMORY_INFO["MemTotal"].strip("GM")) - literal_eval(self.MEMORY_INFO["MemAvailable"].strip("GM"))) * self.GB
                )
            case ["G", "M"]:
                self.MEMORY_INFO["MemUsed"] = self.convertSize(
                    (literal_eval(self.MEMORY_INFO["MemTotal"].strip("GM")) * self.GB - literal_eval(self.MEMORY_INFO["MemAvailable"].strip("GM")) * self.MB)
                )
            case ["M", "G"]:
                self.MEMORY_INFO["MemUsed"] = self.convertSize(
                    (literal_eval(self.MEMORY_INFO["MemTotal"].strip("GM")) * self.MB - literal_eval(self.MEMORY_INFO["MemAvailable"].strip("GM")) * self.GB)
                )
            case ["M", "M"]:
                self.MEMORY_INFO["MemUsed"] = self.convertSize(
                    (literal_eval(self.MEMORY_INFO["MemTotal"].strip("GM")) - literal_eval(self.MEMORY_INFO["MemAvailable"].strip("GM"))) * self.MB
                )
                
    def setMemoryInfo(self,) -> None:
        """finding the memory info from."""

        with open("/proc/meminfo", "r") as memInfo:
            while True:
                line = next(memInfo).strip().split()
                key, value = line[0][:len(line[0])-1], line[1].strip()

                if key in self.MEMORY_INFO:
                    self.MEMORY_INFO[key] = self.convertSize(int(value) * 1024).strip()
                    if key == "Cached":
                        self.MEMORY_INFO["Cached"] = self.convertSize(value)
                        break

        self.calcUsedMemory()
            
        return self.MEMORY_INFO
                    
ins = MEMORY()
while True:
    ins.setMemoryInfo()
    print(ins.MEMORY_INFO)
    sleep(1)
