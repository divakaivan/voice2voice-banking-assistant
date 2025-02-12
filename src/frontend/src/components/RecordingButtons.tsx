import React from 'react';

interface RecordingButtonProps {
  onToggle: () => void;
  isRecording: boolean;
  disabled: boolean;
  className?: string;
}

const RecordingButton: React.FC<RecordingButtonProps> = ({
  onToggle,
  isRecording,
  disabled,
  className = ''
}) => {
  return (
    <button 
      onClick={onToggle} 
      disabled={disabled}
      className={`w-full px-4 py-3 rounded-lg font-medium transition-all
        ${isRecording 
          ? 'bg-red-500 hover:bg-red-600 text-white' 
          : 'bg-blue-500 hover:bg-blue-600 text-white'
        }
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        ${className}`}
      style={{
        backgroundColor: isRecording ? '#e64a19' : '#2196f3',
        color: 'white',
        padding: '12px 20px',
        borderRadius: '8px',
        transition: 'all 0.3s ease',
        cursor: disabled ? 'not-allowed' : 'pointer'
      }}
    >
      {isRecording ? 'Stop Voice Message' : 'Start Voice Message'}
    </button>
  );
};

export default RecordingButton;
