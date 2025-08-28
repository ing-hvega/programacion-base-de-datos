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
NUM_PURCHASE_ORDERS = 30000
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
    conn = None
    cursor = None
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
            # Ensure email doesn't exceed VARCHAR(150)
            if len(email) > 150:
                email = email[:147] + "..."

            password_hash = hash_password("password123")
            first_name = fake.first_name()[:100]  # Limit to VARCHAR(100)
            last_name = fake.last_name()[:100]   # Limit to VARCHAR(100)
            phone = fake.phone_number()[:20]     # Limit to VARCHAR(20)
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

        # Limit employees to maximum 70% of available users to leave room for customers
        max_employees = min(NUM_EMPLOYEES, int(len(available_users) * 0.7))

        for i in range(max_employees):
            user = available_users[i]
            employee_code = generate_unique_code("EMP", used_codes, 6)[:20]  # Limit to VARCHAR(20)
            position = random.choice(positions)[:100]  # Limit to VARCHAR(100)
            salary = round(random.uniform(1000, 8000), 2)  # DECIMAL(10,2)
            hire_date = fake.date_between(start_date='-5y', end_date='today')
            city = random.choice(cities_data)
            commission = round(random.uniform(0, 10), 2) if 'Sales' in position else 0.00  # DECIMAL(5,2)
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

            if (i + 1) % 1000 == 0:
                print(f"Employees inserted: {i + 1}/{max_employees}")

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
        # Use users that aren't already employees - start from where employees ended
        used_user_ids = {emp['user_id'] for emp in employees_data}
        remaining_users = [u for u in available_users if u['id'] not in used_user_ids]

        print(f"Available users for customers: {len(remaining_users)}")

        for i in range(min(NUM_CUSTOMERS, len(remaining_users))):
            user = remaining_users[i]
            customer_type = random.choices(['individual', 'corporate'], weights=[80, 20])[0]
            identification_document = fake.ssn()[:50] if customer_type == 'individual' else fake.ein()[:50]  # VARCHAR(50)
            registration_date = fake.date_between(start_date='-2y', end_date='today')
            city = random.choice(cities_data)
            address = fake.address()  # TEXT field
            credit_limit = round(random.uniform(1000, 50000), 2)  # DECIMAL(12,2)
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
        used_tax_ids = set()  # Track unique tax_ids

        for i in range(NUM_SUPPLIERS):
            company_name = fake.company()[:150]  # VARCHAR(150)

            # Generate unique tax_id using the same logic as codes
            tax_id = generate_unique_code("TAX", used_tax_ids, 6)[:20]  # VARCHAR(20) UNIQUE

            email = fake.company_email()[:150]  # VARCHAR(150)
            phone = fake.phone_number()[:20]  # VARCHAR(20)
            address = fake.address()  # TEXT
            city = random.choice(cities_data)
            contact_name = fake.name()[:100]  # VARCHAR(100)
            contact_phone = fake.phone_number()[:20]  # VARCHAR(20)
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

            if (i + 1) % 500 == 0:
                print(f"Suppliers inserted: {i + 1}/{NUM_SUPPLIERS}")

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
                (category[:100], fake.text(max_nb_chars=200))  # VARCHAR(100) for name
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
            name = f"{fake.word().title()} {parent_category['name']}"[:100]  # VARCHAR(100)

            cursor.execute(
                '''INSERT INTO product_categories (name, description, parent_category_id)
                   VALUES (%s, %s, %s)''',
                (name, fake.text(max_nb_chars=200), parent_category['id'])
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
            code = generate_unique_code("PROD", used_codes, 8)[:50]  # VARCHAR(50)
            name = f"{fake.word().title()} {fake.word().title()}"[:200]  # VARCHAR(200)
            description = fake.text(max_nb_chars=500)  # TEXT
            category = random.choice(categories_data)
            supplier = random.choice([s for s in suppliers_data if s['status'] == 'active'])
            purchase_price = round(random.uniform(10, 500), 2)  # DECIMAL(10,2)
            sale_price = round(purchase_price * random.uniform(1.2, 3.0), 2)  # DECIMAL(10,2)
            current_stock = random.randint(0, 1000)
            minimum_stock = random.randint(5, 50)
            unit = random.choice(units)[:20]  # VARCHAR(20)
            weight = round(random.uniform(0.1, 10.0), 3)  # DECIMAL(8,3)
            dimensions = f"{random.randint(1, 50)}x{random.randint(1, 50)}x{random.randint(1, 50)} cm"[:100]  # VARCHAR(100)
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
                'purchase_price': purchase_price,
                'sale_price': sale_price,
                'current_stock': current_stock,
                'status': status
            })

            if (i + 1) % 1000 == 0:
                print(f"Products inserted: {i + 1}/{NUM_PRODUCTS}")

        conn.commit()
        print(f"Inserted {NUM_PRODUCTS} products\n")

        # 10. Populate warehouses
        warehouses_data = []
        print("Inserting warehouses...")
        for i in range(NUM_WAREHOUSES):
            name = f"Warehouse {fake.city()}"[:100]  # VARCHAR(100)
            address = fake.address()  # TEXT NOT NULL
            city = random.choice(cities_data)
            phone = fake.phone_number()[:20] if random.random() < 0.7 else None  # VARCHAR(20)
            max_capacity = random.randint(1000, 50000)  # INT
            manager = random.choice([e for e in employees_data if 'Manager' in e['position']])
            status = random.choices(['active', 'inactive', 'maintenance'], weights=[85, 10, 5])[0]

            cursor.execute(
                '''INSERT INTO warehouses (name, address, city_id, phone, max_capacity,
                                          manager_employee_id, status)
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
        warehouse_inventory_data = []
        print("Inserting warehouse inventory...")
        for warehouse in warehouses_data:
            # Each warehouse has inventory for 30-70% of products
            num_products = random.randint(int(len(products_data) * 0.3), int(len(products_data) * 0.7))
            warehouse_products = random.sample(products_data, num_products)

            for product in warehouse_products:
                quantity = random.randint(0, 500)
                location = f"A{random.randint(1, 20)}-{random.randint(1, 10)}-{random.randint(1, 50)}"[:50]  # VARCHAR(50)

                cursor.execute(
                    '''INSERT INTO warehouse_inventory (product_id, warehouse_id, quantity, location)
                       VALUES (%s, %s, %s, %s)''',
                    (product['id'], warehouse['id'], quantity, location)
                )

                inventory_id = cursor.lastrowid
                warehouse_inventory_data.append({
                    'id': inventory_id,
                    'product_id': product['id'],
                    'warehouse_id': warehouse['id'],
                    'quantity': quantity
                })

        conn.commit()
        print(f"Inserted {len(warehouse_inventory_data)} warehouse inventory records\n")

        # 12. Populate purchase orders
        purchase_orders_data = []
        print("Inserting purchase orders...")

        # Process in batches to avoid memory issues
        batch_size = 10000
        for batch_start in range(0, NUM_PURCHASE_ORDERS, batch_size):
            batch_end = min(batch_start + batch_size, NUM_PURCHASE_ORDERS)
            batch_orders = []

            for i in range(batch_start, batch_end):
                order_number = generate_unique_code("PO", used_codes, 10)[:50]  # VARCHAR(50)
                supplier = random.choice([s for s in suppliers_data if s['status'] == 'active'])
                employee = random.choice([e for e in employees_data if e['status'] == 'active'])
                order_date = fake.date_between(start_date='-1y', end_date='today')

                # Calculate delivery date (1-30 days after order date)
                delivery_days = random.randint(1, 30)
                estimated_delivery_date = order_date + timedelta(days=delivery_days)

                # Some orders are already delivered
                if random.random() < 0.7:  # 70% delivered
                    actual_delivery_date = estimated_delivery_date + timedelta(days=random.randint(-5, 10))
                    status = 'received'
                else:
                    actual_delivery_date = None
                    status = random.choices(['pending', 'approved', 'shipped', 'cancelled'], weights=[30, 30, 30, 10])[0]

                # Calculate amounts - DECIMAL(12,2)
                subtotal = round(random.uniform(100, 10000), 2)
                taxes = round(subtotal * 0.18, 2)  # 18% tax
                total = round(subtotal + taxes, 2)
                notes = fake.text(max_nb_chars=200) if random.random() < 0.3 else None

                cursor.execute(
                    '''INSERT INTO purchase_orders (order_number, supplier_id, requesting_employee_id,
                                                    order_date, estimated_delivery_date, actual_delivery_date,
                                                    subtotal, taxes, total, status, notes)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (order_number, supplier['id'], employee['id'],
                     order_date, estimated_delivery_date, actual_delivery_date,
                     subtotal, taxes, total, status, notes)
                )
                po_id = cursor.lastrowid
                batch_orders.append({
                    'id': po_id,
                    'number': order_number,
                    'status': status,
                    'supplier_id': supplier['id'],
                    'subtotal': subtotal
                })

            purchase_orders_data.extend(batch_orders)
            conn.commit()
            print(f"Purchase orders inserted: {batch_end}/{NUM_PURCHASE_ORDERS}")

        print(f"Inserted {NUM_PURCHASE_ORDERS} purchase orders\n")

        # 13. Populate purchase order details
        print("Inserting purchase order details...")
        for i, po in enumerate(purchase_orders_data):
            # Each purchase order has 1-5 different products
            num_products = random.randint(1, 5)
            po_products = random.sample([p for p in products_data if p['status'] == 'active'],
                                      min(num_products, len([p for p in products_data if p['status'] == 'active'])))

            for product in po_products:
                quantity = random.randint(1, 100)
                unit_price = round(random.uniform(10, 500), 2)  # DECIMAL(10,2)
                subtotal = round(quantity * unit_price, 2)  # DECIMAL(12,2)

                cursor.execute(
                    '''INSERT INTO purchase_order_details (purchase_order_id, product_id, quantity,
                                                           unit_price, subtotal)
                       VALUES (%s, %s, %s, %s, %s)''',
                    (po['id'], product['id'], quantity, unit_price, subtotal)
                )

            if (i + 1) % 10000 == 0:
                conn.commit()
                print(f"Purchase order details processed: {i + 1}/{len(purchase_orders_data)}")

        conn.commit()
        print(f"Inserted purchase order details for all orders\n")

        # 14. Populate sales
        sales_data = []
        print("Inserting sales...")
        payment_methods = ['cash', 'credit_card', 'debit_card', 'transfer', 'credit']

        for i in range(NUM_SALES):
            sale_number = generate_unique_code("S", used_codes, 10)[:50]  # VARCHAR(50)
            customer = random.choice([c for c in customers_data if c['status'] == 'active'])
            employee = random.choice([e for e in employees_data if e['status'] == 'active'])
            sale_date = fake.date_time_between(start_date='-6m', end_date='now')
            payment_method = random.choice(payment_methods)

            # Calculate amounts - DECIMAL(12,2)
            subtotal = round(random.uniform(50, 2000), 2)
            discount = round(subtotal * random.uniform(0, 0.2), 2) if random.random() < 0.3 else 0.00  # 30% chance of discount
            taxes = round(subtotal * 0.18, 2)  # 18% tax
            total = round(subtotal + taxes - discount, 2)
            notes = fake.text(max_nb_chars=200) if random.random() < 0.2 else None

            status = random.choices(['completed', 'cancelled', 'returned'], weights=[90, 5, 5])[0]

            cursor.execute(
                '''INSERT INTO sales (sale_number, customer_id, salesperson_employee_id, sale_date,
                                     subtotal, discount, taxes, total, payment_method, status, notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (sale_number, customer['id'], employee['id'], sale_date,
                 subtotal, discount, taxes, total, payment_method, status, notes)
            )
            sale_id = cursor.lastrowid
            sales_data.append({
                'id': sale_id,
                'number': sale_number,
                'customer_id': customer['id'],
                'status': status,
                'total': total
            })

            if (i + 1) % 1000 == 0:
                print(f"Sales inserted: {i + 1}/{NUM_SALES}")

        conn.commit()
        print(f"Inserted {NUM_SALES} sales\n")

        # 15. Populate sales details
        print("Inserting sales details...")
        for i, sale in enumerate(sales_data):
            # Each sale has 1-3 different products
            num_products = random.randint(1, 3)
            sale_products = random.sample([p for p in products_data if p['status'] == 'active' and p['current_stock'] > 0],
                                        min(num_products, len([p for p in products_data if p['status'] == 'active' and p['current_stock'] > 0])))

            for product in sale_products:
                quantity = random.randint(1, min(10, product['current_stock']))
                unit_price = round(product['sale_price'] * random.uniform(0.9, 1.1), 2)  # DECIMAL(10,2)
                unit_discount = round(unit_price * random.uniform(0, 0.1), 2) if random.random() < 0.2 else 0.00  # DECIMAL(10,2)
                subtotal = round((unit_price - unit_discount) * quantity, 2)  # DECIMAL(12,2)

                cursor.execute(
                    '''INSERT INTO sale_details (sale_id, product_id, quantity, unit_price, unit_discount, subtotal)
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (sale['id'], product['id'], quantity, unit_price, unit_discount, subtotal)
                )

            if (i + 1) % 1000 == 0:
                conn.commit()
                print(f"Sales details processed: {i + 1}/{len(sales_data)}")

        conn.commit()
        print(f"Inserted sales details for all sales\n")

        # 16. Populate inventory movements
        inventory_movements_data = []
        print("Inserting inventory movements...")
        movement_types = ['in', 'out', 'adjustment', 'transfer']
        reference_types = ['sale', 'purchase', 'adjustment', 'transfer']

        for i in range(NUM_SALES * 2):  # 2 movements per sale on average
            product = random.choice(products_data)
            warehouse = random.choice([w for w in warehouses_data if w['status'] == 'active'])
            movement_type = random.choice(movement_types)
            reference_type = random.choice(reference_types)
            quantity = random.randint(1, 50)
            employee = random.choice([e for e in employees_data if e['status'] == 'active'])
            notes = fake.text(max_nb_chars=200) if random.random() < 0.3 else None
            movement_date = fake.date_time_between(start_date='-6m', end_date='now')
            reference_id = random.choice(sales_data)['id'] if reference_type == 'sale' else None

            cursor.execute(
                '''INSERT INTO inventory_movements (product_id, warehouse_id, movement_type, quantity,
                                                   reference_type, reference_id, employee_id, notes, movement_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (product['id'], warehouse['id'], movement_type, quantity, reference_type,
                 reference_id, employee['id'], notes, movement_date)
            )

            inventory_movements_data.append({
                'id': cursor.lastrowid,
                'product_id': product['id'],
                'warehouse_id': warehouse['id']
            })

        conn.commit()
        print(f"Inserted {len(inventory_movements_data)} inventory movements\n")

        # 17. Populate accounts receivable
        accounts_receivable_data = []
        print("Inserting accounts receivable...")
        credit_sales = [s for s in sales_data if s['status'] == 'completed']

        for sale in credit_sales[:int(len(credit_sales) * 0.3)]:  # 30% of sales have credit
            customer_id = sale['customer_id']
            total_amount = sale['total']
            # Some accounts are partially paid
            if random.random() < 0.6:  # 60% fully pending
                pending_amount = total_amount
                status = 'pending'
            elif random.random() < 0.8:  # 20% partially paid
                pending_amount = round(total_amount * random.uniform(0.3, 0.9), 2)
                status = 'partial'
            else:  # 20% fully paid
                pending_amount = 0.00
                status = 'paid'

            due_date = fake.date_between(start_date='today', end_date='+60d')
            days_overdue = max(0, (datetime.now().date() - due_date).days) if pending_amount > 0 else 0
            if days_overdue > 0:
                status = 'overdue'

            cursor.execute(
                '''INSERT INTO accounts_receivable (sale_id, customer_id, total_amount, pending_amount,
                                                   due_date, days_overdue, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (sale['id'], customer_id, total_amount, pending_amount, due_date, days_overdue, status)
            )

            accounts_receivable_data.append({
                'id': cursor.lastrowid,
                'sale_id': sale['id'],
                'customer_id': customer_id,
                'total_amount': total_amount,
                'pending_amount': pending_amount,
                'status': status
            })

        conn.commit()
        print(f"Inserted {len(accounts_receivable_data)} accounts receivable\n")

        # 18. Populate payments received
        payments_received_data = []
        print("Inserting payments received...")
        payment_methods_received = ['cash', 'credit_card', 'debit_card', 'transfer', 'check']

        for ar in accounts_receivable_data:
            if ar['status'] in ['paid', 'partial']:
                num_payments = random.randint(1, 3)
                remaining_amount = ar['total_amount'] - ar['pending_amount']

                for _ in range(num_payments):
                    if remaining_amount <= 0:
                        break

                    if num_payments == 1:
                        payment_amount = remaining_amount
                    else:
                        payment_amount = round(remaining_amount * random.uniform(0.3, 0.8), 2)

                    payment_method = random.choice(payment_methods_received)
                    reference_number = f"REF{random.randint(100000, 999999)}" if payment_method in ['transfer', 'check'] else None
                    payment_date = fake.date_time_between(start_date='-3m', end_date='now')
                    receiving_employee = random.choice([e for e in employees_data if e['status'] == 'active'])
                    notes = fake.text(max_nb_chars=100) if random.random() < 0.2 else None

                    cursor.execute(
                        '''INSERT INTO payments_received (accounts_receivable_id, payment_amount, payment_method,
                                                         reference_number, payment_date, receiving_employee_id, notes)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (ar['id'], payment_amount, payment_method, reference_number,
                         payment_date, receiving_employee['id'], notes)
                    )

                    payments_received_data.append({
                        'id': cursor.lastrowid,
                        'accounts_receivable_id': ar['id'],
                        'payment_amount': payment_amount
                    })

                    remaining_amount -= payment_amount

        conn.commit()
        print(f"Inserted {len(payments_received_data)} payments received\n")

        # 19. Populate returns
        returns_data = []
        print("Inserting returns...")

        # Returns are based on completed sales
        completed_sales = [s for s in sales_data if s['status'] == 'completed']

        for i in range(min(NUM_RETURNS, len(completed_sales))):
            sale = random.choice(completed_sales)
            return_number = generate_unique_code("R", used_codes, 10)[:50]  # VARCHAR(50)
            return_date = fake.date_time_between(start_date='-6m', end_date='now')
            reason = fake.text(max_nb_chars=300)  # TEXT field
            total_returned = round(sale['total'] * random.uniform(0.1, 1.0), 2)  # DECIMAL(12,2)
            status = random.choices(['approved', 'rejected', 'pending', 'processed'], weights=[60, 10, 20, 10])[0]

            # Get customer from sale
            customer_id = sale['customer_id']
            authorizing_employee = random.choice([e for e in employees_data if e['status'] == 'active'])

            cursor.execute(
                '''INSERT INTO returns (return_number, sale_id, customer_id, authorizing_employee_id,
                                       return_date, reason, total_returned, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (return_number, sale['id'], customer_id, authorizing_employee['id'],
                 return_date, reason, total_returned, status)
            )
            return_id = cursor.lastrowid
            returns_data.append({
                'id': return_id,
                'number': return_number,
                'sale_id': sale['id']
            })

            # Remove the sale from available sales to avoid duplicate returns
            completed_sales.remove(sale)

        conn.commit()
        print(f"Inserted {len(returns_data)} returns\n")

        # 20. Populate return details
        return_details_data = []
        print("Inserting return details...")
        product_conditions = ['new', 'used', 'damaged']

        for return_record in returns_data:
            # Each return has 1-3 products returned
            num_products = random.randint(1, 3)
            return_products = random.sample([p for p in products_data if p['status'] == 'active'], num_products)

            for product in return_products:
                quantity_returned = random.randint(1, 5)
                unit_price = round(product['sale_price'] * random.uniform(0.9, 1.1), 2)  # DECIMAL(10,2)
                subtotal_returned = round(unit_price * quantity_returned, 2)  # DECIMAL(12,2)
                product_condition = random.choice(product_conditions)

                cursor.execute(
                    '''INSERT INTO return_details (return_id, product_id, quantity_returned, unit_price,
                                                  subtotal_returned, product_condition)
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (return_record['id'], product['id'], quantity_returned, unit_price,
                     subtotal_returned, product_condition)
                )

                return_details_data.append({
                    'id': cursor.lastrowid,
                    'return_id': return_record['id'],
                    'product_id': product['id']
                })

        conn.commit()
        print(f"Inserted {len(return_details_data)} return details\n")

        print("=== DATABASE POPULATION COMPLETED SUCCESSFULLY ===")
        print(f"Summary:")
        print(f"- Countries: {len(countries_data)}")
        print(f"- Regions: {len(regions_data)}")
        print(f"- Cities: {len(cities_data)}")
        print(f"- Users: {len(users_data)}")
        print(f"- Employees: {len(employees_data)}")
        print(f"- Customers: {len(customers_data)}")
        print(f"- Suppliers: {len(suppliers_data)}")
        print(f"- Categories: {len(categories_data)}")
        print(f"- Products: {len(products_data)}")
        print(f"- Warehouses: {len(warehouses_data)}")
        print(f"- Warehouse Inventory: {len(warehouse_inventory_data)}")
        print(f"- Purchase Orders: {len(purchase_orders_data)}")
        print(f"- Sales: {len(sales_data)}")
        print(f"- Inventory Movements: {len(inventory_movements_data)}")
        print(f"- Accounts Receivable: {len(accounts_receivable_data)}")
        print(f"- Payments Received: {len(payments_received_data)}")
        print(f"- Returns: {len(returns_data)}")
        print(f"- Return Details: {len(return_details_data)}")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
