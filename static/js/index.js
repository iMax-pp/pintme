window.addEvent('domready', function(){

    /**********************************
     * Composer switcher code
     **********************************/

    var currentComposer = 'text';
    if( window.location.hash != '' )
    {
        var hash = window.location.hash;
        var currentComposer = hash.substring(1);
    }

    $('share'+currentComposer).setStyle('visibility', 'visible');

    $$('#post-choice-menu ul li a').each(function(el){
        el.addEvent('click', function(){
            $('share'+currentComposer).setStyle('visibility', 'hidden');
            currentComposer = el.rel;
            $('share'+currentComposer).setStyle('visibility', 'visible');
        });
    });

    $('textedit').mooEditable();
    $('quoteedit').mooEditable();
    $('sourceedit').mooEditable();
    $('descedit').mooEditable();
    $('captionedit').mooEditable();
    $('quoteedit').mooEditable();
    $('descedit2').mooEditable();

});
