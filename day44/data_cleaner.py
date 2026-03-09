import pandas as pd

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully!")
        return df
    except Exception as e:
        print("Error loading data:", e)
        return None
    
def clean_data(df):
    """Clean the data."""
    print("\n--- Cleaning Data ---")
    print("Initial Shape:", df.shape)

    # Handle Missing Values
    print("\nHandling Missing Values...")
    df = df.dropna()  # Drop rows with missing values
    print("After Dropping Missing Values:", df.shape)

    # Remove Duplicates
    print("\nRemoving Duplicates...")
    df = df.drop_duplicates()
    print("After Removing Duplicates:", df.shape)

    return df


def save_data(df, output_path):
    """Save the cleaned data to a new CSV file."""
    try:
        df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")
    except Exception as e:
        print("Error saving data:", e)
        
        
if __name__ == "__main__":
    # Load the data
    data = load_data("data.csv")
    
    if data is not None:
        # Clean the data
        cleaned_data = clean_data(data)
        
        # Save the cleaned data
        save_data(cleaned_data, "cleaned_data.csv")
        
        