window.addEvent('domready', function(){

    /**********************************
     * Composer switcher code
     **********************************/

    var currentComposer = $('shareText');
    var currentComposerTab = $$('div#composer .tabs li')[0];

    $$('div#composer ul.tabs li').each(function(el){
        
        el.addEvent('click', function(){
            
            currentComposerTab.removeClass('toggled');
            currentComposerTab = el;
            currentComposerTab.addClass('toggled');
            
            currentComposer.removeClass('toggled');
            currentComposer = $(el.title);
            currentComposer.addClass('toggled');
            
        });
        
    });
    
    
    /**********************************
     * Avatar uploader
     **********************************/
    
    
    
});