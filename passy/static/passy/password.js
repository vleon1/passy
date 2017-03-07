function fillPassword(url, id_postfix) {

    const passwordTimeout = 5000;

    const getButton = jQuery('#download_' + id_postfix)[0];
    const copyButton = jQuery('#clipboard_' + id_postfix)[0];

    jQuery.getJSON(url, function(data) {
        setPassword(data);
        setTimeout(resetPassword, passwordTimeout);
    });

    function setPassword(data) {
        getButton.style.visibility = 'hidden';
        getButton.style.display = 'none';

        copyButton.setAttribute('data-clipboard-text', data.stored_password_text);
        copyButton.style.visibility = '';
        copyButton.style.display = '';
    }

    function resetPassword() {
        copyButton.setAttribute('data-clipboard-text', '');
        copyButton.style.visibility = 'hidden';
        copyButton.style.display = 'none';

        getButton.style.visibility = '';
        getButton.style.display = '';
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
    var length = form_query.find("input[name=length]")[0].value;
    var use_symbols = form_query.find("input[name=use_symbols]")[0].checked;

    var stored_password_text_field = jQuery("input[name=stored_password_text]")[0];

    jQuery.getJSON(url, {length: length, use_symbols: use_symbols}).done(function(data) {
        stored_password_text_field.value = data['generated_password'];
    });
}

function initClipboard() {
    // Tooltip
    jQuery('[id^=clipboard_]').tooltip({
        trigger: 'manual',
        placement: 'bottom'
    });

    function setTooltip(button, message) {
        jQuery(button).tooltip('hide').attr('data-original-title', message).tooltip('show');
    }

    // Clipboard
    const clipboard = new Clipboard('[id^=clipboard_]');
    const hiddenClipboard = new Clipboard('[id^=hidden_clipboard_]');

    clipboard.on('success', function(e) {
        e.clearSelection();
        setTooltip(e.trigger, 'Copied!');
    });
    clipboard.on('error', function(e) {
        setTooltip(e.trigger, 'Press Ctrl-C to copy');
    });

    hiddenClipboard.on('success', function(e) {
        e.clearSelection();
        executeHiddenButton(e)
    });
    hiddenClipboard.on('error', function(e) {
        executeHiddenButton(e)
    });

    function executeHiddenButton(e) {
        const id = e.trigger.dataset['executeTarget'];
        document.getElementById(id).click()
    }
}

function initGetRandomPasswordForm() {
    // Overrides the get password button to call rest directly
    jQuery('#get_random_password_form').submit(function (event) {

        event.preventDefault();

        getPassword(event.target);
    });
}
