<template>
  <div>
    <div>
      <h1>Planos</h1>
      <div>
        <a-button type="primary" @click="handleOpenForm">Crear plano</a-button>
      </div>
    </div>

    <div>
      <a-table
          :columns="columns"
          :dataSource="dataSource"
      >

      </a-table>
    </div>

    <PlaneFormComponent />
  </div>
</template>

<script setup>
import PlaneFormComponent from '@/components/Plane/PlaneFormComponent.vue'

import { usePlaneComposable } from "@/composable/plane/plane.composable.js"


const { dataSource, columns, handleOpenForm } = usePlaneComposable()

</script>

<style scoped></style>