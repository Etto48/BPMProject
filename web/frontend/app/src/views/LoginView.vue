<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCurrentUser } from '@/composables/useCurrentUser';
import type { UserData } from '@/types';
import backgroundSvgDark from '../assets/background-dark.svg';
import backgroundSvgLight from '../assets/background-light.svg';
import logoSvg from '../assets/logo.svg';

const router = useRouter();
const { fetchUser } = useCurrentUser();

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const activeTab = ref<'login' | 'register'>('login');
const errorMessage = ref('');
const hasError = ref(false);

const passwordsMatch = computed(() => {
    return password.value === confirmPassword.value && password.value !== '';
});

const showPasswordMismatch = computed(() => {
    return activeTab.value === 'register' && 
           confirmPassword.value !== '' && 
           password.value !== confirmPassword.value;
});

const isRegisterDisabled = computed(() => {
    return activeTab.value === 'register' && !passwordsMatch.value;
});

function clearError() {
    errorMessage.value = '';
    hasError.value = false;
}

function login() {
    const body: UserData = {
        username: username.value,
        password: password.value
    };
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(body),
    }).then(async (response) => {
        if (response.ok) {
            await fetchUser(); // Fetch user data after successful login
            router.push('/');
        } else {
            hasError.value = true;
            if (response.status === 401) {
                errorMessage.value = 'Invalid username or password';
            } else {
                errorMessage.value = 'An error occurred. Please try again.';
            }
        }
    }).catch(() => {
        hasError.value = true;
        errorMessage.value = 'Network error. Please check your connection.';
    });
}

function register() {
    const body: UserData = {
        username: username.value,
        password: password.value
    };

    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(body),
    }).then(async (response) => {
        if (response.ok) {
            await fetchUser(); // Fetch user data after successful registration
            router.push('/');
        } else {
            hasError.value = true;
            if (response.status === 409) {
                errorMessage.value = 'Username already exists';
            } else {
                errorMessage.value = 'An error occurred. Please try again.';
            }
        }
    }).catch(() => {
        hasError.value = true;
        errorMessage.value = 'Network error. Please check your connection.';
    });
}

function selectTab(tab: 'login' | 'register') {
    activeTab.value = tab;
    clearError();
}

</script>

<template>
    <div class="login-background light" :style="{ backgroundImage: `url(${backgroundSvgLight})` }"></div>
    <div class="login-background dark" :style="{ backgroundImage: `url(${backgroundSvgDark})` }"></div>
    <div class="title-container">
        <img :src="logoSvg" alt="AIRA Logo" class="logo" />
        <h1 class="gradient-text">AIRA</h1>
    </div>
    <main class="card gradient-border">
        <div class="tab-selector">
            <button 
                :class="{ active: activeTab === 'login' }"
                @click="selectTab('login')"
            >
                Login
            </button>
            <button 
                :class="{ active: activeTab === 'register' }"
                @click="selectTab('register')"
            >
                Register
            </button>
        </div>

        <Transition name="error-fade">
            <div v-if="hasError" class="error-message">
                {{ errorMessage }}
            </div>
        </Transition>

        <div class="input-group">
            <label for="username">Username</label>
            <div class="input-wrapper input-gradient-border" :class="{ 'error-border': hasError }">
                <input id="username" type="text" placeholder="Enter your username" class="styled-input" v-model="username" @input="clearError" />
            </div>
        </div>
        <div class="input-group">
            <label for="password">Password</label>
            <div class="input-wrapper input-gradient-border" :class="{ 'error-border': hasError }">
                <input id="password" type="password" placeholder="Enter your password" class="styled-input" v-model="password" @input="clearError" />
            </div>
        </div>
        <Transition name="slide-fade">
            <div v-if="activeTab === 'register'" class="input-group">
                <label for="confirm-password">Confirm Password</label>
                <div class="input-wrapper input-gradient-border">
                    <input id="confirm-password" type="password" placeholder="Confirm your password" class="styled-input" v-model="confirmPassword" />
                </div>
            </div>
        </Transition>
        
        <Transition name="error-fade">
            <div v-if="showPasswordMismatch" class="warning-message">
                Passwords do not match
            </div>
        </Transition>
        
        <button class="gradient-button" :disabled="isRegisterDisabled" @click="activeTab === 'login' ? login() : register()">{{ activeTab === 'login' ? 'Login' : 'Register' }}</button>
    </main>
</template>

<style scoped>
.login-background {
    position: fixed;
    bottom: -30px;
    left: -30px;
    width: calc(100% + 60px);
    height: calc(100% + 60px);
    background-size: contain;
    background-repeat: no-repeat;
    background-position: left bottom;
    
    pointer-events: none;
    animation: background-animation 10s ease-in-out infinite;
}

