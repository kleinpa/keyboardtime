/*global angular, d3, window*/
(function () {
  'use strict';

  angular.module('metrics', [])
    .controller('CtrlMetrics', function ($scope, $http, $interval) {
      $http.get('/info').success(function (x) { $scope.info = x; });

      function refreshData() {
        $http.get('/data').success(function (x) {
          $scope.data = x;


          $scope.by_day = d3.nest()
            .key(function (x) {
              var d = new Date(x.start);
              return new Date(d.getFullYear(), d.getMonth(), d.getDate()).toISOString();
            })
            .sortKeys(d3.descending)
            .entries(x);

          //$interval(refreshData, 100, 1);
        });
      }
      refreshData();
    })
    .factory('chartColors', function () {
      var color_classes = [
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
      var cache = d3.map();
      var counter = 0;

      return function (name) {
        if (!cache.has(name)) {
          cache.set(name, color_classes[counter++]);
        }
        return cache.get(name);
      };
    })
    .directive('dayTimeline', ['chartColors', function (chartColors) {
      return {
        restrict: 'E',
        scope: {
          data: '=',
        },
        link: function (scope, element) {

          var margin = {top: 30, right: 5, bottom: 10, left: 5};
          var height = 100;
          var width;

          var svg = d3.select(element[0])
            .append("svg")
            .attr("height", height + margin.top + margin.bottom);

          var chart = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
          var axis_group = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          var d = new Date(scope.data[0].start);
          var xScale = d3.time.scale()
            .domain([
              new Date(d.getFullYear(), d.getMonth(), d.getDate(), 8, 30),
              new Date(d.getFullYear(), d.getMonth(), d.getDate(), 18, 30)]);

          var xAxis = d3.svg.axis()
            .orient('top')
            .scale(xScale)
            .ticks(d3.time.hours, 1)
            .tickFormat(d3.time.format('%H'));

          function render_data(data) {
            chart.selectAll(".bar").remove();

            var bars = chart.selectAll(".bar").data(data).enter()
              .append("g").attr("class", "bar")
              .attr("transform", function (d) { return "translate(" + xScale(new Date(d.start)) + ",0)"; });

            bars.append("rect")
              .attr("width", function (d) {
                return xScale(new Date(0, 0, 0, 0, 0, d.duration)) - xScale(new Date(0, 0, 0, 0, 0, 0));
              })
              .attr("height", height)
              .attr("class", function (d) {return chartColors(d.application); });

            bars.append("title").text(function (d) { return d.application; });
          }

          function update_width() {
            width = svg.node().parentNode.offsetWidth - margin.left - margin.right;
            svg.attr("width", width + margin.left + margin.right);
            xScale = xScale.range([0, width]);

            axis_group.selectAll(".axis").remove();
            axis_group.append("g")
              .attr("class", "axis x-axis")
              .call(xAxis);

            render_data(scope.data);
          }

          update_width();
          window.addEventListener('resize', update_width);

          scope.$watch('data', function () {
            render_data(scope.data);
          }, true);
        }
      };
    }])
    .directive('dayPercentbar', ['chartColors', function (chartColors) {
      return {
        restrict: 'E',
        scope: {
          data: '='
        },
        link: function (scope, element) {
          var margin = {top: 0, right: 5, bottom: 0, left: 5};
          var height = 20;

          var svg = d3.select(element[0])
            .append("svg")
            .attr("class", "dayPercentBar")
            .attr("height", height + margin.top + margin.bottom);

          var chart = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          var xScale = d3.scale.linear();

          function render_data(data) {
            var applications = d3.nest()
              .key(function (d) { return d.application; })
              .rollup(function (ds) { return {duration: d3.sum(ds, function (d) {return d.duration; }) }; })
              .entries(data);

            var total = d3.sum(applications, function (d) { return d.values.duration; });
            xScale.domain([0, total]);

            applications = applications.sort(function (a, b) { return b.values.duration - a.values.duration; });

            var sum = 0;
            applications.forEach(function (d) {
              d.values.prev = sum;
              sum += d.values.duration;
            });

            var bars = chart.selectAll("g").remove();
            bars = chart.selectAll("g").data(applications).enter()
              .append("g")
              .attr("transform", function (d) { return "translate(" + xScale(d.values.prev) + ",0)"; });

            bars.append("rect")
              .attr("width", function (d) { return xScale(d.values.duration); })
              .attr("height", height)
              .attr("class", function (d) {return chartColors(d.key); });

            bars.append("title").text(function (d) { return d.key; });
            bars.append("text")
              .attr("x", 1.5)
              .attr("y", height - 3)
              .text(function (d) { return d.key; });
          }

          function update_width() {
            var width = svg.node().parentNode.offsetWidth - margin.left - margin.right;
            svg.attr("width", width + margin.left + margin.right);
            xScale = xScale.range([0, width]);

            render_data(scope.data);
          }

          update_width();
          window.addEventListener('resize', update_width);

          scope.$watch('data', function () {
            //render_data(applications);
          }, true);
        }
      };
    }]);
}());
