CREATE DATABASE IF NOT EXISTS greenery;
USE greenery;

-- 1. Categories Table (For filtering by plant types)
CREATE TABLE IF NOT EXISTS Categories (
    categoryID INT AUTO_INCREMENT PRIMARY KEY,
    categoryName VARCHAR(100) NOT NULL,
    description TEXT
);

-- 2. Users Table (Includes Remember Me functionality)
CREATE TABLE IF NOT EXISTS user_base(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
); 

-- 3. Plants Table (Includes attributes for filtering/browse page)
CREATE TABLE IF NOT EXISTS Plants (
    plantID INT AUTO_INCREMENT PRIMARY KEY,
    commonName VARCHAR(100) NOT NULL,
    scientificName VARCHAR(100),
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stockQuantity INT DEFAULT 0,
    imageUrl VARCHAR(255),
    categoryID INT,
    difficultyLevel ENUM('Beginner', 'Intermediate', 'Expert'),
    isAirCleaner BOOLEAN DEFAULT FALSE,
    lightRequirement ENUM('Low', 'Medium', 'Bright Indirect', 'Direct Sunlight'),
    isPetFriendly BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID)
);
-- 4. Favorites Table (Includes the custom Notes feature)
CREATE TABLE IF NOT EXISTS Favorites (
    favoriteID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    plantID INT,
    personalNotes TEXT, -- "Ensures users easily remember why they saved a plant"
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (plantID) REFERENCES Plants(plantID)
);

-- 5. Cart Table (Includes the Gift option)
CREATE TABLE IF NOT EXISTS Cart (
    cartID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    isGift BOOLEAN DEFAULT FALSE, -- From the Cart page layout
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

-- 6. Cart Items
CREATE TABLE IF NOT EXISTS Cart_Items (
    cartItemID INT AUTO_INCREMENT PRIMARY KEY,
    cartID INT,
    plantID INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (cartID) REFERENCES Cart(cartID) ON DELETE CASCADE,
    FOREIGN KEY (plantID) REFERENCES Plants(plantID)
);
-- 7. Orders Table (Final Transaction)
CREATE TABLE IF NOT EXISTS Orders (
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    totalAmount DECIMAL(10, 2),
    orderStatus VARCHAR(50) DEFAULT 'Pending',
    isGift BOOLEAN DEFAULT FALSE,
    shippingAddressAtTime TEXT,
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

-- 8. Order Items (Snapshot of price at purchase)
CREATE TABLE IF NOT EXISTS Order_Items (
    orderItemID INT AUTO_INCREMENT PRIMARY KEY,
    orderID INT,
    plantID INT,
    quantity INT,
    priceAtPurchase DECIMAL(10, 2),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID),
    FOREIGN KEY (plantID) REFERENCES Plants(plantID)
);

-- 9. Contact Submissions
CREATE TABLE IF NOT EXISTS Contact_Submissions (
    submissionID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    topic VARCHAR(100),
    messageText TEXT
);