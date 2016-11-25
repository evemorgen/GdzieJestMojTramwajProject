var app = angular.module('checkCtrl', []);
app.config(['$httpProvider', function($httpProvider) {
            $httpProvider.defaults.useXDomain = true;
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
            }
]);
app.controller('check', function($scope, $http){
    $scope.test = {};
    $scope.test.status = 'None';
    $scope.test.number = 'None';

    $scope.healthcheck = function() {
        console.log('healthcheck');
        $http({
            url: 'http://192.168.1.123:8888/healthcheck',
            method: 'post',
            }).then(function(response){
            console.log(response);
            $scope.test = response.data;
        });
    };
    $scope.getstatus = function(logsAmount) {
        console.log('status');
        $http.post(
            'http://192.168.1.123:8888/mpk_db/get_status',
            {number: parseInt(logsAmount)}
        ).then(function(res){
            $scope.logs = res.data.status;
        });
    };
});


