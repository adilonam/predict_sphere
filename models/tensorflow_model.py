import json
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from .abstract_model import AbstractModel
from sklearn.metrics import mean_squared_error  
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
import numpy as np



class TensorFlowModel(AbstractModel):
    epochs = 20
    prob = 0.54

    def __init__(self) -> None:
        self.encoder = OneHotEncoder()
        super().__init__()



    
 

    def reshape_input(self , X):
        return X.reshape((X.shape[0], X.shape[1], 1))



    
    def fit(self ,  X, y):
        
        # No need for one-hot encoding in binary classification:
        # Remove the encoder fitting line

        self.scaler = MinMaxScaler()
        X = self.scaler.fit_transform(X)
        
        
        X = self.reshape_input(X)
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # No need to reshape X_train since we are assuming
        # it has already been reshaped for LSTM layers appropriately

        # Build the model
        self.model = Sequential([
                    LSTM(64, input_shape=(X.shape[1], X.shape[2]), return_sequences=True),
                    BatchNormalization(),
                    Dropout(0.5),
                    LSTM(32, return_sequences=False),
                    BatchNormalization(),
                    Dropout(0.5),
                    Dense(64, activation='relu'),
                    BatchNormalization(),
                    Dropout(0.5),
                    Dense(32, activation='relu'),
                    BatchNormalization(),
                    Dropout(0.5),
                    Dense(1, activation='sigmoid')
                ])
                        
        # Compile the model
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  

        # Train the model
        self.model.fit(
            X, 
            y, 
            epochs=self.epochs,  # Replace self.epochs with the actual number of epochs you want
            batch_size=32,       # The batch size
            verbose=1
        )

        predictions = self.model.predict(X_test)

        print(predictions.mean())
        self.set_metrics((predictions > self.prob).astype("int32") , y_test)
        return True




    def predict(self, long_df):
        X = long_df[self.features].values
        X = self.scaler.transform(X)
        X = self.reshape_input(X)
        
        predictions = self.model.predict(X)
        return predictions
    


    




