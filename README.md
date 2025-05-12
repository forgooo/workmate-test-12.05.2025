# workmate-test-12.05.2025

Особенности реализации:
  -Поддержка различных названий столбцов с зарплатой (hourly_rate, rate, salary)
  
  -Обработка пустых файлов и ошибок формата
  
  -Гибкая архитектура для добавления новых типов отчетов
  
  -Четкое форматирование вывода с выравниванием колонок
  
  -Подробные сообщения об ошибках
  

Использование
Базовый синтаксис
  python main.py файл1.csv [файл2.csv ...] --report REPORT_TYPE [--output FILENAME]
  
Примеры команд
Сформировать отчет по выплатам и вывести в консоль:
  python main.py employees.csv --report payout
  
Сформировать отчет и сохранить в файл:
  python main.py data1.csv data2.csv --report payout --output report (создаст файл report.csv)

![image](https://github.com/user-attachments/assets/911adbdc-c57f-4980-b8b1-0a2e240743a8)
