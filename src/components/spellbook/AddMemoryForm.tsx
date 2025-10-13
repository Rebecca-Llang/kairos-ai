import React, { useState } from 'react';
import { useMemories } from '@/hooks';
import { normalizeMemoryKey } from '@/utils/helpers';

const AddMemoryForm: React.FC = () => {
  const { addMemory } = useMemories();
  const [formData, setFormData] = useState({
    memory_key: '',
    memory_value: '',
    priority: 5,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      // Normalize the memory key before sending
      const normalizedData = {
        ...formData,
        memory_key: normalizeMemoryKey(formData.memory_key),
      };

      await addMemory(normalizedData);
      // Reset form on success
      setFormData({
        memory_key: '',
        memory_value: '',
        priority: 5,
      });
      setErrors({});
      setShowSuccess(true);
      // Hide success message after 3 seconds
      window.setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      // Error is handled by the hook
    } finally {
      setIsSubmitting(false);
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
    <div className='bg-dark-matter/80 border border-stardust/50 rounded-xl p-4 md:p-6 mb-6 md:mb-8'>
      <h3 className='text-base md:text-lg font-semibold text-starlight mb-3 md:mb-4'>
        Add New Memory
      </h3>

      {/* Success Message */}
      {showSuccess && (
        <div className='mb-4 p-4 bg-green-900/30 border border-green-500/70 rounded-lg text-green-200 text-sm shadow-lg animate-pulse'>
          <div className='flex items-center gap-2'>
            <span className='text-lg'>✅</span>
            <div>
              <p className='font-medium'>Memory added successfully!</p>
              <p className='text-green-300/80 text-xs mt-1'>
                Check the list below to see your new memory.
              </p>
            </div>
          </div>
        </div>
      )}

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
            disabled={isSubmitting}
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
            rows={3}
            className={`w-full px-3 py-2 bg-stardust/30 border rounded-lg text-starlight placeholder-moonbeam/50 focus:outline-none focus:border-nebula transition-colors resize-none ${
              errors.memory_value ? 'border-red-500' : 'border-stardust/50'
            }`}
            placeholder='Enter memory content...'
            disabled={isSubmitting}
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
            disabled={isSubmitting}
          />
          {errors.priority && (
            <p className='text-red-400 text-xs mt-1'>{errors.priority}</p>
          )}
        </div>

        {/* Submit Button */}
        <div className='pt-3 md:pt-4'>
          <button
            type='submit'
            disabled={isSubmitting}
            className='w-full px-4 py-2 bg-nebula/20 text-nebula border border-nebula/50 rounded-lg hover:bg-nebula/30 hover:text-starlight transition-all duration-200 hover:shadow-glow disabled:opacity-50 disabled:cursor-not-allowed'
          >
            {isSubmitting ? 'Adding Memory...' : 'Add Memory'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddMemoryForm;
