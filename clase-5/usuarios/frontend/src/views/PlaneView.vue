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
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'options'">
            <div class="list-actions">
              <edit-outlined class="action-icon" @click="handleEdit(record._id)" />
              <delete-outlined class="action-icon" @click="handleDelete(record._id)" />
            </div>
          </template>
        </template>

      </a-table>
    </div>

    <PlaneFormComponent />
  </div>
</template>

<script setup>
import PlaneFormComponent from '@/components/Plane/PlaneFormComponent.vue'

import { usePlaneComposable } from "@/composable/plane/plane.composable.js"
import {DeleteOutlined, EditOutlined, EyeOutlined} from "@ant-design/icons-vue";


const { dataSource, columns, handleOpenForm, handleEdit, handleDelete } = usePlaneComposable()

</script>

<style scoped>
.list-actions {
  display: flex;
  gap: 10px;
  font-size: 18px;
  justify-content: center;
  cursor: pointer;
}
</style>