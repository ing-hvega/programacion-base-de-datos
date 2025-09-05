<template>
  <div class="about">

    Contador: {{count}}

    <a-button type="primary" @click="handleIncrement" >+</a-button>
    <a-button type="primary" @click="handleDecrement">-</a-button>
  </div>
</template>

<script setup>

import {useCounterComposable} from "@/composable/counter.composable.js"


const {
  count,
  handleIncrement,
  handleDecrement,
} = useCounterComposable()

</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
