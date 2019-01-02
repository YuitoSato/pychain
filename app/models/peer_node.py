from app.database.sqlite import db


class PeerNode(db.Model):
    __tablename__ = "peer_nodes"
    peer_node_id = db.Column(db.Text, primary_key = True, autoincrement = False)
    url = db.Column(db.String(length = 64), nullable = False)
    address = db.Column(db.String(length = 64), nullable = False)

    @classmethod
    def list(cls):
        return cls.query.all()

