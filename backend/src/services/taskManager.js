import { Task } from '../models/Task.js';
import { Agent } from '../models/Agent.js';

export class TaskManager {
  static createTask({ title, description, creatorAgentId, priority = 0 }) {
    try {
      return Task.create({ title, description, creatorAgentId, priority });
    } catch (error) {
      throw new Error(`Failed to create task: ${error.message}`);
    }
  }

  static getTask(id) {
    const task = Task.findById(id);
    if (!task) {
      throw new Error('Task not found');
    }
    return task;
  }

  static getAllTasks() {
    return Task.findAll();
  }

  static getPendingTasks() {
    return Task.findPending();
  }

  static assignTask(taskId, agentId) {
    const task = Task.findById(taskId);
    if (!task) {
      throw new Error('Task not found');
    }

    if (task.status !== 'pending') {
      throw new Error('Task is not available for assignment');
    }

    const agent = Agent.findById(agentId);
    if (!agent) {
      throw new Error('Agent not found');
    }

    return Task.assignToAgent(taskId, agentId);
  }

  static updateTaskStatus(taskId, status) {
    if (!['pending', 'in_progress', 'completed', 'cancelled'].includes(status)) {
      throw new Error('Invalid task status');
    }

    return Task.updateStatus(taskId, status);
  }

  static completeTask(taskId, result = null) {
    const task = Task.findById(taskId);
    if (!task) {
      throw new Error('Task not found');
    }

    if (task.status === 'completed') {
      throw new Error('Task is already completed');
    }

    return Task.complete(taskId, result);
  }

  static getTasksByAgent(agentId) {
    return Task.getByAgent(agentId);
  }

  static findBestAgentForTask(taskId) {
    const task = Task.findById(taskId);
    if (!task) {
      throw new Error('Task not found');
    }

    // Get online agents
    const onlineAgents = Agent.getOnlineAgents();

    if (onlineAgents.length === 0) {
      return null;
    }

    // Simple algorithm: Return agent with least tasks
    const agentTaskCounts = {};
    onlineAgents.forEach(agent => {
      const tasks = Task.getByAgent(agent.id);
      const activeTasks = tasks.filter(t => t.status !== 'completed');
      agentTaskCounts[agent.id] = activeTasks.length;
    });

    // Find agent with minimum tasks
    const bestAgentId = Object.keys(agentTaskCounts).reduce((a, b) =>
      agentTaskCounts[a] < agentTaskCounts[b] ? a : b
    );

    return Agent.findById(parseInt(bestAgentId));
  }

  static autoAssignTask(taskId) {
    const bestAgent = this.findBestAgentForTask(taskId);
    if (!bestAgent) {
      throw new Error('No available agents for task assignment');
    }

    return this.assignTask(taskId, bestAgent.id);
  }

  static getTaskStats() {
    const all = Task.findAll();
    const pending = Task.findPending();

    const completed = all.filter(t => t.status === 'completed');
    const inProgress = all.filter(t => t.status === 'in_progress');

    return {
      total: all.length,
      pending: pending.length,
      in_progress: inProgress.length,
      completed: completed.length
    };
  }
}
