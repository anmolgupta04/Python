"""
Interactive Data Visualization Tool
Supports Matplotlib, Seaborn, and Plotly for creating various chart types
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class DataVisualizationTool:
    """A comprehensive tool for data visualization using multiple libraries"""
    
    def __init__(self, data=None):
        """
        Initialize the visualization tool
        
        Args:
            data: pandas DataFrame or path to CSV file
        """
        if data is None:
            self.df = None
        elif isinstance(data, str):
            self.df = pd.read_csv(data)
        elif isinstance(data, pd.DataFrame):
            self.df = data
        else:
            raise ValueError("Data must be a DataFrame or path to CSV file")
        
        # Set styling
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
    def load_data(self, file_path):
        """Load data from CSV file"""
        self.df = pd.read_csv(file_path)
        print(f"Data loaded successfully! Shape: {self.df.shape}")
        print("\nFirst 5 rows:")
        print(self.df.head())
        return self
    
    def create_sample_data(self):
        """Generate sample data for demonstration"""
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', periods=12, freq='MS')
        
        self.df = pd.DataFrame({
            'Date': dates,
            'Sales': np.random.randint(10000, 50000, 12),
            'Expenses': np.random.randint(5000, 30000, 12),
            'Profit': np.random.randint(3000, 20000, 12),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 12),
            'Category': np.random.choice(['Electronics', 'Clothing', 'Food'], 12)
        })
        print("Sample data generated!")
        print(self.df.head())
        return self
    
    def get_info(self):
        """Display dataset information"""
        print("\n=== Dataset Information ===")
        print(f"Shape: {self.df.shape}")
        print(f"\nColumns: {list(self.df.columns)}")
        print(f"\nData Types:\n{self.df.dtypes}")
        print(f"\nMissing Values:\n{self.df.isnull().sum()}")
        print(f"\nBasic Statistics:\n{self.df.describe()}")
        
    # ============= MATPLOTLIB VISUALIZATIONS =============
    
    def plot_bar_matplotlib(self, x_col, y_col, title="Bar Chart"):
        """Create bar chart using Matplotlib"""
        plt.figure(figsize=(12, 6))
        plt.bar(self.df[x_col], self.df[y_col], color='steelblue', alpha=0.7)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    def plot_line_matplotlib(self, x_col, y_cols, title="Line Chart"):
        """Create line chart using Matplotlib"""
        plt.figure(figsize=(12, 6))
        
        if isinstance(y_cols, str):
            y_cols = [y_cols]
        
        for col in y_cols:
            plt.plot(self.df[x_col], self.df[col], marker='o', label=col, linewidth=2)
        
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel('Values', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    def plot_scatter_matplotlib(self, x_col, y_col, title="Scatter Plot"):
        """Create scatter plot using Matplotlib"""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df[x_col], self.df[y_col], alpha=0.6, s=100, c='coral', edgecolors='black')
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    def plot_histogram_matplotlib(self, col, bins=20, title="Histogram"):
        """Create histogram using Matplotlib"""
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[col], bins=bins, color='green', alpha=0.7, edgecolor='black')
        plt.xlabel(col, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    # ============= SEABORN VISUALIZATIONS =============
    
    def plot_bar_seaborn(self, x_col, y_col, hue=None, title="Bar Chart"):
        """Create bar chart using Seaborn"""
        plt.figure(figsize=(12, 6))
        sns.barplot(data=self.df, x=x_col, y=y_col, hue=hue, palette='viridis')
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
    def plot_box_seaborn(self, x_col=None, y_col=None, title="Box Plot"):
        """Create box plot using Seaborn"""
        plt.figure(figsize=(10, 6))
        if x_col:
            sns.boxplot(data=self.df, x=x_col, y=y_col, palette='Set2')
        else:
            sns.boxplot(data=self.df[y_col], palette='Set2')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
    def plot_violin_seaborn(self, x_col, y_col, title="Violin Plot"):
        """Create violin plot using Seaborn"""
        plt.figure(figsize=(12, 6))
        sns.violinplot(data=self.df, x=x_col, y=y_col, palette='muted')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
    def plot_heatmap_seaborn(self, title="Correlation Heatmap"):
        """Create correlation heatmap using Seaborn"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
    def plot_pairplot_seaborn(self, hue=None):
        """Create pairplot using Seaborn"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        sns.pairplot(self.df[numeric_cols], hue=hue, palette='husl', diag_kind='kde')
        plt.suptitle('Pairplot of Numeric Variables', y=1.02, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    # ============= PLOTLY VISUALIZATIONS =============
    
    def plot_bar_plotly(self, x_col, y_col, title="Interactive Bar Chart"):
        """Create interactive bar chart using Plotly"""
        fig = px.bar(self.df, x=x_col, y=y_col, title=title,
                     color=y_col, color_continuous_scale='Blues')
        fig.update_layout(template='plotly_white', height=500)
        fig.show()
        
    def plot_line_plotly(self, x_col, y_cols, title="Interactive Line Chart"):
        """Create interactive line chart using Plotly"""
        if isinstance(y_cols, str):
            y_cols = [y_cols]
        
        fig = go.Figure()
        for col in y_cols:
            fig.add_trace(go.Scatter(x=self.df[x_col], y=self.df[col], 
                                    mode='lines+markers', name=col))
        
        fig.update_layout(title=title, xaxis_title=x_col, yaxis_title='Values',
                         template='plotly_white', height=500, hovermode='x unified')
        fig.show()
        
    def plot_scatter_plotly(self, x_col, y_col, color_col=None, size_col=None, 
                           title="Interactive Scatter Plot"):
        """Create interactive scatter plot using Plotly"""
        fig = px.scatter(self.df, x=x_col, y=y_col, color=color_col, size=size_col,
                        title=title, hover_data=self.df.columns)
        fig.update_layout(template='plotly_white', height=500)
        fig.show()
        
    def plot_pie_plotly(self, names_col, values_col, title="Interactive Pie Chart"):
        """Create interactive pie chart using Plotly"""
        fig = px.pie(self.df, names=names_col, values=values_col, title=title,
                    hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        fig.show()
        
    def plot_histogram_plotly(self, col, title="Interactive Histogram"):
        """Create interactive histogram using Plotly"""
        fig = px.histogram(self.df, x=col, title=title, nbins=30,
                          color_discrete_sequence=['indianred'])
        fig.update_layout(template='plotly_white', height=500)
        fig.show()
        
    def plot_box_plotly(self, y_col, x_col=None, title="Interactive Box Plot"):
        """Create interactive box plot using Plotly"""
        fig = px.box(self.df, x=x_col, y=y_col, title=title,
                    color=x_col, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(template='plotly_white', height=500)
        fig.show()
        
    def plot_3d_scatter_plotly(self, x_col, y_col, z_col, color_col=None,
                              title="3D Scatter Plot"):
        """Create 3D scatter plot using Plotly"""
        fig = px.scatter_3d(self.df, x=x_col, y=y_col, z=z_col, color=color_col,
                           title=title)
        fig.update_layout(height=600)
        fig.show()
        
    def plot_sunburst_plotly(self, path_cols, values_col, title="Sunburst Chart"):
        """Create sunburst chart using Plotly"""
        fig = px.sunburst(self.df, path=path_cols, values=values_col, title=title)
        fig.update_layout(height=600)
        fig.show()
    
    # ============= ADVANCED VISUALIZATIONS =============
    
    def plot_dashboard(self):
        """Create a comprehensive dashboard with multiple visualizations"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:3]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribution', 'Time Series', 'Correlation', 'Box Plot'),
            specs=[[{'type': 'histogram'}, {'type': 'scatter'}],
                   [{'type': 'heatmap'}, {'type': 'box'}]]
        )
        
        # Histogram
        fig.add_trace(go.Histogram(x=self.df[numeric_cols[0]], name=numeric_cols[0]),
                     row=1, col=1)
        
        # Line chart
        fig.add_trace(go.Scatter(y=self.df[numeric_cols[0]], mode='lines+markers',
                                name=numeric_cols[0]), row=1, col=2)
        
        # Heatmap
        corr = self.df[numeric_cols].corr()
        fig.add_trace(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns,
                                colorscale='RdBu'), row=2, col=1)
        
        # Box plot
        fig.add_trace(go.Box(y=self.df[numeric_cols[0]], name=numeric_cols[0]),
                     row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False, title_text="Data Dashboard")
        fig.show()
        
    def save_chart(self, fig, filename, format='png'):
        """Save chart to file"""
        if format == 'html':
            fig.write_html(filename)
        else:
            fig.write_image(filename, format=format)
        print(f"Chart saved as {filename}")


