<template>
  <div>
    <div class="m-container">
      <form>
        <!-- Phần thông báo đăng nhập sai -->
        <div
          v-if="isError"
          class="m-row info-error"
        >
          Đăng nhập sai, xin vui lòng thử lại
        </div>
        <!-- Phần email -->
        <div class="m-row">
          <label form="Email">
            <span>Tài khoản</span>
            <input
              class="m-input"
              type="text"
              placeholder="example@gmail.com"
              v-model="login.username"
            />
          </label>

        </div>
        <!-- Phần password -->
        <div class="m-row">
          <label form="Password">
            <span>Mật khẩu</span>
            <input
              class="m-input"
              type="password"
              placeholder="password"
              v-model="login.password"
            />
          </label>
        </div>

        <!-- Phần submit -->
        <div class="m-row">
          <button
            class="m-btn m-btn-sign-up"
            type="submit"
            @click.prevent="onSumbitLogin"
          >Đăng Nhập</button>
        </div>
      </form>
      <div class="m-footer-sign-up">
        <span class="m-text">Tôi là 1 người mới.</span>
        <div>
          <router-link
            to="register"
            class="m-text-sign-in"
          >Đăng kí</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      login: {
        username: "",
        password: "",
      },
      isError: false,
    };
  },
  methods: {
    async onSumbitLogin() {
      // Gọi o2authen_info để chứng thực
      // var me = this;
      try {
        let response = await axios.get("oauth2_info/");
        let res = await axios.post("o/token/", {
          username: this.login.username,
          password: this.login.password,
          client_id: response.data.client_id,
          client_secret: response.data.client_secret,
          grant_type: "password",
        });
        console.log(res);
        localStorage.setItem("access_token", res.data.access_token);
        let user = await axios.get("users/current-user/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        localStorage.setItem("YourUser", JSON.stringify(user.data));
        console.log(user.data);
        this.$router.push("/");
      } catch (error) {
        this.isError = true;
      }
    },
  },
};
</script>

<style scoped>
.info-error {
  color: #691911;
  background-color: #f4d6d2;
  border-color: #f0c5c1;
  height: 30px;
  display: flex;
  line-height: 30px;
  padding: 0px 10px;
}
</style>