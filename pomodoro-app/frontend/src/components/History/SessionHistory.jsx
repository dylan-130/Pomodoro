

import React, { useEffect, useState } from 'react';
import { api } from '../../utils/api';

const SessionHistory = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await api.get('/sessions');
        setSessions(response.data);
      } catch (err) {
        setError('Failed to load session history');
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, []);

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Session History</h2>
      {loading ? (
        <p className="text-gray-600 dark:text-gray-400">Loading...</p>
      ) : error ? (
        <p className="text-red-600 dark:text-red-400">{error}</p>
      ) : sessions.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No sessions found.</p>
      ) : (
        <ul className="space-y-4">
          {sessions.map((session) => (
            <li
              key={session.id}
              className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 shadow-sm bg-white dark:bg-gray-800"
            >
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {new Date(session.start_time).toLocaleString()}
              </div>
              <div className="text-lg font-medium text-gray-900 dark:text-white capitalize">
                {session.session_type}
              </div>
              <div className="text-sm text-gray-700 dark:text-gray-300">
                Duration: {Math.round(session.duration / 60)} minutes
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SessionHistory;