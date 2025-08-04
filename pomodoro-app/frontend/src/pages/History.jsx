import React, { useState, useEffect } from 'react';
import { Clock, Calendar, TrendingUp, Filter, CheckCircle, Coffee, Book } from 'lucide-react';
import { api } from '../utils/api';

const History = ({ user }) => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'work', 'break', 'completed'
  const [sortBy, setSortBy] = useState('recent'); // 'recent', 'oldest', 'duration'

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await api.get('/timer/sessions');
      setSessions(response.data.sessions);
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredAndSortedSessions = () => {
    let filtered = sessions;

    // Apply filters
    switch (filter) {
      case 'work':
        filtered = sessions.filter(session => session.session_type === 'work');
        break;
      case 'break':
        filtered = sessions.filter(session => session.session_type === 'break');
        break;
      case 'completed':
        filtered = sessions.filter(session => session.completed);
        break;
      default:
        filtered = sessions;
    }

    // Apply sorting
    switch (sortBy) {
      case 'oldest':
        filtered.sort((a, b) => new Date(a.started_at) - new Date(b.started_at));
        break;
      case 'duration':
        filtered.sort((a, b) => b.duration - a.duration);
        break;
      default: // recent
        filtered.sort((a, b) => new Date(b.started_at) - new Date(a.started_at));
    }

    return filtered;
  };

  const getSessionStats = () => {
    const completedSessions = sessions.filter(s => s.completed);
    const workSessions = completedSessions.filter(s => s.session_type === 'work');
    const totalWorkTime = workSessions.reduce((total, session) => total + session.duration, 0);
    const today = new Date().toDateString();
    const todaySessions = completedSessions.filter(s => 
      new Date(s.started_at).toDateString() === today
    );

    return {
      totalSessions: completedSessions.length,
      workSessions: workSessions.length,
      totalWorkTime,
      todaySessions: todaySessions.length,
    };
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDuration = (minutes) => {
    if (minutes < 60) {
      return `${minutes}m`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const stats = getSessionStats();
  const displaySessions = filteredAndSortedSessions();

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="card">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
            ))}
          </div>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="card">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-2"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Session History
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Track your productivity and see your progress over time
        </p>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="stats-card">
          <div className="flex justify-center mb-3">
            <CheckCircle className="h-8 w-8 text-green-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {stats.totalSessions}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Total Completed
          </div>
        </div>

        <div className="stats-card">
          <div className="flex justify-center mb-3">
            <Book className="h-8 w-8 text-primary-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {stats.workSessions}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Work Sessions
          </div>
        </div>

        <div className="stats-card">
          <div className="flex justify-center mb-3">
            <Clock className="h-8 w-8 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {formatDuration(stats.totalWorkTime)}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Total Focus Time
          </div>
        </div>

        <div className="stats-card">
          <div className="flex justify-center mb-3">
            <TrendingUp className="h-8 w-8 text-orange-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {stats.todaySessions}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Today's Sessions
          </div>
        </div>
      </div>

      {/* Filters and Sorting */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col space-y-2">
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Filter:</span>
            </div>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="input-field text-sm py-2 w-full"
            >
              <option value="all">All Sessions</option>
              <option value="work">Work Only</option>
              <option value="break">Breaks Only</option>
              <option value="completed">Completed Only</option>
            </select>
          </div>

          <div className="flex flex-col space-y-2">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Sort by:</span>
            </div>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="input-field text-sm py-2 w-full"
            >
              <option value="recent">Most Recent</option>
              <option value="oldest">Oldest First</option>
              <option value="duration">Duration</option>
            </select>
          </div>
        </div>
      </div>

      {/* Sessions List */}
      {displaySessions.length === 0 ? (
        <div className="card text-center py-12">
          <Clock className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No sessions found
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            {filter === 'all' 
              ? "Start your first Pomodoro session to see your history here."
              : "No sessions match your current filter. Try adjusting your filters."
            }
          </p>
        </div>
      ) : (
        <div className="space-y-4 mb-20">
          {displaySessions.map((session) => (
            <div
              key={session.id}
              className={`card hover:shadow-md transition-shadow border-l-4 ${
                session.session_type === 'work'
                  ? 'border-primary-500'
                  : 'border-green-500'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className={`p-2 rounded-full ${
                    session.session_type === 'work'
                      ? 'bg-primary-100 dark:bg-primary-900'
                      : 'bg-green-100 dark:bg-green-900'
                  }`}>
                    {session.session_type === 'work' ? (
                      <Book className="h-5 w-5 text-primary-500" />
                    ) : (
                      <Coffee className="h-5 w-5 text-green-500" />
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium text-gray-900 dark:text-white capitalize">
                        {session.session_type} Session
                      </h3>
                      <span className={`text-xs px-4 py-2 rounded-full ml-8 ${
                        session.completed
                          ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                          : 'bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300'
                      }`}>
                        {session.completed ? 'Completed' : 'In Progress'}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      Started {formatDate(session.started_at)}
                    </p>
                    {session.completed_at && (
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Completed {formatDate(session.completed_at)}
                      </p>
                    )}
                  </div>
                </div>

                <div className="text-right ml-6">
                  <div className="text-lg font-semibold text-gray-900 dark:text-white">
                    {formatDuration(session.duration)}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Duration
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Weekly Summary */}
      {sessions.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            This Week's Summary
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-xl font-bold text-primary-500">
                {sessions.filter(s => {
                  const sessionDate = new Date(s.started_at);
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return sessionDate >= weekAgo && s.completed && s.session_type === 'work';
                }).length}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Work Sessions</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-green-500">
                {sessions.filter(s => {
                  const sessionDate = new Date(s.started_at);
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return sessionDate >= weekAgo && s.completed && s.session_type === 'break';
                }).length}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Break Sessions</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-blue-500">
                {formatDuration(sessions.filter(s => {
                  const sessionDate = new Date(s.started_at);
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return sessionDate >= weekAgo && s.completed && s.session_type === 'work';
                }).reduce((total, session) => total + session.duration, 0))}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Focus Time</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-orange-500">
                {Math.round(sessions.filter(s => {
                  const sessionDate = new Date(s.started_at);
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return sessionDate >= weekAgo && s.completed;
                }).length / 7)}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Daily Average</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;