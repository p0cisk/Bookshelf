var vm = new Vue({
    el: '#root',
    
    data: {
        searchText: '',
        authorData: {},
        stories: [],
    },
    
    methods: {
        loadAuthor : function(){
            let self = this;
            $.getJSON('/api/authors/'+currentAuthor, function(data){
                self.authorData = data;
                self.currentAuthor = data['id'];
            });
            $.getJSON('/api/authors_stories/'+currentAuthor, function(data){
                self.stories = data.result;
            });
        },
    },
    
    computed: {
        filteredStories: function(){
            if (!this.searchText){ return this.stories };
            let text = this.searchText.toLowerCase();
            return this.stories.filter(function(story){
                return story.title.toLowerCase().indexOf( text )!==-1;
            })
        },
    }
});

vm.loadAuthor()
