# How to Run the Project Locally

Follow these instructions to set up the environment, configure the database, and run the application on your local machine.

## Prerequisites

Ensure you have the following installed before proceeding:
* **Python 3.8+**
* **MySQL** (via phpMyAdmin or your preferred database manager)
* **Git** (optional, for cloning the repository)

---

## 1. Setup the Repository and Environment

Clone the repository to your local machine and navigate into the project folder.

Next, create and activate a Python virtual environment:

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Inside the .venv folder find the pyvenv.cfg file and paste these in:

```bash
include-system-site-packages = false
version = 3.14.0
implementation = CPython
prompt = greenery-project
uv = 0.9.5
```

---

## 2. Install Dependencies

Ensure your package manager (`pip`) is up-to-date:
```bash
python -m pip install --upgrade pip
```

Install all required packages from the `requirements.txt` file, along with the `uv` package manager needed to run the application:
```bash
pip install -r requirements.txt
pip install uv
```

---

## 3. Configure the Database

1. Open **phpMyAdmin** (or your MySQL interface).
2. Create a new database named **`greenery`**.
3. Open an SQL query window on the new `greenery` database and execute the following queries to populate the initial categories and plant data:

```sql
INSERT INTO Categories (categoryID, categoryName, description) VALUES
(1, 'Lush Everyday Foliage', 'Classic, leafy green companions perfect for brightening up any living space.'),
(2, 'Desert Conquerors & Cacti', 'Fierce, sun-worshipping succulents and cacti that thrive on neglect.'),
(3, 'Moisture-Loving Ferns', 'Delicate, arching fronds that love a good misting and humid environments.'),
(4, 'Dramatic Vines & Trailing', 'Cascading beauties and theatrical vines that love to hang around and show off.'),
(5, 'Zen Masters & Specialty', 'Ancient bonsai, lucky bamboo, and other unique plants that demand respect and bring peace.');

INSERT INTO Plants (
    plantName, 
    description, 
    price, 
    stockQuantity, 
    imageUrl, 
    categoryID, 
    plantSize, 
    isAirCleaner, 
    lightRequirement, 
    isPetFriendly
) VALUES 
('Snake Plant', 'A nearly indestructible plant known for purifying the air.', 25.00, 50, 'snake_plant.jpg', 1, 'Large', TRUE, 'Low', FALSE),
('Spider Plant', 'Fun, easy to grow, and entirely safe for your furry friends.', 15.50, 40, 'spider_plant.jpg', 1, 'Medium', TRUE, 'Bright Indirect', TRUE),
('ZZ Plant', 'Thrives on neglect and tolerates very low light.', 30.00, 25, 'zz_plant.jpg', 1, 'Medium', TRUE, 'Low', FALSE),
('Monstera Deliciosa', 'The famous Swiss Cheese plant. A stunning statement piece.', 45.00, 15, 'monstera.jpg', 1, 'Large', TRUE, 'Bright Indirect', FALSE),
('Boston Fern', 'Classic fern with graceful, arching fronds.', 20.00, 30, 'boston_fern.jpg', 3, 'Medium', TRUE, 'Medium', TRUE),
('Aloe Vera', 'Handy medicinal succulent that loves the sun.', 12.00, 60, 'aloe_vera.jpg', 2, 'Small', TRUE, 'Direct Sunlight', FALSE),
('Peace Lily', 'Features beautiful white blooms and excellent air filtering.', 28.00, 20, 'peace_lily.jpg', 1, 'Medium', TRUE, 'Low', FALSE),
('String of Pearls', 'A beautiful cascading succulent.', 18.00, 35, 'string_of_pearls.jpg', 4, 'Small', FALSE, 'Bright Indirect', FALSE),
('Genghis Khan', 'A fiercely resilient, heavily armored cactus that will conquer your living room. Thrives on neglect and demands absolute territory.', 89.99, 1, 'genghis_khan.jpg', 2, 'Ultra Large', FALSE, 'Direct Sunlight', FALSE),
('The Opossum Vine', 'A highly dramatic, nocturnal-leaning vine. It will absolutely "play dead" and collapse if you are one day late on watering, but miraculously resurrects an hour after a good soak.', 16.50, 30, 'opossum_plant.jpg', 4, 'Medium', TRUE, 'Low', TRUE),
('Lucky Bamboo', 'Brings good fortune and unparalleled zen to your desk. Extremely low-maintenance and virtually indestructible unless watered with pure spite.', 19.99, 100, 'bamboo.jpg', 5, 'Small', TRUE, 'Low', FALSE),
('Zen Master Bonsai', 'Requires the patience of a monk and the precision of a surgeon. Will judge your life choices silently, but might just outlive you if treated with respect.', 65.00, 5, 'bonsai.jpg', 5, 'Small', TRUE, 'Bright Indirect', FALSE),
('The Feline Party Starter', 'Officially known as Catnip, but we just call it the Cat Plant. Side effects for your furry roommate include midnight zoomies, intense staring at blank walls, and purring at airplane decibels.', 12.99, 42, 'cat_plant.jpg', 1, 'Small', FALSE, 'Bright Indirect', TRUE),
('Fiddle Leaf Fig', 'A popular statement plant with large, heavily veined, violin-shaped leaves.', 55.00, 12, 'fiddle_leaf.jpg', 1, 'Large', TRUE, 'Bright Indirect', FALSE),
('Golden Pothos', 'An incredibly forgiving trailing vine that grows quickly and is nearly impossible to kill.', 14.99, 45, 'pothos.jpg', 4, 'Small', TRUE, 'Low', FALSE),
('Rubber Tree', 'Features striking, glossy, burgundy-green leaves. An excellent air purifier.', 35.00, 20, 'rubber_tree.jpg', 1, 'Medium', TRUE, 'Bright Indirect', FALSE),
('Bird''s Nest Fern', 'A tropical fern with crinkly, apple-green fronds. Loves humidity and is totally pet safe.', 22.50, 25, 'birds_nest_fern.jpg', 3, 'Medium', TRUE, 'Medium', TRUE),
('Jade Plant', 'A classic succulent with thick, woody stems and oval-shaped leaves. Symbolizes good luck.', 18.00, 30, 'jade_plant.jpg', 2, 'Small', FALSE, 'Direct Sunlight', FALSE),
('Calathea Medallion', 'Famous for its stunning patterned leaves that fold up at night like hands in prayer.', 28.00, 15, 'calathea.jpg', 1, 'Medium', TRUE, 'Medium', TRUE),
('English Ivy', 'A classic, elegant trailing plant that looks beautiful hanging from a bookshelf or basket.', 16.50, 40, 'english_ivy.jpg', 4, 'Small', TRUE, 'Bright Indirect', FALSE),
('Parlor Palm', 'A lush, bushy palm that brings a tropical feel indoors. Safe for cats and dogs.', 42.00, 10, 'parlor_palm.jpg', 1, 'Large', TRUE, 'Medium', TRUE),
('Cast Iron Plant', 'True to its name, this plant can survive almost anything, including extreme low light.', 32.00, 18, 'cast_iron.jpg', 1, 'Medium', TRUE, 'Low', TRUE),
('Maidenhair Fern', 'Delicate, fan-shaped leaves on wiry black stems. Requires consistent moisture.', 24.00, 20, 'maidenhair.jpg', 3, 'Small', TRUE, 'Bright Indirect', TRUE),
('Meyer Lemon Tree', 'A beautiful indoor citrus tree that produces fragrant white blossoms and real, edible lemons. Thrives in bright, sunny spots.', 65.00, 8, 'lemon_tree.jpg', 5, 'Large', TRUE, 'Direct Sunlight', FALSE),
('Monstera Adansonii', 'A striking trailing vine with unique perforated leaves. Grows quickly in the right conditions.', 24.50, 25, 'monstera_adansonii.jpg', 4, 'Medium', TRUE, 'Bright Indirect', FALSE),
('ZZ Raven', 'A stunning variation of the classic ZZ plant with deep purple, nearly black foliage. Extremely low maintenance.', 45.00, 15, 'zz_raven.jpg', 1, 'Medium', TRUE, 'Low', FALSE),
('Chinese Money Plant', 'Also known as Pilea, featuring perfectly round, coin-shaped leaves on delicate stems.', 19.99, 40, 'pilea.jpg', 1, 'Small', TRUE, 'Bright Indirect', TRUE),
('Zebra Succulent', 'A compact succulent with thick, dark green leaves covered in white, raised stripes.', 12.50, 50, 'zebra_haworthia.jpg', 2, 'Small', FALSE, 'Bright Indirect', TRUE),
('Philodendron Birkin', 'A beautiful compact plant with dark green leaves and striking white pinstripe variegation.', 29.00, 20, 'philodendron_birkin.jpg', 1, 'Small', TRUE, 'Bright Indirect', FALSE),
('Staghorn Fern', 'An epiphytic fern with dramatic fronds that resemble deer antlers. Can be mounted on wood.', 38.00, 12, 'staghorn_fern.jpg', 3, 'Medium', TRUE, 'Medium', TRUE),
('String of Hearts', 'A delicate trailing succulent with heart-shaped leaves patterned with silver and pale green.', 22.00, 30, 'string_of_hearts.jpg', 4, 'Small', FALSE, 'Bright Indirect', TRUE),
('Burro''s Tail', 'A fascinating succulent with thick, trailing stems covered in pale green, plump leaves.', 26.50, 18, 'burros_tail.jpg', 2, 'Medium', FALSE, 'Direct Sunlight', TRUE),
('Dragon Tree', 'A striking structural plant with long, spiky green leaves edged in red. Great for tight spaces.', 34.00, 10, 'dragon_tree.jpg', 1, 'Large', TRUE, 'Medium', FALSE),
('Anthurium', 'Features bright red, heart-shaped waxy blooms that last for months. Adds a great pop of color.', 31.00, 22, 'anthurium.jpg', 1, 'Medium', TRUE, 'Bright Indirect', FALSE),
('Bird of Paradise', 'A magnificent tropical floor plant with massive, glossy leaves that brings instant jungle vibes to any bright room.', 75.00, 10, 'bird_of_paradise.jpg', 1, 'Ultra Large', TRUE, 'Direct Sunlight', FALSE),
('Alocasia Polly', 'Also known as the African Mask plant, featuring stunning dark green arrow-shaped leaves with bold, contrasting pale veins.', 28.50, 24, 'alocasia_polly.jpg', 1, 'Medium', TRUE, 'Bright Indirect', FALSE);
```

---

## 4. Run the Application

Once the database is populated, start the application using `uv`:

```bash
uv run app.py
```

The server will start, and the application will be accessible via your `localhost` address in your browser. Enjoy!
