from pathlib import Path

import streamlit as st
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from xgboost import XGBClassifier, XGBRegressor
from aimodel import DataProcessor, Evaluation, NeuralNetworkModel, RandomForestModel, XGBoostModel

st.title("AI Model")


def choose_dataset():
    """
    choose dataset for the AI Model
    """
    uploaded_file = st.file_uploader("Choose Dataset", type=(["csv", "xlsx", "xls"]))
    root_path = "Dataset/ClassificationDataset"
    if uploaded_file is not None:
        return Path(root_path) / Path(uploaded_file.name)
    return None


# Getting the user input for X and Y columns
def select_data(file_path):
    data_processor = DataProcessor(file_path)
    # select X_columns and y_columns
    columns = data_processor.get_columns()
    X_columns = st.multiselect("Choose your X_Columns", columns)
    y_columns = st.multiselect("Choose your y_Columns", columns)
    data_processor.select_X_y(X_columns, y_columns)
    return data_processor


# Split the dataset for training and testing
def split_data(data_processor):
    # select test size
    test_size_input = st.slider("Select test size", 0.1, 1.0, 0.25)
    data_processor.splitData(test_size=test_size_input)
    return data_processor
    # if st.button(label='Split Data'):
    #     data_processor.splitData(test_size=test_size_input)
    #     return data_processor
    # return None


# Check the data processed or Raw
def check_data():
    data_processed = st.radio(
        "Is the data already processed or it is a Raw data",
        ["***Raw***", "***Processed***"],
    )
    return data_processed


# Scale data for smoothning
def scale_data(data_processor):
    return data_processor.scaleData()


# select model to perform the training
def select_model():
    model_option = st.selectbox(
        "Select your AI model 🤖", ("Neural Network", "Random Forest", "XGBoost")
    )
    return model_option


# Setting the Configuration by getting user input
def get_training_config(model_option):
    # Used to set Neural Network type
    class_mapping_nn = {
        "Classification": MLPClassifier, 
        "Regression": MLPRegressor
    }

    # Used to set Random Forest type
    class_mapping_rf = {
        "Classification": RandomForestClassifier,
        "Regression": RandomForestRegressor,
    }

    # Used to set XGBoost type
    class_mapping_xgb = {
        "Classification": XGBClassifier,
        "Regression": XGBRegressor,
    }

    # training configuration for Neural Network
    if model_option == "Neural Network":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_classifier_or_regressor = st.selectbox(
                "Nature of Data: ", ("Classification", "Regression")
            )
        with col2:
            act_fn = st.selectbox("Activation Function: ", ("relu", "tanh", "logistic"))
        with col3:
            no_of_layers = st.number_input(
                "Number of hidden layers", min_value=10, max_value=100, step=5
            )
        with col4:
            no_of_neurons = st.number_input(
                "Number of neurons", min_value=100, max_value=500, step=10
            )

        return NeuralNetworkModel(
            classifier_or_regressor=class_mapping_nn[selected_classifier_or_regressor],
            activation_fn=act_fn,
            no_of_layers=no_of_layers,
            no_of_neurons=no_of_neurons
        )

    # training configuration for Random Forest
    elif model_option == "Random Forest":
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_classifier_or_regressor = st.selectbox(
                "Nature of Data: ", ("Classification", "Regression")
            )
        with col2:
            n_est = st.number_input(
                "Number of Estimators", min_value=100, max_value=1000, step=50
            )

        with col3:
            if selected_classifier_or_regressor == "Classification":
                criterion = st.selectbox("Criterion: ", ("gini", "entropy", "log_loss"), 
                                         help='The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “log_loss” and “entropy” both for the Shannon information gain.'
                                         )
            else:
                criterion = st.selectbox(
                    "Criterion: ", ("friedman_mse", "squared_error", "poisson"),
                    help='The function to measure the quality of a split. Supported criteria are “squared_error” for the mean squared error, which is equal to variance reduction as feature selection criterion and minimizes the L2 loss using the mean of each terminal node, “friedman_mse”, which uses mean squared error with Friedman’s improvement score for potential splits, and “poisson” which uses reduction in Poisson deviance to find splits. Training using “absolute_error” is significantly slower than when using “squared_error”.'
                )
        return RandomForestModel(
            classifier_or_regressor=class_mapping_rf[selected_classifier_or_regressor],
            n_estimators=n_est,
            criterion=criterion
        )
    
    # training configuration for XGBoost
    elif model_option == "XGBoost":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_classifier_or_regressor = st.selectbox(
                "Nature of Data: ", ("Classification", "Regression")
            )
        with col2:
            n_est = st.number_input(
                "Number of Estimators", min_value=100, max_value=1000, step=50
            )
        with col3:
            learning_rate = st.number_input(
                "Learning Rate", min_value=0.1, max_value=0.3, step=0.1
            )
        with col4:
            if selected_classifier_or_regressor == "Classification":
                objective = st.selectbox("Objective: ", ("binary:logistic", "binary:logitraw", "binary:hinge"),
                                         help='Specify the learning task and the corresponding learning objective. binary:logistic: logistic regression for binary classification, output probability. binary:logitraw: logistic regression for binary classification, output score before logistic transformation binary:hinge: hinge loss for binary classification. This makes predictions of 0 or 1, rather than producing probabilities.'
                                         )
            else:
                objective = st.selectbox(
                    "Objective: ", ("reg:squarederror", "reg:squaredlogerror", "reg:logistic"),
                    help='Specify the learning task and the corresponding learning objective. reg:squarederror: regression with squared loss. reg:squaredlogerror: regression with squared log loss. reg:logistic: logistic regression, output probability'
                )
        return XGBoostModel(
            classifier_or_regressor=class_mapping_xgb[selected_classifier_or_regressor],
            n_estimators=n_est,
            objective=objective,
            learning_rate=learning_rate
        )


