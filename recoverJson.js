require('fs').readFile('path/wikidataExtract/WikiExtracted_test.json', function (err, data) {
    if (err) 
       // error handling

    var obj = JSON.parse(data);
    console.log(obj)
});