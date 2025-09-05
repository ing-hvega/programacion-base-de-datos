<template>
  <form @submit.prevent="onSubmit" class="form">
    <div class="form-field">
      <label for="name" class="form-label">
        Nombre *
      </label>
      <input
        id="name"
        v-model="values.name"
        @blur="handleBlur('name')"
        @input="handleChange('name', $event.target.value)"
        type="text"
        class="form-input"
        :class="{ 'form-input--error': errors.name && touched.name }"
        placeholder="Ingresa tu nombre"
      >
      <span v-if="errors.name && touched.name" class="form-error">
        {{ errors.name }}
      </span>
    </div>

    <div class="form-field">
      <label for="email" class="form-label">
        Email *
      </label>
      <input
        id="email"
        v-model="values.email"
        @blur="handleBlur('email')"
        @input="handleChange('email', $event.target.value)"
        type="email"
        class="form-input"
        :class="{ 'form-input--error': errors.email && touched.email }"
        placeholder="ejemplo@correo.com"
      >
      <span v-if="errors.email && touched.email" class="form-error">
        {{ errors.email }}
      </span>
    </div>

    <div class="form-field">
      <label for="phone" class="form-label">
        Teléfono
      </label>
      <input
        id="phone"
        v-model="values.phone"
        @blur="handleBlur('phone')"
        @input="handleChange('phone', $event.target.value)"
        type="tel"
        class="form-input"
        :class="{ 'form-input--error': errors.phone && touched.phone }"
        placeholder="+1234567890"
      >
      <span v-if="errors.phone && touched.phone" class="form-error">
        {{ errors.phone }}
      </span>
    </div>

    <div class="form-field">
      <label for="message" class="form-label">
        Mensaje *
      </label>
      <textarea
        id="message"
        v-model="values.message"
        @blur="handleBlur('message')"
        @input="handleChange('message', $event.target.value)"
        class="form-textarea"
        :class="{ 'form-textarea--error': errors.message && touched.message }"
        placeholder="Escribe tu mensaje aquí..."
        rows="4"
      ></textarea>
      <span v-if="errors.message && touched.message" class="form-error">
        {{ errors.message }}
      </span>
    </div>

    <div class="form-actions">
      <button
        type="button"
        @click="resetForm"
        class="btn btn--secondary"
        :disabled="isSubmitting"
      >
        Limpiar
      </button>
      <button
        type="submit"
        class="btn btn--primary"
        :disabled="!isValid || isSubmitting"
      >
        {{ isSubmitting ? 'Enviando...' : 'Enviar' }}
      </button>
    </div>

    <div v-if="submitStatus" class="form-status" :class="`form-status--${submitStatus.type}`">
      {{ submitStatus.message }}
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useForm } from '@/composables/advanced'
import { useNotificationStore } from '@/stores/notifications'
import { validators } from '@/utils/helpers'

const notificationStore = useNotificationStore()
const submitStatus = ref(null)

// Configuración de validación
const validationRules = {
  name: [
    { validator: validators.required, message: 'El nombre es requerido' },
    { validator: (value) => validators.minLength(value, 2), message: 'El nombre debe tener al menos 2 caracteres' }
  ],
  email: [
    { validator: validators.required, message: 'El email es requerido' },
    { validator: validators.email, message: 'Debe ser un email válido' }
  ],
  phone: [
    { validator: (value) => !value || validators.phone(value), message: 'Debe ser un teléfono válido' }
  ],
  message: [
    { validator: validators.required, message: 'El mensaje es requerido' },
    { validator: (value) => validators.minLength(value, 10), message: 'El mensaje debe tener al menos 10 caracteres' }
  ]
}

const initialValues = {
  name: '',
  email: '',
  phone: '',
  message: ''
}

const {
  values,
  errors,
  touched,
  isSubmitting,
  isValid,
  handleChange,
  handleBlur,
  resetForm,
  handleSubmit
} = useForm(initialValues, validationRules)

// Simular envío de formulario
const submitForm = async (formData) => {
  // Simular delay de API
  await new Promise(resolve => setTimeout(resolve, 2000))

  // Simular éxito/error aleatoriamente
  if (Math.random() > 0.3) {
    notificationStore.success('Formulario enviado exitosamente!')
    submitStatus.value = { type: 'success', message: 'Formulario enviado correctamente' }
    resetForm()
    setTimeout(() => { submitStatus.value = null }, 3000)
  } else {
    throw new Error('Error al enviar el formulario')
  }
}

const onSubmit = async () => {
  try {
    await handleSubmit(submitForm)
  } catch (error) {
    notificationStore.error('Error al enviar el formulario')
    submitStatus.value = { type: 'error', message: 'Error al enviar el formulario' }
    setTimeout(() => { submitStatus.value = null }, 3000)
  }
}
</script>

<style scoped>
.form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: white;
}

.form-field {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #2c3e50;
  font-size: 14px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s ease;
  background-color: white;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-input--error,
.form-textarea--error {
  border-color: #e74c3c;
}

.form-input--error:focus,
.form-textarea--error:focus {
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-error {
  display: block;
  margin-top: 4px;
  color: #e74c3c;
  font-size: 12px;
}

.form-actions {
  display: flex;
