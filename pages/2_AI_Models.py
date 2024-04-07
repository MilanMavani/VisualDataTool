import os

import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from xgboost import XGBClassifier, XGBRegressor

from src.aimodel import (
    DataProcessor,
    Evaluation,
    NeuralNetworkModel,
    RandomForestModel,
    XGBoostModel,
)

st.set_option("deprecation.showPyplotGlobalUse", False)

st.title("AI based Classification and Regression Models")


# Dictionary mapping string labels to corresponding AI Models : Neural Network, Random Forest and XGBoost.
# Key:
#    - Classification: For classification tasks
#    - Regression: For regression tasks

class_mapping_nn = {"Classification": MLPClassifier, "Regression": MLPRegressor}

class_mapping_rf = {
    "Classification": RandomForestClassifier,
    "Regression": RandomForestRegressor,
}

class_mapping_xgb = {
    "Classification": XGBClassifier,
    "Regression": XGBRegressor,
}


def choose_dataset():
    """
    choose a dataset to perform features of the AI based Models
    """
    uploaded_file = st.file_uploader("Choose Dataset", type=(["csv", "xlsx", "xls"]))
    if uploaded_file is not None:
        _, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension == ".csv":
            uploaded_file_df = pd.read_csv(uploaded_file)
        elif file_extension in (".xlsx", ".xls"):
            uploaded_file_df = pd.read_excel(uploaded_file)
        return DataProcessor(uploaded_file_df)
    return None


def select_problem_type():
    """
    choose the problem type to perform features of the AI based Models
    """
    select_problem_type = st.selectbox(
        "Nature of Data: ", ("Classification", "Regression")
    )
    if select_problem_type == "Classification":
        st.info(
            "Classification categorizes data into predefined classes based on their features, enabling prediction of unseen data's class.",
            icon="ℹ️",
        )
    elif select_problem_type == "Regression":
        st.info(
            "Regression in ML predicts numerical outcomes by establishing relationships between variables through mathematical equations.",
            icon="ℹ️",
        )
    return select_problem_type


def select_data(data_processor, problem_type):
    """
    Selects the input features (X) and target variable (y) columns based on user input.

    Parameters:
    - data_processor (DataProcessor): An instance of the DataProcessor class that provides methods to process the data.
    - problem_type (str): Specifies the type of problem, e.g., "Classification" or "Regression".

    Returns:
    - data_processor (DataProcessor): An updated instance of the DataProcessor class.
    """
    columns = data_processor.get_columns()
    X_columns = st.multiselect("Choose your Input Columns", columns)
    y_columns = st.multiselect("Choose your Output Columns", columns)
    data_processor.select_X_y(X_columns, y_columns)

    return data_processor, X_columns, y_columns


def split_data(data_processor, problem_type):
    """
    Split the dataset into training and testing part based on user input.

    Parameters:
    - data_processor (DataProcessor): An instance of the DataProcessor class that provides methods to process the data.
    - problem_type (str): Specifies the type of problem, e.g., "Classification" or "Regression".

    Returns:
    - data_processor (DataProcessor): An updated instance of the DataProcessor class.
    """
    test_size_input = st.slider(
        "Select test size for training the model", 0.1, 1.0, 0.25
    )
    try:
        data_processor.splitData(
            test_size=test_size_input, classifier_or_regressor=problem_type
        )
        return data_processor
    except ValueError:
        st.error("Input and output not selected")
        return


def check_data():
    """
    Checks whether the data is already processed or raw.

    Returns:
    - data_processed (str): Indicates whether the data is raw or processed.
    """
    data_processed = st.radio(
        "Select state of data", ["Raw", "Processed"], horizontal=True
    )
    return data_processed


def scale_data(data_processor: DataProcessor):
    """
    Scales the data if it is raw for smoothning purpose.

    Returns:
    - data_processor (DataProcessor): An updated instance of the DataProcessor class.
    """
    return data_processor.scaleData()


def select_model():
    """
    It allows the user to select an AI model from a predefined list.
    - Users can choose from options including "Neural Network", "Random Forest", and "XGBoost".

    Returns:
    - model_option (str): The selected AI model.
    """
    model_option = st.selectbox(
        "Select your AI model 🤖", ("Neural Network", "Random Forest", "XGBoost")
    )
    return model_option


