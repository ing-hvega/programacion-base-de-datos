import {useCounterStore} from '@/stores/counter.store.js'
import {storeToRefs} from 'pinia'


export function useCounterComposable() {
    const counterStore = useCounterStore()

    const {count} = storeToRefs(counterStore)


    const handleIncrement = () => {
        count.value++
    }

    const handleDecrement = () => {
        count.value--
    }

    return {
        count,
        handleIncrement,
        handleDecrement,
    }
} //