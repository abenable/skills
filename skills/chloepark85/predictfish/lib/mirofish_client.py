"""MiroFish API Client"""
import os
import io
import time
import requests
from typing import Dict, Any, Optional


class MiroFishClient:
    """Client for MiroFish swarm intelligence API"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("MIROFISH_URL", "http://localhost:5001")
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check MiroFish API health status"""
        try:
            # Try project list as health check
            response = self.session.get(f"{self.base_url}/api/graph/project/list", timeout=5)
            response.raise_for_status()
            return {"status": "ok", "url": self.base_url}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": "Cannot connect to MiroFish (is Docker running?)"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def create_project(self, seed_text: str, project_name: str, simulation_requirement: str, retries: int = 3) -> Dict[str, Any]:
        """Step 1: Upload seed text and generate ontology (with retries for LLM JSON errors)"""
        for attempt in range(retries):
            files = {
                'files': ('seed.txt', io.BytesIO(seed_text.encode('utf-8')), 'text/plain')
            }
            data = {
                'simulation_requirement': simulation_requirement,
                'project_name': project_name,
                'additional_context': 'Market success prediction simulation'
            }
            response = self.session.post(
                f"{self.base_url}/api/graph/ontology/generate",
                files=files,
                data=data,
                timeout=120
            )
            if response.status_code == 500 and attempt < retries - 1:
                time.sleep(3)
                continue
            response.raise_for_status()
            return response.json()
        response.raise_for_status()
        return response.json()
    
    def build_graph(self, project_id: str) -> Dict[str, Any]:
        """Step 2: Build knowledge graph from project"""
        payload = {"project_id": project_id}
        response = self.session.post(
            f"{self.base_url}/api/graph/build",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Check async task status"""
        response = self.session.get(f"{self.base_url}/api/graph/task/{task_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    
    def wait_for_task(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """Wait for async task to complete"""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_task_status(task_id)
            data = result.get("data", {})
            status = data.get("status", "")
            if status in ("completed", "success", "done"):
                return result
            if status in ("failed", "error"):
                raise Exception(f"Task failed: {data.get('error', 'unknown')}")
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {task_id} timed out after {timeout}s")
    
    def prepare_simulation(self, project_id: str) -> Dict[str, Any]:
        """Step 3: Read entities and prepare simulation"""
        # First get project to find graph_id
        response = self.session.get(f"{self.base_url}/api/graph/project/{project_id}", timeout=10)
        response.raise_for_status()
        project = response.json()
        graph_id = project.get("data", {}).get("graph_id", "")
        
        if not graph_id:
            raise Exception("No graph_id found in project")
        
        # Get entities
        response = self.session.get(f"{self.base_url}/api/simulation/entities/{graph_id}", timeout=30)
        response.raise_for_status()
        
        return {"graph_id": graph_id, "entities": response.json()}
    
    def generate_profiles(self, graph_id: str) -> Dict[str, Any]:
        """Step 3b: Generate simulation profiles from graph"""
        payload = {"graph_id": graph_id, "use_llm": True}
        response = self.session.post(
            f"{self.base_url}/api/simulation/generate-profiles",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    
    def create_simulation(self, project_id: str, graph_id: str = "") -> Dict[str, Any]:
        """Step 4a: Create simulation"""
        payload = {"project_id": project_id}
        if graph_id:
            payload["graph_id"] = graph_id
        response = self.session.post(
            f"{self.base_url}/api/simulation/create",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def prepare_sim(self, simulation_id: str) -> Dict[str, Any]:
        """Step 4b: Prepare simulation (async, LLM generates config)"""
        payload = {"simulation_id": simulation_id}
        response = self.session.post(
            f"{self.base_url}/api/simulation/prepare",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_prepare_status(self, simulation_id: str) -> Dict[str, Any]:
        """Check prepare task status"""
        response = self.session.post(
            f"{self.base_url}/api/simulation/prepare/status",
            json={"simulation_id": simulation_id},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def wait_for_prepare(self, simulation_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """Wait for prepare to complete"""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_prepare_status(simulation_id)
            data = result.get("data", {})
            status = data.get("status", "")
            if status in ("completed", "success", "done", "ready"):
                return result
            if status in ("failed", "error"):
                raise Exception(f"Prepare failed: {data.get('error', 'unknown')}")
            time.sleep(poll_interval)
        raise TimeoutError(f"Prepare timed out after {timeout}s")

    def start_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """Step 4c: Start simulation"""
        payload = {"simulation_id": simulation_id}
        response = self.session.post(
            f"{self.base_url}/api/simulation/start",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_run_status(self, simulation_id: str) -> Dict[str, Any]:
        """Get simulation run status"""
        response = self.session.get(
            f"{self.base_url}/api/simulation/{simulation_id}/run-status",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_simulation(self, simulation_id: str, timeout: int = 600, poll_interval: int = 10) -> Dict[str, Any]:
        """Wait for simulation to complete"""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_run_status(simulation_id)
            data = result.get("data", {})
            status = data.get("runner_status", data.get("status", ""))
            if status in ("completed", "finished", "done"):
                return result
            if status in ("failed", "error", "stopped"):
                raise Exception(f"Simulation failed: {data.get('error', status)}")
            time.sleep(poll_interval)
        raise TimeoutError(f"Simulation timed out after {timeout}s")
    
    def generate_report(self, simulation_id: str, project_id: str) -> Dict[str, Any]:
        """Step 5: Generate prediction report (async)"""
        payload = {"simulation_id": simulation_id, "project_id": project_id}
        response = self.session.post(
            f"{self.base_url}/api/report/generate",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        data = result.get("data", {})
        task_id = data.get("task_id")
        report_id = data.get("report_id")
        
        if task_id:
            # Wait for report generation
            start = time.time()
            while time.time() - start < 300:
                status_resp = self.session.post(
                    f"{self.base_url}/api/report/generate/status",
                    json={"task_id": task_id},
                    timeout=10
                )
                status_data = status_resp.json().get("data", {})
                st = status_data.get("status", "")
                if st in ("completed", "done"):
                    break
                if st in ("failed", "error"):
                    raise Exception(f"Report generation failed: {status_data.get('error')}")
                time.sleep(10)
        
        if report_id:
            return self.get_report(report_id)
        return result
    
    def get_report(self, report_id: str) -> Dict[str, Any]:
        """Get generated report"""
        response = self.session.get(f"{self.base_url}/api/report/{report_id}", timeout=10)
        response.raise_for_status()
        return response.json()
