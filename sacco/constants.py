

try:
    from api.models import Settings
    
    values = Settings.objects.get(pk=1)
    values.refresh_from_db()

    SHARES_ENTRANCE_FEE = values.SHARES_ENTRANCE_FEE
    SHARES_APPLICATION_FEE = values.SHARES_APPLICATION_FEE
    SAVINGS_ENTRANCE_FEE = values.SAVINGS_ENTRANCE_FEE
    MIN_LOAN = values.MIN_LOAN 
    MAX_LOAN = values.MAX_LOAN
    CAPITAL_SHARE = values.CAPITAL_SHARE
    SHARES_MIN =values.SHARES_MIN
    ACCOUNT = values.ACCOUNT
    ACCOUNT_WITHDRAWAL = values.ACCOUNT_WITHDRAWAL
    PROCESSING_FEE = values.PROCESSING_FEE
    PASSBOOK = values.PASSBOOK
    INTEREST = values.INTEREST
    INSUARANCE = values.INSUARANCE
    PHONE_NUMBER = values.PHONE_NUMBER

except Exception as e:
    # from api.models import Settings
    
    # values = Settings.objects.get(pk=1)
    # values.refresh_from_db()

    # SHARES_ENTRANCE_FEE = values.SHARES_ENTRANCE_FEE,
    # SHARES_APPLICATION_FEE = values.SHARES_APPLICATION_FEE,
    # SAVINGS_ENTRANCE_FEE = values.SAVINGS_ENTRANCE_FEE,
    # MIN_LOAN = values.MIN_LOAN 
    # MAX_LOAN = values.MAX_LOAN
    # CAPITAL_SHARE = values.CAPITAL_SHARE
    # SHARES_MIN =values.SHARES_MIN
    # ACCOUNT = values.ACCOUNT
    # ACCOUNT_WITHDRAWAL = values.ACCOUNT_WITHDRAWAL
    # PROCESSING_FEE = values.PROCESSING_FEE
    # PASSBOOK = values.PASSBOOK
    # INTEREST = values.INTEREST
    # INSUARANCE = values.INSUARANCE
    # PHONE_NUMBER = values.PHONE_NUMBER

    

    REGISTRATION_FEE = 0
    MIN_LOAN = 0
    MAX_LOAN = 0
    CAPITAL_SHARE = 0
    SHARES_MIN = 0
    ACCOUNT = 0
    ACCOUNT_WITHDRAWAL = 0
    PROCESSING_FEE = 0
    PASSBOOK = 0
    INTEREST = 0
    INSUARANCE = 0
    PHONE_NUMBER = 0 

    print(e)





ERROR_SEF_AMOUNT = 'Share Entrance Fee entered is not equal to KES '
ERROR_SAF_AMOUNT = 'Share Application Fee entered is not equal to KES '
ERROR_SaEF_AMOUNT = 'Savings Entrance Fee entered is not equal to KES '
ERROR_F_L_REQUIRED = 'First Name and Last Name are required '
ERROR_ID_NO_REQUIRED = 'ID Number is required '
 


ERROR_AMOUNT = 'Amount is required'
ERROR_INC_AMOUNT = 'Amount entered is not equal to KES ' 
ERROR_REG_EXISTS = 'This member has already paid registration fee'
ERROR_REG_MEMBER = 'Choose a member'
ERROR_LOAN_FEE = 'Please ensure atleast one member has paid relevant loan fees'

SUCCESS_FEE_SAVED = 'Fee saved successfully'
SUCCESS_FEE_EDITED = 'Fee edited successfully'

MEMBERS_EXIST = 'Sacco Members are required'


ERROR_CS_MONTH_PAYMENT = "'s Payment already exists"


ERROR_SHARE_MIN = 'Amount entered should be more or equal to KES '


ERROR_MIN_LOAN = 'Minimum Loan is ' + str(MIN_LOAN)
ERROR_MAX_LOAN = 'Maximum Loan is ' + str(MAX_LOAN)
LOAN_REQUIRED = 'Loan fee is required'
LOAN_DURATION = 'Duration in months is required'
LOAN_INTEREST_REQ = 'interest is required'
LOAN_INTEREST_CALC = 'An error occured calculating interest'
LOAN_INSURANCE_REQ = 'Insurance is required'
LOAN_INSURANCE_CALC = 'An error occured calculating insuarance, please refresh the page'
ERROR_LOAN_EDIT = 'This loan cannot be edited because of an existing payment'
ERROR_404 = 'This page does not exist'

MEMBER_EMAIL_EXISTS = "Something went wrong"
ERROR_PK_CONSTRAINT = "This member cannot be deleted because of existing payements and loans"



