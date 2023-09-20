import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#def portfolio_valuation(principal, monthly_investment, roi_annual, monthly_increase_rate, investment_months, withdrawal_start_multiplier, withdrawal_multiplier, withdrawal_months):
def portfolio_valuation(principal, monthly_investment, roi_annual, monthly_increase_rate, investment_months, withdrawal_start_monthly, withdrawal_start_multiplier, withdrawal_multiplier, withdrawal_months):

    roi_monthly = (1 + roi_annual) ** (1/12) - 1
    values = []
    total_months = investment_months + withdrawal_months
    
    for month in range(1, total_months + 1):
        if month <= investment_months:  # Investing phase
            principal = principal * (1 + roi_monthly) + monthly_investment
            # Adjust the monthly_investment at the end of each year
            if month % 12 == 0:  
                monthly_investment *= (1 + monthly_increase_rate)
        else:  # Withdrawal phase
            yearly_withdrawal_multiplier = withdrawal_start_multiplier * (1 + withdrawal_multiplier) ** (month // 12 - investment_months // 12)
            withdrawal = withdrawal_start_monthly * yearly_withdrawal_multiplier
            principal = principal * (1 + roi_monthly) - withdrawal
            
        if month % 12 == 0:  # Only store values at the end of each year
            values.append(principal)
    
    return values

def plot_portfolio(initial_investment, monthly_investment, roi_annual, monthly_increase_rate, investment_years, withdrawal_start_monthly, withdrawal_years):
    
    investment_months = 12 * investment_years
    withdrawal_months = 12 * withdrawal_years
    withdrawal_start_multiplier = 1.1 ** investment_years
    
    #values = portfolio_valuation(initial_investment, monthly_investment, roi_annual, monthly_increase_rate, 
                                 #investment_months, withdrawal_start_multiplier, roi_annual, withdrawal_months)
    
    values = portfolio_valuation(initial_investment, monthly_investment, roi_annual, monthly_increase_rate, 
                             investment_months, withdrawal_start_monthly, withdrawal_start_multiplier, 
                             roi_annual, withdrawal_months)

    
    values_in_millions = np.array(values) / 1e6
    
    # Plotting
    plt.figure(figsize=(12, 6))
    years = np.arange(1, investment_months//12 + withdrawal_months//12 + 1)
    plt.plot(years, values_in_millions, label="Portfolio Value", color="blue", marker='o')
    plt.xlabel("Years")
    plt.ylabel("Portfolio Value (in Millions)")
    plt.title("Portfolio Valuation with Investments and Withdrawals")
    plt.xticks(years)  # Set x-axis ticks to show each year
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return plt.gcf()  # Return the current figure

def main():
    st.title("Portfolio Valuation with Investments and Withdrawals")

    # Create columns for sliders
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        initial_investment = st.slider('Initial Investment:', 0, 10000, 0, 100)
        monthly_investment = st.slider('Monthly Investment:', 0, 5000, 2000, 100)
        
    with col2:
        roi_annual = st.slider('ROI Annual:', 0.0, 0.2, 0.10, 0.01)
        monthly_increase_rate = st.slider('Monthly Increase Rate:', 0.0, 0.2, 0.05, 0.01)
        
    with col3:
        investment_years = st.slider('Investment Years:', 1, 50, 25, 1)
        withdrawal_start_monthly = st.slider('Withdrawal Start:', 0, 5000, 2000, 100)
        
    with col4:
        withdrawal_years = st.slider('Withdrawal Years:', 1, 50, 25, 1)

    fig = plot_portfolio(initial_investment, monthly_investment, roi_annual, monthly_increase_rate, investment_years, withdrawal_start_monthly, withdrawal_years)
    st.pyplot(fig)  # Display the plot in Streamlit

if __name__ == "__main__":
    main()
