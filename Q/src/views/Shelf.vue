<template>
  <div>
    <span style="font-size:30px;font-weight:bold;line-height:70px">藏书几何</span>
    <el-input placeholder="检索标题关键词" v-model="inputSearch" style="width:200px;float: right;padding: 15px; "><el-button slot="append" icon="el-icon-search" circle @click="search"></el-button></el-input>
    <el-divider></el-divider>
    <div v-if="length>0">
    <div v-for="(item,index) in articles" :key="index">
      <el-card class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <el-link :underline="false" style="font-size:20px;font-weight:550;" @click="gotoA(item.id)">{{item.title}}</el-link>
          <el-link  v-if="item.collectionName==''" :underline="false" icon="el-icon-folder-opened" style="float: right; padding: 4px;font-size:13px" @click="A(item.id)">添加至合集</el-link>
          <span v-else style="font-size:13px;float: right; padding: 4px;">来自合集：{{item.collectionName}}</span>
          <el-dialog :visible.sync="dialogFormVisible" width=30%>
            <el-select v-model="value" filterable placeholder="请选择合集">
              <el-option
                v-for="item in options"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="addToCollection()">确 定</el-button>
            </div>
          </el-dialog>
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
      <el-empty v-if="emptyoption==1" description="还没有导入文章呢"></el-empty>
      <el-empty v-else description="没有检索到关键字欸"></el-empty>
    </div>
  </div>
</template>

<script>
import qs from 'qs';
export default {
    data() {
        return{
          articles:[],
          inputSearch:'',
          length:'',
          emptyoption:1,
          dialogFormVisible: false,
          dialogFormID:'',
          options:[],
          value: ''
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
              this.length=res.data.length
              this.options=res.data.collections
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
      A(a){
        this.dialogFormVisible = true;
        this.dialogFormID=a;
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
      addToCollection(){
        let data={
          aid: this.dialogFormID,
          cid:this.value
        }
        this.$axios({
          method:"post",
          url:"addArticleToCollection",
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
      search(){
        let data={
          search:this.inputSearch
        }
        this.$axios({
          method:"post",
          url:"searchArticle",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              this.articles=res.data.articles
              this.length=res.data.length
              this.emptyoption=2
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