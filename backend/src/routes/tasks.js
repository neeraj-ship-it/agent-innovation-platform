import express from 'express';
import { TaskManager } from '../services/taskManager.js';

const router = express.Router();

// Create a new task
router.post('/', (req, res) => {
  try {
    const { title, description, creatorAgentId, priority } = req.body;

    if (!title) {
      return res.status(400).json({ error: 'Task title is required' });
    }

    const task = TaskManager.createTask({
      title,
      description,
      creatorAgentId,
      priority
    });

    // Emit socket event to notify all connected agents
    if (req.io) {
      req.io.emit('task:created', task);
      console.log(`[Socket] Emitted task:created for: ${title}`);
    }

    res.status(201).json(task);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all tasks
router.get('/', (req, res) => {
  try {
    const tasks = TaskManager.getAllTasks();
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get pending tasks
router.get('/pending', (req, res) => {
  try {
    const tasks = TaskManager.getPendingTasks();
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get task by ID
router.get('/:id', (req, res) => {
  try {
    const task = TaskManager.getTask(parseInt(req.params.id));
    res.json(task);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

// Update task
router.put('/:id', (req, res) => {
  try {
    const { status } = req.body;
    const task = TaskManager.updateTaskStatus(parseInt(req.params.id), status);
    res.json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Assign task to agent
router.post('/:id/assign', (req, res) => {
  try {
    const { agentId } = req.body;

    if (!agentId) {
      return res.status(400).json({ error: 'Agent ID is required' });
    }

    const task = TaskManager.assignTask(parseInt(req.params.id), agentId);
    res.json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Auto-assign task
router.post('/:id/auto-assign', (req, res) => {
  try {
    const task = TaskManager.autoAssignTask(parseInt(req.params.id));
    res.json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Complete task
router.post('/:id/complete', (req, res) => {
  try {
    const { result } = req.body;
    const task = TaskManager.completeTask(parseInt(req.params.id), result);
    res.json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get tasks by agent
router.get('/agent/:agentId', (req, res) => {
  try {
    const tasks = TaskManager.getTasksByAgent(parseInt(req.params.agentId));
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get task stats
router.get('/stats/all', (req, res) => {
  try {
    const stats = TaskManager.getTaskStats();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
