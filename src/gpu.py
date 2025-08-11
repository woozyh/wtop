#!/usr/bin/python3.12.3

try:
    from pynvml import (
        nvmlInit,
        NVMLError,
        nvmlDeviceGetName,
        NVML_TEMPERATURE_GPU,
        nvmlDeviceGetMemoryInfo,
        nvmlDeviceGetTemperature,
        nvmlDeviceGetHandleByIndex,
    )
except ImportError:
    print("Error: first try pip install -r requirements.txt then try again.")
    

class GPU(object):

    MB: int = 2**20
    GB: int = 2**30

    GPU_INFO: dict = {
        "modelName": "N/A",
        "usedMemory": "N/A",
        "totalMemory": "N/A",
        "temperature": "N/A",
        "initializing": "",
    }

    def __init__(self,) -> None:
        """initializing GPU class."""

        try:
            nvmlInit()
            self.GPU_INFO["initializing"] = True
            self.handle = nvmlDeviceGetHandleByIndex(0)
            self.temperatureSensor = NVML_TEMPERATURE_GPU
            self.GPU_INFO["modelName"] = nvmlDeviceGetName(self.handle)
        except NVMLError as er:
            print(f"Error occured on GPU: {er}")
            self.GPU_INFO["initializing"] = False
            
    def setGpuDynamicStatus(self,) -> dict:
        """setting gpu info by each iteration."""
        
        gpuInfo: dict = self.GPU_INFO.copy()

        convertMemorySize = lambda memorySize: f"{int(memorySize) / self.GB: .1f}G" if memorySize > self.MB else f"{int(memorySize) / self.MB: .0f}M"
        
        try:
            memInfo = nvmlDeviceGetMemoryInfo(self.handle)
            gpuInfo["usedMemory"] = convertMemorySize(memInfo.used)
            gpuInfo["totalMemory"] = convertMemorySize(memInfo.total)
            gpuInfo["temperature"] = nvmlDeviceGetTemperature(self.handle, self.temperatureSensor)

        except NVMLError:
            pass

        return gpuInfo
    
