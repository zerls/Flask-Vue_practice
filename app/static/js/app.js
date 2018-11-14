var app = new Vue({
    el: '#app',
    data: {
        name:'john',
        hasname:'NoKnow',
        static:"",
        places:"",
        place_static:"",
        place:""

    },
    computed:{

    },
    methods:{
        Hasname: function () {
            axios.post('/api/v0/name', {name:this.name
                })
                .then(function (response) {
                    this.hasname = response.data.hasname
                }.bind(this))
        },
        delname: function () {
            axios.post('/api/v0/delname', {name:this.name
                })
                .then(function (response) {
                    this.static = response.data.static
                }.bind(this))
        },
        addname: function () {
            axios.post('/api/v0/addname', {name:this.name
                })
                .then(function (response) {
                    this.static = response.data.static
                }.bind(this))
        },
        listname: function () {
            axios.post('/api/v0/listname', {name:this.name
                })
                .then(function (response) {
                    this.static = response.data.static
                }.bind(this))
        },
        listUser_info: function () {
            axios.post('/api/v0/listUserInfo', {name:this.name
                })
                .then(function (response) {
                    this.static = response.data.static
                }.bind(this))
        },
        Place_info:function () {
            axios.post('/api/v0/Place_info', {place:this.place
                })
                .then(function (response) {
                    this.place_static = response.data.static
                }.bind(this))
        },
        listPlace:function () {
            axios.post('/api/v0/listPlace', {place:this.place})
                .then(function (response) {
                    this.places = response.data.static
                }.bind(this))
        },
    }
});


// listPlace