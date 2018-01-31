var async = require('async');
var fs = require('fs');
var r = require('request')
var dbpediaLookup = require('dbpedia-entity-lookup');
//var parseXlsx = require('excel');
var WikidataSearch = require('wikidata-search').WikidataSearch;
var wikidataSearch = new WikidataSearch();
var xlsx = require('node-xlsx');
var Dataset = null


var obj = JSON.parse(fs.readFileSync('Clean_DS.json', 'utf8'), 1000);
//console.log(obj);
var count = 0
async.eachSeries(obj, function(item, cb){
    // item['extracted_Db'] = {}
    // item['extracted_wiki'] = {}
    console.log(item.Name_mod+': In Process');
    async.series([
        function(done) {
            if(item['rawData_Db']==null){
                console.log('Fetching dbpedia')
                var options = {  
                    url: 'http://lookup.dbpedia.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString='+item.Name_mod,
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'Accept-Charset': 'utf-8',
                        'User-Agent': 'my-reddit-client'
                    }
                };

                r.get(options, function(err, response, body){
                    if(err) {
                        console.log(err)
                    } else {
                        //console.log(body)
                        item['rawData_Db'] = body
                        done();
                    }
                });
            } else {
                console.log('dbpedia data already fetched')
                done();
            }
            
        },
        function(done) {
            if(item['rawData_wiki:']==null){
                console.log('Fetching Wikidata')
                wikidataSearch.set('search', item.Name_mod); //set the search term
                wikidataSearch.search(function(result, error) {
                    if(error) {
                        console.log(error);
                        cb(error);
                    } else {
                        //console.log(result)
                        item['rawData_wiki:'] = result;
                        done()
                    }
                });
            } else {
                console.log('WikiData data already fetched')
                done(); 
            } 
        }
    ], function(err) {
        if(err) console.log(err) // "another thing" 
        else {
            count = count + 1;
            console.log('Done entity: ' + count.toString())
            fs.writeFile('Extracted_Entities.json', JSON.stringify(obj), 'utf8', function(err){
                    console.log(item.Name_mod+': Fetched and Saved');  
                    cb();
            });
        }
    });


}, function(err){
    if(err) console.log(err)
    else {
        console.log('Dataset saved and finished');  
           
    }   
});


        