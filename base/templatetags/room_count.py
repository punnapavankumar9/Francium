from django import template


register = template.Library()

@register.filter
def room_count_by_topic(topic):
    return topic.room_set.filter(is_private = False).count()

@register.filter
def room_count(topic):
    return topic.room_set.all().count()