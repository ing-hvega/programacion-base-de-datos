# Script to populate the sales database with fake data
# Complete sales system with 20 related tables
import mysql.connector
from faker import Faker
from datetime import datetime, timedelta
import random
import hashlib

# Initialize Faker
fake = Faker('en_US')  # Configured for English

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'sales_system',
    'port': 3308
}

# Record quantity configuration
NUM_COUNTRIES = 20
NUM_REGIONS = 100
NUM_CITIES = 500
NUM_USERS = 5000
NUM_EMPLOYEES = 20000
NUM_CUSTOMERS = 5000
NUM_SUPPLIERS = 5000
NUM_CATEGORIES = 300
NUM_PRODUCTS = 10000
NUM_WAREHOUSES = 100
NUM_PURCHASE_ORDERS = 3000000
NUM_SALES = 20000
NUM_RETURNS = 1000


def generate_unique_email(used_emails):
    """Generates a unique email that is not in the set of used emails"""
    max_attempts = 1000
    attempts = 0

    while attempts < max_attempts:
        email = fake.email()
        if email not in used_emails:
            used_emails.add(email)
            return email
        attempts += 1

    # If no unique one is found, create one with timestamp
    unique_email = f"{fake.user_name()}{int(datetime.now().timestamp())}@{fake.domain_name()}"
    used_emails.add(unique_email)
    return unique_email


def generate_unique_code(prefix, used_codes, length=8):
    """Generates a unique code with prefix"""
    max_attempts = 1000
    attempts = 0

    while attempts < max_attempts:
        code = f"{prefix}{random.randint(10 ** (length - 1), (10 ** length) - 1)}"
        if code not in used_codes:
            used_codes.add(code)
            return code
        attempts += 1

    # If no unique one is found, add timestamp
    code = f"{prefix}{int(datetime.now().timestamp())}"
    used_codes.add(code)
    return code


def hash_password(password):
    """Generates simple password hash"""
    return hashlib.sha256(password.encode()).hexdigest()


