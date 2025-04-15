
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Panel() {
  const [appointments, setAppointments] = useState([]);
  const [guardian, setGuardian] = useState({});
  const [events, setEvents] = useState({});

  useEffect(() => {
    axios.get("http://localhost:5000/appointments").then(res => setAppointments(res.data));
    axios.get("http://localhost:5000/guardian").then(res => setGuardian(res.data));
    axios.get("http://localhost:5000/events").then(res => setEvents(res.data));
  }, []);

  return (
    <div className="panel">
      <h3>Upcoming Appointments</h3>
      <ul>
        {appointments.map((a, index) => (
          <li key={index}>{a.date} at {a.time} ({a.type})</li>
        ))}
      </ul>

      <h3>Guardian Profile</h3>
      <p>Vitals: {guardian.vitals}</p>
      <ul>
        {guardian.medication?.map((m, i) => (
          <li key={i}>{m.name} - {m.dose}</li>
        ))}
      </ul>
      <p>Hospital: {guardian.hospital}</p>

      <h3>Group Event</h3>
      <p>{events.topic} at {events.time}</p>
      <p>Hosted by: {events.hospital}</p>
      <a href={events.link} target="_blank" rel="noopener noreferrer">Join Zoom</a>
    </div>
  );
}

export default Panel;
