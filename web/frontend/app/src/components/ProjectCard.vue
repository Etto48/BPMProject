<script setup lang="ts">
import { ref } from 'vue';
import { Trash2 } from 'lucide-vue-next';
import ConfirmModal from './ConfirmModal.vue';

const props = defineProps<{ projectId: number; title: string; description: string }>();
const emit = defineEmits<{ (e: 'deleted', id: number): void, (e: 'click'): void }>();

const showConfirm = ref(false);
const isDeleting = ref(false);
const error = ref('');

function openConfirm() {
    error.value = '';
    showConfirm.value = true;
}

async function confirmDelete() {
    isDeleting.value = true;
    error.value = '';
    try {
        const res = await fetch(`/api/projects/${props.projectId}`, { method: 'DELETE' });
        if (!res.ok) {
            const text = await res.text();
            throw new Error(text || `Delete failed (${res.status})`);
        }
        emit('deleted', props.projectId);
        showConfirm.value = false;
    } catch (e: unknown) {
        // safely extract message from unknown
        let msg = String(e);
        if (e && typeof e === 'object' && 'message' in e) {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            msg = (e as any).message ?? msg;
        }
        error.value = msg;
    } finally {
        isDeleting.value = false;
    }
}
</script>

<template>
    <div class="project-card card gradient-border hoverable" @click="$emit('click')">
        <div class="title-container">
            <h3 class="capsule gradient-background">{{ title }}</h3>
            <button class="delete-btn" @click.stop="openConfirm" aria-label="Delete project">
                <Trash2 :size="16" />
            </button>
        </div>
        <div class="gradient-background-light description-wrapper">
            <p>{{ description }}</p>
        </div>
    </div>

    <ConfirmModal
        v-model:visible="showConfirm"
        title="Delete project?"
        :confirmDisabled="isDeleting"
        confirmText="Delete"
        cancelText="Cancel"
        :error="error"
        @confirm="confirmDelete"
    >
        <p>Are you sure you want to permanently delete "{{ title }}"? This action cannot be undone.</p>
    </ConfirmModal>
</template>

<style scoped>
.title-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.project-card {
    position: relative;
    transition: background-color 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    height: 250px;
}

.project-card h3 {
    display: -webkit-box;
    flex: 1;
    padding: 2px 1rem;
    font-weight: 600;
    transition: filter 0.3s ease, background-color 0.2s ease;
    overflow: hidden;
    -webkit-line-clamp: 1;
    line-clamp: 1;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
}

.description-wrapper {
    flex: 1;
    border-radius: 8px;
    padding: 1rem;
    transition: filter 0.3s ease, background-color 0.2s ease;
    min-height: 0;
}

.description-wrapper p {
    margin: 0;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 5;
    line-clamp: 5;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    max-height: 100%;
}

/* Delete button styled to match site colors and utility classes */
.delete-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    margin-left: 8px;
    padding: 0;
    border-radius: 50%;
    border: 1px solid var(--color-threat);
    background-color: var(--color-threat-light);
    color: var(--color-threat);
    cursor: pointer;
    transition: transform 0.08s ease, filter 0.12s ease, background-color 0.12s ease;
}

@media (hover: hover) {
    .delete-btn:hover {
        filter: brightness(0.9);
    }   
}

@media (prefers-color-scheme: dark) {
    @media (hover: hover) {
        .delete-btn:hover {
            filter: brightness(1.5);
        }
    }
}

.delete-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Modal styling using existing card and color variables */
/* Modal styles moved to ConfirmModal.vue */
</style>