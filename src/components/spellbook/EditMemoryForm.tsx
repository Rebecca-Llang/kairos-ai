import React, { useState } from 'react';
import { Memory } from '@/types';
import { formatMemoryKey, normalizeMemoryKey } from '@/utils/helpers';

interface EditMemoryFormProps {
  memory: Memory;
  onSave: (updatedMemory: Partial<Memory>) => void;
  onCancel: () => void;
}

const EditMemoryForm: React.FC<EditMemoryFormProps> = ({
  memory,
  onSave,
  onCancel,
}) => {
  const [formData, setFormData] = useState({
    memory_key: memory.memory_key,
    memory_value: memory.memory_value,
    priority: memory.priority,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.memory_key.trim()) {
      newErrors.memory_key = 'Memory key is required';
    } else {
      const normalizedKey = normalizeMemoryKey(formData.memory_key);
      if (!normalizedKey) {
        newErrors.memory_key = 'Memory key must contain valid characters';
      }
    }

    if (!formData.memory_value.trim()) {
      newErrors.memory_value = 'Memory content is required';
    }

    if (formData.priority < 1 || formData.priority > 10) {
      newErrors.priority = 'Priority must be between 1 and 10';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      // Normalize the memory key before saving
      const normalizedData = {
        ...formData,
        memory_key: normalizeMemoryKey(formData.memory_key),
      };
      onSave(normalizedData);
    }
  };

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <div className='bg-dark-matter/90 border border-nebula/50 rounded-xl p-4 md:p-6 shadow-glow'>
      <h3 className='text-base md:text-lg font-semibold text-starlight mb-3 md:mb-4'>
        Edit {formatMemoryKey(memory.memory_key)}
      </h3>

      <form onSubmit={handleSubmit} className='space-y-3 md:space-y-4'>
        {/* Memory Key */}
        <div>
          <label className='block text-sm font-medium text-moonbeam mb-2'>
            Memory Key
          </label>
          <input
            type='text'
            value={formData.memory_key}
            onChange={e => handleInputChange('memory_key', e.target.value)}
            className={`w-full px-3 py-2 bg-stardust/30 border rounded-lg text-starlight placeholder-moonbeam/50 focus:outline-none focus:border-nebula transition-colors ${
              errors.memory_key ? 'border-red-500' : 'border-stardust/50'
            }`}
            placeholder='e.g., Preferred Name, Current Goals, Personal Strengths'
          />
          {errors.memory_key && (
            <p className='text-red-400 text-xs mt-1'>{errors.memory_key}</p>
          )}
          <p className='text-moonbeam/60 text-xs mt-1'>
            ℹ️ Type naturally with spaces - we&apos;ll format it automatically
            for storage
          </p>
        </div>

        {/* Memory Value */}
        <div>
          <label className='block text-sm font-medium text-moonbeam mb-2'>
            Content
          </label>
          <textarea
            value={formData.memory_value}
            onChange={e => handleInputChange('memory_value', e.target.value)}
            rows={4}
            className={`w-full px-3 py-2 bg-stardust/30 border rounded-lg text-starlight placeholder-moonbeam/50 focus:outline-none focus:border-nebula transition-colors resize-none ${
              errors.memory_value ? 'border-red-500' : 'border-stardust/50'
            }`}
            placeholder='Enter memory content...'
          />
          {errors.memory_value && (
            <p className='text-red-400 text-xs mt-1'>{errors.memory_value}</p>
          )}
        </div>

        {/* Priority */}
        <div>
          <label className='block text-sm font-medium text-moonbeam mb-2'>
            Priority (1-10)
          </label>
          <input
            type='number'
            min='1'
            max='10'
            value={formData.priority}
            onChange={e =>
              handleInputChange('priority', parseInt(e.target.value) || 1)
            }
            className={`w-full px-3 py-2 bg-stardust/30 border rounded-lg text-starlight placeholder-moonbeam/50 focus:outline-none focus:border-nebula transition-colors ${
              errors.priority ? 'border-red-500' : 'border-stardust/50'
            }`}
          />
          {errors.priority && (
            <p className='text-red-400 text-xs mt-1'>{errors.priority}</p>
          )}
        </div>

        {/* Action Buttons */}
        <div className='flex flex-col sm:flex-row gap-3 pt-3 md:pt-4'>
          <button
            type='submit'
            className='flex-1 px-4 py-2 bg-nebula/20 text-nebula border border-nebula/50 rounded-lg hover:bg-nebula/30 hover:text-starlight transition-all duration-200 hover:shadow-glow'
          >
            Save Changes
          </button>
          <button
            type='button'
            onClick={onCancel}
            className='flex-1 px-4 py-2 bg-moonbeam/10 text-moonbeam border border-moonbeam/30 rounded-lg hover:bg-moonbeam/20 hover:text-starlight transition-all duration-200'
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditMemoryForm;
