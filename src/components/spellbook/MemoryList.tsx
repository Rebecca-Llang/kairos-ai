// Memory list component - List of all memories with search and filtering
// This file will contain the memory list display, search functionality, and bulk actions

import React from 'react';
import MemoryCard from './MemoryCard';
import { useMemories } from '@/hooks';
import { Memory } from '@/types';

const MemoryList: React.FC = () => {
  const { memories, isLoading, error, deleteMemory, updateMemory } =
    useMemories();

  const handleDelete = async (memory: Memory) => {
    if (memory.id) {
      try {
        await deleteMemory(memory.id);
      } catch (error) {
        // Error is already handled by the hook - no action needed
        void error; // Suppress unused variable warning
      }
    }
  };

  const handleUpdate = async (memory: Memory, updatedData: Partial<Memory>) => {
    if (memory.id) {
      try {
        await updateMemory(memory.id, updatedData);
      } catch (error) {
        // Error is already handled by the hook - no action needed
        void error; // Suppress unused variable warning
      }
    }
  };

  if (isLoading) {
    return (
      <div className='w-full max-w-7xl'>
        <div className='text-center text-moonbeam py-8'>
          <div className='inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-nebula mb-4'></div>
          <p>Loading memories...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className='text-red-400'>Error: {error}</div>;
  }

  if (!memories || memories.length === 0) {
    return (
      <div className='w-full max-w-7xl'>
        <div className='text-center text-moonbeam py-8'>
          <div className='text-4xl mb-4'>📝</div>
          <p className='text-lg mb-2'>No memories found</p>
          <p className='text-sm text-moonbeam/70'>
            Add your first memory using the form above!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className='w-full max-w-7xl'>
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6'>
        {memories.map((memory: Memory) => (
          <MemoryCard
            key={memory.id}
            memory={memory}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
          />
        ))}
      </div>
    </div>
  );
};

export default MemoryList;
