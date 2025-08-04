# PomodoroFlow - Time Management Software

#### Video Demo: <URL HERE>
#### Description:

PomodoroFlow is a comprehensive time management application built around the Pomodoro Technique, designed to help users boost their productivity through structured work and break sessions. The application features a modern, responsive interface with both light and dark mode support, built using React for the frontend and Flask for the backend.

## Features

### Core Functionality
- **Pomodoro Timer**: 25-minute work sessions with 5-minute breaks
- **Session Management**: Track and manage work/break sessions
- **Auto-switching**: Automatically switches between work and break sessions
- **Long Breaks**: 15-minute breaks after every 4 work sessions
- **Session History**: Complete history of all timer sessions
- **Statistics**: Track total sessions, study time, and weekly progress

### User Interface
- **Modern Design**: Clean, intuitive interface with red/gray/white color scheme
- **Dark Mode**: Full dark mode support with automatic theme switching
- **Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Updates**: Live timer with visual progress indicators
- **Notifications**: Browser notifications when sessions complete

### Timetable Planning
- **Study Planning**: Create detailed study timetables with custom schedules
- **Break Integration**: Include breaks in your study plans
- **Date Management**: Organize timetables by date
- **Visual Schedule**: Clear timeline view of your planned sessions

### User Management
- **Secure Authentication**: User registration and login system
- **Session Persistence**: Maintains user sessions across browser restarts
- **Personal Data**: Each user's data is isolated and secure

## Technical Stack

### Frontend
- **React 19**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework for styling
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Lucide React**: Beautiful, customizable icons

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database for data persistence
- **Flask-CORS**: Cross-origin resource sharing support
- **Werkzeug**: Security utilities for password hashing

### Database Schema
- **Users**: User accounts with username, email, and password
- **Timer Sessions**: Track individual work/break sessions
- **Timetables**: Study schedule planning
- **Timetable Entries**: Individual time slots within timetables

## Project Structure

```
pomodoro-app/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── auth/        # Authentication components
│   │   │   └── Layout.jsx   # Main layout component
│   │   ├── pages/           # Page components
│   │   │   ├── Home.jsx     # Main dashboard with timer
│   │   │   ├── Timetable.jsx # Study schedule planning
│   │   │   └── History.jsx  # Session history and stats
│   │   ├── hooks/           # Custom React hooks
│   │   │   └── useTimer.js  # Timer logic and state management
│   │   ├── utils/           # Utility functions
│   │   │   └── api.js       # API client configuration
│   │   └── styles/          # CSS and styling
│   └── package.json         # Frontend dependencies
├── backend/                  # Flask backend application
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── pomodoro.db        # SQLite database
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8 or higher
- npm or yarn package manager

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd pomodoro-app/backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python3 -c "from app import init_db; init_db(); print('Database initialized')"
   ```

5. Start the Flask server:
   ```bash
   python3 app.py
   ```
   The backend will run on http://localhost:5000

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd pomodoro-app/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on http://localhost:5173

## Usage Guide

### Getting Started
1. Open the application in your browser
2. Create a new account or log in with existing credentials
3. You'll be taken to the home dashboard with the Pomodoro timer

### Using the Timer
1. **Select Session Type**: Choose between "Work Session" (25 minutes) or "Break Session" (5 minutes)
2. **Start Timer**: Click the "Start" button to begin your session
3. **Monitor Progress**: Watch the circular progress indicator
4. **Pause/Reset**: Use the pause button to stop temporarily or reset to start over
5. **Auto-switching**: The timer automatically switches between work and break sessions

### Creating Timetables
1. Navigate to the "Timetable" page
2. Click "Create New Timetable"
3. Fill in the title, description, and date
4. Add time entries with subjects and break periods
5. Save your timetable for future reference

### Viewing History
1. Go to the "History" page to see all your completed sessions
2. Filter by session type (work/break) or completion status
3. Sort by date or duration
4. View statistics including total study time and weekly progress

### Dark Mode
- Toggle between light and dark themes using the sun/moon icon in the navigation
- Your preference is automatically saved and restored

## Design Decisions

### Color Scheme
The application uses a red/gray/white color palette that aligns with the Pomodoro Technique's focus on productivity and energy. Red represents urgency and focus, while gray provides a neutral, professional backdrop.

### User Experience
- **Intuitive Navigation**: Clear, accessible navigation with icons and labels
- **Visual Feedback**: Progress indicators and animations provide immediate feedback
- **Responsive Design**: Works seamlessly across all device sizes
- **Accessibility**: High contrast ratios and keyboard navigation support

### Technical Architecture
- **Separation of Concerns**: Frontend and backend are completely separated
- **RESTful API**: Clean, predictable API endpoints
- **State Management**: React hooks for local state management
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Future Enhancements

- **Mobile App**: Native iOS and Android applications
- **Team Features**: Collaborative study sessions and group timetables
- **Advanced Analytics**: Detailed productivity insights and trends
- **Integration**: Calendar integration and third-party app connections
- **Customization**: User-defined session lengths and break patterns
- **Offline Support**: Work without internet connection
- **Export Features**: Export data to CSV or PDF formats

## Contributing

This project was built as a CS50 Final Project, demonstrating proficiency in:
- Full-stack web development
- Database design and management
- User interface design
- API development and integration
- Modern JavaScript and Python programming

The codebase follows best practices for maintainability, scalability, and user experience, making it a solid foundation for future development and learning.