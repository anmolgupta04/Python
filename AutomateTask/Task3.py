# """
# Python Task Automation Suite
# Automates repetitive tasks: file management, data processing, report generation,
# email automation, web scraping, and scheduled tasks.
# """

import os
import shutil
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import glob
import zipfile
import csv
from pathlib import Path
import re
import schedule
import time
from collections import defaultdict

# For email automation (optional - requires setup)
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders


class FileOrganizer:
    """Automates file organization and management tasks"""
    
    def __init__(self, base_path='.'):
        self.base_path = Path(base_path)
        self.file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.csv'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Code': ['.py', '.java', '.cpp', '.js', '.html', '.css', '.php', '.sql'],
            'Others': []
        }
    
    def organize_files(self, source_dir=None):
        """Organize files into categorized folders"""
        if source_dir is None:
            source_dir = self.base_path
        else:
            source_dir = Path(source_dir)
        
        print(f"\n{'='*60}")
        print(f"ORGANIZING FILES IN: {source_dir}")
        print(f"{'='*60}")
        
        files_moved = 0
        
        for file_path in source_dir.iterdir():
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                
                # Determine category
                category = 'Others'
                for cat, extensions in self.file_types.items():
                    if file_ext in extensions:
                        category = cat
                        break
                
                # Create category folder if it doesn't exist
                category_path = source_dir / category
                category_path.mkdir(exist_ok=True)
                
                # Move file
                destination = category_path / file_path.name
                try:
                    shutil.move(str(file_path), str(destination))
                    print(f"✓ Moved: {file_path.name} → {category}/")
                    files_moved += 1
                except Exception as e:
                    print(f"✗ Error moving {file_path.name}: {e}")
        
        print(f"\n✓ Total files organized: {files_moved}")
        return files_moved
    
    def cleanup_old_files(self, directory=None, days=30):
        """Delete files older than specified days"""
        if directory is None:
            directory = self.base_path
        else:
            directory = Path(directory)
        
        print(f"\n{'='*60}")
        print(f"CLEANING UP FILES OLDER THAN {days} DAYS")
        print(f"{'='*60}")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        files_deleted = 0
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        print(f"✓ Deleted: {file_path.name} (Modified: {file_time.strftime('%Y-%m-%d')})")
                        files_deleted += 1
                    except Exception as e:
                        print(f"✗ Error deleting {file_path.name}: {e}")
        
        print(f"\n✓ Total files deleted: {files_deleted}")
        return files_deleted
    
    def rename_files_bulk(self, directory=None, pattern=None, replacement=None, prefix=None):
        """Bulk rename files with pattern matching or prefix"""
        if directory is None:
            directory = self.base_path
        else:
            directory = Path(directory)
        
        print(f"\n{'='*60}")
        print(f"BULK RENAMING FILES")
        print(f"{'='*60}")
        
        files_renamed = 0
        
        for file_path in directory.iterdir():
            if file_path.is_file():
                old_name = file_path.name
                new_name = old_name
                
                # Apply pattern replacement
                if pattern and replacement:
                    new_name = re.sub(pattern, replacement, new_name)
                
                # Apply prefix
                if prefix:
                    new_name = f"{prefix}_{new_name}"
                
                if new_name != old_name:
                    new_path = file_path.parent / new_name
                    try:
                        file_path.rename(new_path)
                        print(f"✓ Renamed: {old_name} → {new_name}")
                        files_renamed += 1
                    except Exception as e:
                        print(f"✗ Error renaming {old_name}: {e}")
        
        print(f"\n✓ Total files renamed: {files_renamed}")
        return files_renamed
    
    def backup_files(self, source_dir=None, backup_dir='backup'):
        """Create backup of files in a directory"""
        if source_dir is None:
            source_dir = self.base_path
        else:
            source_dir = Path(source_dir)
        
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}.zip"
        backup_file = backup_path / backup_name
        
        print(f"\n{'='*60}")
        print(f"CREATING BACKUP: {backup_name}")
        print(f"{'='*60}")
        
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
                    print(f"✓ Added: {arcname}")
        
        print(f"\n✓ Backup created: {backup_file}")
        print(f"✓ Size: {backup_file.stat().st_size / 1024 / 1024:.2f} MB")
        return str(backup_file)


