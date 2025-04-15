
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Appointments() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/appointments")
      .then(res => setAppointments(res.data));
  }, []);

  return (
    <div className="panel">
      <h3>Appointments</h3>
      <ul>
        {appointments.map((a, i) => (
          <li key={i}>{a.date} at {a.time} ({a.type})</li>
        ))}
      </ul>
    </div>
  );
}

export default Appointments;
