#!/usr/bin/python3.12.3


from time import sleep
from os import listdir, sysconf, sysconf_names
    
class CPU(object):

    
    PATHS: dict = {
        "stat": "/proc/stat",
        "cpuInfo": "/proc/cpuinfo",
        "frequency": "/sys/devices/system/cpu/cpufreq",
        "temperature": "/sys/class/hwmon",
        "coreTemperature": [],
    }
    
    CPU_INFO: dict = {
        "model name": "",
        "cpu cores": "",
    }
    
    CPU_CORES_INFO: dict = {
        "id": "",
        "frequency": "",
        "utilization": "",
        "temperature": "",
    }

    # getting the clock rate of the system. -> https://man7.org/linux/man-pages/man2/times.2.html
    SYSTEM_CLOCK_TICK = sysconf(sysconf_names['SC_CLK_TCK'])

    def __init__(self,) -> None:
        """initializing cpu class."""
        
        self.setCpuStatics()
        
        self.curTime: list = []
        self.prevTime: list = []

        # extracting frequncies and temperature directories
        self.frequency: list = listdir(self.PATHS["frequency"])
        self.temperature: list = listdir(self.PATHS["temperature"])

        # first sort then try to match with each core
        self.frequency.sort()
        self.temperature.sort()

        self.findCoreTemp()
        self.setCoreTempPath()
        
    def findCoreTemp(self,) -> None:
        """finding the directory which contains temperatures then the label of cores.
        >> https://www.kernel.org/doc/html/v6.9/hwmon/coretemp.html.
        """
        
        for temp in self.temperature:
            with open(f"{self.PATHS['temperature']}/{temp}/name") as temperature:
                if temperature.readline().strip() == "coretemp":
                    self.temperature = temp
                    break
                else:
                    pass

    def setCoreTempPath(self,) -> None:
        """finding the core temperature path."""

        for core in range(int(self.CPU_INFO["cpu cores"]) + 1):
            with open(f"{self.PATHS['temperature']}/{self.temperature}/temp{str(core + 1)}_label") as tempLabel:
                if tempLabel.readline().strip()[:4] == "Core":
                    self.PATHS["coreTemperature"].append(f"{self.PATHS['temperature']}/{self.temperature}/temp{str(core + 1)}_input")
                else:
                    pass
                
    def setCpuStatics(self,) -> None:
        """extracting static cpu information."""

        with open(self.PATHS["cpuInfo"], "r") as cpuInfo:
            for _ in range(26):
                line = next(cpuInfo)
                key, value = line.split(":")
                if key.strip() in self.CPU_INFO:
                    self.CPU_INFO[key.strip()] = value.strip()
            cpuInfo.close()

    def setCpuTimes(self,) -> None:
        """reading time of cpu for each core from /proc/stat."""

        self.prevTime = self.curTime
        self.curTime = []
        
        with open(self.PATHS["stat"]) as stat:
            next(stat)
            for _ in range(int(self.CPU_INFO["cpu cores"])):
                line = next(stat)
                self.curTime.append(line.strip().split())
            
    def calcCoreUtilization(self, core: int = 0) -> str:
        """calculating the core utilization.
        >> try 'man proc_stat' or https://man7.org/linux/man-pages/man5/proc_stat.5.html.
        """
        
        prevIdle: int = int(self.prevTime[core][4]) + int(self.prevTime[core][5])
        prevTotal: int = sum([int(time) for time in self.prevTime[core][1:]])

        curIdle: int = int(self.curTime[core][4]) + int(self.curTime[core][5])
        curTotal: int = sum([int(time) for time in self.curTime[core][1:]])

        return str(int((1 - ((curIdle - prevIdle) / (curTotal - prevTotal))) * 100))+"%" if (curTotal - prevTotal) > 0 else "0%"

    def setCoreTemperature(self,):
        """finding the core related temperature."""

        for coreTemp in self.PATHS["coreTemperature"]:
            with open(coreTemp) as temperature:
                return temperature.readline().strip()
            
    def setCoreFrequency(self, core: int = 0) -> str:
        """finding the core frequency."""
        
        with open(f"{self.PATHS['frequency']}/{self.frequency[core]}/scaling_cur_freq") as frequency:
            return frequency.readline().strip()
            
    def setCpuCoreStatics(self,) -> list:
        """extracting info for each core."""
    
        result: list = []
                        
        convertFrequency = lambda frequency: f"{int(int(frequency) / 1000)} Mhz" if len(frequency) <= 6 else f"{int(frequency) / 1000000 :.1f} Ghz"
        convertTemperature = lambda temperature: f"{int(temperature) / 1000: .0f}"    
        
        for core in range(int(self.CPU_INFO["cpu cores"])):
            coreInfo = self.CPU_CORES_INFO.copy()
            
            coreInfo["id"]          = core
            coreInfo["frequency"]   = convertFrequency(self.setCoreFrequency(core))
            coreInfo["temperature"] = convertTemperature(self.setCoreTemperature())
            coreInfo["utilization"] = self.calcCoreUtilization(core)

            result.append(coreInfo)
            
        return result
            
