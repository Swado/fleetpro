$(document).ready(function() {
    var map = new jsVectorMap({
        selector: '#map',
        map: 'us_merc',
        zoomOnScroll: true,
        zoomButtons: true,
        regionStyle: {
            initial: {
                fill: '#c9d6de',
            },
            hover: {
                fill: '#2C3E50'
            },
            selected: {
                fill: '#E67E22'
            }
        },
        onRegionClick: function(event, code) {
            // Get the state name from the map
            var stateName = map.getRegionName(code);
            // Update the state select
            $('#state').val(code.toUpperCase());
            
            // Show selection in UI
            $('#selected-region').text('Selected: ' + stateName);
        },
        onRegionSelected: function(event, code, isSelected, selectedRegions) {
            if (isSelected) {
                // You could trigger an API call here to get cities in the selected state
                // For now, we'll just focus on state selection
                $('#region-helper').text('Now enter a city in ' + map.getRegionName(code));
            }
        }
    });
});
