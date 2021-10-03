var start = 0;
var create = 1;
var wwd = new WorldWind.WorldWindow("canvasOne");
var highlightedItems = [];
var id_name = '', lat = '', long = '', alt = '';
var param = "0";
var time = "0";

function recuperer_arguments (arg) {
    /** Retrieve the category of satellites to be displayed
     * @param {string} arg Satellite category number
     */

    param = arg;
    create = 1;
}

function recuperer_temps (arg) {
    /** Get the time we want to display
     * @param {string} arg Additional time
     */

    time = arg;
}

function updateURL () {
    /** Give the url to make a request to the API to get all the data we want to display
     * @return {string} Return the url
     */

    var url = '/data-space-debris/';
    var urlParam = url.concat("", param);
    var newURL = urlParam.concat("/", time);

    return newURL;
}

var newURL = updateURL();

fetch(newURL)
    .then(function (response) {
        return response.json();
    }).then(function (donnee) {
        fct_wwd(donnee);
    });

function updateDataFunc () {
    /** Update all the data we want to display on the HTML page
    */

    newURL = updateURL();

    fetch(newURL)
    .then(function (response) {
        return response.json();
    }).then(function (donnee) {
        fct_wwd(donnee);
    });

    setTimeout(updateDataFunc, 1000);
}

updateDataFunc();

function updateUrlNewTime () {
    /** Give the url to make a request to the API to retrieve the desired date
     * @return {string} Return the url
     */

    var url = '/get-new-time/';
    var newURL = url.concat("", time);

    return newURL;
}

var UrlNewTime  = updateUrlNewTime();

fetch(UrlNewTime)
    .then(function (response) {
        return response.json();
    }).then(function (donnee) {
        document.getElementById("newtime").innerHTML = donnee;
    });

function updateTime () {
    /** Update the time that is displayed on the HTML page
     */

    UrlNewTime = updateUrlNewTime();

    fetch(UrlNewTime)
    .then(function (response) {
        return response.json();
    }).then(function (donnee) {
        document.getElementById("newtime").innerHTML = donnee;
    });

    setTimeout(updateTime, 1000);
}

updateTime();

function fct_wwd(dictionnaire) {
    /** Create a WorldWindow for the canvas and upload the placemarks
     * @param {dict} dictionnaire Dictionary of the contains all the debris
     */

    if (!start){
        //var wwd = new WorldWind.WorldWindow("canvasOne");
        wwd.addLayer(new WorldWind.BMNGOneImageLayer());
        wwd.addLayer(new WorldWind.BMNGLandsatLayer());
        wwd.addLayer(new WorldWind.CompassLayer());
        wwd.addLayer(new WorldWind.CoordinatesDisplayLayer(wwd));
        wwd.addLayer(new WorldWind.ViewControlsLayer(wwd));

        var date = new Date();
        var at = new WorldWind.AtmosphereLayer()
        at.time = date;
        wwd.addLayer(at);

        var st = new WorldWind.StarFieldLayer()
        st.time = date;

        st.enabled = true
        st.showSun = true
        st.starDataSource = WorldWind.configuration.baseUrl + 'images/stars.json'
        st.sunImageSource = WorldWind.configuration.baseUrl + 'images/sunTexture.png'

        wwd.addLayer(st);
        wwd.addEventListener("mousemove", handlePick);

        start = 1
    }

    if (create){
        placeMark(dictionnaire, wwd);
        create = 0;
    }

    updatePlacemark(dictionnaire)

    // Add WMS imagery
    var serviceAddress =
    "https://neo.sci.gsfc.nasa.gov/wms/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0";
    var layerName = "MOD_LSTD_CLIM_M";

    var createLayer = function (xmlDom) {
    var wms = new WorldWind.WmsCapabilities(xmlDom);
    var wmsLayerCapabilities = wms.getNamedLayer(layerName);
    var wmsConfig = WorldWind.WmsLayer.formLayerConfiguration(wmsLayerCapabilities);
    var wmsLayer = new WorldWind.WmsLayer(wmsConfig);
    wwd.addLayer(wmsLayer);
    };

    var logError = function (jqXhr, text, exception) {
        console.log(
            "There was a failure retrieving the capabilities document: " +
            text +
            " exception: " +
            exception
        );
    };

    $.get(serviceAddress).done(createLayer).fail(logError);
}

