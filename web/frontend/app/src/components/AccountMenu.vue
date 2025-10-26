<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { ChevronDown, LogOut, User, HelpCircle } from 'lucide-vue-next';
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
            <span class="account-name">{{ accountName }}</span>
            <ChevronDown :class="{ rotated: isMenuOpen }" />
        </div>
        <Transition name="backdrop">
            <div v-if="isMenuOpen" class="dropdown-backdrop" @click="closeMenu"></div>
        </Transition>
        <Transition name="dropdown">
            <div v-if="isMenuOpen" class="dropdown-menu">
                <button @click="{{closeMenu(); router.push('/profile');}}" class="dropdown-item">
                    <User :size="20" />
                    <span>Profile</span>
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
        </Transition>
    </div>
</template>

<style scoped>
.account-menu-container {
    position: relative;
    height: 100%;
    display: flex;
    align-items: stretch;
}

.account-button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    cursor: pointer;
    border: 2px solid var(--color-border);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    transition: background-color 0.2s, border-radius 0.2s;
    height: 100%;
    width: 200px;
}

.account-name {
    text-align: start;
    margin-right: auto;
}

.account-menu-container:has(.dropdown-menu) .account-button {
    border-radius: 10px 10px 0 0;
    border-bottom-color: transparent;
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
    top: 100%;
    left: 0;
    right: 0;
    background-color: var(--color-background);
    border: 2px solid var(--color-border);
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1001;
    transform-origin: top;
}

.dropdown-enter-active {
    animation: dropdownFadeIn 0.2s ease-out;
}

.dropdown-leave-active {
    animation: dropdownFadeOut 0.2s ease-in;
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
        width: unset;
    }

    .account-button span {
        display: none;
    }

    .account-button svg {
        display: none;
    }

    .account-menu-container:has(.dropdown-menu) .account-button {
        border-radius: 10px;
        border-bottom-color: var(--color-border);
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
        border: 2px solid var(--color-border);
        border-radius: 20px 20px 0 0;
        padding: 1rem;
        box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.2);
        border-left: 2px solid var(--color-border);
        border-right: 2px solid var(--color-border);
        border-top: 2px solid var(--color-border);
        border-bottom: none;
    }

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
        transform: scaleY(0);
    }
    to {
        opacity: 1;
        transform: scaleY(1);
    }
}

@keyframes dropdownFadeOut {
    from {
        opacity: 1;
        transform: scaleY(1);
    }
    to {
        opacity: 0;
        transform: scaleY(0);
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