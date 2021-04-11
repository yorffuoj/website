var mymap = L.map('mapid').setView([43.6118, 1.4465], 15);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

{% for station in stations %}
    var status;
    {% if station.status == 'OPEN' %}
        status = "<span class=\"badge badge-pill badge-success float-right\">Ouverte</span>";
    {% else %}
        status = "<span class=\"badge badge-pill badge-danger float-right\">Fermée</span>";
    {% endif %}

    var available_bikes_icon = "";
    {% if station.available_bikes == 0 %}
        available_bikes_icon = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-x-circle-fill text-danger\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" style=\"overflow: visible\">\
            <path fill-rule=\"evenodd\" d=\"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z\"/>\
        </svg>"
    {% elif station.available_bikes <= 5 %}
        available_bikes_icon = "<svg width=\"1.0625em\" height=\"1em\" viewBox=\"0 0 17 16\" class=\"bi bi-exclamation-triangle-fill text-warning\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" style=\"overflow: visible\">\
            <path fill-rule=\"evenodd\" d=\"M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 5zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z\"/>\
        </svg>"
    {% else %}
        available_bikes_icon = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-check-circle-fill text-success\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" style=\"overflow: visible\">\
            <path fill-rule=\"evenodd\" d=\"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z\"/>\
        </svg>"
    {% endif %}
    var available_bikes = available_bikes_icon + " {{ station.available_bikes }} vélouses dispos";

    var available_bike_stands_icon = "";
    {% if station.available_bike_stands == 0 %}
        available_bike_stands_icon = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-x-circle-fill text-danger\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" style=\"overflow: visible\">\
            <path fill-rule=\"evenodd\" d=\"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z\"/>\
        </svg>"
    {% elif station.available_bike_stands <= 5 %}
        available_bike_stands_icon = "<svg width=\"1.0625em\" height=\"1em\" viewBox=\"0 0 17 16\" class=\"bi bi-exclamation-triangle-fill text-warning\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" style=\"overflow: visible\">\
            <path fill-rule=\"evenodd\" d=\"M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 5zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z\"/>\
        </svg>"
    {% else %}
        available_bike_stands_icon = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-check-circle-fill text-success\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" style=\"overflow: visible\">\
            <path fill-rule=\"evenodd\" d=\"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z\"/>\
        </svg>"
    {% endif %}
    var available_bike_stands = available_bike_stands_icon + " {{ station.available_bike_stands }} bornes libres";

    var info_button = "<a href=\"{% url 'velose:detail' station.number %}\">Informations</a>";

    var add_button = "<a href=\"{% url 'velose:add_numb' station.number %}\">Ajouter la station</a>";

    L.marker([{{ station.position.lat }}, {{ station.position.lng }}])
        .bindPopup("<strong>{{ station.name }}</strong><br>\
                    Station {{ station.number }}" + status + "<br>" +
                    available_bikes + "<br>" +
                    available_bike_stands + "<br>" +
                    info_button + "<br>" +
                    add_button)
        .addTo(mymap);
{% endfor %}

mymap.on('click', onMapClick);
