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
              <el-button type="primary" @click="autoImport">确 定</el-button>
            </div>
          </el-dialog>
        </div>
      </el-tab-pane>
      <el-tab-pane label="其它" name="second">待完善！</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import qs from 'qs';
  export default {
    data() {
      return {
        activeName: 'first',
        inputLink:'',
        dialogFormVisible: false,
        inputYear:'',
        getID:'',
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      autoImport(){
        let data={
          link: this.inputLink,
          year: this.inputYear
        }
        this.$axios({
          method:"post",
          url:"spiderArticle",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
          if (res.data.code === 200) {
            this.getID=res.data.id;
            this.$router.push("/article?index="+this.getID);
          }
          }
        ).catch((err) => {
          console.log("err=>", err);
        })
      }
    }
  };
</script>

<style>
</style>