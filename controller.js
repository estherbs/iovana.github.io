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

function pageDown(event) {
    var key = event.keyCode;
    if(key == 13 && !slided.get()) {
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

    $(document).ready(function(){
        
    });
