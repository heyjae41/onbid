<template>
  <div class="black-bg" v-if="prdRegModalOpenStatus == true">
    <div class="white-bg">
      <h4>상품알람</h4>
      <p>
        <span>{{ iherbPrdName }} &nbsp;</span>
      </p>
      <ebutton class="w-100 btn btn-primary btn-lg" @click="prdReg()"> 알림등록 </ebutton>
      <ebutton
        class="w-100 btn btn-primary btn-lg"
        @click="prdRegModalOpenStatus = false"
      >
        닫기
      </ebutton>
    </div>
  </div>
  <div class="home">
    <div class="col-12">
      <label for="prd_url" class="form-label">URL</label
      ><input type="text" class="form-control" id="prd_url" />
      <ebutton class="w-100 btn btn-primary btn-lg" @click="prdDetail()">
        상품알림받기
      </ebutton>
    </div>
  </div>
  <div class="home">
    <div class="album py-5 bg-light">
      <div class="container">
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
          <div class="col" v-for="(item, idx) in state.items" :key="idx">
            <CardComp :item="item" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { reactive } from "vue";
import CardComp from "@/components/CardComp.vue";

export default {
  name: "HomePage",
  components: { CardComp },
  setup() {
    const state = reactive({
      items: [],
      iherbPrdId: "",
      iherbPrdName: "",
      iherbPrdUrl: "",
      iherbPrdPrice: "",
    });

    axios.get("/api/items").then(({ data }) => {
      state.items = data;
    });

    const prdReg = () => {
      axios.post("/api/prd").then(({ data }) => {
        state.iherbPrdId = data.prd_id;
        state.iherbPrdName = data.name;
        state.iherbPrdUrl = data.prd_url;
        state.iherbPrdPrice = data.price;
      });
    };

    const prdDetail = () => {
      this.prdRegModalOpenStatus = true;

      axios.get("/api/prd").then(({ data }) => {
        state.iherbPrdId = data.prd_id;
        state.iherbPrdName = data.name;
        state.iherbPrdUrl = data.prd_url;
        state.iherbPrdPrice = data.price;
      });
    };

    return {
      state,
      prdReg,
      prdDetail,
    };
  },
  data() {
    return {
      prdRegModalOpenStatus: false,
    };
  },
};
</script>

<style scoped>
body {
  margin: 0;
}

.black-bg {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 5);
  position: fixed;
  padding: 20px;
}

.white-bg {
  width: 100%;
  background: white;
  border-radius: 8px;
  padding: 20px;
}
</style>
