var app = angular.module('checkCtrl', []);
app.config(['$httpProvider', function($httpProvider) {
            $httpProvider.defaults.useXDomain = true;
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
            }
]);



app.controller('backendTests', function($scope, $rootScope, $http){
    $scope.healthcheckResult = {};
    $scope.healthcheckResult.status = 'None';
    $scope.healthcheckResult.number = 'None';

    $scope.healthcheck = function() {
        $http({
            url: $rootScope.config.url + '/healthcheck',
            method: 'post',
            }).then(function(response){
                $scope.healthcheckResult = response.data;
        });
    };

    $scope.getstatus = function(logsAmount) {
        $http.post(
            $rootScope.config.url + '/mpk_db/get_status',
            {number: parseInt(logsAmount)}
        ).then(function(res){
            $scope.logs = res.data.status;
        });
    };
});
