import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Timetable from './pages/Timetable';
import History from './pages/History';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import { TimerProvider } from './context/TimerContext';
import { api } from './utils/api';
import './App.css';

// Create a wrapper component to handle navigation
const AuthWrapper = ({ children, user }) => {
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!user) {
      navigate('/');
    }
  }, [user, navigate]);

  return children;
};

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const checkAuth = async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.data.user);
    } catch (error) {
      console.log('Not authenticated');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: '#ffffff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          animation: 'spin 1s linear infinite',
          borderRadius: '50%',
          height: '8rem',
          width: '8rem',
          borderBottom: '2px solid #ef4444'
        }}></div>
      </div>
    );
  }

  // Simple fallback if there are any errors
  try {
    return (
      <Router>
        <div style={{
          minHeight: '100vh',
          background: darkMode ? '#111827' : '#f9fafb',
          transition: 'all 0.3s'
        }}>
          <div style={{
            maxWidth: '80rem',
            margin: '0 auto',
            padding: '0 1rem'
          }}>
            <Routes>
              <Route 
                path="/register" 
                element={!user ? (
                  <Register onRegister={handleLogin} />
                ) : (
                  <Navigate to="/" replace />
                )} 
              />
              
              <Route 
                path="/*" 
                element={!user ? (
                  <Login onLogin={handleLogin} />
                ) : (
                  <AuthWrapper user={user}>
                    <TimerProvider>
                      <Layout 
                        user={user} 
                        onLogout={handleLogout} 
                        darkMode={darkMode} 
                        toggleDarkMode={toggleDarkMode}
                      >
                        <Routes>
                          <Route path="/" element={<Home user={user} />} />
                          <Route path="/timetable" element={<Timetable user={user} />} />
                          <Route path="/history" element={<History user={user} />} />
                          <Route path="*" element={<Navigate to="/" replace />} />
                        </Routes>
                      </Layout>
                    </TimerProvider>
                  </AuthWrapper>
                )}
              />
            </Routes>
          </div>
        </div>
      </Router>
    );
  } catch (error) {
    console.error('App error:', error);
    return (
      <div style={{
        minHeight: '100vh',
        background: '#fef2f2',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          textAlign: 'center'
        }}>
          <h1 style={{
            fontSize: '1.5rem',
            fontWeight: '700',
            color: '#991b1b',
            marginBottom: '1rem'
          }}>PomodoroFlow</h1>
          <p style={{
            color: '#dc2626'
          }}>Loading application...</p>
          <p style={{
            fontSize: '0.875rem',
            color: '#ef4444',
            marginTop: '0.5rem'
          }}>If this persists, please refresh the page.</p>
        </div>
      </div>
    );
  }
}

export default App;