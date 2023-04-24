import os
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
import uuid
from django.conf import settings
import re


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def upload_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s.%s" % (timezone.now(), instance.station.name, instance.created_by, ext)
    return os.path.join('uploads/receipts/', filename)


def add_months(created_on, num_months):
    # Get today's date
    # today = datetime.now()
    today = created_on

    # Add the specified number of months to the date
    new_month = today.month + num_months
    new_year = today.year + new_month // 12
    new_month = new_month % 12

    if new_month == 0:
        new_year -= 1
        new_month = 12
    new_date = datetime(new_year, new_month, today.day)
    return new_date

def num_length(num):
    return len(str(num))

def remove_leading_zero_and_prefix(number):
    number = str(number)
    if number[0] == "0":
        number = number[1:]
    number = "+254" + number
    return number

def contains_254(number):
    return "+254" in str(number)

def starts_with_zero(num):
    return str(num).startswith("0")

def generate_transaction_uuid():
    transaction_uuid = uuid.uuid4()
    return transaction_uuid

def formate_date_time(date_obj):
    clean_date = re.sub(r'\b(?:midnight|noon|[ap]\.m\.|,)\b', '', date_obj).strip()
    clean_date = clean_date.rstrip(',')
    formats = ['%B %d, %Y', '%d %b, %Y', '%d. %b, %Y']
    
    for fmt in formats:
         try:
            created_on = datetime.strptime(clean_date, fmt)
            break
         except ValueError:
            pass
    else:
        print("Could not parse date")
    
    return created_on




# USE als_expense;
# DELIMITER // ;
# CREATE PROCEDURE `sp_update_user`(IN usr_id INT, IN user_username varchar(20), IN user_first_name  varchar(20), IN user_last_name varchar(20), IN user_email varchar(20), IN g_id INT)
# BEGIN
# 	UPDATE auth_user SET username = user_username, first_name = user_first_name, last_name = user_last_name, email = user_email WHERE id = usr_id;
#     DELETE FROM auth_user_groups WHERE user_id = usr_id;
#     INSERT INTO auth_user_groups  (user_id, group_id) VALUES (usr_id, g_id);
# END 


            
""" DELIMITER // 
CREATE PROCEDURE `sp_delete_user` (IN usr_id INT)
BEGIN
	DELETE FROM auth_user_groups WHERE user_id = usr_id;
    DELETE FROM api_userprofile WHERE user_id = usr_id;
    DELETE FROM auth_user WHERE id = usr_id;
END
 """


# USE als_expense;
# DELIMITER // ;
# CREATE PROCEDURE `sp_float_vs_expense_amount` ()
# BEGIN
# 	SELECT id, expense_station.name, 
#     (SELECT COALESCE(SUM(expense_float.amount), 0) from expense_float WHERE expense_float.station_id = expense_station.id) as float_sum, 
#     (SELECT COALESCE(SUM(expense_expense.amount), 0) from expense_expense WHERE expense_expense.station_id =  expense_station.id AND expense_expense.created_on = DATE(NOW())) 
#     as expense_sum FROM expense_station; 
# END


# USE als_expense;
# DELIMITER // ;
# CREATE PROCEDURE `sp_update_profile`(IN usr_id INT, IN user_username varchar(20), IN user_first_name  varchar(20), IN user_last_name varchar(20), IN user_email varchar(20))
# BEGIN
# 	UPDATE auth_user SET username = user_username, first_name = user_first_name, last_name = user_last_name, email = user_email WHERE id = usr_id;
# END 


""" DELIMITER $$
CREATE PROCEDURE sp_loan_per_month(IN start_date DATE, IN end_date DATE)
BEGIN
    SELECT 
    DATE_FORMAT(created_on, '%b') as month, 
    SUM(total) as total_amount
    FROM api_loan
    WHERE created_on BETWEEN start_date AND end_date
    GROUP BY MONTH(created_on)
    ;
END$$
DELIMITER ; """