# ============= USAGE EXAMPLES =============

def main():
    """Demonstrate the Data Visualization Tool"""
    
    print("=" * 60)
    print("DATA VISUALIZATION TOOL")
    print("=" * 60)
    
    # Initialize tool with sample data
    viz = DataVisualizationTool()
    viz.create_sample_data()
    
    print("\n" + "=" * 60)
    print("DATASET INFORMATION")
    print("=" * 60)
    viz.get_info()
    
    # Matplotlib Examples
    print("\n" + "=" * 60)
    print("MATPLOTLIB VISUALIZATIONS")
    print("=" * 60)
    
    print("\n1. Bar Chart (Matplotlib)")
    viz.plot_bar_matplotlib('Region', 'Sales', 'Sales by Region')
    
    print("\n2. Line Chart (Matplotlib)")
    viz.plot_line_matplotlib('Date', ['Sales', 'Expenses', 'Profit'], 
                            'Monthly Trends')
    
    print("\n3. Scatter Plot (Matplotlib)")
    viz.plot_scatter_matplotlib('Sales', 'Profit', 'Sales vs Profit')
    
    print("\n4. Histogram (Matplotlib)")
    viz.plot_histogram_matplotlib('Sales', bins=15, title='Sales Distribution')
    
    # Seaborn Examples
    print("\n" + "=" * 60)
    print("SEABORN VISUALIZATIONS")
    print("=" * 60)
    
    print("\n5. Bar Chart with Hue (Seaborn)")
    viz.plot_bar_seaborn('Region', 'Sales', hue='Category', 
                        title='Sales by Region and Category')
    
    print("\n6. Box Plot (Seaborn)")
    viz.plot_box_seaborn('Region', 'Sales', title='Sales Distribution by Region')
    
    print("\n7. Violin Plot (Seaborn)")
    viz.plot_violin_seaborn('Region', 'Profit', title='Profit Distribution by Region')
    
    print("\n8. Correlation Heatmap (Seaborn)")
    viz.plot_heatmap_seaborn('Correlation Matrix')
    
    # Plotly Examples
    print("\n" + "=" * 60)
    print("PLOTLY INTERACTIVE VISUALIZATIONS")
    print("=" * 60)
    
    print("\n9. Interactive Bar Chart (Plotly)")
    viz.plot_bar_plotly('Region', 'Sales', 'Interactive Sales by Region')
    
    print("\n10. Interactive Line Chart (Plotly)")
    viz.plot_line_plotly('Date', ['Sales', 'Expenses'], 
                        'Interactive Monthly Trends')
    
    print("\n11. Interactive Scatter Plot (Plotly)")
    viz.plot_scatter_plotly('Sales', 'Profit', color_col='Region',
                           title='Sales vs Profit by Region')
    
    print("\n12. Interactive Pie Chart (Plotly)")
    viz.plot_pie_plotly('Region', 'Sales', 'Sales Distribution by Region')
    
    print("\n13. Interactive Histogram (Plotly)")
    viz.plot_histogram_plotly('Sales', 'Sales Distribution')
    
    print("\n14. Interactive Box Plot (Plotly)")
    viz.plot_box_plotly('Sales', 'Region', 'Sales Distribution by Region')
    
    print("\n15. Dashboard (Plotly)")
    viz.plot_dashboard()
    
    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the main demonstration
    main()
    
    # Example: Load your own data
    # viz = DataVisualizationTool('your_data.csv')
    # viz.plot_bar_plotly('column_x', 'column_y')