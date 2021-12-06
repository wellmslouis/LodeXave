<template>
  <div>
    <span style="font-size:30px;font-weight:bold;line-height:70px">藏书几何</span>
    <el-divider></el-divider>
    <div v-if="length>0">
        <el-row>
    <div v-for="(item,index) in tags" :key="index">
            <el-col :offset="1" :span="5">
                <el-card class="box-card" shadow="hover">
                    <div slot="header" class="clearfix">
                    <el-link :underline="false" style="font-size:20px;font-weight:550;" @click="gotoT(item.id)">#{{item.name}}({{item.number}})</el-link>
                    <el-link v-if="item.collectionName==''" :underline="false" icon="el-icon-folder-opened" style="float: right; padding: 4px;font-size:13px">添加合集</el-link>
                    </div>
                    <div class="clearfix">
                        <el-link :underline="false" icon="el-icon-notebook-2" style="padding: 4px 0;font-size:13px">导出全部</el-link>
                        <el-link :underline="false" icon="el-icon-delete" style="padding: 4px;font-size:13px;float: right;" @click="delete_(item.id)">删除标签</el-link>
                    </div>
                </el-card>
            </el-col>
    </div>
    </el-row>
    </div>
    <div v-else>
      <el-empty v-if="emptyoption==1" description="还没有标签呢"></el-empty>
      <el-empty v-else description="没有检索到标签欸"></el-empty>
    </div>
  </div>
</template>

<script>
import qs from 'qs';
export default {
    data() {
        return{
          tags:[],
          inputSearch:'',
          length:'',
          emptyoption:1,//1正常，2检索关键字
        }
    },
    created(){
        this.$axios({
          method:"post",
          url:"displayAllTags",
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              this.tags=res.data.tags
              this.length=res.data.length
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
    },
    methods: {
      gotoT(a){
        this.$router.push("/tag?index="+a);
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
          url:"deleteTag",
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