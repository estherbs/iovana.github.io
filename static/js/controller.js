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
}

    $(document).ready(function(){
        setInterval(checkUrlEntered(), 17);
    });
