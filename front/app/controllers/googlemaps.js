var app = angular.module('googleMaps', ['uiGmapgoogle-maps']);

app.config(
['uiGmapGoogleMapApiProvider', function(GoogleMapApiProviders) {
        GoogleMapApiProviders.configure({
        key: 'AIzaSyAaXG_f0jhDrRp2Y0o5AUvTnlaaaW_7apI',
        v: '3', //defaults to latest 3.X anyhow
        libraries: 'weather,geometry,visualization'

        });
    }]
);

app.controller('mapMagic', function($scope, $rootScope, $http){
    $scope.map = { center: { latitude: 50.062334, longitude: 19.937002 }, zoom: 12, markers: []};
    $scope.stops = {}
    $http({
        //url: $rootScope.config.url + '/graph_api/get_all_stops',
        url: 'http://0.0.0.0:8888/graph_api/get_all_stops',
        method: 'post',
    }).then(function(response){
        var stops = response.data.data;
        for(var stop in stops) {
            if(stops.hasOwnProperty(stop)){
                var marker = {
                    id: stop,
                    coords: {
                        latitude: stops[stop].x,
                        longitude: stops[stop].y
                    },
                    icon: {url: 'http://i.imgur.com/REfIpfW.png'},
                    options: {
                        title: stop,
                    }
                }
                $scope.map.markers.push(marker);
            }
        }
        console.log($scope.map.markers)
    });

    console.log($scope.map.markers);
});
