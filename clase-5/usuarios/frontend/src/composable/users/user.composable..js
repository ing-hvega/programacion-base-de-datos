import { storeToRefs } from "pinia";
import { onMounted, watch } from "vue";
import { message } from "ant-design-vue";
import debounce from "lodash.debounce";

import { useUsersStore } from "@/stores/user.store..js";
import { useUserService } from "@/services/user.service.js";

export function useUserComposable(options = { loadDataOnMount: true }) {
    const userStore = useUsersStore();
    const { form, pagination, search, openForm, loading, dataSource } = storeToRefs(userStore);
    const { resetForm } = userStore;

    const {createUser, listUsers} = useUserService

    const keyMessage = "key_message";

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
        },
        {
            title: 'Opciones',
            dataIndex: 'options',
            key: 'options',
            width: "8%",
            align: "center",
        }
    ];

    const mountedListUsers = async () => {
        const response = await listUsers();
        dataSource.value = response.data;
        pagination.value = response.pagination;
    };

    const handleChangeTable = async (pagination, searchTerm = undefined) => {
        const { current, pageSize } = pagination;
        const response = await listUsers(current, pageSize, searchTerm);
        dataSource.value = response.data;
        pagination.value = response.pagination;
    };

    const handleOpen = () => {
        openForm.value = true;
    };

    const handleCancel = () => {
        openForm.value = false;
    };

    const handleSaveForm = async () => {
        loading.value = true;

        try {
            const response = await createUser({ ...form.value });

            if (response.status) {
                message.success({
                    content: "Usuario creado exitosamente",
                    key: keyMessage
                });
                await mountedListUsers();
                await new Promise(resolve => setTimeout(resolve, 1000));
                openForm.value = false;
                resetForm();
            } else {
                message.error({
                    content: "Error al crear usuario: " + (response.message || "Sin detalles"),
                    key: keyMessage
                });
            }
        } catch (e) {
            console.error("Error al crear usuario:", e);
            message.error({
                content: `El usuario no pudo ser creado: ${e.message || 'Error desconocido'}`,
                key: keyMessage
            });
        } finally {
            loading.value = false;
        }
    };

    const debouncedSearch = debounce(async (searchTerm) => {
        await handleChangeTable({ ...pagination.value }, searchTerm);
    }, 500);

    if (options.loadDataOnMount) {
        onMounted(async () => {
            await mountedListUsers();
        });
    }

    watch(search, (newSearch, oldSearch) => {
        if (newSearch !== oldSearch && options.loadDataOnMount) {
            debouncedSearch(newSearch);
        }
    });

    return {
        form,
        pagination,
        search,
        openForm,
        loading,
        dataSource,

        columns,

        handleOpen,
        handleCancel,
        handleSaveForm,
        handleChangeTable,
    };
}