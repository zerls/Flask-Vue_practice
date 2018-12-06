Vue.component('ppoint', {
    data: function () {
      return {
        count: 0,
        sty:{position:'absolute', 
            left:this.x*100-16+'px',top:this.y*100-36+'px',cursor:'pointer',color:'white'}
      }
   
    },
    props:[
        'msg',
        'x',
        'y',
      ],
    template: '<div  :style="sty" >\
    <div style="position:absolute; \
    width: 30px;\
    height: 30px;\
    border-radius: 50%;\
    background: rgb(0, 0, 0,0.8);\
    box-shadow: rgba(128, 128, 128, 0.05) 0px 4px 15px;\
    border-bottom-left-radius: 0;\
    transform: rotate(-45deg);"></div>\
    <span align="center" style="position:absolute; left:10px;top:4px;"\
    >{{ msg }}</span>\
    </div>',
  })

var app1= new Vue({
    el: '#can',
    data: {
        placelist: [
            {
              "id": 1, 
              "name": "p1", 
              "x": 1.0, 
              "y": 2.0
            }, 
            {
              "id": 2, 
              "name": "p2", 
              "x": 2.0, 
              "y": 2.0
            }, 
            {
              "id": 3, 
              "name": "p3", 
              "x": 3.0, 
              "y": 1.0
            }, 
            {
              "id": 4, 
              "name": "p4", 
              "x": 2.0, 
              "y": 1.0
            }, 
            {
              "id": 5, 
              "name": "p5", 
              "x": 5.0, 
              "y": 1.0
            }
          ]

    },
    computed:{

    },
    methods:{
        tripe(name){
            console.log("log:"+name)
            // alert(name)
        }
    }
})
  var app = new Vue({
    el: '#app',
    data: {
        name:'john',
        hasname:'NoKnow',
        static:"",
        places:"",
        place_static:"",
        place:"",

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