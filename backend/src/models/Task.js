import db from './Database.js';

export class Task {
  static create({ title, description, creatorAgentId, priority = 0 }) {
    return db.insert('tasks', {
      title,
      description,
      creator_agent_id: creatorAgentId,
      assigned_agent_id: null,
      status: 'pending',
      priority,
      completed_at: null
    });
  }

  static findById(id) {
    const task = db.findById('tasks', id);
    if (task) {
      return this._enrichTask(task);
    }
    return null;
  }

  static findAll() {
    return db.findAll('tasks')
      .map(t => this._enrichTask(t))
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  static findPending() {
    return db.findAll('tasks', t => t.status === 'pending')
      .map(t => this._enrichTask(t))
      .sort((a, b) => b.priority - a.priority || new Date(a.created_at) - new Date(b.created_at));
  }

  static updateStatus(id, status) {
    const updates = { status };
    if (status === 'completed') {
      updates.completed_at = new Date().toISOString();
    }
    const task = db.update('tasks', id, updates);
    return task ? this._enrichTask(task) : null;
  }

  static assignToAgent(id, agentId) {
    const task = db.update('tasks', id, {
      assigned_agent_id: agentId,
      status: 'in_progress'
    });
    return task ? this._enrichTask(task) : null;
  }

  static complete(id, result = null) {
    const task = db.update('tasks', id, {
      status: 'completed',
      completed_at: new Date().toISOString()
    });
    return task ? this._enrichTask(task) : null;
  }

  static getByAgent(agentId) {
    return db.findAll('tasks', t => t.assigned_agent_id === agentId)
      .map(t => this._enrichTask(t))
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  static delete(id) {
    return db.delete('tasks', id);
  }

  static _enrichTask(task) {
    const creatorAgent = task.creator_agent_id ? db.findById('agents', task.creator_agent_id) : null;
    const assignedAgent = task.assigned_agent_id ? db.findById('agents', task.assigned_agent_id) : null;

    return {
      ...task,
      creator_name: creatorAgent ? creatorAgent.name : null,
      assigned_name: assignedAgent ? assignedAgent.name : null
    };
  }
}
