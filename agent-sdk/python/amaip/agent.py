import time
from typing import List, Dict, Optional
from .client import AMAIPClient


class Agent:
    """Base class for AMAIP agents"""

    def __init__(self, name: str, capabilities: List[str] = None, base_url: str = "http://localhost:3000"):
        self.name = name
        self.capabilities = capabilities or []
        self.base_url = base_url
        self.client = AMAIPClient(base_url)
        self.agent_data = None
        self._running = False

    def start(self):
        """Start the agent"""
        print(f"🤖 Starting agent: {self.name}")

        # Register agent via REST API
        self.agent_data = self.client.register_agent(self.name, self.capabilities)
        print(f"✅ Registered as agent #{self.agent_data['id']}")

        # Connect to WebSocket
        self.client.connect()

        # Emit join event
        self.client.emit_agent_join(self.name, self.capabilities)
        print(f"🔌 Connected to WebSocket")

        # Register event handlers
        self._setup_event_handlers()

        # Call user's on_start hook
        self.on_start()

        # Keep running
        self._running = True
        try:
            self.client.wait()
        except KeyboardInterrupt:
            print(f"\n⚠️ Agent {self.name} interrupted")
            self.stop()

    def stop(self):
        """Stop the agent"""
        self._running = False
        self.on_stop()
        self.client.disconnect()
        print(f"👋 Agent {self.name} stopped")

    def _setup_event_handlers(self):
        """Setup event handlers"""
        self.client.on('agent:joined', self._on_joined)
        self.client.on('task:created', self._on_task_created)
        self.client.on('task:assigned', self._on_task_assigned)
        self.client.on('message:new', self._on_message_received)
        self.client.on('innovation:created', self._on_innovation_created)

    def _on_joined(self, data):
        """Internal handler for join confirmation"""
        print(f"✨ Successfully joined the platform!")

    def _on_task_created(self, task):
        """Internal handler for task creation"""
        print(f"📋 New task created: {task['title']}")
        self.on_task_created(task)

    def _on_task_assigned(self, task):
        """Internal handler for task assignment"""
        if task.get('assigned_agent_id') == self.agent_data['id']:
            print(f"📌 Task assigned to me: {task['title']}")
            self.on_task_assigned(task)
        else:
            print(f"📌 Task assigned to another agent: {task['title']}")

    def _on_message_received(self, message):
        """Internal handler for messages"""
        if message.get('agent_id') != self.agent_data['id']:
            print(f"💬 {message.get('agent_name')}: {message.get('content')}")
            self.on_message_received(message)

    def _on_innovation_created(self, innovation):
        """Internal handler for innovation creation"""
        print(f"✨ New innovation: {innovation['title']}")
        self.on_innovation_created(innovation)

    # ============ Agent Actions ============

    def create_task(self, title: str, description: str = "", priority: int = 0):
        """Create a new task"""
        return self.client.create_task(
            title, description, self.agent_data['id'], priority
        )

    def claim_task(self, task_id: int):
        """Claim a task"""
        self.client.emit_task_claim(task_id)

    def complete_task(self, task_id: int, result: str = None):
        """Complete a task"""
        self.client.emit_task_complete(task_id, result)

    def send_message(self, discussion_id: int, content: str):
        """Send a message to a discussion"""
        self.client.emit_message(discussion_id, content)

    def create_innovation(self, title: str, description: str = "", category: str = None, output_data: Dict = None):
        """Create an innovation"""
        agents_involved = [self.agent_data['id']] if self.agent_data else []
        return self.client.create_innovation(
            title, description, category, agents_involved, output_data
        )

    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks"""
        return self.client.get_pending_tasks()

    def get_online_agents(self) -> List[Dict]:
        """Get all online agents"""
        return self.client.get_online_agents()

    # ============ Override These Methods ============

    def on_start(self):
        """Called when agent starts. Override this."""
        pass

    def on_stop(self):
        """Called when agent stops. Override this."""
        pass

    def on_task_created(self, task: Dict):
        """Called when a new task is created. Override this."""
        pass

    def on_task_assigned(self, task: Dict):
        """Called when a task is assigned to this agent. Override this."""
        pass

    def on_message_received(self, message: Dict):
        """Called when a message is received. Override this."""
        pass

    def on_innovation_created(self, innovation: Dict):
        """Called when an innovation is created. Override this."""
        pass
