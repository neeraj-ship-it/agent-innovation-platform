import express from 'express';
import { InnovationTracker } from '../services/innovationTracker.js';
import { scoreInnovation } from '../services/wowScoring.js';

const router = express.Router();

// Create a new innovation
router.post('/', (req, res) => {
  try {
    const { title, description, category, agentsInvolved, outputData } = req.body;

    if (!title) {
      return res.status(400).json({ error: 'Innovation title is required' });
    }

    // Auto-categorize if not provided
    const finalCategory = category || InnovationTracker.categorizeInnovation({ title, description });

    const innovation = InnovationTracker.createInnovation({
      title,
      description,
      category: finalCategory,
      agentsInvolved,
      outputData
    });

    // Calculate WOW score using AI algorithm
    const allInnovations = InnovationTracker.getAllInnovations();
    const scoredInnovation = scoreInnovation(innovation, { innovations: allInnovations });

    // Update innovation with WOW score
    const finalInnovation = {
      ...innovation,
      wow_score: scoredInnovation.wow_score,
      star_rating: scoredInnovation.star_rating,
      wow_level: scoredInnovation.wow_level
    };

    res.status(201).json(finalInnovation);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all innovations
router.get('/', (req, res) => {
  try {
    const innovations = InnovationTracker.getAllInnovations();
    res.json(innovations);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get top innovations
router.get('/top', (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 10;
    const innovations = InnovationTracker.getTopInnovations(limit);
    res.json(innovations);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get innovation by ID
router.get('/:id', (req, res) => {
  try {
    const innovation = InnovationTracker.getInnovation(parseInt(req.params.id));
    res.json(innovation);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

// Get innovations by category
router.get('/category/:category', (req, res) => {
  try {
    const innovations = InnovationTracker.getByCategory(req.params.category);
    res.json(innovations);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Upvote an innovation
router.put('/:id/vote', (req, res) => {
  try {
    const innovation = InnovationTracker.upvote(parseInt(req.params.id));
    res.json(innovation);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

// Get innovation stats
router.get('/stats/all', (req, res) => {
  try {
    const stats = InnovationTracker.getInnovationStats();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get agent contributions
router.get('/agent/:agentId/contributions', (req, res) => {
  try {
    const contributions = InnovationTracker.getAgentContributions(
      parseInt(req.params.agentId)
    );
    res.json(contributions);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
