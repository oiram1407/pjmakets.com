from django.contrib import admin
from .models import *

#Views for Companies Section
class CompanieAdmin(admin.ModelAdmin):
  list_display = ("name", "user")
admin.site.register(Companie, CompanieAdmin)

class CompanieUserRelatedAdmin(admin.ModelAdmin):
  list_display = ("get_company_name", "user_company", "user")
  @admin.display(ordering='company_name', description='Company Name')
  def get_company_name(self, obj):
    return obj.company.name
admin.site.register(CompaniesUserRelated, CompanieUserRelatedAdmin)

class CompaniesPlataformsRelatedAdmin(admin.ModelAdmin):
  list_display = ("get_company_name", "plataform", "status", "user")
  @admin.display(ordering='company_name', description='Company Name')
  def get_company_name(self, obj):
    return obj.company.name
admin.site.register(CompaniesPlataformsRelated, CompaniesPlataformsRelatedAdmin)

admin.site.register(WaMessagesTemplates)
admin.site.register(Settings)
admin.site.register(WaOutCommingLog)
admin.site.register(WaOutcomigProgramedMessages)

class ProductAdmin(admin.ModelAdmin):
  list_display = ("get_product_name", "sku", "status", "user")
  @admin.display(ordering='product_name', description='Product Name')
  def get_product_name(self, obj):
    return obj.name
admin.site.register(Product, ProductAdmin)

class ProductsRelatedPlataformAdmin(admin.ModelAdmin):
  list_display = ("get_product_name", "method", "user")
  @admin.display(ordering='product_name', description='Product Name')
  def get_product_name(self, obj):
    return obj.product.name
admin.site.register(ProductsRelatedPlataform, ProductsRelatedPlataformAdmin)

class ProductsInventoryAdmin(admin.ModelAdmin):
  list_display = ("get_product_name", "quantity", "user")
  @admin.display(ordering='product_name', description='Product Name')
  def get_product_name(self, obj):
    return obj.product.name
admin.site.register(ProductsInventory, ProductsInventoryAdmin)

class ProductsInventoryUpdateAdmin(admin.ModelAdmin):
  list_display = ("get_product_name", "method_update", "quantity", "user")
  @admin.display(ordering='product_name', description='Product Name')
  def get_product_name(self, obj):
    return obj.product.name
admin.site.register(ProductsInventoryUpdate, ProductsInventoryUpdateAdmin)

class ProductsPriceAdmin(admin.ModelAdmin):
  list_display = ("get_product_name", "plataform_name", "product_price", "user")
  @admin.display(ordering='product_name', description='Product Name')
  def get_product_name(self, obj):
    return obj.product.name
admin.site.register(ProductsPrice, ProductsPriceAdmin)

class ShipProvidersAdmin(admin.ModelAdmin):
  list_display = ("provider_name", "provider_slug", "provider_url", "status", "user")

admin.site.register(ShipProviders, ShipProvidersAdmin)

