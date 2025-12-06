import streamlit as st 
import pandas as pd 
import plotly.express as px

st.set_page_config(layout='wide', page_title= 'Telecom EDA', page_icon= 'telecom-svgrepo-com.svg')

html_title = "<h1 style='color: white; text-align: center;'>Telecom EDA Project</h1>"
st.markdown(html_title, unsafe_allow_html= True)
#st.image("https://media.istockphoto.com/id/1488521147/photo/global-network-usa-united-states-of-america-north-america-global-business-flight-routes.jpg?s=2048x2048&w=is&k=20&c=MVLf6tCo7bEIhyR8hRlJyiTtej0gZmiaZQyk6Wh2qkY=")
st.image("photo_telecom.jpeg")

page = st.sidebar.radio('Page', ['Home','Univariate', 'Multivariate' ])

df = pd.read_csv('cleaned_df.csv', index_col=0)


total_customers = len(df)
total_churned = (df['churn'] == 'Yes').sum()
churn_rate = round(total_churned / total_customers * 100, 2)
avg_monthly_charges = round(df['monthlycharges'].mean(), 2)


kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("👥 Total Customers", total_customers)
kpi2.metric("💵 Avg Monthly Charges", avg_monthly_charges)
kpi3.metric("📉 Churn Rate (%)", churn_rate)
kpi4.metric("🔻 Total Churned", total_churned)


if page == 'Home':
    st.header('Dataset Overview')
    st.dataframe(df)

    st.header('Dataset Description')
    st.image("description-telecom.png")


elif page == 'Univariate':
    tab_num, tab_cat = st.tabs(['Numerical','Categorical'])
    # Numerical Tab
    num_cols = df.select_dtypes(include='number')     
    column_num = tab_num.selectbox('Select column', num_cols.columns)  
    tab_num.plotly_chart(px.histogram(data_frame = df, x = column_num , title = column_num))


   # Categorical Tab
    cat_cols = df.select_dtypes(include='object')     
    column_cat = tab_cat.selectbox('Select column', cat_cols.columns) 

    chart = tab_cat.selectbox('Select chart', ['Histogram', 'Pie'])

    if chart == 'Histogram':
       fig = px.histogram(data_frame=df, x=column_cat, title=column_cat)
       fig.update_xaxes(categoryorder='max descending')  
       tab_cat.plotly_chart(fig)

    elif chart == 'Pie':
         fig = px.pie(data_frame=df, names=column_cat, title=column_cat)
         tab_cat.plotly_chart(fig)
elif page == 'Multivariate':

     st.header('Is there is any numerical correlation between Data ?')
     df_corr = df.corr(numeric_only=True).round(2)
     st.plotly_chart(px.imshow(df_corr, text_auto = True, width=1000 , height=800))

     st.header('What the average of total Monthly Charges per churn ?')
     churn_MonthlyCharges_df = df.groupby('churn')['monthlycharges'].mean().round(2).reset_index()
     st.plotly_chart(px.bar(data_frame= churn_MonthlyCharges_df , x ='churn' , y = 'monthlycharges', labels = { 'churn' : 'Churn', 'monthlycharges' : 'Average Monthly charges'} ,
        title= 'Average Monthly charges per churn' , text_auto= True ))

    # what the average of total tenure per churn?
     st.header('What the average of total tenure per churn ?')
     churn_tenure_df = df.groupby('churn')['tenure'].mean().round(2).reset_index()
     st.plotly_chart(px.bar(data_frame=churn_tenure_df , x ='churn' , y = 'tenure', labels = { 'churn' : 'Churn', 'tenure' : 'Average Tenure'} , title= 'Average tenure per churn' , text_auto= True ))

     #Which gender make more churn ?
     st.header('Which gender make more churn ?')
     st.plotly_chart(px.histogram(data_frame=df, x = 'gender', color= 'churn' , barmode='group'))


     ## Is the dependents affect churn ?
     st.header('Is the dependents affect churn ?')
     st.plotly_chart(px.histogram(data_frame=df, x = 'dependents', color= 'churn' , barmode='group').update_xaxes(categoryorder = 'max descending' ))

     # Is the partner affect churn?
     st.header('Is the partner affect churn ?')
     st.plotly_chart(px.histogram(data_frame=df, x = 'partner', color= 'churn' , barmode='group').update_xaxes(categoryorder = 'max descending' ))

