<template>
  <div>
    <span style="font-size:30px;font-weight:bold;line-height:70px">藏书几何</span>
    <el-input placeholder="检索关键词" v-model="input3" style="width:200px;float: right;padding: 15px; "><el-button slot="append" icon="el-icon-search" circle></el-button></el-input>
    <el-divider></el-divider>
    <div v-for="(item,index) in articles" :key="index">
      <el-card class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <el-link :underline="false" style="font-size:20px;font-weight:550;" @click="gotoA(item.id)">{{item.title}}</el-link>
        </div>
        <div class="clearfix">
          <span style="font-size:13px">作者：{{item.author}} 发表时间：{{item.publicTime}}</span>
          <el-link :underline="false" icon="el-icon-delete" style="float: right; padding: 4px;font-size:13px">删除</el-link>
          <el-link :underline="false" icon="el-icon-notebook-2" style="float: right; padding: 4px 0;font-size:13px">导出</el-link>
          <el-link :underline="false" icon="el-icon-edit" style="float: right; padding: 4px;font-size:13px">编辑</el-link>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
    data() {
        return{
          articles:[]
        }
    },
    created(){
        this.$axios({
          method:"post",
          url:"displayAllArticles",
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              this.articles=res.data.articles
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
    },
    methods: {
      gotoA(a){
        this.$router.push("/article?index="+a);
      }
    }
}
</script>

<style>
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }
</style>