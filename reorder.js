function reverse_lists() {
    var olists = document.getElementsByTagName('ol');
    for (var i = 0; i < olists.length; i++) {
        if (!olists[i].className.match(/\breversed\b/))
            continue;
        
        var offset = 0;
        // Check if list has non-1 starting value
        if (olists[i].hasAttribute('start')) {
            offset = parseInt(olists[i].getAttribute('start')) - 1;
        }
        var items = olists[i].getElementsByTagName('li');
        for(var j = 0; j < items.length; j++) {
            items[j].setAttribute("value", offset + items.length - j);
        }
    }
}