<script setup lang="ts">
import { useProject } from '@/composables/useProject';
import { stepNames } from '@/constants';
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ChevronRight, ChevronDown } from 'lucide-vue-next';

const route = useRoute()
const router = useRouter()
const { project, projectId } = useProject()
const isMenuOpen = ref(false)
const menuRef = ref<HTMLElement | null>(null)

const selectedStep = computed(() => {
    if (route.name === 'risk-discovery') {
        return 0
    } else if (route.name === 'qualitative-analysis') {
        return 1
    } else if (route.name === 'planning') {
        return 2
    } else if (route.name === 'project-overview') {
        return 3
    } else {
        return null
    }
})
const currentStep = computed(() => project.value?.currentStep)

const currentStepName = computed(() => {
    if (selectedStep.value === 0) return 'Risk Discovery'
    if (selectedStep.value === 1) return 'Qualitative Analysis'
    if (selectedStep.value === 2) return 'Planning'
    if (selectedStep.value === 3) return 'Project Overview'
    return 'Select Step'
})

function navigateToStep(step: 0 | 1 | 2 | 3) {
    router.push(`/project/${projectId.value}/${stepNames[step]}`)
    closeMenu()
}

function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value
}

function closeMenu() {
    isMenuOpen.value = false
}

function handleClickOutside(event: MouseEvent) {
    if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
        closeMenu()
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})

</script>

<template>
    <div v-if="currentStep !== undefined" class="progress-nav-container" ref="menuRef">
        <!-- Desktop View -->
        <div class="progress-nav">
            <button class="progress-nav-button" :class="{ active: selectedStep === 0 }" :disabled="currentStep<0 || selectedStep == 0" @click="navigateToStep(0)">
                Risk Discovery
            </button>
            <ChevronRight class="arrow" />
            <button class="progress-nav-button" :class="{ active: selectedStep === 1 }" :disabled="currentStep<1 || selectedStep == 1" @click="navigateToStep(1)">
                Qualitative Analysis
            </button>
            <ChevronRight class="arrow" />
            <button class="progress-nav-button" :class="{ active: selectedStep === 2 }" :disabled="currentStep<2 || selectedStep == 2" @click="navigateToStep(2)">
                Planning
            </button>
            <ChevronRight class="arrow" />
            <button class="progress-nav-button" :class="{ active: selectedStep === 3 }" :disabled="currentStep<3 || selectedStep == 3" @click="navigateToStep(3)">
                Project Overview
            </button>
        </div>

        <!-- Mobile View -->
        <button class="mobile-step-button" @click="toggleMenu">
            <span>{{ currentStepName }}</span>
            <ChevronDown :class="{ rotated: isMenuOpen }" />
        </button>
        
        <Transition name="backdrop">
            <div v-if="isMenuOpen" class="dropdown-backdrop" @click="closeMenu"></div>
        </Transition>
        
        <Transition name="dropdown">
            <div v-if="isMenuOpen" class="dropdown-menu">
                <button 
                    class="dropdown-item" 
                    :class="{ active: selectedStep === 0, disabled: currentStep < 0 }" 
                    :disabled="currentStep < 0"
                    @click="navigateToStep(0)"
                >
                    <span class="step-number">1</span>
                    <span>Risk Discovery</span>
                </button>
                <button 
                    class="dropdown-item" 
                    :class="{ active: selectedStep === 1, disabled: currentStep < 1 }" 
                    :disabled="currentStep < 1"
                    @click="navigateToStep(1)"
                >
                    <span class="step-number">2</span>
                    <span>Qualitative Analysis</span>
                </button>
                <button 
                    class="dropdown-item" 
                    :class="{ active: selectedStep === 2, disabled: currentStep < 2 }" 
                    :disabled="currentStep < 2"
                    @click="navigateToStep(2)"
                >
                    <span class="step-number">3</span>
                    <span>Planning</span>
                </button>
                <button 
                    class="dropdown-item" 
                    :class="{ active: selectedStep === 3, disabled: currentStep < 3 }" 
                    :disabled="currentStep < 3"
                    @click="navigateToStep(3)"
                >
                    <span class="step-number">4</span>
                    <span>Project Overview</span>
                </button>
            </div>
        </Transition>
    </div>
