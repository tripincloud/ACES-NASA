import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import callbacks
from dataread import DataReader
from net import MyRNN
import matplotlib.pyplot as plt

dataread = DataReader()
data_array, fin_risk = dataread.get_shuffle_data()

batchsz = 1024  
val_size = 1800  
train_db = tf.data.Dataset.from_tensor_slices((data_array[val_size:, :, :], fin_risk[val_size:]))   
val_db = tf.data.Dataset.from_tensor_slices((data_array[:val_size, :, :], fin_risk[:val_size]))     
train_db = train_db.batch(batchsz)
val_db = val_db.batch(batchsz)
print(train_db)  # ((None, 23, 102), (None,)), types: (tf.float64, tf.float64)>
print(val_db)


def main():
    units = 128    
    epochs = 150   
    model = MyRNN(units)

    log_dir = "logs/"
    
    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor='val_loss',  
        factor=0.8,          
        min_delta=0.1,
        patience=10,        
        verbose=1
    )
   
    checkpoint_period = callbacks.ModelCheckpoint(
        log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
        monitor='val_loss',
        save_weights_only=True,
        save_best_only=True,
        period=30
    )
    
    early_stopping = callbacks.EarlyStopping(
        monitor='val_loss',
        min_delta=0.05,
        patience=20,
        verbose=1
    )

    
    model.compile(optimizer=keras.optimizers.Adam(0.01),
                  loss='mse',
                  metrics=['mse'])

  

    
    history = model.fit(train_db, epochs=epochs, validation_data=val_db,
              callbacks=[reduce_lr, checkpoint_period])
    model.save_weights(log_dir + 'last1.h5')    
    model.summary()

    
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

if __name__ == '__main__':
    main()
