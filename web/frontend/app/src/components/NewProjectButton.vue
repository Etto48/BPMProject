<template>
    <button class="new-project-button card">
        <i class="bi bi-plus-lg"></i>
    </button>
</template>

<style scoped>
.new-project-button {
    background-color: var(--color-background);
    color: var(--color-text);
    min-width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    flex-grow: 1;
    transition: background-color 0.2s ease;
}

.new-project-button i {
    font-size: 3rem;
    display: block;
    aspect-ratio: 1 / 1;
    background-color: var(--color-border);
    border-radius: 50%;
}

@media (hover: hover) {
    .new-project-button:hover {
        background-color: var(--color-border);
        cursor: pointer;
    }
}
</style>