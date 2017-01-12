var app = angular.module('googleMaps', ['ngMap', 'angular-md5']);

app.controller('mapMagic2', function($scope, $rootScope, $http, md5, $interval, NgMap){
    $scope.mapCenter = [50.062334, 19.937002];
    $scope.mapZoom = 15;
    $scope.markery = [];
    $scope.krawedzie = [];
    $scope.trams = []
    $scope.getStops = function(endpoint, iconUrl) {
        $http({
            //url: $rootScope.config.url + '/graph_api/get_all_stops',
            url: 'http://0.0.0.0:8888/graph_api/' + endpoint,
            method: 'post',
        }).then(function(response){
            var stops = response.data.data;
            for(var stop in stops){
                if(stops.hasOwnProperty(stop)){
                    var latlng = new google.maps.LatLng(stops[stop].x, stops[stop].y);
                    var tmpMarker = new google.maps.Marker({
                        title: stop,
                        position: latlng,
                        map: $scope.map,
                        icon: iconUrl
                    });
                    $scope.markery.push(tmpMarker);
                };
            };
        });
    };

    $scope.showEdges = function(line){
        $http.post(
            'http://0.0.0.0:8888/graph_api/get_graph_edges',
            {'line': line}
        ).then(function(response){
            var edges = response.data.data;
            var color = '#' + (md5.createHash(line.toString())).substring(0,6);
            for(krawedz in $scope.krawedzie){
                if($scope.krawedzie.hasOwnProperty(krawedz)){
                    $scope.krawedzie[krawedz].setMap(null);
                }
            }
            $scope.krawedzie = []
            for(var edge in edges){
                    if(edges.hasOwnProperty(edge)){
                        var pin1 = new google.maps.LatLng(edges[edge][0][0].latitude, edges[edge][0][0].longitude)
                        var pin2 = new google.maps.LatLng(edges[edge][0][1].latitude, edges[edge][0][1].longitude)
                        var tmpPolyline = new google.maps.Polyline({
                            path: [pin1, pin2],
                            strokeColor: color,
                            visible: true,
                            map: $scope.map
                        });
                        $scope.krawedzie.push(tmpPolyline);
                    }
                }
            });
    };
    $scope.getTrams = function(line){
        $http.post(
            'http://0.0.0.0:8888/graph_api/get_trams',
            {'line': line}
        ).then(function(response){
            var trams = response.data.data;
            for(var tram in $scope.trams){
                if(trams.hasOwnProperty(tram)){
                    console.log($scope.trams)
                    $scope.trams[tram].setMap(null);
                };
            };
            $scope.trams = []
            for(var tram in trams){
                if(trams.hasOwnProperty(tram)){
                    $scope.createTram(trams[tram].line, {x: trams[tram].position.x, y: trams[tram].position.y});
                };
            };
        });
    };
    $scope.createTram = function(line, pos) {
        pos = new google.maps.LatLng(pos.x, pos.y);
        marker = new google.maps.Marker({
            title: line.toString(),
            position: pos,
            map: $scope.map,
            icon: '../statics/tram.png',
            zIndex: 999
        });
        $scope.trams.push(marker);
    };
    $scope.gen_map = function(){
        $scope.getStops('get_all_stops', '../statics/bus-stop-black.png');
        $scope.getStops('get_all_terminals', '../statics/bus-stop-red.png');
        $scope.getStops('get_all_crossings', '../statics/crossroads.png');
    };
    $scope.gen_edges = function() {
        var trams = [1, 2, 18, 20, 50, 69]
        var item = trams[Math.floor(Math.random()*trams.length)];
        $scope.showEdges(item);
    };
    $scope.get_new_trams = function(){
        $scope.getTrams(18);
    };
    $interval($scope.gen_map, 2000, 1);
    $interval($scope.gen_edges, 5000, 5);
    $interval($scope.get_new_trams, 10000);
});
