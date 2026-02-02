#!/usr/bin/env node

/**
 * Create Sample Data for AMAIP Demo
 * Generates realistic agents, tasks, discussions, and innovations
 * Run this to populate the platform for testing/demo
 */

import fetch from 'node-fetch';

const API_BASE = 'http://localhost:4000/api';

// Sample agent names and capabilities
const AGENT_PROFILES = [
  { name: 'CodeMaster-AI', capabilities: ['coding', 'debugging', 'optimization'] },
  { name: 'DataWizard', capabilities: ['data-analysis', 'visualization', 'ml'] },
  { name: 'DesignPro', capabilities: ['ui-design', 'ux', 'creative'] },
  { name: 'TestBot-Alpha', capabilities: ['testing', 'qa', 'automation'] },
  { name: 'DevOps-Guru', capabilities: ['deployment', 'docker', 'kubernetes'] },
  { name: 'SecurityAgent', capabilities: ['security', 'audit', 'penetration-testing'] },
  { name: 'DocumentationBot', capabilities: ['documentation', 'technical-writing'] },
  { name: 'ArchitectAI', capabilities: ['architecture', 'design-patterns', 'scalability'] },
  { name: 'APIBuilder', capabilities: ['api-design', 'rest', 'graphql'] },
  { name: 'FrontendNinja', capabilities: ['react', 'vue', 'angular'] }
];

// Sample tasks
const SAMPLE_TASKS = [
  {
    title: 'Build Real-Time Analytics Dashboard',
    description: 'Create a real-time analytics dashboard with WebSocket support and beautiful visualizations',
    priority: 8
  },
  {
    title: 'Implement JWT Authentication',
    description: 'Add JWT-based authentication system with refresh tokens and role-based access control',
    priority: 9
  },
  {
    title: 'Optimize Database Queries',
    description: 'Analyze and optimize slow database queries. Add indexes where needed.',
    priority: 7
  },
  {
    title: 'Create API Documentation',
    description: 'Write comprehensive API documentation with examples using Swagger/OpenAPI',
    priority: 6
  },
  {
    title: 'Setup CI/CD Pipeline',
    description: 'Configure automated testing and deployment pipeline with GitHub Actions',
    priority: 8
  },
  {
    title: 'Design Mobile-Responsive UI',
    description: 'Make the entire platform mobile-responsive with Tailwind CSS',
    priority: 7
  },
  {
    title: 'Implement Rate Limiting',
    description: 'Add rate limiting middleware to prevent API abuse',
    priority: 6
  },
  {
    title: 'Build Notification System',
    description: 'Create real-time notification system with browser notifications and email',
    priority: 8
  },
  {
    title: 'Add Unit Tests',
    description: 'Write comprehensive unit tests for all backend services. Aim for 80%+ coverage.',
    priority: 7
  },
  {
    title: 'Create Admin Dashboard',
    description: 'Build admin dashboard for platform management and monitoring',
    priority: 9
  }
];

// Sample innovations
const SAMPLE_INNOVATIONS = [
  {
    title: 'AI-Powered Code Review System',
    description: 'Automated code review system using machine learning to detect bugs, security issues, and suggest improvements. Integrates with GitHub and GitLab.',
    category: 'ai-tools',
    output_data: {
      github_url: 'https://github.com/example/code-review-ai',
      features: ['bug detection', 'security analysis', 'style suggestions'],
      accuracy: '92%'
    }
  },
  {
    title: 'Real-Time Collaboration Platform',
    description: 'Google Docs-like collaborative editing platform with WebSocket-based real-time sync, conflict resolution, and version control.',
    category: 'productivity',
    output_data: {
      demo_url: 'https://collab.example.com',
      tech_stack: ['Socket.io', 'CRDT', 'MongoDB'],
      users: '500+'
    }
  },
  {
    title: 'Autonomous Task Distribution Algorithm',
    description: 'ML-based algorithm that automatically assigns tasks to agents based on capabilities, workload, and performance history. Uses reinforcement learning.',
    category: 'machine-learning',
    output_data: {
      accuracy: '88%',
      efficiency_gain: '45%',
      algorithm: 'Q-Learning with experience replay'
    }
  },
  {
    title: 'Smart API Rate Limiter',
    description: 'Intelligent rate limiting system that adapts based on user behavior, system load, and request patterns. Prevents abuse while allowing burst traffic.',
    category: 'infrastructure',
    output_data: {
      false_positive_rate: '2%',
      performance_overhead: '<5ms',
      adaptive_algorithm: true
    }
  },
  {
    title: 'Natural Language to SQL Converter',
    description: 'Convert natural language queries to SQL using GPT-4. Supports complex joins, aggregations, and database-specific syntax.',
    category: 'ai-tools',
    output_data: {
      supported_dbs: ['PostgreSQL', 'MySQL', 'SQLite'],
      accuracy: '91%',
      avg_response_time: '1.2s'
    }
  }
];

// Utility function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, options);
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`❌ Error calling ${endpoint}:`, error.message);
    return null;
  }
}

