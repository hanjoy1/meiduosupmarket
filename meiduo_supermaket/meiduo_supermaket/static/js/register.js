// 创建Vue对象 vm
let vm = new Vue({
    el:'#app', // 通过id选择器找到绑定的html内容
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    // 数据对象
    data(){
        //v-model
        return{
        username: '',
        password: '',
        password_re: '',
        mobile: '',
        allow: '',
        image_code_url: '',
        image_code: '',
        error_image_code_message: '',
        //v-shou
        error_name: false,
        error_password: false,
        error_password_re: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        //error_message
        error_name_message: '1111111111',
        error_mobile_message: '',
        }
    },
    mounted(){ // 页面加载完会被调用
        // 生成图形验证码
        this.generate_image_code();

    },
    methods:{ //定义和实现方法
        // 生成图形验证码: 封装的思想，方便代码复用
        generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';
            console.log(this.image_code_url);
            //this.image_code_url = '/image_codes/' + this.uuid + '/';
        },
        // 检查用户名
        check_username(){
        // 用户名是否重复
            if (this.error_name == false) {
                let url = '/usernames/' + this.username + '/count/';
                axios.get(url,{
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            console.log(response.data.count);
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }

        },
        // 校验图形验证码
        check_image_code(){
            if (this.image_code.length != 4)
            {
                this.error_image_code_message = '请输入图形验证码';
                this.error_image_code = true;
            }
            else
            {
                this.error_image_code = false;
            }
        },
        // 检查手机号
        check_mobile(){
        },

        // 检查密码
        check_password(){
        },
        // 确认密码
        check_password_re(){
        },
        // 用户允许
        check_error_allow(){},
        // 监听表单提交，校验用户输入的数据
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password_re();
//            this.check_mobile();
//            this.check_allow();

             //校验之后，注册数据中，只要有错误，就禁用掉表单提交的事件
            if (this.error_name == true || this.error_password == true || this.error_password_re == true || this.error_mobile == true || this.error_allow == true)
            {
                //禁用表单
                window.event.returnValue = false;
            };
        },



        },
});
