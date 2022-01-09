<template>
  <div>
    <h1 class="text text-danger">DANH MỤC BÀI HỌC CỦA KHÓA HỌC</h1>
    <div class="m-grid-lesson">
      <div
        v-for="(lesson, index) in lessons"
        :key="lesson.id"
        @click.prevent="clickOnLessonDetail(lesson.id, index)"
      >
        <!-- Phần chung của 1 tiết học -->
        <div
          class="alert alert-secondary d-flex align-items-center"
          role="alert"
        >
          <div class="m-icon">
            <i class="fas fa-plus"></i>
          </div>
          <div>
            {{ lesson.subject}}
          </div>
        </div>
        <!-- Phần bổ sung -->
        <div
          class="m-content-tag-lesson"
          v-show="isLessonDetail[index]"
        >
          <!-- Phần chi tiết -->
          <div class="m-grid-lesson-detail">
            <div class="m-row m-content-style">
              <div class="m-icon-content">
                <i class="fas fa-play"></i>
              </div>
              <div>Nội dung</div>
            </div>
            <div class="m-content-detail">
              <div> {{ lessonDetail.content }}</div>
            </div>
          </div>
          <!-- Các thành phần liên quan của bài học -->
          <div class="m-grid-lesson-detail">
            <div class="m-row m-content-style">
              <div class="m-icon-content">
                <i class="fas fa-play"></i>
              </div>
              <div>Tags</div>
            </div>
            <div class="m-content-detail">
              <ul>
                <li
                  v-for="tag in lessonDetail.tags"
                  :key="tag.id"
                >{{ tag.name}}
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>

    </div>
    <button @click="testdata()">test</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      isLessonDetail: [],
      lessons: [],
      coursesId: this.$route.params.coursesId,
      lessonsId: null,
      lessonDetail: [],
    };
  },
  async created() {
    var me = this;
    try {
      let response = await axios.get(`courses/${this.coursesId}/lessons/`);
      me.lessons = response.data;
      console.log(me.lessons);
      // Khởi tạo mảng false tương ứng
      let countLessons = me.lessons.length;
      for (let index = 0; index < countLessons; index++) {
        me.isLessonDetail[index] = false;
        // me.lessonDetail[index] = [];
      }

      console.log(me.isLessonDetail);
    } catch (error) {
      console.log(error);
    }
    // var me = this;
    // axios
    //   .get(`courses/${this.coursesId}/lessons/`)
    //   .then((response) => {
    //     me.lessons = response.data;
    //     console.log(me.lessons);
    //     // Khởi tạo mảng false tương ứng
    //     let countLessons = me.lessons.length;
    //     for (let index = 0; index < countLessons; index++) {
    //       me.isLessonDetail[index] = false;
    //     }
    //   })
    //   .catch((error) => console.log(error));
  },
  methods: {
    async clickOnLessonDetail(lessonId, index) {
      var me = this;
      if (!this.isLessonDetail[index]) {
        console.log(index);
        // Gọi lên axios lấy thông tin khóa học
        let res = await axios.get(`lessons/${lessonId}/`);
        me.lessonDetail = res.data;
      } else {
        me.lessonDetail = [];
      }
      // Ẩn hiện nội dung chi tiết của tiết học
      me.isLessonDetail[index] = !me.isLessonDetail[index];
      // console.log("fea", me.lessonDetail[index].content);
      // console.log(me);
    },
    testdata() {
      // this.id = ;
      console.log("id", this.lessonsId);
    },
  },
};
</script>


<style scoped>
.m-grid-lesson {
  margin: 20px;
}
.m-icon {
  margin: 0px 10px;
}
.m-grid-lesson-detail {
  /* background-color: #bbb; */
  padding: 10px 0px 0px 30px;
}
.alert {
  margin-bottom: 0px;
}
.m-icon-content {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.m-content-style {
  align-items: center;
  border-bottom: 1px solid #bbb;
}
.m-content-detail {
  margin-left: 30px;
}
.align-items-center:hover {
  cursor: pointer;
}
.m-content-tag-lesson {
  background-color: rgb(235, 228, 228);
}

.editOther {
  background-color: red;
}
</style>

 