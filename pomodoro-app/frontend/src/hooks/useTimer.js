import { useState, useEffect, useRef } from 'react';
import { api } from '../utils/api';

export const useTimer = () => {
  const [timeLeft, setTimeLeft] = useState(25 * 60); // 25 minutes in seconds
  const [isActive, setIsActive] = useState(false);
  const [sessionType, setSessionType] = useState('work'); // 'work' or 'break'
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [completedSessions, setCompletedSessions] = useState(0);
  
  const intervalRef = useRef(null);
  const initialTime = useRef(25 * 60);

  useEffect(() => {
    if (isActive && timeLeft > 0) {
      intervalRef.current = setInterval(() => {
        setTimeLeft((time) => time - 1);
      }, 1000);
    } else if (timeLeft === 0 && isActive) {
      // Timer finished
      handleTimerComplete();
    } else {
      clearInterval(intervalRef.current);
    }

    return () => clearInterval(intervalRef.current);
  }, [isActive, timeLeft]);

  const startTimer = async () => {
    if (!isActive) {
      try {
        const response = await api.post('/timer/sessions', {
          session_type: sessionType,
          duration: Math.ceil(initialTime.current / 60),
        });
        setCurrentSessionId(response.data.session_id);
        setIsActive(true);
      } catch (error) {
        console.error('Failed to start timer session:', error);
      }
    }
  };

  const pauseTimer = () => {
    setIsActive(false);
  };

  const resetTimer = () => {
    setIsActive(false);
    setTimeLeft(initialTime.current);
    setCurrentSessionId(null);
  };

  const handleTimerComplete = async () => {
    setIsActive(false);
    
    if (currentSessionId) {
      try {
        await api.put(`/timer/sessions/${currentSessionId}/complete`);
        setCompletedSessions(prev => prev + 1);
      } catch (error) {
        console.error('Failed to complete timer session:', error);
      }
    }

    // Auto-switch between work and break sessions
    if (sessionType === 'work') {
      setSessionType('break');
      const breakTime = completedSessions > 0 && (completedSessions + 1) % 4 === 0 ? 15 * 60 : 5 * 60; // Long break every 4th session
      setTimeLeft(breakTime);
      initialTime.current = breakTime;
    } else {
      setSessionType('work');
      setTimeLeft(25 * 60);
      initialTime.current = 25 * 60;
    }

    setCurrentSessionId(null);
    
    // Show notification if available
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(`${sessionType === 'work' ? 'Work' : 'Break'} session completed!`, {
        body: sessionType === 'work' ? 'Time for a break!' : 'Time to get back to work!',
        icon: '/favicon.ico',
      });
    }
  };

  const switchSessionType = (type) => {
    if (!isActive) {
      setSessionType(type);
      if (type === 'work') {
        setTimeLeft(25 * 60);
        initialTime.current = 25 * 60;
      } else {
        const breakTime = completedSessions > 0 && completedSessions % 4 === 0 ? 15 * 60 : 5 * 60;
        setTimeLeft(breakTime);
        initialTime.current = breakTime;
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getProgressPercentage = () => {
    return ((initialTime.current - timeLeft) / initialTime.current) * 100;
  };

  // Request notification permission on first use
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  return {
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
  };
};