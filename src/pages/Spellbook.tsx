import React from 'react';
import { AddMemoryForm, MemoryList } from '@/components/spellbook';

const Spellbook: React.FC = () => {
  return (
    <div className='min-h-screen bg-deep-space constellation-bg flex items-center justify-center px-4 py-8'>
      <div className='w-full max-w-7xl'>
        <div className='text-center mb-6 md:mb-8'>
          <h1 className='text-2xl sm:text-3xl md:text-4xl font-bold text-starlight mb-2 md:mb-4 text-glow animate-twinkle'>
            ✨ Spellbook
          </h1>
          <p className='text-sm md:text-base text-moonbeam/80 max-w-2xl mx-auto'>
            Add or edit memories to help Kairos understand you better.
          </p>
          <AddMemoryForm />
        </div>

        <div className='flex justify-center'>
          <MemoryList />
        </div>
      </div>
    </div>
  );
};

export default Spellbook;
