<script setup lang="ts">
import { ArrowLeft, ArrowRight } from 'lucide-vue-next';
import { computed } from 'vue';

const props = defineProps<{
    total: number;
    completed: number;
}>();

const maskImage = computed(() => {
    const dotSize = 12; // 12px
    const gap = 8; // 0.5rem = 8px
    const masks: string[] = [];
    
    for (let i = 0; i < props.completed; i++) {
        const position = i * (dotSize + gap);
        const radius = dotSize / 2;
        // Add a small gradient transition (0.5px) for antialiasing
        masks.push(`radial-gradient(circle at ${position + radius}px center, black ${radius - 0.5}px, transparent ${radius + 0.5}px)`);
    }
    
    return masks.length > 0 ? masks.join(', ') : 'none';
});
</script>

<template>
    <div class="progress-nav">
        <button class="nav-button"><ArrowLeft /></button>
        <div class="progress-indicator" :style="{ '--mask-image': maskImage }">
            <div 
                v-for="index in total" 
                :key="index" 
                class="dot"
                :class="{ 'completed': index <= completed }"
            />
        </div>
        <button class="nav-button"><ArrowRight /></button>
    </div>
</template>

<style scoped>
.progress-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin: auto 0 1rem 0;
    padding: 0 2rem;
}

.progress-indicator {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    position: relative;
}

.progress-indicator::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    height: 12px;
    width: 100%;
    background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2));
    pointer-events: none;
    z-index: 0;
    mask-image: var(--mask-image);
    -webkit-mask-image: var(--mask-image);
    mask-size: 100% 100%;
    -webkit-mask-size: 100% 100%;
    mask-composite: add;
    -webkit-mask-composite: source-over;
    transition: mask-image 0.3s ease;
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: var(--color-border);
    position: relative;
    z-index: 1;
    flex-shrink: 0;
    transition: all 0.3s ease;
}

.nav-button {
    background: none;
    border: none;
    color: var(--color-text-dim-opaque);
    cursor: pointer;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.2s ease;
}

@media (hover: hover) {
    .nav-button:hover {
        color: var(--color-accent-1);
    }
}
</style>