function(){
    var app = angular.module('checkCtrl', []);
    
    app.controller('check', function($scope, $http){
        $http.post(83.30.202.146:8888/healthcheck).then(function(response){
            $scope.test = response.data;
        };)
    };);
};
