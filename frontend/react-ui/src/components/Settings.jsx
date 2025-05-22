
import React from 'react';

function Settings({ onModeChange }) {
  return (
    <div className="panel">
      <h3>Settings</h3>
      <label>
        UI Mode:
        <select onChange={(e) => onModeChange(e.target.value)} defaultValue={localStorage.getItem('mindnest-ui') || 'retro'}>
          <option value="retro">Retro</option>
          <option value="modern">Modern</option>
        </select>
      </label>
    </div>
  );
}

export default Settings;
