<template>
  <div class="table-users-component">
    <div class="actions">
      <a-button type="primary" @click.prevent="handleOpen">Crear usuario</a-button>
    </div>

    <div>
      <div class="title">Listado de usuarios</div>
      <a-table
          bordered
          :dataSource="dataSource"
          :columns="columns"
          @change="handleChangeTable"
          :pagination="{
            total: pagination.total,
            showTotal: (total) => `Total ${total} usuarios`,
            showSizeChanger: true,
            pageSizeOptions: ['5', '10', '20', '50']
        }">
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'options'">
            <div class="list-actions">
              <edit-outlined class="action-icon" @click="handleEdit(record)" />
              <eye-outlined class="action-icon" @click="handleView(record)" />
              <delete-outlined class="action-icon" @click="handleDelete(record)" />
            </div>
          </template>
          <div v-if="column.key === 'type'">
            <a-tag v-if="column.key === 'type'" :color="record.type === 1 ? 'success' : 'error'">
              {{ record.type === 1 ? 'Activo' : 'Inactivo' }}
            </a-tag>
          </div>
        </template>
      </a-table>
    </div>
  </div>

  <FormUserComponent/>
</template>

<script setup>
import {EditOutlined, EyeOutlined, DeleteOutlined} from '@ant-design/icons-vue';
import FormUserComponent from "@/components/Users/FormUserComponent.vue";
import {useUserComposable} from "@/composable/users/user.composable..js";

defineOptions({
  name: 'TableUserComponent',
})

const {columns, pagination, dataSource, handleOpen, handleChangeTable} = useUserComposable()

</script>

<style scoped>
.table-users-component {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  .actions {
    display: flex;
    justify-content: flex-end;
  }

  .title {
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 1rem;
  }

  .list-actions {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    font-size: 1rem;
    cursor: pointer;
  }
}

</style>