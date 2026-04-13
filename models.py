import pymysql

from sql import execute_query, get_db_connection

class BaseModel:
    """Base model class with common functionality"""

    def __repr__(self):
        """Developer-friendly string representation"""
        class_name = self.__class__.__name__
        attrs = []

        # Get all instance attributes (excluding private ones)
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, str):
                    attrs.append(f"{key}='{value}'")
                else:
                    attrs.append(f"{key}={value}")

        return f"{class_name}({', '.join(attrs)})"

    def to_dict(self, exclude_none: bool = True):
        """Convert model to dictionary"""
        from datetime import timedelta

        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if exclude_none and value is None:
                    continue
                # Convert timedelta objects to time strings for JSON serialization
                if isinstance(value, timedelta):
                    total_seconds = int(value.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    data[key] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    data[key] = value
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Create model instance from dictionary"""
        # Filter out None values and private attributes
        filtered_data = {
            k: v for k, v in data.items() if v is not None and not k.startswith("_")
        }
        return cls(**filtered_data)



class UserBase(BaseModel):
    """UserBase model class"""

    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str,
        password_salt: str,
        created_at: str | None = None,
        last_login: str | None = None,
        user_id: int | None = None,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.created_at = created_at
        self.last_login = last_login

    def __str__(self):
        return f"Base User: {self.username} . ID: {self.user_id}"

    def save(self):
        """Create or update user in database"""
        if self.user_id is None:
            # INSERT
            query = """
            INSERT INTO user_base (username, email, first_name, last_name, password_hash, password_salt, created_at, last_login)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.username,
                self.email,
                self.first_name,
                self.last_name,
                self.password_hash,
                self.password_salt,
                self.created_at,
                self.last_login,
            )
            self.user_id = execute_query(query, params, fetch="none")
        else:
            # UPDATE
            self.update()
        return self

    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        query = "SELECT * FROM user_base WHERE user_id = %s"
        result = execute_query(query, (user_id,), fetch="one")
        return cls.from_dict(result) if result else None

    @classmethod
    def get_by_username(cls, username):
        """Get user by username"""
        query = "SELECT * FROM user_base WHERE username = %s"
        result = execute_query(query, (username,), fetch="one")
        return cls.from_dict(result) if result else None

    @classmethod
    def get_all(cls):
        """Get all users"""
        query = "SELECT * FROM user_base ORDER BY username"
        results = execute_query(query, fetch="all")
        return [cls.from_dict(row) for row in results] if results else []

    def update(self):
        """Update user in database"""
        query = """
        UPDATE user_base 
        SET username=%s, email=%s, first_name=%s, last_name=%s, password_hash=%s, password_salt=%s, created_at=%s, last_login=%s
        WHERE user_id=%s
        """
        params = (
            self.username,
            self.email,
            self.first_name,
            self.last_name,
            self.password_hash,
            self.password_salt,
            self.created_at,
            self.last_login,
            self.user_id,
        )
        execute_query(query, params, fetch="none")
        return self

    def update_last_login(self, when: str):
        """Update last_login field"""
        if not self.user_id:
            return self
        query = """
        UPDATE user_base
        SET last_login=%s
        WHERE user_id=%s
        """
        execute_query(query, (when, self.user_id), fetch="none")
        self.last_login = when
        return self

    def delete(self):
        """Delete user from database"""
        if self.user_id:
            query = "DELETE FROM user_base WHERE user_id = %s"
            execute_query(query, (self.user_id,), fetch="none")
            self.user_id = None
        return True


class Cart(BaseModel):
    def __init__ (self, cartID=None, user_id=None, isGift=False):
        self.cartID = cartID
        self.user_id = user_id
        self.isGift = isGift
    
    @classmethod
    def get_or_create_cart(cls, user_id):
        query = "SELECT cartID FROM Cart WHERE user_id = %s"
        cart_data = execute_query(query, (user_id,), fetch="one")
        
        if cart_data:
            return cart_data['cartID']
        else:
            insert_query = "INSERT INTO Cart (user_id) VALUES (%s)"
            return execute_query(insert_query, (user_id,), fetch="none")
        
    @classmethod
    def get_items_with_details (cls, cart_id):
        query = """
            SELECT ci.cartItemID, ci.quantity, p.plantID, p.plantName, p.price, p.imageUrl 
            FROM Cart_Items ci
            JOIN Plants p ON ci.plantID = p.plantID
            WHERE ci.cartID = %s
        """
        return execute_query(query, (cart_id,), fetch="all")
        