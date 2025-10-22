<script setup lang="ts">
import { computed } from 'vue';
import { ChevronDown } from 'lucide-vue-next';
import { useCurrentUser } from '@/composables/useCurrentUser';

const { currentUser, isLoading } = useCurrentUser();
const accountName = computed(() => currentUser.value?.username || '');

</script>

<template>
    <div v-if="!isLoading && currentUser">
        <img alt="Account Icon" src="@/assets/account-icon.svg" width="32" height="32" />
        <span>{{ accountName }}</span>
        <ChevronDown />
    </div>
</template>

<style scoped>
div {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    border: 2px solid var(--color-border);
    border-radius: 10px;
    padding: 0.5rem 1rem;
}

/* Mobile (max-width: 768px) */
@media (max-width: 768px) {
    div {
        padding: 0.5rem;
    }

    div span {
        display: none;
    }

    div svg {
        display: none;
    }
}
</style>