def get_training_config(model_option, selected_classifier_or_regressor):
    """
    It allows the user to set the configuration of an AI model from a predefined parameters and values.
    - Users can choose from options including Activation Function, Number of Hidden layers, Number of Neurons for Neural Network.
    - Users can choose from options including Criterion, Number of Estimators for Random Forest.
    - Users can choose from options including Objective, Number of Estimators, Learning rate for XGBoosting.

    Returns:
    - The configured AI model.
    """

    if model_option == "Neural Network":
        """
        Training configuration for Neural Network
        """
        col1, col2, col3 = st.columns(3)
        with col1:
            act_fn = st.selectbox(
                "Activation Function: ",
                ("relu", "identity", "tanh", "logistic"),
                help="""
                                  Activation function for the hidden layer:
                                  - identity: no-op activation, useful to implement linear bottleneck, returns f(x) = x
                                  - logistic: the logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x)).
                                  - tanh: the hyperbolic tan function, returns f(x) = tanh(x).
                                  - relu: the rectified linear unit function, returns f(x) = max(0, x)
                                  """,
            )
        with col2:
            no_of_layers = st.number_input(
                "Number of hidden layers", min_value=10, max_value=100, step=5
            )
        with col3:
            no_of_neurons = st.number_input(
                "Number of neurons", min_value=100, max_value=500, step=10
            )

        return NeuralNetworkModel(
            classifier_or_regressor=class_mapping_nn[selected_classifier_or_regressor],
            activation_fn=act_fn,
            no_of_layers=no_of_layers,
            no_of_neurons=no_of_neurons,
        )

    elif model_option == "Random Forest":
        """
        Training configuration for Random Forest
        """
        col1, col2 = st.columns(2)
        with col1:
            n_est = st.number_input(
                "Number of Estimators", min_value=100, max_value=1000, step=50
            )

        with col2:
            if selected_classifier_or_regressor == "Classification":
                criterion = st.selectbox(
                    "Criterion: ",
                    ("gini", "entropy", "log_loss"),
                    help="""
                    The function to measure the quality of a split.
                    Supported criteria are:
                    - 'gini' for the Gini impurity
                    - 'log_loss' and 'entropy' both for the Shannon information gain.
                    """,
                )
            else:
                criterion = st.selectbox(
                    "Criterion: ",
                    ("friedman_mse", "squared_error", "poisson"),
                    help="""
                        The function to measure the quality of a split. Supported criteria are:
                        - “squared_error” for the mean squared error, which is equal to variance reduction as feature selection criterion and minimizes the L2 loss.
                        - “friedman_mse”, which uses mean squared error with Friedman’s improvement score for potential splits.
                        - “poisson” which uses reduction in Poisson deviance to find splits.
                        """,
                )
        return RandomForestModel(
            classifier_or_regressor=class_mapping_rf[selected_classifier_or_regressor],
            n_estimators=n_est,
            criterion=criterion,
        )

    elif model_option == "XGBoost":
        """
        Training configuration for XGBoost
        """
        col1, col2, col3 = st.columns(3)
        with col1:
            n_est = st.number_input(
                "Number of Estimators", min_value=100, max_value=1000, step=50
            )
        with col2:
            learning_rate = st.number_input(
                "Learning Rate", min_value=0.01, max_value=0.3, step=0.01
            )
        with col3:
            if selected_classifier_or_regressor == "Classification":
                objective = st.selectbox(
                    "Objective: ",
                    ("binary:logistic", "binary:logitraw", "binary:hinge"),
                    help="""
                    Specify the learning task and the corresponding learning objective. Supported options are:
                    - binary:logistic: logistic regression for binary classification, output probability.
                    - binary:logitraw: logistic regression for binary classification, output score before logistic transformation.
                    - binary:hinge: hinge loss for binary classification. This makes predictions of 0 or 1, rather than producing probabilities.
                    """,
                )
            else:
                objective = st.selectbox(
                    "Objective: ",
                    ("reg:squarederror", "reg:squaredlogerror", "reg:logistic"),
                    help="""
                        Specify the learning task and the corresponding learning objective. Supported options are:
                        - reg:squarederror: regression with squared loss.
                        - reg:squaredlogerror: regression with squared log loss.
                        - reg:logistic: logistic regression, output probability.
                        """,
                )
        return XGBoostModel(
            classifier_or_regressor=class_mapping_xgb[selected_classifier_or_regressor],
            n_estimators=n_est,
            objective=objective,
            learning_rate=learning_rate,
        )


def train_model(model, data_processor_split):
    """
    Trains the specified model using the provided training data.

    Parameters:
    - model: The machine learning model to be trained.
    - data_processor_split (DataProcessorSplit): An instance of the DataProcessorSplit class containing split training data.

    Returns:
    - model: The trained machine learning model.
    - training_success (bool): Indicates whether the training was successful.
    """
    training_success = False
    if st.button("Train Model 🚀", use_container_width=True, type="primary"):
        with st.spinner("Training..."):
            model.train(data_processor_split.X_train, data_processor_split.y_train)
            training_success = True
        st.success("Done!", icon="✅")
    return model, training_success


