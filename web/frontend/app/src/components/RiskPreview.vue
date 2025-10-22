<script setup lang="ts">
import { ref } from 'vue';
import { RiskKind } from '@/types';

const risk_kind = ref<RiskKind>(RiskKind.Threat);
</script>

<template>
    <div class="card risk-preview" :class="risk_kind === RiskKind.Opportunity ? 'opportunity-border' : 'threat-border'">
        <div class="tab-selector">
            <button 
                :class="{ active: risk_kind === RiskKind.Opportunity }"
                @click="risk_kind = RiskKind.Opportunity"
                class="opportunity-tab"
            >
                Opportunity
            </button>
            <button 
                :class="{ active: risk_kind === RiskKind.Threat }"
                @click="risk_kind = RiskKind.Threat"
                class="threat-tab"
            >
                Threat
            </button>
        </div>
        <div class="input-group">
            <label for="risk-title">Title</label>
            <div class="input-wrapper" :class="risk_kind === RiskKind.Opportunity ? 'input-opportunity-border' : 'input-threat-border'">
                <input id="risk-title" class="title styled-input" type="text" :placeholder="risk_kind === RiskKind.Opportunity ? 'Opportunity title' : 'Threat title'" />
            </div>
        </div>
        <div class="input-group">
            <label for="risk-description">Description</label>
            <div class="input-wrapper" :class="risk_kind === RiskKind.Opportunity ? 'input-opportunity-border' : 'input-threat-border'">
                <textarea id="risk-description" class="description styled-input textarea-input" :placeholder="risk_kind === RiskKind.Opportunity ? 'Opportunity description' : 'Threat description'" rows="5"></textarea>
            </div>
        </div>
    </div>
</template>

<style scoped>
.risk-preview {
    flex: 1;
    min-width: 300px;
    padding: 2rem;
    transition: border-color 0.3s ease;
}

/* Threat Border */
.threat-border {
    border: 4px solid var(--color-threat);
}

/* Opportunity Border */
.opportunity-border {
    border: 4px solid var(--color-opportunity);
}

.tab-selector {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    background-color: var(--color-background-soft);
    padding: 0.25rem;
    border-radius: 8px;
}

.tab-selector button {
    flex: 1;
    padding: 0.75rem 1rem;
    border: none;
    background: transparent;
    color: var(--color-text);
    font-size: 1rem;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tab-selector button:hover {
    background-color: var(--color-background-mute);
}

.tab-selector button.threat-tab.active {
    background: var(--color-threat);
    color: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-selector button.opportunity-tab.active {
    background: var(--color-opportunity);
    color: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-group {
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.input-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    font-size: 0.95rem;
    color: var(--color-text);
}

.input-wrapper {
    position: relative;
    border-radius: 8px;
    transition: all 0.3s ease;
}

/* Threat Input Border */
.input-threat-border::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    z-index: -1;
    border-radius: inherit;
    background: var(--color-threat);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    padding: 2px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.input-threat-border:focus-within::before {
    opacity: 1;
}

/* Opportunity Input Border */
.input-opportunity-border::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    z-index: -1;
    border-radius: inherit;
    background: var(--color-opportunity);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    padding: 2px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.input-opportunity-border:focus-within::before {
    opacity: 1;
}

.styled-input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--color-border);
    border-radius: 8px;
    font-size: 1rem;
    background-color: var(--color-background-soft);
    color: var(--color-text);
    transition: all 0.3s ease;
    box-sizing: border-box;
    position: relative;
    display: block;
}

.styled-input:focus {
    outline: none;
    border-color: transparent;
    background-color: var(--color-background);
}

.styled-input::placeholder {
    color: var(--color-text-muted, #999);
}

.textarea-input {
    resize: none;
    min-height: 120px;
    font-family: inherit;
    line-height: 1.5;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .risk-preview {
        padding: 1.5rem;
    }

    .tab-selector button {
        padding: 0.625rem 0.75rem;
        font-size: 0.9rem;
    }

    .textarea-input {
        min-height: 100px;
    }
}
</style>