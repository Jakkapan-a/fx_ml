from app import db

class ForexData(db.Model):
    ### ForexData model history
    __tablename__ = 'forex_data'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False) # Symbol : EURUSD, AUXUSD, etc
    datetime = db.Column(db.DateTime, nullable=False) # Date and time
    timeframe = db.Column(db.String(10), nullable=False) # Timeframe : M1, M5, H1, etc
    open_price = db.Column(db.Float, nullable=False) # Open price
    close_price = db.Column(db.Float, nullable=False) # Close price
    high_price = db.Column(db.Float, nullable=False) # High price
    low_price = db.Column(db.Float, nullable=False) # Low price
    volume = db.Column(db.Integer, nullable=False) # Volume
    created_at = db.Column(db.DateTime, server_default=db.func.now()) # Created at
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()) # Updated

    def __repr__(self):
        return f'<ForexData {self.symbol} {self.datetime} {self.timeframe}>'

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'datetime': self.datetime,
            'timeframe': self.timeframe,
            'open_price': self.open_price,
            'close_price': self.close_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'volume': self.volume,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }