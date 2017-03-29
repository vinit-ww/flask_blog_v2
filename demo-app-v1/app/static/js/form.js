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
		 	url: 'http://127.0.0.1:5000/posts',
		 	headers: {
		   	'Content-Type': 'application/json',
		  },
		  	data: { title: $scope.title,content: $scope.content,author: $scope.author },
		}
		$http(req).then(function(response) {
			var form = document.getElementById("myForm");
			form.reset();
	        alert.log(response.data);
	    });
		//end request

  }
});
