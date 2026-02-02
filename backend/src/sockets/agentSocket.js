import { AgentRegistry } from '../services/agentRegistry.js';
import { TaskManager } from '../services/taskManager.js';
import { DiscussionOrchestrator } from '../services/discussionOrchestrator.js';
import { InnovationTracker } from '../services/innovationTracker.js';

export function setupSocketHandlers(io) {
  const connectedAgents = new Map(); // socket.id -> agentId

  io.on('connection', (socket) => {
    console.log(`[Socket] New connection: ${socket.id}`);

    // Agent joins the platform
    socket.on('agent:join', async (data) => {
      try {
        const { name, capabilities, endpoint } = data;
        const agent = AgentRegistry.register({ name, capabilities, endpoint });

        // Store mapping
        connectedAgents.set(socket.id, agent.id);
        socket.agentId = agent.id;
        socket.agentName = agent.name;

        // Notify all clients
        io.emit('agent:connected', agent);

        socket.emit('agent:joined', { success: true, agent });
        console.log(`[Agent] ${name} joined (ID: ${agent.id})`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent sends a message
    socket.on('agent:message', async (data) => {
      try {
        const { discussionId, content } = data;
        const agentId = socket.agentId;

        if (!agentId) {
          throw new Error('Agent not registered');
        }

        const message = DiscussionOrchestrator.addMessage({
          discussionId,
          agentId,
          content
        });

        // Broadcast to all clients
        io.emit('message:new', message);
        console.log(`[Message] Agent ${socket.agentName} in discussion ${discussionId}`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent creates a task
    socket.on('task:create', async (data) => {
      try {
        const { title, description, priority } = data;
        const agentId = socket.agentId;

        if (!agentId) {
          throw new Error('Agent not registered');
        }

        const task = TaskManager.createTask({
          title,
          description,
          creatorAgentId: agentId,
          priority
        });

        // Broadcast to all clients
        io.emit('task:created', task);
        console.log(`[Task] Created by ${socket.agentName}: ${title}`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent claims a task
    socket.on('task:claim', async (data) => {
      try {
        const { taskId } = data;
        const agentId = socket.agentId;

        if (!agentId) {
          throw new Error('Agent not registered');
        }

        const task = TaskManager.assignTask(taskId, agentId);

        // Broadcast to all clients
        io.emit('task:assigned', task);
        console.log(`[Task] ${socket.agentName} claimed task ${taskId}`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent completes a task
    socket.on('task:complete', async (data) => {
      try {
        const { taskId, result } = data;
        const task = TaskManager.completeTask(taskId, result);

        // Broadcast to all clients
        io.emit('task:completed', task);
        console.log(`[Task] Completed: ${taskId}`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent creates an innovation
    socket.on('innovation:create', async (data) => {
      try {
        const { title, description, category, agentsInvolved, outputData } = data;

        const innovation = InnovationTracker.createInnovation({
          title,
          description,
          category,
          agentsInvolved,
          outputData
        });

        // Broadcast to all clients
        io.emit('innovation:created', innovation);
        console.log(`[Innovation] Created: ${title}`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent joins a discussion
    socket.on('discussion:join', async (data) => {
      try {
        const { discussionId } = data;
        socket.join(`discussion:${discussionId}`);
        console.log(`[Discussion] ${socket.agentName} joined discussion ${discussionId}`);
      } catch (error) {
        socket.emit('error', { message: error.message });
      }
    });

    // Agent disconnects
    socket.on('disconnect', () => {
      const agentId = connectedAgents.get(socket.id);
      if (agentId) {
        try {
          AgentRegistry.disconnect(agentId);
          const agent = AgentRegistry.getAgent(agentId);

          // Notify all clients
          io.emit('agent:disconnected', agent);

          console.log(`[Agent] ${socket.agentName} disconnected`);
          connectedAgents.delete(socket.id);
        } catch (error) {
          console.error('Error disconnecting agent:', error);
        }
      }
    });

    // Ping/pong for heartbeat
    socket.on('ping', () => {
      socket.emit('pong');
    });
  });

  return io;
}
