angular.module('metrics', []).
controller('CtrlMetrics', function($scope, $http, $interval){
  $http.get('/info').success(function(x){ $scope.info = x });

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


      // $interval(refreshData, 100, 1)
    });
  }
  refreshData();
})
.factory('ChartColors', function(){
    color_classes = [
        'fill00', 'fill01', 'fill02', 'fill03',
        'fill04', 'fill05', 'fill06', 'fill07',
        'fill08', 'fill09', 'fill10', 'fill11',
        'fill12', 'fill13', 'fill14', 'fill15',
        'fill16', 'fill17', 'fill18', 'fill19',
        'fill20', 'fill21', 'fill22', 'fill23',
        'fill24', 'fill25', 'fill26', 'fill27',
        'fill28', 'fill29', 'fill30', 'fill31',
        'fill32', 'fill33', 'fill34', 'fill35',
        'fill36', 'fill37', 'fill38', 'fill39'];
    cache = d3.map()
    counter = 0;

    return function(name){
      if (!cache.has(name)){
        cache.set(name, color_classes[counter++]);
      }
      return cache.get(name)
    }
  })
.directive('dayTimeline', ['ChartColors', function (ChartColors) {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {

        var margin = {top: 30, right: 5, bottom: 10, left: 5};
        var height = 100;
        var width = 1200;//parseInt(d3.select('#chart').style('width'), 10);
        var width = width - margin.left - margin.right;

        var applications = 
          d3.nest()
            .key(function(d) { return d.application; })
            .map(scope.data);

        var application_list = d3.keys(applications);

        var svg = d3.select(element[0])
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom);

        var chart = svg.append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var axis_group = svg.append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        d = new Date(scope.data[0].start)
        var xScale = d3.time.scale()
          .domain([
            new Date(d.getFullYear(), d.getMonth(), d.getDate(), 8, 30),
            new Date(d.getFullYear(), d.getMonth(), d.getDate(), 18, 30)])

        var xAxis = d3.svg.axis()
          .orient('top')
          .scale(xScale)
          .ticks(d3.time.hours, 1)
          .tickFormat(d3.time.format('%H'));

        function update_width(){
          width = svg.node().parentNode.offsetWidth - margin.left - margin.right
          svg.attr("width", width + margin.left + margin.right)
          xScale = xScale.range([0,width])
          
          axis_group.selectAll(".axis").remove()
          axis_group.append("g")
            .attr("class", "axis x-axis")
            .call(xAxis)

          render_data(scope.data)
        }

        function render_data(data) {
          chart.selectAll(".bar").remove()

          bars = chart.selectAll(".bar").data(data).enter()
            .append("g").attr("class", "bar")
            .attr("transform", function(d, i) { return "translate(" + xScale(new Date(d.start)) + ",0)"; });

          bars.append("rect")
            .attr("width", function(d){
              return xScale(new Date(new Date(d.start).setSeconds(new Date(d.start).getSeconds() + d.duration))) - xScale(new Date(d.start))
            })
            .attr("height", height)
            .attr("class", function(d){return ChartColors(d.application)})

            bars.append("title").text(function(d){ return d.application })
        };

        update_width();
        window.addEventListener('resize', update_width); 

        scope.$watch('data', function(){
          //render_data(scope.data);
        }, true);
      }
    }
  }])
.directive('dayPercentbar', ['ChartColors', function (ChartColors) {
    return {
      restrict: 'E',
      scope: {
        data: '='
      },
      link: function (scope, element) {

        var margin = {top: 0, right: 5, bottom: 0, left: 5};
        var height = 20;
        var width = 1200;//parseInt(d3.select('#chart').style('width'), 10);
        var width = width - margin.left - margin.right;

        var applications = 
          d3.nest()
            .key(function(d) { return d.application; })
            .rollup(function(ds) { return {duration: d3.sum(ds, function(d){return d.duration})};})
            .entries(scope.data);

        var application_list = d3.keys(applications);

        var total = d3.sum(applications, function(d){ return d.values.duration; });


        applications = applications.sort(function(a,b) { return b.values.duration - a.values.duration});

        sum = 0;
        applications.forEach(function(d,i){
          d.values.prev = sum;
          sum += d.values.duration;
        });

        var svg = d3.select(element[0])
          .append("svg")
          .attr("class", "dayPercentBar")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom);

        var chart = svg.append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        d = new Date(scope.data[0].start)
        var xScale = d3.scale.linear()
          .domain([0, total])

        function update_width(){
          width = svg.node().parentNode.offsetWidth - margin.left - margin.right
          svg.attr("width", width + margin.left + margin.right)
          xScale = xScale.range([0,width])

          render_data(applications)
        }

        function render_data(data) {
          bars = chart.selectAll("g").remove()
          bars = chart.selectAll("g").data(data).enter()
            .append("g")
            .attr("transform", function(d, i) { return "translate(" + xScale(d.values.prev) + ",0)"; });
            //.attr("width", function(d){ return xScale(d.values.duration); })

          bars.append("rect")
            //.attr("x", function(d){ return xScale(d.values.prev); })
            //.attr("y", 0)
            .attr("width", function(d){ return xScale(d.values.duration); })
            .attr("height", height)
            .attr("class", function(d){return ChartColors(d.key); });
          
          bars.append("title").text(function(d){ return d.key; });
          bars.append("text")
            .attr("x", 1.5)
            .attr("y", height - 3)
            .text(function(d){ return d.key; });
        };


        update_width();
        window.addEventListener('resize', update_width); 

        scope.$watch('data', function(){
          //render_data(applications);
        }, true);
      }
    }
  }])
var debounce = function(fn, timeout) 
{
  var timeoutID = -1;
  return function() {
    if (timeoutID > -1) {
      window.clearTimeout(timeoutID);
    }
    timeoutID = window.setTimeout(fn, timeout);
  }
};
