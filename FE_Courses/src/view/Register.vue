<template>
  <div class="m-container">
    <form>
      <!-- Phần thông báo đăng nhập sai -->
      <div
        v-if="isError"
        class="m-row info-error"
      >
        {{ message}}
      </div>
      <!-- Phần tên -->
      <div class="m-row">
        <label form="FullName">
          <span>Họ tên</span>
          <input
            class="m-input"
            type="text"
            placeholder="iMooney..."
            v-model="newUser.first_name"
          />
        </label>
      </div>
      <!-- Phần email -->
      <div class="m-row">
        <label form="Email">
          <span>Tài khoản</span>
          <input
            class="m-input"
            type="email"
            placeholder="example@gmail.com"
            v-model="newUser.username"
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
            v-model="newUser.password"
          />
        </label>
      </div>
      <!-- Phần confirm password -->
      <div class="m-row">
        <label form="Password">
          <span>Mật khẩu</span>
          <input
            class="m-input"
            type="password"
            placeholder="password"
            v-model="confirmPassword"
          />
        </label>
      </div>
      <!-- Phần submit -->
      <div class="m-row">
        <button
          class="m-btn m-btn-sign-up"
          type="submit"
          @click.prevent="RegisterNewUser()"
        >Đăng kí</button>
      </div>
    </form>
    <div class="m-footer-sign-up">
      <span class="m-text">Tôi đã có tài khoản.</span>
      <div>
        <router-link
          to="/login"
          class="m-text-sign-in"
        >Đăng nhập</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      newUser: {
        first_name: "",
        username: "",
        password: "",
      },
      confirmPassword: "",
      isError: false,
      message: "",
    };
  },
  methods: {
    async RegisterNewUser() {
      // Kiểm tra tài khoản
      let len = this.newUser.username.length;
      if (len < 6) {
        this.isError = true;
        this.message = "Tài khoản phải có ít nhất 6 kí tự";
        return false;
      }
      // Kiểm tra mật khẩu
      len = this.newUser.password.length;
      if (len < 8) {
        this.isError = true;
        this.message = "Mật khẩu phải có ít nhất 8 kí tự";
        return false;
      }
      if (this.confirmPassword != this.newUser.password) {
        this.isError = true;
        this.message = "Mật khẩu không trùng nhau";
        return false;
      }
      // Gọi lên axios post để đăng kí thành viên
      try {
        await axios.post("users/", this.newUser);
        alert("Bạn đăng kí thành công");
        this.$router.push("/login");
      } catch (error) {
        console.log(error);
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