var vm = new Vue({
    el: '#root',
    
    data: {
        authors: [],
        searchText: '',
    },
    
    methods: {
        getAuthors : function(){
            let self = this;
            $.getJSON('/api/authors', function(data){
                self.authors = data['result'];
            });
        },
    },
    
    computed: {
        filteredAuthors: function() {
            if (!this.searchText){ return this.authors };
            let text = this.searchText.toLowerCase();
            return this.authors.filter(function(author){
                return author.first_name.toLowerCase().indexOf( text )!==-1 || author.second_name.toLowerCase().indexOf( text )!==-1;
            })
        },
    }
});

vm.getAuthors();
