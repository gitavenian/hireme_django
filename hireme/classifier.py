import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the dataset
df = pd.read_excel("employee_data.xlsx")

# Encode categorical variables
label_encoder = LabelEncoder()
df['emp_skill'] = label_encoder.fit_transform(df['emp_skill'])
df['required_skill'] = label_encoder.fit_transform(df['required_skill'])

# Save the label encoder
with open("label_encoder.pkl", "wb") as file:
    pickle.dump(label_encoder, file)

# Define the feature columns and target column
features = ['emp_skill', 'emp_exp', 'required_skill', 'required_exp']
target = 'convenient'

# Split the data into training and testing sets
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Random Forest model
model = RandomForestClassifier(n_estimators=200, random_state=48)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the model as a .pkl file
with open("Convenient_job_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model and label encoder saved")