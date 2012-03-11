var Calc;
Calc = (function () {
    //first percentage 5%, second percentage 10%
    var fstMark = 5, sndMark = 10, totalCost, discountAmt;
    var defaultUrl = 'http://localhost/post/', defaultTime = 5, timer;
    var result, live = false ; // set to true if server is on

    /* private functions */

    //function to calculate discount
    var calcDiscount = function (cost) {
        if (cost >= 5000 && cost <= 9999)
            return (cost / 100) * fstMark;
        else if (cost >= 10000)
            return (cost / 100) * sndMark;
    };

    // save results to localStorage and sync all result in storage
    var saveResult = function (result) {
        localStorage.setItem('rs_' + rand(), result);

	// smart sync is disabled because no web server exists
	// set live = true & update link if server is present
        if (navigator.onLine && live) {
            smartSync(defaultTime, successCallback)
        }
    };

    // random function is used to generate a unique name for the keys saved in localStorage
    var rand = function () {
        // simple javascript random guid function
	return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    };

    var successCallback = function () {
        timer = null; // clear the timer object
        console.log("Success : Data successfully synced " + new Date().getDate());
        // might want to clear localStorage after the records have been synced
        //localStorage.clear();
    };


    //smart sync can synchronize the currently saved result with the server  \
    // sec - delay time to run sync (in seconds)
    // callback - function to execute after the sync has been completed
    var smartSync = function (sec, callback) {

        //if the timer is not null, which means the sync is not yet complete
        //clear the timer and recreate the timer object adding any new value
        //that might have been added to localStorage
        //nb : reduce the amount of server syncs aka smart sync
        if (timer != null)
            clearTimeout(timer);

        timer = setTimeout(doSync({
            url:defaultUrl,
            data:getResultsJson(),
            success:callback}), 1000 * sec);
    };

    // gets the results from localStorage in JSON format
    var getResultsJson = function() {

        var aResults = {};

        //iterate through the localStorage keys
        for(key in localStorage) {
            aResults[key] = localStorage[key];
        }
        return aResults;
    };

    //ajax method for syncing data with the server
    var doSync = function (obj) {
        $.ajax({
            type:'POST',
            url:obj.url,
            data:obj.data,
            success:obj.success,
            dataType:'json'
        });
    };

    return {
        //function to calculate total cost of tickets
        calculateCost:function () {

            $('#display').val(""); //clear display
            totalCost = ($('#txtAdultCount').val() * 1000) + ($('#txtChildCount').val() * 500);
            discountAmt = (totalCost < 5000) ? 0 : calcDiscount(totalCost);
            result = totalCost + discountAmt;
            $('#total').val(result);

            if (totalCost >= 9500 && totalCost < 10000) {
                $('#display').val('Purchases over $10,000 gives you a 10% discount!');
                return;
            }
        },
        persist:function () {
            if ($('#total').val() > 0) {
                saveResult($('#total').val());
                alert('Result saved!'); //callback ?? \

                //reset the page
                $('#txtChildCount, #txtAdultCount, #total').val(0);
            }
            else alert('Empty!');
        }

    }
})();

// The following function updates the application cache if any files have been changed since the last update
// Sourced from : http://www.html5rocks.com/en/tutorials/appcache/beginner/
window.applicationCache.addEventListener('updateready', function (e) {
    if (window.applicationCache.status == window.applicationCache.UPDATEREADY) {
        window.applicationCache.swapCache();
        window.location.reload();
    }
}, false);