</template>


<style scoped>
.progress-nav-container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    margin: 0 2rem;
}

.progress-nav {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 1rem;
}

.progress-nav-button {
    background: none;
    border: none;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    color: var(--color-text-opaque);
    transition: all 0.2s ease;
}

.progress-nav-button.active {
    cursor: default;
    font-weight: 600;
    background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

@media (hover: hover) {
    .progress-nav-button:hover:not(:disabled) {
        filter: brightness(0.5);
    }
}

@media (prefers-color-scheme: dark) {
    @media (hover: hover) {
        .progress-nav-button:hover:not(:disabled) {
            filter: brightness(1.5);
        }
    }
}

.progress-nav-button:disabled:not(.active) {
    cursor: not-allowed;
    color: var(--color-text-muted);
}

/* Mobile elements - hidden by default */
.mobile-step-button {
    display: none;
}

.dropdown-backdrop {
    display: none;
}

.dropdown-menu {
    display: none;
}

/* Mobile and tablet view (max-width: 1024px) */
@media (max-width: 1024px) {
    .progress-nav-container {
        margin: 0 1rem;
        position: relative;
    }

    /* Hide desktop navigation */
    .progress-nav {
        display: none;
    }

    /* Show mobile button */
    .mobile-step-button {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        width: 100%;
        padding: 0.75rem 1rem;
        background: var(--color-background);
        border: 2px solid var(--color-border);
        border-radius: 10px;
        cursor: pointer;
        font-size: 1rem;
        color: var(--color-text-opaque);
        transition: background-color 0.2s;
    }

    .mobile-step-button:hover {
        background-color: var(--color-background-soft);
    }

    .mobile-step-button svg {
        transition: transform 0.3s ease;
        flex-shrink: 0;
    }

    .mobile-step-button svg.rotated {
        transform: rotate(180deg);
    }

    .dropdown-backdrop {
        display: block;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }

    .dropdown-menu {
        display: flex;
        flex-direction: column;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: var(--color-background);
        border: 2px solid var(--color-border);
        border-bottom: none;
        border-radius: 20px 20px 0 0;
        padding: 1rem;
        box-shadow: 0 -4px 12px var(--shadow-color);
        z-index: 1001;
        gap: 0.5rem;
    }

    .dropdown-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
        padding: 1rem;
        border: none;
        background: none;
        cursor: pointer;
        border-radius: 10px;
        font-size: 1rem;
        color: var(--color-text-opaque);
        transition: background-color 0.2s;
        text-align: left;
    }

    .dropdown-item:hover:not(:disabled) {
        background-color: var(--color-background-soft);
    }

    .dropdown-item.active {
        font-weight: 600;
        background: linear-gradient(135deg, var(--color-accent-1-light), var(--color-accent-2-light));
    }

    .dropdown-item.active span:not(.step-number) {
        background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .dropdown-item:disabled {
        cursor: not-allowed;
        color: var(--color-text-muted);
        opacity: 0.5;
    }

    .step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: var(--color-background-mute);
        font-weight: 600;
        flex-shrink: 0;
    }

    .dropdown-item.active .step-number {
        background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2));
        color: white;
    }

    /* Animations */
    .dropdown-enter-active {
        animation: slideUp 0.3s ease-out;
    }

    .dropdown-leave-active {
        animation: slideDown 0.3s ease-in;
    }

    .backdrop-enter-active {
        animation: fadeIn 0.3s ease-out;
    }

    .backdrop-leave-active {
        animation: fadeOut 0.3s ease-in;
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes fadeOut {
    from {
        opacity: 1;
    }
    to {
        opacity: 0;
    }
}

@keyframes slideDown {
    from {
        transform: translateY(0);
        opacity: 1;
    }
    to {
        transform: translateY(100%);
        opacity: 0;
    }
}

@keyframes slideUp {
    from {
        transform: translateY(100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
</style>
