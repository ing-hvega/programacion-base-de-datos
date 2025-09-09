<template>
  <div class="table-users-component">
    <div class="actions">
      <a-button type="primary" @click.prevent="handleOpen">Crear usuario</a-button>
    </div>

    <div>
      <a-table bordered :dataSource="dataSource" :columns="columns"/>
    </div>
  </div>

  <FormUserComponent />
</template>

<script setup>
import FormUserComponent from "@/components/Users/FormUserComponent.vue";
import {useUserComposable} from "@/composable/users/user.composable..js";

defineOptions({
  name: 'TableUserComponent',
})

const {columns, dataSource, handleOpen} = useUserComposable()
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
}

</style>