window.addEvent('domready', function(){
    var curTab = $$('ul#tabs li')[0];
    $$('ul#tabs li').each(function(el){
        el.addEvent('click', function(){
            curTab.setStyle('background-color', 'silver');
            $(curTab.get('rel')).setStyle('display', 'none');
            curTab = el;
            $(el.get('rel')).setStyle('display', 'block');
            el.setStyle('background-color', 'white');
        });
    });
});
