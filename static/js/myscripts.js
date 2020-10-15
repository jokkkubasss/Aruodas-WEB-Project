let api_key = 'API_KEY'
var map, searchManager;

function GetMap() {
    map = new Microsoft.Maps.Map('#myMap', {
        credentials: api_key,
        center: new Microsoft.Maps.Location(54.681390, 25.279877),
        mapTypeId: Microsoft.Maps.MapTypeId.road,
        zoom: 10

    });

    Microsoft.Maps.loadModule(['Microsoft.Maps.AutoSuggest', 'Microsoft.Maps.Search'], function() {
        var manager = new Microsoft.Maps.AutosuggestManager({
            map: map
        });
        manager.attachAutosuggest('#address-search', '#address-search-container', suggestionSelected);
        searchManager = new Microsoft.Maps.Search.SearchManager(map);
    });

    Microsoft.Maps.Events.addHandler(map, 'click', suggestionSelected);

}

function suggestionSelected(result) {
    //Remove previously results from the map.
    map.entities.clear();

    if (result && result.location && result.location.latitude && result.location.longitude) {
        $('#lat').val(result.location.latitude);
        $('#lon').val(result.location.longitude);

        if (!result.formattedAddress && !result.formattedSuggestion) {
            var addressUrl = "https://dev.virtualearth.net/REST/v1/LocationRecog/";
            let response_data = 'none';
            console.log("TEST1");
            $.getJSON(''.concat(addressUrl + result.location.latitude + "," + result.location.longitude + "?&includeEntityTypes=address&key=" + api_key), function(data) {
                response_data = data.resourceSets[0].resources[0].addressOfLocation[0].formattedAddress;
                console.log(response_data);
                console.log("TEST");
                console.log(data.resourceSets[0].resources[0].addressOfLocation[0].formattedAddress);
                if (response_data) {
                    $('#address-search').val(response_data);
                    $('#address').val(response_data);
                } else {
                    $('#address-search').val('');
                    $('#address').val('');
                }
            });
        };
    } else {
        if (result.formattedAddress) {
            $('#address').val(result.formattedAddress);
        } else if (result.formattedSuggestion) {
            $('#address').val(result.formattedSuggestion);
        }
    }

    //Show the suggestion as a pushpin and center map over it.
    var pin = new Microsoft.Maps.Pushpin(result.location);

    map.entities.push(pin);
    map.setView({
        bounds: result.bestView
    });
}

(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
