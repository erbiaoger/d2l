import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, BatchNormalization, Dropout 
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
# 数据加载与预处理
# radar_data = np.load('radar_data.npy')

# # 数据标准化
# mean = np.mean(radar_data, axis=(0, 1, 2, 3)) 
# std = np.std(radar_data, axis=(0, 1, 2, 3)) 
# radar_data_normalized = (radar_data - mean) / std
# # 数据拆分
# X = radar_data_normalized[:, :-1]
# y = radar_data_normalized[:, 1:, :, :, 0:1]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 建模
model = Sequential([
            BatchNormalization(input_shape=(None, X_train.shape[2], X_train.shape[3], 3)),
            ConvLSTM2D(filters=64, kernel_size=(3, 3), padding='same', return_sequences=True), BatchNormalization(),
            Dropout(0.3),
            ConvLSTM2D(filters=128, kernel_size=(3, 3), padding='same', return_sequences=True), BatchNormalization(),
            Dropout(0.3),
            Conv2D(filters=1, kernel_size=(3, 3), padding='same', activation='linear') ])
# 编译
optimizer = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07) 
model.compile(optimizer=optimizer, loss='mse')
# 定义回调函数
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True) 
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True) 
callbacks = [early_stopping, model_checkpoint]
# 训练
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), callbacks=callbacks)
# 评估
test_loss = model.evaluate(X_test, y_test) 
print(f"Test Loss: {test_loss}")