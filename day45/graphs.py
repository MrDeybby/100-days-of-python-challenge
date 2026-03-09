import matplotlib.pyplot as plt
import pandas as pd


## Create a user selector for the graph and user input to select the data to graph
# User can choice from the following options:
# 1. Line graph
# 2. Bar graph
# 3. Scatter plot
# and then load the data from a CSV file or manually and graph it using the selected graph type.

def graph_data(graph_type, data):
    x = data.iloc[:, 0].name
    y = data.iloc[:, 1].name
    if graph_type == 'line':
        
        plt.plot(data[x], data[y])
        plt.title('Line Graph')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()
    elif graph_type == 'bar':
        plt.bar(data[x], data[y])
        plt.title('Bar Graph')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()
    elif graph_type == 'scatter':
        plt.scatter(data[x], data[y])
        plt.title('Scatter Plot')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()
    else:
        print("Invalid graph type. Please choose from 'line', 'bar', or 'scatter'.")
        
def load_data_from_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data from CSV: {e}")
        return None


def menu():
    print("Welcome to the Graphing Tool!")
    print("Please select the type of graph you want to create:")
    print("1. Line graph")
    print("2. Bar graph")
    print("3. Scatter plot")
    graph_type = input("Enter the number corresponding to your choice: ")
    
    if graph_type == '1':
        return 'line'
    elif graph_type == '2':
        return 'bar'
    elif graph_type == '3':
        return 'scatter'
    else:
        print("Invalid choice. Please try again.")
        return menu()
    
def main():
    graph_type = menu()
    data_source = input("Do you want to load data from a CSV file? (yes/no): ").lower() == 'yes'
    
    if data_source:
        file_path = input("Enter the path to the CSV file: ")
        data = load_data_from_csv(file_path)
        if data is not None:
            graph_data(graph_type, data)
    else:
        x_values = list(map(float, input("Enter the x values separated by commas: ").split(',')))
        y_values = list(map(float, input("Enter the y values separated by commas: ").split(',')))
        data = {'x': x_values, 'y': y_values}
        graph_data(graph_type, data)
    
if __name__ == "__main__":
    main()
    
