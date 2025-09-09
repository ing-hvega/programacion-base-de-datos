<template>
  <a-drawer
      title="Crear usuarios"
      :width="600"
      :open="openForm"
      :footer-style="{ textAlign: 'right' }"
      :closable="false"
  >
    <a-form :model="form" layout="vertical">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Nombre" name="name">
            <a-input v-model:value="form.name" placeholder="Ingrese un nombre" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Correo" name="url">
            <a-input v-model:value="form.email"  placeholder="Ingrese un correo" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Contraseña" name="url">
            <a-input-password v-model:value="form.password"  placeholder="Ingrese una contraseña" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Estado" name="type">
            <a-select v-model:value="form.type" placeholder="Selecciona un estado">
              <a-select-option :value="1">Activo</a-select-option>
              <a-select-option :value="0">Inactivo</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="24">
          <a-form-item label="Comentario" name="description">
            <a-textarea
                v-model:value="form.description"
                :rows="4"
                placeholder="Ingrese un comentario"
            />
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>

    <template #footer>
      <a-space>
        <a-button @click.prevent="handleCancel">Cancelar</a-button>
        <a-button type="primary" @click.prevent="handleSaveForm" :loading="loading">Guardar</a-button>
      </a-space>
    </template>
  </a-drawer>
</template>

<script setup>

import {useUserComposable} from "@/composable/users/user.composable..js";

defineOptions({
  name: 'FormUserComponent',
})

const {form, loading, openForm, handleCancel, handleSaveForm} = useUserComposable({ loadDataOnMount: false });

</script>

<style></style>