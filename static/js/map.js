$(document).ready(function() {
    // Initialize the map
    var map = $('#map').vectorMap({
        map: 'us_aea_en',
        backgroundColor: '#fff',
        borderColor: '#818181',
        borderOpacity: 0.25,
        borderWidth: 1,
        color: '#f4f3f0',
        enableZoom: true,
        hoverColor: '#3498db',
        hoverOpacity: 0.7,
        normalizeFunction: 'linear',
        scaleColors: ['#b6d6ff', '#005ace'],
        selectedColor: '#E67E22',
        selectedRegions: null,
        showTooltip: true,
        onRegionClick: function(element, code, region) {
            // Clear previous selections
            $('.jvectormap-region').css('fill', '#f4f3f0');

            // Highlight selected state
            $(element.path).css('fill', '#E67E22');

            // Update the state select dropdown
            $('#state').val(code.toUpperCase());

            // Show selection in UI
            $('#selected-region').html('<i class="fas fa-map-marker-alt"></i> Selected: ' + region);
            $('#region-helper').html('<i class="fas fa-info-circle"></i> Now enter a city in ' + region);

            // Trigger change event on state select
            $('#state').trigger('change');
        },
        onRegionTipShow: function(e, el, code) {
            el.html(el.html() + ' - Click to select');
        }
    }).vectorMap('get', 'mapObject');

    // Add zoom controls with custom styling
    $('.jvectormap-zoomin, .jvectormap-zoomout').css({
        'background-color': '#2C3E50',
        'color': 'white',
        'padding': '3px',
        'border-radius': '3px',
        'cursor': 'pointer'
    });
});