def main():
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Sets to track unique values
        used_emails = set()
        used_codes = set()

        print("=== STARTING SALES DATABASE POPULATION ===\n")

        # 1. Populate countries
        countries_data = []
        countries_info = [
            ('United States', 'USA'), ('Canada', 'CAN'), ('Mexico', 'MEX'), ('United Kingdom', 'GBR'),
            ('Germany', 'DEU'), ('France', 'FRA'), ('Italy', 'ITA'), ('Spain', 'ESP'),
            ('Brazil', 'BRA'), ('Argentina', 'ARG'), ('Chile', 'CHL'), ('Peru', 'PER'),
            ('Colombia', 'COL'), ('China', 'CHN'), ('Japan', 'JPN'), ('South Korea', 'KOR'),
            ('Australia', 'AUS'), ('India', 'IND'), ('Russia', 'RUS'), ('Netherlands', 'NLD')
        ]

        print("Inserting countries...")
        for i, (name, code) in enumerate(countries_info):
            cursor.execute(
                'INSERT INTO countries (name, iso_code) VALUES (%s, %s)',
                (name, code)
            )
            country_id = cursor.lastrowid
            countries_data.append({'id': country_id, 'name': name, 'code': code})

        conn.commit()
        print(f"Inserted {len(countries_data)} countries\n")

        # 2. Populate regions
        regions_data = []
        print("Inserting regions...")
        for i in range(NUM_REGIONS):
            country = random.choice(countries_data)
            name = f"{fake.state()} - {country['name']}"

            cursor.execute(
                'INSERT INTO regions (name, country_id) VALUES (%s, %s)',
                (name, country['id'])
            )
            region_id = cursor.lastrowid
            regions_data.append({
                'id': region_id,
                'name': name,
                'country_id': country['id']
            })

            if (i + 1) % 25 == 0:
                print(f"Regions inserted: {i + 1}/{NUM_REGIONS}")

        conn.commit()
        print(f"Inserted {NUM_REGIONS} regions\n")

        # 3. Populate cities
        cities_data = []
        print("Inserting cities...")
        for i in range(NUM_CITIES):
            region = random.choice(regions_data)
            name = fake.city()

            cursor.execute(
                'INSERT INTO cities (name, region_id) VALUES (%s, %s)',
                (name, region['id'])
            )
            city_id = cursor.lastrowid
            cities_data.append({
                'id': city_id,
                'name': name,
                'region_id': region['id']
            })

            if (i + 1) % 100 == 0:
                print(f"Cities inserted: {i + 1}/{NUM_CITIES}")

        conn.commit()
        print(f"Inserted {NUM_CITIES} cities\n")

        # 4. Populate users
        users_data = []
        print("Inserting users...")
        for i in range(NUM_USERS):
            email = generate_unique_email(used_emails)
            password_hash = hash_password("password123")
            first_name = fake.first_name()
            last_name = fake.last_name()
            # Limit phone number length to fit in VARCHAR(20)
            phone = fake.phone_number()[:20]
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
            status = random.choices(['active', 'inactive', 'suspended'], weights=[85, 10, 5])[0]

            cursor.execute(
                '''INSERT INTO users (email, password_hash, first_name, last_name, phone,
                                      birth_date, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (email, password_hash, first_name, last_name, phone, birth_date, status)
            )
            user_id = cursor.lastrowid
            users_data.append({
                'id': user_id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'status': status
            })

            if (i + 1) % 500 == 0:
                print(f"Users inserted: {i + 1}/{NUM_USERS}")

        conn.commit()
        print(f"Inserted {NUM_USERS} users\n")

        # 5. Populate employees
        employees_data = []
        print("Inserting employees...")
        available_users = [u for u in users_data if u['status'] == 'active']
        positions = [
            'Sales Representative', 'Sales Supervisor', 'Sales Manager', 'Cashier', 'Warehouse Worker',
            'Warehouse Manager', 'Accountant', 'Accounting Assistant', 'Receptionist', 'Janitor',
            'General Manager', 'Assistant Manager', 'Inventory Analyst', 'Buyer',
            'Purchasing Manager', 'Driver', 'Security', 'Cleaning', 'Maintenance', 'IT Specialist'
        ]

        for i in range(NUM_EMPLOYEES):
            if i >= len(available_users):
                break

            user = available_users[i]
            employee_code = generate_unique_code("EMP", used_codes, 6)
            position = random.choice(positions)
            salary = random.uniform(1000, 8000)
            hire_date = fake.date_between(start_date='-5y', end_date='today')
            city = random.choice(cities_data)
            commission = random.uniform(0, 10) if 'Sales' in position else 0
            status = random.choices(['active', 'inactive', 'leave'], weights=[90, 5, 5])[0]

            cursor.execute(
                '''INSERT INTO employees (user_id, employee_code, position, salary,
                                          hire_date, city_id, commission_percentage, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (user['id'], employee_code, position, salary, hire_date,
                 city['id'], commission, status)
            )
            employee_id = cursor.lastrowid
            employees_data.append({
                'id': employee_id,
                'user_id': user['id'],
                'code': employee_code,
                'position': position,
                'status': status
            })

        # Assign managers to some employees
        for employee in employees_data:
            if random.random() < 0.3:  # 30% of employees have a manager
                manager = random.choice([e for e in employees_data if e['id'] != employee['id']])
                cursor.execute(
                    'UPDATE employees SET manager_id = %s WHERE id = %s',
                    (manager['id'], employee['id'])
                )

        conn.commit()
        print(f"Inserted {len(employees_data)} employees\n")

        # 6. Populate customers
        customers_data = []
        print("Inserting customers...")
        remaining_users = available_users[NUM_EMPLOYEES:]

        for i in range(min(NUM_CUSTOMERS, len(remaining_users))):
            user = remaining_users[i]
            customer_type = random.choices(['individual', 'corporate'], weights=[80, 20])[0]
            identification_document = fake.ssn() if customer_type == 'individual' else fake.ein()
            registration_date = fake.date_between(start_date='-2y', end_date='today')
            city = random.choice(cities_data)
            address = fake.address()
            credit_limit = random.uniform(1000, 50000)
            assigned_employee = random.choice(employees_data) if random.random() < 0.7 else None
            status = random.choices(['active', 'inactive', 'delinquent'], weights=[85, 10, 5])[0]

            cursor.execute(
                '''INSERT INTO customers (user_id, customer_type, identification_document,
                                          registration_date, city_id, address, credit_limit, assigned_employee_id,
                                          status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (user['id'], customer_type, identification_document, registration_date, city['id'],
                 address, credit_limit, assigned_employee['id'] if assigned_employee else None, status)
            )
            customer_id = cursor.lastrowid
            customers_data.append({
                'id': customer_id,
                'user_id': user['id'],
                'type': customer_type,
                'status': status
            })

            if (i + 1) % 200 == 0:
                print(f"Customers inserted: {i + 1}/{min(NUM_CUSTOMERS, len(remaining_users))}")

        conn.commit()
        print(f"Inserted {len(customers_data)} customers\n")

        # 7. Populate suppliers
        suppliers_data = []
        print("Inserting suppliers...")
        for i in range(NUM_SUPPLIERS):
            company_name = fake.company()
            tax_id = fake.ssn()
            email = fake.company_email()
            # Limit phone number length to fit in VARCHAR(20)
            phone = fake.phone_number()[:20]
            address = fake.address()
            city = random.choice(cities_data)
            contact_name = fake.name()
            # Limit contact phone number length to fit in VARCHAR(20)
            contact_phone = fake.phone_number()[:20]
            status = random.choices(['active', 'inactive'], weights=[90, 10])[0]

            cursor.execute(
                '''INSERT INTO suppliers (company_name, tax_id, email, phone, address,
                                          city_id, contact_name, contact_phone, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (company_name, tax_id, email, phone, address, city['id'],
                 contact_name, contact_phone, status)
            )
            supplier_id = cursor.lastrowid
            suppliers_data.append({
                'id': supplier_id,
                'name': company_name,
                'status': status
            })

        conn.commit()
        print(f"Inserted {NUM_SUPPLIERS} suppliers\n")

        # 8. Populate product categories
        categories_data = []
        print("Inserting product categories...")
        main_categories = [
            'Electronics', 'Clothing & Footwear', 'Home & Garden', 'Sports', 'Books',
            'Health & Beauty', 'Automotive', 'Toys', 'Music', 'Movies',
            'Food', 'Beverages', 'Pet Supplies', 'Office Supplies', 'Tools'
        ]

        # Insert main categories
        for category in main_categories:
            cursor.execute(
                'INSERT INTO product_categories (name, description) VALUES (%s, %s)',
                (category, fake.text(max_nb_chars=100))
            )
            category_id = cursor.lastrowid
            categories_data.append({
                'id': category_id,
                'name': category,
                'is_parent': True
            })

        # Insert subcategories
        for i in range(NUM_CATEGORIES - len(main_categories)):
            parent_category = random.choice(categories_data)
            name = f"{fake.word().title()} {parent_category['name']}"

            cursor.execute(
                '''INSERT INTO product_categories (name, description, parent_category_id)
                   VALUES (%s, %s, %s)''',
                (name, fake.text(max_nb_chars=100), parent_category['id'])
            )
            category_id = cursor.lastrowid
            categories_data.append({
                'id': category_id,
                'name': name,
                'is_parent': False
            })

        conn.commit()
        print(f"Inserted {NUM_CATEGORIES} product categories\n")

        # 9. Populate products
        products_data = []
        print("Inserting products...")
        units = ['unit', 'kilogram', 'liter', 'meter', 'box', 'package']

        for i in range(NUM_PRODUCTS):
            code = generate_unique_code("PROD", used_codes, 8)
            name = f"{fake.word().title()} {fake.word().title()}"
            description = fake.text(max_nb_chars=200)
            category = random.choice(categories_data)
            supplier = random.choice([s for s in suppliers_data if s['status'] == 'active'])
            purchase_price = random.uniform(10, 500)
            sale_price = purchase_price * random.uniform(1.2, 3.0)  # 20% to 200% margin
            current_stock = random.randint(0, 1000)
            minimum_stock = random.randint(5, 50)
            unit = random.choice(units)
            weight = random.uniform(0.1, 10.0)
            dimensions = f"{random.randint(1, 50)}x{random.randint(1, 50)}x{random.randint(1, 50)} cm"
            status = random.choices(['active', 'discontinued', 'out_of_stock'], weights=[85, 10, 5])[0]

            cursor.execute(
                '''INSERT INTO products (product_code, name, description, category_id,
                                         supplier_id, purchase_price, sale_price, current_stock, minimum_stock,
                                         unit_of_measure, weight, dimensions, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (code, name, description, category['id'], supplier['id'],
                 purchase_price, sale_price, current_stock, minimum_stock,
                 unit, weight, dimensions, status)
            )
            product_id = cursor.lastrowid
            products_data.append({
                'id': product_id,
                'code': code,
                'name': name,
                'sale_price': sale_price,
                'current_stock': current_stock,
                'status': status
            })

            if (i + 1) % 100 == 0:
                print(f"Products inserted: {i + 1}/{NUM_PRODUCTS}")

        conn.commit()
        print(f"Inserted {NUM_PRODUCTS} products\n")

        # 10. Populate warehouses
        warehouses_data = []
        print("Inserting warehouses...")
        for i in range(NUM_WAREHOUSES):
            name = f"Warehouse {fake.city()}"
            address = fake.address()
            city = random.choice(cities_data)
            # Limit phone number length to fit in VARCHAR(20)
            phone = fake.phone_number()[:20]
            max_capacity = random.randint(1000, 10000)
            manager = random.choice(employees_data)
            status = random.choices(['active', 'inactive', 'maintenance'], weights=[85, 10, 5])[0]

            cursor.execute(
                '''INSERT INTO warehouses (name, address, city_id, phone,
                                           max_capacity, manager_employee_id, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (name, address, city['id'], phone, max_capacity, manager['id'], status)
            )
            warehouse_id = cursor.lastrowid
            warehouses_data.append({
                'id': warehouse_id,
                'name': name,
                'status': status
            })

        conn.commit()
        print(f"Inserted {NUM_WAREHOUSES} warehouses\n")

        # 11. Populate warehouse inventory
        print("Inserting warehouse inventory...")
        inventory_count = 0
        for warehouse in warehouses_data:
            products_in_warehouse = random.sample(products_data, random.randint(50, 200))
            for product in products_in_warehouse:
                quantity = random.randint(0, product['current_stock'])
                location = f"Aisle {random.randint(1, 10)} - Shelf {random.randint(1, 20)}"

                cursor.execute(
                    '''INSERT INTO warehouse_inventory (product_id, warehouse_id, quantity, location)
                       VALUES (%s, %s, %s, %s)''',
                    (product['id'], warehouse['id'], quantity, location)
                )
                inventory_count += 1

        conn.commit()
        print(f"Inserted {inventory_count} inventory records\n")

        # 12. Populate purchase orders
        purchase_orders_data = []
        print("Inserting purchase orders...")
        order_statuses = ['pending', 'approved', 'shipped', 'received', 'cancelled']

        for i in range(NUM_PURCHASE_ORDERS):
            order_number = generate_unique_code("PO", used_codes, 8)
            supplier = random.choice([s for s in suppliers_data if s['status'] == 'active'])
            employee = random.choice([e for e in employees_data if e['status'] == 'active'])
            order_date = fake.date_between(start_date='-1y', end_date='today')
            estimated_delivery_date = order_date + timedelta(days=random.randint(1, 30))
            subtotal = random.uniform(1000, 50000)
            taxes = subtotal * 0.18
            total = subtotal + taxes
            status = random.choice(order_statuses)

            actual_delivery_date = None
            if status in ['received']:
                actual_delivery_date = estimated_delivery_date + timedelta(days=random.randint(-5, 10))

            cursor.execute(
                '''INSERT INTO purchase_orders (order_number, supplier_id, requesting_employee_id,
                                                order_date, estimated_delivery_date, actual_delivery_date, subtotal, taxes,
                                                total, status, notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (order_number, supplier['id'], employee['id'], order_date, estimated_delivery_date,
                 actual_delivery_date, subtotal, taxes, total, status, fake.text(max_nb_chars=100))
            )
            order_id = cursor.lastrowid
            purchase_orders_data.append({
                'id': order_id,
                'number': order_number,
                'total': total,
                'status': status
            })

        conn.commit()
        print(f"Inserted {NUM_PURCHASE_ORDERS} purchase orders\n")

        # 13. Populate purchase order details
        print("Inserting purchase order details...")
        details_count = 0
        for order in purchase_orders_data:
            num_products = random.randint(1, 10)
            order_products = random.sample(products_data, num_products)

            for product in order_products:
                quantity = random.randint(1, 100)
                unit_price = random.uniform(product['sale_price'] * 0.5, product['sale_price'] * 0.8)
                subtotal = quantity * unit_price

                cursor.execute(
                    '''INSERT INTO purchase_order_details (purchase_order_id, product_id,
                                                            quantity, unit_price, subtotal)
                       VALUES (%s, %s, %s, %s, %s)''',
                    (order['id'], product['id'], quantity, unit_price, subtotal)
                )
                details_count += 1

        conn.commit()
        print(f"Inserted {details_count} purchase order details\n")

        # 14. Populate sales
        sales_data = []
        print("Inserting sales...")
        payment_methods = ['cash', 'credit_card', 'debit_card', 'transfer', 'credit']
        sale_statuses = ['pending', 'completed', 'cancelled', 'returned']

        for i in range(NUM_SALES):
            sale_number = generate_unique_code("SL", used_codes, 8)
            customer = random.choice([c for c in customers_data if c['status'] == 'active'])
            salesperson = random.choice([e for e in employees_data if e['status'] == 'active' and 'Sales' in e['position']])
            if not salesperson:  # If no salespeople, use any employee
                salesperson = random.choice([e for e in employees_data if e['status'] == 'active'])

            sale_date = fake.date_time_between(start_date='-6m', end_date='now')
            subtotal = random.uniform(50, 5000)
            discount = subtotal * random.uniform(0, 0.2)  # Up to 20% discount
            taxes = (subtotal - discount) * 0.18
            total = subtotal - discount + taxes
            payment_method = random.choice(payment_methods)
            status = random.choices(sale_statuses, weights=[5, 80, 10, 5])[0]

            cursor.execute(
                '''INSERT INTO sales (sale_number, customer_id, salesperson_employee_id,
                                      sale_date, subtotal, discount, taxes, total, payment_method,
                                      status, notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (sale_number, customer['id'], salesperson['id'], sale_date, subtotal, discount,
                 taxes, total, payment_method, status, fake.text(max_nb_chars=50))
            )
            sale_id = cursor.lastrowid
            sales_data.append({
                'id': sale_id,
                'number': sale_number,
                'customer_id': customer['id'],
                'total': total,
                'payment_method': payment_method,
                'status': status,
                'sale_date': sale_date
            })

            if (i + 1) % 200 == 0:
                print(f"Sales inserted: {i + 1}/{NUM_SALES}")

        conn.commit()
        print(f"Inserted {NUM_SALES} sales\n")

        # 15. Populate sale details
        print("Inserting sale details...")
        sale_details_count = 0
        for sale in sales_data:
            num_products = random.randint(1, 8)
            available_products = [p for p in products_data if p['status'] == 'active' and p['current_stock'] > 0]
            if not available_products:
                continue

            sale_products = random.sample(available_products, min(num_products, len(available_products)))

            for product in sale_products:
                quantity = random.randint(1, min(10, product['current_stock']))
                unit_price = product['sale_price']
                unit_discount = unit_price * random.uniform(0, 0.15)  # Up to 15% discount per item
                subtotal = quantity * (unit_price - unit_discount)

                cursor.execute(
                    '''INSERT INTO sale_details (sale_id, product_id, quantity,
                                                 unit_price, unit_discount, subtotal)
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (sale['id'], product['id'], quantity, unit_price, unit_discount, subtotal)
                )
                sale_details_count += 1

        conn.commit()
        print(f"Inserted {sale_details_count} sale details\n")

        # 16. Populate inventory movements
        print("Inserting inventory movements...")
        movement_types = ['in', 'out', 'adjustment', 'transfer']
        references = ['sale', 'purchase', 'adjustment', 'transfer']
        movements_count = 0

        for i in range(1000):  # 1000 example movements
            product = random.choice(products_data)
            warehouse = random.choice(warehouses_data)
            movement_type = random.choice(movement_types)
            quantity = random.randint(1, 100)
            reference_type = random.choice(references)
            employee = random.choice(employees_data)
            movement_date = fake.date_time_between(start_date='-3m', end_date='now')

            cursor.execute(
                '''INSERT INTO inventory_movements (product_id, warehouse_id, movement_type,
                                                    quantity, reference_type, employee_id, notes,
                                                    movement_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (product['id'], warehouse['id'], movement_type, quantity, reference_type,
                 employee['id'], fake.text(max_nb_chars=100), movement_date)
            )
            movements_count += 1

        conn.commit()
        print(f"Inserted {movements_count} inventory movements\n")

        # 17. Populate accounts receivable
        print("Inserting accounts receivable...")
        accounts_receivable_data = []
        credit_sales = [s for s in sales_data if s['payment_method'] == 'credit' and s['status'] == 'completed']

        for sale in credit_sales:
            due_date = sale['sale_date'].date() + timedelta(days=random.randint(15, 90))
            days_overdue = max(0, (datetime.now().date() - due_date).days)
            pending_amount = sale['total'] * random.uniform(0, 1)  # May be partially paid
            status = 'overdue' if days_overdue > 0 else 'pending'
            if pending_amount == 0:
                status = 'paid'
            elif 0 < pending_amount < sale['total']:
                status = 'partial'

            cursor.execute(
                '''INSERT INTO accounts_receivable (sale_id, customer_id, total_amount,
                                                    pending_amount, due_date, days_overdue, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (sale['id'], sale['customer_id'], sale['total'], pending_amount,
                 due_date, days_overdue, status)
            )
            account_id = cursor.lastrowid
            accounts_receivable_data.append({
                'id': account_id,
                'sale_id': sale['id'],
                'total_amount': sale['total'],
                'pending_amount': pending_amount
            })

        conn.commit()
        print(f"Inserted {len(accounts_receivable_data)} accounts receivable\n")

        # 18. Populate payments received
        print("Inserting payments received...")
        payments_count = 0
        for account in accounts_receivable_data:
            if account['pending_amount'] < account['total_amount']:  # There have been payments
                num_payments = random.randint(1, 3)
                total_paid_amount = account['total_amount'] - account['pending_amount']

                for j in range(num_payments):
                    payment_amount = total_paid_amount / num_payments if j < num_payments - 1 else total_paid_amount - (
                            total_paid_amount / num_payments * j)
                    payment_method = random.choice(['cash', 'credit_card', 'debit_card', 'transfer', 'check'])
                    payment_date = fake.date_time_between(start_date='-2m', end_date='now')
                    employee = random.choice(employees_data)

                    cursor.execute(
                        '''INSERT INTO payments_received (accounts_receivable_id, payment_amount,
                                                          payment_method, reference_number, payment_date,
                                                          receiving_employee_id,
                                                          notes)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (account['id'], payment_amount, payment_method, fake.uuid4()[:20], payment_date,
                         employee['id'], fake.text(max_nb_chars=50))
                    )
                    payments_count += 1

        conn.commit()
        print(f"Inserted {payments_count} payments received\n")

        # 19. Populate returns
        returns_data = []
        print("Inserting returns...")
        completed_sales = [s for s in sales_data if s['status'] == 'completed']
        return_sales = random.sample(completed_sales, min(NUM_RETURNS, len(completed_sales)))

        for sale in return_sales:
            return_number = generate_unique_code("RET", used_codes, 8)
            employee = random.choice(employees_data)
            return_date = sale['sale_date'] + timedelta(days=random.randint(1, 30))
            reason = random.choice([
                'Defective product',
                'Does not meet expectations',
                'Arrived damaged',
                'Wrong order',
                'Customer changed mind',
                'Warranty claim',
                'Sales error'
            ])
            total_returned = sale['total'] * random.uniform(0.1, 1.0)  # Partial or full return
            status = random.choices(['pending', 'approved', 'rejected', 'processed'], weights=[10, 60, 10, 20])[0]

            cursor.execute(
                '''INSERT INTO returns (return_number, sale_id, customer_id,
                                        authorizing_employee_id, return_date, reason, total_returned, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (return_number, sale['id'], sale['customer_id'], employee['id'],
                 return_date, reason, total_returned, status)
            )
            return_id = cursor.lastrowid
            returns_data.append({
                'id': return_id,
                'sale_id': sale['id'],
                'number': return_number,
                'total': total_returned
            })

        conn.commit()
        print(f"Inserted {len(returns_data)} returns\n")

        # 20. Populate return details
        print("Inserting return details...")
        return_details_count = 0
        for return_record in returns_data:
            # Get products from original sale
            cursor.execute(
                'SELECT product_id, quantity, unit_price FROM sale_details WHERE sale_id = %s',
                (return_record['sale_id'],)
            )
            sale_products = cursor.fetchall()

            # Select some products to return
            products_to_return = random.sample(sale_products, random.randint(1, len(sale_products)))

            for product_info in products_to_return:
                product_id, original_quantity, original_price = product_info
                quantity_returned = random.randint(1, original_quantity)
                subtotal_returned = quantity_returned * original_price
                product_condition = random.choices(['new', 'used', 'damaged'], weights=[20, 60, 20])[0]

                cursor.execute(
                    '''INSERT INTO return_details (return_id, product_id,
                                                   quantity_returned, unit_price, subtotal_returned,
                                                   product_condition)
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (return_record['id'], product_id, quantity_returned, original_price,
                     subtotal_returned, product_condition)
                )
                return_details_count += 1

        conn.commit()
        print(f"Inserted {return_details_count} return details\n")

        print("=== POPULATION COMPLETED ===")
        print(f"Total tables populated: 20")

        # Calculate total records
        total_records = sum([
            len(countries_data), NUM_REGIONS, NUM_CITIES, NUM_USERS,
            len(employees_data), len(customers_data), NUM_SUPPLIERS,
            NUM_CATEGORIES, NUM_PRODUCTS, NUM_WAREHOUSES,
            inventory_count, NUM_PURCHASE_ORDERS, details_count,
            NUM_SALES, sale_details_count, movements_count,
            len(accounts_receivable_data), payments_count, len(returns_data),
            return_details_count
        ])
        print(f"Total approximate records: {total_records}")

        cursor.close()
        conn.close()

        print("\nSales database populated successfully!")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"General Error: {e}")


if __name__ == "__main__":
    main()
