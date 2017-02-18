function FillPassword(url, id_postfix) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            setPassword(httpRequest.responseText, id_postfix);
        }
    };
    httpRequest.open("GET", url, true); // true for asynchronous
    httpRequest.setRequestHeader("Accept", "application/json");
    httpRequest.send();
}

function setPassword(data_as_string, id_postfix) {
    var getButton = $('#get' + id_postfix)[0];
    var copyButton = $('#copy' + id_postfix)[0];

    getButton.style.visibility = 'hidden';
    getButton.style.display = 'none';

    copyButton.setAttribute('data-clipboard-text', JSON.parse(data_as_string).password.toString());
    copyButton.style.visibility = 'visible';
}

function initClipboard()
{
    // Tooltip
    $('[id^=copy]').tooltip({
      trigger: 'click',
      placement: 'bottom'
    });

    function setTooltip(btn, message) {
        $(btn).tooltip('hide').attr('data-original-title', message).tooltip('show');
    }

    function hideTooltip(btn) {
        setTimeout(function() {
            $(btn).tooltip('hide');
        }, 1000);
    }

    // Clipboard
    var clipboard = new Clipboard('.btn');

    clipboard.on('success', function(e) {
        setTooltip(e.trigger, 'Copied!');
        hideTooltip(e.trigger);
    });
    clipboard.on('error', function(e) {
        setTooltip(e.trigger, 'Press Ctrl-C to copy');
        hideTooltip(e.trigger);
    });
}
