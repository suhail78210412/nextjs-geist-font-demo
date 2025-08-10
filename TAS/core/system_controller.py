"""
System Controller for TAS
Handles desktop control and system operations
"""

import logging
import subprocess
import platform
import os
from typing import List, Dict, Any

class SystemController:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('TAS.System')
        self.platform = platform.system()
        
    def get_system_info(self) -> Dict[str, str]:
        """Get system information"""
        return {
            "platform": self.platform,
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "architecture": platform.machine()
        }
        
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }
            
    def list_running_processes(self) -> List[str]:
        """List running processes"""
        if self.platform == "Windows":
            return self.execute_command("tasklist").get("stdout", "").splitlines()
        else:
            return self.execute_command("ps aux").get("stdout", "").splitlines()
            
    def open_application(self, app_name: str) -> bool:
        """Open an application"""
        if self.platform == "Windows":
            return self.execute_command(f"start {app_name}")["success"]
        elif self.platform == "Darwin":  # macOS
            return self.execute_command(f"open -a {app_name}")["success"]
        else:  # Linux
            return self.execute_command(f"{app_name} &")["success"]
            
    def close_application(self, app_name: str) -> bool:
        """Close an application"""
        if self.platform == "Windows":
            return self.execute_command(f"taskkill /f /im {app_name}.exe")["success"]
        else:
            return self.execute_command(f"pkill {app_name}")["success"]
            
    def get_system_status(self) -> Dict[str, Any]:
        """Get system health status"""
        status = {
            "cpu_usage": self._get_cpu_usage(),
            "memory_usage": self._get_memory_usage(),
            "disk_usage": self._get_disk_usage(),
            "uptime": self._get_uptime()
        }
        return status
        
    def _get_cpu_usage(self) -> float:
        """Get CPU usage percentage"""
        try:
            if self.platform == "Windows":
                result = self.execute_command("wmic cpu get loadpercentage /value")
                for line in result.get("stdout", "").splitlines():
                    if "LoadPercentage" in line:
                        return float(line.split("=")[1])
            else:
                result = self.execute_command("top -bn1 | grep 'Cpu(s)'")
                # Parse CPU usage from top output
                return 0.0  # Placeholder
        except:
            return 0.0
            
    def _get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage"""
        try:
            if self.platform == "Windows":
                result = self.execute_command("wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value")
                # Parse memory info
                return {"total": 0, "used": 0, "free": 0}
            else:
                result = self.execute_command("free -m")
                # Parse memory info
                return {"total": 0, "used": 0, "free": 0}
        except:
            return {"total": 0, "used": 0, "free": 0}
            
    def _get_disk_usage(self) -> Dict[str, float]:
        """Get disk usage"""
        try:
            if self.platform == "Windows":
                result = self.execute_command("wmic logicaldisk get size,freespace,caption")
                # Parse disk info
                return {"total": 0, "used": 0, "free": 0}
            else:
                result = self.execute_command("df -h /")
                # Parse disk info
                return {"total": 0, "used": 0, "free": 0}
        except:
            return {"total": 0, "used": 0, "free": 0}
            
    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            if self.platform == "Windows":
                result = self.execute_command("systeminfo | findstr 'System Boot Time'")
                return result.get("stdout", "").strip()
            else:
                result = self.execute_command("uptime")
                return result.get("stdout", "").strip()
        except:
            return "Unknown"