# DELIMITER //
# CREATE PROCEDURE sp_loan_per_year()
# BEGIN
#     SELECT 
#     YEAR(created_on) as year, 
#     SUM(total) as total_amount
#     FROM api_loan
#     GROUP BY YEAR(created_on);
# END 


"""
DELIMITER //
CREATE PROCEDURE sp_get_unpaid_loans()
BEGIN
    SELECT api_loan.*,
           MAX(api_payments.created_on) AS last_payment_date,
           CASE
               WHEN DATEDIFF(NOW(), MAX(api_payments.created_on)) <= 30 THEN 'Within 30 days'
               WHEN DATEDIFF(NOW(), MAX(api_payments.created_on)) <= 60 THEN 'Within 60 days'
               WHEN DATEDIFF(NOW(), MAX(api_payments.created_on)) <= 90 THEN 'Within 90 days'
               ELSE 'Over 90 days'
           END AS payment_due,
           SUM(api_payments.paid) AS total_amount_paid,
           ROUND(api_loan.total / api_loan.months, 2) AS expected_monthly_payment,
           
           auth_user.first_name,
           auth_user.last_name
    FROM api_loan
             LEFT JOIN api_payments ON api_loan.id = api_payments.loan_id
             LEFT JOIN api_loanfee ON api_loan.loan_fees_id = api_loanfee.id
             LEFT JOIN auth_user ON api_loanfee.member_id = auth_user.id
    WHERE api_loan.is_paid = 0
    GROUP BY api_loan.id;
  
  END //
DELIMITER ;

"""

