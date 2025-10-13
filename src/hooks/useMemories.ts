import { useState, useEffect, useCallback } from 'react';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types';

// Memory management hook
export const useMemories = () => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMemories = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await memoryService.getMemories();
      // Backend returns {memories: [...]}, not {data: [...]}
      setMemories(response.memories || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch memories');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateMemory = useCallback(
    async (id: number, updatedData: Partial<Memory>) => {
      try {
        await memoryService.updateMemory(id, updatedData);
        // Refresh the memories list after update
        await fetchMemories();
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Failed to update memory'
        );
        throw err;
      }
    },
    [fetchMemories]
  );

  const deleteMemory = useCallback(async (id: number) => {
    try {
      await memoryService.deleteMemory(id);
      setMemories(prev => prev.filter(memory => memory.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete memory');
      throw err;
    }
  }, []);

  const addMemory = useCallback(
    async (memory: Omit<Memory, 'id'>) => {
      try {
        await memoryService.addMemory(memory);
        // Backend returns {message: "..."}, not {data: {...}}
        // We'll need to refetch memories after adding
        await fetchMemories();
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to add memory');
        throw err;
      }
    },
    [fetchMemories]
  );

  useEffect(() => {
    fetchMemories();
  }, [fetchMemories]);

  return {
    memories,
    isLoading,
    error,
    fetchMemories,
    updateMemory,
    deleteMemory,
    addMemory,
  };
};