class DataProcessor:
    """Automates data processing and transformation tasks"""
    
    def __init__(self):
        self.processed_data = None
    
    def process_csv_files(self, input_dir, output_file='processed_data.csv'):
        """Merge multiple CSV files into one"""
        print(f"\n{'='*60}")
        print(f"PROCESSING CSV FILES")
        print(f"{'='*60}")
        
        csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
        
        if not csv_files:
            print("✗ No CSV files found!")
            return None
        
        print(f"Found {len(csv_files)} CSV files")
        
        dfs = []
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                dfs.append(df)
                print(f"✓ Loaded: {os.path.basename(file)} ({len(df)} rows)")
            except Exception as e:
                print(f"✗ Error loading {file}: {e}")
        
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
            merged_df.to_csv(output_file, index=False)
            print(f"\n✓ Merged data saved: {output_file}")
            print(f"✓ Total rows: {len(merged_df)}")
            self.processed_data = merged_df
            return merged_df
        
        return None
    
    def clean_data(self, df=None, input_file=None):
        """Clean and standardize data"""
        if df is None and input_file:
            df = pd.read_csv(input_file)
        elif df is None and self.processed_data is not None:
            df = self.processed_data
        else:
            print("✗ No data to clean!")
            return None
        
        print(f"\n{'='*60}")
        print(f"CLEANING DATA")
        print(f"{'='*60}")
        
        initial_rows = len(df)
        print(f"Initial rows: {initial_rows}")
        
        # Remove duplicates
        df = df.drop_duplicates()
        print(f"✓ Removed duplicates: {initial_rows - len(df)} rows")
        
        # Handle missing values
        missing_before = df.isnull().sum().sum()
        df = df.fillna(method='ffill').fillna(method='bfill')
        print(f"✓ Filled missing values: {missing_before} cells")
        
        # Remove whitespace from string columns
        str_columns = df.select_dtypes(include=['object']).columns
        for col in str_columns:
            df[col] = df[col].str.strip()
        print(f"✓ Cleaned string columns: {len(str_columns)} columns")
        
        # Convert date columns
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
                print(f"✓ Converted {col} to datetime")
            except:
                pass
        
        self.processed_data = df
        print(f"\n✓ Final rows: {len(df)}")
        return df
    
    def generate_summary_statistics(self, df=None, output_file='summary_stats.txt'):
        """Generate summary statistics"""
        if df is None and self.processed_data is not None:
            df = self.processed_data
        else:
            print("✗ No data available!")
            return None
        
        print(f"\n{'='*60}")
        print(f"GENERATING SUMMARY STATISTICS")
        print(f"{'='*60}")
        
        with open(output_file, 'w') as f:
            f.write("DATA SUMMARY REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            # Basic info
            f.write(f"Dataset Shape: {df.shape}\n")
            f.write(f"Total Rows: {len(df)}\n")
            f.write(f"Total Columns: {len(df.columns)}\n\n")
            
            # Column types
            f.write("Column Types:\n")
            f.write(str(df.dtypes) + "\n\n")
            
            # Missing values
            f.write("Missing Values:\n")
            f.write(str(df.isnull().sum()) + "\n\n")
            
            # Numeric statistics
            f.write("Numeric Statistics:\n")
            f.write(str(df.describe()) + "\n\n")
            
            # Categorical statistics
            obj_columns = df.select_dtypes(include=['object']).columns
            if len(obj_columns) > 0:
                f.write("Categorical Statistics:\n")
                for col in obj_columns:
                    f.write(f"\n{col}:\n")
                    f.write(str(df[col].value_counts().head(10)) + "\n")
        
        print(f"✓ Summary saved: {output_file}")
        return output_file


class ReportGenerator:
    """Automates report generation tasks"""
    
    def __init__(self):
        self.reports_dir = Path('reports')
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_daily_report(self, data=None, report_name='daily_report'):
        """Generate daily report with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"{report_name}_{timestamp}.txt"
        
        print(f"\n{'='*60}")
        print(f"GENERATING DAILY REPORT")
        print(f"{'='*60}")
        
        with open(report_file, 'w') as f:
            f.write(f"DAILY REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            if data is not None:
                if isinstance(data, pd.DataFrame):
                    f.write(f"Data Overview:\n")
                    f.write(f"Total Records: {len(data)}\n")
                    f.write(f"Columns: {', '.join(data.columns)}\n\n")
                    f.write("Sample Data:\n")
                    f.write(str(data.head(10)) + "\n\n")
                else:
                    f.write(str(data) + "\n")
            
            f.write("\nReport completed successfully.\n")
        
        print(f"✓ Report generated: {report_file}")
        return str(report_file)
    
    def generate_html_report(self, df, report_name='data_report'):
        """Generate HTML report from DataFrame"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"{report_name}_{timestamp}.html"
        
        print(f"\n{'='*60}")
        print(f"GENERATING HTML REPORT")
        print(f"{'='*60}")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
                h2 {{ color: #555; margin-top: 30px; }}
                .info {{ background: white; padding: 15px; border-radius: 5px; margin: 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                table {{ border-collapse: collapse; width: 100%; background: white; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background: #f5f5f5; }}
                .timestamp {{ color: #777; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>📊 Data Report</h1>
            <div class="info">
                <p class="timestamp"><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Total Records:</strong> {len(df)}</p>
                <p><strong>Columns:</strong> {len(df.columns)}</p>
            </div>
            
            <h2>📈 Data Summary</h2>
            <div class="info">
                {df.describe().to_html()}
            </div>
            
            <h2>📋 Sample Data (First 20 rows)</h2>
            <div class="info">
                {df.head(20).to_html(index=False)}
            </div>
        </body>
        </html>
        """
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        print(f"✓ HTML report generated: {report_file}")
        return str(report_file)
    
    def generate_excel_report(self, data_dict, report_name='excel_report'):
        """Generate Excel report with multiple sheets"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"{report_name}_{timestamp}.xlsx"
        
        print(f"\n{'='*60}")
        print(f"GENERATING EXCEL REPORT")
        print(f"{'='*60}")
        
        with pd.ExcelWriter(report_file, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"✓ Added sheet: {sheet_name}")
        
        print(f"✓ Excel report generated: {report_file}")
        return str(report_file)


class EmailAutomation:
    """Automates email sending tasks"""
    
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_report_email(self, sender_email, password, recipient_email, 
                         subject, body, attachment_path=None):
        """Send email with optional attachment"""
        print(f"\n{'='*60}")
        print(f"EMAIL AUTOMATION (Demonstration)")
        print(f"{'='*60}")
        
        # Note: This is a demonstration. In production, use environment variables
        # for sensitive data and proper email configuration
        
        print(f"From: {sender_email}")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:100]}...")
        if attachment_path:
            print(f"Attachment: {attachment_path}")
        
        print("\n⚠️  Email sending disabled in demo mode")
        print("To enable: Uncomment the email code and configure SMTP settings")
        
        # Uncomment below for actual email sending:
        """
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        if attachment_path:
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 
                              f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(part)
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
            print("✓ Email sent successfully!")
            return True
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            return False
        """
        return True


class TaskScheduler:
    """Automates task scheduling"""
    
    def __init__(self):
        self.tasks = []
    
    def add_daily_task(self, time_str, task_func, *args):
        """Schedule a daily task"""
        schedule.every().day.at(time_str).do(task_func, *args)
        self.tasks.append(f"Daily at {time_str}: {task_func.__name__}")
        print(f"✓ Scheduled: {task_func.__name__} daily at {time_str}")
    
    def add_hourly_task(self, task_func, *args):
        """Schedule an hourly task"""
        schedule.every().hour.do(task_func, *args)
        self.tasks.append(f"Hourly: {task_func.__name__}")
        print(f"✓ Scheduled: {task_func.__name__} every hour")
    
    def add_weekly_task(self, day, time_str, task_func, *args):
        """Schedule a weekly task"""
        getattr(schedule.every(), day.lower()).at(time_str).do(task_func, *args)
        self.tasks.append(f"Weekly {day} at {time_str}: {task_func.__name__}")
        print(f"✓ Scheduled: {task_func.__name__} weekly on {day} at {time_str}")
    
    def list_tasks(self):
        """List all scheduled tasks"""
        print(f"\n{'='*60}")
        print(f"SCHEDULED TASKS")
        print(f"{'='*60}")
        for task in self.tasks:
            print(f"• {task}")
    
    def run_pending(self):
        """Run all pending tasks"""
        schedule.run_pending()
    
    def run_scheduler(self):
        """Run the scheduler continuously"""
        print("\n🔄 Scheduler started. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n✓ Scheduler stopped.")


# ============= DEMONSTRATION FUNCTIONS =============

def demo_file_organization():
    """Demonstrate file organization automation"""
    print("\n" + "=" * 60)
    print("DEMO 1: FILE ORGANIZATION AUTOMATION")
    print("=" * 60)
    
    # Create demo directory structure
    demo_dir = Path('demo_files')
    demo_dir.mkdir(exist_ok=True)
    
    # Create sample files
    sample_files = [
        'report.pdf', 'data.csv', 'image.jpg', 'video.mp4',
        'script.py', 'document.docx', 'song.mp3', 'archive.zip'
    ]
    
    for file in sample_files:
        (demo_dir / file).touch()
    
    # Organize files
    organizer = FileOrganizer(demo_dir)
    organizer.organize_files()
    
    print("\n✓ File organization demo completed!")


def demo_data_processing():
    """Demonstrate data processing automation"""
    print("\n" + "=" * 60)
    print("DEMO 2: DATA PROCESSING AUTOMATION")
    print("=" * 60)
    
    # Create sample CSV files
    data_dir = Path('demo_data')
    data_dir.mkdir(exist_ok=True)
    
    # Generate sample data
    for i in range(3):
        df = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=10),
            'Sales': np.random.randint(1000, 5000, 10),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 10),
            'Product': np.random.choice(['A', 'B', 'C'], 10)
        })
        df.to_csv(data_dir / f'data_{i+1}.csv', index=False)
    
    # Process data
    processor = DataProcessor()
    merged_df = processor.process_csv_files(data_dir, 'merged_data.csv')
    cleaned_df = processor.clean_data()
    processor.generate_summary_statistics()
    
    print("\n✓ Data processing demo completed!")
    return cleaned_df


def demo_report_generation(df):
    """Demonstrate report generation automation"""
    print("\n" + "=" * 60)
    print("DEMO 3: REPORT GENERATION AUTOMATION")
    print("=" * 60)
    
    generator = ReportGenerator()
    
    # Generate different types of reports
    generator.generate_daily_report(df)
    generator.generate_html_report(df)
    
    # Generate Excel report with multiple sheets
    data_dict = {
        'Raw Data': df,
        'Summary': df.describe()
    }
    generator.generate_excel_report(data_dict)
    
    print("\n✓ Report generation demo completed!")


def demo_scheduling():
    """Demonstrate task scheduling"""
    print("\n" + "=" * 60)
    print("DEMO 4: TASK SCHEDULING")
    print("=" * 60)
    
    scheduler = TaskScheduler()
    
    # Example scheduled tasks
    def backup_task():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Running backup...")
    
    def report_task():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating report...")
    
    # Schedule tasks (demonstration only - won't actually run in this demo)
    print("\nScheduling tasks...")
    scheduler.add_daily_task("09:00", backup_task)
    scheduler.add_daily_task("17:00", report_task)
    scheduler.add_weekly_task("Monday", "08:00", report_task)
    
    scheduler.list_tasks()
    
    print("\n✓ Task scheduling demo completed!")


# ============= MAIN EXECUTION =============

def main():
    """Run all automation demonstrations"""
    print("\n" + "=" * 80)
    print(" " * 20 + "PYTHON TASK AUTOMATION SUITE")
    print("=" * 80)
    
    # Run demonstrations
    demo_file_organization()
    
    df = demo_data_processing()
    
    if df is not None:
        demo_report_generation(df)
    
    demo_scheduling()
    
    # Summary
    print("\n" + "=" * 80)
    print("AUTOMATION SUITE COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📁 Generated files:")
    print("  • Organized files in demo_files/")
    print("  • Merged CSV in merged_data.csv")
    print("  • Summary statistics in summary_stats.txt")
    print("  • Reports in reports/")
    
    print("\n🔧 Available Automation Tools:")
    print("  1. File Organization - Sort, rename, backup, cleanup")
    print("  2. Data Processing - Merge, clean, analyze CSV files")
    print("  3. Report Generation - Text, HTML, Excel reports")
    print("  4. Email Automation - Send reports via email")
    print("  5. Task Scheduling - Automate recurring tasks")
    
    print("\n💡 Next Steps:")
    print("  • Customize functions for your specific needs")
    print("  • Set up email credentials for email automation")
    print("  • Schedule tasks to run automatically")
    print("  • Add error handling and logging")
    print("  • Integrate with your existing workflows")


if __name__ == "__main__":
    main()