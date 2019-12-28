from app import DB


class Tag(DB.Model):
    __tablename__ = "tag"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)

    def __init__(self, name):
        """ Constructor for Tag model."""
        self.name = name

    def __repr__(self):
        """ String representation of Tag model object."""
        return f"{self.name}"
