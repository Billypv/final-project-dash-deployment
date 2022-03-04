import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from matplotlib.pyplot import figure, xlabel
import pandas as pd
import plotly.express as px


                
most_purchased_product_overall = pd.read_csv("cleaned_data/requirement_one/most_purchased_product_overall.csv")
most_purchased_product_per_region = pd.read_csv("cleaned_data/requirement_one/most_purchased_product_per_region.csv")
most_purchased_product_per_county = pd.read_csv("cleaned_data/requirement_one/most_purchased_product_per_county.csv")
most_purchased_catagory_overall = pd.read_csv("cleaned_data/requirement_one/most_purchased_catagory_overall.csv")
most_purchased_catagory_per_region = pd.read_csv("cleaned_data/requirement_one/most_purchased_catagory_per_region.csv")
most_purchased_catagory_per_county = pd.read_csv("cleaned_data/requirement_one/most_purchased_catagory_per_county.csv")         

branch_quantity_sold_per_region = pd.read_csv("cleaned_data/requirement_two/branch_quantity_sold_per_region.csv")
branch_quantity_sold_per_county = pd.read_csv("cleaned_data/requirement_two/branch_quantity_sold_per_county.csv")
branch_amount_in_gbp_per_region = pd.read_csv("cleaned_data/requirement_two/branch_amount_in_gbp_per_region.csv")
branch_amount_in_gbp_per_county = pd.read_csv("cleaned_data/requirement_two/branch_amount_in_gbp_per_county.csv")
branch_performance_per_county = branch_quantity_sold_per_county.merge(branch_amount_in_gbp_per_county, on=["branch", "county"])
branch_performance_per_region = branch_quantity_sold_per_region.merge(branch_amount_in_gbp_per_region, on=["branch","region"])
branch_performance_per_county = branch_performance_per_county.sort_values(by="amount_in_gbp", ascending=False)
branch_performance_per_region = branch_performance_per_region.sort_values(by="amount_in_gbp", ascending=False)

top_ten_sales_dataframes_per_hour = pd.read_csv("cleaned_data/requirement_three/top_ten_sales_dataframes_per_hour.csv")

branch_profit = pd.read_csv("cleaned_data/requirement_four/branch_profit.csv")

county_dropdown_options = []
for county in most_purchased_catagory_per_county.county.unique():
    county_dropdown_options.append({"label": county, "value":county})

region_dropdown_options = []
for region in most_purchased_catagory_per_region.region.unique():
    region_dropdown_options.append({"label": region, "value":region})
    
top_ten_branches_options = []
for branch in top_ten_sales_dataframes_per_hour.branch.unique():
    top_ten_branches_options.append({"label":branch, "value":branch})
    

most_purchased_product_overall_figure = px.bar(most_purchased_product_overall.head(5), x="item", y = "quantity", title = "Most purchased product overall")
least_purchased_product_overall_figure = px.bar(most_purchased_product_overall.tail(5), x="item", y = "quantity", title = "Least purchased product overall")
most_purchased_catagory_overall_figure = px.bar(most_purchased_catagory_overall.head(5), x="catagory", y = "quantity",title = "Most purchased catagory overall" )
least_purchased_catagory_overall_figure = px.bar(most_purchased_catagory_overall.tail(5), x="catagory", y = "quantity" ,title = "Least purchased catagory overall" )

