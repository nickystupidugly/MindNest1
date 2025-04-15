
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ZoomMeetings() {
  const [event, setEvent] = useState({});

  useEffect(() => {
    axios.get("http://localhost:5000/events")
      .then(res => setEvent(res.data));
  }, []);

  return (
    <div className="panel">
      <h3>{event.topic}</h3>
      <p>Time: {event.time}</p>
      <p>Hospital: {event.hospital}</p>
      <a href={event.link} target="_blank" rel="noopener noreferrer">Join Zoom</a>
    </div>
  );
}

export default ZoomMeetings;
