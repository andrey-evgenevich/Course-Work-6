from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing


def get_mailing_from_cache():
    if CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailing = cache.get(key)
    if mailing is not None:
        return mailing
    mailing = Mailing.objects.all()
    cache.set(key, mailing)
    return mailing
