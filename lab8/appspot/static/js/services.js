angular.service('Wine', function ($resource) {
    return $resource('/wines/:wineId', {}, {
        update: {method: 'PUT'}
    });
});
