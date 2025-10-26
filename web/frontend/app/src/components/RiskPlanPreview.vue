<script setup lang="ts">
import type { TrackedManagedRisk } from '@/types';
import { RiskKind } from '@/types';
import { computed } from 'vue';
import { Sparkles } from 'lucide-vue-next';
import RiskInfoSection from './RiskInfoSection.vue';

const props = defineProps<{
    risks: Array<TrackedManagedRisk>
    index: number
    isLoading?: boolean
}>();

const currentRisk = computed(() => {
    return props.risks[props.index] || {
        id: 0,
        kind: RiskKind.Threat,
        title: '',
        description: '',
        impact: 0,
        probability: 0,
        contingency: '',
        fallback: ''
    };
})

// Calculate the split point for the progress bar background
const opportunityCount = computed(() => {
    return props.risks.filter(r => r.kind === 'opportunity').length;
});

const splitPercentage = computed(() => {
    return (opportunityCount.value / props.risks.length) * 100;
});

defineEmits<{
    (e: 'accept'): void
}>();
</script>

<template>
    <svg width="0" height="0" style="position: absolute;">
        <defs>
            <linearGradient id="sparkle-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color: var(--color-accent-1); stop-opacity: 1" />
                <stop offset="100%" style="stop-color: var(--color-accent-2); stop-opacity: 1" />
            </linearGradient>
        </defs>
    </svg>
    <div class="flex-column preview-wrapper">
        <div class="preview-container card" :class="currentRisk.kind">
            <!-- Loading Overlay -->
            <Transition name="fade">
                <div v-if="isLoading" class="loading-overlay">
                    <div class="loading-content">
                        <Sparkles class="sparkle-icon" :size="48" />
                        <p class="loading-text">Generating risk management plans...</p>
                    </div>
                </div>
            </Transition>

            <div class="progress-indicator">
                <span class="progress-text">Risk {{ index + 1 }} of {{ risks.length }}</span>
                <div class="progress-bar">
                    <div class="progress-background" :style="{ 
                        background: `linear-gradient(to right, var(--color-opportunity) 0%, var(--color-opportunity) ${splitPercentage}%, var(--color-threat) ${splitPercentage}%, var(--color-threat) 100%)`
                    }"></div>
                    <div class="progress-fill" :style="{ 
                        background: `linear-gradient(to right, var(--color-opportunity) 0%, var(--color-opportunity) ${splitPercentage}%, var(--color-threat) ${splitPercentage}%, var(--color-threat) 100%)`,
                        clipPath: `inset(0 ${100 - ((index + 1) / risks.length) * 100}% 0 0)`
                    }"></div>
                </div>
            </div>
            
            <RiskInfoSection :risk="currentRisk" />

            <div class="input-group">
                <label for="contingency">Contingency Plan</label>
                <div class="input-wrapper">
                    <textarea 
                        id="contingency" 
                        v-model="currentRisk.contingency" 
                        placeholder="No contingency plan provided."
                        rows="3"
                        class="styled-input textarea-input"
                    ></textarea>
                </div>
            </div>

            <div class="input-group">
                <label for="fallback">Fallback Plan</label>
                <div class="input-wrapper">
                    <textarea 
                        id="fallback" 
                        v-model="currentRisk.fallback" 
                        placeholder="No fallback plan provided."
                        rows="3"
                        class="styled-input textarea-input"
                    ></textarea>
                </div>
            </div>

            <div class="button-wrapper">
                <button class="gradient-button" @click="$emit('accept')">
                    {{ index < risks.length - 1 ? 'Accept & Continue' : 'Accept & Finish' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import '@/assets/risk-shared.css';

.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--color-background-mute);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
    border-radius: inherit;
}

.loading-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}

.sparkle-icon {
    fill: url(#sparkle-gradient);
    stroke: url(#sparkle-gradient);
    animation: sparkle-pulse 1.5s ease-in-out infinite;
}

@keyframes sparkle-pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 0.7;
    }
    50% {
        transform: scale(1.2);
        opacity: 1;
    }
}

.loading-text {
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--color-text);
    margin: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.progress-indicator {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.progress-text {
    font-size: 0.9rem;
    color: var(--color-text-muted, #999);
    font-weight: 500;
}

.progress-bar {
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}

.progress-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.2;
    z-index: 0;
}

.progress-fill {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: clip-path 0.3s ease;
    z-index: 1;
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-group label {
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--color-text);
}

.input-wrapper {
    position: relative;
    border-radius: 8px;
}

.styled-input {
    width: 100%;
    padding: 0.625rem 0.875rem;
    border: 2px solid var(--color-border);
    border-radius: 8px;
    font-size: 0.95rem;
    background-color: var(--color-background-soft);
    color: var(--color-text);
    transition: all 0.3s ease;
    box-sizing: border-box;
    font-family: inherit;
    line-height: 1.4;
}

.styled-input:focus {
    outline: none;
    border-color: var(--color-accent-1);
    background-color: var(--color-background);
}

.styled-input::placeholder {
    color: var(--color-text-muted, #999);
}

.textarea-input {
    resize: none;
    min-height: 60px;
}

.button-wrapper {
    display: flex;
    justify-content: flex-end;
    margin-top: 0;
}

.button-wrapper button {
    min-width: 200px;
}

@media (max-width: 768px) {
    .button-wrapper button {
        width: 100%;
    }
}
</style>
