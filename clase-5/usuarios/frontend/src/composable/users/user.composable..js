import {useUsersStore} from "@/stores/user.store..js";
import {storeToRefs} from "pinia";
import {useUserService} from "@/services/user.service.js"
import {message} from "ant-design-vue";
import {onMounted} from "vue";

export function useUserComposable() {
    const userStore = useUsersStore();
    const {form, openForm, loading, dataSource} = storeToRefs(userStore);
    const {resetForm} = userStore;

    const {createUser} = useUserService

    const columns = [
        {
            title: 'Nombre',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Correo',
            dataIndex: 'email',
            key: 'email',
        },
        {
            title: 'Tipo',
            dataIndex: 'type',
            key: 'type',
        },
        {
            title: 'Descripción',
            dataIndex: 'description',
            key: 'description',
        }
    ];

    const handleOpen = () => {
        openForm.value = true;
    };

    const handleCancel = () => {
        openForm.value = false;
    };

    const handleSaveForm = async () => {
        loading.value = true;
        const keyMessage = "key_message"

        try {
            const response = await createUser({...form.value})

            if (response.status) {
                message.success({
                    content: "Usuario creado exitosamente",
                    key: keyMessage
                })
                await mountedListUsers()
                await new Promise(resolve => setTimeout(resolve, 1000))
                openForm.value = false;
                resetForm();
            } else {
                message.error({
                    content: "Error al crear usuario: " + (response.message || "Sin detalles"),
                    key: keyMessage
                })
            }

        } catch (e) {
            console.error("Error al crear usuario:", e);
            message.error({
                content: `El usuario no pudo ser creado: ${e.message || 'Error desconocido'}`,
                key: keyMessage
            })
        } finally {
            loading.value = false;
        }
    }

    const mountedListUsers = async () => {
        const response = await useUserService.listUsers()
        dataSource.value = response.data
    }

    onMounted(async () => {
        await mountedListUsers()
    })

    return {
        form,
        openForm,
        loading,
        columns,
        dataSource,
        handleOpen,
        handleCancel,
        handleSaveForm,
    }
}