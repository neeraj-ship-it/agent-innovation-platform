import express from 'express';
import { DiscussionOrchestrator } from '../services/discussionOrchestrator.js';

const router = express.Router();

// Create a new discussion
router.post('/', (req, res) => {
  try {
    const { topic } = req.body;

    if (!topic) {
      return res.status(400).json({ error: 'Discussion topic is required' });
    }

    const discussion = DiscussionOrchestrator.createDiscussion({ topic });
    res.status(201).json(discussion);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all discussions
router.get('/', (req, res) => {
  try {
    const discussions = DiscussionOrchestrator.getAllDiscussions();
    res.json(discussions);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get active discussions
router.get('/active', (req, res) => {
  try {
    const discussions = DiscussionOrchestrator.getActiveDiscussions();
    res.json(discussions);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get discussion by ID
router.get('/:id', (req, res) => {
  try {
    const discussion = DiscussionOrchestrator.getDiscussion(parseInt(req.params.id));
    res.json(discussion);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

// Close discussion
router.put('/:id/close', (req, res) => {
  try {
    const discussion = DiscussionOrchestrator.closeDiscussion(parseInt(req.params.id));
    res.json(discussion);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Add message to discussion
router.post('/:id/messages', (req, res) => {
  try {
    const { agentId, content } = req.body;

    if (!agentId || !content) {
      return res.status(400).json({ error: 'Agent ID and content are required' });
    }

    const message = DiscussionOrchestrator.addMessage({
      discussionId: parseInt(req.params.id),
      agentId,
      content
    });

    // Emit socket event to notify all connected agents
    if (req.io) {
      req.io.emit('message:new', message);
      console.log(`[Socket] Emitted message:new in discussion ${req.params.id}`);
    }

    res.status(201).json(message);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get messages in discussion
router.get('/:id/messages', (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    const messages = DiscussionOrchestrator.getMessages(parseInt(req.params.id), limit);
    res.json(messages);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get discussion stats
router.get('/:id/stats', (req, res) => {
  try {
    const stats = DiscussionOrchestrator.getDiscussionStats(parseInt(req.params.id));
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get suggested agents for discussion
router.get('/:id/suggest-agents', (req, res) => {
  try {
    const agents = DiscussionOrchestrator.suggestRelevantAgents(parseInt(req.params.id));
    res.json(agents);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
