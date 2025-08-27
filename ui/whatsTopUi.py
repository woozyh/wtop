#!/usr/bin/python3.12.3

import tkinter
from tkinter import ttk


class Ui(tkinter.Tk):

    TITLE: str = "whatsTop"
    GEOMETRY: str = "1000x600"
    
    def __init__(self) -> None:
        """initializing the Ui class."""

        super().__init__()
        
        self.title(self.TITLE)
        self.geometry(self.GEOMETRY)
        self.configure(bg = "black")
        
        self.selectedProcess: str = str()
        
        self.generateWidgets()
        self.rowColumnConfig()
        self.styleConfig()
        self.bindGrids()

    def setSelectedProcess(self, selectedItem: str = "I001") -> None:
        self.selectedProcess = selectedItem
            
    def generateWidgets(self,) -> None:
        """generating needed widget for ui."""

        gpuColumnHeadings = ("totalMem", "usedMem", "temp")
        cpuColumnHeadings = ("core", "freq", "util", "temp")
        memColumnHeadings = ("total", "used", "available", "cached")
        procColumnHeadings = ("pid", "program", "command", "threads", "user", "mem", "cpu")
        
        self.topFrame    = ttk.Frame(self,)
        self.bottomFrame = ttk.Frame(self,)

        self.cpu          = ttk.Labelframe(self.topFrame, text = "CPU", labelanchor = "n")
        self.gpu          = ttk.Labelframe(self.topFrame, text = "GPU", labelanchor = "n")
        self.mem          = ttk.Labelframe(self.topFrame, text = "MEM", labelanchor = "n")
        self.cpuStatus    = ttk.Treeview(self.cpu, columns = cpuColumnHeadings, show = "headings", height = 4)
        self.gpuStatus    = ttk.Treeview(self.gpu, columns = gpuColumnHeadings, show = "headings", height = 4)
        self.memStatus    = ttk.Treeview(self.mem, columns = memColumnHeadings, show = "headings", height = 4)
        self.proc         = ttk.Treeview(self.bottomFrame, columns = procColumnHeadings, show = "headings")
        self.cpuScroll    = ttk.Scrollbar(self.cpu, orient = "vertical", command = self.cpuStatus.yview)
        self.gpuScroll    = ttk.Scrollbar(self.gpu, orient = "vertical", command = self.gpuStatus.yview)
        self.memScroll    = ttk.Scrollbar(self.mem, orient = "vertical", command = self.memStatus.yview)
        self.procScroll   = ttk.Scrollbar(self.bottomFrame, orient = "vertical", command = self.proc.yview)
        self.proc.configure(yscrollcommand = self.procScroll.set)
        self.cpuStatus.configure(yscrollcommand = self.cpuScroll.set)
        self.gpuStatus.configure(yscrollcommand = self.gpuScroll.set)
        self.memStatus.configure(yscrollcommand = self.memScroll.set)

        self.proc.bind("<Key-t>", lambda arg: self.proc.delete(self.selectedProcess))
        self.proc.bind("<<TreeviewSelect>>", lambda arg: self.setSelectedProcess(self.proc.selection()))
        
        for heading in procColumnHeadings:
            self.proc.heading(heading, text = heading)
            self.proc.column(heading, width = 1, anchor = "n")

        for heading in cpuColumnHeadings:
            self.cpuStatus.heading(heading, text = heading)
            self.cpuStatus.column(heading, width = 1, anchor = "n")

        for heading in gpuColumnHeadings:
            self.gpuStatus.heading(heading, text = heading)
            self.gpuStatus.column(heading, width = 1, anchor = "n")

        for heading in memColumnHeadings:
            self.memStatus.heading(heading, text = heading)
            self.memStatus.column(heading, width = 1, anchor = "n")
            
    def rowColumnConfig(self,) -> None:
        """configuring rows and columns for each layouts."""
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 10)
        self.columnconfigure(0, weight = 1)

        self.topFrame.rowconfigure(0, weight = 1)
        self.topFrame.columnconfigure((0, 1, 2), weight = 1)

        self.bottomFrame.rowconfigure(0, weight = 1)
        self.bottomFrame.columnconfigure(1, weight = 1)
        self.bottomFrame.columnconfigure(0, weight = 100)
        
        self.cpu.rowconfigure(0, weight = 1)
        self.cpu.columnconfigure(1, weight = 1)
        self.cpu.columnconfigure(0, weight = 100)
        
        self.gpu.rowconfigure(0, weight = 1)
        self.gpu.columnconfigure(1, weight = 1)
        self.gpu.columnconfigure(0, weight = 100)
        
        self.mem.rowconfigure(0, weight = 1)
        self.mem.columnconfigure(1, weight = 1)
        self.mem.columnconfigure(0, weight = 100)
        
    def styleConfig(self,) -> None:
        """configuring styles."""
