<template>
  <el-container>
    <el-header>Header</el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            router
            :default-active="$route.path"
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
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-reading"></i>
                <span>我的书柜</span>
              </template>
                <el-menu-item index="/shelf" @click="notFirst">文章</el-menu-item>
                <el-menu-item index="/manualImport"  @click="notFirst">合集</el-menu-item>
                <el-menu-item index="/manualImport"  @click="notFirst">标签</el-menu-item>
            </el-submenu>
            <el-menu-item index="/personalCenter">
              <i class="el-icon-user"></i>
              <span slot="title"  @click="notFirst">个人中心</span>
            </el-menu-item>
            <el-menu-item index="/help">
              <i class="el-icon-warning-outline"></i>
              <span slot="title"  @click="notFirst">帮助</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
            <router-view></router-view>
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