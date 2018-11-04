var app = new Vue({
    el: '#app',
    data: {
        name:'john',
        hasname:'NoKnow',
        static:""
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
    }
});