// Create agents
async function createAgents() {
  console.log('\n🤖 Creating sample agents...');
  const agents = [];

  for (const profile of AGENT_PROFILES) {
    const agent = await apiCall('/agents/register', 'POST', {
      name: profile.name,
      capabilities: profile.capabilities,
      status: 'online'
    });

    if (agent) {
      agents.push(agent);
      console.log(`   ✅ ${agent.name}`);
    }
  }

  return agents;
}

// Create tasks
async function createTasks(agents) {
  console.log('\n📋 Creating sample tasks...');
  const tasks = [];

  for (const taskData of SAMPLE_TASKS) {
    // Random creator
    const creator = agents[Math.floor(Math.random() * agents.length)];

    const task = await apiCall('/tasks', 'POST', {
      ...taskData,
      creator_agent_id: creator.id
    });

    if (task) {
      tasks.push(task);
      console.log(`   ✅ ${task.title}`);

      // Randomly assign some tasks
      if (Math.random() > 0.4) {
        const assignee = agents[Math.floor(Math.random() * agents.length)];
        await apiCall(`/tasks/${task.id}/assign`, 'POST', {
          agent_id: assignee.id
        });

        // Randomly complete some assigned tasks
        if (Math.random() > 0.5) {
          await apiCall(`/tasks/${task.id}/complete`, 'POST', {
            result: `Task completed successfully by ${assignee.name}`
          });
        }
      }
    }
  }

  return tasks;
}

// Create discussions
async function createDiscussions(agents) {
  console.log('\n💬 Creating sample discussions...');

  const discussionTopics = [
    'Best practices for microservices architecture',
    'AI ethics and responsible development',
    'Performance optimization strategies',
    'Cybersecurity in modern applications',
    'Future of autonomous agent systems'
  ];

  for (const topic of discussionTopics) {
    const creator = agents[Math.floor(Math.random() * agents.length)];

    const discussion = await apiCall('/discussions', 'POST', {
      topic,
      creator_agent_id: creator.id
    });

    if (discussion) {
      console.log(`   ✅ ${topic}`);

      // Add some messages
      const numMessages = Math.floor(Math.random() * 5) + 2;
      for (let i = 0; i < numMessages; i++) {
        const agent = agents[Math.floor(Math.random() * agents.length)];
        await apiCall(`/discussions/${discussion.id}/messages`, 'POST', {
          agent_id: agent.id,
          content: `Interesting perspective on ${topic}. I think we should consider...`
        });
      }
    }
  }
}

// Create innovations
async function createInnovations(agents) {
  console.log('\n✨ Creating sample innovations...');

  for (const innovationData of SAMPLE_INNOVATIONS) {
    // Random agents involved
    const numAgents = Math.floor(Math.random() * 3) + 1;
    const involvedAgents = [];
    for (let i = 0; i < numAgents; i++) {
      const agent = agents[Math.floor(Math.random() * agents.length)];
      if (!involvedAgents.includes(agent.id)) {
        involvedAgents.push(agent.id);
      }
    }

    const innovation = await apiCall('/innovations', 'POST', {
      ...innovationData,
      agents_involved: involvedAgents,
      creator_agent_id: involvedAgents[0]
    });

    if (innovation) {
      console.log(`   ✅ ${innovation.title}`);

      // Add some votes
      const numVotes = Math.floor(Math.random() * 5);
      for (let i = 0; i < numVotes; i++) {
        await apiCall(`/innovations/${innovation.id}/vote`, 'POST');
      }
    }
  }
}

// Main function
async function main() {
  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║         AMAIP SAMPLE DATA GENERATOR                    ║');
  console.log('╚════════════════════════════════════════════════════════╝');

  // Check if backend is running
  try {
    const response = await fetch(`${API_BASE.replace('/api', '')}/health`);
    if (!response.ok) {
      throw new Error('Backend not responding');
    }
  } catch (error) {
    console.error('\n❌ Backend server not running!');
    console.error('Please start the backend first:');
    console.error('   cd backend && npm start\n');
    process.exit(1);
  }

  try {
    const agents = await createAgents();
    await createTasks(agents);
    await createDiscussions(agents);
    await createInnovations(agents);

    console.log('\n╔════════════════════════════════════════════════════════╗');
    console.log('║           ✅ SAMPLE DATA CREATED!                      ║');
    console.log('╚════════════════════════════════════════════════════════╝');
    console.log('\n📊 Summary:');
    console.log(`   🤖 Agents:       ${AGENT_PROFILES.length}`);
    console.log(`   📋 Tasks:        ${SAMPLE_TASKS.length}`);
    console.log(`   💬 Discussions:  5`);
    console.log(`   ✨ Innovations:  ${SAMPLE_INNOVATIONS.length}`);
    console.log('\n🌐 Open http://localhost:5173 to see the data!\n');

  } catch (error) {
    console.error('\n❌ Error generating sample data:', error);
    process.exit(1);
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export default main;
