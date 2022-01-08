<template>
  <!-- Ẩn hiện diaglog -->
  <div class="m-diaglog-modal">
    <div class="m-popup">
      <!-- Phần first name -->
      <div class="m-row">
        <div class="m-title-attr">First Name</div>
        <div class="m-attr-value">{{user_info.first_name}}</div>
        <div class="m-feature-edit">Edit</div>
      </div>
      <!-- Phần last name -->
      <div class="m-row">
        <div class="m-title-attr">Last Name</div>
        <div
          v-if="!isConvertDivInput"
          class="m-attr-value"
        >
          <li>{{user_info.last_name}}</li>

        </div>
        <input
          v-if="isConvertDivInput"
          type="text"
          class="m-attr-value"
          @mouseleave="isConvertDivInput = false"
          v-model="user_info.last_name"
        />
        <div v-if="isIconEdit"><i class="far fa-edit"></i></div>
        <div
          @mouseover="isIconEdit = true"
          @mouseleave="isIconEdit = false"
          @click.prevent="EditValueFeature()"
          class="m-feature-edit"
        >Edit</div>
      </div>
      <!-- Phần Username -->
      <div class="m-row">
        <div class="m-title-attr">UserName</div>
        <div class="m-attr-value">{{user_info.username}}</div>
        <div class="m-feature-edit">Edit</div>
      </div>
      <!-- Phần Password -->
      <div class="m-row">
        <div class="m-title-attr">Password</div>
        <div class="m-attr-value"> ******* </div>
        <div class="m-feature-edit">Edit</div>
      </div>
      <!-- Phần Avatar -->
      <div class="m-row">
        <div class="m-title-attr">avatar</div>
        <div class="m-attr-value">{{user_info.avatar}}</div>
        <div class="m-feature-edit">Edit</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user_info: {
      type: Object,
      require: true,
    },
  },
  data() {
    return {
      isIconEdit: false,
      isConvertDivInput: false,
    };
  },
  methods: {
    EditValueFeature() {
      console.log("feag");
      this.isConvertDivInput = !this.isConvertDivInput;
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
  background-color: rgba(0, 0, 0, 0.4);
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
  width: 400px;
  height: 300px;
  z-index: 99;
  /* border: 2px solid red; */
}
.m-row {
  display: flex;
  align-items: flex-end;
  margin-bottom: 20px;
  border-bottom: 1px solid rgb(235, 231, 231);
}
.m-title-attr {
  width: 100px;
}
.m-attr-value {
  width: 200px;
  display: inline-flex;
}
.m-feature-edit {
  margin-left: 5px;
  cursor: pointer;
}
input {
  padding: 0px 5px;
}
input:focus {
  outline: none;
  border: 1px solid #bbb;
}
li {
  display: inline;
}
</style>