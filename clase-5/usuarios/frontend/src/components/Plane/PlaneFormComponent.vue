<template>
  <a-drawer
      :title="`${isEdit ? 'Editar' : 'Crear'} plano`"
      :width="720"
      :open="openForm"
      :body-style="{ paddingBottom: '80px' }"
      :footer-style="{ textAlign: 'right' }"
      :closable="false"
  >

    <a-form :model="form" :rules="rules" layout="vertical">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Nombre" name="name">
            <a-input v-model:value="form.name" placeholder="Ingresar nombre" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Versión" name="version">
            <a-input  v-model:value="form.version"  placeholder="Version" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Ruta del archivo" name="route_file">
            <a-input v-model:value="form.route_file"   placeholder="Ruta del archivo"></a-input>
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Estado" name="state">
            <a-select v-model:value="form.state" placeholder="Seleccionar estado">
              <a-select-option :value="1">Activo</a-select-option>
              <a-select-option :value="0">Inactivo</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>
    <template #footer>
      <a-space>
        <a-button @click.prevent="handleCloseForm">Cancelar</a-button>
        <a-button type="primary" @click="handleCreateOrUpdatePlane">Guardar</a-button>
      </a-space>
    </template>
  </a-drawer>
</template>

<script setup>
import { usePlaneComposable } from "@/composable/plane/plane.composable.js"


defineOptions({
  name: 'PlaneFormComponent'
})

const {form, handleCreateOrUpdatePlane, openForm, handleCloseForm, isEdit }  = usePlaneComposable()

</script>

<style></style>