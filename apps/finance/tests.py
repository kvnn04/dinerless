from django.test import TestCase
from django.contrib.auth.models import User
from apps.finance.models import Category, Transaction, Budget
from decimal import Decimal
from apps.finance.api.v1.tests_serializers import (
    CategorySerializerTest, 
    TransactionSerializerTest, 
    BudgetSerializerTest
)

class FinanceSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        
        self.category = Category.objects.create(
            name="Salud", 
            user=self.user, 
            icon="💊"
        )
        
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("150.50"),
            description="Compra de medicina",
            type="EXPENSE"
        )

    def test_category_serialization_robust(self):
        
        serializer = CategorySerializerTest(instance=self.category)
        data = dict(serializer.data)

        self.assertEqual(data['name'], "Salud")
        self.assertEqual(data['icon'], "💊")
        self.assertIsInstance(data['id'], int)

        dirty_payload_empty = {
            "name": "", 
            "icon": "❓",
            "user": self.user.pk
        }

        dirty_payload_long = {
            "name": "E" * 101, # Creamos un nombre de 101 caracteres
            "icon": "⚠️",
            "user": self.user.pk
        }

        bad_serializer_1 = CategorySerializerTest(data=dirty_payload_empty)
        self.assertFalse(bad_serializer_1.is_valid())
        print(f"🚫 Error de Nombre Vacío: {bad_serializer_1.errors['name']}") # type: ignore

        bad_serializer_2 = CategorySerializerTest(data=dirty_payload_long)
        self.assertFalse(bad_serializer_2.is_valid())
        if 'name' in bad_serializer_2.errors:
            print(f"🚫 Error de Nombre Largo: {bad_serializer_2.errors['name']}") # type: ignore

        print("✅ Serializer de Categoría (Filtros de suciedad): OK")

    def test_transaction_serialization_robust(self):
        """Prueba de fuego para Transacciones: Datos válidos e intentos de datos basura"""
        
        serializer = TransactionSerializerTest(instance=self.transaction)
        data = dict(serializer.data)
        
        self.assertEqual(str(data['amount']), "150.50")
        self.assertEqual(data['type'], "EXPENSE")
        # Verifico que el category_name (ReadOnlyField) esté funcionando
        self.assertEqual(data['category_name'], "Salud")


        dirty_payload_negative = {
            "category": self.category.pk,
            "amount": "-100.00",
            "description": "Dinero mágico",
            "type": "EXPENSE",
            "date": "2026-02-13"
        }
        
        dirty_payload_type = {
            "category": self.category.pk,
            "amount": "50.00",
            "description": "Error de tipo",
            "type": "GIFT",  # 'GIFT' no está en ['INCOME', 'EXPENSE']
            "date": "2026-02-13"
        }

        bad_serializer_1 = TransactionSerializerTest(data=dirty_payload_negative)
        is_valid_1 = bad_serializer_1.is_valid()
        
        self.assertFalse(is_valid_1)
        print(f"🚫 Error de Monto capturado: {bad_serializer_1.errors['amount']}")  # type: ignore

        bad_serializer_2 = TransactionSerializerTest(data=dirty_payload_type)
        is_valid_2 = bad_serializer_2.is_valid()
        
        self.assertFalse(is_valid_2)
        print(f"🚫 Error de Tipo capturado: {bad_serializer_2.errors['type']}") # type: ignore
        print("✅ Serializer de Transacción (Filtros de suciedad): OK")
        
    def test_budget_serialization_robust(self):
        """Prueba robusta: Serialización, tipos de datos y validación de lógica"""
        budget_data = {
            "user": self.user,
            "category": self.category,
            "limit_amount": Decimal("1250.75"),
            "month": 12,
            "year": 2026
        }
        budget = Budget.objects.create(**budget_data)
        
        serializer = BudgetSerializerTest(instance=budget)
        data = dict(serializer.data)

        self.assertEqual(str(data['limit_amount']), "1250.75")
        self.assertEqual(data['month'], 12)
        self.assertEqual(data['year'], 2026)
        
        self.assertIsInstance(data['month'], int)
        self.assertIsInstance(data['limit_amount'], str)


        invalid_payload = {
            "limit_amount": "500.00",
            "month": 13, # Mes inexistente
            "year": 2026,
            "category": getattr(self.category, 'id')
        }
        bad_serializer = BudgetSerializerTest(data=invalid_payload)

        is_valid = bad_serializer.is_valid()

        self.assertFalse(is_valid)
        
        self.assertIn('month', bad_serializer.errors)
        print(f"Mensaje de error capturado: {bad_serializer.errors['month']}") # type: ignore
    
        
        print("✅ Serializer de Presupuesto (Robustecido): OK")