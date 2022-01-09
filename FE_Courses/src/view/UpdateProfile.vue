<template>
  <!-- Ẩn hiện diaglog -->
  <div class="m-diaglog-modal">
    <div class="m-popup">
      <div class="container">
        <h1>Edit Profile</h1>
        <hr>
        <div class="row">
          <!-- left column -->
          <div class="col-md-3">
            <div class="text-center">
              <img
                v-if="user_info.avatar"
                :src="`http://127.0.0.1:8000/static${user_info.avatar}`"
                style="width: 80px; height: 80px"
                class="avatar rounded-circle"
                alt="avatar"
              >
              <h6>Upload a different photo...</h6>

              <input
                type="file"
                class="form-control"
              >
            </div>
          </div>

          <!-- edit form column -->
          <div class="col-md-9 personal-info">
            <div class="alert alert-info alert-dismissable">
              <a
                class="panel-close close"
                data-dismiss="alert"
              >×</a>
              <i class="fa fa-coffee"></i>
              <div>
                This is an <strong>.alert</strong>. Use this to show important messages to the user.
              </div>

            </div>
            <h3>Personal info</h3>

            <form
              class="form-horizontal"
              role="form"
            >
              <div class="form-group">
                <label class="col-lg-3 control-label">First name:</label>
                <div class="col-md-8">
                  <input
                    class="form-control"
                    type="text"
                    :value="user_info.first_name"
                    v-on:input="update_user.first_name = $event.target.value"
                  >
                </div>
              </div>
              <!-- Phần last name -->
              <div class="form-group">
                <label class="col-lg-3 control-label">Last name:</label>
                <div class="col-md-8">
                  <input
                    class="form-control"
                    type="text"
                    :value="user_info.last_name"
                    v-on:input="update_user.last_name = $event.target.value"
                  >
                </div>
              </div>
              <!-- Phần địa chỉ email -->
              <div class="form-group">
                <label class="col-lg-3 control-label">Email:</label>
                <div class="col-md-8">
                  <input
                    class="form-control"
                    type="text"
                    :value="user_info.email"
                    v-on:input="update_user.email = $event.target.value"
                  >
                </div>
              </div>
              <!-- Phần user name -->
              <div class="form-group">
                <label class="col-md-3 control-label">Username:</label>
                <div class="col-md-8">
                  <input
                    class="form-control"
                    type="text"
                    :value="user_info.username"
                    v-on:input="update_user.username = $event.target.value"
                  >
                </div>
              </div>
              <div class="form-group">
                <label class="col-md-3 control-label">New Password:</label>
                <div class="col-md-8">
                  <input
                    class="form-control"
                    type="password"
                    :value="reset_password.new_password"
                    v-on:input="update_user.password = $event.target.value"
                  >
                </div>
              </div>
              <div class="form-group">
                <label class="col-md-5 control-label">Confirm new password:</label>
                <div class="col-md-8">
                  <input
                    class="form-control"
                    type="password"
                    :value="reset_password.confirm_password"
                  >
                </div>
              </div>
              <div class="form-group">
                <label class="col-md-3 control-label"></label>
                <div class="col-md-8">
                  <input
                    type="button"
                    class="btn btn-primary"
                    value="Save Changes"
                    @click="updateProfile()"
                  >
                  <span></span>
                  <input
                    type="reset"
                    class="btn btn-default ml-20"
                    value="Cancel"
                    @click="cancelUpdateProfile()"
                  >
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: {
    user_info: {
      type: Object,
      require: true,
    },
  },
  data() {
    return {
      update_user: {},
      // user_info: this.user_info1,
      reset_password: {
        new_password: "",
        confirm_password: "",
      },
    };
  },
  methods: {
    async updateProfile() {
      // Gọi lên axios để patch thông tin
      console.log(this.update_user);
      try {
        await axios.patch(
          `users/${parseInt(this.user_info.id)}/`,
          this.update_user
        );
        this.$emit("updateInterfaceProfile", this.update_user);
        // Hủy popup
        this.$emit("cancelPopUp", false);
      } catch (err) {
        console.log(err);
      }
    },
    getFirstName($event) {
      this.update_user.first_name = $event.target.value;
    },
    cancelUpdateProfile() {
      console.log("x");
      this.$emit("cancelPopUp", false);
    },
  },
};
</script>
<style scoped>
.m-diaglog-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  width: 100%;
  height: 100vh;
  z-index: 98;
  display: block;
}
.m-popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 3px;
  padding: 30px 40px;
  background-color: #fff;
  max-width: 900px;
  z-index: 99;
}
</style>