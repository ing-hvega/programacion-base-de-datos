<template>
  <a-layout>
    <a-layout-header class="header">
      <div class="logo"/>
    </a-layout-header>
    <a-layout>
      <a-layout-sider width="200" style="background: #fff">
        <a-menu
            mode="inline"
            :style="{ height: '100%', borderRight: 0 }"

        >
          <a-sub-menu key="sub1">
            <template #title>
                <span>
                  Panel de control
                </span>
            </template>
            <a-menu-item key="1">
              <RouterLink :to="{name: 'users'}">Usuarios</RouterLink>
            </a-menu-item>
          </a-sub-menu>
        </a-menu>
      </a-layout-sider>
      <a-layout style="padding: 24px 24px 24px 24px">
        <a-layout-content :style="{ background: '#fff', padding: '24px', margin: 0, height: '82vh' }">
          <RouterView/>
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-layout>
</template>

<script>

</script>