"""
CREATE TRIGGER `update_fines` AFTER INSERT ON `api_fines`
 FOR EACH ROW BEGIN
  DECLARE total_fines DECIMAL(10,2);
  
  SELECT SUM(amount) INTO total_fines
  FROM api_fines
  WHERE is_paid = False AND
  loan_id = NEW.loan_id;
  
  UPDATE api_loan
  SET fines = total_fines,
      total = total + total_fines,
      balance = balance + total_fines
  WHERE id = NEW.loan_id;
END

CREATE TRIGGER `update_loan_counters` AFTER INSERT ON `api_loan`
 FOR EACH ROW BEGIN

    SET @s_loans = (SELECT COUNT(*) FROM api_loan WHERE is_deleted = 0);
    SET @s_paid_loans = (SELECT SUM(total) AS total_sum FROM api_loan WHERE is_paid = 1);
    SET @s_unpaid_loans = (SELECT SUM(total) AS total_sum FROM api_loan WHERE is_paid = 0);
    SET @l_this_month = (SELECT SUM(total) AS total__sum FROM api_loan WHERE MONTH(created_on) = MONTH(NOW())AND is_deleted = 0);
    set @l_last_month = (SELECT SUM(total) AS total__sum FROM api_loan WHERE YEAR(created_on) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(created_on) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) AND is_deleted = 0);
    SET @l_this_year = (SELECT SUM(total) AS total__sum FROM api_loan WHERE YEAR(created_on) = YEAR(CURRENT_DATE) AND is_deleted = 0);
    SET @l_last_year = (SELECT SUM(total) AS total__sum FROM api_loan WHERE YEAR(created_on) = YEAR(CURRENT_DATE - INTERVAL 1 YEAR) AND is_deleted = 0);
    SET @t_loan = (SELECT SUM(total) AS total__sum FROM api_loan);
    SET @updated_on = NOW();

    UPDATE api_counter SET
        s_paid_loans = @s_paid_loans,
        s_unpaid_loans = @s_unpaid_loans,
        s_loans = @s_loans,
        l_this_month = @l_this_month,
        l_last_month = @l_last_month,
        l_this_year = @l_this_year,
        l_last_year = @l_last_year,
        t_loan = @t_loan,
        updated_on = @updated_on WHERE id = 1;
END

CREATE TRIGGER `update_loan_counters1` AFTER INSERT ON `api_payments`
 FOR EACH ROW BEGIN

    SET @s_loans = (SELECT COUNT(*) FROM api_loan WHERE is_deleted = 0);
    SET @s_paid_loans = (SELECT SUM(total) AS total_sum FROM api_loan WHERE is_paid = 1);
    SET @s_unpaid_loans = (SELECT SUM(total) AS total_sum FROM api_loan WHERE is_paid = 0);
    SET @l_this_month = (SELECT SUM(total) AS total__sum FROM api_loan WHERE MONTH(created_on) = MONTH(NOW())AND is_deleted = 0);
    set @l_last_month = (SELECT SUM(total) AS total__sum FROM api_loan WHERE YEAR(created_on) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(created_on) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) AND is_deleted = 0);
    SET @l_this_year = (SELECT SUM(total) AS total__sum FROM api_loan WHERE YEAR(created_on) = YEAR(CURRENT_DATE) AND is_deleted = 0);
    SET @l_last_year = (SELECT SUM(total) AS total__sum FROM api_loan WHERE YEAR(created_on) = YEAR(CURRENT_DATE - INTERVAL 1 YEAR) AND is_deleted = 0);
    SET @t_loan = (SELECT SUM(total) AS total__sum FROM api_loan);
    SET @updated_on = NOW();

    UPDATE api_counter SET
        s_paid_loans = @s_paid_loans,
        s_unpaid_loans = @s_unpaid_loans,
        s_loans = @s_loans,
        l_this_month = @l_this_month,
        l_last_month = @l_last_month,
        l_this_year = @l_this_year,
        l_last_year = @l_last_year,
        t_loan = @t_loan,
        updated_on = @updated_on WHERE id = 1;
END

CREATE TRIGGER `update_registration_counters` AFTER INSERT ON `api_registration`
 FOR EACH ROW BEGIN
    SET @s_members = (SELECT COUNT(group_id) FROM auth_user_groups INNER JOIN auth_group ON auth_user_groups.group_id = auth_group.id WHERE auth_group.name = 'Member' GROUP BY group_id);
    SET @s_paid_reg = (SELECT COUNT(*) FROM api_registration WHERE is_deleted = 0);
    SET @s_unpaid_reg =  (@s_members -  @s_paid_reg);
    SET @updated_on = NOW();

    UPDATE api_counter SET
        s_paid_reg = @s_paid_reg,
        s_unpaid_reg = @s_unpaid_reg,
        updated_on = @updated_on WHERE id = 1;
END

CREATE TRIGGER `update_user_counters` AFTER INSERT ON `auth_user`
 FOR EACH ROW BEGIN
    SET @s_members = (SELECT COUNT(group_id) FROM auth_user_groups INNER JOIN auth_group ON auth_user_groups.group_id = auth_group.id WHERE auth_group.name = 'Member' GROUP BY group_id);
    SET @s_users = (SELECT COUNT(group_id) FROM auth_user_groups INNER JOIN auth_group ON auth_user_groups.group_id = auth_group.id WHERE auth_group.name != 'Member' GROUP BY group_id);
    SET @s_active_users = (SELECT COALESCE(COUNT(*), 0) FROM (SELECT auth_group.id FROM auth_user_groups INNER JOIN auth_group ON auth_user_groups.group_id = auth_group.id INNER JOIN auth_user ON auth_user_groups.user_id = auth_user.id WHERE auth_user.is_active = 1 AND auth_user.is_superuser = 0 AND auth_group.name != 'Member'  GROUP BY auth_group.id) AS subquery);
    SET @s_inactive_users = (SELECT COALESCE(COUNT(*), 0) FROM (SELECT auth_group.id FROM auth_user_groups INNER JOIN auth_group ON auth_user_groups.group_id = auth_group.id INNER JOIN auth_user ON auth_user_groups.user_id = auth_user.id WHERE auth_user.is_active = 0 AND auth_user.is_superuser = 0 AND auth_group.name != 'Member' GROUP BY auth_group.id) AS subquery);
    SET @updated_on = NOW();

    UPDATE api_counter SET
        s_members = @s_members,
        s_users = @s_users,
        s_active_users = @s_active_users,
        s_inactive_users = @s_inactive_users,
        updated_on = @updated_on WHERE id = 1;
END


"""