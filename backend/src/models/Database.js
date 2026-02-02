import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dbDir = join(__dirname, '../../data');
const dbPath = join(dbDir, 'database.json');

// Ensure data directory exists
if (!existsSync(dbDir)) {
  mkdirSync(dbDir, { recursive: true });
}

// Initialize database structure
const defaultData = {
  agents: [],
  tasks: [],
  discussions: [],
  messages: [],
  innovations: [],
  _counters: {
    agents: 0,
    tasks: 0,
    discussions: 0,
    messages: 0,
    innovations: 0
  }
};

class Database {
  constructor() {
    this.load();
  }

  load() {
    if (existsSync(dbPath)) {
      const data = readFileSync(dbPath, 'utf-8');
      this.data = JSON.parse(data);
    } else {
      this.data = JSON.parse(JSON.stringify(defaultData));
      this.save();
    }
  }

  save() {
    writeFileSync(dbPath, JSON.stringify(this.data, null, 2));
  }

  getNextId(table) {
    this.data._counters[table]++;
    this.save();
    return this.data._counters[table];
  }

  insert(table, record) {
    const id = this.getNextId(table);
    const newRecord = {
      id,
      ...record,
      created_at: new Date().toISOString()
    };
    this.data[table].push(newRecord);
    this.save();
    return newRecord;
  }

  findById(table, id) {
    return this.data[table].find(item => item.id === id);
  }

  findOne(table, predicate) {
    return this.data[table].find(predicate);
  }

  findAll(table, predicate = null) {
    if (predicate) {
      return this.data[table].filter(predicate);
    }
    return [...this.data[table]];
  }

  update(table, id, updates) {
    const index = this.data[table].findIndex(item => item.id === id);
    if (index !== -1) {
      this.data[table][index] = {
        ...this.data[table][index],
        ...updates
      };
      this.save();
      return this.data[table][index];
    }
    return null;
  }

  delete(table, id) {
    const index = this.data[table].findIndex(item => item.id === id);
    if (index !== -1) {
      this.data[table].splice(index, 1);
      this.save();
      return true;
    }
    return false;
  }

  // Convenience methods
  query(table, filter = {}) {
    return this.data[table].filter(item => {
      return Object.keys(filter).every(key => item[key] === filter[key]);
    });
  }

  count(table, predicate = null) {
    if (predicate) {
      return this.data[table].filter(predicate).length;
    }
    return this.data[table].length;
  }

  clear(table) {
    this.data[table] = [];
    this.save();
  }

  reset() {
    this.data = JSON.parse(JSON.stringify(defaultData));
    this.save();
  }
}

// Create singleton instance
const db = new Database();

export default db;
