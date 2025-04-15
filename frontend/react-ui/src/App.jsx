
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Messages from './components/Messages';
import Appointments from './components/Appointments';
import Medication from './components/Medication';
import ZoomMeetings from './components/ZoomMeetings';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Messages />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/medication" element={<Medication />} />
          <Route path="/zoom" element={<ZoomMeetings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
