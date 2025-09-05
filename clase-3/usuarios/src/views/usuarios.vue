<template>
  <a-table :columns="columns" :data-source="dataSource">

  </a-table>
</template>


<script setup>
import {useUsuariosComposable} from "@/composable/usuarios.composable.js"

const {dataSource, columns} = useUsuariosComposable()


</script>

<style>

</style>