@media (prefers-color-scheme: dark) {
    @keyframes background-animation {
        0%, 100% {
            filter: blur(20px) brightness(0.8);
            transform: scale(1.05);
        }
        50% {
            filter: blur(7px) brightness(1);
            transform: scale(1.3);
        }
    }    
}

@keyframes background-animation {
    0%, 100% {
        filter: blur(20px) brightness(1.2);
        transform: scale(1.05);
    }
    50% {
        filter: blur(7px) brightness(1);
        transform: scale(1.3);
    }
}

.login-background.light {
    display: block;
}

.login-background.dark {
    display: none;
}

@media (prefers-color-scheme: dark) {
    .login-background.light {
        display: none;
    }
    
    .login-background.dark {
        display: block;
    }
}

.title-container {
    position: absolute;
    top: 50%;
    left: 200px;
    display: flex;
    align-items: center;
    gap: 2rem;
    animation: title-animation 1s ease forwards;
}

@keyframes title-animation {
    0% {
        filter: blur(30px);
        transform: scale(3) translate(0, 0);
    }
    100% {
        filter: blur(0px);
        transform: scale(1) translate(0, -50%);
    }
}

.logo {
    width: 120px;
    height: 120px;
    object-fit: contain;
}

h1 {
    font-size: 128px;
    font-weight: 900;
    margin: 0;
}

main {
    position: absolute;
    top: 50%;
    right: 200px;
    transform: translate(0, -50%);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px var(--shadow-color);
    background-color: var(--color-background);
    min-width: 300px;
    width: 400px;
}

.tab-selector {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    background-color: var(--color-background-soft, #f5f5f5);
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
    background-color: var(--color-background-mute, #e0e0e0);
}

.tab-selector button.active {
    background: linear-gradient(125deg, var(--color-accent-1), var(--color-accent-2));
    color: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.gradient-button {
    width: 100%;
    margin-top: 0.5rem;
}

.gradient-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    filter: grayscale(0.5);
}

/* Error message */
.error-message {
    background-color: rgba(var(--color-threat-rgb, 220, 38, 38), 0.1);
    color: var(--color-threat);
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid var(--color-threat);
}

/* Warning message */
.warning-message {
    background-color: rgba(255, 193, 7, 0.1);
    color: #f59e0b;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid #f59e0b;
    text-align: center;
}

/* Error border for inputs */
.input-wrapper.error-border {
    border: 2px solid var(--color-threat) !important;
    background: linear-gradient(var(--color-background), var(--color-background)) padding-box,
                linear-gradient(125deg, var(--color-threat), var(--color-threat)) border-box !important;
}

/* Transition animations */
.error-fade-enter-active,
.error-fade-leave-active {
    transition: all 0.3s ease;
}

.error-fade-enter-from,
.error-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.error-fade-enter-to,
.error-fade-leave-from {
    opacity: 1;
    transform: translateY(0);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    max-height: 0;
    margin-bottom: 0;
    transform: translateY(-10px);
}

.slide-fade-enter-to,
.slide-fade-leave-from {
    opacity: 1;
    max-height: 100px;
    margin-bottom: 1.5rem;
    transform: translateY(0);
}

/* Responsive Design */

/* Desktop - Continuous scaling with viewport width */
.title-container {
    left: clamp(50px, 10vw, 200px);
}

main {
    right: clamp(50px, 10vw, 200px);
}

h1 {
    font-size: clamp(64px, 8vw, 128px);
}

.logo {
    width: clamp(60px, 7.5vw, 120px);
    height: clamp(60px, 7.5vw, 120px);
}

/* Mobile (max-width: 1024px) */
@media (max-width: 1024px) {
    .login-background {
        background-size: cover;
        background-position: center;
        width: 100vw;
        height: 100vh;
    }

    .title-container {
        position: relative;
        left: 0;
        top: 60px;
        right: 0;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: clamp(30px, 8vh, 60px) auto 0;
        width: 100%;
        padding: 0 16px;
    }

    main {
        left: calc(50% - 10px);
        top: 250px;
        transform: translate(-50%, 0);
        width: min(calc(100% - 32px), 500px);
    }

    h1 {
        font-size: clamp(32px, 10vw, 56px);
        text-align: center;
    }

    .logo {
        width: clamp(40px, 12vw, 64px);
        height: clamp(40px, 12vw, 64px);
    }

    .tab-selector button {
        padding: 0.625rem 0.75rem;
        font-size: 0.9rem;
    }

    .input-group {
        margin-bottom: 1.25rem;
    }

    .input-group input {
        padding: 0.625rem 0.875rem;
        font-size: 0.95rem;
    }
}
</style>