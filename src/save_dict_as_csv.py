import csv

data = {
    'Thu nhập lãi và các khoản thu nhập tương tự': 'interest_income_and_similar_income',
    'Chi phí lãi và các chi phí tương tự': 'interest_expense_and_similar_expenses',
    'Thu nhập lãi thuần': 'net_interest_income',
    'Thu nhập từ hoạt động dịch vụ': 'income_from_service_activities',
    'Chi phí hoạt động dịch vụ': 'service_activity_expenses',
    'Lãi thuần từ hoạt động dịch vụ': 'net_profit_from_service_activities',
    'Lãi/(lỗ) thuần từ hoạy động kinh doanh ngoại hối và vàng': 'net_profit_or_loss_from_foreign_exchange_and_gold_trading_activities',
    'Lãi/(lỗ) thuần từ mua bán chứng khoán kinh doanh': 'net_profit_or_loss_from_trading_securities_activities',
    'Lãi/(lỗ) thuần từ mua bán chứng khoán đầu tư': 'net_profit_or_loss_from_investment_securities_activities',
    'Thu nhập từ hoạt động khác': 'income_from_other_activities',
    'Chi phí hoạt động khác': 'other_operating_expenses',
    'Lãi/(lỗ) thuần từ hoạt động khác': 'net_profit_or_loss_from_other_activities',
    'Thu nhập từ góp vốn, mua cổ phần': 'income_from_contributions_share_purchases',
    'Tổng thu nhập hoạt động': 'total_operating_income',
    'Chi phí hoạt động': 'operating_expenses',
    'LN thuần từ hoạt động kinh doanh trước CF dự phòng rủi ro tín dụng': 'net_profit_from_business_operations_before_credit_risk_provisions',
    'Chi phí dự phòng rủi ro tín dụng': 'credit_risk_provisions_expenses',
    'Tổng lợi nhuận trước thuế': 'total_pre_tax_profit',
    'Chi phí thuế TNDN hiện hành': 'current_corporate_income_tax_expenses',
    'Chi phí thuế TNDN hoãn lại': 'deferred_corporate_income_tax_expenses',
    'Chi phí thuế thu nhập doanh nghiệp': 'income_tax_expenses',
    'Lợi nhuận sau thuế': 'profit_after_tax',
    'Lợi ích của cổ đông thiểu số': 'minority_interest',
    'Cổ đông của Công ty mẹ': 'shareholders_of_the_parent_company',
    'Lãi cơ bản trên cổ phiếu': 'basic_earnings_per_share',
    'Doanh số': 'revenue',
    'Các khoản giảm trừ': 'deductions',
    'Doanh số thuần': 'net_sales',
    'Giá vốn hàng bán': 'cost_of_goods_sold',
    'Lãi gộp': 'gross_profit',
    'Thu nhập tài chính': 'financial_income',
    'Chi phí tài chính': 'financial_expenses',
    'Trong đó: Chi phí lãi vay': 'including_interest_expenses',
    'Lãi/(lỗ) từ công ty liên doanh': 'profit_or_loss_from_joint_ventures',
    'Chi phí bán hàng': 'selling_expenses',
    'Chi phí quản lý doanh  nghiệp': 'administrative_expenses',
    'Lãi/(lỗ) từ hoạt động kinh doanh': 'profit_or_loss_from_business_operations',
    'Thu nhập khác': 'other_income',
    'Chi phí khác': 'other_expenses',
    'Thu nhập khác, ròng': 'net_other_income',
    'Lãi/(lỗ) ròng trước thuế': 'net_profit_or_loss_before_tax',
    'Thuế thu nhập doanh nghiệp – hiện thời': 'current_corporate_income_tax',
    'Thuế thu nhập doanh nghiệp – hoãn lại': 'deferred_corporate_income_tax',
    'Chi phí thuế thu nhập doanh nghiệp': 'corporate_income_tax_expenses',
    'Lãi/(lỗ) thuần sau thuế': 'net_profit_or_loss_after_tax',
    'Lợi ích của cổ đông thiểu số': 'minority_interest',
    'Lợi nhuận của Cổ đông của Công ty mẹ': 'profit_attributable_to_shareholders_of_the_parent_company',
    'Lãi cơ bản trên cổ phiếu': 'basic_earnings_per_share',
    'Lãi trên cổ phiếu pha loãng': 'diluted_earnings_per_share',

    'Lưu chuyển tiền thuần từ các hoạt động sản xuất kinh doanh': 'net_cash_flow_from_operating_activities',
    'Lãi/lỗ trước những thay đổi vốn lưu động': 'profit_loss_before_changes_in_working_capital',
    'Lãi trước thuế': 'profit_before_tax',
    'Khấu hao TSCĐ': 'depreciation_of_fixed_assets',
    'Chi phí dự phòng': 'provision_expenses',
    'Lãi/(lỗ) chênh lệch tỷ giá chưa thực hiện': 'unrealized_exchange_rate_gain_loss',
    'Lãi/(lỗ) từ thanh lý tài sản cố định': 'gain_loss_from_disposal_of_fixed_assets',
    'Lãi/(lỗ) từ hoạt động đầu tư': 'gain_loss_from_investment_activities',
    'Chi phí lãi vay': 'interest_expense',
    'Thu lãi và cổ tức': 'interest_and_dividend_received',
    'Các khoản điều chỉnh khác': 'other_adjustments',
    '(Tăng)/giảm các khoản phải thu': 'increase_decrease_in_accounts_receivable',
    '(Tăng)/giảm hàng tồn kho': 'increase_decrease_in_inventory',
    'Tăng/(giảm) các khoản phải trả': 'increase_decrease_in_accounts_payable',
    '( Tăng)/giảm chi phí trả trước': 'increase_decrease_in_prepaid_expenses',
    '(Tăng)/giảm chi phí trả trước': 'increase_decrease_in_prepaid_expenses',
    '(Tăng)/giảm chứng khoán kinh doanh': 'increase_decrease_in_trading_securities',
    'Chi phí lãi vay đã trả': 'interest_paid',
    'Thuế thu nhập doanh nghiệp đã trả': 'income_tax_paid',
    'Tiền thu khác từ các hoạt động kinh doanh': 'other_cash_receipts_from_operating_activities',
    'Tiền chi khác từ các hoạt động kinh doanh': 'other_cash_payments_from_operating_activities',
    'Lưu chuyển tiền tệ ròng từ hoạt động đầu tư': 'net_cash_flow_from_investing_activities',
    'Tiền mua tài sản cố định và các tài sản dài hạn khác': 'cash_paid_for_purchase_of_fixed_assets_and_other_long_term_assets',
    'Tiền thu được từ thanh lý tài sản cố định': 'cash_received_from_disposal_of_fixed_assets',
    'Tiền cho vay hoặc mua công cụ nợ': 'cash_loaned_or_advances_made',
    'Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ': 'cash_received_from_loans_or_advances',
    'Đầu tư vào các doanh nghiệp khác': 'investment_in_other_enterprises',
    'Tiền thu từ việc bán các khoản đầu tư vào các doanh nghiệp khác': 'cash_received_from_sale_of_investments_in_other_enterprises',
    'Cổ tức và tiền lãi nhận được': 'dividends_and_interest_received',
    'Lưu chuyển tiền tệ từ hoạt động tài chính': 'net_cash_flow_from_financing_activities',
    'Tiền thu từ phát hành cổ phiếu và vốn góp': 'cash_received_from_issuance_of_shares_and_contributions',
    'Chi trả cho việc mua lại, trả lại cổ phiếu': 'cash_paid_for_repurchase_or_return_of_shares',
    'Tiền thu được các khoản đi vay': 'cash_received_from_borrowings',
    'Tiển trả các khoản đi vay': 'cash_repayments_of_borrowings',
    'Tiền thanh toán vốn gốc đi thuê tài chính': 'cash_payments_of_principal_under_lease_financing',
    'Cổ tức đã trả': 'dividends_paid',
    'Tiền lãi đã nhận': 'interest_received',
    'Lưu chuyển tiền thuần trong kỳ': 'net_cash_flow_for_the_period',
    'Tiền và tương đương tiền đầu kỳ': 'cash_and_cash_equivalents_at_the_beginning_of_the_period',
    'Ảnh hưởng của chênh lệch tỷ giá': 'effect_of_exchange_rate_changes',
    'Tiền và tương đương tiền cuối kỳ': 'cash_and_cash_equivalents_at_the_end_of_the_period'
}


# Specify the file name for saving the CSV data
csv_file = 'data.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())

    # Write the header (field names)
    writer.writeheader()

    # Write the data
    for row in zip(*data.values()):
        writer.writerow(dict(zip(data.keys(), row)))
                        
print("hi")