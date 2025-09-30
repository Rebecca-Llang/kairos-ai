import ChatInterface from '@/components/chat/ChatInterface';
import React from 'react';

const Chat: React.FC = () => {
  return (
    <div className='min-h-screen bg-deep-space constellation-bg'>
      <div className='container mx-auto px-4 sm:px-6 py-6 sm:py-8 max-w-6xl'>
        <div className='text-center mb-6 sm:mb-8 animate-twinkle'>
          <h1 className='text-2xl sm:text-3xl lg:text-4xl font-bold text-starlight mb-2 animate-float text-glow drop-shadow-[0_0_20px_rgba(99,102,241,0.5)]'>
            Chat with Kairos
          </h1>
          <p className='text-sm sm:text-base lg:text-lg text-moonbeam px-4'>
            Your AI companion for creative and introspective conversations
          </p>
        </div>
        <ChatInterface />
      </div>
    </div>
  );
};

export default Chat;
