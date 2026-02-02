import db from './Database.js';

export class Innovation {
  static create({ title, description, category, agentsInvolved = [], outputData = {} }) {
    return db.insert('innovations', {
      title,
      description,
      category,
      agents_involved: agentsInvolved,
      output_data: outputData,
      wow_score: 0
    });
  }

  static findById(id) {
    return db.findById('innovations', id);
  }

  static findAll() {
    return db.findAll('innovations')
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  static getByCategory(category) {
    return db.findAll('innovations', i => i.category === category)
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  static getTopRated(limit = 10) {
    return db.findAll('innovations')
      .sort((a, b) => b.wow_score - a.wow_score || new Date(b.created_at) - new Date(a.created_at))
      .slice(0, limit);
  }

  static upvote(id) {
    const innovation = db.findById('innovations', id);
    if (innovation) {
      return db.update('innovations', id, {
        wow_score: innovation.wow_score + 1
      });
    }
    return null;
  }

  static delete(id) {
    return db.delete('innovations', id);
  }
}
