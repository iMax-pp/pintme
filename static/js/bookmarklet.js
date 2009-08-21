window.addEvent('domready', function(){

    var curTab = $$('ul#tabs li')[0];
    curTab.setStyles({
        'background-color': 'white',
        'border-color': 'white'
    });
    $(curTab.get('rel')).setStyle('visibility', 'visible');

    $$('ul#tabs li').each(function(el){
        el.addEvent('click', function(){
            curTab.setStyles({
                'background-color': 'silver',
                'border-color': '#1F1F1F'
            });
            $(curTab.get('rel')).setStyle('visibility', 'hidden');
            curTab = el;
            $(el.get('rel')).setStyle('visibility', 'visible');
            el.setStyles({
                'background-color': 'white',
                'border-color': 'white'
            });
        });
    });

    var curImage = null;
    $$('#content .imagebox img').each(function(el){
        var w = el.width, h = el.height;
        if( w * h < 2500 )
        {
            el.setStyle('display', 'none');
        }
        else
        {
            var aspect = w / h;
            if( aspect > 1 )
            {
                var scale = 80 / w;
            }
            else
            {
                var scale = 80 / h;
            }
            if( scale < 1 )
            {
                el.setStyles({
                    'width': w * scale,
                    'height': h * scale
                });
            }
        }
        el.addEvent('click', function(){
            if( curImage != null )
            {
                curImage.setStyle('border-color', 'white');
            }
            curImage = el;
            curImage.setStyle('border-color', '#995');
            $('imageurl').setProperty('value', curImage.getProperty('src'));
        });
    });

    $('textedit').mooEditable();
    $('sourceedit').mooEditable();
    $('descedit').mooEditable();
    $('captionedit').mooEditable();
    $('descedit2').mooEditable();

});
