from django.db.models.base import ModelBase
from django.contrib import admin
from .models import *

import adminscopus.models as m

for model_name in dir(m):
    model = getattr(m, model_name)
    if isinstance(model, ModelBase):
        admin.site.register(model)

#admin.site.register(Hub)