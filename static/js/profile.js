window.addEvent('domready', function(){
    
    /**********************************
     * Avatar uploader
     **********************************/

	var link = $('change-avatar');
	var linkIdle = link.get('html');

	function linkUpdate() {
		if (!swf.uploading) return;
		var size = Swiff.Uploader.formatUnit(swf.size, 'b');
		link.set('html', '<span class="small">' + swf.percentLoaded + '% of ' + size + '</span>');
	}
    
    function avatarUpdate() {
        $$('img.avatar-small', 'img.avatar-normal').each(function(el){
        });
    }

	// Uploader instance
	var swf = new Swiff.Uploader({
		path: '/swiff/Swiff.Uploader.swf',
		url: '/account/avatar/' + link.rel,
		verbose: false,
		queued: false,
		multiple: false,
		target: link,
		instantStart: true,
		typeFilter: {
			'Images (*.jpg, *.jpeg, *.gif, *.png)': '*.jpg; *.jpeg; *.gif; *.png'
		},
		fileSizeMax: 1024 * 1024,
		onSelectSuccess: function(files) {
            //alert('Starting Upload', 'Uploading <em>' + files[0].name + '</em> (' + Swiff.Uploader.formatUnit(files[0].size, 'b') + ')');
			this.setEnabled(false);
		},
		onSelectFail: function(files) {
			//alert('<em>' + files[0].name + '</em> was not added!', 'Please select an image smaller than 2 Mb. (Error: #' + files[0].validationError + ')');
		},
		onQueue: linkUpdate,
		onFileComplete: function(file) {
			file.remove();
 			this.setEnabled(true);
		},
		onComplete: function() {
            avatarUpdate();
			link.set('html', linkIdle);
		}
	});

	// Button state
	link.addEvents({
		click: function() {
			return false;
		},
		mouseenter: function() {
			this.addClass('hover');
			swf.reposition();
		},
		mouseleave: function() {
			this.removeClass('hover');
			this.blur();
		},
		mousedown: function() {
			this.focus();
		}
	});	
});