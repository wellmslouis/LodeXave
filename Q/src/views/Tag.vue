<template>
  <div>
    <span style="font-size:30px;font-weight:bold;line-height:70px">#{{name}}</span>
    <el-divider></el-divider>
    <div v-if="length>0">
    <div v-for="(item,index) in articles" :key="index">
      <el-card class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <el-link :underline="false" style="font-size:20px;font-weight:550;" @click="gotoA(item.id)">{{item.title}}</el-link>
          <el-link v-if="item.collectionName==''" :underline="false" icon="el-icon-folder-opened" style="float: right; padding: 4px;font-size:13px">添加合集</el-link>
          <span v-else style="font-size:13px;float: right; padding: 4px;">来自合集：{{item.collectionName}}</span>
        </div>
        <div class="clearfix">
          <span style="font-size:13px">作者：{{item.author}} 发表时间：{{item.publicTime}}</span>
          <el-link :underline="false" icon="el-icon-delete" style="float: right; padding: 4px;font-size:13px" @click="delete_(item.id)">删除</el-link>
          <el-link :underline="false" icon="el-icon-notebook-2" style="float: right; padding: 4px 0;font-size:13px">导出</el-link>
          <el-link :underline="false" icon="el-icon-edit" style="float: right; padding: 4px;font-size:13px" @click="gotoE(item.id)">编辑</el-link>
        </div>
      </el-card>
    </div>
    </div>
    <div v-else>
      <el-empty description="标签内没有文章呢"></el-empty>
    </div>
  </div>
</template>

<script>
import qs from 'qs';
export default {
    data() {
        return{
          articles:[],
          length:'',
          name:''
        }
    },
    created(){
        let data={
          id: this.$route.query.index,
        }
        this.$axios({
          method:"post",
          url:"displayAllArticlesInTag",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              this.articles=res.data.articles
              this.length=res.data.length
              this.name=res.data.name
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
    },
    methods: {
      gotoA(a){
        this.$router.push("/article?index="+a);
      },
      gotoE(a){
        this.$router.push("/editArticle?index="+a);
      },
      delete_(a){
        let data={
          id: a,
        }
        this.$axios({
          method:"post",
          url:"deleteArticle",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              window.location.reload();
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
      },
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