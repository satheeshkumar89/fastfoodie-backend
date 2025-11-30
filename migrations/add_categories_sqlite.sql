-- SQLite Migration: Add Categories Table and Update Menu Items
-- Date: 2025-11-26

-- Step 1: Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    icon VARCHAR(255),
    is_active BOOLEAN DEFAULT 1,
    display_order INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_categories_id ON categories (id);
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories (name);

-- Step 2: Insert 60 predefined categories
INSERT OR IGNORE INTO categories (id, name, display_order, is_active) VALUES
(1, 'Beverages', 1, 1),
(2, 'Breakfast', 2, 1),
(3, 'Biryani', 3, 1),
(4, 'Burgers', 4, 1),
(5, 'Chinese', 5, 1),
(6, 'North Indian', 6, 1),
(7, 'South Indian', 7, 1),
(8, 'Pizzas', 8, 1),
(9, 'Desserts', 9, 1),
(10, 'Salads', 10, 1),
(11, 'Snacks', 11, 1),
(12, 'Seafood', 12, 1),
(13, 'BBQ & Grill', 13, 1),
(14, 'Healthy Food', 14, 1),
(15, 'Combos & Meals', 15, 1),
(16, 'Pure Veg', 16, 1),
(17, 'Ice Creams', 17, 1),
(18, 'Indian Breads', 18, 1),
(19, 'Thali', 19, 1),
(20, 'Rice Bowls', 20, 1),
(21, 'Pasta', 21, 1),
(22, 'Sandwiches', 22, 1),
(23, 'Wraps & Rolls', 23, 1),
(24, 'Shawarma', 24, 1),
(25, 'Momos', 25, 1),
(26, 'Fried Rice & Noodles', 26, 1),
(27, 'Chaat', 27, 1),
(28, 'Sweets', 28, 1),
(29, 'Bakery', 29, 1),
(30, 'Tandoori', 30, 1),
(31, 'Kebabs', 31, 1),
(32, 'Gravy Dishes', 32, 1),
(33, 'Soups', 33, 1),
(34, 'Starters', 34, 1),
(35, 'Curries', 35, 1),
(36, 'Juices', 36, 1),
(37, 'Shakes', 37, 1),
(38, 'Tea & Coffee', 38, 1),
(39, 'Appetizers', 39, 1),
(40, 'Gujarati', 40, 1),
(41, 'Rajasthani', 41, 1),
(42, 'Andhra', 42, 1),
(43, 'Hyderabadi', 43, 1),
(44, 'Punjabi', 44, 1),
(45, 'Mughlai', 45, 1),
(46, 'Arabian', 46, 1),
(47, 'Thai', 47, 1),
(48, 'Japanese', 48, 1),
(49, 'Korean', 49, 1),
(50, 'Italian', 50, 1),
(51, 'Mexican', 51, 1),
(52, 'American', 52, 1),
(53, 'Mediterranean', 53, 1),
(54, 'Street Food', 54, 1),
(55, 'Organic', 55, 1),
(56, 'Vegan', 56, 1),
(57, 'Jain Friendly', 57, 1),
(58, 'Kids Menu', 58, 1),
(59, 'Party Packs', 59, 1),
(60, 'Weekend Specials', 60, 1);

-- Step 3: Add category_id column to menu_items (if not exists)
-- SQLite doesn't support ALTER TABLE ADD COLUMN IF NOT EXISTS directly
-- So we check if column exists first via a separate query

-- For now, we'll use a workaround: create new table with correct schema
-- and copy data over

-- Create new menu_items table with category_id
CREATE TABLE IF NOT EXISTS menu_items_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    category_id INTEGER,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    discount_price DECIMAL(10, 2),
    image_url VARCHAR(500),
    is_vegetarian BOOLEAN,
    is_available BOOLEAN,
    preparation_time INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY(restaurant_id) REFERENCES restaurants (id),
    FOREIGN KEY(category_id) REFERENCES categories (id)
);

-- Copy data from old table to new table, mapping category strings to IDs
INSERT INTO menu_items_new (
    id, restaurant_id, category_id, name, description, price, 
    discount_price, image_url, is_vegetarian, is_available, 
    preparation_time, created_at, updated_at
)
SELECT 
    m.id,
    m.restaurant_id,
    c.id as category_id,
    m.name,
    m.description,
    m.price,
    m.discount_price,
    m.image_url,
    m.is_vegetarian,
    m.is_available,
    m.preparation_time,
    m.created_at,
    m.updated_at
FROM menu_items m
LEFT JOIN categories c ON LOWER(m.category) = LOWER(c.name);

-- Drop old table
DROP TABLE menu_items;

-- Rename new table to menu_items
ALTER TABLE menu_items_new RENAME TO menu_items;

-- Recreate index
CREATE INDEX ix_menu_items_id ON menu_items (id);

-- Verification
SELECT 'Categories created:' as status, COUNT(*) as count FROM categories;
SELECT 'Menu items migrated:' as status, COUNT(*) as count FROM menu_items;
