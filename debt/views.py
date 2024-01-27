from django.shortcuts import render
from .forms_loan import CustomerLoan
from .form_customer import CustomerAdd
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.db.models import Count
import numpy as np
import plotly.express as px
import scipy.stats as stats
from django.db.models import Sum
from plotly.offline import plot
import plotly.graph_objs as go

#home page to display Business Target
def home(request):
   # Calculate the total sum of Loan.RequestedLoan
    total_requested_loan = Loan.objects.aggregate(Sum('RequestedAmount'))['RequestedAmount__sum']

    # Set the target amount /take last added field
    fetch_target = Target.objects.latest('RegisteredDate')
    target_amount=fetch_target.Amount

    # Calculate the percentage position
    percentage_position = (total_requested_loan / target_amount) * 100

    # Create a gauge chart using Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_requested_loan,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Requested Loan By Target"},
        gauge=dict(
            axis=dict(range=[None, target_amount]),
            steps=[
                {'range': [0, target_amount / 3], 'color': "lightgray"},
                {'range': [target_amount / 3, 2 * target_amount / 3], 'color': "#E4A11B"},
                {'range': [2 * target_amount / 3, target_amount], 'color': "darkgray"}
            ],
            threshold=dict(
                line={'color': "red", 'width': 4},
                thickness=0.75,
                value=total_requested_loan
            )
        )
    ))

    # Add legend and percentage position
    fig.update_layout(
        showlegend=True,
        legend=dict(title='Legend'),
        font=dict(family='Roboto Condensed, sans-serif'),  
        annotations=[
            {
                'x': 0.5,
                'y': 0.5,
                'xref': 'paper',
                'yref': 'paper',
                'text': f'{percentage_position:.2f}%',
                'showarrow': False,
                'font': {'size': 20}
            }
        ],
    # Adjust margins as needed   
    margin=dict(l=20, r=20, t=20, b=20)  
    )

    # Convert the figure to HTML
    gauge_html = plot(fig, output_type='div')

    # Format the monetary values in TZS format
    import locale
    locale.setlocale(locale.LC_ALL, 'sw_TZ.UTF-8')
    formatted_total_requested_loan = locale.currency(total_requested_loan, grouping=True).replace(".00", "")
    formatted_target_amount = locale.currency(target_amount, grouping=True).replace(".00", "")

    return render(request, "home.html",{'gauge': gauge_html,'target':formatted_target_amount,'total_requested_loan': formatted_total_requested_loan})



