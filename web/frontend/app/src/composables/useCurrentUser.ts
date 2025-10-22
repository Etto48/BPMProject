import { ref, readonly } from 'vue';
import type { UserResponse } from '@/types';

const currentUser = ref<UserResponse | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

export function useCurrentUser() {
  async function fetchUser(): Promise<boolean> {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await fetch('/api/me', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        currentUser.value = data;
        return true;
      } else {
        currentUser.value = null;
        return false;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
      currentUser.value = null;
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  function clearUser() {
    currentUser.value = null;
    error.value = null;
  }

  return {
    currentUser: readonly(currentUser),
    isLoading: readonly(isLoading),
    error: readonly(error),
    fetchUser,
    clearUser
  };
}
