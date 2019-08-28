import sys
sys.path.append('../DeepCTR/')
import pandas as pd
import tensorflow as tf
from sklearn.metrics import log_loss, roc_auc_score
from deepctr.models import DeepFM
from deepctr.inputs import SparseFeat, DenseFeat,get_fixlen_feature_names
from tensorflow.python.keras.callbacks import EarlyStopping

def roc_auc_score_pyfunc(y_true, y_pred):
    return tf.py_func(roc_auc_score, (y_true, y_pred), tf.double)

def log_loss_pyfunc(y_true, y_pred):
    return tf.py_func(log_loss, (y_true, y_pred), tf.double)

sparse_features = ['uid', 'author_id', 'u_region_id', 'g_region_id', 'item_id', 'music_id']
dense_features = ['generate_time', 'date', 'duration']
# using_features = ['uid', 'author_id', 'u_region_id', 'g_region_id', 'item_id', 'music_id', 'generate_time', 'date', 'duration']
targets = ['finish', 'like']

def model_generate(method, train_X, train_y, val_X, val_y, linear_feature_columns, dnn_feature_columns):
    model = DeepFM(linear_feature_columns, dnn_feature_columns, embedding_size=32)
    model.compile("adam", "binary_crossentropy", metrics=[roc_auc_score_pyfunc, log_loss_pyfunc])
    history = model.fit(train_X, train_y, validation_data=(val_X, val_y), batch_size=4096, epochs=5,
                        callbacks=[EarlyStopping()])
    return model, history

def main(method):

    Use_SF = False
    if len(sys.argv) > 0 and sys.argv[0] == 'SF':
        Use_SF = True

    train, vali, test = GetFeatures(Use_SF)

    feature_count = []
    for feat in sparse_features:
        print("Fitting {}".format(feat))
        labels = {}
        for x in train[feat]:
            if x not in labels:
                labels[x] = len(labels) + 1
        print("Transforming {}".format(feat))
        for df in [train, vali, test]:
            df[feat] = df[feat].map(lambda x: labels.get(x, 0))
        feature_count.append(len(labels) + 1)

    sparse_feature_columns = [SparseFeat(f, f_c) for f, f_c in zip(sparse_features, feature_count)]
    dense_feature_columns = [DenseFeat(f, 1) for f in dense_features]
    fixlen_feature_columns = sparse_feature_columns + dense_feature_columns
    dnn_feature_columns = fixlen_feature_columns
    linear_feature_columns = fixlen_feature_columns

    fixlen_feature_names = get_fixlen_feature_names(linear_feature_columns + dnn_feature_columns)

    train_model_input = [train[name] for name in fixlen_feature_names]
    vali_model_input = [vali[name] for name in fixlen_feature_names]
    test_model_input = [test[name] for name in fixlen_feature_names]

    def eval(target_list):
        model, history = model_generate(method, train_model_input, train[target_list], vali_model_input, vali[target_list],
                                        linear_feature_columns, dnn_feature_columns)
        pred_ans = model.predict(test_model_input, batch_size=256)
        for id in range(len(target_list)):
            target = target_list[id]
            print(target + " test LogLoss", round(log_loss(test[target].values, pred_ans[id]), 4))
            print(target + " test AUC", round(roc_auc_score(test[target].values, pred_ans[id]), 4))

    eval(targets)

if __name__ == "__main__":
    main(***)
