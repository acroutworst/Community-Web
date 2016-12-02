/**
 * Created by Jessica on 12/1/16.
 */
//intialize the app
var app = angular.module('app', []);

//initialize the app controller
app.controller('MainCtrl', function($scope, $http) {

  //store the JSON URL
  var theUrl = "http://api.pugetsound.onebusaway.org/api/where/schedule-for-stop/1_76305.json?key=65f351d5-6625-4a62-af86-88c05ae26b54";

  //parse the JSON URL w/ jsonp and AJAX
  $.ajax({
    dataType: "jsonp",
    url: theUrl,
  }).done(function(data) {

    //define scopes for the JSON data
    $scope.data = data.data;
    $scope.currentTime = data.currentTime;


    //Binary Search Tree functions

    //Node struct
    function Node(desc, time, bus) {
      this.desc = desc;
      this.time = time;
      this.bus = bus;
      this.left = null;
      this.right = null;
    }

    //BSTree Constructor
    function BinarySearchTree() {
      this.root = null;
    }

    //BSTree Insert
    BinarySearchTree.prototype.push = function(desc, time, bus) {
      var root = this.root;
      var newNode = new Node(desc, time, bus);

      //if root is null, then create a new node at root
      if (root === null) {
        this.root = newNode;
        return;
      }

      //current and parent vars initialized to iterate thru BSTree and insert
      var current = root;
      var parent;
      while (true) {
        parent = current;
        if (time < current.time) {
          current = current.left;
          if (current === null) {
            parent.left = newNode;
            return;
          }
        } else {
          current = current.right;
          if (current === null) {
            parent.right = newNode;
            return;
          }
        }
      }
    }

    //create new BSTree var
    var bst = new BinarySearchTree();

    //intialize variables to hold desc, time, bus to be pushed into the BSTree
    var d, t, b;

    //loop through the stopRouteSchedules array in JSON
    for (var bus = 0; bus < $scope.data.entry.stopRouteSchedules.length; bus++) {
      //loop through the stopRouteDirectionSchedules array in JSON
      for (var dir = 0; dir <= 1; dir++) {
        //loop through the routes array in JSON
        for (var route = 0; route < $scope.data.entry.stopRouteSchedules[bus].stopRouteDirectionSchedules[dir].scheduleStopTimes.length; route++) {

          //if the arrivalTime is in the future, then convert it to minutes and store
          if ((($scope.data.entry.stopRouteSchedules[bus].stopRouteDirectionSchedules[dir].scheduleStopTimes[route].arrivalTime) - $scope.currentTime) > 0) {
            var timeConvert = TimeUnit.MILLIS.toMinutes((($scope.data.entry.stopRouteSchedules[bus].stopRouteDirectionSchedules[dir].scheduleStopTimes[route].arrivalTime) - $scope.currentTime));
            t = timeConvert;

            //compare the route# to match to shortName in JSON and store for bus route #
            for (var routeid = 0; routeid < $scope.data.references.routes.length; routeid++) {
              if (($scope.data.entry.stopRouteSchedules[bus].routeId) == ($scope.data.references.routes[routeid].id)) {
                b = $scope.data.references.routes[routeid].shortName;
              }
            }

            //store the tripHeadSign for description
            d = $scope.data.entry.stopRouteSchedules[bus].stopRouteDirectionSchedules[dir].tripHeadsign;

            //push node values into BSTree
            bst.push(d, t, b);
          }
        }
      }
    }

    //adds data into the "businfo" element id in html file
    var populate = document.getElementById("businfo");

    var finalForm = "";

    inorder(bst.root);
    //tree inorder function

    fill();

    function inorder(node) {
      if (node) {
        inorder(node.left);
        //console.log(node.bus + ", " + node.desc + ", " + node.time);
        finalForm += ("<tr><td>" + node.bus + "</td><td>" + node.desc + "</td><td>" + node.time + "</td></tr>");
        inorder(node.right);
      }
    }

    function fill() {
      populate.innerHTML += finalForm;
    }

  });


});