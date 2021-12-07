<template>
  <el-container>
    <el-header>Header</el-header>
    <el-main>
        <div class="zxyA">
            <el-row>
              <div v-for="tag in tags" :key="tag">
              <el-col  :offset="0.25"  :span="2">
                <el-tag >{{tag}}</el-tag>
              </el-col>
              </div>
            </el-row>
            <div >
              <span style="font-size:30px;font-weight:bold;line-height:70px;">{{title}}</span>
              <el-link icon="el-icon-edit" style="font-size:20px;font-weight:bold;line-height:70px;" @click="gotoE"></el-link>
            </div>
            <el-divider></el-divider>
            <div style="white-space: pre-wrap;line-height:40px;">{{content}}</div>
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
    },
    methods: {
      gotoE(){
        this.$router.push("/editArticle?index="+this.$route.query.index);
      }
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