#Register Loan
def loan(request):
    form=CustomerLoan(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Registered Successfully !")
        form=CustomerLoan()
        return HttpResponseRedirect('/loan')
    context={
        "form":form
    }
    return render(request, "loan.html",context)

 #Register New Customer
def newcustomer(request):
    if request.method == 'POST':
        form_customer = CustomerAdd(request.POST, request.FILES)
        if form_customer.is_valid():
            form_customer.save()
            form_customer=CustomerAdd()
            messages.success(request, "Registered Successfully!")
            return HttpResponseRedirect('/customer')
        else:
            messages.error(request, "Error in form submission. Please check the form.")
    else:
        form_customer = CustomerAdd()

    context = {
        "form": form_customer
    }
    return render(request, "customers.html", context)





#simple analytics
def analytics(request):
    # Query to fetch data from Loan and Customer models based on CustomerNationalID
    loans_with_customers = Loan.objects.select_related('Customer', 'EmployeeID').filter(
        Customer__CustomerNationalID__isnull=False)

    # Separate query to calculate the sum of certain fields
    sum_data = Loan.objects.aggregate(
        total_requested_amount=Sum('RequestedAmount'),
        total_interest=Sum('Interest'),
        total_actual_debt=Sum('ActualDebt'),
        total_cash_receivable=Sum('CashReceivable'),
    )
    # Format the sum_data with TZS monetary representation
    formatted_sum_data = {
        'total_requested_amount': '{:,.2f} TZS'.format(sum_data['total_requested_amount'] or 0),
        'total_interest': '{:,.2f} TZS'.format(sum_data['total_interest'] or 0),
        'total_actual_debt': '{:,.2f} TZS'.format(sum_data['total_actual_debt'] or 0),
        'total_cash_receivable': '{:,.2f} TZS'.format(sum_data['total_cash_receivable'] or 0),
    }

    # Fetch data for customers who have taken a loan
    customers_with_loans = Customer.objects.filter(loan__isnull=False).distinct()

    # Get the frequencies of each resident for customers with loans
    resident_frequencies = customers_with_loans.values('Resident').annotate(count=Count('Resident'))

    # Create a bar graph using Plotly Express
    bar_graph = px.bar(resident_frequencies, x='Resident', y='count',
                       title='Customer Locations [ Given a Loan is Taken ]',
                       labels={'count': 'Frequency', 'Resident': 'Customer Resident'},
                       category_orders={'Resident': ['Resident1', 'Resident2',
                                                     'Resident3']})  

    # Customize the layout
    bar_graph.update_layout(
        showlegend=True,
        xaxis=dict(title='Customer Resident', 
                   showgrid=True, 
                   gridwidth=1,
                     gridcolor='lightgray',
                   categoryorder='total descending'),

        yaxis=dict(title='Frequency', 
                   showgrid=True,
                     gridwidth=1,
                       gridcolor='lightgray'),

        legend=dict(title='Customer Resident'),
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',  # Make background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Make plot area transparent

        font=dict(family='Roboto Condensed, sans-serif'),  # Set font family for the entire graph
    )
    bar_graph.update_traces(marker_color='#343a40')
    # Convert the figure to HTML
    bar_graph_html = bar_graph.to_html(full_html=False)

    return render(request,
                   'analytics.html',
                  {'loans_with_customers': loans_with_customers, 
                   'formatted_sum_data': formatted_sum_data,
                   'bar_graph_html': bar_graph_html, })

#simple trends
def trends(request):
    # Prepare data for box plots
    # Separate query to get data for box plots
    box_plot_data = Loan.objects.values(
        'LoanID',
        'QualityAssurance',
        'MonthlyInstallment',
        'ActualDebt',
        'CashReceivable',
        'Interest',
        'RequestedAmount'
    )
    box_plot_traces = []
    for field in ['QualityAssurance', 'MonthlyInstallment', 'ActualDebt', 'CashReceivable', 'Interest',
                  'RequestedAmount']:
        trace = go.Box(
            y=[item[field] for item in box_plot_data],
            name=field,
            # boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            boxmean='sd',  # Display standard deviation as well
            boxpoints='outliers',  # Display outliers

        )
        box_plot_traces.append(trace)

    # Layout for the box plots
    layout = go.Layout(
        title='Box Plots for Loan Metrics',
        xaxis=dict(title='Metrics'),
        yaxis=dict(title='Amount (TZS)'),
        boxmode='group',
        plot_bgcolor='rgba(0,0,0,0)',  # Remove background color
        margin=dict(l=50, r=50, b=50, t=80),  # Adjust margin for better appearance
        font=dict(family='Roboto Condensed, sans-serif'),  # Set font family for the entire graph

    )
    # Create the figure
    box_plot_figure = go.Figure(data=box_plot_traces, layout=layout)

    # Convert the figure to HTML
    box_plot_html = plot(box_plot_figure, output_type='div')

    # Query to fetch data from Loan and Customer models based on CustomerNationalID
    loans_with_customers = Loan.objects.select_related('Customer', 'EmployeeID').filter(
        Customer__CustomerNationalID__isnull=False)

    # Separate query to get data for Interest
    interest_data = Loan.objects.values_list('Interest', flat=True)

    # Calculate Z-scores for Interest
    z_scores = stats.zscore(interest_data)
    # Generate Normal Distribution curve
    x_values = np.linspace(min(interest_data) - 3 * np.std(interest_data),
                           max(interest_data) + 3 * np.std(interest_data), 1000)
    y_values = stats.norm.pdf(x_values, np.mean(interest_data), np.std(interest_data))

    # Calculate Z-scores for Interest
    z_scores = stats.zscore(interest_data)

    # Get the indices of outliers (Z-scores > 3 or < -3)
    outlier_indices = np.where(np.abs(z_scores) > 3)[0]

    # Plot Normal Distribution curve
    curve_trace = go.Scatter(x=x_values, y=y_values, mode='lines', name='Normal Distribution Curve')

    # Highlight outliers in red
    outlier_trace = go.Scatter(x=np.array(interest_data)[outlier_indices], y=np.zeros(len(outlier_indices)),
                               mode='markers', name='Outliers', marker=dict(color='red', size=8))

    # Add threshold lines at 3 standard deviations
    threshold_positive = np.mean(interest_data) + 3 * np.std(interest_data)
    threshold_negative = np.mean(interest_data) - 3 * np.std(interest_data)
    threshold_trace_positive = go.Scatter(x=[threshold_positive, threshold_positive], y=[0, max(y_values)],
                                          mode='lines', name='Threshold (3 SD) - Positive', line=dict(dash='dash'))
    threshold_trace_negative = go.Scatter(x=[threshold_negative, threshold_negative], y=[0, max(y_values)],
                                          mode='lines', name='Threshold (3 SD) - Negative', line=dict(dash='dash'))

    # Add a vertical line at the mean
    mean_trace = go.Scatter(x=[np.mean(interest_data), np.mean(interest_data)], y=[0, max(y_values)],
                            mode='lines', name='Mean', line=dict(color='red', dash='dash'))

    # Create the figure
    distribution_figure = go.Figure(data=[curve_trace, threshold_trace_positive, threshold_trace_negative,
                                          mean_trace, outlier_trace],
                                          layout=go.Layout(title='Normal Distribution Curve for Interest',
                                                     showlegend=True,  # Disable legend
                                                     xaxis=dict(title='Interest'),
                                                     yaxis=dict(title='Density'),
                                                     plot_bgcolor='rgba(0,0,0,0)',  # Remove background
                                                     font=dict(family='Roboto Condensed, sans-serif'),
                                                     # Set font family for the entire graph
                                                     ))

    # Convert the figure to HTML
    distribution_html = plot(distribution_figure, output_type='div')
    # Create a table of Z-scores and PDF for each Interest
    z_score_table = []
    for interest, z_score in zip(interest_data, z_scores):
        pdf_value = stats.norm.pdf(interest, np.mean(interest_data), np.std(interest_data))
        if z_score > 3 or z_score < -3:
            status = "Out of Range"
        else:
            status = "Normally"
        z_score_table.append({
            'Interest': round(interest, 1),
            'Z_Score': round(z_score, 3),
            'PDF': round(pdf_value,9),
            "Status": status
        })

    # Pass the data to the template
    return render(request, 'trends.html', {'box_plot_html': box_plot_html,
                                           'loans_with_customers': loans_with_customers,
                                           'distribution_html': distribution_html,
                                           'z_score_table': z_score_table,
                                           
                                           })




import plotly.io as pio
def checkup(request):

   # Fetch data from models
    loans = Loan.objects.all()
    customers = Customer.objects.all()

    # Create a DataFrame for easy manipulation
    loan_data = {
        'CustomerResident': [],
        'RequestedAmountSum': [],
        'Type': [],
    }

    for customer in customers:
        loans_for_customer = loans.filter(Customer=customer)
        if loans_for_customer.exists():
            sum_requested_amount = loans_for_customer.aggregate(SumRequestedAmount=models.Sum('RequestedAmount'))['SumRequestedAmount']

            loan_data['CustomerResident'].append(customer.Resident)
            loan_data['RequestedAmountSum'].append(sum_requested_amount)
            loan_data['Type'].append('Max')

            loan_data['CustomerResident'].append(customer.Resident)
            loan_data['RequestedAmountSum'].append(sum_requested_amount)
            loan_data['Type'].append('Min')

   # Create Plotly bar graph
    fig = px.bar(loan_data, x='CustomerResident', y='RequestedAmountSum', color='Type',
                 labels={'RequestedAmountSum': 'Requested Amount Sum'},
                 title='Sum of Loan Requested Amounts (Max and Min) by Customer Resident',
                 barmode='group',
                 color_discrete_map={'Max': '#28a745', 'Min': '#343a40'})  # 
   

    # Update layout for transparency, grids, and borders
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Background transparency
        plot_bgcolor='rgba(0,0,0,0)',   # Plot area transparency
        xaxis=dict(gridcolor='rgba(255,255,255,0.5)', showgrid=True),  # Grid color for x-axis
        yaxis=dict(gridcolor='rgba(255,255,255,0.5)', showgrid=True),
        showlegend=True,
        font=dict(family="Roboto Condensed, sans-serif"),  # Set font family
    )

    # Convert the Plotly figure to HTML format for rendering in the template
    graph_html = pio.to_html(fig, full_html=False)

    # Render the template with the graph
    return render(request, 'checkup.html', {'graph_html': graph_html})








































 