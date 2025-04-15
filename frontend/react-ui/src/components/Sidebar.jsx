
import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Therapist Office</h2>
      <ul>
        <li><Link to="/">Messages</Link></li>
        <li><Link to="/appointments">Appointments</Link></li>
        <li><Link to="/medication">Medication</Link></li>
        <li><Link to="/zoom">Zoom Meetings</Link></li>
      </ul>
    </div>
  );
}

export default Sidebar;
