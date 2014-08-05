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

    var kelly = ['kelly00', 'kelly01', 'kelly02', 'kelly03',
                 'kelly04', 'kelly05', 'kelly06', 'kelly07',
                 'kelly08', 'kelly09', 'kelly10', 'kelly11',
                 'kelly12', 'kelly13', 'kelly14', 'kelly15',
                 'kelly16', 'kelly17', 'kelly18', 'kelly19'];

    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {

        var margin = {top: 30, right: 30, bottom: 30, left: 30};
        var height = 100;
        var width = 1200;//parseInt(d3.select('#chart').style('width'), 10);
        var width = width - margin.left - margin.right;

        var applications =  d3.keys(d3.nest()
          .key(function(d) { return d.application; })
          .map(scope.data));

        var svg = d3.select(element[0])
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        d = new Date(scope.data[0].start)
        var xScale = d3.time.scale()
          .range([0,width])
          .domain([
            new Date(d.getFullYear(), d.getMonth(), d.getDate()),
            new Date(d.getFullYear(), d.getMonth(), d.getDate()+1)])



        var xAxis = d3.svg.axis().scale(xScale)
          .ticks(d3.time.hours, 1)
          .tickFormat(d3.time.format('%H'));



        svg.append("rect")
          .attr("x", 0)
          .attr("y", .5)
          .attr("width", "500px")
          .attr("height", 1)
          .attr("fill", "#CCCCCC")

        svg.selectAll("rect")
          .data(scope.data)
          .enter()
          .append("rect")
          .attr("x", function(d){ return xScale(new Date(d.start)) })
          .attr("y", 0)
          .attr("width", function(d){
            return xScale(new Date(new Date(d.start).setSeconds(new Date(d.start).getSeconds() + d.duration))) - xScale(new Date(d.start))
          })
          .attr("height", height)
          .attr("class", function(d){return kelly[applications.indexOf(d.application)]})
          .append("title").text(function(d){ return d.application })

        svg.append("g")
          .attr("class", "axis x-axis")
          .call(xAxis.orient('top'))

        scope.render = function(data) {



        };

        scope.$watch('data', function(){
          scope.render(scope.data);
        }, true);
      }
    }
  }])
