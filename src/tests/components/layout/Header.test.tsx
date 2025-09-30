import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Header from '@/components/layout/Header';

// Mock the useNavigation hook
vi.mock('@/hooks/useNavigation', () => ({
  useNavigation: () => ({
    activeTab: 'Chat',
    items: [
      { name: 'Chat', href: '/chat' },
      { name: 'Spellbook', href: '/spellbook' },
    ],
  }),
}));

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('Header Component', () => {
  it('renders the header with title', () => {
    renderWithRouter(<Header />);

    expect(screen.getByText('Kairos AI')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    renderWithRouter(<Header />);

    expect(screen.getByText('Chat')).toBeInTheDocument();
    expect(screen.getByText('Spellbook')).toBeInTheDocument();
  });
});
