<script setup lang="ts">
import { computed } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router';
import AccountMenu from '@/components/AccountMenu.vue';

const route = useRoute();
const isLoginView = computed(() => route.name === 'login' || route.name == null);
</script>

<template>
  <header v-if="!isLoginView">
    <div class="nav-title-container">
      <nav>
        <RouterLink to="/">
          <img alt="AIRA logo" class="logo" src="@/assets/logo.svg" />
          <span class="gradient-text">AIRA</span>
        </RouterLink>
      </nav>
    </div>
    <AccountMenu />
  </header>

  <RouterView />
</template>

<style scoped>

header {
  line-height: 1.5;
  position: sticky;
  position: -webkit-sticky;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  width: 100%;
  height: fit-content;
  display: flex;
  flex-direction: row;
  z-index: 1000;
  background-color: var(--color-background);
  box-shadow: 0 10px 10px var(--shadow-color);
  padding: 1rem;
  margin-bottom: 0;
}

.nav-title-container {
  display: flex;
  align-items: center;
  margin-right: auto;
}

.logo {
  display: block;
  width: 37.5px;
  height: 37.5px;
  object-fit: contain;
}

nav {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-size: 40px;
  font-weight: 900;
}

nav a {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

nav a span {
  font-weight: 900;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

/* Mobile (max-width: 768px) */
@media (max-width: 768px) {
  header {
    padding: 0.75rem 1rem;
    margin-bottom: 1.5rem;
  }

  nav a span {
    display: none;
  }

  nav a {
    gap: 0;
  }

  .logo {
    width: 32px;
    height: 32px;
  }
}

</style>
