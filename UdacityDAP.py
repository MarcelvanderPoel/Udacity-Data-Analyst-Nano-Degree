import unicodecsv
from collections import defaultdict
import numpy as np

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

# Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
def print_mean_std_min_max(engagementvar):
    total_minutes_by_account = {}
    for account_key, engagement_for_student in engagement_by_account.items():
        total_minutes = 0
        for engagement_record in engagement_for_student:
            total_minutes += engagement_record[engagementvar]
        total_minutes_by_account[account_key] = total_minutes

# Summarize the data about minutes spent in the classroom
    total_minutes = total_minutes_by_account.values()
    print engagementvar
    print 'Mean:', np.mean(total_minutes)
    print 'Standard deviation:', np.std(total_minutes)
    print 'Minimum:', np.min(total_minutes)
    print 'Maximum:', np.max(total_minutes)


#reading all files

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

print "ENROLLMENTS "+str(enrollments[0])
print len(enrollments)

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    engagement_record['account_key'] = engagement_record['acct']
    del engagement_record['acct']
    engagement_record['has_visited'] = 0
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited']=1

print "DAILY ENGAGEMENT "+str(daily_engagement[0])
print len(daily_engagement)

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

print "PROJECT SUBMISSIONS "+str(project_submissions[0])
print len(project_submissions)

unique_project_submitters = get_unique_students(project_submissions)
print 'UNIQUE PROJECT SUBMITTERS ' + str(len(unique_project_submitters))

unique_engagement_students = get_unique_students(daily_engagement)
print 'UNIQUE DAILY ENGAGERS ' + str(len(unique_engagement_students))

unique_enrolled_students = get_unique_students(enrollments)
print 'UNIQUE ENROLLERS ' + str(len(unique_enrolled_students))

# Create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])

# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print len(non_udacity_enrollments)
print len(non_udacity_engagement)
print len(non_udacity_submissions)

i=0
paid_students={}
for enrollment in non_udacity_enrollments:
    if (enrollment['days_to_cancel'] == None) or (enrollment['days_to_cancel'] > 7):

        if (enrollment['account_key'] not in paid_students or
                    enrollment['join_date'] > paid_students[enrollment['account_key']]):
            paid_students[enrollment['account_key']] = enrollment['join_date']

print len(paid_students)

engagement_records_for_paid_students=[]
for engagement in non_udacity_engagement:
    if engagement['account_key'] in paid_students:

        if within_one_week(paid_students[engagement['account_key']], engagement['utc_date']):
            engagement_records_for_paid_students.append(engagement)

print len(engagement_records_for_paid_students)

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
engagement_by_account = defaultdict(list)
for engagement_record in engagement_records_for_paid_students:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)


print_mean_std_min_max('total_minutes_visited')
print_mean_std_min_max('lessons_completed')
print_mean_std_min_max('has_visited')