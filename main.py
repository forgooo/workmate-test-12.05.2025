import argparse
from typing import List, Dict, Any, Callable
from collections import defaultdict


class EmployeeData:
    def __init__(self, id: str, email: str, name: str, department: str, hours_worked: str, hourly_rate: str):
        self.id = id
        self.email = email
        self.name = name
        self.department = department
        self.hours_worked = float(hours_worked)
        self.hourly_rate = float(hourly_rate)


def read_csv_file(file_path: str) -> List[EmployeeData]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if not lines:
        raise ValueError(f"Файл {file_path} пустой")
    
    headers = [header.strip() for header in lines[0].split(',')]
    rate_aliases = ['hourly_rate', 'rate', 'salary']
    rate_header = next((h for h in headers if h in rate_aliases), None)
    
    if not rate_header:
        raise ValueError(f"Нет нужной колонки в {file_path}")
    
    data = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(',')]
        if len(values) != len(headers):
            continue
        
        record = dict(zip(headers, values))
        try:
            employee = EmployeeData(
                id=record['id'],
                email=record['email'],
                name=record['name'],
                department=record['department'],
                hours_worked=record['hours_worked'],
                hourly_rate=record[rate_header]
            )
            data.append(employee)
        except KeyError as e:
            raise ValueError(f"Отсутсвует колонка в {file_path}: {e}")
    
    return data


def generate_payout_report(employees: List[EmployeeData]) -> str:
    employees_sorted = sorted(employees, key=lambda x: x.department)
    departments = defaultdict(list)
    for employee in employees_sorted:
        departments[employee.department].append(employee)
    report_lines = []
    total_payout = 0.0
    report_lines.append(f"{'Отдел':<15} {'Имя':<20} {'Часы':>10} {'Ставка':>10} {'Выплата':>15}") # можно доделать автоформацию по длинне
    report_lines.append("-" * 70)
    
    for department, dept_employees in departments.items():
        report_lines.append(f"Отдел: {department}")
        dept_total = 0.0
        
        for emp in dept_employees:
            payout = emp.hours_worked * emp.hourly_rate
            dept_total += payout
            report_lines.append(
                f"{'':<15} {emp.name:<20} {emp.hours_worked:>10.1f} "
                f"{emp.hourly_rate:>10.2f} {payout:>15.2f}"
            )
        report_lines.append(f"{'':<15} {'Итого по отделу:':<20} {'':>20} {dept_total:>15.2f}")
        report_lines.append("-" * 70)
        total_payout += dept_total
    report_lines.append(f"{'':<15} {'ОБЩИЙ ИТОГ:':<20} {'':>20} {total_payout:>15.2f}")
    
    return '\n'.join(report_lines)


REPORT_GENERATORS = {
    'payout': generate_payout_report
}


def save_report_to_csv(report: str, output_file: str):
    with open(output_file, 'w') as f:
        f.write(report)


def main():
    parser = argparse.ArgumentParser(description='Generate employee reports.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                      help='CSV files')
    parser.add_argument('--report', type=str, required=True,
                      help='Тип отчёта')
    parser.add_argument('--output', type=str, required=False,
                      help='Название файла, куда записать отчёт')
    
    args = parser.parse_args()
    
    if args.report not in REPORT_GENERATORS:
        print(f"Доступные отчеты: {', '.join(REPORT_GENERATORS.keys())}")
        return
    
    all_employees = []
    for file_path in args.files:
        try:
            employees = read_csv_file(file_path)
            all_employees.extend(employees)
        except Exception as e:
            print(f"Ошибка чтения {file_path}: {e}")
            return
    
    if not all_employees:
        print("Нет данных для генерации отчета")
        return
    
    report_generator = REPORT_GENERATORS[args.report] # a
    report = report_generator(all_employees)
    
    if args.output:
        output_file = f"{args.output}.csv"
        save_report_to_csv(report, output_file)
        print(f"Отчет сохранен в {output_file}")
    else:
        print(report)


if __name__ == '__main__':
    main()