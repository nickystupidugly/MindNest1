
import React from 'react';

const WindowChrome = ({ title, children }) => (
  <div className="panel">
    <div className="window-header">
      <div className="btn red"></div>
      <div className="btn yellow"></div>
      <div className="btn green"></div>
      <span style={{ marginLeft: '1rem' }}><strong>{title}</strong></span>
    </div>
    {children}
  </div>
);

export default WindowChrome;