# train model
def train_model(model, data_processor_split):
    training_success = False
    if st.button("Train Model 🚀", use_container_width=True, type="primary"):
        model.train(data_processor_split.X_train, data_processor_split.y_train)
        training_success = True
        st.success("Done!", icon="✅")
    return model, training_success


# Get prediction
def get_prediction(model, data_processor_split):
    return model.predict(data_processor_split.X_test)


# Evaluate the model
def get_evaluation(model, data_processor_split):
    # evaluation = Evaluation(data_processor.y_test, model.prediction)
    evaluation = Evaluation(y_test=data_processor_split.y_test, y_pred=model.prediction)
    st.header("Evaluation")
    col1, col2, col3 = st.columns(3)
    col1.metric(value=round(evaluation.get_accuracy(), 2), label="Accuracy")
    col2.metric(value=round(evaluation.get_rmse(), 2), label="RMSE")
    col3.metric(value=round(evaluation.get_precision(), 3), label="Precision")
    cm = evaluation.get_confusionmatrix()
    st.header("Confusion Matrix")
    evaluation.plot_confusion_matrix(cm)


def main():
    try:
        file_path = choose_dataset()
    except ValueError:
        st.error("No file is selected!")
    if file_path:
        data_processor = select_data(file_path)
        data_processor_split = split_data(data_processor)
        data_process_status = check_data()
        if data_process_status == "Raw":
            data_processor_split = scale_data(data_processor_split)
        model_selected = select_model()
        model = get_training_config(model_selected)
        # model_trained = train_model(model_with_config, data_processor_split)
        # model, status = model.train(data_processor_split.X_train, data_processor_split.y_train)
        model, status = train_model(model, data_processor_split)
        # model.predict(data_processor_split.X_test)
        if status:
            get_prediction(model, data_processor_split)
            get_evaluation(model, data_processor_split)


if __name__ == "__main__":
    main()
