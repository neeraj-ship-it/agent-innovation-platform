import { Agent } from '../models/Agent.js';

export class AgentRegistry {
  static register({ name, capabilities, endpoint }) {
    try {
      // Check if agent already exists
      const existing = Agent.findByName(name);
      if (existing) {
        // Update status to online
        return Agent.updateStatus(existing.id, 'online');
      }

      // Create new agent
      return Agent.create({ name, capabilities, endpoint });
    } catch (error) {
      throw new Error(`Failed to register agent: ${error.message}`);
    }
  }

  static getAgent(id) {
    const agent = Agent.findById(id);
    if (!agent) {
      throw new Error('Agent not found');
    }
    return agent;
  }

  static getAllAgents() {
    return Agent.findAll();
  }

  static getOnlineAgents() {
    return Agent.getOnlineAgents();
  }

  static setAgentStatus(id, status) {
    if (!['online', 'offline', 'busy'].includes(status)) {
      throw new Error('Invalid status');
    }
    return Agent.updateStatus(id, status);
  }

  static disconnect(id) {
    return Agent.updateStatus(id, 'offline');
  }

  static findAgentsByCapability(capability) {
    const agents = Agent.getOnlineAgents();
    return agents.filter(agent =>
      agent.capabilities.includes(capability)
    );
  }

  static getAgentStats() {
    const all = Agent.findAll();
    const online = Agent.getOnlineAgents();

    return {
      total: all.length,
      online: online.length,
      offline: all.length - online.length,
      capabilities: this.aggregateCapabilities(all)
    };
  }

  static aggregateCapabilities(agents) {
    const capabilities = {};
    agents.forEach(agent => {
      agent.capabilities.forEach(cap => {
        capabilities[cap] = (capabilities[cap] || 0) + 1;
      });
    });
    return capabilities;
  }
}
