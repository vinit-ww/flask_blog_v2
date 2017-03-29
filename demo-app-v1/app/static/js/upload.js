var app = angular.module('myApp', [])
		.run(['$http', function($http) {
		  $http.defaults.headers.post['X-CSRFToken'] = document.getElementsByName('csrf-token')[0].content
		}]);

//form validation
app.controller("myCtrl", function($scope,$http) {
  	$scope.myFunc = function () {
  		//start request
		var req = {
		 	method:'POST',
		 	url: 'http://localhost:5000/upload',
		 	headers: {
		   	'Content-Type': 'multipart/form-data',
		   	'Access-Control-Allow-Origin: *',
		  },
		  	data: { file: $scope.file},
		}
		$http(req).then(function(response) {
		    alert.log(response.data);
	    });
		//end request

  }
});
