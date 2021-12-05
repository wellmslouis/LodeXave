<template>
  <el-container>
    <el-header>Header</el-header>
    <el-main>
        <div class="zxyB">
            <el-input v-model="title" placeholder="请输入标题" ></el-input>
            <el-input v-model="author" placeholder="请输入作者" ></el-input>
            <el-input v-model="strT" placeholder="请输入标签（以英文分号隔开）" ></el-input>
            <el-input
              type="textarea"
              :rows="20"
              placeholder="请输入内容"
              v-model="content">
            </el-input>
            <el-button plain @click="edit">修改</el-button>
        </div>
    </el-main>
    </el-container>
</template>

<script>
import qs from 'qs';
export default {
    data() {
        return{
            title:'',
            content:'',
            tags:[],
            author:'',
            strT:'',
        }
    },
    created(){
        let data={
          id: this.$route.query.index,
        }
        this.$axios({
          method:"post",
          url:"displayArticle",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
                this.title=res.data.title
                this.content=res.data.content
                this.tags=res.data.tag
                this.author=res.data.author
                this.strT=res.data.strT
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
    },
     methods: {
      edit(){
        let data={
          id: this.$route.query.index,
          title:this.title,
          content:this.content,
          author:this.author,
          strT:this.strT
        }
        this.$axios({
          method:"post",
          url:"editArticle",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
          if (res.data.code === 200) {
            this.$router.push("/article?index="+this.$route.query.index);
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
.zxyB {
  margin-top: 30px;
  width: 800px;
  position: absolute;
  left: calc(50% - 400px);
  text-align: left;
  line-height: 70px;
}
</style>