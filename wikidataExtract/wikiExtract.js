var async = require('async');
var fs = require('fs');

var data = JSON.parse(fs.readFileSync('Clean_DS.json', 'utf8'));
var obj = JSON.parse(fs.readFileSync('wikidataExtract/WikiExtracted_test2.json', 'utf8'), 1000);
//var data2=		JSON.parse(fs.readFileSync('wikidataExtract/WikiExtracted.json', { encoding: 'utf8' }));

//console.log(obj)
const result = obj.filter(item => item.wikiExtract == null);
console.log(result.length)

var WikidataSearch = require('wikidata-search').WikidataSearch;
var wikidataSearch = new WikidataSearch();

var count = 0
async.eachSeries(obj, function(item, cb) {
	count = count +1 
	console.log(count)
	if(item.wikiExtract == null) {
		var name = item.Name_mod
		//console.log(name)
		wikidataSearch.set('search', name); //set the search term
		wikidataSearch.search(function(result, error) {
			if(error) {
				console.log(error);
				cb(error);
			} else {
				item.wikiExtract = result;
				fs.writeFile("wikidataExtract/WikiExtracted_24Jan.json", JSON.stringify(obj, null, 4), (err) => {
				    if (err) {
				        console.error(err);
			        	return;
			    	} 
			    	else console.log('Json Saved');
				});
				cb();
		    }
		});
	} else cb();
}, function(error) {
    // if any of the file processing produced an error, err would equal that error
    if( error) {
      // One of the iterations produced an error.
      // All processing will now stop.
      console.log('A file failed to process');
    } else {
      console.log('All files have been processed successfully');
    }
});