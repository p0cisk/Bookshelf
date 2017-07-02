var vm = new Vue({
    el: '#root',
    
    data: {
        books: [],
    },
    
    methods: {
        getBooks : function(){
            let self = this;
            $.getJSON('/api/books', function(data){
                self.books = data['result'];
            });
        }
    }
});

vm.getBooks();
