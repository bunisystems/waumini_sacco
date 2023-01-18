import os
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
import uuid

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


def add_months(num_months):
    # Get today's date
    today = datetime.now()

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


# USE als_expense;
# DELIMITER // ;
# CREATE PROCEDURE `sp_update_user`(IN usr_id INT, IN user_username varchar(20), IN user_first_name  varchar(20), IN user_last_name varchar(20), IN user_email varchar(20), IN g_id INT)
# BEGIN
# 	UPDATE auth_user SET username = user_username, first_name = user_first_name, last_name = user_last_name, email = user_email WHERE id = usr_id;
#     DELETE FROM auth_user_groups WHERE user_id = usr_id;
#     INSERT INTO auth_user_groups  (user_id, group_id) VALUES (usr_id, g_id);
# END 


            
# USE als_expense;
# DELIMITER // ;
# CREATE PROCEDURE `sp_delete_user` (IN usr_id INT)
# BEGIN
# 	DELETE FROM auth_user_groups WHERE user_id = usr_id;
#     DELETE FROM auth_user WHERE id = usr_id;
# END


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