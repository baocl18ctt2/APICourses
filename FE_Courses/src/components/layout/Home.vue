<template>
  <div>
    <h1
      class="text-center text-danger"
      style="margin: 10px 0px"
    >DANH MỤC KHÓA HỌC</h1>
    <div class="row">
      <!-- Hiển thị 1 course -->
      <div
        class="col-sm-4"
        v-for="course in courses"
        :key="course.id"
      >
        <div
          class="card"
          style="width: 350px;"
        >
          <img
            style="width: auto; height: 200px;"
            :src="`${course.image}`"
            alt="Card image cap"
          >
          <div class="card-body">
            <h5 class="card-title">{{course.subject}}</h5>
            <p class="card-text">Ngày tạo: {{tranformDate(course.create_date)}}</p>
            <router-link
              v-if="get_user"
              tag="a"
              class="btn btn-primary"
              :to="{name: 'courses', params: {coursesId: course.id}}"
            >Chi tiết khóa học</router-link>
            <router-link
              v-if="!get_user"
              tag="a"
              class="btn btn-primary"
              :to="{path: '/login'}"
            >Chi tiết khóa học</router-link>
          </div>
        </div>
      </div>
      <!-- :to="{path: `/courses/${course.id}/lessons`}" -->
    </div>

  </div>

</template>

<script>
import axios from "axios";
export default {
  name: "Home",
  data() {
    return {
      courses: null,
      search_params: {
        category_id: "",
        q: "",
      },
      get_user: localStorage.getItem("YourUser"),
    };
  },
  created() {
    this.search_params.category_id = this.$route.query.category_id;
    this.search_params.q = this.$route.query.q;
    if (!this.search_params.q) {
      this.search_params.q = "";
    }
    var me = this;
    if (this.search_params.category_id) {
      // Gọi API lấy dữ liệu
      axios
        .get(
          `courses/?category_id=${this.search_params.category_id}&q=${this.search_params.q}`
        )
        .then((response) => {
          me.courses = response.data.results;
        })
        .catch((error) => console.log(error));
    }
    if (!this.search_params.category_id) {
      // Gọi API lấy dữ liệu
      axios
        .get(`courses/?q=${this.search_params.q}`)
        .then((response) => {
          me.courses = response.data.results;
        })
        .catch((error) => console.log(error));
    }
  },

  methods: {
    tranformDate(date) {
      date = date.substring(0, 10);
      return date;
    },
  },
};
</script>

<style scoped>
.col-sm-4 {
  margin-bottom: 20px;
}
.card-title {
  display: flex;
  margin-bottom: 0.5rem;
  height: 50px;
  align-items: center;
}
</style>