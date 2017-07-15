var vm = new Vue({
    el: '#root',
    
    data: {
        stories: [],
        searchText: '',
    },
    
    methods: {
        getBooks : function(){
            let self = this;
            $.getJSON('/api/stories', function(data){
                self.stories = data['result'];
            });
        }
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

vm.getBooks();
