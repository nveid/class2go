from django.core.management.base import BaseCommand, CommandError
from c2g.models import *
from django.contrib.auth.models import User,Group
from django.db import connection, transaction
from courses.reports.generation.course_dashboard import *

class Command(BaseCommand):
    help = "Get course dashboard stats.\nUsage: manage.py gen_course_dashboard_report course_handle [save_to_s3]\nIf save_to_s3 is 1, the file will be saved to s3. Otherwise, it will be output to console.\n"
        
    def handle(self, *args, **options):
        if len(args) == 0:
            print "No course handle supplied!"
            
        try:
            course = Course.objects.get(handle= args[0], mode='ready')
        except:
            print "Failed to find course with given handle"
            return
        
        save_to_s3 = False
        if len(args) > 1: save_to_s3 = True if (args[1] == '1') else False
        
        report = gen_course_dashboard_report(course, save_to_s3)
        if save_to_s3:
            if report['path']: print "Report successfully written to: %s" % report['path']
            else: print "Failed to generate report or write it to S3!"