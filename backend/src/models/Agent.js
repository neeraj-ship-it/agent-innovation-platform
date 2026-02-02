import db from './Database.js';

export class Agent {
  static create({ name, capabilities = [], endpoint = null }) {
    return db.insert('agents', {
      name,
      capabilities,
      endpoint,
      status: 'online',
      last_seen: new Date().toISOString()
    });
  }

  static findById(id) {
    return db.findById('agents', id);
  }

  static findByName(name) {
    return db.findOne('agents', agent => agent.name === name);
  }

  static findAll() {
    return db.findAll('agents').sort((a, b) =>
      new Date(b.created_at) - new Date(a.created_at)
    );
  }

  static updateStatus(id, status) {
    return db.update('agents', id, {
      status,
      last_seen: new Date().toISOString()
    });
  }

  static getOnlineAgents() {
    return db.findAll('agents', agent => agent.status === 'online')
      .sort((a, b) => new Date(b.last_seen) - new Date(a.last_seen));
  }

  static delete(id) {
    return db.delete('agents', id);
  }
}

export { db };
