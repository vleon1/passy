import jQuery from 'jquery'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import Clipboard from 'clipboard'

export function fillPassword(url, id_postfix) {
    jQuery.getJSON(url, (data) => {
        setPassword(data, id_postfix);
    });

    function setPassword(data, id_postfix) {
        const getButton = jQuery('#get' + id_postfix)[0];
        const copyButton = jQuery('#copy' + id_postfix)[0];

        getButton.style.visibility = 'hidden';
        getButton.style.display = 'none';

        copyButton.setAttribute('data-clipboard-text', data.password.toString());
        copyButton.style.visibility = 'visible';
    }
}

export function initClipboard()
{
    // Tooltip
    jQuery('[id^=copy]').tooltip({
      trigger: 'click',
      placement: 'bottom'
    });

    function setTooltip(button, message) {
        jQuery(button).tooltip('hide').attr('data-original-title', message).tooltip('show');
    }

    function hideTooltip(button) {
        setTimeout(function() {
            jQuery(button).tooltip('hide');
        }, 1000);
    }

    // Clipboard
    const clipboard = new Clipboard('.btn');

    clipboard.on('success', function(e) {
        setTooltip(e.trigger, 'Copied!');
        hideTooltip(e.trigger);
    });
    clipboard.on('error', function(e) {
        setTooltip(e.trigger, 'Press Ctrl-C to copy');
        hideTooltip(e.trigger);
    });
}
