

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, plaintext_password):
        self.password = hashlib.md5(plaintext_password.encode()).hexdigest()

    def __repr__(self):
        return f'<User {self.email}>'