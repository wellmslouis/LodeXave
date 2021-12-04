<template>
  <el-container>
    <el-header>Header</el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            router
            :default-active="$router.path"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-circle-plus-outline"></i>
                <span>导入文章</span>
              </template>
                <el-menu-item index="/autoImport" @click="notFirst">自动导入</el-menu-item>
                <el-menu-item index="/manualImport"  @click="notFirst">手动导入</el-menu-item>
            </el-submenu>
            <el-menu-item index="/shelf">
              <i class="el-icon-reading"></i>
              <span slot="title"  @click="notFirst">我的书柜</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <div v-if="isFirst">首页</div>
          <div v-else>
            <router-view></router-view>
          </div>
        </el-main>
      </el-container>
  </el-container>

</template>

<script>
export default {
  data () {
    return {
      isFirst:true
     }
  },
  methods: {
    handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
    handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
    notFirst(){
      this.isFirst=false
    }
    
  }
}
</script>

<style>
 .el-header {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
</style>