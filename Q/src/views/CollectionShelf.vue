<template>
  <div>
    <span style="font-size:30px;font-weight:bold;line-height:70px">藏卷几何</span>
    <el-link :underline="false" icon="el-icon-circle-plus-outline" style="font-size:30px;font-weight:bold;line-height:70px" @click="add"></el-link>
    <el-divider></el-divider>
    <div v-if="length>0">
    <div v-for="(item,index) in collections" :key="index">
      <el-card class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <el-link :underline="false" style="font-size:20px;font-weight:550;" @click="gotoC(item.id)">{{item.name}}</el-link>
        </div>
        <div class="clearfix">
          <span style="font-size:13px">共{{item.num}}篇文章</span>
          <el-link :underline="false" icon="el-icon-delete" style="float: right; padding: 4px;font-size:13px" @click="delete_(item.id)">删除</el-link>
          <el-link :underline="false" icon="el-icon-notebook-2" style="float: right; padding: 4px 0;font-size:13px">导出</el-link>
          <el-link :underline="false" icon="el-icon-edit" style="float: right; padding: 4px;font-size:13px" @click="dialogFormVisible = true;dialogFormID=item.id">重命名</el-link>
            <el-dialog :visible.sync="dialogFormVisible" width=30%>
            <el-input v-model="inputName" autocomplete="off" placeholder="重命名合集"></el-input>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="modifyName()">确 定</el-button>
            </div>
          </el-dialog>
        </div>
      </el-card>
    </div>
    </div>
    <div v-else>
      <el-empty description="还没有合集呢"></el-empty>
    </div>
  </div>
</template>

<script>
import qs from 'qs';
export default {
    data() {
        return{
          collections:[],
          inputSearch:'',
          length:'',
          emptyoption:1,//1正常，2检索关键字
          dialogFormVisible: false,
          dialogFormID:'',
          inputName:'',
        }
    },
    created(){
        this.$axios({
          method:"post",
          url:"displayAllCollections",
        }).then((res) => {
          console.log("res=>", res);
            if (res.data.code === 200) {
              this.collections=res.data.collections
              this.length=res.data.length
            }
        }
        ).catch((err) => {
          console.log("err=>", err);
        })
    },
    methods: {
      add(){
        this.$axios({
          method:"post",
          url:"createCollection",
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
      modifyName(){
        let data={
          id: this.dialogFormID,
          name:this.inputName
        }
        console.log(data);
        this.$axios({
          method:"post",
          url:"modifyCollectionName",
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
      gotoC(a){
        this.$router.push("/collection?index="+a);
      },
      delete_(a){
        let data={
          id: a,
        }
        this.$axios({
          method:"post",
          url:"deleteCollection",
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