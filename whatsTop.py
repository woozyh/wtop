#!/usr/bin/python3.12.3


from os import path
from ui import whatsTopUi
from time import sleep
from src import (
    cpu,
    gpu,
    mem,
    proc,
)


class WhatsTop():

    MEM_STAT: dict[str, str] = None
    GPU_STAT: dict[str, str] = None
    CPU_STAT: list[dict[str, str]] = None
    PROC_STAT: dict[dict[str, str]] = None

    def __init__(self) -> None:
        """initializing the building block of WhatsTop class."""

        if path.exists("/proc"):
            self.cpu = cpu.CPU()
            self.mem = mem.MEMORY()
            self.proc = proc.PROCESS()
        else:
            print("Error: This program only works on unix/linux based systems which supports /proc.")
            exit()

        self.gpu = gpu.GPU()

        if not self.gpu.GPU_INFO["initializing"]:
            print("Warning: Gpu not initialized, Only nvidia based chips are supported.")
        else:
            print("gpu initialized successfully.")

        self.cpu.setCpuStatics()
        
        self.ui = whatsTopUi.Ui()

        self.generateStatus()
        
    def setStatus(self,) -> None:
        """setting the status to ui relater objects."""

        self.ui.setCpuStatus(status  = self.CPU_STAT)
        self.ui.setMemStatus(status  = self.MEM_STAT)
        self.ui.setGpuStatus(status  = self.GPU_STAT)
        self.ui.setProcStatus(status = self.PROC_STAT)
        
    def generateStatus(self,) -> None:
        """generating status on each cycle."""

        if self.gpu.GPU_INFO["initializing"]:
            self.GPU_STAT = self.gpu.setGpuDynamicStatus()
            
        self.MEM_STAT = self.mem.setMemoryInfo()
            
        self.PROC_STAT = self.proc.setProcessDynamicStatus()
        
        self.cpu.setCpuTimes()
        sleep(0.5)       
        self.cpu.setCpuTimes()
        self.CPU_STAT = self.cpu.setCpuCoreStatics()
        
        self.setStatus()
        self.ui.after(200, self.generateStatus)
        
if __name__ == "__main__":

    ins = WhatsTop()
    ins.ui.mainloop()

