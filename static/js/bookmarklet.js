var win = open('', 'z', 'width=450,height=500');
var doc = win.document;

var selection = '';
if(window.getSelection){
    selection = window.getSelection();
}else if(document.getSelection){
    selection = document.getSelection();
}else if(document.selection){
    selection = document.selection.createRange().text;
}

var images = document.images;

body = "<b>" + document.title + "</b><i>(" + document.URL + "</i>";

if(selection != '')
{
    body += "<br/><b>You selected: </b><blockquote>&#8220" + selection + ";&#8221;</blockquote>"
}

body += "<br/>Page contains " + document.images.length + " images:<br/>";

for( var i = 0; i < images.length; i++ )
{
    body += '<img src="' + images[i].src + '" alt="' + images[i].alt + '" />';
}

doc.write('<html><head></head><body>' + body + '</body>');
