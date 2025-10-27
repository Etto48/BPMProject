<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  visible: boolean;
  title?: string;
  confirmDisabled?: boolean;
  confirmText?: string;
  cancelText?: string;
  error?: string | null;
}>();

const emit = defineEmits<{
  (e: 'update:visible', v: boolean): void;
  (e: 'confirm'): void;
}>();

const confirmLabel = computed(() => props.confirmText ?? 'Delete');
const cancelLabel = computed(() => props.cancelText ?? 'Cancel');

function close() {
  emit('update:visible', false);
}

function onConfirm() {
  emit('confirm');
}
</script>

<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal" role="dialog" aria-modal="true" :aria-labelledby="`confirm-${Math.random()}`">
      <h4 v-if="title">{{ title }}</h4>
      <div class="modal-body">
        <slot />
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <div class="modal-actions">
        <button class="confirm-btn threat-button" :disabled="confirmDisabled" @click="onConfirm">{{ confirmLabel }}</button>
        <button class="cancel-btn secondary-button" :disabled="confirmDisabled" @click="close">{{ cancelLabel }}</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Modal base styles (uses project's CSS variables and utility classes) */
.modal-overlay {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.35);
    z-index: 2201;
    padding: 24px;
}

.modal {
    max-width: 520px;
    width: 100%;
    background: var(--color-background);
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    border: 1px solid var(--color-border);
}

.modal-body {
    margin-top: 6px;
}

.modal-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
    margin-top: 12px;
}

.confirm-btn {
    padding: 0.5rem 0.9rem;
    border-radius: 8px;
}

.cancel-btn {
    padding: 0.5rem 0.9rem;
    border-radius: 8px;
}

.error {
    color: var(--color-threat);
    margin-top: 8px;
}
</style>
