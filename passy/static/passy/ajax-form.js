function replaceDocument(docString) {
    var doc = document.open("text/html");
    doc.write(docString);
    doc.close();
}


function formToJSON(form) {
    var form_data = [].reduce.call(form.elements, function(data, element) {
        data[element.name] = element.value;
        return data;
    });

    return JSON.stringify(form_data);
}


function doAjaxSubmit(e) {
    var form = $(this);
    var btn = $(this.clk);
    var method = btn.data('method') || form.data('method') || form.attr('method') || 'GET';
    method = method.toUpperCase();
    if (method === 'GET') {
        // GET requests can always use standard form submits.
        return;
    }

    var contentType =
        form.find('input[data-override="content-type"]').val() ||
        form.find('select[data-override="content-type"] option:selected').text();
    if (method === 'POST' && !contentType) {
        // POST requests can use standard form submits, unless we have
        // overridden the content type.
        return;
    }

    // At this point we need to make an AJAX form submission.
    e.preventDefault();

    var url = form.attr('action');
    var data;
    if (contentType) {
        data = form.find('[data-override="content"]').val() || ''
    } else {
        contentType = form.attr('enctype') || form.attr('encoding');
        if (contentType === 'multipart/form-data') {
            if (!window.FormData) {
                alert('Your browser does not support AJAX multipart form submissions');
                return;
            }
            // Use the FormData API and allow the content type to be set automatically,
            // so it includes the boundary string.
            // See https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
            contentType = false;
            data = new FormData(form[0]);
        } else {
            contentType = 'application/json';
            data = formToJSON(form[0]);
        }
    }

    var ret = $.ajax({
        url: url,
        method: method,
        data: data,
        contentType: contentType,
        processData: false,
        headers: {'Accept': 'text/html; q=1.0, */*'}
    });
    ret.always(function(data, textStatus, jqXHR) {
        if (textStatus != 'success') {
            jqXHR = data;
        }
        var responseContentType = jqXHR.getResponseHeader("content-type") || "";
        if (responseContentType.toLowerCase().indexOf('text/html') === 0) {
            replaceDocument(jqXHR.responseText);
            try {
                // Modify the location and scroll to top, as if after page load.
                history.replaceState({}, '', url);
                scroll(0,0);
            } catch(err) {
                // History API not supported, so redirect.
                window.location = url;
            }
        } else {
            // Not HTML content. We can't open this directly, so redirect.
            window.location = url;
        }
    });
    return ret;
}


function captureSubmittingElement(e) {
    var target = e.target;
    var form = this;
    form.clk = target;
}


$.fn.ajaxForm = function() {
    var options = {};
    return this
        .unbind('submit.form-plugin  click.form-plugin')
        .bind('submit.form-plugin', options, doAjaxSubmit)
        .bind('click.form-plugin', options, captureSubmittingElement);
};


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = Cookies.get('csrftoken');

        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function() {
        $('form').ajaxForm();
});
