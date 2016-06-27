/**
 * Created by Iovana on 18/06/2016.
 */

var slided = (function(){
    var slid = false;
    return {
        get : function() {
            return slid;
        },
        set : function(b) {
            slid = b;
        }
    };
})();

function pageDown() {
    if(!slided.get()) {
       var height = "-=" + $('#top').height() + "px";
        $('#top').animate({
            'top' : height
        }, 1000);
        $('#bottom').animate({
            'top' : height
        }, 1000);
        slided.set(true);
    }
}

function checkUrlEntered(){
    var urlEntered = $('#iovanaslide');
    if(urlEntered.html()==="url is valid"){
        pageDown();
    }
    var percent = $('#percentage_bar').html();
    // percent = (percent.trim) ? percent.trim() : percent.replace(/^\s+/,'');
    if(percent != ''){
        var x = parseFloat(percent);
        var yr = 255 + (0.875 * x) - (0.01575 * Math.pow(x, 2));
        var yg = 140 - (0.75 * x) - (0.0065 * Math.pow(x, 2));
        var mycolor = "rgb(" + parseInt(yr) + "," + parseInt(yg) + ",0)";
        $('#bottom').css("backgroundColor", mycolor);
    }
}

    $(document).ready(function(){
        setInterval(checkUrlEntered(), 17);
    });
