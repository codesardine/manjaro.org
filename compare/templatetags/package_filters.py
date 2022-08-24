from django import template

register = template.Library()

@register.filter
def report_arch(reports, architecture):
    return reports.items[architecture.name]

@register.filter
def report_total(reports, architecture):
    return reports.get_total(architecture)

@register.filter
def format_branch(value):
    return value.replace("arm-", "")
