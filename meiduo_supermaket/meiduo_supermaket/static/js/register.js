// 创建Vue对象 vm
let vm = new Vue({
    el:'#app', // 通过id选择器找到绑定的html内容
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    // 数据对象
    data:{
        //v-model
        username: '',
        password: '',
        password_re: '',
        mobile: '',
        //v-shou
        error_name: false,
        error_password: false,
        error_password_re: false,
        error_mobile: false,
        error_allow: false,
        //error_message
        error_name_message: '',
        error_mobile_message: '',
    },
    methods:{ //定义和实现方法
// 检查用户名
        check_username(){
        },
        // 检查密码
        check_password(){
        },
        // 确认密码
        check_password_re(){
        },
        // 监听表单提交，校验用户输入的数据
        on_submit(){
        },
    },
});