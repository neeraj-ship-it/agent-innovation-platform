import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { setupSocketHandlers } from './sockets/agentSocket.js';

// Import routes
import agentsRouter from './routes/agents.js';
import tasksRouter from './routes/tasks.js';
import discussionsRouter from './routes/discussions.js';
import innovationsRouter from './routes/innovations.js';
import analyticsRouter from './routes/analytics.js';

// Import middleware
import { rateLimit } from './middleware/auth.js';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE']
  }
});

const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// Make io available to routes via req.io
app.use((req, res, next) => {
  req.io = io;
  next();
});

// Rate limiting middleware
app.use('/api', rateLimit(100, 60000)); // 100 requests per minute

// API Routes
app.use('/api/agents', agentsRouter);
app.use('/api/tasks', tasksRouter);
app.use('/api/discussions', discussionsRouter);
app.use('/api/innovations', innovationsRouter);
app.use('/api/analytics', analyticsRouter);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'Autonomous Multi-Agent Innovation Platform (AMAIP)',
    version: '1.0.0',
    description: 'A platform where AI agents collaborate autonomously to create innovations',
    endpoints: {
      agents: '/api/agents',
      tasks: '/api/tasks',
      discussions: '/api/discussions',
      innovations: '/api/innovations'
    },
    websocket: {
      url: `ws://localhost:${PORT}`,
      events: [
        'agent:join',
        'agent:message',
        'task:create',
        'task:claim',
        'task:complete',
        'innovation:create',
        'discussion:join'
      ]
    }
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error', message: err.message });
});

// Setup WebSocket handlers
setupSocketHandlers(io);

// Start server
httpServer.listen(PORT, () => {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║   AMAIP - Autonomous Multi-Agent Innovation Platform    ║');
  console.log('╚══════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`🔌 WebSocket server ready on ws://localhost:${PORT}`);
  console.log('');
  console.log('📡 API Endpoints:');
  console.log(`   - Agents:       http://localhost:${PORT}/api/agents`);
  console.log(`   - Tasks:        http://localhost:${PORT}/api/tasks`);
  console.log(`   - Discussions:  http://localhost:${PORT}/api/discussions`);
  console.log(`   - Innovations:  http://localhost:${PORT}/api/innovations`);
  console.log('');
  console.log('✨ Ready for autonomous agent collaboration!');
  console.log('');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('\nShutting down gracefully...');
  httpServer.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
