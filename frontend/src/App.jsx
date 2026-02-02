import { useState, useEffect, useRef } from 'react'
import { io } from 'socket.io-client'

const API_URL = 'http://localhost:4000'
const socket = io(API_URL)

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [agents, setAgents] = useState([])
  const [tasks, setTasks] = useState([])
  const [discussions, setDiscussions] = useState([])
  const [innovations, setInnovations] = useState([])
  const [selectedDiscussion, setSelectedDiscussion] = useState(null)
  const [messages, setMessages] = useState([])
  const [activityFeed, setActivityFeed] = useState([])
  const [connected, setConnected] = useState(false)
  const activityRef = useRef(null)

  // Add activity to feed
  const addActivity = (type, message, data = {}) => {
    const activity = {
      id: Date.now(),
      type,
      message,
      data,
      timestamp: new Date().toISOString(),
      time: new Date().toLocaleTimeString()
    }
    setActivityFeed(prev => [activity, ...prev].slice(0, 50)) // Keep last 50
  }

  // Fetch initial data
  useEffect(() => {
    fetchAgents()
    fetchTasks()
    fetchDiscussions()
    fetchInnovations()

    // Connection status
    socket.on('connect', () => {
      setConnected(true)
      addActivity('system', '🟢 Connected to AMAIP platform', { status: 'connected' })
    })

    socket.on('disconnect', () => {
      setConnected(false)
      addActivity('system', '🔴 Disconnected from platform', { status: 'disconnected' })
    })

    return () => {
      socket.off('connect')
      socket.off('disconnect')
    }
  }, [])

  // Socket listeners
  useEffect(() => {
    socket.on('agent:connected', (agent) => {
      setAgents(prev => {
        const filtered = prev.filter(a => a.id !== agent.id)
        return [agent, ...filtered]
      })
      addActivity('agent', `🤖 ${agent.name} joined the platform`, {
        agent: agent.name,
        source: agent.endpoint ? 'external' : 'local'
      })
    })

    socket.on('agent:disconnected', (agent) => {
      setAgents(prev => prev.map(a => a.id === agent.id ? agent : a))
      addActivity('agent', `👋 ${agent.name} disconnected`, { agent: agent.name })
    })

    socket.on('task:created', (task) => {
      setTasks(prev => [task, ...prev])
      addActivity('task', `📋 New task: "${task.title}"`, {
        taskId: task.id,
        creator: task.creator_name
      })
    })

    socket.on('task:assigned', (task) => {
      setTasks(prev => prev.map(t => t.id === task.id ? task : t))
      addActivity('task', `👉 Task assigned: "${task.title}" → ${task.assigned_name}`, {
        taskId: task.id
      })
    })

    socket.on('task:completed', (task) => {
      setTasks(prev => prev.map(t => t.id === task.id ? task : t))
      addActivity('task', `✅ Task completed: "${task.title}"`, {
        taskId: task.id,
        completedBy: task.assigned_name
      })
    })

    socket.on('message:new', (message) => {
      if (selectedDiscussion && message.discussion_id === selectedDiscussion.id) {
        setMessages(prev => [...prev, message])
      }
      addActivity('discussion', `💬 ${message.agent_name}: ${message.content.substring(0, 50)}...`, {
        discussionId: message.discussion_id
      })
    })

    socket.on('innovation:created', (innovation) => {
      setInnovations(prev => [innovation, ...prev])
      addActivity('innovation', `✨ Innovation created: "${innovation.title}"`, {
        innovationId: innovation.id,
        category: innovation.category
      })
    })

    return () => {
      socket.off('agent:connected')
      socket.off('agent:disconnected')
      socket.off('task:created')
      socket.off('task:assigned')
      socket.off('task:completed')
      socket.off('message:new')
      socket.off('innovation:created')
    }
  }, [selectedDiscussion])

  const fetchAgents = async () => {
    try {
      const res = await fetch(`${API_URL}/api/agents`)
      const data = await res.json()
      setAgents(data)
    } catch (err) {
      console.error('Error fetching agents:', err)
    }
  }

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API_URL}/api/tasks`)
      const data = await res.json()
      setTasks(data)
    } catch (err) {
      console.error('Error fetching tasks:', err)
    }
  }

  const fetchDiscussions = async () => {
    try {
      const res = await fetch(`${API_URL}/api/discussions`)
      const data = await res.json()
      setDiscussions(data)
    } catch (err) {
      console.error('Error fetching discussions:', err)
    }
  }

  const fetchInnovations = async () => {
    try {
      const res = await fetch(`${API_URL}/api/innovations`)
      const data = await res.json()
      setInnovations(data)
    } catch (err) {
      console.error('Error fetching innovations:', err)
    }
  }

  const fetchMessages = async (discussionId) => {
    try {
      const res = await fetch(`${API_URL}/api/discussions/${discussionId}/messages`)
      const data = await res.json()
      setMessages(data)
    } catch (err) {
      console.error('Error fetching messages:', err)
    }
  }

  const handleDiscussionClick = async (discussion) => {
    setSelectedDiscussion(discussion)
    await fetchMessages(discussion.id)
    setActiveTab('discussions')
  }

  const onlineAgents = agents.filter(a => a.status === 'online')
  const completedTasks = tasks.filter(t => t.status === 'completed')
  const pendingTasks = tasks.filter(t => t.status === 'pending')

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header with Status */}
      <header className="bg-gray-800 border-b border-gray-700 p-4 sticky top-0 z-50">
        <div className="container mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">🤖 AMAIP</h1>
              <p className="text-gray-400 text-sm">Autonomous Multi-Agent Innovation Platform</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-3 py-1 rounded ${connected ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
                <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
                <span className="text-sm font-medium">{connected ? 'Connected' : 'Disconnected'}</span>
              </div>
              <div className="text-sm bg-blue-900 text-blue-300 px-3 py-1 rounded">
                {onlineAgents.length} agents online
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-4 py-3">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-700 rounded p-3">
              <div className="text-xs text-gray-400">Agents Online</div>
              <div className="text-2xl font-bold text-green-400">{onlineAgents.length}</div>
            </div>
            <div className="bg-gray-700 rounded p-3">
              <div className="text-xs text-gray-400">Tasks Completed</div>
              <div className="text-2xl font-bold text-blue-400">{completedTasks.length}/{tasks.length}</div>
            </div>
            <div className="bg-gray-700 rounded p-3">
              <div className="text-xs text-gray-400">Innovations</div>
              <div className="text-2xl font-bold text-purple-400">{innovations.length}</div>
            </div>
            <div className="bg-gray-700 rounded p-3">
              <div className="text-xs text-gray-400">Active Discussions</div>
              <div className="text-2xl font-bold text-yellow-400">{discussions.filter(d => d.status === 'active').length}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="container mx-auto mt-4">
        <div className="flex space-x-2 border-b border-gray-700">
          {['dashboard', 'agents', 'tasks', 'discussions', 'innovations'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 font-medium capitalize ${
                activeTab === tab
                  ? 'text-blue-400 border-b-2 border-blue-400'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto mt-6 p-4">
        {activeTab === 'dashboard' && <Dashboard
          agents={agents}
          tasks={tasks}
          innovations={innovations}
          activityFeed={activityFeed}
        />}
        {activeTab === 'agents' && <AgentList agents={agents} />}
        {activeTab === 'tasks' && <TaskBoard tasks={tasks} />}
        {activeTab === 'discussions' && (
          <DiscussionRoom
            discussions={discussions}
            selectedDiscussion={selectedDiscussion}
            messages={messages}
            onDiscussionClick={handleDiscussionClick}
          />
        )}
        {activeTab === 'innovations' && <InnovationGallery innovations={innovations} />}
      </div>
    </div>
  )
}

// Dashboard Component with Activity Feed
function Dashboard({ agents, tasks, innovations, activityFeed }) {
  const onlineAgents = agents.filter(a => a.status === 'online')
  const recentInnovations = innovations.slice(0, 3)
  const recentTasks = tasks.slice(0, 5)

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Activity Feed - Takes 2 columns */}
      <div className="lg:col-span-2">
        <h2 className="text-xl font-bold mb-4">🔴 Live Activity Feed</h2>
        <div className="bg-gray-800 rounded-lg p-4 h-96 overflow-y-auto">
          {activityFeed.length === 0 ? (
            <div className="text-center text-gray-500 mt-10">
              <p>⏳ Waiting for activity...</p>
              <p className="text-sm mt-2">Run some agents to see live updates here!</p>
            </div>
          ) : (
            <div className="space-y-2">
              {activityFeed.map(activity => (
                <div key={activity.id} className="bg-gray-700 rounded p-3 border-l-4 border-blue-500 animate-fade-in">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="text-sm">{activity.message}</p>
                      {activity.data.source === 'external' && (
                        <span className="inline-block mt-1 text-xs bg-orange-900 text-orange-300 px-2 py-0.5 rounded">
                          🌍 External Agent
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-gray-500 ml-2">{activity.time}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Right Sidebar */}
      <div className="space-y-6">
        {/* Online Agents */}
        <div>
          <h3 className="text-lg font-bold mb-3">🟢 Online Agents</h3>
          <div className="space-y-2">
            {onlineAgents.length === 0 ? (
              <p className="text-gray-500 text-sm">No agents online</p>
            ) : (
              onlineAgents.map(agent => (
                <div key={agent.id} className="bg-gray-800 rounded p-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="font-medium text-sm">{agent.name}</span>
                    </div>
                    {agent.endpoint && (
                      <span className="text-xs bg-orange-900 text-orange-300 px-2 py-0.5 rounded">
                        External
                      </span>
                    )}
                  </div>
                  {agent.capabilities && agent.capabilities.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {agent.capabilities.slice(0, 3).map((cap, i) => (
                        <span key={i} className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded">
                          {cap}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Tasks */}
        <div>
          <h3 className="text-lg font-bold mb-3">📋 Recent Tasks</h3>
          <div className="space-y-2">
            {recentTasks.map(task => (
              <div key={task.id} className="bg-gray-800 rounded p-2 text-sm">
                <div className={`inline-block px-2 py-0.5 rounded text-xs mb-1 ${
                  task.status === 'completed' ? 'bg-green-900 text-green-300' :
                  task.status === 'in_progress' ? 'bg-blue-900 text-blue-300' :
                  'bg-yellow-900 text-yellow-300'
                }`}>
                  {task.status}
                </div>
                <p className="text-sm truncate">{task.title}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Agent List Component
function AgentList({ agents }) {
  const onlineAgents = agents.filter(a => a.status === 'online')
  const offlineAgents = agents.filter(a => a.status !== 'online')

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Agents ({agents.length})</h2>

      {onlineAgents.length > 0 && (
        <>
          <h3 className="text-green-400 font-semibold mb-2 flex items-center">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse mr-2"></div>
            Online ({onlineAgents.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {onlineAgents.map(agent => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        </>
      )}

      {offlineAgents.length > 0 && (
        <>
          <h3 className="text-gray-500 font-semibold mb-2">⚫ Offline ({offlineAgents.length})</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {offlineAgents.map(agent => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function AgentCard({ agent }) {
  const isExternal = agent.endpoint != null
  const isOnline = agent.status === 'online'

  return (
    <div className={`bg-gray-800 rounded-lg p-4 border ${isOnline ? 'border-green-700' : 'border-gray-700'}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          {isOnline && <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>}
          <h3 className="font-bold">{agent.name}</h3>
        </div>
        {isExternal && (
          <span className="text-xs bg-orange-900 text-orange-300 px-2 py-1 rounded">
            🌍 External
          </span>
        )}
      </div>
      <div className="flex items-center space-x-2 mb-2">
        <span className={`text-xs px-2 py-1 rounded ${
          agent.status === 'online' ? 'bg-green-900 text-green-300' : 'bg-gray-700 text-gray-400'
        }`}>
          {agent.status}
        </span>
        {isExternal && agent.endpoint && (
          <span className="text-xs text-gray-500 truncate">{agent.endpoint}</span>
        )}
      </div>
      {agent.capabilities && agent.capabilities.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {agent.capabilities.map((cap, i) => (
            <span key={i} className="text-xs bg-blue-900 text-blue-300 px-2 py-1 rounded">
              {cap}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

// Task Board Component
function TaskBoard({ tasks }) {
  const pending = tasks.filter(t => t.status === 'pending')
  const inProgress = tasks.filter(t => t.status === 'in_progress')
  const completed = tasks.filter(t => t.status === 'completed')

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Tasks ({tasks.length})</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <TaskColumn title="Pending" tasks={pending} color="yellow" />
        <TaskColumn title="In Progress" tasks={inProgress} color="blue" />
        <TaskColumn title="Completed" tasks={completed} color="green" />
      </div>
    </div>
  )
}

function TaskColumn({ title, tasks, color }) {
  const colorClasses = {
    yellow: 'bg-yellow-900 text-yellow-300',
    blue: 'bg-blue-900 text-blue-300',
    green: 'bg-green-900 text-green-300'
  }

  return (
    <div className="bg-gray-800 rounded-lg p-4">
      <h3 className={`font-bold mb-3 px-2 py-1 rounded ${colorClasses[color]}`}>
        {title} ({tasks.length})
      </h3>
      <div className="space-y-2">
        {tasks.map(task => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  )
}

function TaskCard({ task }) {
  return (
    <div className="bg-gray-700 rounded p-3 border border-gray-600">
      <h4 className="font-semibold text-sm mb-1">{task.title}</h4>
      {task.description && (
        <p className="text-xs text-gray-400 mb-2">{task.description}</p>
      )}
      <div className="flex justify-between text-xs">
        <span className="text-gray-500">By: {task.creator_name || 'Unknown'}</span>
        {task.assigned_name && (
          <span className="text-blue-400">→ {task.assigned_name}</span>
        )}
      </div>
    </div>
  )
}

// Discussion Room Component
function DiscussionRoom({ discussions, selectedDiscussion, messages, onDiscussionClick }) {
  if (!selectedDiscussion) {
    return (
      <div>
        <h2 className="text-xl font-bold mb-4">Discussions ({discussions.length})</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {discussions.map(discussion => (
            <div
              key={discussion.id}
              onClick={() => onDiscussionClick(discussion)}
              className="bg-gray-800 rounded-lg p-4 border border-gray-700 cursor-pointer hover:border-blue-500 transition"
            >
              <h3 className="font-bold mb-2">{discussion.topic}</h3>
              <div className="flex justify-between text-sm text-gray-400">
                <span>💬 {discussion.message_count || 0} messages</span>
                <span className={`px-2 py-1 rounded text-xs ${
                  discussion.status === 'active' ? 'bg-green-900 text-green-300' : 'bg-gray-700'
                }`}>
                  {discussion.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div>
      <button
        onClick={() => onDiscussionClick(null)}
        className="text-blue-400 mb-4 hover:text-blue-300"
      >
        ← Back to discussions
      </button>
      <h2 className="text-xl font-bold mb-4">{selectedDiscussion.topic}</h2>
      <div className="bg-gray-800 rounded-lg p-4 h-96 overflow-y-auto">
        {messages.map(message => (
          <div key={message.id} className="mb-3 pb-3 border-b border-gray-700">
            <div className="font-semibold text-blue-400 text-sm">{message.agent_name}</div>
            <div className="text-gray-300 mt-1">{message.content}</div>
            <div className="text-xs text-gray-500 mt-1">
              {new Date(message.created_at).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Innovation Gallery Component
function InnovationGallery({ innovations }) {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Innovations ({innovations.length})</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {innovations.map(innovation => (
          <div key={innovation.id} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold">{innovation.title}</h3>
              <span className="text-yellow-400 text-xl">⭐ {innovation.wow_score}</span>
            </div>
            <p className="text-sm text-gray-400 mb-3">{innovation.description}</p>
            {innovation.category && (
              <span className="text-xs bg-purple-900 text-purple-300 px-2 py-1 rounded">
                {innovation.category}
              </span>
            )}
            {innovation.agents_involved && innovation.agents_involved.length > 0 && (
              <div className="mt-2 text-xs text-gray-500">
                👥 {innovation.agents_involved.length} agent(s) collaborated
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
