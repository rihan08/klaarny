import streamlit as st

def calculate_dscr(net_operating_income, debt_service):
    """Calculate Debt Service Coverage Ratio (DSCR)."""
    return net_operating_income / debt_service

def calculate_taxable_income(rental_income, expenses, depreciation):
    """Calculate taxable income."""
    return rental_income - expenses - depreciation

def calculate_tax(taxable_income, tax_rate):
    """Calculate tax liability."""
    return taxable_income * tax_rate

def calculate_mortgage_payment(loan_amount, mortgage_rate, loan_term_years):
    """Calculate monthly mortgage payment."""
    monthly_rate = mortgage_rate / 12
    num_payments = loan_term_years * 12
    return (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** (-num_payments))

def main():
    st.title("Real Estate Cash Flow and DSCR Analyzer")
    st.write("Compare the financial performance of normal leases vs. 1-month free rental strategies for multiple properties.")

    # User Inputs for General Parameters
    st.sidebar.header("General Parameters")
    tax_rate = st.sidebar.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=21.0) / 100
    depreciation_years = st.sidebar.number_input("Depreciation Period (Years)", min_value=1, value=27)

    # Add Multiple Properties
    st.header("Add Properties")
    num_properties = st.number_input("Number of Properties", min_value=1, value=1)

    results = []

    for i in range(num_properties):
        st.subheader(f"Property {i+1}")

        # Property-Specific Inputs
        col1, col2 = st.columns(2)
        with col1:
            monthly_rent_normal = st.number_input(f"Monthly Rent (Normal Lease) - Property {i+1}", min_value=0.0, value=1000.0)
            monthly_rent_free_strategy = st.number_input(f"Monthly Rent (1-Month Free) - Property {i+1}", min_value=0.0, value=1090.91)
            operating_expenses = st.number_input(f"Monthly Operating Expenses - Property {i+1}", min_value=0.0, value=200.0)
        with col2:
            property_value = st.number_input(f"Property Value - Property {i+1}", min_value=0.0, value=300000.0)
            loan_amount = st.number_input(f"Loan Amount - Property {i+1}", min_value=0.0, value=200000.0)
            mortgage_rate = st.number_input(f"Annual Mortgage Rate (%) - Property {i+1}", min_value=0.0, value=5.0) / 100
            lease_term_years = st.number_input(f"Lease Term (Years) - Property {i+1}", min_value=1, value=1)

        # Calculations
        monthly_mortgage_payment = calculate_mortgage_payment(loan_amount, mortgage_rate, lease_term_years)
        annual_debt_service = monthly_mortgage_payment * 12
        annual_depreciation = property_value / depreciation_years

        # Normal Lease
        annual_rent_normal = monthly_rent_normal * 12
        annual_noi_normal = annual_rent_normal - (operating_expenses * 12)
        taxable_income_normal = calculate_taxable_income(annual_rent_normal, operating_expenses * 12, annual_depreciation)
        tax_normal = calculate_tax(taxable_income_normal, tax_rate)
        dscr_normal = calculate_dscr(annual_noi_normal, annual_debt_service)

        # 1-Month Free Strategy
        annual_rent_free_strategy = monthly_rent_free_strategy * 11  # 11 months of rent
        annual_noi_free_strategy = annual_rent_free_strategy - (operating_expenses * 12)
        taxable_income_free_strategy = calculate_taxable_income(annual_rent_free_strategy, operating_expenses * 12, annual_depreciation)
        tax_free_strategy = calculate_tax(taxable_income_free_strategy, tax_rate)
        dscr_free_strategy = calculate_dscr(annual_noi_free_strategy, annual_debt_service)

        # Store Results
        results.append({
            "Property": i+1,
            "Normal Lease": {
                "Annual NOI": annual_noi_normal,
                "Taxable Income": taxable_income_normal,
                "Tax Liability": tax_normal,
                "DSCR": dscr_normal,
                "Monthly Cash Flow": monthly_rent_normal - operating_expenses
            },
            "1-Month Free Strategy": {
                "Annual NOI": annual_noi_free_strategy,
                "Taxable Income": taxable_income_free_strategy,
                "Tax Liability": tax_free_strategy,
                "DSCR": dscr_free_strategy,
                "Monthly Cash Flow": monthly_rent_free_strategy - operating_expenses
            }
        })

    # Display Results
    st.header("Results")
    for result in results:
        st.subheader(f"Property {result['Property']}")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Normal Lease**")
            st.write(f"Annual NOI: ${result['Normal Lease']['Annual NOI']:.2f}")
            st.write(f"Taxable Income: ${result['Normal Lease']['Taxable Income']:.2f}")
            st.write(f"Tax Liability: ${result['Normal Lease']['Tax Liability']:.2f}")
            st.write(f"DSCR: {result['Normal Lease']['DSCR']:.2f}")
            st.write(f"Monthly Cash Flow: ${result['Normal Lease']['Monthly Cash Flow']:.2f}")
        with col2:
            st.write("**1-Month Free Strategy**")
            st.write(f"Annual NOI: ${result['1-Month Free Strategy']['Annual NOI']:.2f}")
            st.write(f"Taxable Income: ${result['1-Month Free Strategy']['Taxable Income']:.2f}")
            st.write(f"Tax Liability: ${result['1-Month Free Strategy']['Tax Liability']:.2f}")
            st.write(f"DSCR: {result['1-Month Free Strategy']['DSCR']:.2f}")
            st.write(f"Monthly Cash Flow: ${result['1-Month Free Strategy']['Monthly Cash Flow']:.2f}")

if __name__ == "__main__":
    main()