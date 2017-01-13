var app = angular.module('googleMaps', ['ngMap', 'angular-md5']);

app.controller('mapMagic2', function($scope, $rootScope, $http, md5, $interval, NgMap){
    $scope.mapCenter = [50.062334, 19.937002];
    $scope.mapZoom = 15;
    $scope.markery = [];
    $scope.krawedzie = [];
    $scope.trams = [];
    $scope.lastClicked = null;
    $scope.tramString = `
    <div id="infoWindow" >
        <h3>Hello from tram number: <b>%(name)s</b></h3>
        last stop: %(lastStop)s <br />
        next stop %(nextStop)s <br />
        velocity: %(velocity)skm/h <br />
        state: %(state)s <br />
        distance to next stop: %(distance)s m <br />
        last update: %(lastUp)s <br />
        <div id="infoWindowHandler"></<div>
    </div>  
    `
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

    $scope.clearEdges = function(){
        for(krawedz in $scope.krawedzie){
            if($scope.krawedzie.hasOwnProperty(krawedz)){
                $scope.krawedzie[krawedz].setMap(null);
            }
        }
        $scope.krawedzie = [];
    };

    $scope.showEdges = function(line){
        $http.post(
            'http://0.0.0.0:8888/graph_api/get_graph_edges',
            {'line': line}
        ).then(function(response){
            var edges = response.data.data;
            var color = '#' + (md5.createHash(line.toString())).substring(0,6);
            $scope.clearEdges();
            for(var edge in edges){
                    if(edges.hasOwnProperty(edge)){
                        var pin1 = new google.maps.LatLng(edges[edge][0][0].latitude, edges[edge][0][0].longitude)
                        var pin2 = new google.maps.LatLng(edges[edge][0][1].latitude, edges[edge][0][1].longitude)
                        var tmpPolyline = new google.maps.Polyline({
                            path: [pin1, pin2],
                            strokeColor: color,
                            strokeWeight: 2,
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
                    $scope.trams[tram].setMap(null);
                };
            };
            $scope.trams = []
            for(var tram in trams){
                if(trams.hasOwnProperty(tram)){
                    $scope.createTram(trams[tram].line, {x: trams[tram].position.x, y: trams[tram].position.y}, trams[tram]);
                };
            };
        });
    };
    $scope.createTram = function(line, pos, tramInfo) {
        pos = new google.maps.LatLng(pos.x, pos.y);
        marker = new google.maps.Marker({
            title: line.toString(),
            position: pos,
            map: $scope.map,
            icon: '../statics/bluetrain.png',
            zIndex: 999
        });
        marker.addListener('click', function(){
            if($scope.lastClicked == this.title){
                $scope.clearEdges();
                $scope.lastClicked = null;
            } else {
                var infobox = new google.maps.InfoWindow({
                    content: sprintf($scope.tramString, {
                        name: this.title,
                        lastStop: tramInfo.last_stop['name'],
                        nextStop: tramInfo.next_stop['name'],
                        velocity: tramInfo.velocity,
                        state: tramInfo.state,
                        distance: String(tramInfo.distance_to_go).substr(0, String(tramInfo.distance_to_go).indexOf(".")),
                        lastUp: tramInfo.last_update
                    })
                });
                infobox.open($scope.map, this);
                $scope.showEdges(this.title);
                $scope.lastClicked = this.title;
            }
        })
        $scope.trams.push(marker);
    };
    $scope.gen_map = function(){
        $scope.getStops('get_all_stops', '../statics/bus-stop-black.png');
        $scope.getStops('get_all_terminals', '../statics/stop.png');
        //$scope.getStops('get_all_crossings', '../statics/crossroads.png');
    };
    $scope.get_new_trams = function(){
        $scope.getTrams(18);
    };
    $interval($scope.gen_map, 2000, 1);
    $interval($scope.get_new_trams, 10000);
});
