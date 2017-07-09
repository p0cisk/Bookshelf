var vm = new Vue({
    el: '#root',
    
    data: {
        books: [],
    },
    
    methods: {
        getBooks : function(){
            let self = this;
            $.getJSON('/api/stories', function(data){
                self.books = data['result'];
            });
        }
    }
});

vm.getBooks();
