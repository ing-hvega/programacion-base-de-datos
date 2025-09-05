import { ref, reactive, computed, watch } from 'vue'
import { validators } from '@/utils/helpers'

export function useForm(initialValues = {}, validationRules = {}) {
  const values = reactive({ ...initialValues })
  const errors = ref({})
  const touched = ref({})
  const isSubmitting = ref(false)

  // Función para validar un campo específico
  const validateField = (fieldName, value) => {
    const rules = validationRules[fieldName]
    if (!rules) return null

    for (const rule of rules) {
      if (typeof rule === 'function') {
        const result = rule(value)
        if (result !== true) {
          return result
        }
      } else if (typeof rule === 'object') {
        const { validator, message } = rule
        if (!validator(value)) {
          return message
        }
      }
    }
    return null
  }

  // Función para validar todos los campos
  const validateForm = () => {
    const newErrors = {}
    let isValid = true

    Object.keys(validationRules).forEach(fieldName => {
      const error = validateField(fieldName, values[fieldName])
      if (error) {
        newErrors[fieldName] = error
        isValid = false
      }
    })

    errors.value = newErrors
    return isValid
  }

  // Función para manejar cambios en los campos
  const handleChange = (fieldName, value) => {
    values[fieldName] = value
    touched.value[fieldName] = true

    // Validar el campo después del cambio
    const error = validateField(fieldName, value)
    if (error) {
      errors.value[fieldName] = error
    } else {
      delete errors.value[fieldName]
    }
  }

  // Función para manejar blur de campos
  const handleBlur = (fieldName) => {
    touched.value[fieldName] = true
  }

  // Función para resetear el formulario
  const resetForm = () => {
    Object.keys(values).forEach(key => {
      values[key] = initialValues[key] || ''
    })
    errors.value = {}
    touched.value = {}
    isSubmitting.value = false
  }

  // Computed properties
  const isValid = computed(() => Object.keys(errors.value).length === 0)
  const isDirty = computed(() => Object.keys(touched.value).length > 0)

  // Función para manejar submit
  const handleSubmit = async (submitFn) => {
    if (!validateForm()) {
      return false
    }

    isSubmitting.value = true
    try {
      await submitFn(values)
      return true
    } catch (error) {
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    isDirty,
    handleChange,
    handleBlur,
    validateForm,
    resetForm,
    handleSubmit
  }
}

// Composable para manejo de estado de carga
export function useAsync(asyncFn) {
  const loading = ref(false)
  const error = ref(null)
  const data = ref(null)

  const execute = async (...args) => {
    loading.value = true
    error.value = null

    try {
      const result = await asyncFn(...args)
      data.value = result
      return result
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    loading.value = false
    error.value = null
    data.value = null
  }

  return {
    loading,
    error,
    data,
    execute,
    reset
  }
}

// Composable para paginación
export function usePagination(items, itemsPerPage = 10) {
  const currentPage = ref(1)
  const perPage = ref(itemsPerPage)

  const totalItems = computed(() => items.value?.length || 0)
  const totalPages = computed(() => Math.ceil(totalItems.value / perPage.value))

  const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * perPage.value
    const end = start + perPage.value
    return items.value?.slice(start, end) || []
  })

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  const nextPage = () => {
    goToPage(currentPage.value + 1)
  }

  const prevPage = () => {
    goToPage(currentPage.value - 1)
  }

  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  return {
    currentPage,
    perPage,
    totalItems,
    totalPages,
    paginatedItems,
    hasNextPage,
    hasPrevPage,
    goToPage,
    nextPage,
    prevPage
  }
}
