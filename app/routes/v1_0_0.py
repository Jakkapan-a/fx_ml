import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request, current_app, Response

from app import db
from app.models.forex_data import ForexData
import xgboost as xgb
import sklearn

v1_0_0_bp = Blueprint('/', __name__)

@v1_0_0_bp.route('')
def index():
    return jsonify({'message': 'Welcome to the API!'})

@v1_0_0_bp.route('/predict/<string:symbol>/<string:timeframe>')
def predict(symbol, timeframe):
    """
    Predict next price based on historical data.
    """
    try:
        # URL = /api/v1.0.0/predict/EURUSD/M1?limit=1000
        limit = int(request.args.get('limit', 1000))  # default limit = 1000
        data = ForexData.query.filter_by(symbol=symbol, timeframe=timeframe).order_by(ForexData.datetime.desc()).limit(limit).all()

        if not data:
            return jsonify({'message': 'Data not found!'}), 404

        # Create DataFrame
        df = pd.DataFrame([{'datetime': d.datetime, 'close_price': d.close_price} for d in data])

        # Reverse DataFrame to chronological order
        df = df.iloc[::-1].reset_index(drop=True)

        # Calculate price difference
        df['price_diff'] = df['close_price'].diff().fillna(0)
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['close_price'].values

        # Extract data for training and testing
        train_size = int(len(X) * 0.8)
        X_train, y_train = X[:train_size], y[:train_size]
        X_test, y_test = X[train_size:], y[train_size:]

        # Train XGBoost model
        model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model.fit(X_train, y_train)

        # Predict next price
        future_price = model.predict(np.array([[len(X)]]))[0]

        # Calculate trend and percent change
        last_close_price = y[-1]
        trend = "up" if future_price > last_close_price else "down"
        percent_change = ((future_price - last_close_price) / last_close_price) * 100

        print(f"Symbol: {symbol}, Timeframe: {timeframe}, Future Price: {future_price}, Last Close Price: {last_close_price}, Trend: {trend}, Percent Change: {percent_change}")

        # Return prediction results
        return jsonify({
            "symbol": symbol,
            "timeframe": timeframe,
            "predicted_price": round(float(future_price), 2),
            "last_close_price": round(float(last_close_price), 2),
            "trend": trend,
            "percent_change": round(float(percent_change), 2),
            "date": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'message': str(e)}), 400


@v1_0_0_bp.route('/data/<string:symbol>/<string:timeframe>')
def get_data(symbol, timeframe):
    """
    :param symbol:
    :param timeframe:
    :return:
    """
    try:
        data = ForexData.query.filter_by(symbol=symbol, timeframe=timeframe).order_by(ForexData.datetime.desc()).limit(1000).all()

        if not data:
            return jsonify({'message': 'Data not found!'}), 404

        return jsonify([d.to_dict() for d in data])

    except Exception as e:
        return jsonify({'message': str(e)}), 400

@v1_0_0_bp.route('/add-data')
def add_data():
    """
    :return:
    """
    try:
        symbol = request.args.get('symbol')
        datetime_str = request.args.get('datetime')
        timeframe = request.args.get('timeframe')
        open_price = request.args.get('open_price')
        close_price = request.args.get('close_price')
        high_price = request.args.get('high_price')
        low_price = request.args.get('low_price')
        volume = request.args.get('volume')

        # check required parameters
        if not all([symbol, datetime_str, timeframe, open_price, close_price, high_price, low_price, volume]):
            print('Missing required parameters')
            return jsonify({'message': 'Missing required parameters'}), 400

        if timeframe not in ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']:
            return jsonify({'message': 'Invalid timeframe'}), 400

        # convert datetime to format (YYYY.MM.DD HH:MM to YYYY-MM-DD HH:MM:SS)
        datetime_str = datetime_str.replace('.', '-')
        if len(datetime_str.split(' ')[1]) == 4:
            datetime_str = datetime_str[:11] + '0' + datetime_str[11:]

        print("datetime_str :", datetime_str)

        # convert datetime
        from datetime import datetime
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

        # convert float/int
        open_price = float(open_price)
        close_price = float(close_price)
        high_price = float(high_price)
        low_price = float(low_price)
        volume = int(volume)

        data = ForexData(
            symbol=symbol,
            datetime=datetime_obj,
            timeframe=timeframe,
            open_price=open_price,
            close_price=close_price,
            high_price=high_price,
            low_price=low_price,
            volume=volume
        )

        db.session.add(data)
        db.session.commit()

        return jsonify({'message': 'Data added successfully!'}), 201
    except Exception as e:

        return jsonify({'message': str(e)}), 400