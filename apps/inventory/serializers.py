from rest_framework import serializers
from .models import (
    InventoryCategory, InventoryItem, StockTransaction,
    FeedFormula, FeedFormulaIngredient, InventoryAlert
)


class InventoryCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for inventory categories.
    """
    
    class Meta:
        model = InventoryCategory
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class InventoryItemListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing inventory items.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    stock_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    needs_reorder = serializers.BooleanField(read_only=True)
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'code', 'description',
            'category', 'category_name', 'item_type', 'item_type_display',
            'farm', 'farm_name', 'unit', 'unit_display',
            'quantity', 'reorder_level', 'max_stock',
            'stock_status', 'stock_value', 'needs_reorder',
            'unit_cost', 'supplier_name', 'is_active'
        ]


class InventoryItemDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for inventory item details.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    stock_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    needs_reorder = serializers.BooleanField(read_only=True)
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    recent_transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'code', 'description',
            'category', 'category_name', 'item_type', 'item_type_display',
            'farm', 'farm_name', 'unit', 'unit_display',
            'quantity', 'reorder_level', 'max_stock',
            'stock_status', 'stock_value', 'needs_reorder',
            'unit_cost', 'supplier_name', 'supplier_contact',
            'is_active', 'recent_transactions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']
    
    def get_recent_transactions(self, obj):
        transactions = obj.transactions.all()[:10]
        return StockTransactionSerializer(transactions, many=True).data


class InventoryItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating inventory items.
    """
    
    class Meta:
        model = InventoryItem
        fields = [
            'name', 'description', 'category', 'item_type',
            'farm', 'unit', 'quantity', 'reorder_level',
            'max_stock', 'unit_cost', 'supplier_name', 'supplier_contact'
        ]


class StockTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for stock transactions.
    """
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_code = serializers.CharField(source='item.code', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.full_name', read_only=True)
    
    class Meta:
        model = StockTransaction
        fields = [
            'id', 'item', 'item_name', 'item_code',
            'transaction_type', 'transaction_type_display',
            'date', 'quantity', 'unit_cost', 'total_cost',
            'supplier_name', 'invoice_number', 'reference',
            'notes', 'balance_after',
            'recorded_by', 'recorded_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'total_cost', 'balance_after', 'created_at', 'recorded_by']
    
    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)


class StockTransactionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock transactions.
    """
    
    class Meta:
        model = StockTransaction
        fields = [
            'item', 'transaction_type', 'date', 'quantity',
            'unit_cost', 'supplier_name', 'supplier_contact',
            'invoice_number', 'reference', 'notes'
        ]


class FeedFormulaIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for feed formula ingredients.
    """
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    ingredient_unit = serializers.CharField(source='ingredient.unit', read_only=True)
    
    class Meta:
        model = FeedFormulaIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'ingredient_unit', 'quantity', 'notes']


class FeedFormulaListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing feed formulas.
    """
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    ingredient_count = serializers.IntegerField(source='ingredients.count', read_only=True)
    total_quantity = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = FeedFormula
        fields = [
            'id', 'name', 'description', 'farm', 'farm_name',
            'target_animals', 'ingredient_count', 'total_quantity',
            'is_active', 'created_at'
        ]


class FeedFormulaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for feed formula details.
    """
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    ingredients = FeedFormulaIngredientSerializer(many=True, read_only=True)
    total_quantity = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = FeedFormula
        fields = [
            'id', 'name', 'description', 'farm', 'farm_name',
            'target_animals', 'preparation_instructions',
            'feeding_instructions', 'ingredients',
            'total_quantity', 'is_active',
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class FeedFormulaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating feed formulas.
    """
    
    class Meta:
        model = FeedFormula
        fields = [
            'name', 'description', 'farm', 'target_animals',
            'preparation_instructions', 'feeding_instructions'
        ]
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class InventoryAlertSerializer(serializers.ModelSerializer):
    """
    Serializer for inventory alerts.
    """
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_code = serializers.CharField(source='item.code', read_only=True)
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    acknowledged_by_name = serializers.CharField(source='acknowledged_by.full_name', read_only=True)
    
    class Meta:
        model = InventoryAlert
        fields = [
            'id', 'farm', 'farm_name', 'item', 'item_name', 'item_code',
            'alert_type', 'alert_type_display', 'message',
            'status', 'status_display',
            'acknowledged_by', 'acknowledged_by_name', 'acknowledged_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class InventoryStatsSerializer(serializers.Serializer):
    """
    Serializer for inventory statistics.
    """
    total_items = serializers.IntegerField()
    total_stock_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    low_stock_items = serializers.IntegerField()
    out_of_stock_items = serializers.IntegerField()
    items_by_type = serializers.ListField(child=serializers.DictField())
    items_by_category = serializers.ListField(child=serializers.DictField())
    recent_transactions = serializers.ListField(child=serializers.DictField())
    active_alerts = serializers.IntegerField()


class FeedFormulaPreparationSerializer(serializers.Serializer):
    """
    Serializer for feed formula preparation.
    """
    formula_id = serializers.IntegerField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()
    notes = serializers.CharField(required=False, allow_blank=True)
