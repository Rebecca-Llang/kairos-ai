import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi, describe, it, expect } from 'vitest';
import Header from '../Header';

// Mock the useNavigation hook
vi.mock('@/hooks/useNavigation', () => ({
  useNavigation: () => ({
    activeTab: 'Chat',
    items: [
      { name: 'Chat', href: '/' },
      { name: 'Persona', href: '/persona' },
      { name: 'Spellbook', href: '/spellbook' },
      { name: 'History', href: '/history' },
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

  it('renders all navigation links', () => {
    renderWithRouter(<Header />);

    expect(screen.getByText('Chat')).toBeInTheDocument();
    expect(screen.getByText('Persona')).toBeInTheDocument();
    expect(screen.getByText('Spellbook')).toBeInTheDocument();
    expect(screen.getByText('History')).toBeInTheDocument();
  });
});
