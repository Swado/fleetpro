$(document).ready(function() {
    // Initialize the map
    $('#map').vectorMap({
        map: 'us_aea_en',
        backgroundColor: '#fff',
        borderColor: '#818181',
        borderOpacity: 0.25,
        borderWidth: 1,
        color: '#f4f3f0',
        enableZoom: true,
        hoverColor: '#2C3E50',
        hoverOpacity: 0.7,
        normalizeFunction: 'linear',
        scaleColors: ['#b6d6ff', '#005ace'],
        selectedColor: '#E67E22',
        selectedRegions: null,
        showTooltip: true,
        onRegionClick: function(element, code, region) {
            // Update the state select dropdown
            $('#state').val(code.toUpperCase());

            // Show selection in UI
            $('#selected-region').text('Selected: ' + region);
            $('#region-helper').text('Now enter a city in ' + region);
        }
    });
});