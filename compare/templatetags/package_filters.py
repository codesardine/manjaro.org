from django import template

register = template.Library()

@register.filter
def report_arch(repports, architecture):
    return repports.items[architecture.name]

@register.filter
def report_total(repports, architecture):
    return repports.get_total(architecture)

@register.filter
def format_branch(value):
    return value.replace("arm-", "")
