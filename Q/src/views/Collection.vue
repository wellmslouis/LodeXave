<template>
<div>
    <span style="font-size:30px;font-weight:bold;line-height:70px">【{{name}}】</span>
    <el-divider></el-divider>
    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="OID"
        label="序号"
        width="180">
      </el-table-column>
      <el-table-column
        prop="title"
        label="标题">
      </el-table-column>
      <el-table-column
        label="操作"
        width="250">
        <template slot-scope="scope">
        <el-link :underline="false" icon="el-icon-view" style="padding: 4px 0;font-size:13px" @click="gotoA(scope.row.AID)">查看</el-link>
        <el-link :underline="false" icon="el-icon-top" style="padding: 4px 0;font-size:13px" @click="up(scope.row.OID)">上移</el-link>
        <el-link :underline="false" icon="el-icon-bottom" style="padding: 4px 0;font-size:13px" @click="down(scope.row.OID)">下移</el-link>
        <el-link :underline="false" icon="el-icon-document-delete" style="padding: 4px 0;font-size:13px" @click="delete_(scope.row.AID)">移出</el-link>
        </template>
      </el-table-column>
    </el-table>
    </div>
  </template>

  <script>
    import qs from 'qs';
    export default {
      data() {
        return {
          name:'',
          tableData: [],
        }
      },
      created(){
        let data={
          id: this.$route.query.index,
        }
        this.$axios({
          method:"post",
          url:"displayAllArticlesInCollection",
          data:qs.stringify(data)
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              this.name=res.data.name
              this.tableData=res.data.articles
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
      delete_(a){
        let data={
          id: a,
        }
        this.$axios({
          method:"post",
          url:"deleteArticleFromCollection",
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
      up(a){
        let data={
          oid: a,
          cid:this.$route.query.index,
        }
        this.$axios({
          method:"post",
          url:"moveUpInCollection",
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
      down(a){
        let data={
          oid: a,
          cid:this.$route.query.index,
        }
        this.$axios({
          method:"post",
          url:"moveDownInCollection",
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