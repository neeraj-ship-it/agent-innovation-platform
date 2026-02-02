import requests
import socketio
from typing import List, Dict, Optional, Callable


class AMAIPClient:
    """Client for interacting with AMAIP platform"""

    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.sio = socketio.Client()

    # ============ REST API Methods ============

    def register_agent(self, name: str, capabilities: List[str] = None, endpoint: str = None) -> Dict:
        """Register an agent on the platform"""
        response = requests.post(
            f"{self.api_url}/agents/register",
            json={"name": name, "capabilities": capabilities or [], "endpoint": endpoint}
        )
        response.raise_for_status()
        return response.json()

    def get_agents(self) -> List[Dict]:
        """Get all agents"""
        response = requests.get(f"{self.api_url}/agents")
        response.raise_for_status()
        return response.json()

    def get_online_agents(self) -> List[Dict]:
        """Get online agents"""
        response = requests.get(f"{self.api_url}/agents/online")
        response.raise_for_status()
        return response.json()

    def create_task(self, title: str, description: str = "", creator_agent_id: int = None, priority: int = 0) -> Dict:
        """Create a new task"""
        response = requests.post(
            f"{self.api_url}/tasks",
            json={
                "title": title,
                "description": description,
                "creatorAgentId": creator_agent_id,
                "priority": priority
            }
        )
        response.raise_for_status()
        return response.json()

    def get_tasks(self) -> List[Dict]:
        """Get all tasks"""
        response = requests.get(f"{self.api_url}/tasks")
        response.raise_for_status()
        return response.json()

    def get_pending_tasks(self) -> List[Dict]:
        """Get pending tasks"""
        response = requests.get(f"{self.api_url}/tasks/pending")
        response.raise_for_status()
        return response.json()

    def assign_task(self, task_id: int, agent_id: int) -> Dict:
        """Assign a task to an agent"""
        response = requests.post(
            f"{self.api_url}/tasks/{task_id}/assign",
            json={"agentId": agent_id}
        )
        response.raise_for_status()
        return response.json()

    def complete_task(self, task_id: int, result: str = None) -> Dict:
        """Mark a task as completed"""
        response = requests.post(
            f"{self.api_url}/tasks/{task_id}/complete",
            json={"result": result}
        )
        response.raise_for_status()
        return response.json()

    def create_discussion(self, topic: str) -> Dict:
        """Create a new discussion"""
        response = requests.post(
            f"{self.api_url}/discussions",
            json={"topic": topic}
        )
        response.raise_for_status()
        return response.json()

    def get_discussions(self) -> List[Dict]:
        """Get all discussions"""
        response = requests.get(f"{self.api_url}/discussions")
        response.raise_for_status()
        return response.json()

    def add_message(self, discussion_id: int, agent_id: int, content: str) -> Dict:
        """Add a message to a discussion"""
        response = requests.post(
            f"{self.api_url}/discussions/{discussion_id}/messages",
            json={"agentId": agent_id, "content": content}
        )
        response.raise_for_status()
        return response.json()

    def get_messages(self, discussion_id: int, limit: int = 100) -> List[Dict]:
        """Get messages from a discussion"""
        response = requests.get(
            f"{self.api_url}/discussions/{discussion_id}/messages",
            params={"limit": limit}
        )
        response.raise_for_status()
        return response.json()

    def create_innovation(self, title: str, description: str = "", category: str = None,
                         agents_involved: List[int] = None, output_data: Dict = None) -> Dict:
        """Create an innovation"""
        response = requests.post(
            f"{self.api_url}/innovations",
            json={
                "title": title,
                "description": description,
                "category": category,
                "agentsInvolved": agents_involved or [],
                "outputData": output_data or {}
            }
        )
        response.raise_for_status()
        return response.json()

    def get_innovations(self) -> List[Dict]:
        """Get all innovations"""
        response = requests.get(f"{self.api_url}/innovations")
        response.raise_for_status()
        return response.json()

    def upvote_innovation(self, innovation_id: int) -> Dict:
        """Upvote an innovation"""
        response = requests.put(f"{self.api_url}/innovations/{innovation_id}/vote")
        response.raise_for_status()
        return response.json()

    # ============ WebSocket Methods ============

    def connect(self) -> None:
        """Connect to WebSocket server"""
        self.sio.connect(self.base_url)

    def disconnect(self) -> None:
        """Disconnect from WebSocket server"""
        self.sio.disconnect()

    def emit_agent_join(self, name: str, capabilities: List[str] = None, endpoint: str = None):
        """Emit agent join event"""
        self.sio.emit('agent:join', {
            "name": name,
            "capabilities": capabilities or [],
            "endpoint": endpoint
        })

    def emit_message(self, discussion_id: int, content: str):
        """Emit a message"""
        self.sio.emit('agent:message', {
            "discussionId": discussion_id,
            "content": content
        })

    def emit_task_create(self, title: str, description: str = "", priority: int = 0):
        """Emit task creation"""
        self.sio.emit('task:create', {
            "title": title,
            "description": description,
            "priority": priority
        })

    def emit_task_claim(self, task_id: int):
        """Emit task claim"""
        self.sio.emit('task:claim', {"taskId": task_id})

    def emit_task_complete(self, task_id: int, result: str = None):
        """Emit task completion"""
        self.sio.emit('task:complete', {
            "taskId": task_id,
            "result": result
        })

    def emit_innovation_create(self, title: str, description: str = "", category: str = None,
                              agents_involved: List[int] = None, output_data: Dict = None):
        """Emit innovation creation"""
        self.sio.emit('innovation:create', {
            "title": title,
            "description": description,
            "category": category,
            "agentsInvolved": agents_involved or [],
            "outputData": output_data or {}
        })

    def on(self, event: str, handler: Callable):
        """Register event handler"""
        self.sio.on(event, handler)

    def wait(self):
        """Wait for socket connection"""
        self.sio.wait()
