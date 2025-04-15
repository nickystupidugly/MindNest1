
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Medication() {
  const [profile, setProfile] = useState({});

  useEffect(() => {
    axios.get("http://localhost:5000/guardian")
      .then(res => setProfile(res.data));
  }, []);

  return (
    <div className="panel">
      <h3>Vitals</h3>
      <p>{profile.vitals}</p>
      <h3>Medications</h3>
      <ul>
        {profile.medication?.map((m, i) => (
          <li key={i}>{m.name} - {m.dose}</li>
        ))}
      </ul>
      <h3>Hospital</h3>
      <p>{profile.hospital}</p>
      <button>Request Visit</button>
    </div>
  );
}

export default Medication;
