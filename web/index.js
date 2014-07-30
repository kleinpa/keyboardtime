angular.module('metrics', []).
  controller('CtrlMetrics', function($scope, $http, $interval){
    function refreshData(){
      $http.get('/data').success(function(x){
        $scope.data = x;
        $interval(refreshData, 100, 1)
      });
    }
    refreshData();
  })
