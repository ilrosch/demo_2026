from django.contrib import admin
from shoes import models


@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Providers)
class ProviderAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Producers)
class ProducerAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Units)
class UnitAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Categories)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Orders)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(models.OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PickPoints)
class PickPointsAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Roles)
class RolesAdmin(admin.ModelAdmin):
    ...

@admin.register(models.StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    ...
