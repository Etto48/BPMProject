<script setup lang="ts">
import { ref } from 'vue';
import { ChevronDown } from 'lucide-vue-next';

interface Props {
    title: string;
    description: string;
}

defineProps<Props>();

const showDescription = ref(true);
</script>

<template>
    <div class="card gradient-border hoverable project-info" @click="showDescription = !showDescription">
        <h3 class="gradient-background capsule project-title" :class="{ 'open': showDescription }">
            <span>{{ title }}</span>
            <ChevronDown class="arrow" :class="{ 'open': showDescription }" :size="20" />
        </h3>
        <Transition name="description">
            <div v-if="showDescription" class="gradient-background-light project-description">
                <p>{{ description }}</p>
            </div>
        </Transition>
    </div>
</template>

<style scoped>
.project-info {
    cursor: pointer;
    transition: background-color 0.2s ease, border-color 0.2s ease;
}

.project-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2px 1rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0;
    transition: filter 0.3s ease, background-color 0.2s ease, margin-bottom 0.3s ease;
}

.project-title .arrow {
    transition: transform 0.3s ease;
    display: inline-flex;
    flex-shrink: 0;
}

.project-title .arrow.open {
    transform: rotate(180deg);
}

.project-title.open {
    margin-bottom: 1rem;
}

.project-description {
    border-radius: 8px;
    padding: 1rem;
    transition: filter 0.3s ease, background-color 0.2s ease;
}

.project-description p {
    margin: 0;
    display: block;
}

.description-enter-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.description-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.description-enter-from,
.description-leave-to {
    opacity: 0;
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    min-height: 0;
    margin: 0;
}

.description-enter-to,
.description-leave-from {
    opacity: 1;
    max-height: 200px;
}
</style>
