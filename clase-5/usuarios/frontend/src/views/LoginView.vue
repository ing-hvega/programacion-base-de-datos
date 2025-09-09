<template>
  <div class="login-container">
    <a-form
        name="basic"
        autocomplete="off"
        class="login-form"
        :model="form"
    >
      <div class="logo-container">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTodTA_uzjXXbVJxfatvmWfGMZoDFJWX_Kl-g&s" alt="Logo" class="logo"></img>
      </div>

      <a-form-item
          name="email"
      >
        <a-input placeholder="Correo electrónico" v-model:value="form.email">
          <template #prefix>
            <user-outlined />
          </template>
        </a-input>
      </a-form-item>

      <a-form-item
          name="password"
      >
        <a-input-password placeholder="Contraseña" v-model:value="form.password">
          <template #prefix>
            <lock-outlined />
          </template>
        </a-input-password>
      </a-form-item>

      <a-form-item>
        <a-button class="button-primary" type="primary" @click.prevent="handleAuthSession" :loading="loading">Inicia sesión</a-button>
      </a-form-item>
    </a-form>

  </div>
</template>
<script setup>
import { UserOutlined, LockOutlined  } from '@ant-design/icons-vue';
import {useLoginComposable} from "@/composable/login/login.composable.js";

const {form, loading, handleAuthSession} = useLoginComposable()

</script>

<style scoped>
.login-container {
  background-image: url('https://t4.ftcdn.net/jpg/02/10/45/95/360_F_210459536_XmLDEcKq2DpeNLVmheuWeu9NM9aGKnih.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100dvh;
}

.login-form {
  max-width: 350px;
  width: 100%;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 4px;
  background-color: white;
}

.button-primary {
  width: 100%;
}

.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;

  .logo {
    width: 200px;
    height: auto;
    margin-bottom: 1rem;
  }
}

</style>
