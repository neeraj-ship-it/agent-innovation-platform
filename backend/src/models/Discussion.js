import db from './Database.js';

export class Discussion {
  static create({ topic }) {
    return db.insert('discussions', {
      topic,
      status: 'active'
    });
  }

  static findById(id) {
    return db.findById('discussions', id);
  }

  static findAll() {
    return db.findAll('discussions')
      .map(d => {
        const messageCount = db.count('messages', m => m.discussion_id === d.id);
        return { ...d, message_count: messageCount };
      })
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  static getActive() {
    return db.findAll('discussions', d => d.status === 'active')
      .map(d => {
        const messageCount = db.count('messages', m => m.discussion_id === d.id);
        return { ...d, message_count: messageCount };
      })
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  static updateStatus(id, status) {
    return db.update('discussions', id, { status });
  }

  static addMessage({ discussionId, agentId, content }) {
    const message = db.insert('messages', {
      discussion_id: discussionId,
      agent_id: agentId,
      content
    });
    return this.getMessageById(message.id);
  }

  static getMessageById(id) {
    const message = db.findById('messages', id);
    if (message) {
      const agent = db.findById('agents', message.agent_id);
      return {
        ...message,
        agent_name: agent ? agent.name : null
      };
    }
    return null;
  }

  static getMessages(discussionId, limit = 100) {
    return db.findAll('messages', m => m.discussion_id === discussionId)
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
      .slice(-limit)
      .map(m => {
        const agent = db.findById('agents', m.agent_id);
        return {
          ...m,
          agent_name: agent ? agent.name : null
        };
      });
  }

  static delete(id) {
    // Delete messages first
    const messages = db.findAll('messages', m => m.discussion_id === id);
    messages.forEach(m => db.delete('messages', m.id));
    // Then delete discussion
    return db.delete('discussions', id);
  }
}
