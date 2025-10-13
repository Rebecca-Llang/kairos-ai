// Spellbook components - Memory management UI components
// This file will contain memory cards, add/edit forms, and memory list components

import React, { useState } from 'react';
import { Memory } from '@/types';
import { formatMemoryKey } from '@/utils/helpers';
import EditMemoryForm from './EditMemoryForm';

interface MemoryCardProps {
  memory: Memory;
  onDelete?: (memory: Memory) => void;
  onUpdate?: (memory: Memory, updatedData: Partial<Memory>) => void;
}

const MemoryCard: React.FC<MemoryCardProps> = ({
  memory,
  onDelete,
  onUpdate,
}) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = (updatedData: Partial<Memory>) => {
    if (onUpdate) {
      onUpdate(memory, updatedData);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <EditMemoryForm
        memory={memory}
        onSave={handleSave}
        onCancel={handleCancel}
      />
    );
  }
  return (
    <div className='group relative bg-dark-matter/80 backdrop-blur-sm border border-stardust/50 rounded-xl p-4 md:p-6 transition-all duration-300 hover:border-nebula/50 hover:shadow-glow hover:bg-dark-matter/90 h-fit'>
      {/* Header with memory key */}
      <div className='flex justify-between items-start mb-3 md:mb-4'>
        <h3 className='text-base md:text-lg font-semibold text-starlight group-hover:text-glow transition-all duration-300 leading-tight'>
          {formatMemoryKey(memory.memory_key)}
        </h3>

        {/* Action buttons */}
        <div className='flex gap-1 md:gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300'>
          <button
            onClick={handleEdit}
            className='px-2 md:px-3 py-1 md:py-1.5 text-xs font-medium text-moonbeam bg-stardust/50 hover:bg-nebula/20 hover:text-starlight rounded-lg border border-stardust/30 hover:border-nebula/50 transition-all duration-200 hover:shadow-glow'
          >
            Edit
          </button>
          {onDelete && memory.id && (
            <button
              onClick={() => onDelete(memory)}
              className='px-2 md:px-3 py-1 md:py-1.5 text-xs font-medium text-red-300 bg-red-900/20 hover:bg-red-800/30 hover:text-red-200 rounded-lg border border-red-800/30 hover:border-red-600/50 transition-all duration-200 hover:shadow-[0_0_20px_rgba(239,68,68,0.3)]'
            >
              Delete
            </button>
          )}
        </div>
      </div>

      {/* Memory content */}
      <div className='mb-3 md:mb-4'>
        <p className='text-moonbeam leading-relaxed text-sm md:text-sm'>
          {memory.memory_value}
        </p>
      </div>

      {/* Footer with metadata */}
      <div className='flex justify-between items-center text-xs text-moonbeam/70 border-t border-stardust/30 pt-3'>
        <div className='flex items-center gap-2'>
          <span className='px-2 py-1 bg-nebula/10 text-nebula rounded-md border border-nebula/20 text-xs'>
            Priority: {memory.priority}
          </span>
        </div>

        {memory.created_at && (
          <span className='text-moonbeam/50 text-xs'>
            {new Date(memory.created_at).toLocaleDateString()}
          </span>
        )}
      </div>

      {/* Subtle glow effect */}
      <div className='absolute inset-0 rounded-xl bg-gradient-to-r from-nebula/5 via-transparent to-aurora-teal/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none' />
    </div>
  );
};

export default MemoryCard;