def get_prediction(model, data_processor_split):
    """
    Predict the result using the provided testing data.

    Parameters:
    - model: The machine learning model to be predicted.
    - data_processor_split (DataProcessorSplit): An instance of the DataProcessorSplit class containing split training data.

    Returns:
    - model: The predictions of the machine learning model.
    """
    return model.predict(data_processor_split.X_test)


def plot_confusion_matrix(conf_matrix):
    """
    Plot the confusion matrix of the model.
    Plot: Confusion matrix.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, cmap="Reds", fmt="g")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    return fig


def get_evaluation(model, data_processor_split, problem_type):
    """
    Evaluates the trained model using the provided evaluation data.

    Parameters:
    - model: The trained machine learning model to be evaluated.
    - data_processor_split (DataProcessorSplit): An instance of the DataProcessorSplit class containing split evaluation data.
    - problem_type (str): Specifies the type of problem, e.g., "Classification" or "Regression".

    Returns:
    - evaluation_results: The evaluation results obtained from the model.
    """
    evaluation = Evaluation(y_test=data_processor_split.y_test, y_pred=model.prediction)
    st.header("📊 Evaluation")
    st.subheader("Metrics", divider="red")
    col1, col2, col3 = st.columns(3)
    if problem_type == "Classification":
        col1.metric(
            value=round(evaluation.get_accuracy(), 2),
            label="Accuracy",
            help="The proportion of correctly classified instances. The best value is 1.0 (100%)",
        )
        col2.metric(
            value=round(evaluation.get_precision(), 3),
            label="Precision",
            help="The proportion of true positive predictions among all positive predictions. ",
        )
        col3.metric(
            value=round(evaluation.get_recall_score(), 3),
            label="Recall Score",
            help="The proportion of true positive predictions among all actual positives.",
        )
        cm_test = evaluation.get_confusionmatrix()
        st.subheader("Confusion Matrix for Test Data", divider="red")
        fig = plot_confusion_matrix(cm_test)
        st.pyplot(fig)
    else:
        col1.metric(
            value=round(evaluation.get_mae(), 2),
            label="Mean Absolute Error",
            help="The average absolute difference between predicted and actual values",
        )
        col2.metric(
            value=round(evaluation.get_r2(), 3),
            label="R-squared Score",
            help="The proportion of the variance in the dependent variable that is predictable from the independent variables",
        )
        col3.metric(
            value=round(evaluation.get_rmse(), 2),
            label="Root Mean Squared Error",
            help="The square root of the average of the squares of the differences between predicted and actual values",
        )
        fig = evaluation.scatter_plot_predicted_vs_actual()
        st.subheader("Scatter Plot of Predicted vs. Actual Values", divider="red")
        st.pyplot(fig)


def get_heatmap(df: pd.DataFrame):
    st.subheader("Correlation between variables")
    try:
        fig = sns.heatmap(df.corr(), ax=plt.subplots()[1])
        st.write(fig.get_figure())
    except ValueError:
        st.error(
            "Heatmap can not be plotted. Please check the data processing step!",
            icon="❌",
        )


def get_distribution(df):
    st.subheader("Data Distribution")
    df_num = df.select_dtypes(include=["float64", "int64"])
    df_num.hist(
        figsize=(16, 20),
        bins=30,
        xlabelsize=15,
        ylabelsize=15,
        edgecolor="black",
        color="red",
    )
    for ax in plt.gcf().get_axes():
        ax.set_title(ax.get_title(), fontsize=25)
    st.pyplot()


def main():
    try:
        data_processor = choose_dataset()
    except ValueError:
        st.error("No file is selected!")
        return
    if data_processor:
        get_heatmap(data_processor.data)
        get_distribution(data_processor.data)
        # data_process_status = check_data()
        problem_type = select_problem_type()
        data_processor, input_cols, output_cols = select_data(
            data_processor, problem_type
        )
        if problem_type == "Classification":
            try:
                data_processor.resample_data()
            except ValueError:
                pass
        if data_processor.X.empty:
            st.error("Input and output not selected")
            return
        data_processor_split = split_data(data_processor, problem_type)
        if data_processor_split:
            data_processor_split.scaleData()
            model_selected = select_model()
            model = get_training_config(model_selected, problem_type)
            model, status = train_model(model, data_processor_split)
            if status:
                get_prediction(model, data_processor_split)
                get_evaluation(model, data_processor_split, problem_type)


if __name__ == "__main__":
    main()
