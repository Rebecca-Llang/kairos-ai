import React from 'react';

const History: React.FC = () => {
  return (
    <div className='min-h-screen bg-deep-space constellation-bg flex items-center justify-center px-4'>
      <div className='text-center animate-twinkle max-w-md'>
        <h1 className='text-2xl sm:text-3xl font-bold text-starlight mb-4 text-glow'>
          📜 History
        </h1>
        <p className='text-sm sm:text-base text-moonbeam'>
          Conversation history coming soon...
        </p>
      </div>
    </div>
  );
};

export default History;
