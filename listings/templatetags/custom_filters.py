from django import template

register = template.Library()

@register.filter
def split(value, arg=' '):
    """Split a string by the given argument (default is space)"""
    return value.split(arg)

@register.filter
def get_item(obj, key):
    """Get an attribute/item from an object using its name"""
    try:
        # Try dictionary-like access first
        return obj[key]
    except (KeyError, TypeError):
        try:
            # Try attribute access
            return getattr(obj, key)
        except AttributeError:
            # If both fail, try to get from form fields
            try:
                return obj.fields.get(key)
            except (AttributeError, KeyError):
                return None