import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Chat from '@/pages/Chat';

// Mock the ChatInterface component
vi.mock('@/components/chat/ChatInterface', () => ({
  default: function MockChatInterface() {
    return <div data-testid='chat-interface'>Chat Interface</div>;
  },
}));

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('Chat Page', () => {
  it('renders the chat page with title', () => {
    renderWithRouter(<Chat />);

    expect(screen.getByText('Chat with Kairos')).toBeInTheDocument();
  });

  it('renders the ChatInterface component', () => {
    renderWithRouter(<Chat />);

    expect(screen.getByTestId('chat-interface')).toBeInTheDocument();
  });
});
