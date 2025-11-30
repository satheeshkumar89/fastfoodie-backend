-- Migration: Add Categories Table and Update Menu Items
-- Date: 2025-11-26
-- Description: Creates categories table, seeds with 60 categories, and updates menu_items

-- Step 1: Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    icon VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_categories_id (id),
    INDEX idx_categories_name (name)
);

-- Step 2: Insert 60 predefined categories
INSERT INTO categories (id, name, display_order, is_active) VALUES
(1, 'Beverages', 1, TRUE),
(2, 'Breakfast', 2, TRUE),
(3, 'Biryani', 3, TRUE),
(4, 'Burgers', 4, TRUE),
(5, 'Chinese', 5, TRUE),
(6, 'North Indian', 6, TRUE),
(7, 'South Indian', 7, TRUE),
(8, 'Pizzas', 8, TRUE),
(9, 'Desserts', 9, TRUE),
(10, 'Salads', 10, TRUE),
(11, 'Snacks', 11, TRUE),
(12, 'Seafood', 12, TRUE),
(13, 'BBQ & Grill', 13, TRUE),
(14, 'Healthy Food', 14, TRUE),
(15, 'Combos & Meals', 15, TRUE),
(16, 'Pure Veg', 16, TRUE),
(17, 'Ice Creams', 17, TRUE),
(18, 'Indian Breads', 18, TRUE),
(19, 'Thali', 19, TRUE),
(20, 'Rice Bowls', 20, TRUE),
(21, 'Pasta', 21, TRUE),
(22, 'Sandwiches', 22, TRUE),
(23, 'Wraps & Rolls', 23, TRUE),
(24, 'Shawarma', 24, TRUE),
(25, 'Momos', 25, TRUE),
(26, 'Fried Rice & Noodles', 26, TRUE),
(27, 'Chaat', 27, TRUE),
(28, 'Sweets', 28, TRUE),
(29, 'Bakery', 29, TRUE),
(30, 'Tandoori', 30, TRUE),
(31, 'Kebabs', 31, TRUE),
(32, 'Gravy Dishes', 32, TRUE),
(33, 'Soups', 33, TRUE),
(34, 'Starters', 34, TRUE),
(35, 'Curries', 35, TRUE),
(36, 'Juices', 36, TRUE),
(37, 'Shakes', 37, TRUE),
(38, 'Tea & Coffee', 38, TRUE),
(39, 'Appetizers', 39, TRUE),
(40, 'Gujarati', 40, TRUE),
(41, 'Rajasthani', 41, TRUE),
(42, 'Andhra', 42, TRUE),
(43, 'Hyderabadi', 43, TRUE),
(44, 'Punjabi', 44, TRUE),
(45, 'Mughlai', 45, TRUE),
(46, 'Arabian', 46, TRUE),
(47, 'Thai', 47, TRUE),
(48, 'Japanese', 48, TRUE),
(49, 'Korean', 49, TRUE),
(50, 'Italian', 50, TRUE),
(51, 'Mexican', 51, TRUE),
(52, 'American', 52, TRUE),
(53, 'Mediterranean', 53, TRUE),
(54, 'Street Food', 54, TRUE),
(55, 'Organic', 55, TRUE),
(56, 'Vegan', 56, TRUE),
(57, 'Jain Friendly', 57, TRUE),
(58, 'Kids Menu', 58, TRUE),
(59, 'Party Packs', 59, TRUE),
(60, 'Weekend Specials', 60, TRUE);

-- Step 3: Add category_id column to menu_items
ALTER TABLE menu_items 
ADD COLUMN category_id INT NULL AFTER restaurant_id,
ADD CONSTRAINT fk_menu_items_category_id 
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL;

-- Step 4: Migrate existing category strings to category IDs (best effort)
-- This matches category names case-insensitively
UPDATE menu_items m
JOIN categories c ON LOWER(m.category) = LOWER(c.name)
SET m.category_id = c.id
WHERE m.category IS NOT NULL;

-- Step 5: Drop the old category column (OPTIONAL - uncomment if you want to remove it)
-- ALTER TABLE menu_items DROP COLUMN category;

-- Verification queries
SELECT 'Categories created:' as status, COUNT(*) as count FROM categories;
SELECT 'Menu items with category_id:' as status, COUNT(*) as count FROM menu_items WHERE category_id IS NOT NULL;
