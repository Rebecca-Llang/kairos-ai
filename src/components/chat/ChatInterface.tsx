import React from 'react';
import { useForm } from 'react-hook-form';
import { ChatMessage } from '@/types';
import { useChat } from '@/hooks';
import { formatTimestamp } from '@/utils/helpers';

const ChatInterface: React.FC = () => {
  const { register, handleSubmit, reset } = useForm();
  const {
    messages,
    isLoading,
    isSending,
    isThinking,
    error,
    includeMemories,
    setIncludeMemories,
    sendMessage,
    loadChatHistory,
    clearError,
    canSend,
  } = useChat();

  return (
    <div className='grid grid-cols-1 lg:grid-cols-3 gap-6 h-full'>
      {/* Chat Messages */}
      <div className='lg:col-span-2'>
        <div className='bg-dark-matter rounded-xl border border-gray-700 shadow-lg h-[600px] flex flex-col overflow-hidden'>
          {/* Header */}
          <div className='p-4 border-b border-gray-700 bg-stardust rounded-t-xl'>
            <div className='flex items-center justify-between'>
              <div className='flex items-center space-x-3'>
                <h2 className='text-xl font-semibold text-starlight'>
                  Conversation
                </h2>
              </div>
              <div className='flex items-center space-x-2'>
                <button
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    includeMemories
                      ? 'bg-nebula text-white shadow-glow'
                      : 'bg-dark-matter text-moonbeam hover:bg-stardust hover:text-starlight'
                  }`}
                  onClick={() => setIncludeMemories(!includeMemories)}
                >
                  {includeMemories ? 'Memories On' : 'Memories Off'}
                </button>
                <button
                  className='px-3 py-1 bg-aurora-teal text-white rounded-full text-xs font-medium hover:bg-teal-600 transition-colors disabled:opacity-50 shadow-glow-teal'
                  onClick={loadChatHistory}
                  disabled={isLoading}
                >
                  {isLoading ? 'Loading...' : 'Refresh'}
                </button>
              </div>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className='mx-4 mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg'>
              <div className='flex items-center justify-between'>
                <p className='text-destructive text-sm font-medium'>
                  Error: {error}
                </p>
                <button
                  className='text-destructive hover:text-destructive/80 text-sm font-medium'
                  onClick={clearError}
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}

          {/* Messages */}
          <div className='flex-1 overflow-y-auto p-4 space-y-4'>
            {messages.length === 0 ? (
              <div className='flex items-center justify-center h-full'>
                <div className='text-center animate-twinkle'>
                  <div className='w-16 h-16 mx-auto mb-4 bg-dark-matter rounded-full flex items-center justify-center animate-float'>
                    <span className='text-2xl'>✨</span>
                  </div>
                  <h3 className='text-lg font-medium text-starlight mb-2'>
                    Start a conversation
                  </h3>
                  <p className='text-sm text-moonbeam'>
                    Send a message below to begin chatting with Kairos
                  </p>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message: ChatMessage) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slideUp`}
                  >
                    <div
                      className={`max-w-[80%] p-3 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-nebula text-white shadow-glow'
                          : 'bg-stardust text-starlight border border-gray-600 shadow-lg'
                      }`}
                    >
                      <div className='flex items-center space-x-2 mb-1'>
                        <span className='text-xs font-medium opacity-70'>
                          {message.role === 'user' ? 'You' : 'Kairos'}
                        </span>
                        <span className='text-xs opacity-50'>
                          {formatTimestamp(message.timestamp)}
                        </span>
                      </div>
                      <p className='text-sm leading-relaxed whitespace-pre-wrap'>
                        {message.content}
                      </p>
                    </div>
                  </div>
                ))}

                {/* Thinking Indicator */}
                {isThinking && (
                  <div className='flex justify-start animate-slideUp'>
                    <div className='max-w-[80%] p-3 rounded-lg bg-stardust text-starlight border border-gray-600 shadow-lg'>
                      <div className='flex items-center space-x-2 mb-1'>
                        <span className='text-xs font-medium opacity-70'>
                          Kairos
                        </span>
                        <span className='text-xs opacity-50'>
                          is thinking...
                        </span>
                      </div>
                      <div className='flex items-center space-x-1'>
                        <div className='flex space-x-1'>
                          <div
                            className='w-2 h-2 bg-nebula rounded-full animate-pulse'
                            style={{ animationDelay: '0ms' }}
                          ></div>
                          <div
                            className='w-2 h-2 bg-nebula rounded-full animate-pulse'
                            style={{ animationDelay: '150ms' }}
                          ></div>
                          <div
                            className='w-2 h-2 bg-nebula rounded-full animate-pulse'
                            style={{ animationDelay: '300ms' }}
                          ></div>
                        </div>
                        <span className='text-xs opacity-60 ml-2'>
                          Processing your message...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Chat Input */}
      <div className='lg:col-span-1'>
        <div className='bg-dark-matter border border-gray-700 rounded-xl p-6 shadow-lg'>
          <h3 className='text-lg font-semibold text-starlight mb-4'>
            Send Message
          </h3>
          <form
            onSubmit={handleSubmit(data => {
              if (canSend(data.message)) {
                sendMessage(data.message);
                reset();
              }
            })}
            className='space-y-4'
          >
            <div>
              <textarea
                {...register('message', { required: true })}
                placeholder='Type your message here...'
                disabled={isSending || isThinking}
                className='w-full p-3 border border-gray-700 rounded-lg bg-stardust text-white placeholder-moonbeam focus:outline-none focus:ring-2 focus:ring-nebula/20 focus:border-nebula resize-none disabled:opacity-50 disabled:cursor-not-allowed'
                rows={4}
              />
            </div>
            <button
              type='submit'
              disabled={isSending || isThinking}
              className='w-full bg-nebula text-white hover:bg-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed px-4 py-2 rounded-lg font-medium transition-colors shadow-glow hover:shadow-glow-lg'
            >
              {isSending ? (
                <span className='flex items-center justify-center'>
                  <svg
                    className='animate-spin -ml-1 mr-2 h-4 w-4'
                    fill='none'
                    viewBox='0 0 24 24'
                  >
                    <circle
                      className='opacity-25'
                      cx='12'
                      cy='12'
                      r='10'
                      stroke='currentColor'
                      strokeWidth='4'
                    ></circle>
                    <path
                      className='opacity-75'
                      fill='currentColor'
                      d='M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z'
                    ></path>
                  </svg>
                  Sending...
                </span>
              ) : (
                'Send Message'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
