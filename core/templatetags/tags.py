from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from core.models import Participant
register = template.Library()


@register.simple_tag
def setvar(val=None):
  return val

@register.simple_tag
def getParticipant(id):
  try:
    return Participant.objects.get(pk=id)
  except Exception as e:
    return None