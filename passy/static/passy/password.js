
function fillPassword(url, id_postfix) {

    jQuery.getJSON(url, function(data) {
        setPassword(data, id_postfix);
    });

    function setPassword(data, id_postfix) {
        const getButton = jQuery('#get' + id_postfix)[0];
        const copyButton = jQuery('#copy' + id_postfix)[0];

        const new_visibility = getButton.style.visibility;
        const new_display = getButton.style.display;

        getButton.style.visibility = 'hidden';
        getButton.style.display = 'none';

        copyButton.setAttribute('data-clipboard-text', data.stored_password_text);
        copyButton.style.visibility = new_visibility;
        copyButton.style.display = new_display;
    }
}

function filterPage(filterString) {

    var filterRegexString = filterString ? ".*" + filterString.split('').join(".*") + ".*": ".*";
    var filterRegex = new RegExp(filterRegexString, 'i');

    var rows = jQuery('#passwords_table').find('tbody').find('tr');
    rows.filter(function (index, element) {
       var siteName = getSiteName(element);
       return filterRegex.test(siteName);
    }).attr('style','display: ');
    rows.filter(function (index, element) {
       var siteName = getSiteName(element);
       return !filterRegex.test(siteName);
    }).attr('style','display: none');

    function getSiteName(element) {
        return jQuery(element).find("a[name=site_link]")[0].innerText
    }
}

function getPassword(form) {

    var url = form.action;
    var form_query = jQuery(form);
    var length = form_query.find("input[name=length]")[0].valueAsNumber;
    var use_symbols = form_query.find("input[name=use_symbols]")[0].checked;

    var stored_password_text_field = jQuery("input[name=stored_password_text]")[0];

    jQuery.getJSON(url, {length: length, use_symbols: use_symbols}, function(data) {
        stored_password_text_field.value = data['generated_password'];
    });
}

function confirmHiddenButtonClock(buttonId) {
    if (confirm("Are you sure?") == true){
       document.getElementById(buttonId).click();
    }
}

function initClipboard()
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

function initGetRandomPasswordForm() {
    // Overrides the get password button to call rest directly
    jQuery('#get_random_password_form').submit(function (event) {

        event.preventDefault();

        getPassword(event.target);
    });
}
