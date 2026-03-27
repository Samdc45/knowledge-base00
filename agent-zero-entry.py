#!/usr/bin/env python3
"""
Agent Zero - Unified Entry Point (v1.3 Hybrid)
Routes all tasks through Python autonomous agent (primary) with Docker v1.3 UI as secondary
"""

import json
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class ExecutionMode(Enum):
    DOCKER_V13 = "docker-v1.3-ui"      # Official Agent Zero v1.3 (UI)
    AUTONOMOUS_PYTHON = "python-autonomous"     # Custom autonomous routing
    HYBRID = "hybrid-python-first"                # Python first, Docker fallback

@dataclass
class EntryConfig:
    primary_mode: ExecutionMode = ExecutionMode.AUTONOMOUS_PYTHON
    docker_url: str = "http://localhost:55015"
    python_url: str = "http://localhost:5555"
    fallback_enabled: bool = True
    version: str = "v1.3-hybrid"
    label: str = "command-entry-point"
    info: str = "Unified entry point: Python autonomous (primary) + Docker v1.3 UI (secondary)"

class UnifiedEntryPoint:
    """Single entry point for all Agent Zero operations"""
    
    def __init__(self, config: EntryConfig):
        self.config = config
        self.request_log = []
        self.execution_stats = {
            "total_requests": 0,
            "python_primary": 0,
            "docker_fallback": 0,
            "all_failed": 0
        }
    
    def route_task(self, task: str, data: Optional[Dict] = None, priority: int = 3) -> Dict[str, Any]:
        """Route task through entry point to Python autonomous agent (primary)"""
        self.execution_stats["total_requests"] += 1
        
        request_id = f"REQ-{datetime.now().isoformat()}"
        
        # Primary: Route to Python autonomous agent
        result = self._route_to_python(task, data, request_id, priority)
        if result and not result.get("error"):
            self.execution_stats["python_primary"] += 1
            return result
        
        # Fallback: Route to Docker v1.3 if enabled
        if self.config.fallback_enabled:
            result = self._route_to_docker_v13(task, data, request_id)
            if result and not result.get("error"):
                self.execution_stats["docker_fallback"] += 1
                return result
        
        self.execution_stats["all_failed"] += 1
        return {
            "error": "All routing modes failed",
            "request_id": request_id,
            "task": task,
            "mode_attempted": ["python-autonomous", "docker-v1.3-ui"]
        }
    
    def _route_to_python(self, task: str, data: Optional[Dict], request_id: str, priority: int) -> Optional[Dict]:
        """Route to Python autonomous agent (PRIMARY)"""
        try:
            response = requests.post(
                f"{self.config.python_url}/autonomously/route-task",
                json={"task": task, "data": data or {}, "priority": priority},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return {
                    "request_id": request_id,
                    "mode": "python-autonomous-primary",
                    "task": task,
                    "subagents_used": result.get("subagents_used"),
                    "subagent_names": result.get("subagent_names"),
                    "aggregated_result": result.get("aggregated"),
                    "timestamp": result.get("timestamp"),
                    "status": "success"
                }
        except Exception as e:
            return {"error": str(e), "mode": "python-autonomous", "exception": type(e).__name__}
        return None
    
    def _route_to_docker_v13(self, task: str, data: Optional[Dict], request_id: str) -> Optional[Dict]:
        """Route to Agent Zero v1.3 Docker UI (FALLBACK)"""
        try:
            # v1.3 is primarily UI-based; return UI URL for manual interaction
            return {
                "request_id": request_id,
                "mode": "docker-v1.3-ui-fallback",
                "task": task,
                "message": "Primary autonomous routing failed. Access UI for manual task execution.",
                "ui_url": f"{self.config.docker_url}/",
                "status": "fallback-ui"
            }
        except Exception as e:
            return {"error": str(e), "mode": "docker-v1.3"}
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get unified entry point status"""
        python_status = self._check_python_health()
        docker_status = self._check_docker_health()
        
        return {
            "entry_point": "unified-v1.3-hybrid",
            "label": self.config.label,
            "version": self.config.version,
            "info": self.config.info,
            "primary_mode": self.config.primary_mode.value,
            "fallback_enabled": self.config.fallback_enabled,
            "agents": {
                "python_autonomous": python_status,
                "docker_v13_ui": docker_status
            },
            "stats": self.execution_stats,
            "endpoints": {
                "entry_route": "/entry/route",
                "entry_status": "/entry/status",
                "entry_stats": "/entry/stats",
                "entry_health": "/entry/health",
                "switch_mode": "/entry/switch-mode/<mode>"
            }
        }
    
    def _check_python_health(self) -> Dict[str, Any]:
        """Check Python autonomous agent health"""
        try:
            response = requests.get(f"{self.config.python_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "endpoint": self.config.python_url,
                    "service": data.get("service"),
                    "role": "primary"
                }
        except:
            pass
        return {"status": "unreachable", "endpoint": self.config.python_url, "role": "primary"}
    
    def _check_docker_health(self) -> Dict[str, Any]:
        """Check Docker v1.3 health"""
        try:
            response = requests.get(f"{self.config.docker_url}/", timeout=5)
            if response.status_code == 200:
                return {
                    "status": "running",
                    "endpoint": self.config.docker_url,
                    "type": "ui",
                    "role": "fallback"
                }
        except:
            pass
        return {"status": "unreachable", "endpoint": self.config.docker_url, "role": "fallback"}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        total = self.execution_stats["total_requests"]
        python_ratio = (self.execution_stats["python_primary"] / total * 100) if total > 0 else 0
        docker_ratio = (self.execution_stats["docker_fallback"] / total * 100) if total > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_requests": total,
            "python_primary_success": f"{python_ratio:.1f}%",
            "docker_fallback_used": f"{docker_ratio:.1f}%",
            "all_failed": self.execution_stats["all_failed"],
            "request_log_entries": len(self.request_log)
        }

# REST API
from flask import Flask, request, jsonify

app = Flask(__name__)
config = EntryConfig()
entry = UnifiedEntryPoint(config)

@app.route('/entry/route', methods=['POST'])
def entry_route():
    """Main entry point for task routing"""
    data = request.json
    task = data.get('task')
    payload = data.get('data', {})
    priority = data.get('priority', 3)
    
    result = entry.route_task(task, payload, priority)
    return jsonify(result)

@app.route('/entry/status', methods=['GET'])
def entry_status():
    """Get entry point status"""
    return jsonify(entry.get_status())

@app.route('/entry/stats', methods=['GET'])
def entry_stats():
    """Get execution statistics"""
    return jsonify(entry.get_stats())

@app.route('/entry/health', methods=['GET'])
def entry_health():
    """Health check"""
    return jsonify({
        "service": "agent-zero-unified-entry-point",
        "status": "healthy",
        "label": entry.config.label,
        "version": entry.config.version,
        "info": entry.config.info
    })

if __name__ == '__main__':
    print(f"Starting Unified Entry Point (Agent Zero {config.version})")
    print(f"Primary Mode: {config.primary_mode.value}")
    print(f"Fallback Enabled: {config.fallback_enabled}")
    print(f"Python Autonomous: {config.python_url}")
    print(f"Docker v1.3 UI: {config.docker_url}")
    app.run(host='0.0.0.0', port=7777, debug=False)
