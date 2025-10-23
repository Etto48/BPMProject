<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { ChevronDown, LogOut, User, Settings, HelpCircle } from 'lucide-vue-next';
import { useCurrentUser } from '@/composables/useCurrentUser';
import { useRouter } from 'vue-router';

const router = useRouter();
const { currentUser, isLoading, clearUser } = useCurrentUser();
const accountName = computed(() => currentUser.value?.username || '');
const isMenuOpen = ref(false);
const menuRef = ref<HTMLElement | null>(null);

function logout() {
    fetch('/api/logout', {
        method: 'GET',
        credentials: 'include',
    }).then(() => {
        clearUser();
        router.push('/login');
    });
}

function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value;
}

function closeMenu() {
    isMenuOpen.value = false;
}

function handleClickOutside(event: MouseEvent) {
    if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
        closeMenu();
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
});

</script>

<template>
    <div v-if="!isLoading && currentUser" class="account-menu-container" ref="menuRef">
        <div class="account-button" @click="toggleMenu">
            <img alt="Account Icon" src="@/assets/account-icon.svg" width="32" height="32" />
            <span>{{ accountName }}</span>
            <ChevronDown :class="{ rotated: isMenuOpen }" />
        </div>
        <div v-if="isMenuOpen" class="dropdown-backdrop" @click="closeMenu"></div>
        <div v-if="isMenuOpen" class="dropdown-menu">
            <button @click="closeMenu" class="dropdown-item">
                <User :size="20" />
                <span>Profile</span>
            </button>
            <button @click="closeMenu" class="dropdown-item">
                <Settings :size="20" />
                <span>Settings</span>
            </button>
            <button @click="closeMenu" class="dropdown-item">
                <HelpCircle :size="20" />
                <span>Help</span>
            </button>
            <div class="dropdown-divider"></div>
            <button @click="logout" class="dropdown-item">
                <LogOut :size="20" />
                <span>Logout</span>
            </button>
        </div>
    </div>
</template>

<style scoped>
.account-menu-container {
    position: relative;
}

.account-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    border: 2px solid var(--color-border);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    transition: background-color 0.2s;
}

.account-button:hover {
    background-color: var(--color-background-soft);
}

.account-button svg {
    transition: transform 0.3s ease;
}

.account-button svg.rotated {
    transform: rotate(180deg);
}

.dropdown-backdrop {
    display: none;
}

.dropdown-menu {
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    background-color: var(--color-background);
    border: 2px solid var(--color-border);
    border-radius: 10px;
    padding: 0.5rem;
    min-width: 150px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1001;
    animation: dropdownFadeIn 0.2s ease-out;
    transform-origin: top right;
}

.dropdown-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    padding: 0.75rem 1rem;
    border: none;
    background: none;
    cursor: pointer;
    border-radius: 8px;
    font-size: 1rem;
    color: var(--color-text);
    transition: background-color 0.2s;
}

.dropdown-item:hover {
    background-color: var(--color-background-soft);
}

.dropdown-divider {
    height: 1px;
    background-color: var(--color-border);
    margin: 0.5rem 0;
}

/* Mobile and below (max-width: 768px) */
@media (max-width: 768px) {
    .account-button {
        padding: 0.5rem;
    }

    .account-button span {
        display: none;
    }

    .account-button svg {
        display: none;
    }

    .account-menu-container {
        position: static;
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
        animation: fadeIn 0.3s ease-out;
    }

    .dropdown-menu {
        position: fixed;
        top: auto;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        min-width: unset;
        border-radius: 20px 20px 0 0;
        padding: 1rem;
        box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.2);
        animation: slideUp 0.3s ease-out;
        border-left: none;
        border-right: none;
        border-bottom: none;
    }

    .dropdown-item {
        padding: 1rem;
        font-size: 1.1rem;
        justify-content: flex-start;
    }

    .dropdown-item svg {
        width: 24px;
        height: 24px;
    }

    .dropdown-divider {
        margin: 0.75rem 0;
    }
}

@keyframes dropdownFadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
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