# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
	Profile,
	Search,
	Stock,
	StockDailyFive,
	StockDailyFifteen,
	StockDailyThirty,
	StockWeekly,
	StockMonthly,
)

admin.site.register(Profile)
admin.site.register(Search)
admin.site.register(Stock)
admin.site.register(StockDailyFive)
admin.site.register(StockDailyFifteen)
admin.site.register(StockDailyThirty)
admin.site.register(StockWeekly)
admin.site.register(StockMonthly)
