<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a
        class="navbar-brand"
        href="#"
      >eCourseApp</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div
        class="collapse navbar-collapse d-flex justify-content-between"
        id="navbarSupportedContent"
      >
        <ul class="navbar-nav mr-auto">
          <router-link
            tag="a"
            class="nav-link"
            to="/"
          >Trang chu</router-link>
          <router-link
            tag="a"
            class="nav-link"
            to="/user"
          >User</router-link>
          <li
            class="nav-item"
            v-for="category in categories"
            :key="category.id"
          >
            <router-link
              tag="a"
              class="nav-link"
              :to="{name: 'home', params: {category_id: $route.params.id},  query: {category_id: category.id}}"
            >{{ category.name}}</router-link>
          </li>
          <button @click="testData()">Test</button>
        </ul>

        <form class="d-flex form-inline my-2 my-lg-0">
          <input
            class="form-control mr-sm-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
            v-model="search_courses"
          >
          <button
            type="button"
            class="btn btn-outline-success"
            @click.prevent="searchCourses()"
          >Success</button>
        </form>
        <!-- Phần grid name -->
        <div v-if="get_user">
          <div class="m-grid-name">
            <!-- Phần hiển thị avatar -->
            <div
              v-if="!get_user.avatar"
              class="m-avatar"
            > </div>
            <img
              v-if="get_user.avatar"
              :src="`http://127.0.0.1:8000/static${this.get_user.avatar}`"
              style="width: 40px; height: 40px"
              class="rounded-circle"
              alt="Cinque Terre"
            />
            <!-- Phần hiển thị tên -->
            <div class="m-text-name">{{ displayName()}}</div>
            <!-- Phần dropdown -->
            <div
              class="btndropdown"
              @click="isFeatureProfile = ! isFeatureProfile"
            >
              <i class="fas fa-caret-down"></i>
            </div>
            <div
              v-if="isFeatureProfile"
              class="m-grid-feature-profile"
            >
              <div
                @click="UpdateProfile()"
                class="m-feature"
              >Chỉnh sửa thông tin</div>
              <div
                @click="clickOnLogout()"
                class="m-feature"
              >Thoát</div>
            </div>
          </div>
        </div>
        <div v-if="!get_user">
          <router-link
            to="/login"
            class="btn btn-secondary m-text-login"
          >Đăng nhập</router-link>
        </div>
      </div>
    </nav>
    <UpdateProfile
      v-show="isUpdateProfile"
      :user_info="get_user"
    />
  </div>
</template>

<script>
import axios from "axios";
import UpdateProfile from "../../view/UpdateProfile.vue";
export default {
  components: {
    UpdateProfile,
  },
  data() {
    return {
      categories: [],
      category_id: "",
      search_courses: "",
      get_user: {},
      isFeatureProfile: false,
      isUpdateProfile: false,
    };
  },
  mounted() {
    this.get_user = JSON.parse(localStorage.getItem("YourUser"));
  },
  created() {
    var me = this;
    axios
      .get("categories/")
      .then((response) => {
        me.categories = response.data;
      })
      .catch((error) => console.log(error));
  },
  methods: {
    searchCourses() {
      this.category_id = this.$route.query.category_id;
      if (this.category_id) {
        this.$router.push({
          name: "home",
          query: { category_id: this.category_id, q: this.search_courses },
        });
      } else {
        this.$router.push({ name: "home", query: { q: this.search_courses } });
      }
    },
    testData() {},
    displayName() {
      if (this.get_user.first_name != "" || this.get_user.last_name != "")
        return `${this.get_user.first_name} ${this.get_user.last_name}`;
      else {
        return "Ẩn danh";
      }
    },
    clickOnLogout() {
      let keysToRemove = ["YourUser", "access_token"];
      keysToRemove.forEach((element) => {
        localStorage.removeItem(element);
      });
      this.get_user = null;
    },
    setURLProfile() {
      if (!this.get_user.avatar || this.get_user.avatar == "") {
        // return url("../../assets/images/avatar_empty.jpg");
      } else {
        return `http://127.0.0.1:8000/static${this.get_user.avatar}`;
      }
    },
    UpdateProfile() {
      this.isFeatureProfile = false;
      this.isUpdateProfile = true;
    },
  },
};
</script>

<style scoped>
button.m-btn {
  width: 50px;
}
.router-link-exact-active {
  background-color: rgb(93, 219, 156);
}
.m-grid-name {
  margin-right: 20px;
  display: flex;
  height: 60px;
  line-height: 60px;
  align-items: center;
  position: relative;
}
.m-grid-name .m-text-name {
  font-size: 15px;
  font-weight: 500;
  margin: 0px 10px;
}
.m-grid-feature-profile {
  width: 200px;
  height: 80px;
  background-color: rgb(240, 238, 238);
  position: absolute;
  right: -10px;
  top: 60px;
  z-index: 9999;
  display: block;
}
.m-feature {
  display: flex;
  height: 40px;
  align-items: center;
  font-size: 16px;
  cursor: pointer;
}

.m-feature:hover {
  background-color: rgb(196, 184, 184);
}

.btndropdown {
  cursor: pointer;
}

.m-text-login {
  margin-right: 10px;
}
.m-avatar {
  width: 40px;
  height: 40px;
  min-width: 32px;
  min-height: 32px;
  border-radius: 50%;
  background-image: url(../../assets/images/avatar_empty.jpg);
  background-repeat: no-repeat;
  background-size: contain;
}
</style>