app = dash.Dash(__name__, title= "Dashboard")
server = app.server
app.layout = html.Div([
    html.Div([
        html.H1("Shop Dashboard"),

    ]),
    html.Div([
        html.H2("Most and least purchased Products and Product Catagories overall"),
        html.Div([
            dcc.Graph(figure= most_purchased_product_overall_figure),
            dcc.Graph(figure= least_purchased_product_overall_figure),
            dcc.Graph(figure=most_purchased_catagory_overall_figure),
            dcc.Graph(figure=least_purchased_catagory_overall_figure)
                        
            ]),
        ]),
        html.Div([
            html.H2("Top and bottom most profitable branches"),
            html.Div([
                dcc.Graph(figure=px.bar(branch_profit.head(10), x= "branch", y = "profit", title= f'most profitable branches')),
                dcc.Graph(figure=px.bar(branch_profit.tail(10), x= "branch", y = "profit", title= f'least profitable branches'))
            ])
        ]),
        html.H2("Most and Least Purchased Products and Product catagories by county"),
        dcc.Dropdown(options=county_dropdown_options, id = "product_catagory_overall_county_dropdown"),
        html.Div([
        dcc.Graph(id = "product_most_purchased_county"),
        dcc.Graph(id = "product_least_purchased_county"),
        dcc.Graph(id = "catagory_most_purchased_county"),
        dcc.Graph(id = "catagory_least_purchased_county")               
        ]),
        html.H2("Most and Least Purchased Products and Product catagories by Region"),
        dcc.Dropdown(options=region_dropdown_options, id = "product_catagory_overall_region_dropdown"),
        html.Div([
        dcc.Graph(id = "product_most_purchased_region"),
        dcc.Graph(id = "product_least_purchased_region"),
        dcc.Graph(id = "catagory_most_purchased_region"),
        dcc.Graph(id = "catagory_least_purchased_region")               
        ]),
        
        

    
    html.Div([
        html.H2("Best Perfoming Branches by County"),
        dcc.Dropdown(options=county_dropdown_options, id = "branch_performance_by_county_dropdown"),
        html.Div([
        dcc.Graph(id = "best_performing_branch_county"),
        dcc.Graph(id = "worst_performing_branch_county"),
            
        ])
        
    ]),
    html.Div([
        html.H2("Best Perfoming Branches by Region"),
        dcc.Dropdown(options=region_dropdown_options, id = "branch_performance_by_region_dropdown"),
        html.Div([
        dcc.Graph(id = "best_performing_branch_region"),
        dcc.Graph(id = "worst_performing_branch_region"),
            
        ])        
    ]),
    html.Div([
        html.H2("Top 10 branches sales per hour"),
        dcc.Dropdown(options=top_ten_branches_options, id = "top_ten_sales_per_hour_dropdown"),
        html.Div([
            dcc.Graph(id = "top_ten_sales_per_hour")
        ])
    ])    

    
    
])
                
                
@app.callback(
    Output(component_id="product_most_purchased_county", component_property="figure"),
    Output(component_id="product_least_purchased_county", component_property="figure"),
    Output(component_id="catagory_most_purchased_county", component_property="figure"),
    Output(component_id="catagory_least_purchased_county", component_property="figure"),
    Input(component_id="product_catagory_overall_county_dropdown", component_property="value")
)               
def plot_products_and_categories_by_county(value):
    figure_one = px.bar(most_purchased_product_per_county[most_purchased_product_per_county["county"] == value].head(5), x= "item", y = "quantity", title= f'most purchased products for {value}')
    figure_two = px.bar(most_purchased_product_per_county[most_purchased_product_per_county["county"] == value].tail(5), x= "item", y = "quantity", title= f'least purchased products for {value}')
    figure_three = px.bar(most_purchased_catagory_per_county[most_purchased_catagory_per_county["county"] == value].head(5), x= "catagory", y = "quantity", title= f'most purchased catagorys for {value}')
    figure_four = px.bar(most_purchased_catagory_per_county[most_purchased_catagory_per_county["county"] == value].tail(5), x= "catagory", y = "quantity", title= f'least purchased catagorys for {value}')
    return figure_one, figure_two, figure_three, figure_four

@app.callback(
    Output(component_id="product_most_purchased_region", component_property="figure"),
    Output(component_id="product_least_purchased_region", component_property="figure"),
    Output(component_id="catagory_most_purchased_region", component_property="figure"),
    Output(component_id="catagory_least_purchased_region", component_property="figure"),
    Input(component_id="product_catagory_overall_region_dropdown", component_property="value")
)               
def plot_products_and_categories_by_region(value):
    figure_one = px.bar(most_purchased_product_per_region[most_purchased_product_per_region["region"] == value].head(5), x= "item", y = "quantity", title= f'most purchased products for {value}')
    figure_two = px.bar(most_purchased_product_per_region[most_purchased_product_per_region["region"] == value].tail(5), x= "item", y = "quantity", title= f'least purchased products for {value}')
    figure_three = px.bar(most_purchased_catagory_per_region[most_purchased_catagory_per_region["region"] == value].head(5), x= "catagory", y = "quantity", title= f'most purchased catagorys for {value}')
    figure_four = px.bar(most_purchased_catagory_per_region[most_purchased_catagory_per_region["region"] == value].tail(5), x= "catagory", y = "quantity", title= f'least purchased catagorys for {value}')
    return figure_one, figure_two, figure_three, figure_four

@app.callback(
    Output(component_id="best_performing_branch_county", component_property="figure"),
    Output(component_id="worst_performing_branch_county", component_property="figure"),
    Input(component_id="branch_performance_by_county_dropdown", component_property="value")
)               
def plot_branch_success_by_county(value):
    figure_one = px.bar(branch_performance_per_county[branch_performance_per_county["county"] == value].head(5), x= "branch", y = ["amount_in_gbp","quantity"], title= f'most successful branches for {value}')
    figure_two = px.bar(branch_performance_per_county[branch_performance_per_county["county"] == value].tail(5), x= "branch", y = ["amount_in_gbp","quantity"], title= f'least successful branches for {value}')
    return figure_one, figure_two

@app.callback(
    Output(component_id="best_performing_branch_region", component_property="figure"),
    Output(component_id="worst_performing_branch_region", component_property="figure"),
    Input(component_id="branch_performance_by_region_dropdown", component_property="value")
)               
def plot_branch_success_by_region(value):
    figure_one = px.bar(branch_performance_per_region[branch_performance_per_region["region"] == value].head(5), x= "branch", y = ["amount_in_gbp","quantity"], title= f'most successful branches for {value}')
    figure_two = px.bar(branch_performance_per_region[branch_performance_per_region["region"] == value].tail(5), x= "branch", y = ["amount_in_gbp","quantity"], title= f'least successful branches for {value}')
    return figure_one, figure_two

@app.callback(
    Output(component_id="top_ten_sales_per_hour", component_property="figure"),
    Input(component_id="top_ten_sales_per_hour_dropdown", component_property="value")
)               
def plot_branch_success_by_region(value):
    figure_one = px.line(top_ten_sales_dataframes_per_hour[top_ten_sales_dataframes_per_hour["branch"] == value].reset_index(), y ="quantity" , title= f'Sales per hour for {value}',labels={"_index":"Hours"})
    return figure_one



                
                
                





                
app.run_server(debug=True)

