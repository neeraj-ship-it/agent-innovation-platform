import React, { useState, useEffect } from 'react';

/**
 * Advanced Analytics Dashboard Component
 * Visualizes agent performance, task flow, and innovation metrics
 */

function AnalyticsDashboard({ agents, tasks, innovations }) {
  const [stats, setStats] = useState({
    taskCompletionRate: 0,
    avgTasksPerAgent: 0,
    activeRate: 0,
    innovationRate: 0
  });

  const [topPerformers, setTopPerformers] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    calculateStats();
    findTopPerformers();
  }, [agents, tasks, innovations]);

  const calculateStats = () => {
    const completedTasks = tasks.filter(t => t.status === 'completed');
    const taskCompletionRate = tasks.length > 0 ? (completedTasks.length / tasks.length * 100).toFixed(1) : 0;
    const avgTasksPerAgent = agents.length > 0 ? (tasks.length / agents.length).toFixed(1) : 0;
    const activeAgents = agents.filter(a => a.status === 'online');
    const activeRate = agents.length > 0 ? (activeAgents.length / agents.length * 100).toFixed(0) : 0;
    const innovationRate = tasks.length > 0 ? (innovations.length / tasks.length * 100).toFixed(1) : 0;

    setStats({
      taskCompletionRate,
      avgTasksPerAgent,
      activeRate,
      innovationRate
    });
  };

  const findTopPerformers = () => {
    // Count tasks per agent
    const agentTaskCount = {};
    tasks.forEach(task => {
      if (task.assigned_agent_id) {
        agentTaskCount[task.assigned_agent_id] = (agentTaskCount[task.assigned_agent_id] || 0) + 1;
      }
    });

    // Create leaderboard
    const performers = agents.map(agent => ({
      ...agent,
      taskCount: agentTaskCount[agent.id] || 0,
      completedCount: tasks.filter(t => t.assigned_agent_id === agent.id && t.status === 'completed').length
    })).sort((a, b) => b.completedCount - a.completedCount);

    setTopPerformers(performers.slice(0, 5));
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-white mb-4">📊 Analytics Dashboard</h2>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          title="Task Completion"
          value={`${stats.taskCompletionRate}%`}
          icon="✅"
          color="green"
        />
        <MetricCard
          title="Avg Tasks/Agent"
          value={stats.avgTasksPerAgent}
          icon="📋"
          color="blue"
        />
        <MetricCard
          title="Agent Activity"
          value={`${stats.activeRate}%`}
          icon="🟢"
          color="yellow"
        />
        <MetricCard
          title="Innovation Rate"
          value={`${stats.innovationRate}%`}
          icon="✨"
          color="purple"
        />
      </div>

      {/* Task Status Distribution */}
      <div className="bg-gray-700 rounded p-4">
        <h3 className="text-lg font-semibold text-white mb-3">📊 Task Distribution</h3>
        <TaskDistributionChart tasks={tasks} />
      </div>

      {/* Leaderboard */}
      <div className="bg-gray-700 rounded p-4">
        <h3 className="text-lg font-semibold text-white mb-3">🏆 Top Performers</h3>
        <Leaderboard performers={topPerformers} />
      </div>

      {/* Agent Network Graph */}
      <div className="bg-gray-700 rounded p-4">
        <h3 className="text-lg font-semibold text-white mb-3">🕸️ Agent Collaboration Network</h3>
        <CollaborationNetwork agents={agents} tasks={tasks} />
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, color }) {
  const colorClasses = {
    green: 'from-green-600 to-green-800',
    blue: 'from-blue-600 to-blue-800',
    yellow: 'from-yellow-600 to-yellow-800',
    purple: 'from-purple-600 to-purple-800'
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-lg p-4`}>
      <div className="text-3xl mb-2">{icon}</div>
      <div className="text-2xl font-bold text-white">{value}</div>
      <div className="text-sm text-gray-200">{title}</div>
    </div>
  );
}

function TaskDistributionChart({ tasks }) {
  const pending = tasks.filter(t => t.status === 'pending').length;
  const inProgress = tasks.filter(t => t.status === 'in_progress').length;
  const completed = tasks.filter(t => t.status === 'completed').length;
  const total = tasks.length || 1;

  const pendingPercent = (pending / total) * 100;
  const inProgressPercent = (inProgress / total) * 100;
  const completedPercent = (completed / total) * 100;

  return (
    <div className="space-y-3">
      <div className="space-y-1">
        <div className="flex justify-between text-sm text-gray-300">
          <span>📝 Pending</span>
          <span>{pending} ({pendingPercent.toFixed(0)}%)</span>
        </div>
        <div className="w-full bg-gray-600 rounded-full h-3">
          <div
            className="bg-yellow-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${pendingPercent}%` }}
          />
        </div>
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-sm text-gray-300">
          <span>⚡ In Progress</span>
          <span>{inProgress} ({inProgressPercent.toFixed(0)}%)</span>
        </div>
        <div className="w-full bg-gray-600 rounded-full h-3">
          <div
            className="bg-blue-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${inProgressPercent}%` }}
          />
        </div>
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-sm text-gray-300">
          <span>✅ Completed</span>
          <span>{completed} ({completedPercent.toFixed(0)}%)</span>
        </div>
        <div className="w-full bg-gray-600 rounded-full h-3">
          <div
            className="bg-green-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${completedPercent}%` }}
          />
        </div>
      </div>
    </div>
  );
}

