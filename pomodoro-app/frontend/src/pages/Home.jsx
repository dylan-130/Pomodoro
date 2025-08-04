import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Clock, TrendingUp, Target, Award } from 'lucide-react';
import { useTimerContext } from '../context/TimerContext';
import { api } from '../utils/api';

const Home = ({ user }) => {
  const {
    timeLeft,
    isActive,
    sessionType,
    completedSessions,
    startTimer,
    pauseTimer,
    resetTimer,
    switchSessionType,
    formatTime,
    getProgressPercentage,
  } = useTimerContext();

  const [stats, setStats] = useState({
    total_sessions: 0,
    total_study_time: 0,
    weekly_sessions: 0,
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const progressPercentage = getProgressPercentage();

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome back, {user.username}!
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Ready to boost your productivity with the Pomodoro Technique?
        </p>
      </div>

      {/* Timer Section */}
      <div className="flex flex-col items-center space-y-8">
        <div className="card max-w-md w-full text-center">
          <div className="mb-6">
            <div className="flex justify-center space-x-4 mb-4">
              <button
                onClick={() => switchSessionType('work')}
                className={`session-type-btn ${
                  sessionType === 'work' ? 'active' : ''
                }`}
                disabled={isActive}
              >
                Work Session
              </button>
              <button
                onClick={() => switchSessionType('break')}
                className={`session-type-btn ${
                  sessionType === 'break' ? 'active' : ''
                }`}
                disabled={isActive}
              >
                Break Session
              </button>
            </div>
          </div>

          {/* Timer Circle */}
          <div className="relative mb-8 mx-auto">
            <div className="timer-circle">
              <div
                className="timer-progress"
                style={{
                  '--progress': `${progressPercentage * 3.6}deg`
                }}
              ></div>
              <div className="absolute inset-4 bg-white dark:bg-gray-900 rounded-full flex flex-col items-center justify-center">
                <div className="text-5xl font-bold text-gray-900 dark:text-white mb-2">
                  {formatTime(timeLeft)}
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                  {sessionType === 'work' ? 'Focus Time' : 'Break Time'}
                </div>
              </div>
            </div>
          </div>

          {/* Timer Controls */}
          <div className="timer-controls">
            <button
              onClick={isActive ? pauseTimer : startTimer}
              className="timer-control-btn primary"
            >
              {isActive ? (
                <>
                  <Pause className="h-5 w-5" />
                  <span>Pause</span>
                </>
              ) : (
                <>
                  <Play className="h-5 w-5" />
                  <span>Start</span>
                </>
              )}
            </button>
            <button
              onClick={resetTimer}
              className="timer-control-btn secondary"
            >
              <RotateCcw className="h-5 w-5" />
              <span>Reset</span>
            </button>
          </div>

          {/* Session Counter */}
          <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Completed Sessions Today
            </div>
            <div className="text-2xl font-bold text-primary-500 mt-1">
              {completedSessions}
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
          <div className="stats-card">
            <div className="flex justify-center mb-3">
              <Award className="h-8 w-8 text-primary-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {stats.total_sessions}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Total Sessions
            </div>
          </div>

          <div className="stats-card">
            <div className="flex justify-center mb-3">
              <Clock className="h-8 w-8 text-primary-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {Math.floor(stats.total_study_time / 60)}h {stats.total_study_time % 60}m
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Total Study Time
            </div>
          </div>

          <div className="stats-card">
            <div className="flex justify-center mb-3">
              <TrendingUp className="h-8 w-8 text-primary-500" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {stats.weekly_sessions}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              This Week
            </div>
          </div>
        </div>

        {/* How it Works */}
        <div className="card max-w-2xl w-full">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 text-center">
            How the Pomodoro Technique Works
          </h3>
          <div className="space-y-4 text-gray-600 dark:text-gray-400">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                1
              </div>
              <div>
                <strong className="text-gray-900 dark:text-white">Work for 25 minutes</strong> - Focus on a single task without distractions
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                2
              </div>
              <div>
                <strong className="text-gray-900 dark:text-white">Take a 5-minute break</strong> - Step away from your work and relax
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                3
              </div>
              <div>
                <strong className="text-gray-900 dark:text-white">Repeat the cycle</strong> - After 4 work sessions, take a longer 15-minute break
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                4
              </div>
              <div>
                <strong className="text-gray-900 dark:text-white">Track your progress</strong> - Monitor your productivity and build better habits
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;