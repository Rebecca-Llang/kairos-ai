import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import ChatInterface from '../ChatInterface';
import { useChat } from '@/hooks';

// Mock the useChat hook
vi.mock('@/hooks', () => ({
  useChat: vi.fn(),
}));

// Mock react-hook-form
vi.mock('react-hook-form', () => ({
  useForm: () => ({
    register: vi.fn(),
    handleSubmit: vi.fn(),
    reset: vi.fn(),
  }),
}));

const mockUseChat = useChat as ReturnType<typeof vi.fn>;

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('ChatInterface', () => {
  beforeEach(() => {
    mockUseChat.mockReturnValue({
      messages: [],
      isLoading: false,
      isSending: false,
      isThinking: false,
      error: null,
      includeMemories: false,
      setIncludeMemories: vi.fn(),
      sendMessage: vi.fn(),
      loadChatHistory: vi.fn(),
      clearError: vi.fn(),
      canSend: vi.fn(() => true),
    });
  });

  it('renders the chat interface', () => {
    renderWithRouter(<ChatInterface />);

    expect(screen.getByText('Conversation')).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /send message/i })
    ).toBeInTheDocument();
  });

  it('shows empty state when no messages', () => {
    renderWithRouter(<ChatInterface />);

    expect(screen.getByText('Start a conversation')).toBeInTheDocument();
  });

  it('displays messages when they exist', () => {
    const messages = [
      {
        id: '1',
        role: 'user' as const,
        content: 'Hello Kairos!',
        timestamp: '2024-01-01T12:00:00Z',
      },
    ];

    mockUseChat.mockReturnValue({
      messages,
      isLoading: false,
      isSending: false,
      isThinking: false,
      error: null,
      includeMemories: false,
      setIncludeMemories: vi.fn(),
      sendMessage: vi.fn(),
      loadChatHistory: vi.fn(),
      clearError: vi.fn(),
      canSend: vi.fn(() => true),
    });

    renderWithRouter(<ChatInterface />);

    expect(screen.getByText('Hello Kairos!')).toBeInTheDocument();
  });
});