function Leaderboard({ performers }) {
  if (performers.length === 0) {
    return <p className="text-gray-400">No data yet. Agents will appear here as they complete tasks!</p>;
  }

  const medals = ['🥇', '🥈', '🥉', '🏅', '🏅'];

  return (
    <div className="space-y-2">
      {performers.map((agent, index) => (
        <div
          key={agent.id}
          className="bg-gray-800 rounded p-3 flex items-center justify-between hover:bg-gray-750 transition-colors"
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">{medals[index]}</span>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-white">{agent.name}</span>
                {agent.endpoint && (
                  <span className="text-xs bg-orange-900 text-orange-200 px-2 py-0.5 rounded">
                    🌍 External
                  </span>
                )}
                {agent.status === 'online' && (
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                )}
              </div>
              <div className="text-sm text-gray-400">
                {agent.capabilities?.slice(0, 3).join(', ')}
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xl font-bold text-green-400">{agent.completedCount}</div>
            <div className="text-xs text-gray-400">tasks completed</div>
          </div>
        </div>
      ))}
    </div>
  );
}

function CollaborationNetwork({ agents, tasks }) {
  // Simple visualization of agent collaboration
  const collaborations = {};

  tasks.forEach(task => {
    const creator = task.creator_agent_id;
    const assignee = task.assigned_agent_id;

    if (creator && assignee && creator !== assignee) {
      const key = [creator, assignee].sort().join('-');
      collaborations[key] = (collaborations[key] || 0) + 1;
    }
  });

  const collaborationCount = Object.keys(collaborations).length;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {agents.slice(0, 8).map((agent, i) => (
          <div
            key={agent.id}
            className="bg-gray-800 rounded p-2 text-center relative"
            style={{
              animation: `pulse ${2 + i * 0.3}s ease-in-out infinite`
            }}
          >
            <div className="text-2xl mb-1">🤖</div>
            <div className="text-xs text-gray-300 truncate">{agent.name}</div>
            {agent.status === 'online' && (
              <div className="absolute top-1 right-1 w-2 h-2 bg-green-500 rounded-full" />
            )}
          </div>
        ))}
      </div>

      <div className="text-center p-4 bg-gray-800 rounded">
        <div className="text-3xl font-bold text-blue-400">{collaborationCount}</div>
        <div className="text-sm text-gray-400">Active Collaborations</div>
      </div>

      <div className="text-xs text-gray-500 text-center">
        Network visualization shows agent connections through task collaboration
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
