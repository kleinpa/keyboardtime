angular.module('metrics', []).
controller('CtrlMetrics', function($scope, $http, $interval){
  function refreshData(){
    $http.get('/data').success(function(x){
      $scope.data = x;


      $scope.by_day =
        d3.nest()
          .key(function(x) {
            var d = new Date(x.start);
            return new Date(d.getFullYear(), d.getMonth(), d.getDate()).toISOString();
          })
          .sortKeys(d3.descending)
          .entries(x);


      $interval(refreshData, 100, 1)
    });
  }
  refreshData();
}).
directive( 'dayBar', [
  function () {
    // Kelly's 22 colors of maximum contrast
    var kelly = ['#FFB300', '#803E75', '#FF6800', '#A6BDD7',
                 '#C10020', '#CEA262', '#817066', '#007D34',
                 '#F6768E', '#00538A', '#FF7A5C', '#53377A',
                 '#FF8E00', '#B32851', '#F4C800', '#7F180D',
                 '#93AA00', '#593315', '#F13A13', '#232C16'];

    function decimalDay(d){
      return (
        d.getMilliseconds()/86400000 +
        d.getSeconds()/86400 +
        d.getMinutes()/1440 +
        d.getHours()/24)

    }

    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {

        var applications =  d3.keys(d3.nest()
          .key(function(d) { return d.application; })
          .map(scope.data));

        var svg = d3.select(element[0])
        .append("svg")
        .attr('width', '100%')
        .attr('height', '160px')
        //.attr('viewBox', '.3 0 .4 1')
        .attr('viewBox', '0 0 1 2')
        .attr('preserveAspectRatio', 'none')

        svg.append("rect")
          .attr("x", 0)
          .attr("y", 0)
          .attr("width", 1)
          .attr("height", 1)
          .attr("fill", "#CCCCCC")

        svg.selectAll("rect")
          .data(scope.data)
          .enter()
          .append("rect")
          .attr("x", function(d){ return decimalDay(new Date(d.start)) })
          .attr("y", 0)
          .attr("width", function(d){return d.duration/86400})
          .attr("height", function(d){return 1+(d.activeness/20)})
          .attr("fill", function(d){return kelly[applications.indexOf(d.application)]})
          .append("title").text(function(d){ return d.application })

        scope.render = function(data) {



        };

        scope.$watch('data', function(){
          scope.render(scope.data);
        }, true);
      }
    }
  }])
