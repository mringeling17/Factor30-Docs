import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM, LayerNormalization, Dropout

class TemporalFusionTransformer(tf.keras.Model):
    def __init__(self, hidden_layer_size, dropout_rate, learning_rate, num_heads, num_encoder_steps, num_decoder_steps, output_size, batch_first):
        super(TemporalFusionTransformer, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.num_heads = num_heads
        self.num_encoder_steps = num_encoder_steps
        self.num_decoder_steps = num_decoder_steps
        self.output_size = output_size
        self.batch_first = batch_first

        self.lstm = LSTM(hidden_layer_size, return_sequences=True)
        self.layer_norm = LayerNormalization()
        self.dropout = Dropout(dropout_rate)
        self.dense = Dense(output_size)

    def call(self, inputs):
        x = self.lstm(inputs)
        x = self.layer_norm(x)
        x = self.dropout(x)
        return self.dense(x)

# Puedes agregar más capas y funcionalidades según el diseño original de TFT