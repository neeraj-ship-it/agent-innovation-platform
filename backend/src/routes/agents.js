import express from 'express';
import { AgentRegistry } from '../services/agentRegistry.js';

const router = express.Router();

// Register a new agent
router.post('/register', (req, res) => {
  try {
    const { name, capabilities, endpoint } = req.body;

    if (!name) {
      return res.status(400).json({ error: 'Agent name is required' });
    }

    const agent = AgentRegistry.register({ name, capabilities, endpoint });
    res.status(201).json(agent);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all agents
router.get('/', (req, res) => {
  try {
    const agents = AgentRegistry.getAllAgents();
    res.json(agents);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get online agents
router.get('/online', (req, res) => {
  try {
    const agents = AgentRegistry.getOnlineAgents();
    res.json(agents);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get agent by ID
router.get('/:id', (req, res) => {
  try {
    const agent = AgentRegistry.getAgent(parseInt(req.params.id));
    res.json(agent);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

// Update agent status
router.put('/:id/status', (req, res) => {
  try {
    const { status } = req.body;
    const agent = AgentRegistry.setAgentStatus(parseInt(req.params.id), status);
    res.json(agent);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get agents by capability
router.get('/capability/:capability', (req, res) => {
  try {
    const agents = AgentRegistry.findAgentsByCapability(req.params.capability);
    res.json(agents);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get agent stats
router.get('/stats/all', (req, res) => {
  try {
    const stats = AgentRegistry.getAgentStats();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