function placeMark(dictionnaire, wwd){
    /** Erase the previous placemarks to upload the new placemarks using the dictionary
     * @param {Dictionary} dictionnaire Contains all the debris
     */

    deletePlaceMark(wwd)

    var placemarkLayer = new WorldWind.RenderableLayer();
    wwd.addLayer(placemarkLayer);

    var placemarkAttributes = new WorldWind.PlacemarkAttributes(null);

    placemarkAttributes.imageOffset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION,
        0.3,
        WorldWind.OFFSET_FRACTION,
        0.0
    );

    placemarkAttributes.labelAttributes.offset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION,
        0.5,
        WorldWind.OFFSET_FRACTION,
        1.0
    );


    placemarkAttributes.imageSource = 'https://i.ibb.co/NZLtcjZ/Sans-titre-1.png';
    for (i=0;i<dictionnaire.coordonnees.length;i++) {
        var id = dictionnaire['coordonnees'][i]['id'];
        var nom = dictionnaire['coordonnees'][i]['name'];
        var altitude = dictionnaire['coordonnees'][i]['altitude'];
        var latitude = dictionnaire['coordonnees'][i]['latitude'];
        var longitude = dictionnaire['coordonnees'][i]['longitude'];

        var position = new WorldWind.Position(latitude, longitude, altitude);
        var placemark = new WorldWind.Placemark(position, false, placemarkAttributes);

        placemark.label = id+'/'+nom
        //placemark.alwaysOnTop = true;
        //placemark.altitudeMode = WorldWind.RELATIVE_TO_GROUND;
        placemarkAttributes.labelAttributes.scale = 0
        placemarkLayer.addRenderable(placemark);
    }
}

function updatePlacemark(dictionnaire){
    /** Upload the new position of the placemarks
     * @param {Dictionary} dictionnaire Contains all the debris
     */

    for (i in wwd.layers[7].renderables) {
        wwd.layers[7].renderables[i].position.altitude = dictionnaire['coordonnees'][i]['altitude'];
        wwd.layers[7].renderables[i].position.latitude = dictionnaire['coordonnees'][i]['latitude'];
        wwd.layers[7].renderables[i].position.longitude = dictionnaire['coordonnees'][i]['longitude'];
    }

    wwd.redraw()
}

function deletePlaceMark(wwd){
    /**  Deleta the previous placemarks that were on the canvas to be able to have only the ones according to the time
     * @param {Canvas} wwd
     */

    for (i in wwd.layers){
        if (wwd.layers[i].displayName == 'Layer'){
            wwd.removeLayer(wwd.layers[i])
        }
    }
}

var handlePick = function (o) {
    /** This fucntion allow us to identify the position of the cursor so then we can display the real
     * coordinates of the selected satellite
     * @param {event} o
     */
    var x = o.clientX,
    y = o.clientY;

    var redrawRequired = highlightedItems.length > 0; // must redraw if we de-highlight previously picked items

    // De-highlight any previously highlighted placemarks.
    for (var h = 0; h < highlightedItems.length; h++) {
        highlightedItems[h].highlighted = false;
    }
    highlightedItems = [];

    // Perform the pick. Must first convert from window coordinates to canvas coordinates, which are
    // relative to the upper left corner of the canvas rather than the upper left corner of the page.
    var pickList = wwd.pick(wwd.canvasCoordinates(x, y));

    if (pickList.objects.length > 0) {
        redrawRequired = true;
    }

    // Highlight the items picked by simply setting their highlight flag to true.
    if (pickList.objects.length > 0) {
        for (var p = 0; p < pickList.objects.length; p++) {
            if (pickList.objects[p].userObject.displayName == 'Renderable'){
                id_name = pickList.objects[p].userObject.label
                alt = pickList.objects[p].userObject.position.altitude
                lat = pickList.objects[p].userObject.position.latitude
                long = pickList.objects[p].userObject.position.longitude
            }
        pickList.objects[p].userObject.highlighted = true;

        // Keep track of highlighted items in order to de-highlight them later.
        highlightedItems.push(pickList.objects[p].userObject);

        document.getElementById("name").innerHTML = id_name;
        document.getElementById("altitude").innerHTML = String(alt)+" m";
        document.getElementById("latitude").innerHTML = String(lat)+" °";
        document.getElementById("longitude").innerHTML = String(long)+" °";

        }
    }

    if (redrawRequired) {
        wwd.redraw(); // redraw to make the highlighting changes take effect on the screen
    }
}