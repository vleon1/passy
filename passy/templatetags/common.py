from django import template

register = template.Library()


@register.inclusion_tag('passy/common/error.html')
def render_errors(errors):
    return dict(errors=errors)


@register.inclusion_tag('passy/common/input.html', takes_context=True)
def render_field_input(context, name, value=None, input_id=None, input_type="text", placeholder="", extra_tags="", required=True):

    return dict(name=name, input_id=input_id if input_id is not None else name, input_type=input_type,
                value=value if value is not None else context['form'][name], placeholder=placeholder,
                extra_tags=extra_tags,
                required="required" if required else "")
