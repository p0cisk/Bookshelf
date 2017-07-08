var vm = new Vue({
    el: '#root',
    
    data: {
        authors: [],
    },
    
    methods: {
        getAuthors : function(){
            let self = this;
            $.getJSON('/api/authors', function(data){
                self.authors = data['result'];
            });
        }
    }
});

vm.getAuthors();
