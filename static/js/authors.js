var vm = new Vue({
    el: '#root',
    
    data: {
        authors: [],
        searchText: '',
        currentAuthor: {
            first_name: '',
            second_name: '',
        },
    },
    
    methods: {
        getAuthors : function(){
            let self = this;
            $.getJSON('/api/authors', function(data){
                self.authors = data['result'];
            });
        },
        
        showAuthorModal : function(author){
            if (author){
                this.currentAuthor.id = author.id;
                this.currentAuthor.first_name = author.first_name;
                this.currentAuthor.second_name = author.second_name;
            }else{
                this.currentAuthor.id = null;
                this.currentAuthor.first_name = '';
                this.currentAuthor.second_name = '';
            }
            $('#authorModal').modal("show");
        },
        
        addAuthor : function(){
            let self = this;
            $.ajax({
                url: '/api/authors',
                method: 'POST',
                data: JSON.stringify(self.currentAuthor),
                contentType: 'application/json',
                success: function(data){
                    vm.authors.push(data);
                    vm.authors.sort((a, b) => {
                        if (a.second_name < b.second_name)
                            return -1;
                        if (a.second_name > b.second_name)
                            return 1;
                        if (a.first_name < b.first_name)
                            return -1;
                        return 1;
                    });
                    $('#authorModal').modal("hide");
                }
            });
        },
        
        editAuthor : function(author){
            let self = this;
            $.ajax({
                url: '/api/authors/' + self.currentAuthor.id,
                method: 'PUT',
                data: JSON.stringify(self.currentAuthor),
                contentType: 'application/json',
                success: function(data){
                    let author = vm.authors.find((a) => {
                        return a.id == data.id;
                    });
                    for (var key in data){
                        author[key] = data[key];
                    };
                    $('#authorModal').modal("hide");
                }
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
