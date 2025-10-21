<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { ref } from 'vue';
import backgroundSvg from '../assets/background.svg';
import logoSvg from '../assets/logo.svg';

const activeTab = ref<'login' | 'register'>('login');
</script>

<template>
    <div class="login-background" :style="{ backgroundImage: `url(${backgroundSvg})` }"></div>
    <div class="title-container">
        <img :src="logoSvg" alt="AIRA Logo" class="logo" />
        <h1 class="gradient-text">AIRA</h1>
    </div>
    <div class="card gradient-border">
        <div class="tab-selector">
            <button 
                :class="{ active: activeTab === 'login' }"
                @click="activeTab = 'login'"
            >
                Login
            </button>
            <button 
                :class="{ active: activeTab === 'register' }"
                @click="activeTab = 'register'"
            >
                Register
            </button>
        </div>

        <div class="input-group">
            <label for="username">Username</label>
            <div class="input-wrapper">
                <input id="username" type="text" placeholder="Enter your username" />
            </div>
        </div>
        <div class="input-group">
            <label for="password">Password</label>
            <div class="input-wrapper">
                <input id="password" type="password" placeholder="Enter your password" />
            </div>
        </div>
        <Transition name="slide-fade">
            <div v-if="activeTab === 'register'" class="input-group">
                <label for="confirm-password">Confirm Password</label>
                <div class="input-wrapper">
                    <input id="confirm-password" type="password" placeholder="Confirm your password" />
                </div>
            </div>
        </Transition>
        <button class="gradient-button">{{ activeTab === 'login' ? 'Login' : 'Register' }}</button>
    </div>
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
    filter: blur(15px);
    pointer-events: none;
}

.title-container {
    position: absolute;
    top: 50%;
    left: 200px;
    transform: translate(0, -50%);
    display: flex;
    align-items: center;
    gap: 2rem;
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

.card {
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

.input-wrapper::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    z-index: -1;
    border-radius: inherit;
    background: linear-gradient(125deg, var(--color-accent-1), var(--color-accent-2));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    padding: 2px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.input-wrapper:focus-within::before {
    opacity: 1;
}

.input-group input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--color-border, #e0e0e0);
    border-radius: 8px;
    font-size: 1rem;
    background-color: var(--color-background-soft, #f5f5f5);
    color: var(--color-text);
    transition: all 0.3s ease;
    box-sizing: border-box;
    position: relative;
    display: block;
}

.input-group input:focus {
    outline: none;
    border-color: transparent;
    background-color: var(--color-background);
}

.input-group input::placeholder {
    color: var(--color-text-muted, #999);
}

.gradient-button {
    width: 100%;
    margin-top: 0.5rem;
}

/* Transition animations */
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

.card {
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
        right: 0;
        transform: none;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-direction: column;
        margin: clamp(30px, 8vh, 60px) auto 0;
        width: 100%;
        padding: 0 16px;
    }

    .card {
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