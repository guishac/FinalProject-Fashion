
var url = "/jsonData";


d3.json(url).then(function(response) {
    console.log(response[0]['Item_Name']);
    console.log('Hello')
});
