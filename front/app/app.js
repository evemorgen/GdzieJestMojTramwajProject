var app = angular.module('projectMiss', ['checkCtrl', 'googleMaps', 'ngMap']);


app.run(function($http, $rootScope) {
    $http.get('../app/config.json').then(function(response) {
        $rootScope.config = response.data;
        console.log($rootScope.config);
    });
});
