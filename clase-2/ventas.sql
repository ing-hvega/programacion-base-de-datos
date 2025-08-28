-- Complete sales system database
-- Created to be used with faker_ventas.py

DROP DATABASE IF EXISTS sales_system;
CREATE DATABASE sales_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sales_system;

-- Table 1: Countries
CREATE TABLE countries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    iso_code VARCHAR(3) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Regions/States
CREATE TABLE regions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

-- Table 3: Cities
CREATE TABLE cities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    region_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

-- Table 4: System users
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table 5: Employees
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    employee_code VARCHAR(20) NOT NULL UNIQUE,
    position VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2),
    hire_date DATE NOT NULL,
    city_id INT NOT NULL,
    manager_id INT NULL,
    commission_percentage DECIMAL(5,2) DEFAULT 0.00,
    status ENUM('active', 'inactive', 'leave') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

-- Table 6: Customers
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    customer_type ENUM('individual', 'corporate') NOT NULL,
    identification_document VARCHAR(50) NOT NULL,
    registration_date DATE NOT NULL,
    city_id INT NOT NULL,
    address TEXT,
    credit_limit DECIMAL(12,2) DEFAULT 0.00,
    assigned_employee_id INT,
    status ENUM('active', 'inactive', 'delinquent') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (assigned_employee_id) REFERENCES employees(id)
);

-- Table 7: Suppliers
CREATE TABLE suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(150) NOT NULL,
    tax_id VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city_id INT NOT NULL,
    contact_name VARCHAR(100),
    contact_phone VARCHAR(20),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

-- Table 8: Product categories
CREATE TABLE product_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_category_id INT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES product_categories(id)
);

-- Table 9: Products
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,
    purchase_price DECIMAL(10,2) NOT NULL,
    sale_price DECIMAL(10,2) NOT NULL,
    current_stock INT DEFAULT 0,
    minimum_stock INT DEFAULT 0,
    unit_of_measure VARCHAR(20) DEFAULT 'unit',
    weight DECIMAL(8,3),
    dimensions VARCHAR(100),
    status ENUM('active', 'discontinued', 'out_of_stock') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES product_categories(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- Table 10: Warehouses
CREATE TABLE warehouses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city_id INT NOT NULL,
    phone VARCHAR(20),
    max_capacity INT,
    manager_employee_id INT,
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (manager_employee_id) REFERENCES employees(id)
);

-- Table 11: Warehouse inventory
CREATE TABLE warehouse_inventory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    location VARCHAR(50),
    last_movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_product_warehouse (product_id, warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- Table 12: Purchase orders
CREATE TABLE purchase_orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    supplier_id INT NOT NULL,
    requesting_employee_id INT NOT NULL,
    order_date DATE NOT NULL,
    estimated_delivery_date DATE,
    actual_delivery_date DATE NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    taxes DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    status ENUM('pending', 'approved', 'shipped', 'received', 'cancelled') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (requesting_employee_id) REFERENCES employees(id)
);

-- Table 13: Purchase order details
CREATE TABLE purchase_order_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    purchase_order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Table 14: Sales
CREATE TABLE sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    salesperson_employee_id INT NOT NULL,
    sale_date DATETIME NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    discount DECIMAL(12,2) DEFAULT 0.00,
    taxes DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card', 'transfer', 'credit') NOT NULL,
    status ENUM('pending', 'completed', 'cancelled', 'returned') DEFAULT 'completed',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (salesperson_employee_id) REFERENCES employees(id)
);

-- Table 15: Sales details
CREATE TABLE sale_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    unit_discount DECIMAL(10,2) DEFAULT 0.00,
    subtotal DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Table 16: Inventory movements
CREATE TABLE inventory_movements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    movement_type ENUM('in', 'out', 'adjustment', 'transfer') NOT NULL,
    quantity INT NOT NULL,
    reference_type ENUM('sale', 'purchase', 'adjustment', 'transfer') NOT NULL,
    reference_id INT,
    employee_id INT NOT NULL,
    notes TEXT,
    movement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Table 17: Accounts receivable
CREATE TABLE accounts_receivable (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    customer_id INT NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    pending_amount DECIMAL(12,2) NOT NULL,
    due_date DATE NOT NULL,
    days_overdue INT DEFAULT 0,
    status ENUM('pending', 'paid', 'overdue', 'partial') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Table 18: Payments received
CREATE TABLE payments_received (
    id INT PRIMARY KEY AUTO_INCREMENT,
    accounts_receivable_id INT NOT NULL,
    payment_amount DECIMAL(12,2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card', 'transfer', 'check') NOT NULL,
    reference_number VARCHAR(100),
    payment_date DATETIME NOT NULL,
    receiving_employee_id INT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (accounts_receivable_id) REFERENCES accounts_receivable(id),
    FOREIGN KEY (receiving_employee_id) REFERENCES employees(id)
);

-- Table 19: Returns
CREATE TABLE returns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    return_number VARCHAR(50) NOT NULL UNIQUE,
    sale_id INT NOT NULL,
    customer_id INT NOT NULL,
    authorizing_employee_id INT NOT NULL,
    return_date DATETIME NOT NULL,
    reason TEXT NOT NULL,
    total_returned DECIMAL(12,2) NOT NULL,
    status ENUM('pending', 'approved', 'rejected', 'processed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (authorizing_employee_id) REFERENCES employees(id)
);

-- Table 20: Return details
CREATE TABLE return_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    return_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity_returned INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal_returned DECIMAL(12,2) NOT NULL,
    product_condition ENUM('new', 'used', 'damaged') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (return_id) REFERENCES returns(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
