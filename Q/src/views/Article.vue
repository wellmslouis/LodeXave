<template>
  <el-container>
    <el-header>Header</el-header>
    <el-main>
        <div class="zxyA">
            <el-tag v-for="tag in tags" :key="tag">{{tag}}</el-tag>
            <h1>{{title}}</h1>
            <el-divider></el-divider>
            <div style="white-space: pre-wrap;">{{content}}</div>
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
            tags:[]
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
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
    }
}
</script>

<style>
.zxyA {
  margin-top: 30px;
  width: 800px;
  position: absolute;
  left: calc(50% - 400px);
  text-align: left;
}
</style>