<<<<<<< HEAD
        pass
        
=======

        self.tk.call('lappend', 'auto_path', 'ui/awthemes')
        self.tk.call('package', 'require', 'awdark')
        
        style = ttk.Style(self)
        style.theme_use('awdark')

>>>>>>> themed
    def bindGrids(self,) -> None:
        """griding the built objects"""

        self.topFrame.grid(row = 0, column = 0, sticky = "nsew", padx = 2, pady = 2)
        self.bottomFrame.grid(row = 1, column = 0, sticky = "nsew", padx = 2, pady = 2)
        
        self.cpu.grid(row  = 0, column = 0, sticky = "ew", padx = 2, pady = 2)
        self.mem.grid(row  = 0, column = 1, sticky = "ew", padx = 2, pady = 2)
        self.gpu.grid(row  = 0, column = 2, sticky = "ew", padx = 2, pady = 2)  
        self.proc.grid(row = 0, column = 0, sticky = "nsew", padx = 2, pady = 2)
        self.cpuStatus.grid(row = 0, column = 0, sticky = "nsew", padx = 2, pady = 2)
        self.gpuStatus.grid(row = 0, column = 0, sticky = "nsew", padx = 2, pady = 2)
        self.memStatus.grid(row = 0, column = 0, sticky = "nsew", padx = 2, pady = 2)
        self.cpuScroll.grid(row = 0, column = 1, sticky = "nsew", padx = 1, pady = 1)
        self.gpuScroll.grid(row = 0, column = 1, sticky = "nsew", padx = 1, pady = 1)
        self.memScroll.grid(row = 0, column = 1, sticky = "nsew", padx = 1, pady = 1)
        self.procScroll.grid(row = 0, column = 1, sticky = "nsew", padx = 1, pady = 1)
        
    def setCpuStatus(self, status: list) -> None:
        """binding the cpu cores status to related graphical object."""

        for core in status:

            iid = str(core['id'])
            if iid in self.cpuStatus.get_children():
                self.cpuStatus.item(iid, values=(core["id"], core["frequency"], core["utilization"], core["temperature"]))
            else:
                self.cpuStatus.insert("", "end", iid=iid, values=(core["id"], core["frequency"], core["utilization"], core["temperature"]))

        
    def setMemStatus(self, status: dict) -> None:
        """binding the mem cores status to related graphical object."""

        self.memStatus.delete(*self.memStatus.get_children())

        self.memStatus.insert("", "end", values = (status["MemTotal"], status["MemUsed"], status["MemAvailable"], status["Cached"]))
        
    def setGpuStatus(self, status: dict) -> None:
        """binding the gpu cores status to related graphical object."""

        self.gpu["text"] = status["modelName"]
        
        self.gpuStatus.delete(*self.gpuStatus.get_children())

        self.gpuStatus.insert("", "end", values = (status["totalMemory"], status["usedMemory"], status["temperature"]))
        

    def setProcStatus(self, status: dict) -> None:
        """binding the proc cores status to related graphical object."""

        self.proc.delete(*self.proc.get_children())
        
        for pid in status:
            
            iid = pid            
            if iid != "pid":
                if pid in self.proc.get_children():
                    self.proc.item(iid, values = (pid, status[pid]["Name"], status[pid]["command"], status[pid]["Threads"], status[pid]["Uid"], status[pid]["memoryUsage"], status[pid]["cpuUsage"]))
                else:
                    self.proc.insert("", "end", iid = pid, values = (pid, status[pid]["Name"], status[pid]["command"], status[pid]["Threads"], status[pid]["Uid"], status[pid]["memoryUsage"], status[pid]["cpuUsage"]))
            else:
                pass


