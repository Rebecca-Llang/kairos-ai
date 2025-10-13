import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import MemoryCard from '../MemoryCard';
import { Memory } from '@/types';

// Mock EditMemoryForm
vi.mock('../EditMemoryForm', () => ({
  default: function MockEditMemoryForm({ onCancel }: { onCancel: () => void }) {
    return (
      <div data-testid='edit-memory-form'>
        <button onClick={onCancel}>Cancel</button>
      </div>
    );
  },
}));

describe('MemoryCard Component', () => {
  const mockMemory: Memory = {
    id: 1,
    memory_key: 'preferred_name',
    memory_value: 'Call me Alex',
    priority: 5,
    created_at: '2024-01-01T12:00:00Z',
  };

  const mockOnDelete = vi.fn();
  const mockOnUpdate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders memory information correctly', () => {
    render(
      <MemoryCard
        memory={mockMemory}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    // Formatted key (preferred_name → Preferred Name)
    expect(screen.getByText('Preferred Name')).toBeInTheDocument();
    expect(screen.getByText('Call me Alex')).toBeInTheDocument();
    expect(screen.getByText('Priority: 5')).toBeInTheDocument();
  });

  it('renders date correctly', () => {
    render(
      <MemoryCard
        memory={mockMemory}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    // Date formatting depends on locale (1/2/2024 format)
    const dateText = screen.getByText(/1\/2\/2024/);
    expect(dateText).toBeInTheDocument();
  });

  it('shows edit and delete buttons on hover', () => {
    render(
      <MemoryCard
        memory={mockMemory}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    const editButton = screen.getByRole('button', { name: /edit/i });
    const deleteButton = screen.getByRole('button', { name: /delete/i });

    expect(editButton).toBeInTheDocument();
    expect(deleteButton).toBeInTheDocument();
  });

  it('switches to edit mode when edit button is clicked', () => {
    render(
      <MemoryCard
        memory={mockMemory}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    const editButton = screen.getByRole('button', { name: /edit/i });
    fireEvent.click(editButton);

    // Should show edit form
    expect(screen.getByTestId('edit-memory-form')).toBeInTheDocument();
    // Should not show memory content
    expect(screen.queryByText('Call me Alex')).not.toBeInTheDocument();
  });

  it('calls onDelete when delete button is clicked', () => {
    render(
      <MemoryCard
        memory={mockMemory}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith(mockMemory);
  });

  it('exits edit mode when cancel is clicked', () => {
    render(
      <MemoryCard
        memory={mockMemory}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    // Enter edit mode
    const editButton = screen.getByRole('button', { name: /edit/i });
    fireEvent.click(editButton);
    expect(screen.getByTestId('edit-memory-form')).toBeInTheDocument();

    // Cancel edit
    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelButton);

    // Should show memory content again
    expect(screen.queryByTestId('edit-memory-form')).not.toBeInTheDocument();
    expect(screen.getByText('Call me Alex')).toBeInTheDocument();
  });

  it('does not render delete button when onDelete is not provided', () => {
    render(<MemoryCard memory={mockMemory} />);

    expect(
      screen.queryByRole('button', { name: /delete/i })
    ).not.toBeInTheDocument();
  });

  it('does not render delete button when memory has no id', () => {
    const memoryWithoutId = { ...mockMemory, id: undefined };
    render(
      <MemoryCard
        memory={memoryWithoutId}
        onDelete={mockOnDelete}
        onUpdate={mockOnUpdate}
      />
    );

    expect(
      screen.queryByRole('button', { name: /delete/i })
    ).not.toBeInTheDocument();
  });
});
