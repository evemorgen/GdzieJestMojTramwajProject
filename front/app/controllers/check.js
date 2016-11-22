function(){
    var app = angular.module('checkCtrl', []);
    
    app.controller('check', function($scope, $http){
        $http.post(tu wywolaj ta funkcje bo nie wiem jak).then(function(response){
            $scope.test = response.data;
        };)
    };);
};
