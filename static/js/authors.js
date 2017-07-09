var vm = new Vue({
    el: '#root',
    
    data: {
        authors: [],
        searchText: '',
        currentAuthor: null,
        currentAuthorData: {}
    },
    
    methods: {
        getAuthors : function(){
            let self = this;
            $.getJSON('/api/authors', function(data){
                self.authors = data['result'];
            });
        },
        
        loadAuthor : function(author){
            if (author===null){
                this.currentAuthor = null;
                return
            };
            let self = this;
            $.getJSON('/api/authors/'+author.id, function(data){
                self.currentAuthorData = data;
                self.currentAuthor = data['id'];
            });
        },
        
        showAuthors : function(){
            this.currentAuthor = null;
            this.currentAuthorData = {};
        }
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
