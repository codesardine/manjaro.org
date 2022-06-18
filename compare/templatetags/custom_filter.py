from django import template

register = template.Library()

@register.filter
def repport_arch(repports, architecture):
    return repports.items[architecture.name]

@register.filter
def repport_total(repports, architecture):
    return repports.get_total(architecture)
