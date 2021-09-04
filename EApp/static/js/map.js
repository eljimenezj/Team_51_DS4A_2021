NomC = ['RIOHACHA', 'NECOCLÍ', 'EL CARMEN DE BOLIVAR', 'DIBULLA (SIERRA NEVADA)', 'ARIGUANÍ', 'CAUCASIA', 'MONTERÍA', 'SABANALARGA', 'PIVIJAY', 'CARTAGENA', 'SAHAGÚN', 'SAN PEDRO DE URABÁ', 'SAMPUES', 'TURBO - APARTADO', 'CIÉNAGA', 'AYAPEL', 'EL BANCO', 'VALLEDUPAR']
CodC = [1285504, 1155322, 1210398, 1259275, 1249863, 1207119, 1183916, 1216586, 1234322, 1193453, 1197836, 1166758, 1202369, 1151781, 1245138, 1216434, 1241377, 1271225]
Dpto = ['LA GUAJIRA', 'ANTIOQUIA', 'BOLIVAR', 'LA GUAJIRA', 'MAGDALENA', 'ANTIOQUIA', 'CORDOBA', 'ATLANTICO', 'MAGDALENA', 'BOLIVAR', 'CORDOBA', 'ANTIOQUIA', 'SUCRE', 'ANTIOQUIA', 'MAGDALENA', 'CORDOBA', 'MAGDALENA', 'CESAR']
lat = [11.5344825, 8.4271957, 9.7176675, 11.2724318, 9.8442178, 7.9786912, 8.7606317, 10.6275712, 10.4612025, 10.4002813, 8.9338129, 8.2758536, 9.1823836, 8.021434, 11.0090981, 8.3093061, 9.0035285, 10.4645885]
lon = [-72.9321659, -76.7932168, -75.1320332, -73.3115252, -74.2368738, -75.2153376, -75.9169895, -74.9386441, -74.6234087, -75.5435449, -75.4641746, -76.3841063, -75.3909606, -76.643307, -74.2632396, -75.1583293, -73.9826188, -73.2932689]
populat = [188014, 70824, 70131, 39069, 32758, 123304, 490935, 102334, 33047, 914552, 90494, 30527, 38631, 200931, 105510, 56082, 55530, 490075]

$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

window.onload = function () {

    $("#t1").find('th:eq(0)').html('Date Time');
    $("#t1").find('th:eq(1)').html('DHI Forecast');
    $("#t1").find('th:eq(0)').css({ "text-align": "center", "background-color": "navy", "color": "white", "font-style": "unset", "font-size": "0.9em" });
    $("#t1").find('th:eq(1)').css({ "text-align": "center", "background-color": "navy", "color": "white", "font-style": "unset", "font-size": "0.9em" });
    $("#t1").find('th:eq(2)').css({ "text-align": "center", "background-color": "navy", "color": "white", "font-style": "unset", "font-size": "0.9em" });

    var cities = document.getElementById("concities");

    for (var i = 0; i < Number(NomC.length); i++) {
        var option = document.createElement("OPTION");
        option.innerHTML = NomC[i];
        option.value = i;
        cities.appendChild(option);
    }

    var idc = document.getElementById('pass').value;
    document.getElementById('concities').value = Number(idc);
    select();

    var map = geo.map({
        node: "#map",
        center: { x: lon[Number(idc)], y: lat[Number(idc)] },
        zoom: 7
    });

    map.createLayer('osm');

    var cities = [{ lon: lon[Number(idc)], lat: lat[Number(idc)], name: NomC[Number(idc)] }]

    var layer = map.createLayer('feature', { features: ['point'] });
    var feature = layer.createFeature('point')
        .data(cities)
        .position(function (city) {
            return {
                x: city.lon,
                y: city.lat
            };
        })
        .draw();

    var textLayer = map.createLayer('feature', { features: ['text'] });
    var textFeature = textLayer.createFeature('text')
        .data(cities)
        .position(function (city) {
            return {
                x: city.lon,
                y: city.lat
            };
        })
        .text(function (city) {
            return city.name;
        })
        .draw();

    textFeature.style({
        fontSize: '18px',
        fontFamily: 'tahoma',
        textAlign: 'left',
        textBaseline: 'middle',
        color: 'green',
        offset: { x: 10, y: 0 }
    }).draw();

    feature.style('fillColor', 'red')
        .style({
            'strokeColor': 'black',
            'strokeWidth': 5
        })
        .draw();

};


function select() {
    var i = document.getElementById("concities").value;
    var Nlat = lat[Number(i)];
    var Nlon = lon[Number(i)];
    var dptos = Dpto[Number(i)];
    var Nom = String(NomC[i]);
    var popul = new Intl.NumberFormat().format(populat[Number(i)]);

    // temp

    var owAppId = "20da860edb90c7fc86537181df2428de";

    var tlat = Nlat;
    var tlon = Nlon;
    var url = "http://api.openweathermap.org/data/2.5/weather?lat=" + tlat + "&lon=" + tlon + "&units=metric&APPID=" + owAppId;
    //para el servidor se debe colocar https 
    
    fetch(url).then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById("temp").innerText = 'Temp.: ' + data.main.temp + " °C";
            document.getElementById("hum").innerText = 'Humidity: ' + data.main.humidity + " %";
        });


    //City data
    document.getElementById("mpio").innerText = Nom;
    document.getElementById("dpto").innerText = 'Estate: ' + dptos;
    document.getElementById("popul").innerText = 'Population: ' + popul;
    document.getElementById("ncity").innerText = 'City: ';


    var cities = [{ lon: Nlon, lat: Nlat, name: Nom, population: 'Population: ' + popul }]

    var map = geo.map({
        node: "#map",
        center: { x: Nlon, y: Nlat },
        zoom: 7
    });

    map.createLayer('osm');

    var layer = map.createLayer('feature', { features: ['point'] });
    var feature = layer.createFeature('point')
        .data(cities)
        .position(function (city) {
            return {
                x: city.lon,
                y: city.lat
            };
        })
        .draw();

    var textLayer = map.createLayer('feature', { features: ['text'] });
    var textFeature = textLayer.createFeature('text')
        .data(cities)
        .position(function (city) {
            return {
                x: city.lon,
                y: city.lat
            };
        })
        .text(function (city) {
            return city.name;
        })
        .draw();


    textFeature.style({
        fontSize: '18px',
        fontFamily: 'tahoma',
        textAlign: 'left',
        textBaseline: 'middle',
        color: 'green',
        offset: { x: 10, y: 0 }
    }).draw();

    feature.style('fillColor', 'red')
        .style({
            'strokeColor': 'black',
            'strokeWidth': 5
        })
        .draw();

};