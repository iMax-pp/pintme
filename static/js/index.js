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
    $(currentComposer+'tab').setStyle('border-color', '#1F1F1F');


    var currentComposer = '';

    $$('#post-choice-menu ul li a').each(function(el){
        $('share'+el.rel).setStyle('opacity', 0);
        el.addEvent('click', function(e){
            e.stop();
            if( currentComposer != '' )
            {
                $('share'+currentComposer).morph({
                    'opacity': 0,
                    'display': 'none'
                });
                $(currentComposer+'tab').morph({
                    'border-color': '#FFFFFF'
                });
            }

            if( currentComposer != el.rel )
            {
                currentComposer = el.rel;
                $('share'+currentComposer).morph({
                    'opacity': 1,
                    'display': 'block'
                });
                $(currentComposer+'tab').morph({
                    'border-color': '#1F1F1F'
                });
            }
            else
            {
                currentComposer = '';
            }
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
