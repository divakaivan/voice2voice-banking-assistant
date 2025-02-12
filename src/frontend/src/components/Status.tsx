import React from 'react';

interface StatusProps {
  message?: string;
}

const Status: React.FC<StatusProps> = ({ message }) => {
  return (
    <div className="status">
      {message}
    </div>
  );
};

export default Status;
