import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counterStore', () => {
  const count = ref(20)


  return { count}
})
