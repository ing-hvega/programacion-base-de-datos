<template>
  <a-config-provider :locale="locale">
    <RouterView />
  </a-config-provider>
</template>

<script setup>
import { RouterView } from 'vue-router';
import es_ES from 'ant-design-vue/es/locale/es_ES';

const locale = es_ES;
</script>
