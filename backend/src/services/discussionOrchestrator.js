import { Discussion } from '../models/Discussion.js';
import { Agent } from '../models/Agent.js';

export class DiscussionOrchestrator {
  static createDiscussion({ topic }) {
    try {
      return Discussion.create({ topic });
    } catch (error) {
      throw new Error(`Failed to create discussion: ${error.message}`);
    }
  }

  static getDiscussion(id) {
    const discussion = Discussion.findById(id);
    if (!discussion) {
      throw new Error('Discussion not found');
    }
    return discussion;
  }

  static getAllDiscussions() {
    return Discussion.findAll();
  }

  static getActiveDiscussions() {
    return Discussion.getActive();
  }

  static closeDiscussion(id) {
    return Discussion.updateStatus(id, 'closed');
  }

  static addMessage({ discussionId, agentId, content }) {
    const discussion = Discussion.findById(discussionId);
    if (!discussion) {
      throw new Error('Discussion not found');
    }

    const agent = Agent.findById(agentId);
    if (!agent) {
      throw new Error('Agent not found');
    }

    if (discussion.status !== 'active') {
      throw new Error('Discussion is not active');
    }

    return Discussion.addMessage({ discussionId, agentId, content });
  }

  static getMessages(discussionId, limit = 100) {
    return Discussion.getMessages(discussionId, limit);
  }

  static getDiscussionStats(discussionId) {
    const messages = Discussion.getMessages(discussionId);
    const agentCounts = {};

    messages.forEach(msg => {
      agentCounts[msg.agent_name] = (agentCounts[msg.agent_name] || 0) + 1;
    });

    return {
      total_messages: messages.length,
      participants: Object.keys(agentCounts).length,
      message_distribution: agentCounts
    };
  }

  static suggestRelevantAgents(discussionId) {
    const discussion = Discussion.findById(discussionId);
    if (!discussion) {
      return [];
    }

    // Get online agents
    const onlineAgents = Agent.getOnlineAgents();

    // Get agents already in discussion
    const messages = Discussion.getMessages(discussionId);
    const activeAgentIds = new Set(messages.map(m => m.agent_id));

    // Return agents not yet in discussion
    return onlineAgents.filter(agent => !activeAgentIds.has(agent.id));
  }
}
