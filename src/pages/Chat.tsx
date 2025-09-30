import ChatInterface from '@/components/chat/ChatInterface';
import React from 'react';

const Chat: React.FC = () => {
  return (
    <div className='min-h-screen bg-deep-space constellation-bg'>
      <div className='container mx-auto px-4 py-8 max-w-6xl'>
        <div className='text-center mb-8 animate-twinkle'>
          <h1 className='text-4xl font-bold text-starlight mb-2 animate-float text-glow drop-shadow-[0_0_20px_rgba(99,102,241,0.5)]'>
            Chat with Kairos
          </h1>
          <p className='text-moonbeam text-lg'>
            Your AI companion for creative and introspective conversations
          </p>
        </div>
        <ChatInterface />
      </div>
    </div>
  );
};

export default Chat;
