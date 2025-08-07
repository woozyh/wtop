#!/usr/bin/python3.12.3

from os import listdir, sysconf, sysconf_names
from time import sleep

class PROCESS(object):


    MB: int = 2 ** 20
    GB: int = 2 ** 30

    INTERVAL = 0.6
    
    CLK_TCK: int = sysconf(sysconf_names["SC_CLK_TCK"])
    PAGE_SIZE: int = sysconf(sysconf_names["SC_PAGESIZE"])

    UID_INFO: dict = dict()
    
    PROCESS_INFO: dict = {
        "pid": {
            "Uid": "",
            "Name": "",
            "Threads": "",
            "command": "",
            "cpuUsage": "",
            "curCpuTime": 0,
            "memoryUsage": "",
            "prevCpuTime": 0,
        }
    }

    def __init__(self,) -> None:
        """initalizing the process class."""

        self.cpuPrevTime: int = int()
        self.cpuCurTime: int = int()
        self.setUserIds()

    def setUserIds(self,) -> None:
        """finding the user ids from /etc/passwd."""

        with open("/etc/passwd") as passwd:
            while True:
                try:
                    line = next(passwd).strip().split(":")
                    self.UID_INFO[line[2]] = line[0]
                except StopIteration:
                    break
            
    def getProcessList(self,) -> list:
        """getting process list for each iteration."""

        processes: list = [pid for pid in listdir("/proc") if pid.isdigit()]

        return processes
    
    def setProcessStaticStatus(self, pid: str) -> None:
        """setting the processes static status like pid, name, user, ... ."""
        
        self.PROCESS_INFO.update(
            {pid: self.PROCESS_INFO["pid"].copy()} 
        )

        try:
            with open(f"/proc/{pid}/status") as processStatus:
                while True:
                    line = next(processStatus).strip().split(":")
                    key, value = line[0][:len(line[0])], line[1].strip()
                    
                    if key in self.PROCESS_INFO[pid].keys():
                        if key == "Uid":
                            self.PROCESS_INFO[pid][key] = self.UID_INFO[value.split()[0]]
                        else:
                            self.PROCESS_INFO[pid][key] = value
                        
                    if self.PROCESS_INFO[pid]["Name"] and self.PROCESS_INFO[pid]["Threads"] and self.PROCESS_INFO[pid]["Uid"]:
                        break

            with open(f"/proc/{pid}/cmdline") as processCommand:
                command = processCommand.readline().strip().split()
                if command:
                    self.PROCESS_INFO[pid]["command"] = command[0].strip("\x00")
                else:
                    self.PROCESS_INFO[pid]["command"] = self.PROCESS_INFO[pid]["Name"]

        except FileNotFoundError:
            self.PROCESS_INFO.pop(pid)
                    
    def getMemoryUsage(self, pid: str) -> str:
        """getting memory usage of specific process."""

        convertMemoryUsage = lambda memoryUsage: f"{memoryUsage / self.MB: .0f}M" if memoryUsage < self.GB else f"{memoryUsage / self.GB: .0f}G"

        try:

            with open(f"/proc/{pid}/stat") as memoryUsage:
                line = memoryUsage.readline().strip(")(-:/").split()
                
                return convertMemoryUsage(int(line[23+len(line)-52]) * self.PAGE_SIZE)

        except FileNotFoundError:
            self.PROCESS_INFO.pop(pid)
            
    def setProcessCpuTime(self, pid: int) -> None:
        """setting the process current cpu time and previous cpu time."""

        self.PROCESS_INFO[pid]["prevCpuTime"] = self.PROCESS_INFO[pid]["curCpuTime"]

        try:
            with open(f"/proc/{pid}/stat") as cpuTime:
                
                line = cpuTime.readline().strip().split()
                
                self.PROCESS_INFO[pid]["curCpuTime"] = (int(line[13]) + int(line[14]) + int(line[15]) + int(line[16])) / self.CLK_TCK

        except FileNotFoundError:
            self.PROCESS_INFO.pop(pid)

    def getCpuTime(self,) -> int:
        """getting the cpuTime. in each iteration."""
        
        with open("/proc/stat") as cpuStat:
            line = next(cpuStat).strip().split()

            return sum([int(time) for time in line[1:]]) / self.CLK_TCK

    def calcCpuUtilization(self, pid: int) -> str:
        """calculating the cpu utilization for each process."""

        procPrevTime = self.PROCESS_INFO[pid]["prevCpuTime"]
        procCurTime  = self.PROCESS_INFO[pid]["curCpuTime"]
        
        deltaProc = procCurTime - procPrevTime
        deltaCpu = self.cpuCurTime - self.cpuPrevTime
        
        return f"{min(100, (deltaProc / deltaCpu) * 100): .1f}" if (deltaCpu and deltaProc) > 0 else "0.0"
        
    def setProcessDynamicStatus(self,):
        """setting the process status."""        

        self.cpuPrevTime = self.cpuCurTime
        self.cpuCurTime = self.getCpuTime()

        processList = self.getProcessList()
        
        for pid  in list(self.PROCESS_INFO.keys()):
            if pid != "pid" and pid not in processList:
                self.PROCESS_INFO.pop(pid)
        
        for pid in processList[::-1]:
            if pid not in self.PROCESS_INFO:
                self.setProcessStaticStatus(pid)
            else:
                self.PROCESS_INFO[pid]["memoryUsage"] = self.getMemoryUsage(pid)

                self.setProcessCpuTime(pid)
                
                self.PROCESS_INFO[pid]["cpuUsage"] = self.calcCpuUtilization(pid)

ins = PROCESS()

while True:

    ins.setProcessDynamicStatus()
    print(ins.PROCESS_INFO)
    sleep(0.6)
                
