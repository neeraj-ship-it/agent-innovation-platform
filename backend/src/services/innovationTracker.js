import { Innovation } from '../models/Innovation.js';
import { Agent } from '../models/Agent.js';

export class InnovationTracker {
  static createInnovation({ title, description, category, agentsInvolved = [], outputData = {} }) {
    try {
      return Innovation.create({
        title,
        description,
        category,
        agentsInvolved,
        outputData
      });
    } catch (error) {
      throw new Error(`Failed to create innovation: ${error.message}`);
    }
  }

  static getInnovation(id) {
    const innovation = Innovation.findById(id);
    if (!innovation) {
      throw new Error('Innovation not found');
    }
    return innovation;
  }

  static getAllInnovations() {
    return Innovation.findAll();
  }

  static getByCategory(category) {
    return Innovation.getByCategory(category);
  }

  static getTopInnovations(limit = 10) {
    return Innovation.getTopRated(limit);
  }

  static upvote(id) {
    const innovation = Innovation.findById(id);
    if (!innovation) {
      throw new Error('Innovation not found');
    }
    return Innovation.upvote(id);
  }

  static categorizeInnovation(innovation) {
    const { title, description } = innovation;
    const text = `${title} ${description}`.toLowerCase();

    // Simple keyword-based categorization
    if (text.includes('automat') || text.includes('workflow')) {
      return 'automation';
    } else if (text.includes('tool') || text.includes('utility')) {
      return 'tools';
    } else if (text.includes('ai') || text.includes('ml') || text.includes('model')) {
      return 'ai-ml';
    } else if (text.includes('api') || text.includes('service')) {
      return 'services';
    } else if (text.includes('ui') || text.includes('interface') || text.includes('dashboard')) {
      return 'interfaces';
    } else if (text.includes('data') || text.includes('analyt')) {
      return 'data-analytics';
    } else {
      return 'general';
    }
  }

  static getInnovationStats() {
    const all = Innovation.findAll();

    const byCategory = {};
    all.forEach(innovation => {
      const cat = innovation.category || 'uncategorized';
      byCategory[cat] = (byCategory[cat] || 0) + 1;
    });

    const totalWowScore = all.reduce((sum, inn) => sum + inn.wow_score, 0);

    return {
      total: all.length,
      by_category: byCategory,
      average_wow_score: all.length > 0 ? totalWowScore / all.length : 0,
      top_innovations: Innovation.getTopRated(5)
    };
  }

  static getAgentContributions(agentId) {
    const all = Innovation.findAll();
    const agentInnovations = all.filter(innovation =>
      innovation.agents_involved.includes(agentId)
    );

    return {
      total_contributions: agentInnovations.length,
      innovations: agentInnovations
    };
  }
}
