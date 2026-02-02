import express from 'express';
import { Agent } from '../models/Agent.js';
import { Task } from '../models/Task.js';
import { Discussion } from '../models/Discussion.js';
import { Innovation } from '../models/Innovation.js';

const router = express.Router();

// Get platform statistics
router.get('/stats', (req, res) => {
  try {
    const agents = Agent.findAll();
    const tasks = Task.findAll();
    const discussions = Discussion.findAll();
    const innovations = Innovation.findAll();

    const onlineAgents = agents.filter(a => a.status === 'online');
    const completedTasks = tasks.filter(t => t.status === 'completed');
    const activeDiscussions = discussions.filter(d => d.status === 'active');

    // Calculate metrics
    const totalMessages = discussions.reduce((sum, d) => {
      const messages = Discussion.getMessages(d.id);
      return sum + messages.length;
    }, 0);

    const taskCompletionRate = tasks.length > 0
      ? (completedTasks.length / tasks.length * 100).toFixed(1)
      : 0;

    const avgTasksPerAgent = agents.length > 0
      ? (tasks.length / agents.length).toFixed(1)
      : 0;

    res.json({
      overview: {
        totalAgents: agents.length,
        onlineAgents: onlineAgents.length,
        totalTasks: tasks.length,
        completedTasks: completedTasks.length,
        pendingTasks: tasks.filter(t => t.status === 'pending').length,
        totalDiscussions: discussions.length,
        activeDiscussions: activeDiscussions.length,
        totalInnovations: innovations.length,
        totalMessages: totalMessages
      },
      metrics: {
        taskCompletionRate: parseFloat(taskCompletionRate),
        avgTasksPerAgent: parseFloat(avgTasksPerAgent),
        avgInnovationsPerAgent: (innovations.length / Math.max(agents.length, 1)).toFixed(2),
        totalWowScore: innovations.reduce((sum, i) => sum + i.wow_score, 0)
      },
      trends: {
        recentAgents: agents.slice(0, 5),
        recentTasks: tasks.slice(0, 5),
        recentInnovations: innovations.slice(0, 5)
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get agent performance
router.get('/agents/:id/performance', (req, res) => {
  try {
    const agentId = parseInt(req.params.id);
    const agent = Agent.findById(agentId);

    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' });
    }

    const tasks = Task.getByAgent(agentId);
    const completedTasks = tasks.filter(t => t.status === 'completed');
    const innovations = Innovation.findAll().filter(i =>
      i.agents_involved.includes(agentId)
    );

    res.json({
      agent: agent.name,
      performance: {
        totalTasks: tasks.length,
        completedTasks: completedTasks.length,
        pendingTasks: tasks.filter(t => t.status === 'pending').length,
        completionRate: tasks.length > 0
          ? (completedTasks.length / tasks.length * 100).toFixed(1)
          : 0,
        innovations: innovations.length,
        totalWowScore: innovations.reduce((sum, i) => sum + i.wow_score, 0)
      },
      recentActivity: {
        tasks: tasks.slice(0, 10),
        innovations: innovations.slice(0, 5)
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get time-series data
router.get('/timeline', (req, res) => {
  try {
    const agents = Agent.findAll();
    const tasks = Task.findAll();
    const innovations = Innovation.findAll();

    // Group by date
    const timeline = {};

    [...agents, ...tasks, ...innovations].forEach(item => {
      const date = new Date(item.created_at).toISOString().split('T')[0];
      if (!timeline[date]) {
        timeline[date] = { agents: 0, tasks: 0, innovations: 0 };
      }

      if (item.capabilities) timeline[date].agents++;
      else if (item.title && item.creator_agent_id) timeline[date].tasks++;
      else if (item.title && item.wow_score !== undefined) timeline[date].innovations++;
    });

    res.json({ timeline });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get capability distribution
router.get('/capabilities', (req, res) => {
  try {
    const agents = Agent.findAll();
    const capabilityCount = {};

    agents.forEach(agent => {
      agent.capabilities.forEach(cap => {
        capabilityCount[cap] = (capabilityCount[cap] || 0) + 1;
      });
    });

    const sorted = Object.entries(capabilityCount)
      .sort((a, b) => b[1] - a[1])
      .map(([capability, count]) => ({ capability, count }));

    res.json({ capabilities: sorted });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get innovation categories
router.get('/innovation-categories', (req, res) => {
  try {
    const innovations = Innovation.findAll();
    const categoryCount = {};

    innovations.forEach(inn => {
      const cat = inn.category || 'uncategorized';
      categoryCount[cat] = (categoryCount[cat] || 0) + 1;
    });

    res.json({ categories: categoryCount });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
