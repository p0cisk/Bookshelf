var vm = new Vue({
    el: '#root',
    
    data: {
        searchText: '',
        currentAuthorData: {},
        currentAuthorStories: [],
    },
    
    methods: {
        loadAuthor : function(){
            let self = this;
            $.getJSON('/api/authors/'+currentAuthor, function(data){
                self.currentAuthorData = data;
                self.currentAuthor = data['id'];
            });
            $.getJSON('/api/authors_stories/'+currentAuthor, function(data){
                self.currentAuthorStories = data.result;
            });
        },
        
        showAuthors : function(){
            this.currentAuthor = null;
            this.currentAuthorData = {};
            this.currentAuthorStories = [];
        }
    },
    
    computed: {
        filteredStories: function(){
            return this.currentAuthorStories;
        },
    }
});

vm.loadAuthor()
