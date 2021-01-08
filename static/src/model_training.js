
class TrainedStockModel{
    constructor(){
    }
    loadCountryList(){
        let endpoint = '/model_training/companies-list';
        $.ajax({
            url: endpoint,
            type: 'GET',
            data: {},
            contentType: "application/json",
            dataType: 'json',
            error: function(err) {
//                callback();
            },
            success: function(result) {
                $('#allCompanies').selectize({
                    plugins: ['remove_button'],
                    persist: false,
                    maxItems: null,
                    valueField: 'symbol',
                    labelField: 'name',
                    searchField: ['name'],
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
    let trainedStockObj = new TrainedStockModel();
    trainedStockObj.loadCountryList();
    $("#loading_summary").hide();
    $('.modelForm').on('submit',function(e){
        e.preventDefault();
        let allCompanies= $('#allCompanies').val();
        if(allCompanies && allCompanies.length >0){
            $("#loading_summary").show(1000);
            var formData=$(this).serialize();
            var fullUrl = window.location.origin+window.location.pathname;
            var finalUrl = fullUrl+"?"+formData;
            window.location.href = finalUrl;
        }
        else{
            alert("Please choose the company to train the model.");
        }
    })

});