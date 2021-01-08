
class StockAnalysis{
    constructor(){
    }
    loadCountryList(){
        let endpoint = '/model_training/companies-list';
        $.ajax({
            url: endpoint,
            type: 'GET',
            data: { is_trained: "1"},
            contentType: "application/json",
            dataType: 'json',
            error: function(err) {
//                callback();
            },
            success: function(result) {
                $('#trainedCompanies').selectize({
                    plugins: ['remove_button'],
                    persist: false,
                    maxItems: null,
                    valueField: 'symbol',
                    labelField: 'company_name',
                    searchField: ['company_name'],
                    options: result,
                    render: {
                        item: function(item, escape) {
                            return '<div>' +
                                (item.company_name ? '<span class="name">' + escape(item.company_name) + '</span>' : '') +
                            '</div>';
                        },
                        option: function(item, escape) {
                            var company_name = item.company_name || null;
                            var symbol = item.symbol ? item.symbol : null;
                            var country = item.country ? item.country : null;
                            var trained_on = item.trained_on ? item.trained_on : null;
                            var option= `
                                <div>
                                    <span class="label">${escape(company_name)}</span>
                                    <span class="caption">Code: ${escape(symbol)}, Country: ${escape(country)}, Trained On: ${escape(trained_on)}</span>
                                </div>
                            `;
                            return option;
                        }
                    },
                    onChange: function(value) {
                    }
                });
            }
        })
    }
}

$( document ).ready(function() {
    let stockAnalysisObj = new StockAnalysis();
    stockAnalysisObj.loadCountryList();
    $('.modelForm').on('submit',function(e){
        e.preventDefault();
        let trainedCompanies= $('#trainedCompanies').val();
        if(trainedCompanies && trainedCompanies.length >0){
            var formData=$(this).serialize();
            var fullUrl = window.location.origin+window.location.pathname;
            var finalUrl = fullUrl+"?"+formData;
            window.location.href = finalUrl;
        }
        else{
            alert("Please choose the company to do future prediction.");
        }
    })
//    $('#companies').selectize({
//        plugins: ['remove_button'],
//        persist: false,
//        maxItems: null,
//        valueField: 'value',
//        labelField: 'name',
//        searchField: ['name'],
//        options: [
//          {
//            "value": "A2",
//            "name": "Satellite Provider"
//          },
//          {
//            "value": "O1",
//            "name": "Other Country"
//          }
//        ],
//        onChange: function(value) {
//        }
//    });
//let endpoint = '/stock_forecast/companies-list';
//$.ajax({
//    url: endpoint,
//    type: 'GET',
//    data: { query: "aa"},
//    contentType: "application/json",
//    dataType: 'json',
//    error: function(err) {
//        callback();
//    },
//    success: function(result) {
//        $('#companies').selectize({
//            plugins: ['remove_button'],
//            persist: false,
//            maxItems: null,
//            valueField: 'symbol',
//            labelField: 'name',
//            searchField: ['name'],
//            options: result,
//            onChange: function(value) {
//            }
//        });
//    }
//})

//$("#companies").selectize({
//      plugins: ['remove_button'],
//      valueField: 'symbol',
//      labelField: 'name',
//      searchField: ['name'],
//      closeAfterSelect: true,
//      load: function(query, callback) {
//        let endpoint = '/stock_forecast/companies-list';
//          $.ajax({
//                url: endpoint,
//                type: 'GET',
//                data: { query: "aa"},
//                contentType: "application/json",
//                dataType: 'json',
//                error: function(err) {
//                    callback();
//                },
//                success: function(result) {
//                    callback(result);
//                }
//            })
//
////        $.ajax({
////          url: url,
////          data: { query: query},
////          dataType: "json",
////          type: 'GET',
////          error: function() {
////            callback();
////          },
////          success: function(res) {
////            callback(res);
////          }
////        })
//      }
//    });
});