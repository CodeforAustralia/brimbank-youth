from django import template

register = template.Library()

@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound: 
    #form that is bound means that some data is validated in the form, regardless whether the data is valid or not.
    # f = ContactForm()
    # >>> f.is_bound --> False
    # >>> f = ContactForm({'subject': 'hello'})
    # >>> f.is_bound --> True
    # f = ContactForm({})
    # f.is_bound --> True

        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput': #becayse password field data never be returned to client
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)