<template>
    <div class="threshold-control">
        <label for="risk-threshold">
            <span class="threshold-label-text">Risk Threshold</span>
            <span class="threshold-value">{{ (modelValue * 100).toFixed(0) }}%</span>
        </label>
        <div class="slider-wrapper">
            <input 
                id="risk-threshold"
                type="range" 
                :value="modelValue"
                @input="handleInput"
                min="0" 
                max="1" 
                step="0.01"
                class="threshold-slider"
            />
            <div class="threshold-labels">
                <span>100%</span>
                <span>75%</span>
                <span>50%</span>
                <span>25%</span>
                <span>0%</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    modelValue: number
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: number): void
}>()

const handleInput = (event: Event) => {
    const target = event.target as HTMLInputElement
    emit('update:modelValue', Number(target.value))
}
</script>

<style scoped>
.threshold-control {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem 0 1rem 1rem;
    border-left: 1px solid var(--color-border);
    position: relative;
    align-self: stretch;
    box-sizing: border-box;
}

.slider-wrapper {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    height: 100%;
}

.threshold-control label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--color-heading);
    text-align: center;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    margin-bottom: 1rem;
}

.threshold-label-text {
    white-space: nowrap;
}

.threshold-value {
    font-size: 1.1rem;
    color: var(--color-text)
}

.threshold-slider {
    width: 6px;
    max-height: calc(100vh - 28rem);
    border-radius: 3px;
    background: var(--color-border);
    outline: none;
    -webkit-appearance: slider-vertical;
    appearance: auto;
    writing-mode: vertical-lr;
    direction: rtl;
    cursor: pointer;
}

.threshold-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--color-accent-1);
    cursor: pointer;
    transition: all 0.2s ease;
}

.threshold-slider::-webkit-slider-thumb:hover,
.threshold-slider::-webkit-slider-thumb:active {
    background: var(--color-accent-2);
    transform: scale(1.1);
}

.threshold-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--color-accent-1);
    cursor: pointer;
    border: none;
    transition: all 0.2s ease;
}

.threshold-slider::-moz-range-thumb:hover,
.threshold-slider::-moz-range-thumb:active {
    background: var(--color-accent-2);
    transform: scale(1.1);
}

.threshold-labels {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    margin-top: 0;
    margin-left: 0;
    font-size: 0.875rem;
    color: var(--color-text-dim-opaque);
}

@media (max-width: 1024px) {
    .threshold-control {
        flex-direction: row;
        border-left: none;
        border-top: 1px solid var(--color-border);
        padding: 1rem 1rem 0 1rem;
        height: fit-content;
        align-items: center;
        justify-content: center;
    }
    
    .threshold-control label {
        writing-mode: horizontal-tb;
        transform: rotate(0deg);
        margin-bottom: 0;
        margin-right: 1rem;
        height: fit-content;
    }
    
    .slider-wrapper {
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: fit-content;
    }
    
    .threshold-labels {
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
        height: fit-content;
    }
    
    .threshold-slider {
        width: 100%;
        height: 6px;
        -webkit-appearance: slider-horizontal;
        appearance: auto;
        writing-mode: horizontal-tb;
        direction: ltr;
        cursor: pointer;
    }
}
</style>
