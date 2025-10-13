import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi, describe, it, expect } from 'vitest';
import Spellbook from '../Spellbook';

// Mock the spellbook components
vi.mock('@/components/spellbook', () => ({
  AddMemoryForm: function MockAddMemoryForm() {
    return <div data-testid='add-memory-form'>Add Memory Form</div>;
  },
  MemoryList: function MockMemoryList() {
    return <div data-testid='memory-list'>Memory List</div>;
  },
}));

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('Spellbook Page', () => {
  it('renders the page with title and description', () => {
    renderWithRouter(<Spellbook />);

    expect(screen.getByText('✨ Spellbook')).toBeInTheDocument();
    expect(
      screen.getByText(
        'Add or edit memories to help Kairos understand you better.'
      )
    ).toBeInTheDocument();
  });

  it('renders the AddMemoryForm component', () => {
    renderWithRouter(<Spellbook />);

    expect(screen.getByTestId('add-memory-form')).toBeInTheDocument();
  });

  it('renders the MemoryList component', () => {
    renderWithRouter(<Spellbook />);

    expect(screen.getByTestId('memory-list')).toBeInTheDocument();
  });
});

