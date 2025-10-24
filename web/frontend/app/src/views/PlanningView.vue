<script setup lang="ts">
import { ref } from 'vue';
import ProjectAndRisksSidePanel from '@/components/ProjectAndRisksSidePanel.vue';
import { useRoute, useRouter } from 'vue-router';
import type { TrackedManagedRisk } from '@/types';

const route = useRoute();
const router = useRouter();
const projectId = Number(route.params.id);

const threats = ref<Array<TrackedManagedRisk>>([]);
const opportunities = ref<Array<TrackedManagedRisk>>([]);

</script>

<template>
    <main>
        <ProjectAndRisksSidePanel 
            :threats="threats"
            :opportunities="opportunities"
            :allow-remove="false"
        />
        <div></div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    width: 100%;
    padding: 0;
    flex-direction: row;
    gap: 2rem;
    justify-content: stretch;
    flex: 1;
    overflow: hidden;
}


@media (max-width: 768px) {
    main {
        gap: 0;
        flex-direction: column-reverse;
        align-items: stretch;
        height: auto;
    }
}
</style>