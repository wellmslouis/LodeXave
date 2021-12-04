<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="LOFTER" name="first">
        <div style="line-height:50px">
          <div>目前除网址外，发表年份也需要手动输入。</div>
          <el-input v-model="inputLink" placeholder="请输入文章链接" style="width:500px"></el-input>
          <el-button plain @click="dialogFormVisible = true">自动导入</el-button>
          <el-dialog title="补充信息" :visible.sync="dialogFormVisible" width=30%>
            <el-input v-model="inputYear" autocomplete="off" placeholder="请输入发表年份（四位数字）"></el-input>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
            </div>
          </el-dialog>
        </div>
      </el-tab-pane>
      <el-tab-pane label="其它" name="second">待完善！</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        activeName: 'first',
        inputLink:'',
        dialogFormVisible: false,
        inputYear:'',
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      }
    }
  };
</script>

<style>
</style>