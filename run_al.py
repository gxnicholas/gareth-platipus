import os

from models.non_meta import KNN, SVM
import models.meta.main as platipus
from pathlib import Path
from utils.plot import plot_metrics_graph
from utils import read_pickle, write_pickle, define_non_meta_model_name
from model_params import common_params, knn_params, svm_params, meta_train, meta_test


if __name__ == '__main__':
    # Set up the results directory
    results_folder = './results'

    # TODO: maybe move this to a function in utils?
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
        print('No folder for results storage found')
        print('Make folder to store results at')
    else:
        print('Found existing folder. All results will be stored at')
    print(results_folder)

    # Append the data to cv_stats or overwrite the current results
    overwrite = common_params['cv_stats_overwrite']
    cv_stats_dst = common_params['stats_path']
    if os.path.exists(cv_stats_dst) and overwrite:
        print('Overwriting the current cv_stats.pkl')
        os.remove(cv_stats_dst)

    # Record used models for plotting later
    models_to_plot = []

    # Training different models
    # PLATIPUS
    # platipus_train_params = {**common_params, **meta_params, **meta_train}
    # params = platipus.initialize(["PLATIPUS"], platipus_train_params)
    # platipus.main(params)

    # platipus_test_params = {**common_params, **meta_params, **meta_test}
    # params = platipus.initialize(["PLATIPUS"], platipus_test_params)
    # platipus.main(params)

    # TODO: MAML

    # KNN w/ active learning
    # Trained under option 1
    KNN1_params = {**common_params, **knn_params}
    KNN1_params['model_name'] = define_non_meta_model_name(KNN1_params['model_name'], KNN1_params['pretrain'])
    models_to_plot.append(KNN1_params['model_name'])
    KNN.run_model(KNN1_params)

    # Trained under option 2
    KNN2_params = {**common_params, **knn_params}
    KNN2_params['pretrain'] = False
    KNN2_params['model_name'] = define_non_meta_model_name(KNN2_params['model_name'], KNN2_params['pretrain'])
    models_to_plot.append(KNN2_params['model_name'])
    KNN.run_model(KNN2_params)

    # SVM w/ active learning
    # Trained under option 1
    SVM1_params = {**common_params, **svm_params}
    SVM1_params['model_name'] = define_non_meta_model_name(SVM1_params['model_name'], SVM1_params['pretrain'])
    models_to_plot.append(SVM1_params['model_name'])
    SVM.run_model(SVM1_params)

    # Trained under option 2
    SVM2_params = {**common_params, **svm_params}
    SVM2_params['pretrain'] = False
    SVM2_params['model_name'] = define_non_meta_model_name(SVM2_params['model_name'], SVM2_params['pretrain'])
    models_to_plot.append(SVM2_params['model_name'])
    SVM.run_model(SVM2_params)

    # TODO: RandomForest
    # Random Forest w/ active learning
    # Trained under option 1

    # Trained under option 2

    cv_stats = read_pickle(common_params['stats_path'])
    amines = cv_stats[models_to_plot[0]]['amine']
    # print(cv_stats.keys())
    # print(amines)

    for i, amine in enumerate(amines):
        plot_metrics_graph(96, cv_stats, './results', amine=amine, amine_index=i, models=models_to_plot)
