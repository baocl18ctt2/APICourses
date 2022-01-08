import Register from './view/Register.vue'
import Login from './view/Login.vue'
import Authen from './components/layout/Authen.vue'
import NavBar from './components/layout/NavBar.vue'
import Home from './components/layout/Home.vue'
import User from './components/layout/User.vue'
import Lesson from './components/layout/Lesson.vue'
import UpdateProfile from './view/UpdateProfile.vue'
const routes = [{
        path: '/',
        name: "home",
        components: {
            default: Home,
            'nav-bar': NavBar
        },
    },
    {
        path: '/register',
        name: "authen",
        component: Authen,
        children: [{
            path: '/',
            name: "register",
            component: Register
        }]
    },
    {
        path: '/login',
        name: "authen",
        component: Authen,
        children: [{
            path: '/',
            name: "login",
            component: Login
        }]
    }, {
        path: '/user',
        name: "user",
        components: {
            default: User,
            'nav-bar': NavBar
        }
    },
    {
        path: '/courses/:coursesId/lessons',
        name: "courses",
        components: {
            default: Lesson,
            'nav-bar': NavBar
        }
    },
    {
        path: '/update_profile',
        name: "profile",
        component: UpdateProfile
    },
    // {
    //     path: '/register',
    //     name: "register",
    //     component: Register,
    // }
]
export default routes;